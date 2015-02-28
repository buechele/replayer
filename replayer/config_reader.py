from exceptions import IOError
import os
import re
import ConfigParser

from config_constants import ConfigConstants


class ConfigReader(object):
    def __init__(self, config_file):
        self.config = {}
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
        self.__read_filter(cfgparser, ConfigConstants.FILTER)
        self.config[ConfigConstants.HEADER] = self.__read_dict(cfgparser, 'Header')
        for section in cfgparser.sections():
            if section.startswith('Transform'):
                self.__copy_regex_tuple(cfgparser, section, 'Search', 'Replace', ConfigConstants.TRANSFORM)

    @staticmethod
    def __read_dict(config, section):
        header_dict = {}
        if config.has_section(section):
            for option in config.options(section):
                header_dict[option] = config.get(section, option)
        return header_dict

    def __copy_regex_tuple(self, config, section, arg1, arg2, target):
        if config.has_section(section):
            regex = re.compile(config.get(section, arg1))
            replace = config.get(section, arg2)
            named_tuple = (regex, replace)
            if target in self.config:
                self.config[target].append(named_tuple)
            else:
                self.config[target] = [named_tuple]

    def __read_filter(self, config, section):
        if config.has_section(section):
            cfg = {}
            for option in config.options(section):
                if option == ConfigConstants.FILTERRULE:
                    value = config.get(section, option).strip().lower()
                    self.config[ConfigConstants.FILTERRULE] = not value == 'disallow'
                else:
                    values = config.get(section, option).split(',')
                    cfg[option] = filter(None, map(str.strip, values))
            self.config[section] = cfg

    def __copy_value(self, config, section, option, target, raw=False):
        if config.has_option(section, option):
            self.config[target] = config.get(section, option, raw)

    def merge_dict(self, args):
        for key in args.keys():
            value = args[key]
            if value is not None:
                self.config[key] = args[key]