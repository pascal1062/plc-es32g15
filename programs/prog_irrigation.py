# programs/prog_irrigation.py
import config

def run():
    """Logique métier pour l'arrosage automatique du jardin."""
    
    # 1. ÉVÉNEMENT : Si on appuie sur le bouton START (ou via Node-RED), on lance le timer choisi
    if config.IN1_BP_START_IRRIG.value == 1:
        config.TIMER_IRRIGATION.start(minutes=5.0)

    # 2. SÉCURITÉ : Si on appuie sur le bouton STOP, on arrête tout immédiatement
    if config.IN2_BP_STOP_IRRIG.value == 1:
        config.TIMER_IRRIGATION.reset()
        config.R4_AD_IRRIG.write(0,10) # Fermeture électrovanne/pompe
        return

    # 3. ACTION : Si le timer est actif (en cours de décompte), on démarre l'arrosage
    if config.TIMER_IRRIGATION.is_running and not config.TIMER_IRRIGATION.is_done:
        config.R4_AD_IRRIG.write(1,10)
        pass
    
    # 4. FIN AUTOMATIQUE : Dès que les 20 minutes sont écoulées
    if config.TIMER_IRRIGATION.is_done:
        print(f"Arrosage terminé avec succès. Temps écoulé")
        config.R4_AD_IRRIG.write(0,10) # Arrêt de la pompe
        config.TIMER_IRRIGATION.reset()          # On nettoie le timer pour la prochaine fois

