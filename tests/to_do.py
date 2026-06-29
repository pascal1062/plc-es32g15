# modif digital output
# io_objects.py

class DigitalOutput:
    def __init__(self, name: str, modbus_address: int, register_index: int, initial_value: int = 0):
        self.name = name
        self.address = modbus_address      # Adresse pour l'écriture (ex: 11)
        self.index = register_index        # NOUVEAU : Index dans le tableau des 23 registres pour la lecture
        self.current_value = initial_value # Réalité physique (lue depuis le PLC)
        self.target_value = initial_value  # Volonté logique (définie par vos scripts)

    def update_from_raw(self, raw_registers: list):
        """Met à jour l'état RÉEL de la sortie depuis le scan Modbus de 100ms."""
        self.current_value = raw_registers[self.index]

    def update_hardware(self, plc_service, slave_id: int) -> bool:
        """Compare la volonté logique avec la réalité physique du PLC."""
        if self.target_value != self.current_value:
            success = plc_service.write_register_raw(
                address=self.address, 
                value=self.target_value, 
                slave_id=slave_id
            )
            if success:
                print(f" -> [Sortie {self.name}] Écriture Modbus : {self.target_value} (Ancien état lu : {self.current_value})")
                # On ne met pas à jour current_value ici ! 
                # C'est le prochain scan de lecture qui confirmera que le PLC a bien changé d'état.
                return True
        return False


# La classe AnalogOutput hérite automatiquement du même comportement de Read-Back
class AnalogOutput(DigitalOutput):
    pass


#------------------------------------------------------------------------------------------------------------------------------------
# config.py
# (Conservez vos configurations de connexion, de services et d'entrées...)

# --- SORTIES BINAIRES / DIGITALES ---
# Paramètres : Nom, Adresse d'écriture Modbus, Index de lecture dans le scan de 23 registres
DO_VOYANT_RUN    = DigitalOutput(name="Voyant_Machine_Running", modbus_address=10, register_index=10, initial_value=0)
DO_POMPE         = DigitalOutput(name="Pompe_Principale", modbus_address=11, register_index=11, initial_value=0)

# --- SORTIES ANALOGIQUES ---
AO_VARIATEUR_VIT = AnalogOutput(name="Vitesse_Moteur", modbus_address=12, register_index=12, initial_value=0)


#----------------------------------------------------------------------------------------------------------------------------------
# io_mapper.py
import config

class PLCIORegistry:
    def __init__(self):
        self.inputs = [
            config.AI_TEMPERATURE_1,
            config.DI_BOUTON_START,
            config.DI_BOUTON_STOP
        ]
        self.outputs = [
            config.DO_VOYANT_RUN,
            config.DO_POMPE,
            config.AO_VARIATEUR_VIT
        ]

    def scan_outputs(self, plc_service, slave_id: int):
        """Étape 1 : Pousse les écritures si la logique diffère de la réalité physique."""
        for output in self.outputs:
            output.update_hardware(plc_service, slave_id)

    def scan_inputs(self, raw_registers: list):
        """Étape 2 & 3 : Distribue les données lues aux entrées ET rafraîchit l'état réel des sorties."""
        if not raw_registers:
            return
            
        # Met à jour les entrées
        for input_obj in self.inputs:
            input_obj.update_from_raw(raw_registers)
            
        # NOUVEAU : Met à jour la réalité des sorties directement depuis la puce du PLC
        for output_obj in self.outputs:
            output_obj.update_from_raw(raw_registers)
