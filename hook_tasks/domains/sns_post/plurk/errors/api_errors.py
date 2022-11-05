class PlurkApiError(Exception):
    ...


class InValidData(PlurkApiError):
    ...


class EmptyContent(PlurkApiError):
    ...


class NoCommentPermission(PlurkApiError):
    ...


class AntiFloodError(PlurkApiError):
    ...


class SameContent(AntiFloodError):
    ...


class SpamDomain(AntiFloodError):
    ...


class TooManyNew(AntiFloodError):
    ...
