# utils/timers.py
import time

class PLCReadTimer:
    def __init__(self, name: str):
        self.name = name
        self.start_time = None      # Stocke le moment précis du démarrage
        self.duration = 0           # Durée cible en secondes
        self.is_running = False     # État de marche du timer
        self.elapsed_before_pause = 0 # Permet de figer le temps en cas de stop/pause

    def start(self, minutes: float):
        """Démarre ou reprend la temporisation pour une durée en minutes."""
        if not self.is_running:
            self.duration = minutes * 60.0
            # Si le timer était en pause, on ajuste le point de départ
            self.start_time = time.perf_counter() - self.elapsed_before_pause
            self.is_running = True
            print(f"[⏱ Timer {self.name}] Démarré pour {minutes} minutes.")

    def stop(self):
        """Arrête (met en pause) le décompte sans le réinitialiser à zéro."""
        if self.is_running:
            self.elapsed_before_pause = self.get_elapsed_time()
            self.is_running = False
            print(f"[⏱ Timer {self.name}] Mis en pause.")

    def reset(self):
        """Réinitialise complètement le timer à zéro."""
        self.start_time = None
        self.duration = 0
        self.is_running = False
        self.elapsed_before_pause = 0
        print(f"[⏱ Timer {self.name}] Réinitialisé.")

    def get_elapsed_time(self) -> float:
        """Retourne le temps écoulé en secondes depuis le départ."""
        if not self.is_running:
            return self.elapsed_before_pause
        return time.perf_counter() - self.start_time

    def get_remaining_time(self) -> float:
        """Retourne le temps restant avant la fin en secondes (minimum 0)."""
        remaining = self.duration - self.get_elapsed_time()
        return max(0.0, remaining)

    @property
    def is_done(self) -> bool:
        """Retourne True si le temps imparti est écoulé et que le timer tournait."""
        if self.duration == 0:
            return False
        return self.get_elapsed_time() >= self.duration
