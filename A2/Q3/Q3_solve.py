import zlib
from datetime import datetime
from random import randrange

def randomString(n, charset):
	result = ""
	for i in range(n):
		result += charset[randrange(len(charset))]
	return result

def main():
	tstart = datetime.now()
	charset = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
	hashes = {}
	collisionStr = None
	collisionCRC = None

	# Generate random hash and check if CRC already found
	while True:
		newStr = randomString(6, charset)
		newCrc = zlib.crc32(newStr.encode('UTF-8'))
		if newCrc in hashes:
			if newStr == hashes[newCrc]:
				continue
			else:
				collisionStr = [newStr, hashes[newCrc]]
				collisionCRC = newCrc
				break
		else:
			hashes[newCrc] = newStr
			# if len(hashes) % 1000 == 0:
				# print(len(hashes), newStr)

	# Check that collision found is correct.
	if collisionStr != None:
		firstCRC = zlib.crc32(collisionStr[0].encode('UTF-8'))
		secondCRC = zlib.crc32(collisionStr[1].encode('UTF-8'))
		if firstCRC == secondCRC:
			tend = datetime.now()
			delta = tend - tstart
			print("Collision confirmed:")
			print("\t",collisionStr[0],":",firstCRC)
			print("\t",collisionStr[1],":",secondCRC)
			print("Took:", str(delta.seconds) + "." + str(delta.microseconds), "s")
			print("Calculated", len(hashes), "values.")
		else:
			print("Wrong collision. Starting over.")
			main()

if __name__ == '__main__':
	main()