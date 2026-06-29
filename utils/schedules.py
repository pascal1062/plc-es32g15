# time_manager.py
from datetime import datetime

class TimeSchedule:
    def __init__(self, start_time_str: str, end_time_str: str):
        """
        Initialise une plage horaire au format "HH:MM".
        Exemple : schedule = TimeSchedule("06:00", "20:00")
        """
        self.start_str = start_time_str
        self.end_str = end_time_str
        
    def change_hours(self, new_start_str: str, new_end_str: str):
        """
        MÉTHODE PUBLIQUE : Permet de changer l'horaire à tout moment après la création.
        Exemple : config.SCHED_PISCINE.change_hours("08:00", "18:00")
        """
        self.start_str = new_start_str
        self.end_str = new_end_str
        print(f"[⏰ TimeSchedule] Nouvel horaire appliqué : {self.start_str} à {self.end_str}")

    @property
    def is_active(self) -> bool:
        """
        Vérifie si l'heure actuelle de la Raspberry Pi est dans la plage horaire.
        Retourne True ou False.
        """
        now = datetime.now().time()
        
        # Conversion des chaînes "HH:MM" en objets time de Python
        try:
            start_time = datetime.strptime(self.start_str, "%H:%M").time()
            end_time = datetime.strptime(self.end_str, "%H:%M").time()
        except ValueError as e:
            # Sécurité en cas de mauvaise frappe dans la config lors d'un hot reload
            print(f"[❌ ERREUR HORAIRE] Format d'heure invalide ({self.start_str} ou {self.end_str}) : {e}")
            return False

        # Cas 1 : Plage horaire standard dans la même journée (ex: 06:00 à 20:00)
        if start_time <= end_time:
            return start_time <= now <= end_time
        
        # Cas 2 : Plage horaire à cheval sur minuit (ex: 22:00 à 05:00)
        else:
            return now >= start_time or now <= end_time
