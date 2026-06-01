# 🚀 Introduction

The **IB Grade Tracker (V1)** is a production-grade terminal application designed to help International Baccalaureate (IB) students manage, calculate, and predict their academic trajectories. 

This project is a complete architectural re-engineering of my original prototype (V1). This first version (V1) relies entirely on volatile, short-term Python dictionaries.
---

## 🛠️ Technologies Used

### 🐍 Core Language & Logic
* **Python 3.x:** Built entirely using native Python. It handles the user interaction menus, core GPA calculation logic, and the algorithm that maps student scores against the official IB 1–7 point scale.

### 🧱 Data Management
* **In-Memory Data Structures:** Leveraged built-in Python collections (dictionaries and lists) to temporarily hold, structure, and manipulate user profiles, subjects, and grade inputs during runtime.

---

## ✨ Features

* **Dynamic Score Tracking:** Allows users to input and manage grades across multiple IB subjects in real time.
* **Automated IB Scale Mapping:** Processes raw scores and automatically maps them to the official IB 1–7 point grading scale using conditional logic.
* **GPA & Diploma Trajectory Calculation:** Instantly calculates current core GPAs and projects overall point totals to help students stay on track for their diploma.
* **Interactive Terminal Menu:** A user-friendly, loop-driven command-line interface that handles seamless navigation between adding data, viewing scores, and updating profiles.
* **Structured In-Memory Storage:** Utilizes nested dictionaries to keep subject data, component weights, and earned grades organized during the active session.

---

## ⚙️ Development Process

I built this prototype using an iterative, step-by-step approach to ensure the core logic was stable before adding more features:

1. **Requirements & Logic Mapping:** I analyzed the official IB grading criteria, component weights, and GPA boundaries to map out how the calculations needed to function mathematically.
2. **Architecture Design:** I designed the data schema using nested Python dictionaries (`{subject: {component: grade}}`) to handle multi-layered data structures efficiently in volatile memory.
3. **Core Engine Development:** I wrote the foundational backend logic, starting with basic math functions, then expanding into the conditional logic loops required to map percentages to the 1–7 scale.
4. **Interface Control Flow:** I built the command-line interface loop, implementing robust input validation to prevent user inputs (like typing a letter instead of a number) from crashing the application.
5. **Testing & Refinement:** I manually ran edge-case scenarios (e.g., scoring exact boundary limits like a 79% vs an 80%) to verify that the calculation engine matched official IB results perfectly.

## 🧠 What I Learned

* **Data Structures in Practice:** Gained deep experience working with nested Python dictionaries and lists, learning how to map complex data relationships programmatically.
* **Input Validation & Error Handling:** Realized early on that user input is unpredictable. I learned how to implement robust error-handling loops to prevent invalid inputs from crashing the program.
* **Algorithmic Logic:** Mastered translating a complex, multi-tiered real-world grading system (IB criteria) into clean, conditional code blocks and reusable functions.

---

## 🚀 Areas for Improvement (The Path to V2)

While the prototype successfully solved the math problem, building it revealed a few critical architectural limitations that I plan to address in the next iteration:

* **Data Persistence:** Because V1 relies entirely on volatile in-memory storage (RAM), all student data is wiped clean the moment the terminal script closes. The system needs a dedicated database engine to save data across sessions.
* **Code Reliability & Testing:** Relying solely on manual testing to catch edge-case calculation errors is inefficient and risky. Moving forward, implementing an automated testing framework is a priority to catch bugs instantly.
* **User Interface:** While functional, a command-line interface limits accessibility. Transitioning the frontend to a web-based UI would make the tool significantly easier for everyday students to navigate.

---

## 🖥️ Running the Project
Since this prototype is built entirely using standard Python libraries, you do not need to install any external packages to run it.

Prerequisites
Make sure you have Python 3.x installed on your machine. You can verify this by running:

Bash
python --version

Setup & Execution

1. Clone the repository:
Bash
git clone https://github.com/YOUR_USERNAME/your-repo-name.git

2. Navigate into the project directory:
Bash
cd your-repo-name

3. Run the application 
Bash
python tracker.py
(Note: Replace tracker.py with the actual name of your main Python file if it is named something else, like main.py).

Interact: Follow the on-screen terminal prompts to add subjects, input grades, and calculate your IB trajectory!

---

Live Video


https://github.com/user-attachments/assets/0acd9379-32e8-4033-9c5d-d84a437db864



