from __future__ import annotations
import logging

from iot_protocols.devices.basics import Device
from iot_protocols.devices.interfaces import EnergyMeter
from iot_protocols.devices.models import DeviceHardware
from iot_protocols.protocols.iec62056.client import SerialClient, TariffResponse, messages
from iot_protocols.data import Serie

DEFAULT_ENERGY_REGISTER_MAPPING = {
    "1.25": "P",
    "3.25": "R",
    "1.8.0": "A+",
    "2.8.0": "A",
    "3.8.0": "Q+",
    "4.8.0": "Q-",
    "1.4.0": "P+",
    "2.4.0": "P-",
    "21.25": "P:1",
    "23.25": "R:1",
    "21.8.0": "A+:1",
    "22.8.0": "A-:1",
    "41.25": "P:2",
    "43.25": "R:2",
    "41.8.0": "A+:2",
    "42.8.0": "A-:2",
    "61.25": "P:3",
    "63.25": "R:3",
    "61.8.0": "A+:3",
    "62.8.0": "A-:3"
}


class IEC62056SerialMeter(Device, EnergyMeter):

    _type = "EnergyMeter"
    _energy_mapping = DEFAULT_ENERGY_REGISTER_MAPPING

    def __init__(self,
                 meter_id: str,
                 port: str,
                 baudrate: int=9600,
                 parity: str="E",
                 bytesize: int=7,
                 stopbits: int=1,
                 **kwargs
                 ) -> None:
        super().__init__()
        self._meter_id = meter_id
        self._client = SerialClient(
            baudrate=baudrate,
            port=port,
            parity=parity,
            bytesize=bytesize,
            stopbits=stopbits,
        )
        self._table = kwargs.get("table", 7)
        self._energy_mapping = kwargs.get("mapping", DEFAULT_ENERGY_REGISTER_MAPPING)

    def connect(self) -> None:
        self._client.connect()
        self._read_serial_number_and_model_info()

    def disconnect(self) -> None:
        self._is_connected = False
        self._client.disconnect()
    
    @property
    def protocol(self) -> SerialClient:
        return self._client
    
    @property
    def hardware(self) -> DeviceHardware:
        return DeviceHardware(
            serialNumber=self._serial_number,
            model=self._model
        )

    def _read_serial_number_and_model_info(self) -> None:
        identification_message = None
        with self._client as client:
            identification_message = client.read_tariff_identification(
                device_address=self._meter_id,
                ack_stop=True
            )
        if isinstance(identification_message, messages.IdentificationMessage):
            # Indicate that the response from the meter is valid.
            self._is_connected = True
            self._model = identification_message.identification[1:].replace("\\", "")
            self._serial_number = self._meter_id
            self._id = f"{identification_message.manufacturer}_{self._serial_number}"
        
        else:
            self._is_connected = False
    
    def _get_memory_index_register(self, tariff_response: TariffResponse) -> str | None:
        """_get_memory_index_register Check if the previous month index register exists. If yes return the last_month index value, else None.

        Args:
            tariff_response (TariffResponse): the response from the device.

        Returns:
            str | None: the index value
        """
        for dataset in tariff_response.data:
            if dataset.address == "0.1.0":
                return dataset.value
       
    def _parse_tariff_response(self, response: TariffResponse, old_index: str = None):
        result = {}
        for dataset in response.data:
            if dataset.value is not None and dataset.address in self._energy_mapping:
                key = self._energy_mapping[dataset.address]
                result.update({key: {"value": float(dataset.value), "unit": dataset.unit}})
            
            # Handling of previous period registers
            elif old_index is not None and dataset.value is not None:
                splited = dataset.address.split("*")
                if len(splited) > 1 and splited[0] in self._energy_mapping and splited[1] == old_index:
                    key = self._energy_mapping[splited[0]]
                    result.update({f"{key}_old": {"value": float(dataset.value), "unit": dataset.unit}})
        
        return result
    
    def read_energy(self, table: int=None, **kwargs) -> None:
        response = None
        with self._client as client:
            response = client.request(
                meter_address=self._meter_id,
                table=table
            )
            if not isinstance(response, TariffResponse):
                logging.error(f"Invalid response from meter : {response}")
                return 

            if response.checked == False:
                logging.debug(f"Invalid bcc (received: {response.bcc})!")
                self._bcc_last_check = False
        
        if response is not None:
            old_index = self._get_memory_index_register(response)
            result = self._parse_tariff_response(response, old_index=old_index)
            return result