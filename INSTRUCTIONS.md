# OMR Evaluation System - Setup Instructions

Follow these steps to set up and run the project on your machine.

### ## Step 1: Unzip and Navigate to the Project Folder

1.  Unzip the project folder you received to a location of your choice (e.g., your Desktop).
2.  Open your command prompt (CMD, PowerShell, or Terminal).
3.  Use the `cd` command to navigate into the unzipped project folder.
    ```bash
    cd path/to/the/omr_evaluation_system
    ```

### ## Step 2: Create and Activate a Virtual Environment

This creates an isolated environment for the project's libraries.

1.  **Create the environment** by running this command in your terminal:
    ```bash
    python -m venv venv
    ```
2.  **Activate the environment.** The command depends on your operating system:
    * **On Windows:**
        ```bash
        venv\Scripts\activate
        ```
    * **On macOS or Linux:**
        ```bash
        source venv/bin/activate
        ```
    You will know it's active when you see `(venv)` at the beginning of your command prompt line.

### ## Step 3: Install Required Libraries

This command will automatically install all the necessary packages from the `requirements.txt` file.

1.  Make sure your virtual environment is still active.
2.  Run the following command:
    ```bash
    pip install -r requirements.txt
    ```

### ## Step 4: Run the Web Application

Now you are ready to launch the app.

1.  In the same terminal (with the virtual environment active), run this command:
    ```bash
    streamlit run app.py
    ```
2.  Your default web browser should automatically open a new tab with the OMR Grader application running. You can now upload an OMR sheet image to test it.

---

**To stop the application**, go back to your terminal and press **`Ctrl` + `C`**.