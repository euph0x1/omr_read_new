import streamlit as st
import cv2
import numpy as np
import json
import pandas as pd
from modules.preprocess import preprocess_image
from modules.detect import detect_answers
from modules.evaluate import score_answers
from modules.storage import save_results
import os

def main():
    st.set_page_config(layout="wide")
    st.title("OMR Sheet Evaluator")

    st.sidebar.header("Upload OMR Sheet")
    uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.sidebar.success("Image uploaded successfully!")
        
        # Read the image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img_raw = cv2.imdecode(file_bytes, 1)

        st.subheader("Original Image")
        st.image(img_raw, channels="BGR", use_column_width=True)

        # Placeholder for student name (can be added as a text input later)
        student_name = "Uploaded Student" 
        
        # Process the image
        st.subheader("Processing OMR Sheet...")
        
        # Save uploaded image to a temporary file
        temp_image_path = "temp_omr_sheet.jpeg"
        cv2.imwrite(temp_image_path, img_raw)

        # Preprocess
        img_processed, thresh = preprocess_image(temp_image_path)
        
        # Detect bubbles
        answers = detect_answers(thresh)

        # Load answer key
        with open("data/answer_key.json", "r") as f:
            answer_key = json.load(f)

        # Score
        scores = score_answers(answers, answer_key)
        
        st.subheader("Evaluation Results")
        st.write(f"Student Name: {student_name}")
        
        # Display scores
        scores_df = pd.DataFrame([scores])
        st.table(scores_df)

        # Save results
        save_results(student_name, scores)
        st.success("Results saved to database and CSV!")

        # Display processed image (optional)
        st.subheader("Processed Image (Thresholded)")
        st.image(thresh, use_column_width=True) # Display thresholded image as grayscale
        
        # Provide download option for results
        csv_buffer = scores_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Results as CSV",
            data=csv_buffer,
            file_name="omr_results.csv",
            mime="text/csv",
        )
        
        # Clean up temporary file
        os.remove(temp_image_path)

if __name__ == "__main__":
    main()
