import datetime
import os
class debug_class():
    debug_activated = True
    def __init__(self, custom_variables={"No variables provided": True}, debug_activated=False, file_name='debug.txt', pretty=False):

        self.debug_activated = debug_activated
        if isinstance(self.debug_activated, str):
            self.debug_activated = bool(self.debug_activated)
        self.pretty = pretty
        self.file_name = file_name
        self.indent_number = 0
        self.tab = self.get_number_of_tabs_as_string()
        self.debug_variable_dictionary = custom_variables
        if self.debug_activated is True:
            self.print_dictionary()

    def print_dictionary(self):
        #pretty_json = json.dumps(self.debug_variable_dictionary, indent=4)
        #print(pretty_json)
        print("\n")
        for key in self.debug_variable_dictionary:  # Loop through each key in debug_dictionary
            # print(datetime.datetime.now(), key, +' = ', debug_dictionary[key])
            # print(f"{self.tab}{datetime.datetime.now()} {key} = {self.debug_variable_dictionary[key]}")  # Print key name and value

            try:  # Check if key exist, if it does print
                self.debug_variable_dictionary.get(key)
            except KeyError:  # if key doesn't exist print None
                print(f"{self.tab}{datetime.datetime.now()} {key} = None")  # print serialize in pretty format
            else:  # if try works, so key exist, execute code below
                if self.pretty == False:
                    print(
                        f"{self.tab}{datetime.datetime.now()} {key} = {self.debug_variable_dictionary[key]}")  # print json in pretty format
                    self.debug_module_write_a_file(
                        f"{self.tab}{datetime.datetime.now()} {key} = {self.debug_variable_dictionary[key]}\n")
                elif self.pretty == True:
                    print(
                        f"{self.tab}{datetime.datetime.now()} {key} = {self.debug_variable_dictionary[key]}")  # print json in pretty format
                    self.debug_module_write_a_file(
                        f"{self.tab}{datetime.datetime.now()} {key} = {self.debug_variable_dictionary[key]}\n")


    def get_number_of_tabs_as_string(self):
        tab = ""  # Initialize tab variable as empty string
        for index in range(self.indent_number):  # Loop the number of indents and create tab string
            tab += str('\t')  # Add the number of tabs base on the indent
        return tab  # Return the tab string to print


    def debug_module_write_a_file(self, my_string):
        current_path = os.getcwd()
        path = current_path
        #os.chdir(path)
        filename = self.file_name

        with open(filename, 'a+') as f:
            f.write(my_string)