import logging
from iot_protocols.devices.interfaces import ThreePhasesEnergyMeter
from iot_protocols.devices.models import DeviceHardware, DeviceProfile
from iot_protocols.protocols.modbus import requests, ModbusClient


class SocomecLoad(ThreePhasesEnergyMeter):

    # DEFAULT ENCODINGS
    MAX_U32 = 4294967295
    MAX_S32 = 2147483647
    SOCOMEC_LOAD_ADDRESS_OFFSET = 2048
    SOCOMEC_LOAD_1_MODBUS_MAPPING = {
        "Ap": {
            "address": 19841,
            "count": 2,
            "unit": "kWh",
            "encoding": "uint32"
        },
        "Am": {
            "address": 19844,
            "count": 2,
            "unit": "kWh",
            "encoding": "uint32"
        },
        "L1.U": {
            "address": 18444,
            "count": 2,
            "unit": "V",
            "ratio": 0.01,
            "encoding": "uint32"
        },
        "L2.U": {
            "address": 18446,
            "count": 2,
            "unit": "V",
            "ratio": 0.01,
            "encoding": "uint32"
        },
        "L3.U": {
            "address": 18448,
            "count": 2,
            "unit": "V",
            "ratio": 0.01,
            "encoding": "uint32"
        },
        "L1.I": {
            "address": 18458,
            "count": 2,
            "unit": "mA",
            "encoding": "uint32"
        },
        "L2.I": {
            "address": 18460,
            "count": 2,
            "unit": "mA",
            "encoding": "uint32"
        },
        "L3.I": {
            "address": 18462,
            "count": 2,
            "unit": "mA",
            "encoding": "uint32"
        },
        "I": {
            "address": 18464,
            "count": 2,
            "unit": "mA",
            "encoding": "uint32"
        },
        "F": {
            "address": 18442,
            "count": 2,
            "unit": "mHz",
            "encoding": "uint32"
        },
        "P": {
            "address": 18476,
            "count": 2,
            "unit": "W",
            "encoding": "int32"
        },
        "Q": {
            "address": 18478,
            "count": 2,
            "unit": "VA",
            "encoding": "int32"
        }
    }

    def __init__(self, load_id: int, modbus_id: int, client: ModbusClient) -> None:
        self._load_id = load_id
        self._modbus_id = modbus_id
        self._client = client

    @property
    def id(self) -> int:
        return self._load_id

    def read_energy(self, **kwargs) -> None:
        result = {}
        with self._client as client:
            for name, request in SocomecLoad.SOCOMEC_LOAD_1_MODBUS_MAPPING.items():
                try:
                    value = client.request(
                        requests.ReadHoldingRegister(
                            address=request["address"] + (self.id-1)*SocomecLoad.SOCOMEC_LOAD_ADDRESS_OFFSET, # Each load as an address offset of + 2048
                            unit=self._modbus_id,
                            count=request["count"],
                            encoding=request['encoding']
                        )
                    )
                    if value >= SocomecLoad.MAX_S32:
                        pass

                    else:
                        if "ratio" in request:
                            value = round(value*request['ratio'], 2)
                    
                        result[name] = dict(name=name, value=value, unit=request["unit"])
                        self[name] = result[name]

                except Exception as err:
                    logging.warning(f"Cannot read {name} from modbus : {err}")
        return result


class SocomecMeter:

    def __init__(self, modbus_id: int, port: str, baudrate: int=38400, parity: str="N", bytesize: int=8, stopbits: int=1, timeout: int=5, **kwargs):
        self._client = ModbusClient.with_serial_client(
            port=port,
            method="rtu",
            baudrate=baudrate,
            parity=parity,
            bytesize=bytesize,
            stopbits=stopbits,
            timeout=timeout
        )
        self._modbus_id = modbus_id
        self._model = None
        self.loads = {}

    def __str__(self) -> str:
        return f"SocomecMeter(Modbus RTU | Load : {self._modbus_id}"
        
    def __getitem__(self, key: str) -> SocomecLoad:
        return self.loads.get(key, None)
    
    def __setitem__(self, key: str, value: SocomecLoad) -> None:
        if not isinstance(value, SocomecLoad):
            raise ValueError(f"Invalid Value, must be a Socomec Load, got : {type(value)}")
        
        self.loads[key] = value

    @property
    def Load_1(self) -> SocomecLoad:
        return self["Load_1"]
    
    @property
    def Load_2(self) -> SocomecLoad:
        return self["Load_2"]
    
    @property
    def Load_3(self) -> SocomecLoad:
        return self["Load_3"]
    
    @property
    def Load_4(self) -> SocomecLoad:
        return self["Load_4"]
    
    @property
    def Load_5(self) -> SocomecLoad:
        return self["Load_5"]
    
    @property
    def Load_6(self) -> SocomecLoad:
        return self["Load_6"]
    
    @property
    def hardware(self) -> DeviceHardware:
        return DeviceHardware(
             serialNumber=self._serial_number,
             model=self._model
        )
    
    def connect(self) -> str:
        self._serial_number = self.get_net_ID()
        self._id = f"SOCO_{self._serial_number}"
        self._hardware = DeviceHardware(
            self._serial_number,
            self._model
        )
        self._is_connected = True

    def get_net_ID(self) -> str:
        with self._client as client:
            NET_ID_1 = client.request(
                requests.ReadHoldingRegister(
                    address=50067,
                    count=1,
                    unit=self._modbus_id,
                    encoding="uint16"
                )
            )
            NET_ID_2 = client.request(
                requests.ReadHoldingRegister(
                    address=50068,
                    count=1,
                    unit=self._modbus_id,
                    encoding="uint16"
                )
            )
            return f"{hex(NET_ID_1)[2:].upper()}{hex(NET_ID_2)[2:].upper()}"

    def disconnect(self) -> None:
        self._is_connected = False
        return self._client.disconnect()

    def read_load(self, load_id: int) -> dict:
        result = None
        load = self[f"Load_{load_id}"]
        if load is None:
            load = SocomecLoad(load_id, modbus_id=self._modbus_id, client=self._client)
            result = load.read_energy()
            self[f"Load_{load_id}"] = load
        else:
            result = load.read_energy()
            
        return result