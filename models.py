from utils import validate_sensor_reading, compute_safe_average

class Observation:
    def __init__(self, raw_data: dict):
        self._raw_data = raw_data # protected attribute
        self._is_valid = validate_sensor_reading(raw_data) #calls function from utils.py

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def heart_rate(self) -> float:
        try:
            return self._raw_data.get("heart_rate", 0.0)
        except (ValueError, TypeError):
            return 0.0

    @property
    def activity_level(self) -> float:
        try:
            return self._raw_data.get("activity_level", 0.0)
        except (ValueError, TypeError):
            return 0.0

    @property
    def timestamp(self) -> float:
        try:
            return self._raw_data.get("timestamp", 0)
        except (ValueError, TypeError):
            return 0

class Participant:
    def __init__(self, participant_id: str, age: int, resting_hr: float, max_hr: float):
        if not isinstance(participant_id, str) or not participant_id.strip():
            raise ValueError("Participant ID must be a non-empty string.")
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be a positive integer.")
        if not isinstance(resting_hr, (int, float)) or resting_hr <= 0:
            raise ValueError("Resting HR must be a positive number.")
        if not isinstance(max_hr, (int, float)) or max_hr <= resting_hr:
            raise ValueError("Max HR must be a positive number greater than resting HR.")

        self.participant_id = participant_id
        self.age = age
        self._resting_hr = float(resting_hr)
        self._max_hr = float(max_hr)

    @classmethod
    # factory method constructing a participant from data_generator
    def from_profile(cls, profile: dict, age: int = 30):
        if not isinstance(profile, dict):
            raise TypeError("Profile must be a dictionary.")
        participant_id = profile.get("participant_id", "P001")
        resting_hr = profile.get("baseline_heart_rate", 65)
        max_hr = 220 - age
        return cls(participant_id=participant_id, age=age, resting_hr=resting_hr, max_hr=max_hr)

    @property
    def resting_hr(self) -> float:
        return self._resting_hr

    @property
    def max_hr(self) -> float:
        return self._max_hr

class Session:
    def __init__(self, session_id: str, participant: Participant):
        if not isinstance(participant, Participant):
            raise TypeError("Participant must be a participant.")
        self.session_id = session_id
        self.participant = participant # participant profile reference
        self._observations = [] # list of Observation objects

    # instantiates and stores an Observation object
    def add_observation(self, raw_obs_dict: dict):
        try:
            self._observations.append(Observation(raw_obs_dict))
        except Exception:
            self._observations.append(Observation({}))

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
        tail = valid[split_idx:]
        initial = valid[:split_idx]

        avg_tail_hr = compute_safe_average([o.heart_rate for o in tail])
        avg_init_hr = compute_safe_average([o.heart_rate for o in initial])

        return avg_tail_hr < (avg_init_hr * 0.85)

    @property
    def observations(self):
        return self._observations
