class MissingGcpProject(Exception):
    """Raised when GCP project ID couldn't be found."""


class MissingToken(Exception):
    """Raised when we fail to fetch token"""


class MissingHomeEnv(Exception):
    """Raised when missing $HOME env var"""
