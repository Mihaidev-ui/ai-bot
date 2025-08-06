
def run_liquidity_strategy(data):
    zones = []
    for i in range(2, len(data)-2):
        if data[i-2] < data[i] > data[i+2]:
            zones.append({'type': 'liquidity', 'value': data[i]})
    return {'zones': zones, 'count': len(zones)}
