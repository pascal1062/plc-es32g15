# io_mapper.py (Mise à jour rapide des listes pour correspondre à config.py)
import config

class PLCIORegistry:
    def __init__(self):
        # Liste de toutes vos entrées à scanner et distribuer
        self.inputs = [
            config.T1_TEMP_EXT,
            config.T2_TEMP_PAN,
            config.T3_TEMP_PISC,
            config.T4_PHOTO_EXT,
            config.IN1_BP_START_IRRIG,
            config.IN2_BP_STOP_IRRIG,
        ]
        
        # Liste de toutes vos sorties à surveiller et synchroniser
        self.outputs = [
            config.REFRESH_HREG0,
            config.R1_AD_POM_PISC,
            config.R2_LIBRE,
            config.R3_LIBRE,
            config.R4_AD_IRRIG,
            config.VO1_CHAUFF_PAN,
            config.VO2_LIBRE
        ]

    def scan_outputs(self, plc_service, slave_id: int):
        for output in self.outputs:
            output.update_hardware(plc_service, slave_id)

    def scan_inputs(self, raw_registers: list):
        if not raw_registers:
            return
        for input_obj in self.inputs:
            input_obj.update_from_raw(raw_registers)

        # NOUVEAU : Met à jour la réalité des sorties directement depuis la puce du PLC
        for output_obj in self.outputs:
            output_obj.update_from_raw(raw_registers)