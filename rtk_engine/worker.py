def calculate(x):
    # Placeholder benchmark workload.
    # Real RTK equations will be connected after scaling validation.
    value = 0
    for i in range(500):
        value += (x * i) % 997
    return value
