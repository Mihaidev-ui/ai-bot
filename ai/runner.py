
from core.ai_bot import AIBot

if __name__ == '__main__':
    bot = AIBot()
    sample_data = [1, 3, 2, 5, 8, 7, 2, 4, 6, 5, 1]
    score = bot.execute_strategies(sample_data)
    print("Scor calculat:", score)
    bot.evolve_and_learn()
