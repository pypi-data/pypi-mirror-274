class PyenergiError(Exception):
    """Base class for all Pyenergy-related errors."""


class MissingCredentialsError(PyenergiError):
    """Raised when required credentials are not provided."""


class AuthenticationError(PyenergiError):
    """Raised for issues related to authenticating with the myenergi API."""


class DirectorError(PyenergiError):
    """Raised for issues related to the myenergi Director."""
