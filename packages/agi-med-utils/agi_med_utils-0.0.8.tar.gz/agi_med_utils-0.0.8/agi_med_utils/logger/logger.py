import logging
from pythonjsonlogger import jsonlogger
from sys import stdout

from ..config.singleton import singleton
from ..dig_ass.db import make_session_id


class JsonFormatter(jsonlogger.JsonFormatter):
    pass
    ####
    # additional json formatting possible
    ####

    # def add_fields(self, log_record, record, message_dict):
    #     super(JsonFormatter, self).add_fields(log_record, record, message_dict)
    #     if not log_record.get('timestamp'):
    #         log_record['timestamp'] = record.created
    #     if log_record.get('level'):
    #         log_record['level'] = log_record['level'].upper()
    #     else:
    #         log_record['level'] = record.levelname


@singleton
class LoggerSingleton:
    def __init__(self, loggerConfig) -> None:
        self.logger = logging.getLogger(name=loggerConfig['name'])
        self.logger.setLevel(loggerConfig['level_common'])

        logFilePath = f'{loggerConfig["file_dir"]}/{loggerConfig["name"]}_{make_session_id()}.json'
        fileHandler = logging.FileHandler(logFilePath, mode='a')
        jsonFormatter = JsonFormatter(loggerConfig['format_file'])
        fileHandler.setFormatter(jsonFormatter)
        fileHandler.setLevel(loggerConfig['level_file_handler'])

        stdoutHandler = logging.StreamHandler(stdout)
        stdoutHandler.setFormatter(logging.Formatter(loggerConfig['format_stdout']))
        stdoutHandler.setLevel(loggerConfig['level_stdout_handler'])

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(stdoutHandler)

    def get(self):
        return self.logger
