#!/usr/bin/env python3

# Standard library Imports
import argparse
import os
import sys
import copy

# Local packages imports
try:
    import osi3.osi_sensordata_pb2
    import osi3.osi_sensorview_pb2
except ModuleNotFoundError:
    print('The program encoutered problems while importing OSI. Check your system for reqired dependencies. ')

# Private imports
import data_reader


# Classes
class OsiValidationRules:
    """ This class collects validation rules """
    def __init__(self):
        self._rules = dict()

    def from_dictionary(self, dictionary):
        """ Collect validion rules found in the directory. """
        try:
            for filename in os.listdir(dictionary):
                if filename.startswith('osi_') and filename.endswith('.txt'):
                    self.form_file(dictionary, filename)
                    
        except FileNotFoundError:
            print('Error while reading files OSI-rules. Exiting!')

    def form_file(self, dictionary, filename):
        with open(os.path.join(dictionary, filename), 'r') as file:
            for line in file.readlines():

                # Empty line
                if line.strip() == '':
                    continue
                
                # Comment line
                if line.strip().startswith('#'):
                    continue
                
                # Command line
                try:
                    self.parse_line(line)
                except:
                    print('Not a validid line in file. ')
                    print(line)


    def parse_line(self, line):
        field, verb, *parameters = line.strip().split()
        print(f'Field {field} should comply with rule "{verb}" and parameters {parameters}')
        self._rules.setdefault(field,[]).append({'verb':verb, 'params':parameters})

    def get_rules(self):
        return copy.deepcopy(self._rules)

# Free Functions
os
def command_line_arguments():
    """ Define and handle command line interface """
    parser = argparse.ArgumentParser(
                description='Validate data defined at the input with the table of requirements/')
    parser.add_argument('--rules','-r',
            help='Directory with text files containig rules for validator. ',
            type=str,
            required=True)
    parser.add_argument('--data', '-d',
            help='Path to the file with OSI-serialized data.',
            type=str,
            required=True)
    parser.add_argument('--class', '-c',
            help='Name of the class usssed to serialize the data.',
            choices=['SensorView', 'GroundTruth', 'SensorData'],
            default='SensorView',
            type=str,
            required=False)

    # Handle comand line arguments
    return parser.parse_args()

def main():
    # Handling of command line arguments
    arguments = command_line_arguments()

    # Collect Validation Rules
    validation_rules = OsiValidationRules()
    validation_rules.from_dictionary(arguments.rules)

    # Read the data 

    # Pass the first timestamp for check

    # Grab major OSI version


if __name__ == "__main__":
    main()