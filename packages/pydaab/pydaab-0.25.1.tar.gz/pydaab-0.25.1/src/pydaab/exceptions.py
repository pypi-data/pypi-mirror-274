class PydaabException(Exception):
    """
    Base class for any Pydaab exception
    """


class TooManyMissingFrames(PydaabException):
    pass


class InvalidDuration(PydaabException):
    pass


class InvalidTag(PydaabException):
    pass


class InvalidID3TagVersion(PydaabException):
    pass


class CouldntDecodeError(PydaabException):
    pass


class CouldntEncodeError(PydaabException):
    pass


class MissingAudioParameter(PydaabException):
    pass
