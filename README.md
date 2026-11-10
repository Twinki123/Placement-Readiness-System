# Placement Readiness System

A Streamlit app for campus placement preparation. It combines placement predictions from trained Gradient Boosting and tuned Random Forest models with randomized DSA and Aptitude assessments and a personalized 30-day study plan.

## Run locally

From the project root on Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Project files

- `app.py`: Streamlit interface and application flow.
- `assessment.py`: question banks, randomized quiz attempts, scoring, and 30-day plan generation.
- `predictor.py`: model loading, feature preparation, and predictions.
- `campus_recruitment_gb_model.pkl`: Gradient Boosting model artifact.
- `campus_recruitment_tuned_rf_model.pkl`: Tuned Random Forest model artifact.
- `project.md`: Detailed project and code guide.

The model files are loaded with joblib. Keep scikit-learn at version 1.6.1, as pinned in `requirements.txt`, to match the version used to serialize the artifacts. Quiz results and student inputs are held in Streamlit session state and are not persisted between sessions.