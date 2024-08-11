from enum import Enum

class JwtError(Enum):
    INVALID = "invalid_token"
    NO_TOKEN = "no_token"