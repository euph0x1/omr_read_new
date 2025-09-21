import sqlite3
import csv
import os

def save_results(student_name, scores, db_path="data/results/results.db", csv_path="data/results/results.csv"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Save to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS results (
                        student TEXT, Python INT, EDA INT, MySQL INT,
                        PowerBI INT, Stats INT, Total INT)""")
    cursor.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (student_name, scores["Python"], scores["EDA"], scores["MySQL"],
                    scores["PowerBI"], scores["Stats"], scores["Total"]))
    conn.commit()
    conn.close()

    # Save to CSV
    write_header = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["Student", "Python", "EDA", "MySQL", "PowerBI", "Stats", "Total"])
        writer.writerow([student_name, scores["Python"], scores["EDA"], scores["MySQL"], scores["PowerBI"], scores["Stats"], scores["Total"]])
