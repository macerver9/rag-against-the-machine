from src.indexing.markdown_chunker import find_split_position, split_long_block


if __name__ == "__main__":
    parrafos = """\
hola


que tal

me voy

"""

sin_parr = """\
hola
que
tal
"""

linea = "hola como estas"

sin_sep = "asdasgasdfafasdggasdgasdgasdfasdgsagsdfasdfasfa"

print(split_long_block("Hola mundo", 5))
print(split_long_block("abcdefghijklmnopqrst", 10))
print(split_long_block("Hola\n\nqué tal\n\namigo", 10))
print(split_long_block("Hola\n\nqué tal\n\namigo", 5))