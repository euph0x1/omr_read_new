import cv2
import json

def extract_answers(thresh_img, bubble_contours):
    answers = []
    num_questions = 100   # total across all subjects
    choices = 4           # A, B, C, D

    for q in range(num_questions):
        row = bubble_contours[q*choices:(q+1)*choices]
        bubbled = None
        max_nonzero = 0

        for j, (x,y,w,h) in enumerate(row):
            roi = thresh_img[y:y+h, x:x+w]
            total = cv2.countNonZero(roi)
            if total > max_nonzero:
                max_nonzero = total
                bubbled = j

        answers.append(bubbled)

    return answers


def score_answers(answers, answer_key):
    subjects = ["Python", "EDA", "MySQL", "PowerBI", "Stats"]
    scores = {}
    index = 0

    for subject in subjects:
        key = answer_key[subject]
        correct = 0
        for i in range(20):
            student_ans = answers[index]
            if student_ans is not None and key[i] == chr(ord('a') + student_ans):
                correct += 1
            index += 1
        scores[subject] = correct

    scores["Total"] = sum(scores.values())
    return scores
