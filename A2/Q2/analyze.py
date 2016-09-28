import operator

ifile = open("coupled.cipher")
cipher = ifile.readline().strip().split(' ')
ifile.close()

k = 3
d = {}
for i in range(len(cipher) - k):
	word = "".join(cipher[i:i+k])
	if word in d:
		d[word] += 1
	else:
		d[word] = 0

sorted_dict = sorted(d.items(), key=operator.itemgetter(1))
sorted_dict.reverse()
ofile = open("output.txt", "w+")
for item in sorted_dict:
	ofile.write(item[0])
	ofile.write('\t')
	ofile.write(str(item[1]))
	ofile.write('\n')
