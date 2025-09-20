# app.py

import cv2
import numpy as np
import streamlit as st
import fitz
import sqlite3
import pandas as pd

########################################################################
# Configuration
########################################################################
ANSWER_KEY = {
    1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 2, 7: 2, 8: 3, 9: 2, 10: 2, 11: 3, 12: 3, 13: 3, 14: 3, 15: 3, 16: 3, 17: 3, 18: 3, 19: 3, 20: 3,
    21: 0, 22: 1, 23: 2, 24: 3, 25: 0, 26: 0, 27: 0, 28: 1, 29: 2, 30: 3, 31: 0, 32: 1, 33: 2, 34: 3, 35: 0, 36: 0, 37: 1, 38: 2, 39: 3, 40: 0,
    41: 3, 42: 2, 43: 1, 44: 0, 45: 3, 46: 2, 47: 1, 48: 0, 49: 3, 50: 2, 51: 1, 52: 0, 53: 3, 54: 2, 55: 1, 56: 0, 57: 3, 58: 2, 59: 1, 60: 0,
    61: 3, 62: 3, 63: 3, 64: 3, 65: 3, 66: 3, 67: 3, 68: 3, 69: 3, 70: 3, 71: 3, 72: 3, 73: 3, 74: 3, 75: 3, 76: 3, 77: 3, 78: 3, 79: 3, 80: 3,
    81: 3, 82: 3, 83: 3, 84: 3, 85: 3, 86: 3, 87: 3, 88: 3, 89: 3, 90: 3, 91: 3, 92: 3, 93: 3, 94: 3, 95: 3, 96: 3, 97: 3, 98: 3, 99: 3, 100: 3
}
SUBJECT_BLOCKS_PERCENT = {
    "Python":        [0.07, 0.25, 0.23, 0.82, 1],
    "Data Analysis": [0.24, 0.25, 0.40, 0.82, 21],
    "MySQL":         [0.41, 0.25, 0.57, 0.82, 41],
    "Power BI":      [0.58, 0.25, 0.74, 0.82, 61],
    "Adv Stats":     [0.75, 0.25, 0.91, 0.82, 81]
}
########################################################################

# --- Database and helper functions ---
DB_FILE = "results.db"
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL, score INTEGER NOT NULL, total_questions INTEGER NOT NULL, graded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def add_result_to_db(filename, score, total_questions):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO results (filename, score, total_questions) VALUES (?, ?, ?)", (filename, score, total_questions))
    conn.commit()
    conn.close()

def get_all_results():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT filename, score, total_questions, graded_at FROM results ORDER BY graded_at DESC", conn)
    conn.close()
    return df

def convert_pdf_to_image(pdf_bytes):
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    first_page = pdf_document.load_page(0)
    pix = first_page.get_pixmap(dpi=300)
    return pix.tobytes("png")

# --- CORE CV Functions ---
def preprocess_for_grading(image):
    if image is None or image.size == 0: return None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # --- KEY FIX: Fine-tuned Adaptive Thresholding parameters ---
    # A larger block size can help with uneven lighting across the whole page.
    # Adjusting C can make it more or less sensitive.
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 21, 5) # Changed from 11, 2
    return thresh

def find_and_grade_bubbles(subject_img, subject_thresh, start_q_num):
    score = 0
    num_choices = 4
    
    contours, _ = cv2.findContours(subject_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    bubble_contours = []
    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        aspect_ratio = w / float(h)
        if 0.6 <= aspect_ratio <= 1.4 and 10 < w < 40 and 10 < h < 40:
             bubble_contours.append(c)

    if not bubble_contours:
        return 0

    # --- KEY FIX: More robust sorting ---
    # Group contours by y-coordinate to form rows
    rows = {}
    for c in bubble_contours:
        (x, y, w, h) = cv2.boundingRect(c)
        # Use the y-centroid, rounded to the nearest 10, as the key for the row
        row_key = round((y + h/2) / 10.0) * 10
        if row_key not in rows:
            rows[row_key] = []
        rows[row_key].append(c)

    # Sort rows by their y-coordinate key
    sorted_rows_by_y = sorted(rows.items(), key=lambda item: item[0])
    
    question_rows = []
    for y, row_contours in sorted_rows_by_y:
        # Sort contours in each row by x-coordinate
        sorted_row = sorted(row_contours, key=lambda c: cv2.boundingRect(c)[0])
        question_rows.append(sorted_row)
    
    for i, row_contours in enumerate(question_rows):
        if len(row_contours) != num_choices: continue
        
        pixel_counts = []
        for bubble in row_contours:
            mask = np.zeros(subject_thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [bubble], -1, 255, -1)
            mask = cv2.bitwise_and(subject_thresh, subject_thresh, mask=mask)
            pixel_counts.append(cv2.countNonZero(mask))
        
        if not pixel_counts or max(pixel_counts) < 50:
            continue

        marked_index = np.argmax(pixel_counts)
        current_q_num = start_q_num + i
        correct_answer = ANSWER_KEY.get(current_q_num)

        color = (0, 255, 0) if marked_index == correct_answer else (0, 0, 255)
        if marked_index == correct_answer:
            score += 1

        cv2.drawContours(subject_img, [row_contours[marked_index]], -1, color, 3)

    return score

# --- Main Streamlit App ---
init_db()
st.set_page_config(layout="wide")
st.title("Simple OMR Grader")
st.warning("IMPORTANT: Please upload a clean, tightly cropped image of the OMR sheet for best results.")

uploaded_file = st.file_uploader("Upload a cropped OMR sheet...", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file:
    file_bytes = uploaded_file.getvalue()
    filename = uploaded_file.name
    if uploaded_file.type == "application/pdf":
        try: image_bytes = convert_pdf_to_image(file_bytes)
        except Exception as e: st.error(f"Error converting PDF: {e}"); image_bytes = None
    else: image_bytes = file_bytes
    
    if image_bytes:
        nparr = np.frombuffer(image_bytes, np.uint8)
        original_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        st.image(original_img, caption='Uploaded OMR Sheet', width=600)

        with st.spinner('Grading...'):
            processed_img = cv2.resize(original_img, (800, 1050))
            result_image = processed_img.copy()
            h, w, _ = processed_img.shape
            
            total_score = 0
            
            for subject, (x_start_pct, y_start_pct, x_end_pct, y_end_pct, start_q) in SUBJECT_BLOCKS_PERCENT.items():
                x1 = int(w * x_start_pct)
                y1 = int(h * y_start_pct)
                x2 = int(w * x_end_pct)
                y2 = int(h * y_end_pct)

                subject_img_crop = result_image[y1:y2, x1:x2]
                subject_thresh_crop = preprocess_for_grading(subject_img_crop)

                if subject_thresh_crop is not None:
                    score = find_and_grade_bubbles(subject_img_crop, subject_thresh_crop, start_q)
                    total_score += score
            
            st.success(f"Grading Complete! Total Score: **{total_score} / 100**")
            add_result_to_db(filename, total_score, 100)
            st.image(result_image, caption='Fully Graded OMR Sheet', width=800)

st.markdown("---")
st.subheader("📊 Past Results")
st.dataframe(get_all_results())