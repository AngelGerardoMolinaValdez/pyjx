from enum import Enum

class XrayStatus(Enum):
    PASS = "PASS"
    TODO = "TODO"
    EXECUTING = "EXECUTING"
    FAIL = "FAIL"
    ABORTED = "ABORTED"
