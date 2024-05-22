import time

def random_int(seed: int, min_val, max_val) -> int:
    # Get the current time in milliseconds
    if not isinstance(max_val, int) and not isinstance(max_val, float):
        raise ValueError("max_val must be an integer or float")
    if not isinstance(min_val, int) and not isinstance(min_val, float):
        raise ValueError("min_val must be an integer or float")
    if min_val == max_val:
        return min_val
    if min_val > max_val:
        temp = min_val
        temp2 = max_val
        min_val = temp2
        max_val = temp
        del temp, temp2
    current_time = time.time()
    current_ms = int((current_time - int(current_time)) * 1000)
    # Calculate the range
    range_length = max_val - min_val + 1
    
    # Modify the seed based on its value and current_ms
    if seed < 50:
        modified_seed = seed
    else:
        modified_seed = seed / 50

    # Calculate the pseudo-random integer
    res = min_val + (round(modified_seed * current_ms) % range_length)
    return res

def random_choice(seed: int, choice_list: list) -> str:
    minl = range(len(choice_list))[0] +1
    maxl = range(len(choice_list))[len(choice_list) - 1] + 1
    res = random_int(seed, minl, maxl) - 1
    return choice_list[res]

def random_choicew(seed: int, choice_list: list, weights_norm: list) -> str:
    # Generate a random number between 0 and 1
    random_number = random_int(seed, 0, 10000) / 10000.0
    
    # Perform weighted selection
    cumulative_weight = 0.0
    for i, weight in enumerate(weights_norm):
        cumulative_weight += weight
        if random_number < cumulative_weight:
            return choice_list[i]

    # If for some reason the loop ends without returning a choice, return the last choice
    return choice_list[-1]

def normalize_weights(weights: list) -> list:
    total = sum(weights)
    return [w / total for w in weights]

def shuffle(seed, list_to_shuffle: list) -> list:
    lts = list_to_shuffle
    shuffled_list = lts.copy()
    n = len(shuffled_list)
    for i in range(n - 1, 0, -1):
        j = random_int(seed, 0, i)
        shuffled_list[i], shuffled_list[j] = shuffled_list[j], shuffled_list[i]
    return shuffled_list

def random_seed() -> int:
    seed = ""
    current_time = time.time()
    current_ms = int((current_time - int(current_time)) * 1000)
    for _ in range(200):
        check = random_int(current_ms, 0, 9)
        seed += str(check)
    return int(seed)