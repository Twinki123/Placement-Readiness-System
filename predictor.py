from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATHS = {
    "Gradient Boosting": PROJECT_ROOT / "campus_recruitment_gb_model.pkl",
    "Tuned Random Forest": PROJECT_ROOT / "campus_recruitment_tuned_rf_model.pkl",
}
MODEL_NAMES = tuple(MODEL_PATHS)
FEATURE_COLUMNS = (
    "CGPA",
    "HSC_Marks",
    "Workshops/Certifications",
    "Internships",
    "Projects",
    "SoftSkillsRating",
    "PlacementTraining_Yes",
    "SSC_Marks",
    "ExtracurricularActivities_Yes",
    "AptitudeTestScore",
)


@dataclass(frozen=True)
class Prediction:
    label: str
    placement_probability: float
    confidence: float


@lru_cache(maxsize=len(MODEL_PATHS))
def load_model(model_name: str) -> Any:
    try:
        model_path = MODEL_PATHS[model_name]
    except KeyError as error:
        raise ValueError(f"Unknown model: {model_name}") from error

    if not model_path.is_file():
        raise FileNotFoundError(f"Model file not found: {model_path.name}")

    model = joblib.load(model_path)
    model_features = tuple(getattr(model, "feature_names_in_", ()))
    if model_features != FEATURE_COLUMNS:
        raise ValueError(
            f"{model_path.name} has an unexpected feature schema. "
            "The app expects the model's ten campus recruitment features."
        )
    return model


def build_feature_frame(profile: Mapping[str, Any]) -> pd.DataFrame:
    values = {
        "CGPA": profile["CGPA"],
        "HSC_Marks": profile["HSC_Marks"],
        "Workshops/Certifications": profile["Workshops/Certifications"],
        "Internships": profile["Internships"],
        "Projects": profile["Projects"],
        "SoftSkillsRating": profile["SoftSkillsRating"],
        "PlacementTraining_Yes": int(profile["PlacementTraining"] == "Yes"),
        "SSC_Marks": profile["SSC_Marks"],
        "ExtracurricularActivities_Yes": int(
            profile["ExtracurricularActivities"] == "Yes"
        ),
        "AptitudeTestScore": profile["AptitudeTestScore"],
    }
    return pd.DataFrame([[values[column] for column in FEATURE_COLUMNS]], columns=FEATURE_COLUMNS)


def predict(model_name: str, profile: Mapping[str, Any]) -> Prediction:
    model = load_model(model_name)
    features = build_feature_frame(profile)
    predicted_class = model.predict(features)[0]
    classes = list(model.classes_)
    positive_class_index = classes.index(1)
    probabilities = model.predict_proba(features)[0]
    placement_probability = float(probabilities[positive_class_index])
    label = "Placed" if int(predicted_class) == 1 else "Not placed"
    confidence = float(max(probabilities))
    return Prediction(label, placement_probability, confidence)