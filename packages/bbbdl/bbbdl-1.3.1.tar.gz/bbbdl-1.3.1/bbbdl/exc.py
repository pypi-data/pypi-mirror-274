class BBBDLException(Exception):
    """
    An :class:`Exception` occoured in bbbdl.
    """


class MetadataNotFoundError(BBBDLException):
    """
    The metadata (``{base_url}/presentation/{meeting_id}/metadata.xml``) of the specified meeting could not be
    retrieved.
    """


class SourceNotFoundError(BBBDLException):
    """
    The specified url didn't return a successful HTTP status code (200 <= x < 300).
    """
