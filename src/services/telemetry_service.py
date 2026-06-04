# src/services/telemetry_service.py

import os
import random
import numpy as np
import pandas as pd

from config.scenarios import (
    Scenario,
    SCENARIO_DATASET_FILTERS,
    SCENARIO_TELEMETRY_RANGES,
    SCENARIO_HOTSPOT_FLOORS,
)

from src.telemetria import TelemetriaSnapshot

_df = None


def _carregar_dataset() -> pd.DataFrame:
    global _df

    if _df is None:
        path = os.path.join("data", "wildfire_dataset.csv")
        _df = pd.read_csv(path)

    return _df


def _hotspots_do_dataset(scenario: Scenario) -> int:
    df = _carregar_dataset()

    filtro = SCENARIO_DATASET_FILTERS.get(
        scenario,
        lambda df: df
    )

    subset = filtro(df)

    if subset.empty:
        subset = df

    row = subset.sample(1).iloc[0]

    raw_score = (
        row["area"]
        + (row["temp"] * 0.5)
        + (row["ISI"] * 0.3)
    )

    hotspots = int(np.clip(raw_score / 5, 0, 50))

    floor = SCENARIO_HOTSPOT_FLOORS.get(scenario, 0)

    return max(hotspots, floor)


def _validar_snapshot(t: TelemetriaSnapshot) -> TelemetriaSnapshot:
    return TelemetriaSnapshot(
        thermal_hotspots=max(0, min(50, t.thermal_hotspots)),
        battery_level=round(max(0.0, min(100.0, t.battery_level)), 1),
        signal_strength=round(max(0.0, min(100.0, t.signal_strength)), 1),
        geo_accuracy=round(max(0.0, min(100.0, t.geo_accuracy)), 1),
        image_buffer_queue=max(0, min(100, t.image_buffer_queue)),
        optical_integrity=round(max(0.0, min(100.0, t.optical_integrity)), 1),
    )


def gerar_telemetria_dataset(
    scenario: Scenario = Scenario.NORMAL
) -> TelemetriaSnapshot:

    thermal_hotspots = _hotspots_do_dataset(scenario)

    ranges = SCENARIO_TELEMETRY_RANGES.get(
        scenario,
        SCENARIO_TELEMETRY_RANGES[Scenario.NORMAL]
    )

    snapshot = TelemetriaSnapshot(
        thermal_hotspots=thermal_hotspots,

        battery_level=round(
            random.uniform(*ranges["battery"]),
            1
        ),

        signal_strength=round(
            random.uniform(*ranges["signal"]),
            1
        ),

        geo_accuracy=round(
            random.uniform(*ranges["geo"]),
            1
        ),

        image_buffer_queue=random.randint(
            *ranges["buffer"]
        ),

        optical_integrity=round(
            random.uniform(*ranges["optical"]),
            1
        ),
    )

    return _validar_snapshot(snapshot)