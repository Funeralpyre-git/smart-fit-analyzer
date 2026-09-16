def get_sample_scenarios():
    return {
        "resting": [
            {"timestamp": i,
             "heart_rate": 62,
             "skin_response": 1.1,
             "temperature": 32.5,
             "activity_level": 0.1,
             "signal_quality": 0.95
             }
            for i in range(1, 6)
        ],
        "moderate_activity": [
            {"timestamp": i,
             "heart_rate": 125,
             "skin_response": 2.5,
             "temperature": 33.8,
             "activity_level": 0.6,
             "signal_quality": 0.91
             }
            for i in range(1, 6)
        ],
        "high_activity": [
            {"timestamp": i,
             "heart_rate": 170,
             "skin_response": 3.8,
             "temperature": 35.1,
             "activity_level": 0.9,
             "signal_quality": 0.92
             }
            for i in range(1, 6)
        ],
        "recovery": [
            {"timestamp": 1, "heart_rate": 165, "skin_response": 3.5, "temperature": 34.5, "activity_level": 0.85, "signal_quality": 0.90},
            {"timestamp": 2, "heart_rate": 160, "skin_response": 3.2, "temperature": 34.2, "activity_level": 0.80, "signal_quality": 0.92},
            {"timestamp": 3, "heart_rate": 120, "skin_response": 2.1, "temperature": 33.5, "activity_level": 0.30, "signal_quality": 0.91},
            {"timestamp": 4, "heart_rate": 95, "skin_response": 1.5, "temperature": 33.0, "activity_level": 0.15, "signal_quality": 0.93}
        ],
        "invalid_sensor_data": [
            {"timestamp": i, "heart_rate": -1, "skin_response": 0.0, "temperature": 0.0, "activity_level": 1.5, "signal_quality": 0.20}
            for i in range(1,6)
        ]
    }