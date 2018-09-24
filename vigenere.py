import click
import sys
from itertools import cycle


@click.command()
@click.option('-k', '--key', required=True,
              help="Key to use to encode/decode")
@click.option('-d', '--decode', is_flag=True,
              help="Decode ciphertext instead of encoding")
def main(key, decode):
    shifts = cycle(ord(c.lower()) - ord('a') for c in key)

    def shift(c):
        if not c.isalpha():
            return c  # only letters

        up = c.isupper()

        s = next(shifts)
        offset = ord('A') - ord('a') if up else 0
        if decode:
            s = -s

        if up:  # preserve lower/upper
            s -= offset

        e = (ord(c) - ord('a') + s) % 26
        return chr(e + ord('a') + offset)

    for line in sys.stdin:
        print(''.join(shift(c) for c in line.strip()))


if __name__ == "__main__":
    main()
