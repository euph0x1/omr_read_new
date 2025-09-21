# 📄 OMR Read New

## 🚩 Problem Statement
Manual evaluation of OMR (Optical Mark Recognition) sheets is:

- Time-consuming when there are many students.  
- Prone to human error (misreading, fatigue, inconsistent marking).  
- Difficult to organize results efficiently for multiple subjects.  

This project automates reading, scoring, and storing of OMR sheets to speed up the process and improve accuracy.

---

## 🔍 Approach
The system follows these steps:

1. **Preprocessing** – Use OpenCV to clean, resize, threshold, and align OMR sheet images.  
2. **Bubble/Mark Detection** – Detect filled bubbles via contour analysis.  
3. **Answer Comparison** – Match detected answers with the predefined answer key.  
4. **Scoring** – Calculate per-subject and total scores.  
5. **Results Storage** – Save results to both **CSV** and **SQLite database**.  
6. **Web App (Streamlit)** – Upload OMR sheets via browser, view results instantly, and download CSV reports.

---

## ⚙️ Tech Stack
- **Python 3.x**  
- **OpenCV** – Image processing & bubble detection  
- **Pandas** – Data handling and CSV export  
- **SQLite** – Persistent results storage  
- **Streamlit** – Web application interface  

---

## 🛠️ Installation

Set up the project locally:

```bash
# 1. Clone the repository
git clone https://github.com/euph0x1/omr_read_new.git
cd omr_read_new

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Prepare input data
# Put OMR sheet images in:
data/
```

## ▶️ Usage
Option 1: Command Line
```
python main.py
```
+ Processes all sheets in data/

+ Saves results to:

  + results/results.csv

  + results/results.db

Console example:
<pre>
Processing sheet: sheet1.png …
Detected 45 / 50 correct
Saved to results/results.csv
Database updated: results/results.db
</pre>

Option 2: Streamlit Web App

Run the web interface with:
```
streamlit run streamlit_app.py
```
Features:

+ Upload OMR sheet images via browser

+ View processed results instantly

+ Download CSV of results

+ Results are also saved automatically in results/


## 📂 Repository Structure
<pre>
   .
├── data/               # Input OMR images + answer key
├── modules/            # Helper modules (preprocessing, detection, scoring, etc.)
├── results/            # Outputs: CSV + SQLite DB
├── main.py             # CLI entry point
├── streamlit_app.py    # Streamlit web app entry point
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
</pre>


lace the answer key in:
data/answer_key.json
