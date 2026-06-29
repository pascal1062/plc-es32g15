# modbus_service.py
from typing import Union, List
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

MAX_REG = 31

class ModbusPLCService:
    def __init__(self, port: str, baudrate: int, timeout: float = 0.08):
        self.port = port
        self.client = ModbusSerialClient(
            port=port, baudrate=baudrate, parity='N', stopbits=1, bytesize=8, timeout=timeout
        )

    def connect(self) -> bool:
        return self.client.connect()

    def disconnect(self):
        self.client.close()

    def write_register_raw(self, address: int, value: int, slave_id: int = 1) -> bool:
        """Écrit directement une valeur dans un registre."""
        try:
            response = self.client.write_register(address=address, value=value, slave=slave_id)
            return not response.isError()
        except ModbusException:
            return False

    def read_registers_raw(self, address: int = 0x00, count: int = MAX_REG, slave_id: int = 1) -> Union[List, None]:
        """Lit directement un bloc de registres."""
        try:
            response = self.client.read_holding_registers(address=address, count=count, slave=slave_id)
            if response.isError():
                return None
            return response.registers
        except ModbusException:
            return None
