from sys import argv
from catalog import CatalogHTTP

if len(argv) < 2:
    print "Brakujacy parametr podczas uruchomienia!"
    print "%s [port]"%(argv[0],)
    exit()

if __name__ == "__main__":
    ch = CatalogHTTP(int(argv[1]))
    ch.start()
