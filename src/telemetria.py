# src/telemetria.py

from dataclasses import dataclass


@dataclass
class TelemetriaSnapshot:
    thermal_hotspots: int       # 0–50 focos detectados
    battery_level: float        # 0.0–100.0 %
    signal_strength: float      # 0.0–100.0 %
    geo_accuracy: float         # 0.0–100.0 %
    image_buffer_queue: int     # 0–100 imagens na fila
    optical_integrity: float    # 0.0–100.0 %