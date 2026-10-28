import json
import os
from datetime import date

import streamlit as st


TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(tasks, list):
        return []

    for task in tasks:
        task["deadline"] = date.fromisoformat(task["deadline"])
        task.setdefault("completed", False)

    return tasks


def save_tasks(tasks):
    tasks_to_save = []
    for task in tasks:
        task_to_save = task.copy()
        task_to_save["deadline"] = task["deadline"].isoformat()
        tasks_to_save.append(task_to_save)

    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks_to_save, file, indent=4)


st.set_page_config(
    page_title="Smart Study Planner",
    page_icon=None,
    layout="wide",
)

st.markdown(
    """
    <style>
        :root {
            --background: #F5F0FF;
            --surface: #FFFFFF;
            --strong-border: #725A91;
            --border: #9484A8;
            --inner-border: #B6A9C5;
            --primary: #8B5CF6;
            --hover: #7C3AED;
            --text: #31204F;
            --secondary-text: #6B5A85;
            --highlight: #EDE9FE;
        }

        .stApp {
            background: var(--background);
            color: var(--text);
        }

        [data-testid="stSidebar"] {
            background: #FBF9FF;
            border-right: 1px solid var(--inner-border);
            padding: 1.5rem 1.25rem;
        }

        [data-testid="stSidebar"] * {
            color: var(--text);
        }

        [data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--strong-border);
            border-radius: 8px;
            min-height: 140px;
            padding: 22px;
        }

        [data-testid="stMetricLabel"] {
            color: var(--secondary-text);
            font-size: 1.02rem;
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: var(--text);
            font-size: 2.5rem;
            font-weight: 700;
        }

        .task-card {
            background: var(--surface);
            border: 1px solid var(--strong-border);
            border-radius: 8px;
            padding: 34px 24px;
            text-align: center;
        }

        .empty-title {
            color: var(--text);
            font-size: 1.05rem;
            margin: 0 0 6px 0;
        }

        .empty-message {
            color: var(--secondary-text);
            margin: 0;
        }

        .header-logo {
            display: none;
        }

        .edge-logo {
            position: absolute;
            top: 1.25rem;
            right: 3rem;
            display: grid;
            place-items: center;
            width: 64px;
            height: 64px;
            margin: 0 auto 14px;
            border: 1px solid var(--strong-border);
            border-radius: 10px;
            background: var(--surface);
            color: var(--text);
            font-size: 1.05rem;
            font-weight: 800;
            letter-spacing: 0.04em;
        }

        .brand-block {
            display: none;
        }

        .brand-block-visible {
            display: none;
            align-items: center;
            align-items: center;
            gap: 10px;
            margin: 4px 0 12px;
        }

        .brand-mark {
            display: none;
            place-items: center;
            width: 42px;
            height: 42px;
            flex: 0 0 42px;
            border: 2px solid var(--strong-border);
            border-radius: 8px;
            background: var(--surface);
            color: var(--text);
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 0.04em;
        }

        .brand-name {
            color: var(--text);
            font-size: 1.14rem;
            line-height: 1.25;
            font-weight: 750;
        }

        .sidebar-nav {
            display: grid;
            gap: 4px;
            margin-top: 24px;
        }

        .sidebar-link {
            color: var(--text);
            border: 1px solid var(--inner-border);
            border-left: 4px solid var(--inner-border);
            padding: 9px 10px;
            font-size: 0.92rem;
        }

        .sidebar-link.active {
            color: var(--text);
            background: var(--surface);
            border: 1px solid var(--strong-border);
            border-left: 4px solid var(--primary);
            font-weight: 650;
        }

        .brand-description,
        .subtitle {
            color: var(--secondary-text);
        }

        .subtitle {
            font-size: 1.05rem;
            margin: -18px 0 28px 0;
        }

        h1, h2, h3 {
            color: var(--text);
        }

        h2 {
            font-size: 1.65rem;
            margin: 0 0 12px;
            text-align: left;
        }

        h3 {
            text-align: left;
        }

        header[data-testid="stHeader"] {
            height: 0;
        }

        footer[data-testid="stFooter"] {
            visibility: hidden;
        }

        .block-container {
            max-width: none;
            width: 100%;
            padding: 2.25rem 3rem 3rem;
        }

        [data-testid="stMetric"] {
            border: 1px solid var(--strong-border);
            min-height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: none;
        }

        [data-testid="stVerticalBlockBorderWrapper"] > div {
            background: var(--surface);
            border: 1px solid var(--strong-border);
            border-radius: 8px;
            padding: 20px 22px;
        }

        [data-testid="stForm"] {
            background: var(--surface);
            border: 1px solid var(--strong-border);
            border-radius: 8px;
            padding: 24px;
            box-shadow: none;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stSelectbox"] > div,
        [data-testid="stDateInput"] input {
            background: var(--surface);
            color: var(--text);
            border: 1px solid var(--inner-border);
            min-height: 46px;
        }

        [data-testid="stTextInput"] input:focus,
        [data-testid="stNumberInput"] input:focus,
        [data-testid="stDateInput"] input:focus,
        [data-testid="stSelectbox"] > div:focus-within {
            border-color: var(--primary);
            box-shadow: 0 0 0 1px var(--primary);
        }

        div.stButton > button {
            background: var(--primary);
            color: #FFFFFF;
            border: 2px solid var(--primary);
            border-radius: 8px;
            min-height: 48px;
            padding: 0.5rem 1.25rem;
            font-size: 1rem;
            font-weight: 650;
        }

        div.stButton > button:hover {
            background: var(--hover);
            border: 2px solid var(--strong-border);
            color: #FFFFFF;
        }

        [data-testid="stNotification"] {
            border: 1px solid var(--strong-border);
            border-radius: 8px;
        }

        div.stButton > button[kind="secondary"] {
            width: 100%;
            margin-top: 8px;
            background: var(--primary);
            color: #FFFFFF;
            border-color: var(--primary);
        }

        .page-title {
            color: var(--text);
            text-align: left;
            font-size: 2.65rem;
            font-weight: 750;
            letter-spacing: -0.02em;
            margin: 0 0 4px;
        }

        .subtitle {
            text-align: left;
            margin: 4px 0 28px 0;
            font-size: 1.08rem;
        }

        .section-caption {
            color: var(--secondary-text);
            text-align: left;
            margin: -5px 0 16px 0;
        }

        .task-title {
            color: var(--text);
            font-size: 1.05rem;
            font-weight: 650;
            margin: 0 0 12px 0;
        }

        .task-detail-block {
            min-height: 82px;
            height: 100%;
            border: 1px solid var(--inner-border);
            border-radius: 6px;
            padding: 10px 10px 8px;
            background: #FFFFFF;
        }

        .task-detail {
            color: var(--secondary-text);
            font-size: 0.78rem;
            margin: 0 0 4px 0;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .task-value {
            color: var(--text);
            font-size: 0.95rem;
            font-weight: 550;
            margin: 0;
        }

        .status-pill,
        .priority-pill {
            display: inline-block;
            border: 2px solid var(--strong-border);
            border-radius: 999px;
            padding: 5px 10px;
            font-size: 0.78rem;
            font-weight: 650;
        }

        .status-pending {
            color: var(--primary);
            background: var(--highlight);
            border-color: var(--border);
        }

        .status-completed {
            color: var(--text);
            background: #FFFFFF;
            border: 1px solid var(--strong-border);
        }

        .priority-high {
            color: #FFFFFF;
            background: var(--primary);
            border-color: var(--primary);
        }

        .priority-medium {
            color: var(--text);
            background: var(--highlight);
            border-color: var(--strong-border);
        }

        .priority-low {
            color: var(--secondary-text);
            background: #FFFFFF;
            border-color: var(--border);
        }

        @media (max-width: 900px) {
            .block-container {
                padding: 1.25rem 0.5rem 2rem;
            }

            [data-testid="stMetric"] {
                min-height: 120px;
                padding: 16px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        '''<div class="brand-block">
            <div class="brand-name">Study<br>Planner</div>
        </div>''',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="brand-description">Plan tasks, prioritize your work, and stay focused on your study goals.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '''<nav class="sidebar-nav">
            <span class="sidebar-link active">Dashboard</span>
            <span class="sidebar-link">Tasks</span>
            <span class="sidebar-link">Completed</span>
        </nav>''',
        unsafe_allow_html=True,
    )

st.markdown(
    '''<div class="edge-logo" aria-hidden="true">SP</div>
    <h1 class="page-title">Smart Study Planner</h1>
    <p class="subtitle">Plan smarter. Study better.</p>''',
    unsafe_allow_html=True,
)

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

st.subheader("Add New Task")
with st.form("add_task_form", clear_on_submit=True):
    task_name = st.text_input("Task name", placeholder="e.g. Operating Systems lab report")

    detail_col1, detail_col2 = st.columns(2)
    with detail_col1:
        task_type = st.selectbox(
            "Task type",
            options=["Assignment", "Exam", "Study Session"],
        )
        importance = st.selectbox(
            "Importance",
            options=["Low", "Medium", "High"],
        )

    with detail_col2:
        deadline = st.date_input("Deadline", value=date.today())
        estimated_time = st.number_input(
            "Estimated study time (hours)",
            min_value=0.0,
            step=0.5,
            format="%.1f",
        )

    submitted = st.form_submit_button("Add Task", use_container_width=True)

if submitted:
    task_name = task_name.strip()

    if not task_name:
        st.error("Please enter a task name.")
    elif estimated_time <= 0:
        st.error("Estimated study time must be greater than zero.")
    else:
        task_ids = [task.get("id", 0) for task in st.session_state.tasks]
        st.session_state.tasks.append(
            {
                "id": max(task_ids, default=0) + 1,
                "name": task_name,
                "type": task_type,
                "deadline": deadline,
                "importance": importance,
                "estimated_time": estimated_time,
                "completed": False,
            }
        )
        save_tasks(st.session_state.tasks)
        st.success("Task added successfully.")

tasks = st.session_state.tasks
pending_tasks = [task for task in tasks if not task["completed"]]
completed_tasks = [task for task in tasks if task["completed"]]

col1, col2, col3 = st.columns(3)
col1.metric("Total Tasks", len(tasks))
col2.metric("Pending Tasks", len(pending_tasks))
col3.metric("Completed Tasks", len(completed_tasks))

st.header("Your Study Tasks")
st.markdown(
    '<p class="section-caption">Tasks are ranked by importance, deadline urgency, and estimated study time.</p>',
    unsafe_allow_html=True,
)


def calculate_priority(task):
    importance_points = {"Low": 1, "Medium": 2, "High": 3}

    days_left = (task["deadline"] - date.today()).days
    if days_left <= 0:
        urgency_points = 3
    elif days_left <= 3:
        urgency_points = 2
    else:
        urgency_points = 1

    study_time_points = 2 if task["estimated_time"] >= 2 else 1
    score = importance_points[task["importance"]] + urgency_points + study_time_points

    return score


def get_priority_label(score):
    if score >= 7:
        return "High Priority"
    if score >= 5:
        return "Medium Priority"
    return "Low Priority"


ranked_tasks = sorted(
    pending_tasks,
    key=lambda task: (-calculate_priority(task), task["deadline"]),
)

if not ranked_tasks:
    st.markdown(
        """
        <div class="task-card">
            <p class="empty-title">No tasks yet</p>
            <p class="empty-message">No tasks yet. Add your first study task soon.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    for task in ranked_tasks:
        score = calculate_priority(task)
        priority_label = get_priority_label(score)
        priority_class = priority_label.lower().replace(" ", "-")

        with st.container(border=True):
            title_col, status_col = st.columns([4, 1])
            title_col.markdown(
                f'<p class="task-title">{task["name"]}</p>',
                unsafe_allow_html=True,
            )
            status_col.markdown(
                '<span class="status-pill status-pending">Pending</span>',
                unsafe_allow_html=True,
            )

            type_col, deadline_col, importance_col, time_col, score_column = st.columns(5)
            task_details = (
                (type_col, "Type", task["type"]),
                (deadline_col, "Deadline", task["deadline"]),
                (importance_col, "Importance", task["importance"]),
                (time_col, "Estimated", f'{task["estimated_time"]:.1f} hours'),
                (
                    score_column,
                    "Priority",
                    f'<span class="priority-pill priority-{priority_class.split("-")[0]}">{priority_label} · {score}</span>',
                ),
            )
            for column, label, value in task_details:
                column.markdown(
                    f'<div class="task-detail-block"><p class="task-detail">{label}</p><p class="task-value">{value}</p></div>',
                    unsafe_allow_html=True,
                )

            if st.button(
                "Mark Completed",
                key=f"complete_{task['id']}",
            ):
                task["completed"] = True
                save_tasks(st.session_state.tasks)
                st.rerun()

st.subheader("Completed Tasks")
if not completed_tasks:
    st.caption("No completed tasks yet.")
else:
    for task in completed_tasks:
        score = calculate_priority(task)
        priority_label = get_priority_label(score)
        priority_class = priority_label.lower().replace(" ", "-").split("-")[0]

        with st.container(border=True):
            title_col, status_col = st.columns([4, 1])
            title_col.markdown(
                f'<p class="task-title">{task["name"]}</p>',
                unsafe_allow_html=True,
            )
            status_col.markdown(
                '<span class="status-pill status-completed">Completed</span>',
                unsafe_allow_html=True,
            )

            type_col, deadline_col, importance_col, time_col, score_column = st.columns(5)
            task_details = (
                (type_col, "Type", task["type"]),
                (deadline_col, "Deadline", task["deadline"]),
                (importance_col, "Importance", task["importance"]),
                (time_col, "Estimated", f'{task["estimated_time"]:.1f} hours'),
                (
                    score_column,
                    "Priority",
                    f'<span class="priority-pill priority-{priority_class}">{priority_label} · {score}</span>',
                ),
            )
            for column, label, value in task_details:
                column.markdown(
                    f'<div class="task-detail-block"><p class="task-detail">{label}</p><p class="task-value">{value}</p></div>',
                    unsafe_allow_html=True,
                )
