HIVE = "hive"
TEMPERAMENT = "temperament"
HIVES = ["mozambeeque", "new beeland", "the beehamas", "puerto beeco"]


INSPECTION_HEADER = {
    HIVE: str,
    TEMPERAMENT: int,
    "brood_boxes": int,
    "supers": int,
    "dn4_brood": int,
    "dn4_stores": int,
    "sn4_brood": int,
    "sn4_stores": int,
    "eggs": bool,
    "larvae": bool,
    "drones": bool,
    "queen_cells": bool,
    "queen_found": bool,
}

DATE_COLS = ["inspection_date"]
PRIMARY_DATE_COL = "inspection_date"
