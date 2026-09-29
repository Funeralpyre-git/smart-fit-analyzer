##### custom exception classes #####

# Raised when an identifier is invalid
class InvalidIdentifierError(ValueError):
    pass

# Raised when a CSV row contains invalid types, missing fields, or out-of-range values
class InvalidRecordError(ValueError):
    pass