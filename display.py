def display(state):
    for i in range(3):
        for j in range(3):
            item = state[i * 3 + j]
            item = item if item != 0 else '_'
            print(item, end=' ')
        print()
    print()
