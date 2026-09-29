import unittest
from pathlib import Path
from exceptions import InvalidIdentifierError
from validators import validate_participant_id, validate_session_id
from models import Participant, Session
from analyzer import FitnessAnalyzer

class TestAssignment2(unittest.TestCase):
    def test_regex_validation(self):
        # valid IDs
        self.assertTrue(validate_participant_id("P001"))
        self.assertTrue(validate_session_id("FIT-2026-001"))

        # invalid IDs throwing custom exceptions
        with self.assertRaises(InvalidIdentifierError):
            validate_participant_id("P1")
        with self.assertRaises(InvalidIdentifierError):
            validate_session_id("FIT-26-101")

    def test_insufficient_data_handling(self):
        p = Participant("P001", "Jeff", resting_hr=67)
        session = Session("FIT-2026-001", p)
        analyzer = FitnessAnalyzer.create_default()

        # session with 0 valid observations should classify as insufficient_data
        res = analyzer.analyze(session)
        self.assertEqual(res["classification"], "insufficient_data")

if __name__ == "__main__":
    unittest.main()