class SplitLedgerException(Exception):
    pass


class ValidationException(SplitLedgerException):
    pass


class LicensingException(SplitLedgerException):
    pass
