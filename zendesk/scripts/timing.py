import atexit
import timeit

from colorama import init
from colorama import Fore

init()

# Prints the amount of time the program takes.
def endlog():
    end = timeit.default_timer()
    elapsed = end - start
    print (Fore.MAGENTA + "Elapsed time: " + seconds_to_string(elapsed) + Fore.RESET)


# Convert seconds to a string represntation of the time.
def seconds_to_string(t):
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])

start = timeit.default_timer()
atexit.register(endlog)