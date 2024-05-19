import datetime
import sys
import os
import pickle
import configparser
class utility_class:
    def __init__(self):
        pass
    #   Set option to print full numpy matrix
    @classmethod
    def utility_save_list_of_objects_to_file(cls, inputs):
        ri = {
            "list_of_objects_full_path_file_name": None,
            "object_list": [],
        }
        ri.update(inputs)
        # Let's assume you have a list of objects you want to save
        my_objects = ri['object_list']  # Replace these with your actual objects

        # Specify your filename
        filename = ri['full_path_file_name']

        # Open a file in binary write mode and use pickle to dump the list of objects
        try:
            if filename is None:
                raise ValueError("Filename cannot be None.")
            with open(filename, 'wb') as file:
                pickle.dump(my_objects, file)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    @classmethod
    def utility_load_list_of_objects_from_file(cls, inputs):
        ri = {
            "list_of_objects_full_path_file_name": None,
        }
        ri.update(inputs)

        # Specify your filename (must be the same as the one used for saving)
        filename = ri['full_path_file_name']

        try:
            with open(filename, 'rb') as file:
                loaded_objects = pickle.load(file)
                print('Successfully loaded objects:')
                print(loaded_objects)
        except EOFError:
            # File exists but is empty
            print('File is empty, returning an empty list.')
            loaded_objects = []  # Return an empty list if the file is empty
        except FileNotFoundError:
            # Handle case where file does not exist
            print('File not found, returning an empty list.')
            loaded_objects = []
        except Exception as e:
            # Handle other potential exceptions
            print(f'An error occurred: {e}')
            loaded_objects = []

        return loaded_objects
    @classmethod
    def load_file_as_string(cls, inputs):
        # required inputs for load_file_as_string
        # ri = {
        #     "full_path_file_name": None,
        # }
        # ri.update(inputs)
        ri = {
            "full_path_file_name": None,
        }
        ri.update(inputs)
        file_path = ri['full_path_file_name']
        try:
            with open(file_path, 'r') as file:
                file_contents = file.read()
            return file_contents
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
        except PermissionError:
            print(f"Error: Permission denied while trying to read file '{file_path}'.")
            return None
        except Exception as e:
            print(f"Error: An unexpected error occurred while reading file '{file_path}': {e}")
            return None
    # text_to_save = "Hello, world!"
    # file_path = 'path/to/your/file.txt'
    # save_text_to_file(text_to_save, file_path)
    @classmethod
    def save_text_to_file(cls, inputs):
        # required inputs for load_file_as_string
        # ri = {
        #     "full_path_file_name": None,
        # }
        # ri.update(inputs)
        ri = {
            "full_path_file_name": None,
            "text": None
        }
        ri.update(inputs)
        file_path = ri['full_path_file_name']
        text = ri['full_path_file_name']
        try:
            with open(file_path, 'w') as file:
                file.write(text)
            print(f"Text successfully saved to '{file_path}'.")
        except Exception as e:
            print(f"Error: An unexpected error occurred while saving text to '{file_path}': {e}")

    # Example usage (commented out for reference)
    # text_to_save = "Hello, world!"
    # file_path = 'path/to/your/file.txt'
    # save_text_to_file(text_to_save, file_path)

    @classmethod
    def save_configuration_file(cls, inputs):
        # Required inputs for save_configuration_file()
        # ri = {
        #     "configuration_full_path_file_name": None,
        #     "configuration_dictionary": None,
        # }
        ri = {
            "configuration_full_path_file_name": None,
            "configuration_dictionary": None,
        }
        ri.update(inputs)
        config_dict = ri['configuration_dictionary']
        file_path = ri['configuration_full_path_file_name']
        config = configparser.ConfigParser()
        config.read_dict(config_dict)
        with open(file_path, 'w') as config_file:
            config.write(config_file)
        print(f"Configuration saved to '{file_path}'")

    # Example configuration dictionary
    config_dict = {
        'Section1': {
            'key1': 'value1',
            'key2': 'value2'
        },
        'Section2': {
            'key3': 'value3'
        }
    }

    # # Example file path
    # file_path = 'config.ini'
    #
    # # Save configuration to INI file
    # save_config(config_dict, file_path)

    @classmethod
    def load_configuration_file(cls, inputs):
        # required inputs for load_configuration_file
        # ri = {
        #     "configuration_full_path_file_name": None,
        # }
        ri = {
            "configuration_full_path_file_name": None,
        }
        ri.update(inputs)
        file_path = ri['configuration_full_path_file_name']
        config = configparser.ConfigParser()
        config.read(file_path)
        config_dict = {section: dict(config.items(section)) for section in config.sections()}
        return config_dict

        # # Load configuration from INI file
        # loaded_config_dict = load_config(file_path)
        # print("Loaded configuration:")
        # print(loaded_config_dict)

class defaultdict_class(dict): # Defaults to none when access keys don't exist, int and floats are defaulted to 0 if they don't exist
    def __missing__(self, key):
        return 0 if isinstance(self.default_factory(), (int, float)) else None

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            return self.default_factory()

    def _parse_numeric(self, value):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return None

    def __add__(self, other):
        result = DefaultDict()
        for key in set(self) | set(other):
            self_value = self.get(key, 0)
            other_value = other.get(key, 0)

            self_numeric = self._parse_numeric(self_value)
            other_numeric = self._parse_numeric(other_value)

            if self_numeric is not None and other_numeric is not None:
                result[key] = self_numeric + other_numeric
            else:
                result[key] = self_value + other_value
        return result

    # # Example usage
    # my_dict = DefaultDict()
    #
    # # Adding values to non-existing keys
    # my_dict['a'] += 5
    # my_dict['b'] += "10.5"  # String containing a number
    #
    # print(my_dict)  # Output: {'a': 5, 'b': 10.5}
    #
    # # Performing addition with another DefaultDict
    # other_dict = DefaultDict()
    # other_dict['a'] += "2"  # String containing a number
    # other_dict['c'] += 7
    #
    # result = my_dict + other_dict
    # print(result)  # Output: {'a': 7, 'b': 10.5, 'c': 7}
