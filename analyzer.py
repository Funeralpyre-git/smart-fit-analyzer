from utils import calculate_relative_intensity
from models import Session

class BaseAnalyzer:
    def analyze(self, session: Session) -> dict:
        raise NotImplementedError("Subclasses must override analyze()")


##### Derived analyzer overriding base behavior for fitness data #####
class FitnessAnalyzer(BaseAnalyzer):
    @classmethod
    # class method acting as an alternative constructor
    def create_default(cls):
        return cls()

    @staticmethod
    def is_sufficient_data(usable_count: int, total_count: int) -> bool:
        if total_count == 0:
            return False
        return (usable_count / total_count) >= 0.50

    def analyze(self, session: Session) -> dict:
        valid_obs = session.get_valid_observations()
        total_obs = len(session._observations)
        usable_obs = len(valid_obs)

        # checks for insufficient data scenario
        if not self.is_sufficient_data(usable_obs, total_obs):
            return {
                "usable_observations": usable_obs,
                "total_observations": total_obs,
                "classification": "insufficient_data",
                "rationale": "More than 50% of sensor readings were invalid or poor quality.",
                "summaries": {}
            }

        summaries = session.calculate_summaries()
        avg_hr = summaries["avg_heart_rate"]
        part = session.participant
        rel_hr = calculate_relative_intensity(avg_hr, part.max_hr)

        # classify based on relative intensity thresholds
        if rel_hr < 55:
            classification = "resting"
            rationale = f"Heart rate remained near resting baseline ({rel_hr}% of max HR). "
        elif rel_hr < 75:
            classification = "moderate_activity"
            rationale = f"Heart rate indicates moderate activity ({rel_hr}% of max HR). "
        else:
            classification = "high_activity"
            rationale = f"Heart rate indicates high activity ({rel_hr}% of max HR). "

        # check for recovery post-activity
        if classification in ["moderate_activity", "high_activity"] and session.detect_recovery_trend():
            classification = "recovering"
            rationale += "Significant decline in heart rate detected towards session end."

        return {
            "usable_observations": usable_obs,
            "total_observations": total_obs,
            "classification": classification,
            "rationale": rationale,
            "summaries": summaries,
        }