import click
from PIL import Image


def ascii_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)


def bin_to_ascii(bin_string):
    return ''.join(chr(int(bin_string[i*8:i*8+8] or '0', 2))
                   for i in range((len(bin_string) // 8) + 1))


def encode(bits, path_in, path_out, row_first):
    bits = iter(bits)
    im = Image.open(path_in)
    pix = im.load()

    def _tamper(v, b):
        return int(format(v, 'b')[:-1] + b, 2)

    def _bit():
        try:
            return next(bits)
        except StopIteration:
            return '0'

    coords = [(i, j) for j in range(im.height) for i in range(im.width)]
    if row_first:
        coords = [(i, j) for i in range(im.width) for j in range(im.height)]

    for i, j in coords:
        r, g, b, a = pix[i, j]
        r = _tamper(r, _bit())
        g = _tamper(g, _bit())
        b = _tamper(b, _bit())
        pix[i, j] = r, g, b, a

    im.save(path_out)


def decode(path_in, row_first):
    im = Image.open(path_in)
    pix = im.load()

    rows, cols = im.height, im.width

    def _comp(i, j, k):
        return pix[i, j][k]

    def _get(i, j):
        return ''.join(bin(_comp(i, j, k))[-1] for k in (0, 1, 2))

    if row_first:
        return ''.join(_get(i, j) for i in range(cols) for j in range(rows))
    return ''.join(_get(i, j) for j in range(rows) for i in range(cols))


@click.group()
def main():
    pass


@click.option('-i', '--input-image', required=True,
              help="Path to the input image")
@click.option('-o', '--output-image', required=True,
              help="Path to the output image")
@click.option('-t', '--text', required=True,
              help="ASCII message to hide")
@click.option('-r', '--rows-first', is_flag=True,
              help="Encode first on rows then on cols. Default cols then rows")
@main.command(name='encode')
def encode_image(text, input_image, output_image, rows_first):
    b = ascii_to_bin(text)
    encode(b, input_image, output_image, rows_first)


@click.option('-i', '--input-image', required=True,
              help="Path to the input image")
@click.option('-r', '--rows-first', is_flag=True,
              help="Decode first rows then cols. Default cols then rows")
@main.command(name='decode')
def decode_image(input_image, rows_first):
    print(bin_to_ascii(decode(input_image, rows_first)))


if __name__ == "__main__":
    main()
