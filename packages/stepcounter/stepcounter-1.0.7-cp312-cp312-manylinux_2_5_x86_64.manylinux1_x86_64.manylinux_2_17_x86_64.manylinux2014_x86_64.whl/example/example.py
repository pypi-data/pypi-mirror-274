class Counter:
    def __init__(self) -> None:
        # This line records __setattr__ of a Counter
        self.x = 0

    def add(self, num) -> None:
        # This line records __add__ (addition) of an int
        # and also records __setattr__ of a Counter as ints are immutable
        self.x += num


def gcd(a: int, b: int) -> int:
    # This line records __ne__ (not equal) function of an int
    while b != 0:
        # This line records __mod__ (modulo) function of an int
        a, b = b, a % b
    return a


def main() -> None:
    # Defining a list for example usage
    list_ = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # This line records __len__ (len) function of a list
    len(list_)

    # This line records pop function of a list
    list_.pop()

    # This line records __contains__ (in) function of a list
    # Evaluation is equal to the list_ length
    5 in list_

    # This line records the call of gcd function
    gcd(54545, 64545)

    counter = Counter()

    # This line records the call of add function of the Counter class
    counter.add(1)
