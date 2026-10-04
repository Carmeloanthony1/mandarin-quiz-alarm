import mysql.connector
import time
import os
import sys
from dotenv import load_dotenv

DB_CONFIG = {
    'host' : os.getenv('DB_HOST'),
    'port' : int(os.getenv('DB_PORT')),
    'user' : os.getenv('DB_USER'),
    'name' : os.getenv("DB_NAME")
}

def dev_cancel(user_input):
    bypass_word = ["dev"]
    return 
def check_answer(user_input, correct_meaning):
    """convert user_input and correct_meaning into lower case"""
    if not user_input:
        return False

    user_input_after = user_input.lower().split()
    correct_meaning_after = correct_meaning.lower()

    return any(word in correct_meaning_after for word in user_input_after)

def run_gate(target_score = 3):
    """lock hp"""
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor(dictionary = True)
    except Exception as e:
        print(f"Gagal koneksi ke Database : {e}")
        return False
    
    score = 0
    os.system('clear')
    print("=" * 50)
    print("HSK GATEWAY LOCK - Selesaikan {target_score} Soal!")
    print("=" * 50)

    while score < target_score:
        cursor.execute("SELECT * FROM VOCAB WHERE ID_HSK = 1 ORDER BY RAND() LIMIT 1")
        item = cursor.fetchone() #untuk ambil 1 row data di db

        if not item:
            print("Data di table vocab kosong")

        print(f"\n[SKOR : {score}/{target_score}]")
        print(f"Hanzi : {item['Hanzi']}")
        print(f"Hanzi : {item['Pinyin']}")

        user_answer = input("Jawaban (arti) : ").strip()

        if dev_cancel(user_input):
            print(f"[DEV CANCEL] | AUTO STOP PROGRAM")
            score += 3

        if check_answer(user_answer, item['Meaning']):
            print("Correct")
            score += 1
        else:
            print(f"Salah!, {item['Hanzi']} | {item['Pinyin']} memiliki arti {item['Meaning']}")
    
    db.close()
    print("\n" + "=" * 50)
    print("Selamat beraktivitas!")
    return True

if __name__ = "__main__":
    run_gate(target_score = 3)