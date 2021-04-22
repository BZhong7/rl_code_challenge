from intelhex import IntelHex

example_hex = IntelHex()
example_hex.fromfile("example.hex", format="hex")

text_hex = open("hexdump.txt", "w")
example_hex.dump(text_hex)
text_hex.close()
