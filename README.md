# 📄 OMR Read New

## 🚩 Problem Statement
Manual evaluation of OMR (Optical Mark Recognition) sheets is:

- Time-consuming when there are many students.  
- Prone to human error (misreading, fatigue, inconsistent marking).  
- Difficult to organize results efficiently for multiple subjects.  

This project aims to automate reading, scoring, and storing of OMR sheets to speed up the process and improve accuracy.

---

## 🔍 Approach
The system follows these steps:

1. **Preprocessing**  
   Use OpenCV to prepare input OMR sheet images (e.g. resizing, thresholding, denoising, alignment) so that bubble detection works reliably.

2. **Bubble/Mark Detection**  
   Identify which bubbles are filled using contour detection or related image analysis in the `modules` folder.

3. **Answer Comparison**  
   Compare detected answers against a predefined answer key to decide correctness.

4. **Scoring**  
   Compute per-subject scores and overall total scores.

5. **Results Storage**  
   Save the final results in both CSV and SQLite database formats, so they are easy to view, share, and query.

---

## ⚙️ Tech Stack

- **Python 3.x**  
- **OpenCV** – Image processing and detection  
- **Pandas** – Data handling, tabular operations  
- **SQLite** – Storage of results  
- (Other modules in `modules/` as helpers for preprocessing, detection, etc.)

---

## 🛠️ Installation

To get the project running locally:

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
# Put scanned OMR sheet images in:
data/
# (If needed) Place the answer key in a JSON or other format in data/, e.g.:
# data/answer_key.json or as required by your implementation
```

## ▶️ Usage
```
python main.py
```

The script will process images from the data/ directory.

+ Results will be saved into:

  + results/results.csv

  + results/results.db (SQLite database)

+ Example console output might look like:
```
Processing sheet: sheet1.png …
Detected 45 / 50 correct
Saved to results/results.csv
Database updated: results/results.db
```

<pre>
.
├── data/               # Input OMR images (+ answer key file(s))
├── modules/            # Helper modules (preprocessing, detection, scoring, etc.)
├── results/            # Outputs: CSV + SQLite DB
├── main.py             # Entry point for running evaluation
├── requirements.txt    # List of required Python packages
└── README.md           # Project documentation
</pre>

## 🚀 Future Work

Build a web interface (e.g. using Streamlit or Flask) for uploading sheets and viewing results.

Use a machine-learning based method to improve bubble detection, especially in noisy or misaligned sheets.

Support multiple OMR sheet layouts/formats automatically.

Add reporting dashboards or visualizations (scores per student, item-wise analysis).

Add error logging and more robust exception handling for bad or unreadable images.


💡 Contributions welcome! Feel free to raise issues or submit pull requests to improve accuracy, usability, or add features.
