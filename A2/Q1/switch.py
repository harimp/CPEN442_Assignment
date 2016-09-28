cipherfile = open("cipher.txt")
rulebook = open("switch.rule")
ofile = open("output-switch.txt", "w+")

cipher = ""
for line in cipherfile:
	cipher = line

rules = {}
for line in rulebook:
	rule = list(line.strip().split(' '))
	if len(rule) > 1:
		rules[rule[0]] = rule[1]
	else:
		rules[rule[0]] = rule[0]

cipher = list(cipher)
for i in range(len(cipher)):
	cipher[i] = rules[cipher[i]]
ofile.write("".join(cipher))