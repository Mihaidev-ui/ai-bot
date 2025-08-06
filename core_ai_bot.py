
from strategies.strategy_wave import detect_wave
from ai.ai_scorer import score_strategy
from training.loop import train_loop

class AIBot:
    def __init__(self):
        self.memory = []
        print("[INIT] AIBot extins inițializat.")

    def analyze(self, data):
        result = detect_wave(data)
        score = score_strategy(result)
        self.memory.append((data, result, score))
        print(f"[ANALYZE] Data: {data}, Score: {score}")
        return score

    def evolve(self):
        print("[EVOLVE] Simulare evoluție strategie...")
        if self.memory:
            best = max(self.memory, key=lambda x: x[2])
            print(f"[EVOLVE] Cel mai bun: {best}")
        else:
            print("[EVOLVE] Nicio strategie evaluată.")

    def train(self):
        print("[TRAIN] Antrenament AI...")
        train_loop()

    def run(self, data):
        print("[RUN] Ciclu complet AI")
        self.analyze(data)
        self.evolve()
        self.train()
