
from strategies.strategy_liquidity_grab import run_liquidity_strategy
from ai.scoring_engine import score_output
from training.optimizer import train_model

class AIBot:
    def __init__(self):
        self.results = []

    def execute_strategies(self, data):
        result = run_liquidity_strategy(data)
        score = score_output(result)
        self.results.append((result, score))
        return score

    def evolve_and_learn(self):
        if not self.results:
            print("Nimic de antrenat.")
            return
        best = max(self.results, key=lambda x: x[1])
        print("Cel mai bun rezultat:", best)
        train_model(best[0])
