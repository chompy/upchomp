from lib import ConfigParser

class iniGet(object):

    def __init__(self, file):
        self.parser = ConfigParser.RawConfigParser()
        self.file = file
        self.parser.read(file)

    def get(self, group, item):
        try:
            return self.parser.get(group, item)
        except:
            return 0
            
    def set(self, group, item, value):            
        if not self.parser.has_section(group): self.parser.add_section(group)
        self.parser.set(group, item, value)  
        # Writing our configuration file to 'example.cfg'
        with open(self.file, 'wb') as configfile:
            self.parser.write(configfile)         

    def getInt(self, group, item):
        try:
            return self.parser.getint(group, item)
        except:
            return 0

    def getFloat(self, group, item):
        try:
            return self.parser.getfloat(group, item)
        except:
            return 0
            
            
    def getBool(self, group, item):
        try:
            return self.parser.getboolean(group, item)
        except:
            return 0
