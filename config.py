# config.py
from modbus_service import ModbusPLCService
from redis_service import RedisPLCService
from io_objects import AnalogInput, BinaryInput, DigitalOutput, AnalogOutput
from utils.schedules import TimeSchedule
from utils.timers import PLCReadTimer
from utils.ntc10KTypeIII import SCALE_RANGE as SR1
from utils.ntc10KDegC_B3950 import SCALE_RANGE as SR2
from utils.aicPhotocell import SCALE_RANGE as SR3
#from utils.therm10KDegCPullD import SCALE_RANGE

# ==============================================================================
# 1. PARAMÈTRES DE CONFIGURATION PHYSIQUE
# ==============================================================================
#PORT = '/dev/ttyUSB0'       # Port série sur votre Raspberry Pi
PORT = '/dev/ttySC0'       # Port série sur votre Raspberry Pi
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

# --- ENTRÉES ANALOGIQUES (registre modbus) ---
T1_TEMP_EXT  = AnalogInput(name="Temp Exterieur T1", register_index=9, filter=80.0, calib=0.0, scale=SR2)
T2_TEMP_PAN  = AnalogInput(name="Temp Panneau T2", register_index=10, filter=80.0, calib=0.0, scale=SR1)
T3_TEMP_PISC = AnalogInput(name="Temp Piscine T3", register_index=11, filter=80.0, calib=0.0, scale=SR1)
T4_PHOTO_EXT = AnalogInput(name="Photocell Ext T4", register_index=12, filter=80.0, calib=0.0, scale=SR3)

# --- ENTRÉES BINAIRES / DIGITALES (registre modbus) ---
IN1_BP_START_IRRIG = BinaryInput(name="Bouton start Irrig IN1", register_index=5)
IN2_BP_STOP_IRRIG = BinaryInput(name="Bouton stop Irrig IN2", register_index=6)

# --- SORTIES VIRTUEL / DIGITALES (registre modbus) ---
REFRESH_HREG0 = DigitalOutput(name="modbus serial refresh", modbus_address=0, register_index=0, initial_value=0)

# --- SORTIES BINAIRES / DIGITALES (registre modbus) ---
R1_AD_POM_PISC = DigitalOutput(name="A/D Pompe Pisc R1", modbus_address=1, register_index=1, initial_value=0)
R2_LIBRE       = DigitalOutput(name="Relais Libre R2", modbus_address=2, register_index=2, initial_value=0)
R3_LIBRE       = DigitalOutput(name="Relais Libre R3", modbus_address=3, register_index=3, initial_value=0)
R4_AD_IRRIG    = DigitalOutput(name="A/D Pompe Irrig R4", modbus_address=4, register_index=4, initial_value=0)

# --- SORTIES ANALOGIQUES (Adresse Modbus réelle pour l'écriture) ---
VO1_CHAUFF_PAN = AnalogOutput(name="Chauffage Panneau VO1", modbus_address=17, register_index=17, initial_value=0)
VO2_LIBRE = AnalogOutput(name="Sortie Analog Libre VO2", modbus_address=18, register_index=18, initial_value=0)


# ==============================================================================
# 4. INSTANCIATION DES HORAIRES (Schedules)
# ==============================================================================
# Horaire pour la piscine (6h à 20h)
SCHED_PISCINE = TimeSchedule(start_time_str="06:00", end_time_str="20:00")

# Horaire pour l'arrosage du jardin (uniquement la nuit de 22h à 23h30)
SCHED_ARROSAGE_SOIR = TimeSchedule(start_time_str="22:00", end_time_str="23:30")


# ==============================================================================
# 5. INSTANCIATION DE VOS TIMERS
# ==============================================================================
TIMER_IRRIGATION = PLCReadTimer("Irrigation_Jardin")