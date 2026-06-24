class StockMovementTypes:
    MAX_LENGTH = 30
    PURCHASE = 'PURCHASE'
    SALE = 'SALE'
    SALE_CANCEL = 'SALE_CANCEL'
    PURCHASE_CANCEL = 'PURCHASE_CANCEL'
    MANUAL_INCREASE = 'MANUAL_INCREASE'
    MANUAL_DECREASE = 'MANUAL_DECREASE'

    CHOICES = (
        (PURCHASE, 'Purchase'),
        (SALE, 'Sale'),
        (SALE_CANCEL, 'Sale Cancel'),
        (PURCHASE_CANCEL, 'Purchase Cancel'),
        (MANUAL_INCREASE, 'Manual Increase'),
        (MANUAL_DECREASE, 'Manual Decrease'),
    )


