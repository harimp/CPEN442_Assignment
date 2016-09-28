import random
import math

def randomKey():
	alpha = list("ABCDEFGHILKMNOPQRSTUVWXYZ")
	key = ""
	while alpha:
		randomI = random.randrange(len(alpha))
		key += alpha[randomI]
		del alpha[randomI]
	return key

def findKeyChar(key, c):
	i = list(key).index(c)
	return [int(i/5), i % 5]

def findKey (key, i, j):
	return key[i * 5 + j]

def decipherCouple(key, couple):
	[x1, x2] = findKeyChar(key, couple[0])
	[y1, y2] = findKeyChar(key, couple[1])
	result = []
	if x1 == y1: # same row
		result.append(findKey(key, x1, (5 + x2 - 1) % 5))
		result.append(findKey(key, y1, (5 + y2 - 1) % 5))
	elif x2 == y2: # same col
		result.append(findKey(key, (5 + x1 - 1) % 5, x2))
		result.append(findKey(key, (5 + y1 - 1) % 5, y2))
	else: # square
		result.append(findKey(key, x1, y2))
		result.append(findKey(key, y1, x2))
	return result

def decipher(key, ciphertext):
	plaintext = ""
	i = 0
	while i < len(ciphertext):
		plaintext += "".join(decipherCouple(key, ciphertext[i:i+2]))
		i += 2
	return plaintext

def analyzeScore(key, ciphertext, quadgram):
	plaintext = decipher(key, ciphertext)
	score = 0.0
	for i in range(len(ciphertext) - 4):
		quad = plaintext[i:i+4]
		if quad in quadgram[0]:
			score += math.log10 (float(quadgram[0][quad])/quadgram[1])
		else:
			score += math.log10 (float(0.01 / quadgram[1]))
	return score

def changeKey(key, swapping, x):
	newKey = ""
	if x == 1: # flip NW to SE
		for i in range(25):
			newKey += key[swapping[0][i]]
	elif x == 2: # flip top down
		for i in range(25):
			newKey += key[swapping[1][i]]
	elif x == 3: # flip left right
		for i in range(25):
			newKey += key[swapping[2][i]]
	elif x == 4: # change two random row
		rand1 = random.randrange(5)
		rand2 = random.randrange(5)
		while rand2 == rand1: # cannot be same number
			rand2 = random.randrange(5)
		for i in range(5):
			if i == rand1:
				newKey += key[rand2*5:rand2*5+5]
			elif i == rand2:
				newKey += key[rand1*5:rand1*5+5]
			else:
				newKey += key[i*5:i*5+5]
	elif x == 5: # change two random col
		rand1 = random.randrange(5)
		rand2 = random.randrange(5)
		while rand2 == rand1: # cannot be same number
			rand2 = random.randrange(5)
		for i in range(5):
			for j in range(5):
				if j == rand1:
					newKey += key[i*5 + rand2]
				elif j == rand2:
					newKey += key[i*5 + rand1]
				else:
					newKey += key[i*5 + j]
	else:
		rand1 = random.randrange(25)
		rand2 = random.randrange(25)
		while rand2 == rand1: # cannot be same number
			rand2 = random.randrange(25)
		newKey = list(key)
		temp = newKey[rand1]
		newKey[rand1] = newKey[rand2]
		newKey[rand2] = temp
		newKey = "".join(newKey)
	return newKey


if __name__ == '__main__':
	# Get ciphertext
	ifile = open("cipher.txt")
	ciphertext = ifile.readline().strip()
	ifile.close()
	print("Ciphertext fetched.")

	# Prepare quadgram dictionary
	ifile = open("english_quadgrams.txt")
	quadgram = [{}, 0]
	totalQuadgram = 0
	for line in ifile:
		line = line.strip().split(' ')
		quadgram[1] += int(line[1])
		quadgram[0][line[0]] = int(line[1])
	print("Quadgrams ready.")

	# find best simplified temperature
	cipherLength = len(ciphertext)
	temperature = 10 + 0.087 * (cipherLength - 84)

	# Prepare swapping preset values
	swapping = []
	swapping.append([24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
	swapping.append([20, 21, 22, 23, 24, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4])
	swapping.append([4, 3, 2, 1, 0, 9, 8, 7, 6, 5, 14, 13, 12, 11, 10, 19, 18, 17, 16, 15, 24, 23, 22, 21, 20])

	# Make random key
	parentKey = randomKey()
	parentScore = analyzeScore(parentKey, ciphertext, quadgram)

	i = 0
	while i < 50000:
		x = random.randrange(1,51) # random number between 1 and 50
		childKey = changeKey(parentKey, swapping, x)

		childScore = analyzeScore(childKey, ciphertext, quadgram)
		dScore = parentScore - childScore
		if dScore < 0:
			parentScore = childScore
			parentKey = childKey
			print(i, parentKey, parentScore)
		else:
			prob = float(1) / math.exp(float(dScore) / float(temperature))
			randomFloat = random.random() # random from 0.0 to 1.0
			if prob > randomFloat:
				parentScore = childScore # accept child
				parentKey = childKey
				print(i, parentKey, parentScore)
			else:
				i += 1

