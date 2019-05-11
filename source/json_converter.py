from xml_parser import *


def add_to_class(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class JSONConverter:
    @add_to_class(XMLObject)
    def write_to_json(self, file):
        file.write("    \"" + self.obj_name + "\": {\n")
        for index, field in enumerate(self.fields):
            field.write_to_json(file)
            if index != len(self.fields) - 1:
                file.write(",\n")
            else:
                file.write("\n")
        file.write("    }")

    @add_to_class(XMLField)
    def write_to_json(self, file):
        file.write("        \"" + self.name + "\": ")
        if self.type == "string":
            file.write("\"" + self.value + "\"")
        else:
            file.write(self.value)

    def convert_to_json(self, object_list):
        with open("output.json", mode='w') as output_file:
            output_file.write("{\n")
            for index, xml_object in enumerate(object_list):
                xml_object.write_to_json(output_file)
                if index != len(object_list) - 1:
                    output_file.write(",\n")
                else:
                    output_file.write("\n")
            output_file.write("}")
