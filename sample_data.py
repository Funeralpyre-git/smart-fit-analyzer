from data_generator import generate_fitness_data

# imports and calls data_generator.py to generate sample datasets

def get_sample_scenarios() -> dict:
    scenario_mapping ={
        "resting": "resting",
        "moderate_activity": "moderate_activity",
        "high_activity": "high_activity",
        "recovery": "recovery",
        "invalid_sensor_data": "poor_quality"
    }

    scenarios = {}
    for name, gen_scenario in scenario_mapping.items():
        profile, observations = generate_fitness_data(
            participant_id="P101",
            scenario=gen_scenario,
            seed=42,
            number_of_windows=10
        )
        scenarios[name] = (profile, observations)
    return scenarios