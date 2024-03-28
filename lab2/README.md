# Lab 2

To run, execute the following:

```bash
python main.py
```

> May have to use `python3`, or install python if it is not on your system

Accepts the following arguments
- `--size=`
    - Size of the board
- `--depth=`
    - Depth limit of the alpha-beta algorithm
- `--winning-length=`
    - The number of squares in a row to win
- `--move-three-distance=`
    - The distance the first players second move must be placed away from their first
- `--eval-func=`
    - Which evaluation function to use. 1 for evaluation function 1, any other int for 2

Note there is not error handling on these. If `--move-three-distance=100` and `--size=2`, the program will not work

Example of using all the arguments:

```bash
python main.py --size=9 --depth=3 --winning-length=3 --move-three-distance=3 --eval-func=2
```

> Note: they can appear in any order
