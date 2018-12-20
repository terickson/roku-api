# Config Parser code from http://code.activestate.com/recipes/426406-an-easy-to-use-configuration-reader/
#
'''

    EXAMPLE
    c = Configuration('Importador.ini')
    print c.Origem.host, c.Origem.port
    # An extra: print the configuration object itself
    print c
'''
import os
from configparser import SafeConfigParser


class Configuration:
    def __init__(self, fileName):
        if os.path.isfile(fileName):
            cp = SafeConfigParser()
            cp.read(fileName)
            self.__parser = cp
            self.fileName = fileName
        else:
            print('''
                Please create a file called ''' + fileName + ''' in the same directory as this script.
                It should look like:
[<config_section_name>]
<config_option_1>: <config_value_1>
<config_option_2>: <config_value_2>
                ''')
            raise ValueError('file not found', fileName)

    def __getattr__(self, name):
        if name in self.__parser.sections():
            return Section(name, self.__parser)
        else:
            return None

    def __str__(self):
        p = self.__parser
        result = []
        result.append('<Configuration from %s>' % self.fileName)
        for s in p.sections():
            result.append('[%s]' % s)
            for o in p.options(s):
                result.append('%s=%s' % (o, p.get(s, o)))
        return '\n'.join(result)

    def getsections(self):
        p = self.__parser
        return(p.sections())


class Section:
    def __init__(self, name, parser):
        self.name = name
        self.__parser = parser

    def __getattr__(self, name):
        return self.__parser.get(self.name, name)
