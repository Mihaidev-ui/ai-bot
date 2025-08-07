class AIBot:
    def __init__(self):
        self.config = CONFIG
        self.memory = Memory()
        self.orchestrator = Orchestrator(self.memory)
        self.executor = ExecutionFlow(self.memory)

    def run(self):
        log("Starting AI Trading Bot...")
        strategies = self.orchestrator.load_strategies()
        for strat in strategies:
            log(f"Executing: {strat.name}")
            result = self.executor.execute(strat)
            self.memory.save_result(strat.name, result)
        self.orchestrator.evolve()
        log("Cycle complete.")
