from exceptions import IOError
import os
import re
import ConfigParser

from config_constants import ConfigConstants


class ConfigReader(object):
    def __init__(self, config_file):
        self.__config = {}
        if config_file is not None:
            if os.path.isfile(config_file):
                self.__read_config_file(config_file)
            else:
                raise IOError('File ' + config_file + ' not found')

    def __read_config_file(self, config_file):
        cfgparser = ConfigParser.SafeConfigParser()
        cfgparser.optionxform = str
        cfgparser.read(config_file)
        self.__copy_value(cfgparser, 'General', 'LogFormat', ConfigConstants.LOGFORMAT, True)
        self.__copy_value(cfgparser, 'General', 'Host', ConfigConstants.HOST)
        self.__copy_filter(cfgparser, 'Allow', 'Status', ConfigConstants.STATUS)
        self.__copy_filter(cfgparser, 'Allow', 'Methods', ConfigConstants.METHODS)
        self.__copy_tuple(cfgparser, 'Header', ConfigConstants.HEADER)
        for section in cfgparser.sections():
            if section.startswith('Transform'):
                self.__copy_regex_tuple(cfgparser, section, 'Search', 'Replace', ConfigConstants.TRANSFORM)

    def __copy_tuple(self, config, section, target):
        if config.has_section(section):
            for option in config.options(section):
                free_tuple = (option, config.get(section, option))
                if target in self.__config:
                    self.__config[target].append(free_tuple)
                else:
                    self.__config[target] = [free_tuple]

    def __copy_regex_tuple(self, config, section, arg1, arg2, target):
        if config.has_section(section):
            regex = re.compile(config.get(section, arg1))
            replace = config.get(section, arg2)
            named_tuple = (regex, replace)
            if target in self.__config:
                self.__config[target].append(named_tuple)
            else:
                self.__config[target] = [named_tuple]

    def __copy_filter(self, config, section, option, target):
        if config.has_option(section, option):
            value = config.get(section, option)
            self.__config[target] = value.split(",")

    def __copy_value(self, config, section, option, target, raw=False):
        if config.has_option(section, option):
            self.__config[target] = config.get(section, option, raw)

    def merge_dict(self, args):
        for key in args.keys():
            value = args[key]
            if value is not None:
                self.__config[key] = args[key]

    def get_config(self):
        return self.__config