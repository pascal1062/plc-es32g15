# programs/prog_irrigation.py
import config

def run():
    """Logique métier pour l'arrosage automatique du jardin."""
    
    # RÈGLE 1 : Si le capteur de fin de course (utilisé ici comme détecteur de pluie ou niveau haut) est actif,
    # on n'arrose pas et on éteint le voyant running.
    if config.DI_FIN_COURSE.value == 1:
        #config.DO_VOYANT_RUN.target_value = 0
        config.DO_VOYANT_RUN.write(1,10)
        #config.AO_VARIATEUR_VIT.target_value = 0 # Arrêt du variateur/électrovanne
        #return

    # RÈGLE 2 : Si la pression descend trop bas (ex: sous 200 unités brutes), on allume le voyant pour indiquer un flux
    if config.T4.value < 200:
        #config.DO_VOYANT_RUN.target_value = 1
        #config.AO_VARIATEUR_VIT.target_value = 500 # On ouvre la vanne analogique à moitié (50%)
        pass
