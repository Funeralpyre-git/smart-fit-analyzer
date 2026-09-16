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
├── utils.py		# Standalone helper functions for validation, math, and report formatting
├── models.py		# Domain classes (Participants, Observation, Session)
├── analyzer.py		# Analysis hierarchy (BaseAnalyzer and FitnessAnalyzer)
├── sample_data.py	# Mock sensor streams for all 5 mandatory scenarios
├── main.py			# Application running all scenarios
├── tests.py		# Unit test suite verifying logic across scenarios and edge cases
└── README.md		# Documentation
```
The codebase is decomposed into specialized modules to improve readability and maintainability:
* ```utils.py``` contains foundational, non-class utility functions for sensor schema validation, safe mathematical averaging, relative intensity calculations, and string report formatting.
* ```models.py``` houses core data models (Participant, Observation, Session) encapsulating participant baselines and t ime-series sensor windows.
* ```analyzer.py``` implements the analysis class hierarchy (BaseAnalyzer, FitnessAnalyzer) that processes session objects and applies classification rules.

## 3. Class Design
The application is structured around four primary classes, each adhering to the Single Responsibility Principle:</br> </br>
```Participant``` manages individual user demographic data and personal baseline reference values (```resting_hr```, ```max_hr```). It serves as the personal benchmark for computing relative exertion and intensity percentages.</br> </br>
```Observation``` encapsulates a single time-window sensor reading. It parses raw measurement dictionaries, validates sensor ranges, and exposes cleaned, ready-only biometric properties.</br> </br>
```Session``` represents a complete workout session composed of sequential ```Observation``` windows. It manages time-series collections, calculates summary statistics (min, max, avg), filters invalid data, and evaluates tail-end recovery trends.</br> </br>
```BaseAnalyzer``` & ```FitnessAnalyzer``` evaluates session metrics and outputs structured classification dictionaries and rationales. It applies classification algorithms (resting, moderate activity, high activity, recovering, or insufficient data) and checks data completeness.\

## 4. Object-Oriented Design
**Composition**\
Demonstrated in the ```Session``` class, which contains a collection of ```Observation``` objects and refrences a ```Participant``` object. A ```Session``` owns its observations and manages their lifecycles during analysis.</br> </br>
**Encapsulation**\
Demonstrated in ```Observation``` and ```Participant``` classes through protected attributes (e.g., ```_raw_data```, ```_resting_hr```, ```_max_hr```, ```_is_valid```). Access to these attributes is controlled via read-only ```@property``` decorators, preventing unauthorized direct modification.</br> </br>
**Inheritance & Method Overriding**\
```BaseAnalyzer``` serves as an abstract base class defining the ```analyze(session)``` interface. ```FitnessAnalyzer``` inherits from ```BaseAnalyzer``` and overrides ```analyze()``` to implement fitness-specific classification logic and threshold rules.</br> </br>
**Class Methods & Static Methods**\
* Class Method (```@classmethod```):
  ```FitnessAnalyzer.create_default()``` acts as an alternative constructor for instantiating the analyzer.
* Static Method (```@staticmethod):
  ```FitnessAnalyzer.is_sufficient_data(usable_count), total_count)``` provides a utility function to determine if valid readings meet the minimum 50% data threshold without accessing instance state.

## 5. Standalone Utility Functions


## 6. Assumptions & Classification Logic


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
--- Scenario: MODERATE_ACTIVITY ---
=== FITNESS SESSION REPORT ===
Usable Samples : 5/5
Classification : moderate_activity
Rationale      : Heart rate indicates moderate activity (67.57% of max HR). 
Avg Heart Rate : 125.0 bpm
==============================
```

## 9. Scenario Coverage

## 10. Known Limitations
- In-memory operations
- Simulated inputs
- Standard library


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
