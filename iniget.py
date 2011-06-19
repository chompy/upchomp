from lib import ConfigParser

class iniGet(object):

    def __init__(self, file):
        self.parser = ConfigParser.ConfigParser()
        self.parser.read(file)

    def get(self, group, item):
        try:
            return self.parser.get(group, item)
        except:
            return 0

    def getInt(self, group, item):
        try:
            return self.parser.getint(group, item)
        except:
            return 0

    def getBool(self, group, item):
        try:
            return self.parser.getboolean(group, item)
        except:
            return 0
