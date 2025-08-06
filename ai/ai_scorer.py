
def score_strategy(output):
    if output.get("wave"):
        return output["strength"] / 10
    return 0.1
