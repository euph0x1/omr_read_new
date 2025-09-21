import cv2
import json
from modules.preprocess import preprocess_image
from modules.detect import detect_answers
from modules.evaluate import extract_answers, score_answers
from modules.storage import save_results

if __name__ == "__main__":
    image_path = "data/omr_sheets/img1.jpeg"
    student_name = "G. Bhanu Prasad"

    # Preprocess
    img, thresh = preprocess_image(image_path)

    # Detect bubbles
    bubble_contours = detect_answers(thresh)

    # Extract answers
    
    
    from modules.detect import detect_answers
    answers = detect_answers(thresh)


    # Load answer key
    with open("data/answer_key.json", "r") as f:
        answer_key = json.load(f)

    # Score
    scores = score_answers(answers, answer_key)

    # Save
    save_results(student_name, scores)

    print("Evaluation complete:", scores)
