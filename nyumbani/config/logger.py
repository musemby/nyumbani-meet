import logging

from django.conf import settings

# instantiate the root (parent) logger object (this is what gets called
# to create log messages)
root_logger = logging.getLogger()
# remove the default StreamHandler which isn't formatted well
root_logger.handlers = []
# set the lowest-severity log message to be included by the root_logger (this
# doesn't need to be set for each of the handlers that are added to the
# root_logger later because handlers inherit the logging level of their parent
# if their level is left unspecified. The root logger uses WARNING by default
root_logger.setLevel(logging.INFO)

# create the file_handler, which controls log messages which will be written
# to a log file (the default write mode is append)
file_handler = logging.FileHandler('/var/log/vert.log')
# create the console_handler (which enables log messages to be sent to stdout)
console_handler = logging.StreamHandler()

# create the formatter, which controls the format of the log messages
# I like this format which includes the following information:
# 2022-04-01 14:03:03,446 - script_name.py - function_name - Line: 461 - INFO - Log message.
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - Line: %(lineno)d - %(levelname)s - %(message)s')
# add the formatter to the handlers so they get formatted as desired
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# set the severity level of the console_hander to ERROR so that only messages
# of severity ERROR or higher are printed to the console
console_handler.setLevel(logging.ERROR)

# add the handlers to the root_logger
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)
