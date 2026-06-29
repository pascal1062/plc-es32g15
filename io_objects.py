# io_objects.py

ADC_VOLTS_CALIB = 24 # mV

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
        #self.ad_value = raw_registers[self.index]
        #register reading millivolts
        self.volts = (raw_registers[self.index] - ADC_VOLTS_CALIB) / 1000
        self.newvalue = self.aic(self.volts) + self.calib
        self.value = round(self.lastvalue + (( 100.0 - self.filter) / 100.0 * (self.newvalue - self.lastvalue)), 5)
        self.lastvalue = self.value
        

class BinaryInput:
    def __init__(self, name: str, register_index: int):
        self.name = name
        self.index = register_index
        self.value = 0 # 0 ou 1
        #self._newvalue = self.value
        self._lastvalue = self.value
        
    def changed(self):
        if self.value != self._lastvalue:
            val = 1
        else:
            val = 0
        self._lastvalue = self.value
        return val
    
    def rising(self):
        if self.value != self._lastvalue:
            val = self.value
        else:
            val = 0
        self._lastvalue = self.value
        return val
    
    def falling(self):
        if (self.value != self._lastvalue):
            val = not self.value
        else:
            val = 0
        self._lastvalue = self.value
        return val

    def update_from_raw(self, raw_registers: list):
        self.value = raw_registers[self.index]


class DigitalOutput:
    def __init__(self, name: str, modbus_address: int, register_index: int, initial_value: int = 0):
        self.name = name
        self.address = modbus_address
        self.index = register_index
        self.current_value = initial_value
        self.priority_array = {i: None for i in range(1, 17)}
        self.relinquish_default = initial_value
        
    def update_from_raw(self, raw_registers: list):
        """Met à jour l'état RÉEL de la sortie depuis le scan Modbus de 100ms."""
        self.current_value = raw_registers[self.index]

    @property
    def target_value(self) -> int:
        """Calcule la valeur cible selon la plus haute priorité active."""
        for priority in range(1, 17):
            value = self.priority_array[priority]
            if value is not None:
                return value
        return self.relinquish_default

    def write(self, value: int, priority: int,):
        """Définit la valeur pour une priorité spécifique (1 à 16)."""
        if not (1 <= priority <= 16):
            raise ValueError("La priorité doit être comprise entre 1 et 16.")
        self.priority_array[priority] = value

    def relinquishpriority(self, priority: int):
        """Libère une priorité spécifique en la remettant à None."""
        if not (1 <= priority <= 16):
            raise ValueError("La priorité doit être comprise entre 1 et 16.")
        self.priority_array[priority] = None

    def update_hardware(self, plc_service, slave_id: int) -> bool:
        """Vérifie s'il y a un changement et l'écrit sur le Modbus."""
        # target_value est maintenant évalué dynamiquement ici
        target = self.target_value
        if target != self.current_value:
            success = plc_service.write_register_raw(
                address=self.address, 
                value=target, 
                slave_id=slave_id
            )
            if success:
                print(f" -> [Sortie {self.name}] Synchronisée sur Modbus: {target}")
                #self.current_value = target --- on ne met a jour ici 
                return True
        return False


# La classe AnalogOutput suivra exactement la même logique que DigitalOutput
class AnalogOutput(DigitalOutput):
    pass
