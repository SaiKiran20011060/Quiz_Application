# Enhanced Quiz Application

A feature-rich desktop quiz application built with Python and `tkinter`. This application provides a modern user interface, a full user authentication system with different roles, and dynamic quiz content management.

 
*(Suggestion: Take a screenshot of your app's main menu and upload it to a site like Imgur, then replace the URL above to display an image here.)*

---

## Features

*   **Modern UI**: A clean, light-themed interface with custom-drawn, interactive widgets.
*   **User Authentication**: Secure login and sign-up system. Passwords and security answers are hashed and never stored in plain text.
*   **Password Recovery**: A "Forgot Password" flow that uses security questions to allow users to reset their password.
*   **Role-Based Access Control**:
    *   **Root Admin**: The main administrator (`sai kiran`) who can manage other admins and add quiz questions.
    *   **Admin**: Users promoted by the Root Admin. They can add new quiz questions.
    *   **User**: The default role for new users, who can play quizzes and view high scores.
*   **Dynamic Quizzes**:
    *   Questions and categories are loaded from an external `questions.json` file.
    *   Admins can add new questions or create entirely new categories through the UI.
*   **Engaging Gameplay**:
    *   Three difficulty levels (Easy, Medium, Hard) that adjust the number of questions and time limit.
    *   An optional timer for an added challenge.
    *   Instant feedback on answers.
*   **Score Tracking**: A persistent high-scores list that tracks the top 10 players.

---

## For Users: How to Run the Application

This is a desktop application for Windows. You do not need to install Python or any other tools to run it.

1.  **Go to the Releases Page**: Click here to go to the releases section of this repository. *(Note: Replace `your-username/your-repo-name` with your actual GitHub details).*

2.  **Download the `.exe` File**: From the latest release, find the "Assets" section and download the `enhanced_quiz_app.exe` file.

3.  **Run the Application**: Double-click the downloaded `enhanced_quiz_app.exe` file to start the quiz application.

> **Note on Windows Security:**
> When you run the `.exe` for the first time, Windows Defender may show a blue pop-up saying "Windows protected your PC". This is normal for applications from new developers.
> *   Click on **"More info"**.
> *   Then, click the **"Run anyway"** button that appears.

---

## For Developers: Running from Source

If you want to run the application from the source code or make your own changes, follow these steps.

### Prerequisites

*   Python 3.x

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd your-repo-name
    ```

3.  **Run the application:**
    ```bash
    python "Quiz App/enhanced_quiz_app.py"
    ```

### Building the Executable

To package the application into a standalone `.exe` file yourself, you will need `pyinstaller`.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Run the build command from the project root directory:**
    This command bundles the script and all necessary data files (`.json`) into a single executable.
    ```bash
    pyinstaller --onefile --windowed --add-data "questions.json;." --add-data "users.json;." --add-data "scores.json;." "Quiz App/enhanced_quiz_app.py"
    ```

3.  The final `enhanced_quiz_app.exe` will be located in the `dist` folder.

---

## Default Accounts

For management and demonstration purposes, the following accounts are automatically created.

### Root Admin Credentials

This account has full administrative privileges, including managing other admins and adding questions.

*   **Username**: `sai kiran`
*   **Password**: `sai123@R`

### Demo User Account

This is a standard user account for testing the quiz-taking functionality.

*   **Username**: `demo`
*   **Password**: `demo`