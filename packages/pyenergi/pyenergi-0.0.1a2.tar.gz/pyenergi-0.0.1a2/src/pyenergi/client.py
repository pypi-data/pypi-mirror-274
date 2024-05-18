import enum
import logging
import os
from abc import ABC
from dataclasses import dataclass
from datetime import datetime, time
from enum import Enum, IntEnum, StrEnum
from functools import cached_property
from typing import Literal, overload

import httpx
from pydantic import BaseModel

from . import exceptions, schemas
from .schemas import (
    ChargeMode,
    CTType,
)

logger = logging.getLogger(__name__)


class Hub:
    """
    A myenergi Hub.

    :param serial_number: A myenergi Hub serial number.
    :param api_key: The API key for the myenergi Hub.
    """

    _DIRECTOR_URL = "https://director.myenergi.net/"
    """myenergi API director URL.

    The director is queried for the Hub's ASN, which is used as the base URL for further
    API requests.
    """

    serial_number: str
    api_key: str

    def __init__(self, serial_number: str | None = None, api_key: str | None = None):
        """Initialise a myenergi Hub.

        Authentication credentials (hub serial number and API key) must either be
        provided as arguments to the constructor, or as environment variables
        (``PYENERGI_HUB_SERIAL_NUMBER`` and ``PYENERGI_API_KEY`` respectively).

        :param serial_number: A myenergi Hub serial number. All API operations
            will pertain to devices related to this Hub.

        :param api_key: The API key for the myenergi Hub.
        """
        # We authenticate with the myenergi API using a hub serial number and associated
        # API key. These are accepted either via the constructor, or via environment
        # variables.

        # Ensure that, if either credential is provided, both are provided.
        if any([serial_number, api_key]) and not all([serial_number, api_key]):
            raise ValueError("Both hub serial number and API key must be provided.")

        # If neither credential is provided, attempt to load them from the environment.
        if not any([serial_number, api_key]):
            serial_number = os.getenv("PYENERGI_HUB_SERIAL_NUMBER")
            api_key = os.getenv("PYENERGI_API_KEY")

        # If either credential is still not provided, raise an error.
        if not (serial_number and api_key):
            raise exceptions.MissingCredentialsError
        else:
            self.serial_number = serial_number
            self.api_key = api_key

    async def test(self) -> bool:
        """Attempt to connect to the myenergi API.

        Use this to test myenergi API connectivity, including the validity of the
        configured authorisation credentials.

        :returns: ``True`` if the connection was successful, ``False`` otherwise.

        :raises:
            :py:class:`AuthenticationError`: If the provided authentication credentials
            are invalid.

            :py:class:`PyenergiError`: If the connection was unsuccessful.
        """
        await self._get("/cgi-jstatus-E", raise_for_status=True)
        return True

    async def get_zappis(self) -> list["Zappi"]:
        """Get all Zappis associated with this myenergi Hub."""
        response = await self._get("/cgi-jstatus-Z")
        response_zappis = schemas.AllZappisStatusResponse.parse_raw(response.content)
        return [
            Zappi.from_api_object(client=self, response=zappi)
            for zappi in response_zappis.zappi
        ]

    async def _set_base_url_if_not_set(self):
        if str(self._httpx.base_url) == "":
            logger.debug("Setting base URL for the first time.")
            self._httpx.base_url = await self._get_asn_url()
        else:
            logger.debug("Base URL already set.")

    # ASN lookup

    async def _get_asn_url(self):
        """Get the myenergi API 'ASN' URL for the configured myenergi Hub.

        This is used as the base URL for all API requests related to the Hub.

        :returns: The API base URL.
        """
        response = await self._httpx.get(self._DIRECTOR_URL)
        try:
            asn = response.headers["x_myenergi-asn"]
        except KeyError as e:
            raise exceptions.DirectorError("No ASN header present.") from e
        else:
            return f"https://{asn}"

    async def _set_asn_url(self):
        self._httpx.base_url = await self._get_asn_url()

    # HTTP client internals

    @cached_property
    def _httpx(self):
        return httpx.AsyncClient(
            auth=httpx.DigestAuth(username=self.serial_number, password=self.api_key),
        )

    async def _get(self, *args, raise_for_status=True, **kwargs):
        await self._set_base_url_if_not_set()
        response = await self._httpx.get(*args, **kwargs)
        if response.status_code == httpx.codes.UNAUTHORIZED:
            raise exceptions.AuthenticationError
        if raise_for_status:
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise exceptions.PyenergiError from e
        return response


class ChargeStatus(Enum):
    NOT_CONNECTED = enum.auto()
    """No EV is connected."""

    WAITING_FOR_EV = enum.auto()
    """The Zappi is waiting for the connected EV to allow charging to begin."""

    CHARGING = enum.auto()
    """Charging is underway."""

    FAULT = enum.auto()
    """An EV is connected, but the connection has faulted."""

    PAUSED = enum.auto()
    """An EV is connected, and charging is paused."""

    COMPLETE = enum.auto()
    """An EV is connected, and charging is complete."""


class LastCommandStatus(StrEnum):
    """The status of the last command sent to a Zappi."""

    PROCESSING = "Processing"
    """The Zappi is currently processing the command."""

    SUCCESS = "Success"
    """The command was successfully executed by the Zappi."""

    FAILED = "Failed"
    """The command failed to be executed by the Zappi."""

    NOT_SENT = "Not sent"
    """No command has been sent to the Zappi."""


class CT(BaseModel):
    """Information pertaining to a particular CT (current transformer)."""

    type: CTType
    """The type that has been assigned to the CT."""

    power: int | None
    """The power, in watts, that the CT has most recently measured."""


@dataclass(kw_only=True)
class Entity(ABC):
    _client: Hub


class BoostMode(IntEnum):
    """Zappi Boost modes."""

    STOP = 2
    MANUAL = 3
    SMART = 4


type EnergyToAddAmount = Literal[5, 10, 20, 40, 60, 80, 100]


@dataclass(kw_only=True)
class Zappi(Entity):
    """A myenergi Zappi device."""

    serial_number: int
    """Hardware serial number."""

    firmware_version: str
    """Firmware version."""

    is_new_bootloader_available: bool
    """Is a new bootloader version available?"""

    system_datetime: datetime
    """The Zappi's system date / time."""

    is_daylight_savings: bool
    """Whether or not daylight savings is turned on."""

    last_command_status: LastCommandStatus
    """The status of the last command sent to the Zappi."""

    last_command_waiting_seconds: int
    """How long, in seconds, it has been since the last command was sent.

    This value is as it is returned by the myenergi API. It does not autmoatically
    increment as time passes, unless you re-query the API.
    """

    charge_status: ChargeStatus
    """The Zappi's current charge status."""

    @property
    def ev_connected(self):
        return self.charge_status != ChargeStatus.NOT_CONNECTED

    charge_mode: ChargeMode
    """The Zappi's current charging mode."""

    is_boosting: bool
    """Is the Zappi currently charging due to a Boost?"""

    minimum_green_level: int
    """The minimum green energy level (for Eco and Eco+ modes)."""

    smart_boost_end_time: time | None
    """The time at which the Smart Boost will end."""

    smart_boost_energy_to_add: int | None
    """The amount of energy (in kWh) to add during the Smart Boost."""

    scheduled_boost_start_time: time | None
    """The time at which the Scheduled Boost will start."""

    scheduled_boost_energy_to_add: int | None
    """The amount of energy (in kWh) to add during the Scheduled Boost."""

    priority: int
    """This Zappi's priority relative to other devices associated with this myenergy Hub."""

    grid_frequency: float
    """The grid's current frequency."""

    grid_voltage: float
    """The grid's current voltage."""

    phases: Literal[1, 3]
    """The number of electrical phases."""

    cts: dict[int, CT]
    """Information pertaining to each of the Zappi's current transformers."""

    diversion_amount: int
    """Power being diverted to the Zappi, in watts."""

    power_generation: int
    """The amount of power currently being generated, as measured by the Zappi."""

    power_grid: int
    """The amount of power currently being drawn from the grid, as measured by the Zappi.

    If this value is negative, power is currently being exported to the grid.
    """

    is_locked: bool
    """Is the Zappi currently locked?"""

    should_lock_when_plugged_in: bool
    """Should the Zappi lock when an EV is plugged in?"""

    should_lock_when_unplugged: bool
    """Should the Zappi lock when an EV is unplugged?"""

    should_charge_when_locked: bool
    """Should the Zappi charge a connected EV when locked?"""

    should_charge: bool
    """Is the Zappi allowed to charge an EV?"""

    is_being_tampered_with: bool
    """Is the Zappi currently being tampered with?"""

    @classmethod
    def from_api_object(cls, client: Hub, response: schemas.ZappiStatus) -> "Zappi":
        system_datetime = datetime.combine(
            date=response.current_date, time=response.current_time
        )

        smart_boost_end_time = time(
            hour=response.smart_boost_end_time_hour or 0,
            minute=response.smart_boost_end_time_minute or 0,
        )

        scheduled_boost_start_time = time(
            hour=response.scheduled_boost_hour or 0,
            minute=response.scheduled_boost_minute or 0,
        )

        is_locked = bool(response.lock_status & 1)
        lock_when_plugged_in = bool(response.lock_status & 2)
        lock_when_unplugged = bool(response.lock_status & 4)
        charge_when_locked = bool(response.lock_status & 8)
        charge_session_allowed = bool(response.lock_status & 16)

        zappi = cls(
            _client=client,
            serial_number=response.serial_number,
            firmware_version=response.firmware_version,
            charge_status=cls._get_charge_status(
                charge_status=response.charge_status,
                plug_status=response.plug_status,
            ),
            charge_mode=response.charge_mode,
            last_command_status=cls._get_command_status(response.command_timer),
            last_command_waiting_seconds=response.command_timer,
            system_datetime=system_datetime,
            is_daylight_savings=response.is_daylight_savings,
            cts=cls._get_cts(response),
            diversion_amount=response.diversion_amount,
            priority=response.priority,
            minimum_green_level=response.minimum_green_level,
            smart_boost_end_time=smart_boost_end_time,
            smart_boost_energy_to_add=response.smart_boost_energy_to_add,
            scheduled_boost_start_time=scheduled_boost_start_time,
            scheduled_boost_energy_to_add=response.scheduled_boost_energy_to_add,
            grid_frequency=response.grid_frequency,
            grid_voltage=response.grid_voltage,
            phases=response.phases,
            power_grid=response.grid_power,
            power_generation=response.generating_power,
            is_new_bootloader_available=response.new_bootloader_available,
            is_boosting=response.is_boosting,
            is_being_tampered_with=response.being_tampered_with,
            is_locked=is_locked,
            should_lock_when_plugged_in=lock_when_plugged_in,
            should_lock_when_unplugged=lock_when_unplugged,
            should_charge_when_locked=charge_when_locked,
            should_charge=charge_session_allowed,
        )

        return zappi

    @staticmethod
    def _get_cts(response: schemas.ZappiStatus) -> dict[int, CT]:
        cts = {}
        for i in range(1, 7):
            ct_type = getattr(response, f"ct_{i}_type", None)
            ct_power = getattr(response, f"ct_{i}_power", None)
            if not (ct_type is None or ct_power is None):
                cts[i] = CT(type=ct_type, power=ct_power)
        return cts

    @staticmethod
    def _get_command_status(command_timer: int) -> LastCommandStatus:
        match command_timer:
            case 254:
                return LastCommandStatus.SUCCESS
            case 253:
                return LastCommandStatus.FAILED
            case 255:
                return LastCommandStatus.NOT_SENT
            # Values 1-10 indicate that the command is still processing.
            case value if 10 <= value <= 1:
                return LastCommandStatus.PROCESSING
            case value:
                raise ValueError(f"Invalid command timer value: {value}")

    @staticmethod
    def _get_charge_status(
        charge_status: schemas.ChargeStatus, plug_status: schemas.PlugStatus
    ) -> ChargeStatus:
        match plug_status, charge_status:
            case schemas.PlugStatus.EV_DISCONNECTED, _:
                return ChargeStatus.NOT_CONNECTED
            case schemas.PlugStatus.WAITING_FOR_EV, _:
                return ChargeStatus.WAITING_FOR_EV
            case schemas.PlugStatus.CHARGING, _:
                return ChargeStatus.CHARGING
            case schemas.PlugStatus.FAULT, _:
                return ChargeStatus.FAULT
            case schemas.ChargeStatus.PAUSED, schemas.PlugStatus.EV_CONNECTED:
                return ChargeStatus.PAUSED
            case schemas.ChargeStatus.COMPLETE, schemas.PlugStatus.EV_CONNECTED:
                return ChargeStatus.COMPLETE
            case _:
                raise ValueError(
                    f"Invalid charge / plug status: {charge_status}, {plug_status}"
                )

    # Change charge mode / boost mode.

    async def set_charge_mode(self, mode: ChargeMode):
        """Set the Zappi's charge mode.

        :param mode: The charge mode to set.

        :returns: ``True`` if the charge mode was successfully set.

        :raises:
            :py:class:`ValueError`: If the charge mode is invalid.

            :py:class:`PyenergiError`: If another API-related error occurs.
        """
        response = await self._set_charge_boost_mode(charge_mode=mode)
        return True

    @overload
    async def set_boost_mode(
        self,
        *,
        mode: Literal[BoostMode.SMART],
        energy_to_add: EnergyToAddAmount,
        finish_by: time,
    ): ...

    @overload
    async def set_boost_mode(
        self,
        *,
        mode: Literal[BoostMode.MANUAL],
        energy_to_add: EnergyToAddAmount,
    ): ...

    @overload
    async def set_boost_mode(
        self,
        *,
        mode: Literal[BoostMode.STOP],
    ): ...

    async def set_boost_mode(
        self,
        *,
        mode: BoostMode,
        energy_to_add: EnergyToAddAmount | None = None,
        finish_by: time | None = None,
    ):
        """Set the Zappi's Boost mode.

        :param mode: The Boost mode to set.

        :param energy_to_add: The amount of energy to add during the Boost.

        :param finish_by: The time at which the Boost should finish.

        The ``finish_by`` and ``energy_to_add`` parameters are sometimes required, and
        sometimes not allowed at all, depending on the `mode` parameter. See the
        override signatures for more information.

        :returns: ``True`` if the Boost mode was successfully changed.

        :raises:
            :py:class:`ValueError`: If the charge mode is invalid.

            :py:class:`PyenergiError`: If another API-related error occurs.
        """

        return await self._set_charge_boost_mode(
            boost_mode=mode,
            energy_to_add=energy_to_add,
            charge_mode=None,
            finish_by=finish_by,
        )

    async def stop_boosting(self):
        return await self._set_charge_boost_mode(boost_mode=BoostMode.STOP)

    async def _set_charge_boost_mode(
        self,
        *,
        charge_mode: ChargeMode | None = None,
        boost_mode: BoostMode | None = None,
        energy_to_add: EnergyToAddAmount | None = None,
        finish_by: time | None = None,
    ):
        """Set the charge or Boost mode.

        Changing these two configuration options is handled by this one underlying
        method to reflect the structure of the myenergi API. A more sane interface
        is provided by the client's public interface.
        """
        # Validate the input.
        #
        # Either change charge or boost mode, not both.
        if charge_mode is not None and boost_mode is not None:
            raise ValueError("Cannot change charge and Boost mode simultaneously.")
        if charge_mode is None and boost_mode is None:
            raise ValueError("Must change either charge or Boost mode.")

        # When changing charge mode, do not define finish by or energy to add.
        if charge_mode is not None and (
            finish_by is not None or energy_to_add is not None
        ):
            raise ValueError(
                "Cannot set finish by or energy to add when changing charge mode."
            )

        # When changing boost mode, define energy to add.
        if boost_mode is not None and energy_to_add is None:
            raise ValueError("Must define energy to add when changing Boost mode.")

        # When using smart boost, define finish by.
        if boost_mode == BoostMode.SMART and finish_by is None:
            raise ValueError("Must define finish by when using Smart Boost.")

        # Finish by minute is one of available choices.
        if finish_by is not None and finish_by.minute not in [0, 15, 30, 45]:
            raise ValueError("Finish by minute must be one of 0, 15, 30, or 45.")

        charge_mode_number = charge_mode.value if charge_mode is not None else 0
        boost_mode_number = boost_mode.value if boost_mode is not None else 0
        energy_to_add_number = energy_to_add or 0
        finish_by_hour = finish_by.hour if finish_by is not None else 0
        finish_by_minute = finish_by.minute if finish_by is not None else 0

        url = (
            f"/cgi-zappi-mode-Z{self.serial_number}-{charge_mode_number}-"
            f"{boost_mode_number}-{energy_to_add_number}-"
            f"{finish_by_hour:2.0}{finish_by_minute:2.0}"
        )

        response = await self._client._get(url)
        response.raise_for_status()
        return True
