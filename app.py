from __future__ import annotations

from typing import Any

import streamlit as st

from assessment import (
    QUESTIONS_PER_ASSESSMENT,
    QUIZZES,
    build_30_day_plan,
    create_attempt,
    score_assessment,
)
from predictor import MODEL_NAMES, predict


st.set_page_config(
    page_title="Placement Lab",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root {
        --ink: #1b292e;
        --muted: #64757b;
        --paper: #f3f7f8;
        --line: #dce6e8;
        --teal: #087f8c;
        --coral: #ed7658;
        --mint: #dff1eb;
        --gold: #f2d277;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); letter-spacing: 0; }
    .stApp { background: radial-gradient(ellipse at 92% 0%, #dfedef 0, transparent 30%), var(--paper); }
    [data-testid="stSidebar"], [data-testid="stExpandSidebarButton"] { display: none !important; }
    [data-testid="stAppViewContainer"] > .main { padding-top: 1rem; }
    h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif; letter-spacing: 0; color: var(--ink); }
    .brand-kicker, .page-kicker { color: var(--teal); font-size: 0.76rem; font-weight: 700; text-transform: uppercase; }
    .page-copy { max-width: 760px; color: var(--muted); font-size: 1rem; }
    .top-nav-brand { display: flex; align-items: center; gap: 10px; min-height: 48px; }
    .top-nav-mark { display: grid; place-items: center; width: 36px; height: 36px; border-radius: 8px; background: var(--ink); color: #fff; font-family: 'Space Grotesk', sans-serif; font-weight: 700; }
    .top-nav-name { color: var(--ink); font-family: 'Space Grotesk', sans-serif; font-size: .95rem; font-weight: 700; white-space: nowrap; }
    .top-nav-meta { color: var(--muted); font-size: .62rem; font-weight: 700; letter-spacing: .04em; }
    .top-nav-status { text-align: right; white-space: nowrap; }
    .top-nav-status span { display: block; color: var(--muted); font-size: .62rem; font-weight: 700; }
    .top-nav-status strong { color: var(--ink); font-family: 'Space Grotesk', sans-serif; font-size: .95rem; }
    .top-nav-divider { height: 1px; margin: 8px 0 24px; background: var(--line); }
    [data-testid="stRadioGroup"][aria-label="Workspace"] { display: flex; width: 100%; gap: 4px; padding: 4px; border: 1px solid var(--line); border-radius: 8px; background: #e8eff0; }
    [data-testid="stRadioGroup"][aria-label="Workspace"] > div { flex: 1 1 0; min-width: 0; }
    [data-testid="stRadioGroup"][aria-label="Workspace"] label[data-testid="stRadioOption"] { width: 100%; min-height: 38px; padding: 7px 10px; border: 1px solid transparent; border-radius: 6px; color: var(--muted); }
    [data-testid="stRadioGroup"][aria-label="Workspace"] label[data-testid="stRadioOption"] > div { justify-content: center; width: 100%; }
    [data-testid="stRadioGroup"][aria-label="Workspace"] label[data-testid="stRadioOption"] > div > div:first-child { display: none; }
    [data-testid="stRadioGroup"][aria-label="Workspace"] label[data-testid="stRadioOption"] p { margin: 0; font-size: .86rem; font-weight: 600; white-space: nowrap; }
    [data-testid="stRadioGroup"][aria-label="Workspace"] > div[data-selected="true"] label[data-testid="stRadioOption"] { border-color: #d9e7e8; background: #fff; color: var(--teal); box-shadow: 0 2px 7px rgba(27,41,46,.08); }
    .stButton > button[kind="primary"], .stFormSubmitButton > button {
        background: var(--teal); color: white; border: 0; border-radius: 6px;
        min-height: 46px; font-weight: 700;
    }
    .stButton > button[kind="primary"]:hover, .stFormSubmitButton > button:hover { background: #096b76; color: white; border: 0; }
    [data-testid="stMetric"] { background: #fff; padding: 16px; border: 1px solid var(--line); border-radius: 6px; }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stProgressBar"] > div > div { background: var(--teal); }
    div[data-testid="stForm"] { border: 0; padding: 0; }
    [data-testid="stExpander"] { background: rgba(255,255,255,.82); border: 1px solid var(--line); border-radius: 6px; }
    [data-testid="stTabs"] button[aria-selected="true"] { color: var(--teal); }
    @media (max-width: 700px) {
        .page-copy { font-size: .95rem; }
        [data-testid="stMetric"] { padding: 12px; }
        .top-nav-status, .top-nav-meta { display: none; }
        [data-testid="stRadioGroup"][aria-label="Workspace"] label[data-testid="stRadioOption"] { padding: 7px 4px; }
        [data-testid="stRadioGroup"][aria-label="Workspace"] label[data-testid="stRadioOption"] p { font-size: .76rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.session_state.setdefault("assessment_results", {})
st.session_state.setdefault("quiz_versions", {})
st.session_state.setdefault("quiz_attempts", {})


def page_header(kicker: str, title: str, description: str) -> None:
    st.markdown(f'<div class="page-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p class="page-copy">{description}</p>', unsafe_allow_html=True)
    st.divider()


def start_new_attempt(subject: str) -> None:
    versions = st.session_state["quiz_versions"]
    versions[subject] = versions.get(subject, 0) + 1
    st.session_state["assessment_results"].pop(subject, None)
    previous_attempt = st.session_state["quiz_attempts"].get(subject, [])
    excluded_indices = [item["question_index"] for item in previous_attempt]
    st.session_state["quiz_attempts"][subject] = create_attempt(
        subject, excluded_indices
    )


def render_prediction() -> None:
    page_header(
        "Campus recruitment / Predictor",
        "Placement prediction",
        "Compare your profile against the trained campus recruitment models. Use the assessment and study plan to work on the skills behind the score.",
    )
    model_view = st.radio(
        "Prediction view",
        ("Compare both", *MODEL_NAMES),
        horizontal=True,
        key="prediction_view",
    )

    with st.form("student_profile"):
        st.subheader("Student profile")
        academic, experience = st.columns(2, gap="large")

        with academic:
            st.markdown("#### Academic record")
            cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
            school_col, college_col = st.columns(2)
            with school_col:
                ssc_marks = st.number_input("SSC marks", min_value=0, max_value=100, value=70)
            with college_col:
                hsc_marks = st.number_input("HSC marks", min_value=0, max_value=100, value=70)
            aptitude = st.slider("Aptitude score", min_value=0, max_value=100, value=50)

        with experience:
            st.markdown("#### Experience and skills")
            internships = st.number_input("Internships", min_value=0, max_value=20, value=0)
            projects = st.number_input("Projects", min_value=0, max_value=50, value=0)
            certifications = st.number_input(
                "Workshops / certifications", min_value=0, max_value=50, value=0
            )
            soft_skills = st.slider(
                "Soft skills rating", min_value=0.0, max_value=5.0, value=3.0, step=0.1
            )
            yes_no_col, activities_col = st.columns(2)
            with yes_no_col:
                placement_training = st.selectbox("Placement training", ("Yes", "No"))
            with activities_col:
                extracurricular = st.selectbox(
                    "Extracurricular activities", ("Yes", "No")
                )

        submitted = st.form_submit_button(
            "Run placement prediction", type="primary", use_container_width=True
        )

    if submitted:
        st.session_state["submitted_profile"] = {
            "CGPA": cgpa,
            "SSC_Marks": ssc_marks,
            "HSC_Marks": hsc_marks,
            "AptitudeTestScore": aptitude,
            "Internships": internships,
            "Projects": projects,
            "Workshops/Certifications": certifications,
            "SoftSkillsRating": soft_skills,
            "PlacementTraining": placement_training,
            "ExtracurricularActivities": extracurricular,
        }

    profile = st.session_state.get("submitted_profile")
    if not profile:
        st.info("Complete the profile and run a prediction to see the model results.")
        return

    st.subheader("Prediction results")
    selected_models = MODEL_NAMES if model_view == "Compare both" else (model_view,)
    results = []
    failures = []
    for model_name in selected_models:
        try:
            results.append((model_name, predict(model_name, profile)))
        except Exception as error:
            failures.append((model_name, error))

    for model_name, error in failures:
        st.error(f"{model_name} could not be loaded: {error}")
    if failures:
        st.info("Install the pinned dependencies from requirements.txt, then restart the app.")

    if results:
        result_columns = st.columns(len(results), gap="medium")
        for column, (model_name, result) in zip(result_columns, results):
            with column:
                st.markdown(f"#### {model_name}")
                if result.label == "Placed":
                    st.success("Predicted outcome: Placed")
                else:
                    st.warning("Predicted outcome: Not placed")
                st.metric("Estimated placement probability", f"{result.placement_probability:.1%}")
                st.progress(result.placement_probability)
                st.caption(f"Model confidence in its selected class: {result.confidence:.1%}")

        if len(results) > 1:
            labels = {result.label for _, result in results}
            if len(labels) == 1:
                st.info("Both models predict the same placement outcome.")
            else:
                st.warning("The models disagree. Treat this as an uncertain result and review the profile.")
        st.caption("These estimates reflect model outputs, not a guarantee of placement.")


def render_assessment() -> None:
    page_header(
        "Placement preparation / Diagnostic",
        "Skill assessment",
        "Take a short original-question diagnostic in data structures and algorithms or aptitude. Your topic signals feed directly into the study plan.",
    )

    results: dict[str, Any] = st.session_state["assessment_results"]
    subject = st.radio("Choose a subject", tuple(QUIZZES), horizontal=True, key="quiz_subject")
    completed = len(results)
    status_col, detail_col = st.columns((1, 2))
    with status_col:
        st.metric("Assessments complete", f"{completed} / {len(QUIZZES)}")
    with detail_col:
        st.caption("Eight questions per subject. Treat topic-level results as a first diagnostic, not a formal certification.")

    version = st.session_state["quiz_versions"].get(subject, 0)
    attempts: dict[str, Any] = st.session_state["quiz_attempts"]
    if subject not in attempts:
        attempts[subject] = create_attempt(subject)
    attempt = attempts[subject]
    questions = tuple(
        QUIZZES[subject][item["question_index"]] for item in attempt
    )
    answers: dict[int, str | None] = {}
    displayed_options = []
    with st.form(f"quiz_form_{subject}"):
        st.subheader(f"{subject} diagnostic")
        st.caption(
            f"{QUESTIONS_PER_ASSESSMENT} shuffled questions from a {len(QUIZZES[subject])}-question bank. "
            "Questions and answer choices are mixed on each attempt."
        )
        for question_index, (question, attempt_item) in enumerate(zip(questions, attempt)):
            options = tuple(
                question.options[index] for index in attempt_item["option_order"]
            )
            displayed_options.append(options)
            answers[question_index] = st.radio(
                f"{question_index + 1:02}. {question.prompt}",
                options,
                index=None,
                key=f"answer_{subject}_{version}_{attempt_item['question_index']}",
            )
        submitted = st.form_submit_button(
            "Submit assessment", type="primary", use_container_width=True
        )

    if submitted:
        if any(answer is None for answer in answers.values()):
            st.warning("Answer all questions before submitting your assessment.")
        else:
            answer_indexes = {
                question_index: attempt[question_index]["option_order"][
                    displayed_options[question_index].index(answer)
                ]
                for question_index, answer in answers.items()
                if answer is not None
            }
            question_indices = [item["question_index"] for item in attempt]
            results[subject] = score_assessment(
                subject, answer_indexes, question_indices
            )
            st.session_state["assessment_results"] = results

    result = results.get(subject)
    if not result:
        return

    st.divider()
    st.subheader("Your result")
    score_col, correct_col, signal_col = st.columns(3)
    score_col.metric("Score", f"{result['score']}%")
    correct_col.metric("Correct", f"{result['correct']} / {result['total']}")
    weaker_topics = [
        topic
        for topic, topic_score in sorted(
            result["topic_scores"].items(), key=lambda item: item[1]["percent"]
        )
        if topic_score["percent"] < 100
    ]
    signal_col.metric("Topics to revisit", len(weaker_topics))
    st.progress(result["score"] / 100)

    topic_col, review_col = st.columns((1, 1), gap="large")
    with topic_col:
        st.markdown("#### Topic signals")
        for topic, topic_score in result["topic_scores"].items():
            st.markdown(f"**{topic}** · {topic_score['correct']} / {topic_score['total']}")
            st.progress(topic_score["percent"] / 100)
    with review_col:
        st.markdown("#### Answer review")
        for question_number, item in enumerate(result["review"], start=1):
            label = "Correct" if item["is_correct"] else "Review"
            with st.expander(f"{question_number:02}. {label} · {item['question']}"):
                st.markdown(f"**Your answer:** {item['selected']}")
                st.markdown(f"**Correct answer:** {item['answer']}")
                st.write(item["explanation"])

    st.button(
        "Retake this assessment",
        on_click=start_new_attempt,
        args=(subject,),
        key=f"retake_{subject}",
    )


def render_plan() -> None:
    page_header(
        "Placement preparation / Study plan",
        "Your 30-day plan",
        "A practical daily routine that gives extra time to weaker assessment areas, then builds toward timed mixed practice and a final simulation.",
    )

    results: dict[str, Any] = st.session_state["assessment_results"]
    if not results:
        st.info("Complete at least one subject assessment to create your personalized plan.")
        st.markdown("### Start with a baseline")
        st.write("The DSA and Aptitude diagnostics identify the topics that need the most practice.")
        return

    plan = build_30_day_plan(results)
    average_score = round(sum(result["score"] for result in results.values()) / len(results))
    weakest_subject = min(results, key=lambda subject: results[subject]["score"])
    metric_col, focus_col, coverage_col = st.columns(3)
    metric_col.metric("Baseline average", f"{average_score}%")
    focus_col.metric("Priority subject", weakest_subject)
    coverage_col.metric("Assessments used", f"{len(results)} / {len(QUIZZES)}")
    st.progress(average_score / 100)

    if len(results) < len(QUIZZES):
        missing_subjects = [subject for subject in QUIZZES if subject not in results]
        st.info(
            f"{', '.join(missing_subjects)} has not been assessed yet. Its plan days use a balanced foundation sequence; take that diagnostic for a more precise split."
        )

    st.markdown("#### Plan structure")
    st.markdown(
        "**Days 1-7** foundations  ·  **8-14** guided practice  ·  **15-21** timed sets  ·  **22-27** mixed revision  ·  **28-30** mock, review, and final simulation"
    )

    week_ranges = ((1, 7), (8, 14), (15, 21), (22, 30))
    week_tabs = st.tabs(("Week 1", "Week 2", "Week 3", "Week 4 + final"))
    for tab, (first_day, last_day) in zip(week_tabs, week_ranges):
        with tab:
            for item in plan[first_day - 1 : last_day]:
                with st.expander(
                    f"Day {item['day']:02}  /  {item['phase']}",
                    expanded=item["day"] == 1,
                ):
                    st.caption(
                        f"{item['subject']}  ·  {item['focus']}  ·  {item['minutes']} minutes"
                    )
                    st.write(item["task"])


brand_col, nav_col, status_col = st.columns((1.1, 4.2, 0.8), vertical_alignment="center")
with brand_col:
    st.markdown(
        '<div class="top-nav-brand"><span class="top-nav-mark">P</span>'
        '<div><div class="top-nav-name">Placement Lab</div>'
        '<div class="top-nav-meta">CAMPUS READINESS</div></div></div>',
        unsafe_allow_html=True,
    )
with nav_col:
    active_view = st.radio(
        "Workspace",
        ("Prediction", "Assessment", "30-day plan"),
        horizontal=True,
        label_visibility="collapsed",
        key="active_view",
    )
with status_col:
    assessment_count = len(st.session_state["assessment_results"])
    st.markdown(
        '<div class="top-nav-status"><span>ASSESSMENTS</span>'
        f"<strong>{assessment_count} / {len(QUIZZES)}</strong></div>",
        unsafe_allow_html=True,
    )
st.markdown('<div class="top-nav-divider"></div>', unsafe_allow_html=True)


if active_view == "Prediction":
    render_prediction()
elif active_view == "Assessment":
    render_assessment()
else:
    render_plan()