from typing import List


def display(state: List[int]):
    for i in range(3):
        for j in range(3):
            item = state[i * 3 + j]
            item = item if item != 0 else ' '
            print(item, end=' ')
        print()
    print()


def up(state: List[int]):
    index = state.index(0)
    if index > 5:
        return state[:]
    other = index + 3
    copy = state[:]

    copy[index] = copy[other]
    copy[other] = 0

    return copy


def down(state: List[int]):
    index = state.index(0)
    if index < 3:
        return state[:]

    other = index - 3
    copy = state[:]

    copy[index] = copy[other]
    copy[other] = 0

    return copy


def left(state: List[int]):
    index = state.index(0)

    if index % 3 == 2:
        return state[:]
    other = index + 1
    copy = state[:]

    copy[index] = copy[other]
    copy[other] = 0
    return copy


def main():
    state = [
        0, 1, 2,
        3, 4, 5,
        6, 7, 8
    ]
    display(state)
    state = left(state)
    display(state)


if __name__ == '__main__':
    main()
