from .randomness import *
floor: int = 0
instseed = randomness.random_seed()

def random_int(seed: int, min_val, max_val) -> int:
    res = randomness.random_int(seed, min_val, max_val)
    return res

def random_choice(seed: int, choice_list: list) -> str:
    res = randomness.random_choice(seed, choice_list)
    return res

def random_choicew(seed: int, choice_list: list, weights_norm: list) -> str:
    res = randomness.random_choicew(seed, choice_list, weights_norm)
    return res

def normalize_weights(weights: list) -> list:
    res = randomness.normalize_weights(weights)
    return res

def shuffle(seed, list_to_shuffle: list) -> list:
    res = randomness.shuffle(seed, list_to_shuffle)
    return res

def random_seed() -> int:
    res = randomness.random_seed()
    return res