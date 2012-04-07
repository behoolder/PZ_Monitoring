from sys import argv
from sensor import SensorHTTP

if len(argv) < 3 :
    print "Brakujacy parametr podczas uruchomienia!"
    print "%s [port sensora] [adres i port monitora]" % (argv[0])
    exit()

if __name__ == "__main__":
    shttp = SensorHTTP(argv[1], argv[2])
    shttp.start(True)