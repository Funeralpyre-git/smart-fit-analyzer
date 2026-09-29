##### regex validation and sensor checks #####
import re
from exceptions import InvalidIdentifierError

# regex patterns anchored with full-match behavior
PARTICIPANT_ID_PATTERN = re.compile(r"^P\d{3}$")
SESSION_ID_PATTERN = re.compile(r"^FIT-\d{4}-\d{3}$")

# validates participant identifier format (P followed by 3 digits)
def validate_participant_id(participant_id: str) -> bool:
    if not isinstance(participant_id, str) or not PARTICIPANT_ID_PATTERN.match(participant_id.strip()):
        raise InvalidIdentifierError("Invalid Participant ID format: '{participant_id}'. Expected format: 'P001'.")
    return True

# validates session identifier format (FIT-YYYY-NNN)
def validate_session_id(session_id: str) -> bool:
    if not isinstance(session_id, str) or not SESSION_ID_PATTERN.match(session_id.strip()):
        raise InvalidIdentifierError("Invalid Session ID format: '{session_id}'. Expected format: 'FIT-2026-0001'.")
    return True

# checks various physiological ranges and signal quality threshold
def validate_sensor_values(heart_rate: float, activity_level: float, temperature: float, signal_quality: float) -> bool:
    if not (30.0 <= heart_rate <= 220.0):
        return False
    if not (0.0 <= activity_level <= 1.0):
        return False
    if not (0.0 <= temperature <= 45.0):
        return False
    if signal_quality <= 0.70:
        return False
    return True