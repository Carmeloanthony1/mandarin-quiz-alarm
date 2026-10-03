import datetime
import os
import subprocess
import time
from dotenv import load_dotenv
import requests

load_dotenv()
DC_WEBHOOK_URL = os.getenv("discord_bot")
AUDIO_FILE = "./assets/alarm.mp3"

# Variabel global untuk menyimpan referensi proses mpv
player_process = None


def notification_discord(judul_notif, pesan):
    """ngirim notif lewat discord"""
    if not DC_WEBHOOK_URL:
        print("ERROR: DC_WEBHOOK_URL TIDAK DI TEMUKAN DI ENV")
        return

    payload = {
        "username": "Alarm Bot",
        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4whOBKg3khP5cqAV90Y-N77-sdxyarrKCwJMdzLZkZA&s=10",
        "embeds": [
            {
                "title": f"{judul_notif}",
                "description": pesan,
                "color": 15158332,
                "timestamp": datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat(),
            }
        ],
    }

    try:
        response = requests.post(DC_WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code in [200, 204]:
            print("[STATUS] : Notifikasi berhasil terkirim")
        else:
            print("[STATUS] : Notifikasi gagal terkirim")
    except Exception as e:
        print(f"Error Discord : {e}")


def playsound():
    """Memutar lagu secara berulang di background (Non-blocking)"""
    global player_process
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_audio = os.path.join(base_dir, "assets", "alarm.mp3")

    if os.path.exists(path_audio):
        # Pakai Popen supaya mpv jalan di background tanpa menahan skrip Python
        player_process = subprocess.Popen(
            ["mpv", "--no-video", "--loop=inf", path_audio],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("[STATUS] : Berhasil play alarm (looping)")
    else:
        print(f"[STATUS] : Gagal play alarm, file tidak ditemukan di {path_audio}")


def stopsound():
    """Menghentikan pemutar mpv"""
    global player_process

    if player_process:
        player_process.terminate()
        player_process = None

    subprocess.run(
        ["killall", "mpv"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("[STATUS] : Suara alarm berhasil dimatikan")


def input_waktu():
    print("PENGATURAN WAKTU")
    while True:
        try:
            jam = int(input("Masukan jam (0-23) : "))
            menit = int(input("Masukan menit (0-59) : "))
            if 0 <= jam <= 23 and 0 <= menit <= 59:
                sekarang = datetime.datetime.now()
                target_alarm = sekarang.replace(
                    hour=jam, minute=menit, second=0, microsecond=0
                )

                if target_alarm <= sekarang:
                    target_alarm += datetime.timedelta(days=1)

                print(f"Waktu alarm di set pada {jam:02d}:{menit:02d} WIB")

                format_waktu = target_alarm.strftime("%H:%M")
                judul_notif = f"ALARM DI SET PADA PUKUL {format_waktu} WIB"
                pesan = f"anda akan di bangunkan pukul {format_waktu} WIB"
                notification_discord(judul_notif, pesan)

                return target_alarm
            else:
                print(
                    "[STATUS] : Jam harus 0-23 dan menit harus 0-59! Coba lagi.\n"
                )

        except ValueError:
            print("[STATUS] : Input harus berupa angka! coba lagi.\n")


def jalankan_alarm(target_alarm):
    print("[STATUS] Menunggu waktu alarm (CTRL + C untuk membatalkan)")
    while True:
        sekarang = datetime.datetime.now()
        if sekarang >= target_alarm:
            print("[STATUS] BANGONNN!!!!!")
            format_waktu = target_alarm.strftime("%H:%M")
            judul_notif = f"WAKTUNYA BANGUN! {format_waktu}"
            pesan = "Selesaikan 3 pertanyaan ini untuk membuka HP"
            notification_discord(judul_notif, pesan)

            playsound()

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                stopsound()
                print(
                    "[STATUS] : Alarm berhasil di matikan, selamat beraktivitas"
                )
                break

        time.sleep(2)

if __name__ == "__main__":
    target = input_waktu()
    jalankan_alarm(target)