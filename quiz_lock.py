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
        cursor.execute(SELECT * FROM VOCAB WHERE ID_HSK = 1 ORDER BY RAND() LIMIT 1)
        item = cursor.fetchone() #untuk ambil 1 row data di db

        if not item:
            print("Data di table vocab kosong")

        print(f"\n[SKOR : {score}/{target_score}]")
        print(f"Hanzi : {item['Hanzi']}")
        print(f"Hanzi : {item['Pinyin']}")

        user_answer = input("Jawaban (arti) : ").strip()

    