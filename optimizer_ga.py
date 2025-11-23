import random

def score_config(cfg):
    # placeholder: evaluate config on historical data; here use synthetic score
    return random.uniform(0,1)

def ga_optimize(param_space, population_size=20, generations=10):
    # param_space: dict name->list of possible values
    keys = list(param_space.keys())
    def random_individual():
        return {k: random.choice(param_space[k]) for k in keys}
    population = [random_individual() for _ in range(population_size)]
    for g in range(generations):
        scored = [(ind, score_config(ind)) for ind in population]
        scored.sort(key=lambda x:-x[1])
        # keep top half
        survivors = [ind for ind,_ in scored[:population_size//2]]
        # breed
        children = []
        while len(children) < population_size - len(survivors):
            a = random.choice(survivors); b = random.choice(survivors)
            child = {}
            for k in keys:
                child[k] = random.choice([a[k], b[k]])
                if random.random() < 0.1:
                    child[k] = random.choice(param_space[k])
            children.append(child)
        population = survivors + children
    best = max(population, key=score_config)
    return best
