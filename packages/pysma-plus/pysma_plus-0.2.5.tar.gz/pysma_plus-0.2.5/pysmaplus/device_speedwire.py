"""
Implementation for SMA Speedwire

Originally based on https://github.com/Wired-Square/sma-query/blob/main/src/sma_query_sw/commands.py
Improved with Information from https://github.com/mhop/fhem-mirror/blob/master/fhem/FHEM/76_SMAInverter.pm
Receiver classes completely reimplemented by little.yoda

"""
import logging
import time
import ctypes
import binascii
import copy
import collections
import struct
import asyncio
from typing import Any, Dict, Optional, List, Annotated
from ctypes import LittleEndianStructure
from asyncio import DatagramProtocol, Future

from .helpers import version_int_to_string
from .definitions_speedwire import commands, responseDef, speedwireHeader, speedwireHeader6065

from .sensor import Sensors, Sensor
from .device import Device
from .const import SMATagList

from .exceptions import (
    SmaConnectionException,
    SmaReadException,
    SmaAuthenticationException,
)


_LOGGER = logging.getLogger(__name__)

APP_ID = 125
ANY_SERIAL = 0xFFFFFFFF
ANY_SUSYID = 0xFFFF

# Login Timeout in seconds
LOGIN_TIMEOUT = 900


def get_encoded_pw(password, installer=False):
    """Encodes the password"""
    byte_password = bytearray(password.encode("ascii"))

    if installer:
        login_code = 0xBB
    else:
        login_code = 0x88

    encodedpw = bytearray(12)

    for index in range(0, 12):
        if index < len(byte_password):
            encodedpw[index] = (login_code + byte_password[index]) % 256
        else:
            encodedpw[index] = login_code

    return encodedpw


class SpeedwireFrame:
    """Class for the send speedwire messages"""

    _frame_sequence = 1
    _id = (ctypes.c_ubyte * 4).from_buffer(bytearray(b"SMA\x00"))
    _tag0 = (ctypes.c_ubyte * 4).from_buffer(bytearray(b"\x00\x04\x02\xA0"))
    _group1 = (ctypes.c_ubyte * 4).from_buffer(bytearray(b"\x00\x00\x00\x01"))
    _eth_sig = (ctypes.c_ubyte * 4).from_buffer(bytearray(b"\x00\x10\x60\x65"))
    _ctrl2_1 = (ctypes.c_ubyte * 2).from_buffer(bytearray(b"\x00\x01"))
    _ctrl2_2 = (ctypes.c_ubyte * 2).from_buffer(bytearray(b"\x00\x01"))

    _data_length = 0  # Placeholder value
    _longwords = 0  # Placeholder value
    _ctrl = 0  # Placeholder value

    class FrameHeader(LittleEndianStructure):
        """Frame Header"""

        _pack_ = 1
        _fields_ = [
            ("id", ctypes.c_ubyte * 4),
            ("tag0", ctypes.c_ubyte * 4),
            ("group1", ctypes.c_ubyte * 4),
            ("data_length", ctypes.c_uint16),
            ("eth_sig", ctypes.c_ubyte * 4),
            ("longwords", ctypes.c_ubyte),
            ("ctrl", ctypes.c_ubyte),
        ]

    class DataHeader(LittleEndianStructure):
        # pylint: disable=too-few-public-methods
        """Data header"""
        _pack_ = 1
        _fields_ = [
            ("dst_sysyid", ctypes.c_uint16),
            ("dst_serial", ctypes.c_uint32),
            ("ctrl2_1", ctypes.c_ubyte * 2),
            ("app_id", ctypes.c_uint16),
            ("app_serial", ctypes.c_uint32),
            ("ctrl2_2", ctypes.c_ubyte * 2),
            ("preamble", ctypes.c_uint32),
            ("sequence", ctypes.c_uint16),
        ]

    class LogoutFrame(LittleEndianStructure):
        # pylint: disable=too-few-public-methods
        """Logout"""
        _pack_ = 1
        _fields_ = [
            ("command", ctypes.c_uint32),
            ("data_start", ctypes.c_uint32),
            ("data_end", ctypes.c_uint32),
        ]

    class LoginFrame(LittleEndianStructure):
        # pylint: disable=too-few-public-methods
        """Login"""
        _pack_ = 1
        _fields_ = [
            ("command", ctypes.c_uint32),
            ("login_type", ctypes.c_uint32),
            ("timeout", ctypes.c_uint32),
            ("time", ctypes.c_uint32),
            ("data_start", ctypes.c_uint32),
            ("user_password", ctypes.c_ubyte * 12),
            ("data_end", ctypes.c_uint32),
        ]

    class QueryFrame(LittleEndianStructure):
        # pylint: disable=too-few-public-methods
        """Query Frame"""

        _pack_ = 1
        _fields_ = [
            ("command", ctypes.c_uint32),
            ("first", ctypes.c_uint32),
            ("last", ctypes.c_uint32),
            ("data_end", ctypes.c_uint32),
        ]

    # def getLogoutFrame(self, inverter):
    #     frame_header = self.getFrameHeader()
    #     frame_data_header = self.getDataHeader(inverter)
    #     frame_data = self.LogoutFrame()

    #     frame_header.ctrl = 0xA0
    #     frame_data_header.dst_sysyid = 0xFFFF
    #     frame_data_header.ctrl2_1 = (ctypes.c_ubyte * 2).from_buffer(bytearray(b"\x00\x03"))
    #     frame_data_header.ctrl2_2 = (ctypes.c_ubyte * 2).from_buffer(bytearray(b"\x00\x03"))

    #     frame_data.command = commands["logoff"]["command"]
    #     frame_data.data_start = 0xFFFFFFFF
    #     frame_data.data_end = 0x00000000

    #     data_length = ctypes.sizeof(frame_data_header) + ctypes.sizeof(frame_data)

    #     frame_header.data_length = int.from_bytes(data_length.to_bytes(2, "big"), "little")

    #     frame_header.longwords = (data_length // 4)

    #     return bytes(frame_header) + bytes(frame_data_header) + bytes(frame_data)

    def getLoginFrame(self, password, serial: int, installer: bool):
        # pylint: disable=too-few-public-methods
        """Returns a Login Frame"""
        frame_header = self.getFrameHeader()
        frame_data_header = self.getDataHeader(password, serial)
        frame_data = self.LoginFrame()

        frame_header.ctrl = 0xA0
        frame_data_header.dst_sysyid = 0xFFFF
        frame_data_header.ctrl2_1 = (ctypes.c_ubyte * 2).from_buffer(
            bytearray(b"\x00\x01")
        )
        frame_data_header.ctrl2_2 = (ctypes.c_ubyte * 2).from_buffer(
            bytearray(b"\x00\x01")
        )

        frame_data.command = commands["login"]["command"]
        frame_data.login_type = (0x07, 0x0A)[installer]
        frame_data.timeout = LOGIN_TIMEOUT
        frame_data.time = int(time.time())
        frame_data.data_start = 0x00000000  # Data Start
        frame_data.user_password = (ctypes.c_ubyte * 12).from_buffer(
            get_encoded_pw(password, installer)
        )
        frame_data.date_end = 0x00000000  # Packet End

        data_length = ctypes.sizeof(frame_data_header) + ctypes.sizeof(frame_data)

        frame_header.data_length = int.from_bytes(
            data_length.to_bytes(2, "big"), "little"
        )

        frame_header.longwords = data_length // 4

        return bytes(frame_header) + bytes(frame_data_header) + bytes(frame_data)

    def getQueryFrame(self, password, serial: int, command_name: str):
        """Return Query Frame"""
        frame_header = self.getFrameHeader()
        frame_data_header = self.getDataHeader(password, serial)
        frame_data = self.QueryFrame()

        command = commands[command_name]

        frame_header.ctrl = 0xA0
        frame_data_header.dst_sysyid = 0xFFFF
        frame_data_header.ctrl2_1 = (ctypes.c_ubyte * 2).from_buffer(
            bytearray(b"\x00\x00")
        )
        frame_data_header.ctrl2_2 = (ctypes.c_ubyte * 2).from_buffer(
            bytearray(b"\x00\x00")
        )

        frame_data.command = command["command"]
        frame_data.first = command["first"]
        frame_data.last = command["last"]
        frame_data.date_end = 0x00000000

        data_length = ctypes.sizeof(frame_data_header) + ctypes.sizeof(frame_data)

        frame_header.data_length = int.from_bytes(
            data_length.to_bytes(2, "big"), "little"
        )

        frame_header.longwords = data_length // 4

        return bytes(frame_header) + bytes(frame_data_header) + bytes(frame_data)

    def getFrameHeader(self):
        """Return Frame Header"""
        newFrameHeader = self.FrameHeader()
        newFrameHeader.id = self._id
        newFrameHeader.tag0 = self._tag0
        newFrameHeader.group1 = self._group1
        newFrameHeader.data_length = self._data_length
        newFrameHeader.eth_sig = self._eth_sig
        newFrameHeader.longwords = self._longwords
        newFrameHeader.ctrl = self._ctrl

        return newFrameHeader

    def getDataHeader(self, password, serial):
        """Return Data Header"""
        newDataHeader = self.DataHeader()

        newDataHeader.dst_susyid = ANY_SUSYID
        newDataHeader.dst_serial = ANY_SERIAL
        newDataHeader.ctrl2_1 = self._ctrl2_1
        newDataHeader.app_id = APP_ID
        newDataHeader.app_serial = serial
        newDataHeader.ctrl2_2 = self._ctrl2_2
        newDataHeader.preamble = 0
        newDataHeader.sequence = self._frame_sequence | 0x8000

        self._frame_sequence += 1

        return newDataHeader


class SMAClientProtocol(DatagramProtocol):
    """Basic Class for communication"""

    _commandFuture: Future[Any] = None

    debug: Dict[str, Any] = {
        "msg": collections.deque(maxlen=len(commands) * 10),
        "data": {},
        "unfinished": set(),
        "ids": set(),
        "sendcounter": 0,
        "resondcounter": 0,
        "failedCounter": 0
    }

    def __init__(self, password, on_connection_lost):
        self.speedwire = SpeedwireFrame()
        self.transport = None
        self.password = password
        self.on_connection_lost = on_connection_lost
        self.cmds = []
        self.cmdidx = 0
        self.future = None
        self.data_values = {}
        self.sensors = {}
        self._group = None
        self._resendcounter = 0
        self._failedCounter = 0
        self._sendCounter = 0

        self.allCmds = []
        self.allCmds.extend(commands.keys())
        self.allCmds.remove("login")
        self.allCmds.remove("logoff")

    def connection_made(self, transport):
        self.transport = transport

    async def controller(self):
        try:
            if self._resendcounter == 0:
                self.debug["sendcounter"] += 1
                self._sendCounter += 1

            await asyncio.wait_for(self._commandFuture, timeout=0.5)
            self.cmdidx += 1
            self._resendcounter = 0
        except asyncio.TimeoutError:
            _LOGGER.debug(f"Timeout in command. Resendcounter: {self._resendcounter}")
            self._resendcounter += 1
            self.debug["resendcounter"] += 1
            if (self._resendcounter > 2):
                # Giving up. Next Command
                _LOGGER.debug(f"Timeout in command")
                self.cmdidx += 1
                self._resendcounter = 0
                self._failedCounter += 1
                self.debug["failedcounter"] += 1

        await self._send_next_command()


    def _confirm_repsonse(self, code=-1):
        if self._commandFuture.done():
            _LOGGER.debug(f"unexpected message {code:08X}")
            return
        self._commandFuture.set_result(True)

    async def start_query(self, cmds: List, future, group: str):
        self.cmds = ["login"]
        self.cmds.extend(cmds)
        self.future = future
        self.cmdidx = 0
        self._failedCounter = 0
        self._sendCounter = 0
        self._group = group
        self.data_values = {}
        self.sensors = {}
        _LOGGER.debug("Sending login")
        self.debug["msg"].append(["SEND", "login"])
        await self._send_next_command()

    def connection_lost(self, exc):
        _LOGGER.debug(f"Connection lost: {exc}")
        self.on_connection_lost.set_result(True)

    def _send_command(self, cmd):
        """Send the Command"""
        _LOGGER.debug(
            f"Sending command [{len(cmd)}] -- {binascii.hexlify(cmd).upper()}"
        )
        self._commandFuture = asyncio.get_running_loop().create_future()
        asyncio.get_running_loop().create_task(self.controller())
        self.transport.sendto(cmd)

    async def _send_next_command(self):
        """Send the next command in the list"""
        if not self.future:
            return
        if self.cmdidx >= len(self.cmds):
            # All commands send. Clean up.
            f = self.future
            self.future = None
            await asyncio.sleep(0.1)  # Wait for delayed respones
            self.debug["data"] = self.data_values
            self.cmds = []
            self.cmdidx = 0
            f.set_result(True)
        else:
            # Send the next command
            self.debug["msg"].append(["SEND", self.cmds[self.cmdidx]])
            _LOGGER.debug("Sending " + self.cmds[self.cmdidx])
            if (self.cmds[self.cmdidx]) == "login":
                groupidx = ["user", "installer"].index(self._group)
                self._send_command(
                    self.speedwire.getLoginFrame(self.password, 0, groupidx)
                )
            else:
                self._send_command(
                    self.speedwire.getQueryFrame(
                        self.password, 0, self.cmds[self.cmdidx]
                    )
                )

    def _getFormat(self, handler):
        """Return the necessary information for extracting the information"""
        converter = None
        format = handler.get("format", "")
        if format == "int":
            format = "<l"
        elif format == "" or format == "uint":
            format = "<L"
        elif format == "version":
            format = "<L"
            converter = version_int_to_string
        else:
            raise ValueError(f"Unknown Format {format}")
        size = struct.calcsize(format)
        return (format, size, converter)

    def handle_login(self, msg):
        """Is called if a login repsonse is received"""
        _LOGGER.debug("Login repsonse received!")
        self.sensors = {}
        self.data_values = {"error": msg.error}
        if msg.error == 256:
            _LOGGER.error("Login failed!")
            self.future.set_exception(
                SmaAuthenticationException(
                    "Login failed! Credentials wrong (user/install or password)"
                )
            )

    def handle_newvalue(self, sensor: Sensor, value: Any):
        """Set the new value to the sensor"""
        if value is None:
            return
        sen = copy.copy(sensor)
        if sen.factor and sen.factor != 1:
            value /= sen.factor
        sen.value = value
        if sen.key in self.sensors:
            oldValue = self.sensors[sen.key].value
            if oldValue != value:
                _LOGGER.warning(
                    f"Overwriting sensors {sen.key} {sen.name} {oldValue} with new values {sen.value}"
                )
        self.sensors[sen.key] = sen
        self.data_values[sen.key] = value

    def extractvalues(self, handler: Dict, subdata):
        (formatdef, size, converter) = self._getFormat(handler)
        values = []
        for idx in range(8, len(subdata), size):
            v = struct.unpack(formatdef, subdata[idx : idx + size])[0]
            if v in [0xFFFFFFFF, 0x80000000, 0xFFFFFFEC]:
                v = None
            else:
                if converter:
                    v = converter(v)
                if "mask" in handler:
                    v = v & handler["mask"]
            values.append(v)
        return values

    def handle_register(self, subdata, register_idx: int):
        """Handle the payload with all the registers"""
        code = int.from_bytes(subdata[0:4], "little")
        # c = f"{(code & 0xFFFFFFFF):08X}"
        c = f"{code:08X}"
        msec = int.from_bytes(subdata[4:8], "little")  # noqa: F841

        # Fix for strange response codes
        self.debug["ids"].add(c[6:])
        if c.endswith("07"):
            c = c[:7] + "1"

        # Handle unknown Responses
        if c not in responseDef:
            values = []
            valuesPos = []
            for idx in range(8, len(subdata), 4):
                v = struct.unpack("<l", subdata[idx : idx + 4])[0]
                values.append(v)
                valuesPos.append(f"{idx + 54}")
            _LOGGER.warning(f"No Handler for {c}: {values} @ {valuesPos}")
            self.debug["unfinished"].add(f"{c}")
            return

        # Handle known repsones
        for handler in responseDef[c]:
            values = self.extractvalues(handler, subdata)
            if "sensor" not in handler:
                continue
            v = values[handler["idx"]]

            sensor = handler["sensor"]

            # Special handling for a response that returns two values under the same code
            if isinstance(sensor, List):
                if register_idx >= len(sensor):
                    _LOGGER.warning(
                        f"No Handler for {c} at register idx {register_idx}: {values}"
                    )
                    continue
                _LOGGER.debug(
                    f"Special Handler for {c} at register idx {register_idx}: {values}"
                )
                sensor = sensor[register_idx]
            self.handle_newvalue(sensor, v)

    # Unfortunately, there is no known method of determining the size of the registers
    # from the message. Therefore, the register size is determined from the number of
    # registers and the size of the payload.
    def calc_register(self, data, msg: speedwireHeader6065):
        cnt_registers = msg.lastRegister - msg.firstRegister + 1
        size_datapayload = len(data) - 54 - 4
        size_registers = (
            size_datapayload // cnt_registers
            if size_datapayload % cnt_registers == 0
            else -1
        )
        return (cnt_registers, size_registers)

    # Main routine for processing received messages.
    def datagram_received(self, data, addr):
        _LOGGER.debug(f"RECV: {addr} Len:{len(data)} {binascii.hexlify(data).upper()}")
        self.debug["msg"].append(
            ["RECV", len(data), binascii.hexlify(data).upper().decode("utf-8")]
        )

        # Check if message is a 6065 protocol
        msg = speedwireHeader.from_packed(data[0:18])
        if not msg.check6065():
            _LOGGER.debug("Ignoring non 6065 Response. %d", msg.protokoll)
            return

        # If the requested information is not available, send the next command,
        if len(data) < 58:
            _LOGGER.debug(f"NACK [{len(data)}] -- {data}")
            self._confirm_repsonse()
            return

        # Handle Login Responses
        msg6065 = speedwireHeader6065.from_packed(data[18 : 18 + 36])
        if msg6065.isLoginResponse():
            self.handle_login(msg6065)
            self._confirm_repsonse()
            return


        # Filter out non matching responses
        (cnt_registers, size_registers) = self.calc_register(data, msg6065)
        code = int.from_bytes(data[54:58], "little")
        codem = code & 0x00FFFF00
        if len(data) == 58 and codem == 0:
            _LOGGER.debug(f"NACK [{len(data)}] -- {data}")
            self._confirm_repsonse()
            return
        if size_registers <= 0 or size_registers not in [16, 28, 40]:
            _LOGGER.warning(
                f"Skipping message. --- Len {data} Ril {codem} {cnt_registers} x {size_registers} bytes"
            )
            self._confirm_repsonse(code)
            return

        # Extract the values for each register
        for idx in range(0, cnt_registers):
            start = idx * size_registers + 54
            self.handle_register(data[start : start + size_registers], idx)

        self._confirm_repsonse(code)


class SMAspeedwireINV(Device):
    """Adapter between Device-Class and SMAClientProtocol"""

    _transport = None
    _protocol = None
    _deviceinfo: Dict[str, Any] = {}
    _debug: Dict[str, Any] = {
        "overalltimeout": 0
    }

    def __init__(self, host: str, group: str, password: Optional[str]):
        self._host = host
        self._group = group
        self._password = password
        if group not in ["user", "installer"]:
            raise KeyError(f"Invalid user type: {group} (user or installer)")

        self.check()

    def check(self) -> None:
        keysname = {}
        sensorname = {}
        for responses in responseDef.values():
            for response in responses:
                if "sensor" not in response or not isinstance(
                    response["sensor"], Sensor
                ):
                    continue
                sensor = response["sensor"]
                if sensor.key in keysname:
                    print("Doppelter SensorKey " + sensor.key)
                    raise RuntimeError("Doppelter SensorKey " + sensor.key)
                keysname[sensor.key] = 1
                if sensor.name in sensorname:
                    print("Doppelter SensorName " + sensor.name)
                    raise RuntimeError("Doppelter Sensorname " + sensor.name)
                sensorname[sensor.name] = 1

        keysname = {}
        sensorname = {}
        for x in commands.items():
            if "registers" not in x[1]:
                continue
            for r in x[1]["registers"]:
                if "name" in r:
                    name = r["name"]
                    if name in keysname:
                        print("Doppelter Keyname " + name)
                        raise RuntimeError("Doppelter Keyname " + name)
                    keysname[name] = 1
                if "sensor" in r:
                    sensor = r["sensor"]
                    if isinstance(sensor, Sensor) and sensor.key in sensorname:
                        print("Doppelter Sensorname " + sensor.key)
                        raise RuntimeError("Doppelter Sensorname " + sensor.key)
                    sensorname[name] = 1

    async def new_session(self) -> bool:
        loop = asyncio.get_running_loop()
        on_connection_lost = loop.create_future()

        self._transport, self._protocol = await loop.create_datagram_endpoint(
            lambda: SMAClientProtocol(self._password, on_connection_lost),
            remote_addr=(self._host, 9522),
        )
        # Test with device_info if the ip and user/pwd are correct
        await self.device_info()
        if (self._protocol._failedCounter >= self._protocol._sendCounter):
            raise SmaConnectionException("No connection to device: %s:9522",self._host)

    async def device_info(self) -> dict:
        fut = asyncio.get_running_loop().create_future()
        await self._protocol.start_query(["TypeLabel", "Firmware"], fut, self._group)
        try:
            await asyncio.wait_for(fut, timeout=5)
        except TimeoutError:
            self._debug["overalltimeout"] += 1
            _LOGGER.warning("Timeout in device_info")
            if (
                "error" in self._protocol.data_values
                and self._protocol.data_values["error"] == 0
            ):
                raise SmaReadException(
                    "Reply for request not received"
                )  # Recheck Logic
            raise SmaConnectionException("No connection to device")
        data = self._protocol.data_values

        invcnr = data.get("inverter_class", 0)
        invc = SMATagList.get(invcnr, "Unknown device")

        invtnr = data.get("inverter_type", 0)
        invt = SMATagList.get(invtnr, "Unknown type")
        self._deviceinfo = {
            "serial": data.get("serial", ""),
            "name": str(invt) + " (" + str(invtnr) + ")",
            "type": str(invc) + " (" + str(invcnr) + ")",
            "manufacturer": "SMA",
            "sw_version": data.get("Firmware", ""),
        }
        return self._deviceinfo

    async def get_sensors(self) -> Sensors:
        fut = asyncio.get_running_loop().create_future()
        c = self._protocol.allCmds
        device_sensors = Sensors()
        try:
            await self._protocol.start_query(c, fut, self._group)
            await asyncio.wait_for(fut, timeout=5)
            for s in self._protocol.sensors.values():
                device_sensors.add(s)
        except asyncio.TimeoutError as e:
            self._debug["overalltimeout"] += 1
            raise e
        return device_sensors


    async def read(self, sensors: Sensors) -> bool:
        fut = asyncio.get_running_loop().create_future()
        c = self._protocol.allCmds
        await self._protocol.start_query(c, fut, self._group)
        try:
            await asyncio.wait_for(fut, timeout=5)
            self._update_sensors(sensors, self._protocol.sensors)
            return True
        except asyncio.TimeoutError as e:
            self._debug["overalltimeout"] += 1
            raise e

    def _update_sensors(self, sensors, sensorReadings):
        """Update a sensor with the sensor reading"""
        _LOGGER.debug("Received %d sensor readings", len(sensorReadings))
        for sen in sensors:
            if sen.enabled and sen.key in sensorReadings:
                value = sensorReadings[sen.key].value
                if sen.mapper:
                    sen.mapped_value = sen.mapper.get(value, str(value))
                sen.value = value

    async def close_session(self) -> None:
        self._transport.close()

    async def get_debug(self) -> Dict:
        ret = self._protocol.debug.copy()
        ret["unfinished"] = list(ret["unfinished"])
        ret["msg"] = list(ret["msg"])
        ret["ids"] = list(ret["ids"])
        ret["device_info"] = self._deviceinfo
        ret["overalltimeout"] = self._debug["overalltimeout"]
        return ret

    # wait for a response or a timeout
    async def detect(self, ip) -> bool:
        ret = await super().detect(ip)
        try:
            ret[0]["testedEndpoints"] = str(ip) + ":9522"
            await self.new_session()
            fut = asyncio.get_running_loop().create_future()
            await self._protocol.start_query(["TypeLabel"], fut, self._group)
            try:
                await asyncio.wait_for(fut, timeout=5)
            except TimeoutError:
                _LOGGER.warning("Timeout in detect")
            if (
                "error" in self._protocol.data_values
                and self._protocol.dataValuess["error"] == 0
            ):
                raise SmaReadException(
                    "Reply for request not received"
                )  ## TODO recheck logic
            raise SmaConnectionException("No connection to device")
        except SmaAuthenticationException as e:
            ret[0]["status"] = "maybe"
            ret[0]["exception"] = e
            ret[0]["remark"] = "only unencrypted Speedwire is supported"
        except Exception as e:
            ret[0]["status"] = "failed"
            ret[0]["exception"] = e
        return ret
