from sys import argv
from monitor import MonitorHTTP

if len(argv) < 3:
    print "Brakujacy parametr podczas uruchomienia!"
    print "%s [port] [adres:port]"%(argv[0],)
    print "Pierwszy parametr oznacza port na ktorym ma zostac uruchomiony monitor"
    print "Drugim parametrem jest adres i port katalogu"
    exit()

if __name__ == "__main__":
    mh = MonitorHTTP(int(argv[1]), argv[2])
    mh.start()
