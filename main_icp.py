import oc
import sys
import time

# total arguments
totalArg = len(sys.argv)
if totalArg <= 1:
    print('arg error')
else:
    run = True
    while run is True:
        try:
                oc.run(sys.argv[1])
        except:
                print('error')
                run = True
                time.sleep(5)
