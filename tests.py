import unittest
from models import Participant, Session
from analyzer import FitnessAnalyzer
from sample_data import get_sample_scenarios


class TestFitnessAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = FitnessAnalyzer.create_default()
        self.scenarios = get_sample_scenarios()

    # helper method to unpack profile and observation and construct session
    def _run_scenario(self, scenario_key: str, age: int = 30) -> dict:
        profile_dict, observations = self.scenarios[scenario_key]
        participant = Participant.from_profile(profile_dict, age=age)
        session = Session(f"TEST-{scenario_key.upper()}", participant)
        for obs in observations:
            session.add_observation(obs)
        return self.analyzer.analyze(session)

    ###########################
    # 5 operational scenarios #
    ###########################

    # resting
    def test_resting_session(self):
        res = self._run_scenario("resting", age=30)
        self.assertEqual(res["classification"], "resting")
        self.assertGreaterEqual(res["usable_observations"], 5)

    # moderate
    def test_moderate_activity_session(self):
        res = self._run_scenario("moderate_activity", age=30)
        self.assertEqual(res["classification"], "moderate_activity")

    # high activity
    def test_high_activity_session(self):
        res = self._run_scenario("high_activity", age=50)
        self.assertEqual(res["classification"], "high_activity")

    # recovery
    def test_recovery_session(self):
        res = self._run_scenario("recovery", age=50)
        self.assertEqual(res["classification"], "recovering")

    # invalid data
    def test_invalid_sensor_data(self):
        res = self._run_scenario("invalid_sensor_data", age=30)
        self.assertEqual(res["classification"], "insufficient_data")

    ####################################
    # utility functions and validation #
    ####################################
    def test_participant_validation(self):
        p = Participant("P100", age=25, resting_hr=60, max_hr=195)
        self.assertEqual(p.resting_hr, 60.0)
        self.assertEqual(p.max_hr, 195.0)

        with self.assertRaises(ValueError):
            Participant("", age=25, resting_hr=60, max_hr=195)

    def test_analyzer_static_and_class_method(self):
        self.assertTrue(FitnessAnalyzer.is_sufficient_data(5, 10))
        self.assertFalse(FitnessAnalyzer.is_sufficient_data(4, 10))

if __name__ == "__main__":
    unittest.main()