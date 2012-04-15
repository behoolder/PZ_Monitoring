from sys import argv
from sensor import Sensor

if len(argv) < 3 :
    print "Brakujacy parametr podczas uruchomienia!"
    print "%s [port sensora] [adres i port monitora]" % (argv[0])
    exit()

if __name__ == "__main__":
    s = Sensor(argv[1], argv[2])
    s.start()