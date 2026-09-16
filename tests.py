import unittest
from models import Participant, Session
from analyzer import FitnessAnalyzer
from sample_data import get_sample_scenarios


class TestFitnessAnalyzer(unittest.TestCase):
    def setUp(self):
        self.participant = Participant("P001", 25, resting_hr=60, max_hr=190)
        self.analyzer = FitnessAnalyzer.create_default()
        self.scenarios = get_sample_scenarios()

    def test_resting_session(self):
        session = Session("S01", self.participant)
        for obs in self.scenarios["resting"]:
            session.add_observation(obs)
        res = self.analyzer.analyze(session)
        self.assertEqual(res["classification"], "resting")

    def test_invalid_sensor_data(self):
        session = Session("S05", self.participant)
        for obs in self.scenarios["invalid_sensor_data"]:
            session.add_observation(obs)
        res = self.analyzer.analyze(session)
        self.assertEqual(res["classification"], "insufficient_data")

if __name__ == "__main__":
    unittest.main()