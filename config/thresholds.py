# config/thresholds.py

RISK_THRESHOLDS = {
    "hotspots_critical": 25,
    "hotspots_warning":  12,
    "hotspots_elevated": 5,
    "battery_emergency_critical": 10,
    "battery_emergency":         20,
    "battery_warning":           35,
    "signal_failure":    20,
    "signal_degraded":   50,
    "geo_critical":      40,
    "geo_degraded":      65,
    "buffer_critical":   85,
    "buffer_elevated":   65,
    "optical_failure":   60,
    "optical_degraded":  75,
}

SEVERITY_LEVELS = {
    "EMERGENCY": 70,
    "CRITICAL":  45,
    "WARNING":   20,
    "NOMINAL":   0,
}