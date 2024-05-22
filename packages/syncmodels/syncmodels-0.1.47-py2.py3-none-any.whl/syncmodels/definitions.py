import re
from enum import Enum

# from .models import (
#     BudgetTypeEnum,
#     TravelPartyCompositionEnum,
# )

DEFAULT_LANGUAGE = "es"

MODEL_TABLE = "model"

UID_TYPE = str

MONOTONIC_KEY = "wave__"
MONOTONIC_SINCE = "since__"
MONOTONIC_SINCE_KEY = "since_key__"
MONOTONIC_SINCE_VALUE = "since_value__"
ALT_KEY = "id__"
FORCE_SAVE = "__save"
REG_PRIVATE_KEY = r".*__$"
REG_FQID = r"((?P<table>\w+):)?(?P<uid>\w+)$"


def filter_4_compare(data):
    """Filter data to be used for comparison"""
    result = {
        key: value for key, value in data.items() if not re.match(REG_PRIVATE_KEY, key)
    }
    # check id:
    uid = result.get("id")
    if uid is not None:
        m = re.match(REG_FQID, uid)
        if m:
            result["uid"] = m.group("uid")

    return result


# ----------------------------------------------------------
# enumerate helpers
# ----------------------------------------------------------
