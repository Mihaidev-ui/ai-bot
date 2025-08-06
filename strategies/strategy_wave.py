
def detect_wave(data):
    print("Detectare undă în date:", data)
    if max(data) - min(data) > 5:
        return {"wave": True, "strength": max(data) - min(data)}
    return {"wave": False}
