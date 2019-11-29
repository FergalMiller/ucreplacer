##############################################
# Created on 28th November by Fergal Miller. #
##############################################

import sys
import os


def get_user_input_of(reason) -> str:
    user_inp = ""
    while len(user_inp) < 1:
        user_inp = input("Please specify the " + reason + ": ")
    return user_inp


def illegal_characters_in_line(s, illegal_characters) -> set:
    result: set = set()
    for character in illegal_characters:
        if s.__contains__(character):
            result.add(character)
    return result


def get_illegal_characters(illegal_characters_location) -> list:
    illegal_characters = []
    try:
        with open(illegal_characters_location) as illegal_characters_file:
            content = illegal_characters_file.read()
            print("Fetching illegal characters...")
            for c in list(content):
                if not (c == ' ' or c == '\n' or c == ','):
                    illegal_characters.append(c)
    except FileNotFoundError:
        print("Error! Schema could not be found in location", illegal_characters_location)
        illegal_characters = get_illegal_characters(get_user_input_of("location of your illegal characters text file"))
    return illegal_characters


def write_schema_file(schema_location, schema: dict):
    try:
        with open(schema_location, 'w') as schema_file:
            for entry in schema.items():
                schema_file.write(entry[0] + ',' + entry[1] + '\n')
    except FileNotFoundError:
        if input("schema.txt not found. Create new schema file in this directory? (y/n):") == "y":
            open(schema_location, 'x').close()
            write_schema_file(schema_location, schema)


def build_schema(illegal_characters) -> dict:
    schema = {}
    print("Building new schema from illegal characters...")

    with open('temp.txt', 'x') as inp_file:
        inp_file.writelines(illegal_characters)

    os.system("native2ascii -encoding utf8 temp.txt temp.txt")

    with open('temp.txt', 'r') as out_file:
        escaped_chars = out_file.read().split("\\")[1:]

    os.remove("temp.txt")

    index = 0
    while index < len(escaped_chars):
        formatted_escape = "\\" + escaped_chars[index][:5]
        schema[illegal_characters[index]] = formatted_escape
        index += 1

    print("Schema built. Writing to schema text file...")
    write_schema_file(schema_default_location, schema)
    return schema


def get_schema(schema_location) -> dict:
    schema = {}
    try:
        with open(schema_location, 'r') as schema_file:
            lines = schema_file.readlines()
            for line in lines:
                pair = line.strip().split(",")
                if pair[0] in schema:
                    print("Warning: multiple entries in schema for key:", pair[0])
                else:
                    schema[pair[0]] = pair[1]
    except FileNotFoundError:
        print("Error! Schema could not be found in location", schema_location)
        schema = get_schema(get_user_input_of("location of your schema text file"))
    return schema


def replace_illegal_characters_in_target_file(target_file_path, schema):
    property_file = open(target_file_path, "r")
    properties = property_file.readlines()
    index = 0
    for line in properties:
        illegal_characters = illegal_characters_in_line(line, schema.keys())
        for illegalCharacter in illegal_characters:
            line = line.replace(illegalCharacter, schema[illegalCharacter])
        properties[index] = line.__str__()
        index += 1
    property_file = open(target_file_path, "w")
    property_file.writelines(properties)
    property_file.close()


def prepare_schema() -> dict:
    if input("You should build your schema again if you have changed your illegal characters file "
             "since the last build. Would you like to (re)build the schema? (y/n): ") == "y":
        return build_schema(get_illegal_characters(illegal_characters_default_location))
    else:
        return get_schema(schema_default_location)


def bulk(root_search_directory, file_extension):
    schema = prepare_schema()

    for root, dirs, files in os.walk(root_search_directory):
        for file in files:
            if file.endswith(file_extension):
                target_file = os.path.join(root, file)
                print("Replacing illegal characters in", target_file)
                replace_illegal_characters_in_target_file(target_file, schema)


def single(file_path):
    schema = prepare_schema()
    print("Replacing illegal characters in file at path:", file_path)
    replace_illegal_characters_in_target_file(file_path, schema)


def main():
    # First argument: Choose bulk or single
    # Second argument: Target file directory (bulk) or specific file name (single)
    # Third argument: Tile file extension (only applicable to bulk)
    args = sys.argv[1:]
    num_of_args = len(args)
    if num_of_args < 1:
        single(get_user_input_of("file you would like to modify"))
    else:
        if args[0] == "bulk":
            if num_of_args < 2:
                bulk(get_user_input_of("file path you would like to search"),
                     get_user_input_of("file extension"))
            elif num_of_args < 3:
                bulk(args[1], get_user_input_of("file extension"))
            else:
                bulk(args[1], args[2])
        elif args[0] == "single":
            if num_of_args < 2:
                single(get_user_input_of("file you would like to modify"))
            else:
                single(args[1])
        elif ["h", "-h"].__contains__(args[0]):
            print()
        else:
            print("Unrecognised argument:", args[0], "- please specify 'bulk' or 'single' as the first argument")


schema_default_location = "schema.txt"
illegal_characters_default_location = "illegalchars.txt"
main()
