# Gallery operating hours for the motor controller.
# Weekday keys use Python's datetime.weekday(): Monday=0 ... Sunday=6.
# Days omitted from this dict are treated as closed.

GALLERY_HOURS = {
    1: {"open": "12:00", "close": "17:55", "label": "Tuesday"},
    2: {"open": "12:00", "close": "17:55", "label": "Wednesday"},
    3: {"open": "12:00", "close": "17:55", "label": "Thursday"},
    4: {"open": "12:00", "close": "17:55", "label": "Friday"},
    5: {"open": "12:00", "close": "16:55", "label": "Saturday"},
}
