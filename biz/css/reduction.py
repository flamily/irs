def apply_reduction(raw_results):
    results = raw_results[0]["faceAttributes"]["emotion"]

    accumulator = 0
    count = 0
    for _, value in results.items():
        accumulator += value
        count += 1

    return (accumulator/count) * 100
