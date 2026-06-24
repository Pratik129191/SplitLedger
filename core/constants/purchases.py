class PurchaseStatus:
    MAX_LENGTH = 30
    POSTED = 'POSTED'
    CANCELLED = 'CANCELLED'

    CHOICES = (
        (POSTED, 'POSTED'),
        (CANCELLED, 'CANCELLED'),
    )