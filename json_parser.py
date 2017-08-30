from __future__ import absolute_import, unicode_literals

from cStringIO import StringIO

def escape_quate(input_buffer, start_index, quate, string_builder):
    curr_index = start_index
    while input_buffer[curr_index] == '\\' and input_buffer[curr_index+1] == quate:
        string_builder.write(quate)
        curr_index += 2

    return curr_index, string_builder

def read_string(input_buffer, start_index):
    # assums the first charachter is a ' or a "
    starting_quate = input_buffer[start_index]
    string_builder = StringIO()
    curr_index = start_index + 1
    len_input = len(input_buffer)

    while curr_index < len_input and input_buffer[curr_index] != starting_quate:
        curr_index, string_builder = escape_quate(input_buffer, curr_index, starting_quate, string_builder)
        if curr_index < len_input and input_buffer[curr_index] != starting_quate:
            string_builder.write(input_buffer[curr_index])
            curr_index += 1

    end_index = curr_index + 1
    return end_index, string_builder.getvalue() 

def skip_whitespace(input_buffer, start_index):
    curr_index = start_index 
    len_input = len(input_buffer)

    while curr_index < len_input and input_buffer[curr_index] == ' ':
        curr_index += 1

    return curr_index


def read_dictionery(input_buffer, start_index):
    curr_dict = {}
    curr_index = start_index + 1 # assums the first charachter is the '{'
    len_input = len(input_buffer)

    while curr_index < len_input and input_buffer[curr_index] != '}':
        curr_index = skip_whitespace(input_buffer, curr_index)
        curr_index, key = read_string(input_buffer, curr_index)
        curr_index = skip_whitespace(input_buffer, curr_index)
        curr_index += 1 # skip the ':'
        curr_index = skip_whitespace(input_buffer, curr_index)
        curr_index, obj = read_obj(input_buffer, curr_index)
        curr_dict[key] = obj
        #curr_index = skip_whitespace(input_buffer, curr_index)
        if input_buffer[curr_index] == ',':
            curr_index += 1
    end_index = curr_index + 1
    return end_index, curr_dict

def read_array(input_buffer, start_index):
    curr_array = []
    curr_index = start_index + 1 # assums the first charachter is the '{'
    len_input = len(input_buffer)

    while curr_index < len_input and input_buffer[curr_index] != ']':
        curr_index = skip_whitespace(input_buffer, curr_index)
        curr_index, obj = read_obj(input_buffer, curr_index)
        curr_array.append(obj)
        curr_index = skip_whitespace(input_buffer, curr_index)
        if input_buffer[curr_index] == ',':
            curr_index += 1
    end_index = curr_index + 1
    return end_index, curr_array

def read_obj(input_buffer, start_index):
    if input_buffer[start_index:start_index+4] == 'null':
        return start_index + 5, None
    elif input_buffer[start_index] == '\'' or input_buffer[start_index] == '"':
        return read_string(input_buffer, start_index)
    elif input_buffer[start_index] == '{':
        return read_dictionery(input_buffer, start_index)
    elif input_buffer[start_index] == '[':
        return read_array(input_buffer, start_index)
    else:
        raise Exception('Parse exception', input_buffer[start_index], start_index, input_buffer)
