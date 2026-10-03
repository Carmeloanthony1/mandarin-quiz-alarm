import time
import datetime
import os

def notification_termux(title, pesan):
    """ngirimin notifikasi lokal ke hp secara offline lewat termux"""
    os.system(
        f'termux-notification -t "{title}" -c "{pesan}" --priority high'
    )
    #pada bagian ini, kita kasih title nya nanti sesuai dengan urgensi yang di perlukan
    # -c itu pesan 
    #--priority high itu biar notifikasi kita ada di paling atas

def input_waktu():
    print("PENGATURAN WAKTU")
    while True:
        try:
            jam = int(input("Masukan jam (0-23) : "))
            menit = int(input("Masukan menit (0-59) : "))
            if 0 <= jam <= 23 and 0 <= menit <= 59:
                sekarang = datetime.datetime.now() 
                """
                ngambil waktu sekarang sekaligus sama tanggal, setelah sudah di set
                """
                target_alarm = sekarang.replace(hour = jam, minute = menit, second = 0, microsecond = 0)

                if (target_alarm <= sekarang):
                    target_alarm += datetime.timedelta(days=1)
                
                """
                kalau target yang di set itu waktunya ternyata udah lewat, maka dia
                akan auto set untuk ke esokan hari nya. 
                """
                format_waktu = target_alarm.strftime("%H:%M")
                judul_notif = f"ALARM DI SET PADA PUKUL {format_waktu} WIB"
                pesan_notif = f"anda akan di bangunkan pukul {format_waktu} WIB"
                notification_termux(judul_notif, pesan_notif)

                print(f"Waktu alarm di set pada {jam}:{menit} WIB")
                return target_alarm
            else:
                print("Jam harus 0-23 dan menit harus 0-59! Coba lagi.\n")

        except ValueError:
            print("Input harus berupa angka! coba lagi.\n")

if __name__ == "__main__" :
    target = input_waktu()



