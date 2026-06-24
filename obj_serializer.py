# obj_serializer.py

def serialize_analog_input(ai_obj) -> dict:
    """Squelette pour les entrées analogiques complexes."""
    return {
        "name": ai_obj.name,
        "value": ai_obj.value,
        "ad_value": getattr(ai_obj, "ad_value", 0),
        "scale": getattr(ai_obj, "scale", 1.0),
        "calibration": getattr(ai_obj, "calib", 0.0),
        "filtre": getattr(ai_obj, "filter", 0.0),
        "volt": getattr(ai_obj, "volts", 0.0),
        "index": ai_obj.index
    }

def serialize_binary_input(di_obj) -> dict:
    """Squelette pour les entrées binaires."""
    return {
        "name": di_obj.name,
        "value": di_obj.value,
        "index": di_obj.index
    }

def serialize_output(out_obj) -> dict:
    """Squelette pour les sorties (Digital/Analog)."""
    return {
        "name": out_obj.name,
        "current_value": out_obj.current_value,
        "target_value": out_obj.target_value,
        "address": out_obj.address,
        "priority": out_obj.priority_array        
    }

def serialize_time_schedule(sched_obj, key_name: str) -> dict:
    """Squelette pour exporter un horaire TimeSchedule vers Node-RED."""
    return {
        "id": key_name,                     # Exemple: "SCHED_PISCINE"
        "start": sched_obj.start_str,
        "end": sched_obj.end_str,
        "is_active": sched_obj.is_active
    }
