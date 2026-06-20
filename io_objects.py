# io_objects.py

ADC_VOLTS = 3.3 * 1.055

class AnalogInput:
    def __init__(self, name: str, register_index: int, filter: float, calib: float, scale: object):
        self.name = name
        self.index = register_index
        self.filter = filter
        self.calib = calib
        self.scale = scale
        self.ad_value = 0
        self.volts = 0.0
        self.value = 0.0
        self.newvalue = 0.0
        self.lastvalue = 0.0
        #self.value = self.presentvalue
        
    def update_from_raw_old(self, raw_registers: list):
        self.value = raw_registers[self.index]
        #self.ad_value = raw_registers[self.index]
        #self.volts = self.ad_value * (ADC_VOLTS / 4095)
        
    def aic(self, v):
        sr = self.scale
        _volt = v

        if sr[-1][0] < sr[0][0] and _volt <= sr[-1][0]: 
            return sr[-1][1]  
        if sr[-1][0] < sr[0][0] and _volt >= sr[0][0]: 
            return sr[0][1]   

        if sr[-1][0] > sr[0][0] and _volt <= sr[0][0]: 
            return sr[0][1]
        if sr[-1][0] > sr[0][0] and _volt >= sr[-1][0]: 
            return sr[-1][1]
        
        for i in range(len(sr) - 1): 
            volt1, val1 = sr[i] 
            volt2, val2 = sr[i+1] 

            if  (volt1 >= _volt >= volt2) or (volt1 <= _volt <= volt2):
                # Linear interpolation
                val = val1 + (val2 - val1) * ((_volt - volt1) / (volt2 - volt1))
                return val
           
        return self._lastvalue
    
    def update_from_raw(self, raw_registers: list):
        self.ad_value = raw_registers[self.index]
        self.volts = self.ad_value * (ADC_VOLTS / 4095)
        self.newvalue = self.aic(self.volts) + self.calib
        self.value = round(self.lastvalue + (( 100.0 - self.filter) / 100.0 * (self.newvalue - self.lastvalue)), 5)
        self.lastvalue = self.value
        

class BinaryInput:
    def __init__(self, name: str, register_index: int):
        self.name = name
        self.index = register_index
        self.value = 0 # 0 ou 1

    def update_from_raw(self, raw_registers: list):
        self.value = raw_registers[self.index]


class DigitalOutput:
    def __init__(self, name: str, modbus_address: int, initial_value: int = 0):
        self.name = name
        self.address = modbus_address
        self.current_value = initial_value
        self.target_value = initial_value  # C'est cette variable que vos futurs scripts modifieront

    def update_hardware(self, plc_service, slave_id: int) -> bool:
        """Vérifie s'il y a un changement et l'écrit sur le Modbus."""
        if self.target_value != self.current_value:
            success = plc_service.write_register_raw(
                address=self.address, 
                value=self.target_value, 
                slave_id=slave_id
            )
            if success:
                print(f" -> [Sortie {self.name}] Synchronisée sur Modbus: {self.target_value}")
                self.current_value = self.target_value
                return True
        return False

# La classe AnalogOutput suivra exactement la même logique que DigitalOutput
class AnalogOutput(DigitalOutput):
    pass
