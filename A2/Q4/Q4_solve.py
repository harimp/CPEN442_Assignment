from random import randrange
from zlib import crc32
from datetime import datetime
from itertools import product
import sys, math

def randomString(n, charset):
        result = ""
        for i in range(n):
                result += charset[randrange(len(charset))]
        return result

def main():
        tstart = datetime.now()
        charset = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        x = "31065121" # my student number
        xcrc = crc32(x.encode('UTF-8'))

        counter = 0
        start = "AAA"
        perm = product(charset, repeat = 6)
        for y in perm:
                y = "".join(y)
                ycrc = crc32(y.encode('UTF-8'))
                if ycrc == xcrc and x != y:
                        tend = datetime.now()
                        delta = tend - tstart
                        print("Collision confirmed:")
                        print("\t",x,":",xcrc)
                        print("\t",y,":",ycrc)
                        print("Took:", str(delta.seconds) + "." + str(delta.microseconds), "s")
                        print("Calculated", counter, "values.")
                        break
                else:
                        counter += 1
                        if (y[0:3] != start):
                                start = y[0:3]
                                print(counter, y, 100 * float(counter) / math.pow(2,32),'%')

if __name__ == '__main__':
        main()
