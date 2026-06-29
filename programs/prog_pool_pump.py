# programs/prog_pool_pump.py
import config

def run():
    """Logique métier pour le contrôle de la pompe de piscine."""
    
    # RÈGLE 1 : Si le bouton STOP est appuyé, on coupe immédiatement la pompe
    #if config.DI_BOUTON_STOP.value == 1:
        #config.DO_POMPE.target_value = 0
        #return # On sort de la fonction
    #    pass
    
    # RÈGLE 2 : Si le bouton START est appuyé, on démarre la pompe
    #if config.DI_BOUTON_START.value == 1:
        #config.DO_POMPE.target_value = 1
        #print(config.DI_BOUTON_START.value)
    #    pass

    # RÈGLE 3 : Sécurité thermique complexe : si la température de la cuve 1 dépasse 45°C
    # (Exemple d'utilisation de la valeur brute ou scalée de l'objet)
    #if config.AI_TEMPERATURE_1.value > 450: # Si la valeur brute stockée est par ex. x10 (45.0°C)
        #config.DO_POMPE.target_value = 0
        #print("[ALERTE PISCINE] Surchauffe de la cuve ! Arrêt de sécurité.")
    #    pass

    # Utilisation directe de l'objet horaire
    if config.SCHED_PISCINE.is_active:
        #config.DO_POMPE.target_value = 1
        config.R1_AD_POM_PISC.write(1,10)
    else:
        #config.DO_POMPE.target_value = 0
        config.R1_AD_POM_PISC.write(0,10)