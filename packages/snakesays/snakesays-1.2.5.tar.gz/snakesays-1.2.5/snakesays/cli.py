import sys
from snakesays import snake


def snakesay():
    snake.say(" ".join(sys.argv[1:]))


if __name__ == "__main__":
    snakesay()
