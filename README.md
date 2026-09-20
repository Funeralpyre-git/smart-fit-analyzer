```text
┌──────────────────────────────────────────────────────────────┐
│   ___                  _     ___ _ _                         │
│  / __|_ __  __ _ _ _ _| |_  | __(_) |_ _ _  ___ ___ ___      │
│  \__ \ '  \/ _` | '_/ _`  _| | _|| |  _| ' \/ -_|_-<_-<      │
│  |___/_|_|_\__,_|_| \__,_|_| |_| |_|\__|_||_\___/__/__/      │
│                                                              │
│   ♥ ---/\_/\_----/\_/\/\_----/\_/\_---  [ 125 BPM | 98% HR ] │
└──────────────────────────────────────────────────────────────┘


---
```
# Smart Fitness Session Analyzer
Selected Option: A\
Course: Problem-Solving with Scripting (ACIT4420-1 26H)\
Student Name:\
Student ID:

## 1. Overview
The Smart Fitness Session Analyzer is a Python application that processes, validates, analyzes, and classyfies wearable sensor time-series data collected during exercise sessions. Wearable fitness monitors generate biometric data like
- Heart rate
- Skin response
- Body temperature
- Activity level
- Signal quality

The application ingests simulated multi-sensor observation windows, validates readings against physical and signal quality constraints, compares session metrics against individual participant reference baselines, detects recovery trends, and classifies overall session intensity.

## 2. Repository Structure
The project is divided into modular Python files.

```
smart-fitness-analyzer/
│  
├── utils.py			# Standalone helper functions for validation, math, and report formatting
├── models.py			# Domain classes (Participants, Observation, Session)
├── analyzer.py			# Analysis hierarchy (BaseAnalyzer and FitnessAnalyzer)
├── sample_data.py		# Mock sensor streams for all 5 mandatory scenarios
├── main.py				# Application running all scenarios
├── tests.py			# Unit test suite verifying logic across scenarios and edge cases
├── data_generator.py	# Supplied data generator module
└── README.md			# Documentation
```
The codebase is decomposed into specialized modules to improve readability and maintainability:
* ```utils.py``` contains foundational, non-class utility functions for sensor schema validation, safe mathematical averaging, relative intensity calculations, and string report formatting.
* ```models.py``` houses core data models (Participant, Observation, Session) encapsulating participant baselines and t ime-series sensor windows.
* ```analyzer.py``` implements the analysis class hierarchy (BaseAnalyzer, FitnessAnalyzer) that processes session objects and applies classification rules.

## 3. Class Design
The application is structured around four primary classes, each adhering to the Single Responsibility Principle:</br> </br>
```Participant``` manages individual user demographic data and personal baseline reference values (```resting_hr```, ```max_hr```). It serves as the personal benchmark for computing relative exertion and intensity percentages. Also provides a ```@classmethod from_profile(product_dict, age)``` factory method to construct ```Participant``` instances directly from raw profile dictionaries produced by ```data_generator.py```</br> </br>
```Observation``` encapsulates a single time-window sensor reading. It parses raw measurement dictionaries, validates sensor ranges, and exposes cleaned, ready-only biometric properties.</br> </br>
```Session``` represents a complete workout session composed of sequential ```Observation``` windows. It manages time-series collections, calculates summary statistics (min, max, avg), filters invalid data, and evaluates tail-end recovery trends.</br> </br>
```BaseAnalyzer``` & ```FitnessAnalyzer``` evaluates session metrics and outputs structured classification dictionaries and rationales. It applies classification algorithms (resting, moderate activity, high activity, recovering, or insufficient data) and checks data completeness.

## 4. Object-Oriented Design
**Composition**\
Demonstrated in the ```Session``` class, which contains a collection of ```Observation``` objects and refrences a ```Participant``` object. A ```Session``` owns its observations and manages their lifecycles during analysis.</br> </br>
**Encapsulation**\
Demonstrated in ```Observation``` and ```Participant``` classes through protected attributes (e.g., ```_raw_data```, ```_resting_hr```, ```_max_hr```, ```_is_valid```). Access to these attributes is controlled via read-only ```@property``` decorators, preventing unauthorized direct modification.</br> </br>
**Inheritance & Method Overriding**\
```BaseAnalyzer``` serves as an abstract base class defining the ```analyze(session)``` interface. ```FitnessAnalyzer``` inherits from ```BaseAnalyzer``` and overrides ```analyze()``` to implement fitness-specific classification logic and threshold rules.</br> </br>
**Class Methods & Static Methods**
* Class Method (```@classmethod```):
	* ```Participant.from_profile(profile_dict, age)``` acts as factory constructor converting raw profile dictionaries from ```data_generator.py``` into ```Participant``` instances.
	* ```FitnessAnalyzer.create_default()``` acts as an alternative constructor for instantiating the analyzer.
* Static Method (```@staticmethod)```:
	*  ```FitnessAnalyzer.is_sufficient_data(usable_count), total_count)``` provides a utility function to determine if valid readings meet the minimum 50% data threshold without accessing instance state.

## 5. Standalone Utility Functions
The project includes four standalone utility functions for validation, math, and output formatting:
1. ```validate_sensor_reading(obs: dict) -> bool``` checks for required keys, validates physical biometric ranges (heart rate 30-220 bpm, Activity 0.0-1.0, Temp 20-45°C), and enforces signal quality >= 0.70.
2. ```compute_safe_average(values: list) -> float``` safely calculates the arithmetic mean over non-empty numerical lists.
3. ```calculate_relative_intensity(current_hr: float, max_hr: float) -> float``` compares exertion as a percentage of max heart rate (```(current_hr / max_hr) * 100```).
4. ```format_console_report(summary_dict) ->  str``` formats structured analysis dictionaries into human-readable console reports.

## 6. Assumptions & Classification Logic
**Data Validation Ruleset**\
An observation is flagged as invalid if:
* Any required key is missing from the dictionary.
* ```signal_quality``` is below 0.70.
* Biometric values fall outside physiological limits (e.g., heart rate < 30 or > 220 bpm, activity level < 0.0 or > 1.0.

**Classification Rules**
* **Insufficient Data**: Triggered if less than 50% of session observations are valid.
* **Resting**: Relative Heart Rate < 55% of max HR.
* **Moderate Activity**: 55% <= Relative Heart Rate < 75% of max HR.
* **High Activity**: Relative Heart Rate >= 75% of max HR.
* **Recovering**: Triggered when a session classified as moderate or high activity exhibits a significant drop in average heart rate (final 30% window avg HR drops below 85% of initial 70% of max HR.

## 7. Installation & Running Instructions
**Prerequisites**
* Python 3.8 or higher
* Only uses the Python standard library (no ```pandas```, ```numpy```, or any third-party packages required).
 > [!NOTE]
>On Windows systems where ```python3```is not aliased, use ```python main.py```insead.

**Instructions**
1. Clone the repository
	```
	git clone https://github.com/Funeralpyre-git/smart-fit-analyzer.git
	cd /smart-fit-analyzer
	```
2. Run the main application:
	```
	python3 main.py
	```
3. Run the test suite:
	```
	python3 -m unittest tests.py
	```
## 8. Example Output
```
--- Scenario: HIGH_ACTIVITY ---
=== FITNESS SESSION REPORT ===
Usable Samples : 10/10
Classification : moderate_activity
Rationale      : Heart rate indicates moderate activity (72.0% of max HR). 
Avg Heart Rate : 136.8 bpm
==============================
```

## 9. Scenario Coverage
The test suite in ```tests.py```validates five distinct operational scenarios supplied via ```data_generator.py```:
1. **Resting Session**: Low activity level and HR near baseline.
2. **Moderate Activity**: Sustained excercise at 55-74% relative HR.
3. **High Activity**: Intensive exercise at >= 75% relative HR.
4. **Activity Followed by Recovery**: Exertion phase followed by a sharp drop in HR/activity near session termination.
5. **Poor-Quality / Invalid Sensor Data**: Streams dominated by corrupted or out-of-bounds readings resulting in an ```insufficient_data``` output.

## 10. Known Limitations
- In-memory operations: Data is processed in-memory without persistent storage or database integration.
- Simulated inputs: Uses simulated batch observations generated by ```data_generator.py``` rather than real-time Bluetooth streaming inputs.
- Standard library: Metric calculations rely on standard Python arithmetic without external statistical modeling libraries like ```numpy``` or ```scipy```.
