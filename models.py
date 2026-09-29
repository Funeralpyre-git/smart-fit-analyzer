from utils import validate_sensor_reading, compute_safe_average, calculate_relative_intensity
from validators import validate_participant_id, validate_session_id

class Observation:
    def __init__(self, timestamp: int, heart_rate: float, skin_response: float, temperature: float, activity_level: float, signal_quality: float, is_valid: bool = True):
        self.timestamp = int(timestamp)
        self.heart_rate = float(heart_rate)
        self.skin_response = float(skin_response)
        self.temperature = float(temperature)
        self.activity_level = float(activity_level)
        self.signal_quality = float(signal_quality)
        self._is_valid = bool(is_valid)

    @property
    def is_valid(self) -> bool:
        return self._is_valid

class Participant:
    def __init__(self, participant_id: str, name: str, resting_hr: float, max_hr: float= 185.0):
        validate_participant_id(participant_id)
        self.participant_id = participant_id.strip()
        self.name = name.strip() if name else "unknown"

        self._resting_hr = float(resting_hr)
        self._max_hr = float(max_hr)

    @property
    def resting_hr(self) -> float:
        return self._resting_hr

    @property
    def max_hr(self) -> float:
        return self._max_hr

class Session:
    def __init__(self, session_id: str, participant: Participant):
        validate_session_id(session_id)
        self.session_id = session_id.strip()
        self.participant = participant # participant profile reference
        self._observations = [] # list of Observation objects

    # instantiates and stores an Observation object
    def add_observation(self, obs: Observation):
        if isinstance(obs, Observation):
            self._observations.append(obs)

    # filters out invalid or poor-quality observations
    def get_valid_observations(self) -> list:
        return [obs for obs in self._observations if obs.is_valid]

    # computes min, max, and average metrics for valid data
    def calculate_summaries(self) -> dict:
        valid = self.get_valid_observations()
        if not valid:
            return {}
        hrs = [o.heart_rate for o in valid]
        acts = [o.activity_level for o in valid]
        return {
            "avg_heart_rate": compute_safe_average(hrs),
            "max_heart_rate": round(max(hrs), 2),
            "min_heart_rate": round(min(hrs), 2),
            "avg_activity": compute_safe_average(acts)
        }

    def detect_recovery_trend(self) -> bool:
        valid = self.get_valid_observations()
        if len(valid) < 4:
            return False

        split_idx = int(len(valid) * 0.7)
        initial = valid[:split_idx]
        tail = valid[split_idx:]
        if not initial or not tail:
            return False

        avg_init_hr = compute_safe_average([o.heart_rate for o in initial])
        avg_tail_hr = compute_safe_average([o.heart_rate for o in tail])
        
        return avg_tail_hr < (avg_init_hr * 0.85)

    '''
    @property
    def observations(self):
        return self._observations
    '''