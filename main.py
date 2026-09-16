import sample_data
from models import Participant, Session
from analyzer import FitnessAnalyzer
from sample_data import get_sample_scenarios
from utils import format_console_report

def main():
    participant = Participant("P101", age=30, resting_hr=65, max_hr=185)
    analyzer = FitnessAnalyzer.create_default()
    scenarios = sample_data.get_sample_scenarios() # retrieves from sample_data.py (WiP)

    for name, raw_logs in scenarios.items():
        session = Session(f"SESS-{name}", participant)
        for log in raw_logs:
            session.add_observation(log)

        # Produces a structured dict output and displays it
        result_dict = analyzer.analyze(session)
        print(f"\n--- Scenario: {name.upper()} ---")
        print(format_console_report(result_dict))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

