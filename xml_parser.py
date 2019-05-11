import re


class XMLKeywords(object):
    def __init__(self):
        self.object = "<object>"
        self.object_end = "</object>"
        self.obj_name = "<obj_name>"
        self.field = "<field>"
        self.field_end = "</field>"
        self.name = "<name>"
        self.type = "<type>"
        self.value = "<value>"


class XMLObject(object):
    def __init__(self):
        self.obj_name = None
        self.fields = []

    def __str__(self):
        return "Object {}".format(self.obj_name)


class XMLField(object):
    def __init__(self):
        self.name = None
        self.type = None
        self.value = None

    def __str__(self):
        return "Field: {0}, type: {1}, value: {2}".format(self.name, self.type, self.value)


class XMLParser(object):
    def __init__(self):
        self.objects = []

    def parse(self, input_file):
        with open(input_file) as xml_input:
            keywords = XMLKeywords()
            obj_ref = None
            field_ref = None
            for line in xml_input:
                parsed_line = self.parse_line(line, keywords)
                if parsed_line['keyword'] == keywords.object:
                    obj_ref = XMLObject()
                elif parsed_line['keyword'] == keywords.object_end:
                    if self.validate_object(obj_ref):
                        self.objects.append(obj_ref)
                        obj_ref = None
                elif parsed_line['keyword'] == keywords.obj_name:
                    obj_ref.obj_name = parsed_line['argument']
                elif parsed_line['keyword'] == keywords.field:
                    field_ref = XMLField()
                elif parsed_line['keyword'] == keywords.field_end:
                    if self.validate_field(field_ref):
                        obj_ref.fields.append(field_ref)
                        field_ref = None
                elif parsed_line['keyword'] == keywords.name:
                    field_ref.name = parsed_line['argument']
                elif parsed_line['keyword'] == keywords.type:
                    if self.validate_field_type(parsed_line['argument']):
                        field_ref.type = parsed_line['argument']
                elif parsed_line['keyword'] == keywords.value:
                    field_ref.value = parsed_line['argument']
                else:
                    pass
        for obj in self.objects:
            print(obj)
            for fields in obj.fields:
                print(fields)

    def validate_field_type(self, f_type):
        return f_type == "int" or f_type == "string"

    def validate_field(self, xml_field):
        return xml_field.name is not None and xml_field.type is not None and xml_field.value is not None

    def validate_object(self, xml_object):
        return xml_object.obj_name is not None and xml_object.fields

    def parse_line(self, line, keywords):
        line = line.strip()
        line_keyword = None
        for keyword in vars(keywords).values():
            if re.match(keyword, line):
                line_keyword = keyword
        result = {'keyword': line_keyword}
        if line_keyword == keywords.obj_name:
            line = re.sub('</obj_name>$', '', line)
            obj_name = re.sub('^<obj_name>', '', line)
            result.update({'argument': obj_name})
            return result
        elif line_keyword == keywords.name:
            line = re.sub('</name>$', '', line)
            name = re.sub('^<name>', '', line)
            result.update({'argument': name})
            return result
        elif line_keyword == keywords.type:
            line = re.sub('</type>$', '', line)
            _type = re.sub('^<type>', '', line)
            result.update({'argument': _type})
            return result
        elif line_keyword == keywords.value:
            line = re.sub('</value>$', '', line)
            val = re.sub('^<value>', '', line)
            result.update({'argument': val})
            return result
        else:
            return result








