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
        return self._raw_data.get("heart_rate", 0.0)

    @property
    def activity_level(self) -> float:
        return self._raw_data.get("activity_level", 0.0)

    @property
    def timestamp(self) -> float:
        return self._raw_data.get("timestamp", 0)

class Participant:
    def __init__(self, participant_id: str, age: int, resting_hr: float, max_hr: float):
        self.participant_id = participant_id
        self.age = age
        self._resting_hr = resting_hr #protected attribute
        self._max_hr = max_hr # protected attribute

    @property
    def resting_hr(self) -> float:
        return self._resting_hr

    @property
    def max_hr(self) -> float:
        return self._max_hr

class Session:
    def __init__(self, session_id: str, participant: Participant):
        self.session_id = session_id
        self.participant = participant # participant profile reference
        self._observations = [] # list of Observation objects

    # instantiates and stores an Observation object
    def add_observation(self, raw_obs_dict: dict):
        self._observations.append(Observation(raw_obs_dict))

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
            "max_heart_rate": max(hrs),
            "min_heart_rate": min(hrs),
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
