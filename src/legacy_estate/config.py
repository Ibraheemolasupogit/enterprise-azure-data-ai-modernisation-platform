from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EstateProfile:
    """Scale settings for deterministic synthetic legacy estate generation."""

    customers: int
    depots: int
    vehicles: int
    shipments: int
    cases: int
    payment_ratio: float
    event_multiplier: int


PROFILE_SPECS: dict[str, EstateProfile] = {
    "tiny": EstateProfile(
        customers=8,
        depots=4,
        vehicles=8,
        shipments=18,
        cases=6,
        payment_ratio=0.7,
        event_multiplier=4,
    ),
    "development": EstateProfile(
        customers=120,
        depots=12,
        vehicles=80,
        shipments=1_000,
        cases=140,
        payment_ratio=0.78,
        event_multiplier=5,
    ),
    "performance": EstateProfile(
        customers=2_000,
        depots=40,
        vehicles=1_200,
        shipments=50_000,
        cases=8_000,
        payment_ratio=0.82,
        event_multiplier=6,
    ),
}


DEFAULT_SEED = 20260820

