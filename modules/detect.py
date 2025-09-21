import cv2
import numpy as np

def detect_answers(thresh, num_questions=100, num_choices=4, subjects=5):
    """
    Detects marked answers from the thresholded OMR sheet.
    - Assumes grid layout: 5 subjects × 20 questions each = 100 total.
    - Each question has 4 options (a, b, c, d).
    Returns: list of answers (0=a, 1=b, 2=c, 3=d, None if blank/ambiguous).
    """

    answers = []
    h, w = thresh.shape

    # Divide sheet into subjects (rows)
    subject_height = h // subjects

    for s in range(subjects):
        subject_img = thresh[s * subject_height:(s + 1) * subject_height, :]
        q_height = subject_img.shape[0] // (num_questions // subjects)

        for q in range(num_questions // subjects):
            q_img = subject_img[q * q_height:(q + 1) * q_height, :]

            # Split each question into options (a,b,c,d)
            option_width = q_img.shape[1] // num_choices
            filled = []

            for opt in range(num_choices):
                opt_img = q_img[:, opt * option_width:(opt + 1) * option_width]

                # Count nonzero pixels (ink)
                total_pixels = cv2.countNonZero(opt_img)
                filled.append(total_pixels)

            # Determine marked option
            max_val = max(filled)
            if max_val < 200:  # threshold to ignore blanks
                answers.append(None)
            else:
                max_idx = np.argmax(filled)
                # Check ambiguity (two filled bubbles close in size)
                sorted_vals = sorted(filled, reverse=True)
                if len(sorted_vals) > 1 and (sorted_vals[0] - sorted_vals[1]) < 100:
                    answers.append(None)  # ambiguous
                else:
                    answers.append(max_idx)

    return answers
