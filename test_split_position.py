from src.indexing.markdown_chunker import find_split_position


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

print(find_split_position(parrafos, 0, 20))
print(find_split_position(sin_parr, 0, 20))
print(find_split_position(linea, 0, 20))
print(find_split_position(linea, 0, 10))