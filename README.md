# Automated OMR Evaluation & Scoring System

This project is a web-based OMR sheet evaluation system built for the Innomatics Research Labs Hackathon. It automates the process of grading OMR sheets by using computer vision techniques to read, analyze, and score them.

## Problem Statement

The traditional method of manually grading thousands of OMR sheets is slow, prone to human error, and resource-intensive. This delays feedback to students, which is critical for their learning and placement preparation. The goal of this project was to create a scalable, automated system to solve this problem.

## Our Solution

We developed a web application using Streamlit and OpenCV that allows an evaluator to upload a scanned OMR sheet (as an image or PDF). The application processes the sheet, grades it against a predefined answer key, and stores the results in a local database for auditing. Our final solution uses a robust, simplified approach that requires a well-cropped input image, ensuring high accuracy and reliability.

### Key Features
* **Multi-Format Upload:** Accepts OMR sheets in `.jpg`, `.png`, and `.pdf` formats.
* **Automated Grading:** Processes a 100-question, 5-subject OMR sheet and calculates the total score.
* **Visual Feedback:** Displays the graded sheet with correctly and incorrectly marked answers highlighted.
* **Database Storage:** Saves every result to a local SQLite database for a persistent audit trail.
* **Simple Web Interface:** Built with Streamlit for an intuitive user experience.

## Tech Stack
* **Language:** Python
* **Core Libraries:** OpenCV, NumPy
* **Web Framework:** Streamlit
* **File Handling:** PyMuPDF (for PDFs), Pandas (for data display)
* **Database:** SQLite

## How to Run the Project Locally

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
The application will open in your web browser.

## Challenges & Future Work

The most significant challenge was reliably detecting and "straightening" (perspective warping) OMR sheets from raw photos with varying angles and lighting. After several attempts, we pivoted to a more robust solution that processes cleanly cropped scans for guaranteed accuracy.

**Future enhancements could include:**
* Implementing a fully automatic document detection and straightening algorithm that is robust to all conditions.
* Using OCR to automatically detect the exam "Set No." and load the correct answer key from the database.
* Expanding the dashboard to include detailed analytics and performance tracking for students and subjects.

## Demo

*(Here you can add a screenshot or a GIF of your working application)*

---
*Project by [Your Name/Team Name]*