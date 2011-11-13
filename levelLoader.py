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

import hashlib, zipfile, os, shutil, time, iniget


def levelList():

  # Map Path
  map_path = "maps/"

  # Get directory List
  mapFiles = os.listdir(map_path)
  mapList = []

  for i in mapFiles:
    loadMap = load(i, [])
    if not loadMap: continue

    mapList.append(i)

  return mapList

def getMapHash(levelFile):
  mapPath = load(levelFile, ['maps'])
  if not mapPath: return None
  return hashlib.sha224(open(mapPath + "maps").read()).hexdigest()    

def load(levelFile, extractFile = None ):

  # Find Map File
  if not os.path.exists(levelFile):

    if os.path.exists("maps/" + levelFile):
      levelFile = "maps/" + levelFile
    else:
      return None

  # Check if Zip or Directory
  isZip = False
  if zipfile.is_zipfile(levelFile):
    isZip = True
  elif not os.path.isdir(levelFile):
    return None

  # If zip, unzip!

  if isZip:
    # Make Temp storage directory
    if os.path.exists("temp"): 
      shutil.rmtree("temp")
      time.sleep(.25)
    os.mkdir("temp")        

    zip_file = zipfile.ZipFile(levelFile)

    if not extractFile:
      zip_file.extractall("temp/")
    else:
      for i in extractFile:
        zip_file.extract(i, "temp/")
          
    zip_file.close()

    levelFile = "temp"

  # Return the path to the level files.
  return levelFile + "/"
