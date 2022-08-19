class MetabaseApiException(Exception):
    pass


class AuthenticationFailure(MetabaseApiException):
    pass


class EmptyDataReceived(MetabaseApiException):
    pass


class InvalidDataReceived(MetabaseApiException):
    pass


class InvalidParameters(MetabaseApiException):
    pass


class RequestFailure(MetabaseApiException):
    pass


class ItemNotFound(MetabaseApiException):
    pass


class ItemInPersonalCollection(MetabaseApiException):
    pass


class NoUpdateProvided(MetabaseApiException):
    pass
