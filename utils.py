##### utils.py defines the 4 required standalone functions
##### for validation, math, and output presentation.

# checks for missing keys, physical bounds, and signal quality
def validate_sensor_reading(obs: dict) -> bool:
    required_keys = {"timestamp", "heart_rate", "skin_response", "temperature", "activity_level", "signal_quality"}
    if not required_keys.issubset(obs.keys()):
        return False
    if not (30 <= obs["heart_rate"] <= 220 and 0.0 <= obs["activity_level"] <= 1.0):
        return False
    return obs["signal_quality"] >= 0.70

# calculates mean safely over non-empty lists
def compute_safe_average(values: list) -> float:
    return round(sum(values) / len(values), 2) if values else 0.0

# calculates relative intensity as a percentage of participation max HR
def calculate_relative_intensity(current_hr: float, max_hr: float) -> float:
    return round((current_hr / max_hr) * 100, 2) if max_hr > 0 else 0.0

# converts a structured result dictionary into a readable console string
def format_console_report(summary_dict: dict) -> str:
    return(
    f"=== FITNESS SESSION REPORT ===\n"
    f"Usable Samples : {summary_dict['usable_observations']}/{summary_dict['total_observations']}\n"
    f"Classification : {summary_dict['classification']}\n"
    f"Rationale      : {summary_dict['rationale']}\n"
    f"Avg Heart Rate : {summary_dict['summaries'].get('avg_heart_rate', 'N/A')} bpm\n"
    f"=============================="
    )

