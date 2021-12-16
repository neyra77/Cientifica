AUTOMATED_FILE = "indexAuto.html"
START = True
END = False

WHATSAPP_LINK = "https://wa.me/19098096441"
TELEGRAM_LINK = "https://t.me/framos1"


# Helpermethod to write line plus have a next line char
def writeLine(f, content):
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
def head(f):
	writeLine(f, tagStr("head", START))
	writeLine(f, completeTag("title", "Silabos"))

	linkSel = {"rel": "stylesheet", "type": "text/css", "href": "styleA.css"}
	writeLine(f, tagStr("link", START, linkSel))
	writeLine(f, tagStr("head", END))


# Title in website
def title(f):
	writeLine(f, tagStr("div", START, {"id": "title"}))
	writeLine(f, tagStr("h1", START))	
	writeLine(f, completeTag("center", "Universidad Cientifica del Sur"))	
	writeLine(f, completeTag("center", "(Silabos de Medicina Humana)"))	
	writeLine(f, tagStr("h1", END))


def createLinkDict(link, additional=None):
	default = {"target":"_blank",
					"rel": "noopener noreferrer", 
					"href": link}
	if additional:
		default.update(additional)

	return default


def contactUnit(f, service, link, additional):
	writeLine(f, service + ":") 
	writeTag(f, "span", START, {"class": "contact_info"})
	selectors = createLinkDict(link, additional) 
	writeLine(f, completeTag("a", service, selectors))	
	writeTag(f, "span", END)


	


def contactInfo(f):
	writeTag(f, "div", START, {"class": "preamble"})		

	contactUnit(f, "Whatsapp", WHATSAPP_LINK, {"class":"whatsappinfo"})
	contactUnit(f, "Telegram", TELEGRAM_LINK, {"class":"telegraminfo"})

	writeTag(f, "div", END)


def writeTag(f, name, start, selectors={}):
	writeLine(f, tagStr(name, start, selectors)) 


def mainDiv(f):
	writeLine(f, tagStr("div", START, {"id": "main"}))
	contactInfo(f)			



	writeLine(f, tagStr("div", END)) 


# Main core of HTML
def body(f):
	writeLine(f, tagStr("body", START))		

	# Here the core is written	
	title(f)
	writeLine(f, tagStr("div", START, {"class": "container"}))
	
	mainDiv(f)

	writeLine(f, tagStr("div", END)) 
	writeLine(f, tagStr("div", END)) 
	writeLine(f, tagStr("body", END))		


def preamble(f):
	writeLine(f, "<?xml version=\"1.0\" encoding=\"utf-8\"?>")


def main():
	# Open the file
	f = open(AUTOMATED_FILE, "w")
	preamble(f)
		
	# Start the HTML tag
	writeLine(f, tagStr("html", START))
	head(f)	

	body(f)


	# END the HTML tag
	writeLine(f, tagStr("html", END))



	# CLose the file
	f.close()
	


if __name__ == "__main__":
	main()
