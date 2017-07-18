import requests
import json
import os
import shutil
from config import *
import re
import sys
import datetime

def run(folder):
  #current dir, sub dirs, files
  current, dirs, files = os.walk(folder).next()
  for file in files:
    #if file is movie format
    if(file.endswith(FORMATS)):
      #if SE returns it is TV Episode
      SE = findSxxExx(file)
      if(SE != None and os.stat(folder+'/'+file).st_size > MIN_TV_SIZE):
        handleTV(file, current, SE)
      #if the file size is bigger than given constant
      elif(os.stat(folder+'/'+file).st_size > MIN_MOVIE_SIZE):
        handleMovie(file, current)
  #call recursively through directories
  for subdir in dirs:
    run(folder+'/'+subdir)

def findSxxExx(file):
  a = re.compile('S..E..', re.IGNORECASE)
  answer = a.search(file)

  if(answer == None):
    a = re.compile('\dx\d\d', re.IGNORECASE)
    answer = a.search(file)
  #returns None if search unsuccessful
  return answer

def handleTV(file, path, SE):
  print("TV - "+file)
  try:
    pathandtitle = genTVFileName(file, SE)
    try:
      if(not TESTING):
        os.makedirs(pathandtitle[0])
    except:
      pass
    finally:
      if(TESTING):
        print("     from"+path+'/'+file) 
        print("     to"+pathandtitle[0]+pathandtitle[1])
        # shutil.copy(IN_FOLDER+file, pathandtitle[0]+pathandtitle[1])
      else:
        shutil.move(path+'/'+file, pathandtitle[0]+pathandtitle[1])
  except Exception as e:
    errorlog(e, path+file)

def genTVFileName(filename, SE):
  group = SE.group()
  season = group[1:3]
  episode = group[4:]

  extension = os.path.splitext(filename)[1]

  title = filename[:SE.start()]
  title = title.replace('.', ' ').rstrip()

  requrl = "http://www.omdbapi.com/?t="+title.replace(' ', "%20")+"&r=json&Season="+season+"&Episode="+episode
  response = requests.get(requrl)
  movie = json.loads(response.text)
  if(movie["Response"] == "False"):
    raise NameError

  return (TV_FOLDER+title+"/Season "+season+'/', title+' - '+group+' - '+movie["Title"]+extension)

def handleMovie(file, path):
  print("Movie - "+file)
  try:
    name = genMovieFileName(file)
    if(TESTING):
      print("     "+name)
    else:
      shutil.move(path+'/'+file, MOVIE_FOLDER+name)
  except Exception as e:
    errorlog(e, path+file)

def genMovieFileName(filename):
  extension = os.path.splitext(filename)[1]

  yearsearch = re.compile('\d\d\d\d').search(filename)

  title = filename[:yearsearch.start()]
  title = title.replace('.', ' ').rstrip()

  return (title + ' (' + yearsearch.group()+')'+extension)

def errorlog(exception, filename):
  logfile = open(LOG_FILE, "a+")
  logfile.write(datetime.datetime.today().strftime("%m/%d/%y - %H:%M:%S -- "))
  logfile.write(str(exception))
  logfile.write("\n   "+filename+'\n')
  logfile.close()

if __name__ == "__main__":

  if(TESTING):
      print("\nWARNING: IN TEST MODE. WILL NOT MOVE FILES")

  if(len(sys.argv) == 2):
    IN_FOLDER = sys.argv[1]
  elif(len(sys.argv) > 2):
    print("\nOnly in directory is able to be set. Please configure directories in config.py")

  if(os.path.exists(IN_FOLDER)):
    print("\nIn    : " + IN_FOLDER)
  else:
    print("directory does not exist : " + IN_FOLDER)
    sys.exit(1)

  print("Movies: " + MOVIE_FOLDER)
  print("TV    : " + TV_FOLDER+'\n')

  run(IN_FOLDER)

