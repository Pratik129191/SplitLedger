class SaleStatus:
    MAX_LENGTH = 20
    DRAFT = "DRAFT"
    POSTED = "POSTED"
    CANCELLED = "CANCELLED"

    CHOICES = [
        (DRAFT, "Draft"),
        (POSTED, "Posted"),
        (CANCELLED, "Cancelled"),
    ]