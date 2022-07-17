import re
COURSE_PATTERN = re.compile(r".*\(((\d{4}-|Verano)\d{1})\)")


AUTOMATED_FILE = "indexAuto.html"
f = open(AUTOMATED_FILE, "w")


START = True
END = False


EMPTY = "(empty)"
WHATSAPP_LINK = "https://wa.me/19098096441"
TELEGRAM_LINK = "https://t.me/framos1"
EMAIL = "cientifica.silabo@gmail.com"
UPDATED = "15/12/21"
FILE = "automated.html"
MISSION = "Esta pagina NO tiene fines de lucro. El objetivo es reunir los silabos en un sitio f    acilmente acessible para utilizarlos en planificar nuestro estudio, tener una idea de lo que vienen los siguientes ciclos y poder repasar durante las vacaciones. Eventualmente queremos tener todas las carreras profesionales." 



# Helpermethod to write line plus have a next line char
def writeLine(content):
	f.write(content + "\n")

def completeTag(tag: str, content: str, cssSelectors={}):
	return tagStr(tag, True, cssSelectors) + content + tagStr(tag, False)


# Helper method for printing the tag:
# NAME is the name of the tag e.g. div, h1, center, etc
# START is a boolean that says whether it is a start or end tag
def tagStr(name: str, start: bool, cssSelectors = {}):
	optionalSlash = "" if start else "/"
	selectors = ""
	for sel in cssSelectors:
		selectors += sel + "=\"" + cssSelectors[sel] + "\" "
	return "<" + optionalSlash + name + " " + selectors + ">"


# everything inside HEAD tag: title & link
def head():
	writeLine(tagStr("head", START))
	writeLine(completeTag("title", "Silabos"))

	linkSel = {"rel": "stylesheet", "type": "text/css", "href": "styleA.css"}
	writeLine(tagStr("link", START, linkSel))
	writeLine(tagStr("head", END))


# Title in website
def title():
	writeLine(tagStr("div", START, {"id": "title"}))
	writeLine(tagStr("h1", START))	
	writeLine(completeTag("center", "Universidad Cientifica del Sur"))	
	writeLine(completeTag("center", "(Silabos de Medicina Humana)"))	
	writeLine(tagStr("h1", END))


def createLinkDict(link, additional=None):
	default = {"target":"_blank",
					"rel": "noopener noreferrer", 
					"href": link}
	if additional:
		default.update(additional)

	return default


def contactUnit(service, link, additional):
	writeLine(service + ":") 
	writeTag("span", START, {"class": "contact_info"})
	selectors = createLinkDict(link, additional) 
	writeLine(completeTag("a", service, selectors))	
	writeTag("span", END)


def insertLineBreak():
	f.write(tagStr("br", END))	


def classSel(className):
	return {"class": className}	


def contactInfo():
	writeTag("div", START, {"class": "preamble"})		

	contactUnit("Whatsapp", WHATSAPP_LINK, classSel("whatsappinfo"))
	insertLineBreak()	
	contactUnit("Telegram", TELEGRAM_LINK, classSel("telegraminfo"))
	insertLineBreak()	
	writeLine("Correo: ")
	writeLine(completeTag("span", EMAIL, classSel("email"))) 
	insertLineBreak()	
	writeLine(completeTag("span", 
				"Ultima actualizaci&oacute;n: " + UPDATED, classSel("last_updated"))) 
	writeTag("div", END)


def writeTag(name, start, selectors={}):
	writeLine(tagStr(name, start, selectors)) 


def pageMission():
	insertLineBreak()
	f.write(MISSION)


def courseUpdate(label, mssg):
	writeTag("i", START)
	writeLine(completeTag("b", label))
	f.write(mssg)
	writeTag("i", END)
	insertLineBreak()	
	

def generateAnnouncements():
	# Read the announcement file
	announcementFile = open("announcements.txt")
	announcements = announcementFile.readlines()
	announcementFile.close()
	announcements = [x.strip() for x in announcements if x != "\n"]
	#TODO: put a test that announcements has to be divisible by 4
	

	# Build each announcement
	firstAnnouncement = True #Only first one has this
	for i in range(0, int(len(announcements)/4)):		
		writeTag("p", START)
		if firstAnnouncement:
			writeLine("Actualizaciones")
			firstAnnouncement = False		
		writeLine(completeTag("span", announcements[4*i], classSel("post"))) #0th pos is date
		writeLine(completeTag("span", announcements[4*i + 1])) #1st pos is Salute 
		insertLineBreak()
		if announcements[4*i+2] != EMPTY:	
			courseUpdate("Nuevos: ", announcements[4*i+2]) #2nd pos is nuevos
		if announcements[4*i+3] != EMPTY:	
			courseUpdate("Actualizado: ", announcements[4*i+3]) #3rd pos is actualizados
		writeTag("p", END)


def announcements():
	writeTag("div", START, {"class": "announcements", "style": "max-height: 30em;  overflow-y: scroll;"})
	writeTag("ul", START, classSel("list-group"))
	writeTag("li", START, classSel("list-group-item"))
	
	generateAnnouncements()

	writeTag("li", END)
	writeTag("ul", END)
	writeTag("div", END)


def parseCourseString(c):
	res = COURSE_PATTERN.match(c)	
	print(res)
	print(res.groups())


# iterates a list of lists with each element being a semester
# e.g. Course X
# 	- class a (2020-1)
# 	- class b (2021-2)
# 	- class c (2022-1) 
# and produces each semester HTML
def generateSemesters(semesters):
	# This code creates the HTML for each semester
	for i in range(0, len(semesters)):
		writeTag("div", START, classSel("semester"))
		writeLine(completeTag("h2", semesters[i].pop(0)))
		writeTag("ul", START)
		for c in semesters[i]: # Iterat through each course
			#(name, year) = parseCourseString(c) 
			parseCourseString(c) 
			writeTag("li", START)
			writeLine(c)
			selectors = createLinkDict("LINK GOES HERE")  #TODO implement drive links
			writeTag("a", START, selectors)
			writeLine("YEAR GOES HERE") #TODO: finish this, regex prob #TODO: maybe a completeTag
			writeTag("a", END) 
			writeTag("li", END)	
		writeTag("ul", END)
		writeTag("div", END)

def semesters():
	semesterFile = open("semesters.txt")
	rawSemesters = semesterFile.readlines()
	semesterFile.close()

	# Parse it into the correct containers for easy iteration and HTML generation
	semesters = [] # List of lists to hold each semester
	sem = [] # placeholder
	for s in rawSemesters:
		if s == "\n":
			semesters.append(sem.copy())
			sem.clear()
		else:
			sem.append(s)
	if len(sem) > 0:
		semesters.append(sem) # Edge case

	generateSemesters(semesters)


def mainDiv():
	writeLine(tagStr("div", START, {"id": "main"}))
	contactInfo()			
	pageMission()
	announcements()
	semesters()
	writeLine(tagStr("div", END)) 


# Main core of HTML
def body():
	writeLine(tagStr("body", START))		

	# Here the core is written	
	title()
	writeLine(tagStr("div", START, {"class": "container"}))
	
	mainDiv()

	writeLine(tagStr("div", END)) 
	writeLine(tagStr("div", END)) 
	writeLine(tagStr("body", END))		


def preamble():
	writeLine("<?xml version=\"1.0\" encoding=\"utf-8\"?>")


def main():
	# File is opened at beginning in globals 
	preamble()
		
	# Start the HTML tag
	writeLine(tagStr("html", START))
	head()	

	body()


	# END the HTML tag
	writeLine(tagStr("html", END))



	# CLose the file
	f.close()
	


if __name__ == "__main__":
	main()
