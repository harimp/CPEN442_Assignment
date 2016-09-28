import sys, os

inputfile = "cipher.txt"

ifile = open(inputfile)

cipher = ""

try:
	for line in ifile:
		cipher = line
finally:
	pass

cipherLen = len(cipher)					# cipher length
print(cipherLen)
for scope in range(1,17):
	stat = {} 								# statistical data buffer
	ofile = open("output-" + str(scope) + ".txt", "w+")

	endpoint = cipherLen-scope+1			# last set of [scope] characters to search
	for i in range(endpoint):				# from 0 to end
		current = cipher[i:i+scope]
		if current in stat:
			continue
		for j in range(i, endpoint):		# from i to end
			seek = cipher[j:j+scope]
			if current == seek:
				if seek in stat:
					stat[seek] += 1			# another one found
				else:
					stat[seek] = 1			# add new item to stat

	statkey = sorted(stat, key=stat.get) 	# sort stat by number of occations found
	statkey.reverse() 						# by ascending order
	for key in statkey:
		if stat[key] >= 1:
			ofile.write(str(key) + '\t' + str(stat[key]) + '\n') # write result
	ofile.close()

ifile.close()
