
def run_advanced_liquidity_strategy(prices, volumes, highs, lows):
    zones = []
    for i in range(5, len(prices) - 5):
        recent_highs = highs[i-5:i]
        recent_lows = lows[i-5:i]
        is_liquidity_spike = prices[i] > max(recent_highs) and volumes[i] > max(volumes[i-5:i]) * 1.5
        is_fakeout = prices[i+1] < prices[i] and prices[i+2] < prices[i+1] and volumes[i+1] < volumes[i]

        confirmed_ob = lows[i+2] > lows[i+1] and prices[i+3] > prices[i+2]

        if is_liquidity_spike and is_fakeout and confirmed_ob:
            zones.append({
                'index': i,
                'price': prices[i],
                'volume': volumes[i],
                'context': {
                    'spike_over_highs': True,
                    'fakeout_pattern': True,
                    'order_block_confirmation': True
                }
            })

    confidence = min(len(zones) / 3, 1.0) if zones else 0.0
    return {
        'strategy': 'liquidity_grab_advanced',
        'zones_detected': len(zones),
        'zones': zones,
        'confidence_score': round(confidence, 2)
    }
