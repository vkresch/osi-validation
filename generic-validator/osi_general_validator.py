#!/usr/bin/env python3

# Standard library Imports
import argparse
import sys
import os
from collections import namedtuple
import logging

# Local packages imports
try:
    import osi3.osi_sensordata_pb2
    import osi3.osi_sensorview_pb2
except ModuleNotFoundError:
    print('The program encountered problems while importing OSI. Check your system for required dependencies. ')

# Private imports
from osi_validation_rules import OSIValidationRules
from osi_validator_logger import OSIValidatorLogger
from osi_id_manager import OSIIDManager
from osi_data_container import OSIDataContainer

# Free Functions
def command_line_arguments():
    """ Define and handle command line interface """
    parser = argparse.ArgumentParser(
        description='Validate data defined at the input with the table of requirements/')
    parser.add_argument('--rules', '-r',
                        help='Directory with text files containig rules for validator. ',
                        type=str,
                        required=True)
    parser.add_argument('--data', '-d',
                        help='Path to the file with OSI-serialized data.',
                        type=str,
                        required=True)
    parser.add_argument('--type', '-t',
                        help='Name of the message type used to serialize the data.',
                        choices=['SensorView', 'GroundTruth', 'SensorData'],
                        default='SensorView',
                        type=str,
                        required=False)
    parser.add_argument('--output', '-o',
                        help='Output folder of the log files.',
                        default='.',
                        type=str,
                        required=False)
    parser.add_argument('--debug',
                        help='Set the debug mode to ON.',
                        action="store_true")

    # Handle comand line arguments
    return parser.parse_args()


def main():
    # Handling of command line arguments
    arguments = command_line_arguments()

    # Instanciate Logger
    print("Instanciate logger")
    directory = arguments.output
    if not os.path.exists(directory):
        os.makedirs(directory)
    logger = OSIValidatorLogger(arguments.debug, directory)

    # Read the data
    logger.info("Read the data")
    odc = OSIDataContainer()
    odc.from_file(arguments.data, arguments.type)

    # Instanciate ID Manager
    id_manager = OSIIDManager(logger)

    # Collect Validation Rules 
    logger.info("Collect validation rules")
    ovr = OSIValidationRules(logger, id_manager)
    ovr.from_yaml_directory(arguments.rules)

    # Pass the timesteps
    logger.info("Pass the timesteps")
    for i in range(0, len(odc.data)):
        id_manager.reset()
        logger.info(f"Checking the timestep {i}")
        sv = odc.data[i]
        fake_field_descriptor = namedtuple('fake_field_descriptor',['name']) 
        fake_field_descriptor.name = arguments.type

        # Check common rules
        ovr.check_message([(fake_field_descriptor, sv)], ovr._rules[arguments.type])
        
        # Resolve ID and references
        id_manager.resolve_unicity()
        id_manager.resolve_references()

    # Grab major OSI version

if __name__ == "__main__":
    main()