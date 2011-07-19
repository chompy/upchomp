"""
    UpChomp - A momentum game staring Chompy
    Copyright (C) 2011 Nathan Ogden
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from lib import ConfigParser

class iniGet(object):

    def __init__(self, file):
    
        """
        Inits IniGet Object, uses Python ConfigParser.
        
        @param string file - Ini file to load.
        """
    
        self.parser = ConfigParser.RawConfigParser()
        self.file = file
        self.parser.read(file)

    def get(self, group, item):
        
        """
        Attempts to get a group/item.
        
        @param string group - Ini group.
        @param string item - Ini variable.
        @return string - Returns the ini var if available.
        """
    
        try:
            return self.parser.get(group, item)
        except:
            return 0
            
    def set(self, group, item, value):          
    
        """
        Sets a value in the Ini file.
        
        @param string group - Ini group.
        @param string item - Ini variable.
        @param string value - Value to set.
        """
      
        if not self.parser.has_section(group): self.parser.add_section(group)
        self.parser.set(group, item, value)  
        # Writing our configuration file to 'example.cfg'
        with open(self.file, 'wb') as configfile:
            self.parser.write(configfile)         

    def getInt(self, group, item):
    
        """
        Attempts to get a group/item as an int.
        
        @param string group - Ini group.
        @param string item - Ini variable.
        @return int - Returns the ini var if available.
        """
    
        try:
            return self.parser.getint(group, item)
        except:
            return 0

    def getFloat(self, group, item):
    
        """
        Attempts to get a group/item as a float.
        
        @param string group - Ini group.
        @param string item - Ini variable.
        @return float - Returns the ini var if available.
        """
    
        try:
            return self.parser.getfloat(group, item)
        except:
            return 0
            
            
    def getBool(self, group, item):
    
        """
        Attempts to get a group/item as a bool.
        
        @param string group - Ini group.
        @param string item - Ini variable.
        @return bool - Returns the ini var if available.
        """
    
        try:
            return self.parser.getboolean(group, item)
        except:
            return 0
