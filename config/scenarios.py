# config/scenarios.py

from enum import Enum

class Scenario(Enum):
    WILDFIRE    = "wildfire_escalation"
    LOW_POWER   = "low_power_emergency"
    COMM_FAIL   = "communication_failure"
    NORMAL      = "normal"

SCENARIO_MENU = {
    "1": (Scenario.WILDFIRE,  "Escalada de Incêndio Crítico"),
    "2": (Scenario.LOW_POWER, "Emergência de Energia Baixa"),
    "3": (Scenario.COMM_FAIL, "Falha de Comunicação"),
    "4": (Scenario.NORMAL,    "Operação Normal"),
}

SCENARIO_DATASET_FILTERS = {
    Scenario.WILDFIRE:  lambda df: df[df["area"] > 10],
    Scenario.LOW_POWER: lambda df: df[df["area"] <= 5],
    Scenario.COMM_FAIL: lambda df: df[df["wind"] > 5],
    Scenario.NORMAL:    lambda df: df[df["area"] == 0],
}

SCENARIO_TELEMETRY_RANGES = {
    Scenario.WILDFIRE: {
        "battery":  (30.0, 60.0),
        "signal":   (60.0, 85.0),
        "geo":      (75.0, 92.0),
        "buffer":   (65,   95),
        "optical":  (80.0, 96.0),
    },
    Scenario.LOW_POWER: {
        "battery":  (5.0,  18.0),
        "signal":   (40.0, 65.0),
        "geo":      (55.0, 78.0),
        "buffer":   (10,   35),
        "optical":  (60.0, 82.0),
    },
    Scenario.COMM_FAIL: {
        "battery":  (50.0, 80.0),
        "signal":   (5.0,  22.0),
        "geo":      (30.0, 58.0),
        "buffer":   (55,   90),
        "optical":  (70.0, 90.0),
    },
    Scenario.NORMAL: {
        "battery":  (72.0, 100.0),
        "signal":   (82.0, 100.0),
        "geo":      (90.0, 100.0),
        "buffer":   (0,    25),
        "optical":  (92.0, 100.0),
    },
}

SCENARIO_HOTSPOT_FLOORS = {
    Scenario.WILDFIRE:  25,
    Scenario.LOW_POWER: 0,
    Scenario.COMM_FAIL: 8,
    Scenario.NORMAL:    0,
}