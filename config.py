# config.py
from modbus_service import ModbusPLCService
from redis_service import RedisPLCService
from io_objects import AnalogInput, BinaryInput, DigitalOutput, AnalogOutput
from utils.time_manager import TimeSchedule
from utils.therm10KDegCPullD import SCALE_RANGE

# ==============================================================================
# 1. PARAMÈTRES DE CONFIGURATION PHYSIQUE
# ==============================================================================
PORT = '/dev/ttyUSB0'       # Port série sur votre Raspberry Pi
BAUDRATE = 38400            # Vitesse de communication
SLAVE_ID = 1                # Identifiant esclave Modbus de la carte PLC
POLL_INTERVAL = 0.100       # Cycle de scan de 100 millisecondes

# --- Activation / Configuration Redis ---
REDIS_ENABLED = True
redis_client = RedisPLCService(host='localhost', port=6379, db=0, enabled=REDIS_ENABLED)


# ==============================================================================
# 2. INSTANCE UNIQUE DU SERVICE MODBUS
# ==============================================================================
# Instancié ici de manière isolée pour être importé par les autres fichiers
plc = ModbusPLCService(port=PORT, baudrate=BAUDRATE, timeout=0.08)


# ==============================================================================
# 3. DÉFINITION DE VOS OBJETS ENTRÉES ET SORTIES (I/O)
# ==============================================================================

# --- ENTRÉES ANALOGIQUES (Index de position dans le tableau brut des 23 registres) ---
T1 = AnalogInput(name="Temp_Test_1", register_index=8, filter=80.0, calib=0.0, scale=SCALE_RANGE)
T2 = AnalogInput(name="Temp_Test_2", register_index=9, filter=80.0, calib=0.0, scale=SCALE_RANGE)
T4 = AnalogInput(name="Temp_Test_4", register_index=11, filter=80.0, calib=0.0, scale=SCALE_RANGE)

# --- ENTRÉES BINAIRES / DIGITALES (Index de position dans le tableau brut) ---
DI_BOUTON_START  = BinaryInput(name="Bouton_Start", register_index=4)
DI_BOUTON_STOP   = BinaryInput(name="Bouton_Stop", register_index=5)
DI_FIN_COURSE    = BinaryInput(name="Capteur_Fin_Course", register_index=6)

# --- SORTIES BINAIRES / DIGITALES (Adresse Modbus réelle pour l'écriture) ---
DO_VOYANT_RUN    = DigitalOutput(name="Voyant_Machine_Running", modbus_address=0, initial_value=0)
DO_POMPE         = DigitalOutput(name="Pompe_Principale", modbus_address=1, initial_value=0)

# --- SORTIES ANALOGIQUES (Adresse Modbus réelle pour l'écriture) ---
AO_VARIATEUR_VIT = AnalogOutput(name="Vitesse_Moteur", modbus_address=16, initial_value=0)


# ==============================================================================
# 4. INSTANCIATION DES HORAIRES (Schedules)
# ==============================================================================
# Horaire pour la piscine (6h à 20h)
SCHED_PISCINE = TimeSchedule(start_time_str="06:00", end_time_str="20:00")

# Horaire pour l'arrosage du jardin (uniquement la nuit de 22h à 23h30)
SCHED_ARROSAGE_SOIR = TimeSchedule(start_time_str="22:00", end_time_str="23:30")