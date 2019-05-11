import sys
import os

sys.path.append(os.path.abspath("./source"))
from json_converter import *


def main():
    parser = XMLParser()
    objects = parser.parse(input_file="input.xml")
    converter = JSONConverter()
    converter.convert_to_json(objects)


if __name__ == "__main__":
    main()
