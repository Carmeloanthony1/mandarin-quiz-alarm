import mysql.connector
import time
import os
import sys
from dotenv import load_dotenv
import random

base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

DB_CONFIG = {
    'host' : os.getenv('DB_HOST'),
    'port' : os.getenv('DB_PORT'),
    'user' : os.getenv('DB_USER'),
    'password' : os.getenv("DB_PASSWORD"),
    'database' : os.getenv("DB_NAME")
}

def dev_cancel(user_answer):
    bypass_word = ["dev"]
    return user_answer.lower() in bypass_word

def check_answer(selected_option, correct_meaning):
    return selected_option == correct_meaning

def random_answer(target_item, all_items):
    """Pilihan ganda (1 benar, 3 salah)"""
    correct_answer = target_item['Meaning']
    wrong_answer = list({item['Meaning'] for item in all_items if item['Meaning'] != correct_answer})

    options = random.sample(wrong_answer, min(3, len(wrong_answer))) + [correct_answer]
    random.shuffle(options)

    return options, correct_answer

def run_gate(target_score = 3):
    """lock hp"""
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor(dictionary = True)

        cursor.execute("SELECT * FROM VOCAB WHERE ID_HSK = 1 ORDER BY RAND() LIMIT 10")
        sample_item = cursor.fetchall() #untuk ambil 1 row data di db

    except Exception as e:
        print(f"Gagal koneksi ke Database : {e}")
        return False
        
    if not sample_item or len(sample_item) < 4:
        print("Data di table tidak sesuai dengan kebutuhan")
        db.close()
        return False
    
    score = 0
    os.system('clear')
    print("=" * 50)
    print(f"HSK GATEWAY LOCK - Selesaikan {target_score} Soal!")
    print("=" * 50)

    labels = ['A', 'B', 'C', 'D']

    while score < target_score:
        item = random.choice(sample_item)

        print(f"\n[SKOR : {score}/{target_score}]")
        print(f"Hanzi : {item['Hanzi']}")
        print(f"Pinyin : {item['Pinyin']}")

        options, correct_meaning = random_answer(item, sample_item)
        print("\n Pilih Jawaban yang benar : ")
        for idx, option in enumerate(options):
            print(f" {labels[idx]}. {option}")

        user_answer = input("\nJawaban (A/B/C/D) : ").strip()

        if dev_cancel(user_answer):
            print(f"[DEV CANCEL] | AUTO STOP PROGRAM")
            score = target_score
            break

        user_choice = user_answer.upper()
        if user_choice in labels:
            chosen_index = labels.index(user_choice)
            selected_option = options[chosen_index]

            if check_answer(selected_option, correct_meaning):
                print("CORRECT!")
                score += 1

            else:
                print(f"FALSE!, {item['Hanzi']} | {item['Pinyin']} memiliki arti {item['Meaning']}")
        else:
            print("Input tidak valid! Masukkan A, B, C, atau D.")
    
    db.close()
    print("\n" + "=" * 50)
    print("Selamat beraktivitas!")
    return True

if __name__ == "__main__":
    run_gate(target_score = 3)