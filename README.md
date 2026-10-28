# Smart Study Planner with Priority Scheduling

A beginner-friendly Python and Streamlit application that helps students organize study tasks and rank pending work by importance and deadline urgency.

## Features

- Create study tasks with a type, deadline, importance, and estimated hours.
- Automatically calculate priority scores and sort pending tasks.
- Mark tasks as completed and view them separately.
- Save and load tasks permanently using JSON.
- See total, pending, and completed task counts in a clean dashboard.

## OS Concepts Demonstrated

- **Scheduling:** Priority-based ordering of pending tasks.
- **Process state:** Pending and completed task states.
- **File management:** Persistent storage using a local JSON file.
- **Resource estimation:** Estimating study time and workload.

## Technologies Used

- Python
- Streamlit
- JSON
- Python `datetime` module

## Installation

1. Clone or download this project.
2. Open the project folder in a terminal.
3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate it:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the Application

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit in your browser.
