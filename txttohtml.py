import os

#Returns dictionary with all the titles, bodies, tags, and entry numbers
def allentries():
	title = []
	body = []
	tags = []
	entry = []
	for each in os.listdir("entries"):
		currentfile = open("entries/" + each, "r")
		line = currentfile.readline()
		while line != "":
			if line.rstrip() == "TITLE:":
				line = currentfile.readline()
				title = title + [line.rstrip()]
			elif line.rstrip() == "TAGS:":
				line = currentfile.readline()
				tags = tags + [line.rstrip().split()]
			if line.rstrip() == "ENTRY:":
				line = currentfile.readline()
				entry = entry + [int(line.rstrip())]
			elif line.rstrip() == "BODY:":
				current_body = ""
				while line != "TITLE:\n" and line != "TAGS:\n" and line != '':
					line = currentfile.readline()
					if line == "\n":
						current_body= current_body + "<br>"
					else:
						current_body = current_body + line.decode('utf-8').rstrip() + "<br>"
				body = body + [current_body]
			line = currentfile.readline()
	currentfile.close()
	dictionary = {"titles": title, "bodies": body, "tags": tags, "entries": entry}

	#bubble sort algorithm, making sure entry position corresponds to array position
	temp = ""
	i = 0
	count = 0
	while count < len(dictionary["entries"]):
		i = 0
		while i < len(dictionary["entries"]) - 1:
			if dictionary["entries"][i] > dictionary["entries"][i + 1]:
				temp = dictionary["entries"][i]
				dictionary["entries"][i] = dictionary["entries"][i+1]
				dictionary["entries"][i+1] = temp

				#same logic for titles
				temp = dictionary["titles"][i]
				dictionary["titles"][i] = dictionary["titles"][i+1]
				dictionary["titles"][i+1] = temp
				#tags
				temp = dictionary["tags"][i]
				dictionary["tags"][i] = dictionary["tags"][i+1]
				dictionary["tags"][i+1] = temp
				#bodies
				temp = dictionary["bodies"][i]
				dictionary["bodies"][i] = dictionary["bodies"][i+1]
				dictionary["bodies"][i+1] = temp
			i += 1
		count += 1


	return dictionary



#def specified_tag:

#def specified_entry:
				