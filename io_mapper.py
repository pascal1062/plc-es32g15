# io_mapper.py (Mise à jour rapide des listes pour correspondre à config.py)
import config

class PLCIORegistry:
    def __init__(self):
        # Liste de toutes vos entrées à scanner et distribuer
        self.inputs = [
            config.T1,
            config.T2,
            config.T3,
            config.T4,
            config.DI_BOUTON_START,
            config.DI_BOUTON_STOP,
            config.DI_FIN_COURSE
        ]
        
        # Liste de toutes vos sorties à surveiller et synchroniser
        self.outputs = [
            config.DO_VOYANT_RUN,
            config.DO_POMPE,
            config.AO_VARIATEUR_VIT
        ]

    def scan_outputs(self, plc_service, slave_id: int):
        for output in self.outputs:
            output.update_hardware(plc_service, slave_id)

    def scan_inputs(self, raw_registers: list):
        if not raw_registers:
            return
        for input_obj in self.inputs:
            input_obj.update_from_raw(raw_registers)
