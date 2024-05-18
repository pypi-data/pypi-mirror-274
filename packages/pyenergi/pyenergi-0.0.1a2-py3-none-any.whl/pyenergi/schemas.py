import logging
from datetime import date, datetime, time
from enum import IntEnum, StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field, validator

logger = logging.getLogger(__name__)


class PlugStatus(StrEnum):
    EV_DISCONNECTED = "A"
    """Not EV is connected."""

    EV_CONNECTED = "B1"
    """An EV is connected."""

    WAITING_FOR_EV = "B2"
    """The Zappi is waiting for the connected EV to allow charging to begin."""

    EV_READY_TO_CHARGE = "C1"
    """An EV is connected, and ready to charge."""

    CHARGING = "C2"
    """An EV is connected, and charging."""

    FAULT = "F"
    """The electrical connection to the EV has faulted."""


class ChargeStatus(IntEnum):
    PAUSED = 1
    """Charging is paused."""

    CHARGING = 3
    """Charging is underway."""

    BOOSTING = 4
    """Charging is underway, via a 'boost'."""

    COMPLETE = 5
    """Charging is complete."""


class ChargeMode(IntEnum):
    FAST = 1
    """Fast"""

    ECO = 2
    """Eco"""

    ECO_PLUS = 3
    """Eco+"""

    STOPPED = 4
    """Stopped"""


class SmartBoostConfigured:
    smart_boost_start_time_hour: int
    smart_boost_start_time_minute: int
    smart_boost_energy_to_add: int


class ApiObject(BaseModel):
    pass


class CTType(StrEnum):
    INTERNAL_LOAD = "Internal Load"
    BATTERY = "AC Battery"
    MONITOR = "Monitor"
    GENERATION_AND_BATTERY = "Gen & Battery"
    STORAGE = "Storage"
    GENERATION = "Generation"
    GRID = "Grid"


class ZappiStatus(ApiObject):
    serial_number: int = Field(alias="sno")

    firmware_version: str = Field(alias="fwv")
    new_bootloader_available: bool = Field(alias="newBootloaderAvailable")

    plug_status: PlugStatus = Field(alias="pst")
    charge_status: ChargeStatus = Field(alias="sta")
    charge_mode: ChargeMode = Field(alias="zmo")

    lock_status: int = Field(alias="lck")

    command_timer: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 253, 254, 255] = Field(
        alias="cmt"
    )

    current_date: date = Field(alias="dat")
    current_time: time = Field(alias="tim")
    is_daylight_savings: bool = Field(alias="dst")

    ct_1_type: CTType | None = Field(alias="ectt1", default=None)
    ct_1_power: int | None = Field(alias="ectp1", default=None)
    ct_2_type: CTType | None = Field(alias="ectt2", default=None)
    ct_2_power: int | None = Field(alias="ectp2", default=None)
    ct_3_type: CTType | None = Field(alias="ectt3", default=None)
    ct_3_power: int | None = Field(alias="ectp3", default=None)
    ct_4_type: CTType | None = Field(alias="ectt4", default=None)
    ct_4_power: int | None = Field(alias="ectp4", default=None)
    ct_5_type: CTType | None = Field(alias="ectt5", default=None)
    ct_5_power: int | None = Field(alias="ectp5", default=None)
    ct_6_type: CTType | None = Field(alias="ectt6", default=None)
    ct_6_power: int | None = Field(alias="ectp6", default=None)

    diversion_amount: int = Field(alias="div")
    priority: int = Field(alias="pri")

    minimum_green_level: int = Field(alias="mgl")

    is_boosting: bool = Field(alias="bsm")

    smart_boost_end_time_hour: int | None = Field(alias="sbh", default=None)
    smart_boost_end_time_minute: int | None = Field(alias="sbm", default=None)
    smart_boost_energy_to_add: int | None = Field(alias="sbk", default=None)

    scheduled_boost_hour: int | None = Field(alias="tbh", default=None)
    scheduled_boost_minute: int | None = Field(alias="tbm", default=None)
    scheduled_boost_energy_to_add: int | None = Field(alias="tbk", default=None)

    grid_frequency: float = Field(alias="frq")
    grid_voltage: float = Field(alias="vol")
    phases: Literal[1, 3] = Field(alias="pha")
    phase_setting: str = Field(alias="phaseSetting")

    generating_power: int = Field(alias="gen")

    grid_power: int = Field(alias="grd")

    # Not sure yet
    bst: int
    tz: int
    che: int
    bss: int
    zs: int
    being_tampered_with: bool = Field(alias="beingTamperedWith")
    battery_discharge_enabled: bool = Field(alias="batteryDischargeEnabled")
    g100_lockout_state: str | None = Field(alias="g100LockoutState")

    @validator(*[f"ct_{n + 1}_type" for n in range(6)], pre=True)
    @classmethod
    def validate_ct_type(cls, value: Any):
        return None if value == "None" else value

    @validator("current_date", pre=True)
    @classmethod
    def validate_current_date(cls, value: Any):
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()  # noqa: DTZ007
        except ValueError:
            return value

    @validator("g100_lockout_state")
    @classmethod
    def validate_g100_lockout_state(cls, value: str) -> str | None:
        return None if value == "NONE" else value


class AllZappisStatusResponse(ApiObject):
    zappi: tuple[ZappiStatus]
