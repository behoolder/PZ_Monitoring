from sys import argv
from monitor import MonitorHTTP

if len(argv) < 2 :
    print "Brakujacy parametr podczas uruchomienia!"
    print "%s [port]"%(argv[0],)
    exit()

if __name__ == "__main__":
    mh = MonitorHTTP(int(argv[1]))
    mh.start()
