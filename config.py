#configuration settings for movie organizer

TESTING = False
IN_FOLDER = "/Users/augiedoebling/Downloads/"
MOVIE_FOLDER = "/Users/augiedoebling/Media/"
TV_FOLDER = "/Volumes/AugieExt/Media/TV Shows/"
LOG_FILE = "/Users/augiedoebling/Desktop/MovieOrganizeLogs.txt"
MIN_MOVIE_SIZE = 400000000 #400 megabytes
MIN_TV_SIZE = 50000000 #50 megabytes
FORMATS = ("avi", "flv", "m4v", "mkv", "mov", "mp4", "m4v", "mpg", "wmv")
if(TESTING):
   FORMATS = ("avi", "flv", "m4v", "mkv", "mov", "mp4", "m4v", "mpg", "wmv", "utpart")