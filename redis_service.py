# redis_service.py
import redis
import json
import obj_serializer  # <-- Utilisation de votre fichier universel
import config

class RedisPLCService:
    def __init__(self, host='localhost', port=6379, db=0, enabled=True):
        self.enabled = enabled
        self.r = None
        self.pubsub = None
        
        if self.enabled:
            try:
                self.r = redis.Redis(host=host, port=port, db=db, decode_responses=True)
                self.r.ping()
                self.pubsub = self.r.pubsub()
                self.pubsub.subscribe('plc:commands')
                print("[🔴 Redis] Connecté. Prêt pour les objets universels.")
            except redis.ConnectionError:
                self.enabled = False

    def publish_telemetry(self, io_registry):
        """Pousse l'intégralité du système (I/O et Divers) vers Redis."""
        if not self.enabled or not self.r:
            return

        try:
            # 1. Sérialisation des Entrées
            inputs_data = {}
            for inp in io_registry.inputs:
                if inp.__class__.__name__ == "AnalogInput":
                    inputs_data[inp.name] = obj_serializer.serialize_analog_input(inp)
                else:
                    inputs_data[inp.name] = obj_serializer.serialize_binary_input(inp)

            # 2. Sérialisation des Sorties
            outputs_data = {}
            for out in io_registry.outputs:
                outputs_data[out.name] = obj_serializer.serialize_output(out)

            # 3. Sérialisation des Variables Diverses (Ex: Horaires TimeSchedule)
            system_schedules = {}
            # On cherche dynamiquement tous les TimeSchedule présents dans config.py
            for attr_name in dir(config):
                attr_value = getattr(config, attr_name)
                if attr_value.__class__.__name__ == "TimeSchedule":
                    system_schedules[attr_name] = obj_serializer.serialize_time_schedule(attr_value, attr_name)

            # Conversion JSON globale
            inputs_json = json.dumps(inputs_data)
            outputs_json = json.dumps(outputs_data)
            schedules_json = json.dumps(system_schedules)

            # Envoi groupé dans Redis (Cache + Publication)
            pipe = self.r.pipeline()
            pipe.set("plc:inputs", inputs_json)
            pipe.set("plc:outputs", outputs_json)
            pipe.set("plc:schedules", schedules_json)
            
            pipe.publish("plc:inputs", inputs_json)
            pipe.publish("plc:outputs", outputs_json)
            pipe.publish("plc:schedules", schedules_json)
            pipe.execute()
            
        except Exception as e:
            print(f"[❌ Redis] Erreur publication objets complexes : {e}")

    def check_incoming_commands(self):
        """Vérification des commandes entrantes de Node-RED."""
        if not self.enabled or not self.pubsub:
            return

        try:
            message = self.pubsub.get_message(ignore_subscribe_messages=True)
            if message and message['type'] == 'message':
                data = json.loads(message['data'])
                
                # Action existante : Changement d'heure à la volée
                if data.get("action") == "change_hours":
                    sched_name = data.get("schedule")
                    if hasattr(config, sched_name):
                        getattr(config, sched_name).change_hours(data.get("start"), data.get("end"))
                        
                # Action existante : Commande manuelle des sorties
                # Format attendu : {"action": "manual_command", "output": "DO_POMPE", "value": 1, "priority": 8}
                elif data.get("action") == "manual_command":
                    output_name = data.get("output")
                    new_value = data.get("value")
                    priority = data.get("priority")
                    if hasattr(config, output_name):
                        output_object = getattr(config, output_name)
                        output_object.write(new_value,priority)            
                        print(f"[🔴 Redis] Demande reçue : {output_name} cible définie à {new_value}")
                    else:
                        print(f"[❌ Redis] La sortie '{output_name}' n'existe pas dans config.py")
                            
        except Exception as e:
            print(f"[❌ Redis] Erreur traitement commande : {e}")
