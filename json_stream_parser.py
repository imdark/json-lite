from __future__ import absolute_import, unicode_literals

from cStringIO import StringIO

def escape_quate(input_buffer, curr_char, quate, string_builder):
    while curr_char != '' and curr_char == '\\':
        next_char = input_buffer.read(1)
        if next_char == quate:
            string_builder.write(quate)
        else:
            string_builder.write('\\' + next_char)
        curr_char = input_buffer.read(1)

    return curr_char, string_builder

def read_string(input_buffer, curr_char):
    # assums the first charachter is a ' or a "
    starting_quate = curr_char
    string_builder = StringIO()
    curr_char = input_buffer.read(1)

    while curr_char != '' and curr_char != starting_quate:
        curr_char, string_builder = escape_quate(input_buffer, curr_char, starting_quate, string_builder)
        if curr_char is not None and curr_char != starting_quate:
            string_builder.write(curr_char)
            curr_char = input_buffer.read(1)

    curr_char = input_buffer.read(1)
    return curr_char, string_builder.getvalue() 

def skip_whitespace(input_buffer, curr_char):
    while curr_char is not None and curr_char == ' ':
        curr_char = input_buffer.read(1) 

    return curr_char


def read_dictionery(input_buffer):
    curr_dict = {}
    curr_char = input_buffer.read(1) # assums the first charachter is the '{'
    while curr_char != '' and curr_char != '}':
        curr_char = skip_whitespace(input_buffer, curr_char)
        curr_char, key = read_string(input_buffer, curr_char)
        curr_char = skip_whitespace(input_buffer, curr_char)
        curr_char = input_buffer.read(1) # skip the ':'
        curr_char = skip_whitespace(input_buffer, curr_char)
        curr_char, obj = read_obj(input_buffer, curr_char)
        curr_dict[key] = obj
        #curr_index = skip_whitespace(input_buffer, curr_index)
        if curr_char == ',':
            curr_char = input_buffer.read(1)
    curr_char = input_buffer.read(1)
    return curr_char, curr_dict

def read_array(input_buffer):
    curr_array = []
    curr_char = input_buffer.read(1) # assums the first charachter is the '{'

    while curr_char != '' and curr_char != ']':
        curr_char = skip_whitespace(input_buffer, curr_char)
        curr_char, obj = read_obj(input_buffer, curr_char)
        curr_array.append(obj)
        curr_char = skip_whitespace(input_buffer, curr_char)
        if curr_char == ',':
            curr_char = input_buffer.read(1)
    curr_char = input_buffer.read(1)
    return curr_char, curr_array

def load(input_buffer):
    start_char = input_buffer.read(1)
    _, obj = read_obj(input_buffer, start_char)
    return obj

def read_obj(input_buffer, start_char):
    if start_char == 'n':
        return input_buffer.read(5) , None
    elif start_char == '\'' or start_char == '"':
        return read_string(input_buffer, start_char)
    elif start_char == '{':
        return read_dictionery(input_buffer)
    elif start_char == '[':
        return read_array(input_buffer)
    else:
        raise Exception('Parse exception', start_char, input_buffer)
