# main.py
import time
import config
from io_mapper import PLCIORegistry

# IMPORTATION DE VOS PROGRAMMES DE LOGIQUE
from programs import prog_pool_pump
from programs import prog_irrigation

def main():
    io_system = PLCIORegistry()
    
    if not config.plc.connect():
        print("Erreur d'ouverture du port série Modbus.")
        return

    print("Scanner PLC & Moteur de programmes démarrés (100ms)...")
    
    print("Scanner PLC actif avec synchronisation Redis...")
    cycle_counter = 0

    try:
        while True:
            start_time = time.perf_counter()
            cycle_counter += 1
            
            # =============================================================
            # 0. INTERCEPTION DES ORDRES NODE-RED via REDIS
            # =============================================================
            config.redis_client.check_incoming_commands()

            # 1. ÉCRITURE : Synchronise les sorties si un programme a changé une target_value au cycle précédent
            io_system.scan_outputs(config.plc, config.SLAVE_ID)

            # 2. LECTURE : Récupère l'état à jour des 23 registres de la carte PLC
            raw_data = config.plc.read_registers_raw(slave_id=config.SLAVE_ID)
            
            if raw_data is not None:
                # 3. MISE À JOUR : Injecte les données fraîches dans les objets d'entrées
                io_system.scan_inputs(raw_data)
                
                # =============================================================
                # 4. EXÉCUTION DES LOGIQUES MÉTIER (Vos scripts de programmes)
                # =============================================================
                # Chaque programme s'exécute l'un après l'autre avec les mêmes données d'entrées synchronisées
                prog_pool_pump.run()
                prog_irrigation.run()
                # =============================================================

                # =============================================================
                # 5. ENVOI VERS REDIS (Pour Node-RED)
                # =============================================================
                # S'exécute de façon transparente à chaque cycle de 100ms
                # config.redis_client.publish_telemetry(io_system)
                # voir plus bas send à toutes les secondes
                # =============================================================

                # 6. AFFICHAGE TERM : Toutes les secondes
                if cycle_counter >= 10:
                    current_time = time.strftime('%H:%M:%S')
                    print(f"[{current_time}] Registres bruts (23) : {raw_data} -> Données poussées vers Redis")
                    config.redis_client.publish_telemetry(io_system)
                    cycle_counter = 0

            # Contrôle strict du cycle de 100ms
            elapsed = time.perf_counter() - start_time
            sleep_time = config.POLL_INTERVAL - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                print(f"Warning: Dépassement de cycle ! {elapsed*1000:.1f}ms")

    except KeyboardInterrupt:
        print("\nArrêt du système d'automatisation.")
    finally:
        config.plc.disconnect()

if __name__ == "__main__":
    main()
