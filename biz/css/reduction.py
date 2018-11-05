def apply_reduction(raw_results):
    results = raw_results[0]["faceAttributes"]["emotion"]

    sum = 0
    count = 0
    for key, value in results.items():
        sum += value
        count += 1

    return (sum/count) * 100
