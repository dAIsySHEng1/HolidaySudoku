try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from splashScreen import *
from helpScreen import *
from playScreen import *
from mouseOnly import *
from standard import *
from keyOnly import *

##################################
# main
##################################

def main():
    runAppWithScreens(initialScreen='splashScreen', width = 800, height = 600)

main()