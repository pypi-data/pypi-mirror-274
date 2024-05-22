import json

class Defined_Command():
    def __init__(self):
        self.name = None
        self.description = None
        self.syntax = None
        self.min_args = None
        self.max_args = None
        self.defined_flags = None

class Executed_Command():
    def __init__(self):
        self.name = None
        self.args = []
        self.flags = []
        self.properties = None

class CLI():
    def __init__(self):
        self.defined_commands = []
        self.current_command = None

    def parse_input(self, user_input):
        self.current_command = Executed_Command()
        input_array = user_input.strip().split(" ")
        command_length = len(input_array)

        if command_length == 1:
            if input_array[0] == '':
                raise ValueError("Empty command.")
            
        for iterator, element in enumerate(input_array):
            if iterator == 0:
                self.current_command.properties = self.get_command_properties(element)
    
                if self.current_command.properties == None:
                    raise ValueError("Command not defined")
                
                self.current_command.name = element

            elif "-" in element:
                if element[0] == "-":
                    self.current_command.flags.append(element)

            else:
                self.current_command.args.append(element)

        if self.current_command.properties.max_args is not None:
            if len(self.current_command.args) > self.current_command.properties.max_args:
                raise SyntaxError("Too many arguements")
        
        if self.current_command.properties.min_args is not None:
            if len(self.current_command.args) < self.current_command.properties.min_args:
                raise SyntaxError("Too few arguements")
                
        if self.current_command.properties.defined_flags is not None:
            for flag in self.current_command.flags:
                if flag not in self.current_command.properties.defined_flags:
                    raise SyntaxError("Undefined flag")

    def json_to_lookup(self, path):
        with open(path, "r") as f:
            defined_commands = json.load(f)
            if "commands" not in defined_commands:
                raise SyntaxError('Json file formatted incorrectly. Should be formatted as: \n{ \n\t"commands": [...] \n}')
            
        self.populate_lookup(defined_commands["commands"])
            
    def populate_lookup(self, defined_commands):
        for command in defined_commands:
            if "name" not in command:
                raise SyntaxError('Commands require a specified name. \nSyntax: \n{\n\t"name": <name>,\n\t"description": <description>,\n\t"syntax": <syntax>\n}')
            
            command_struct = Defined_Command()
            
            if "description" in command:
                command_struct.description = command["description"]

            if "syntax" in command:
                command_struct.syntax = command["syntax"]

            if "min_args" in command:
                command_struct.min_args = command["min_args"]

            if "max_args" in command:
                command_struct.max_args = command["max_args"]

            if "defined_args" in command:
                command_struct.defined_args = command["defined_args"]

            if "defined_flags" in command:
                command_struct.defined_flags = command["defined_flags"]

            command_struct.name = command["name"]

            self.defined_commands.append(command_struct)

    def get_command_properties(self, queried_command):
        for defined_command in self.defined_commands:
            if queried_command in defined_command.name:
                return defined_command
        
        return None
    
    def help(self):
        for defined_command in self.defined_commands:
            print(defined_command.name)

            if defined_command.description is not None:
                print(f"  description: {defined_command.description}")

            if defined_command.syntax is not None:
                print(f"  syntax: {defined_command.syntax}")

        