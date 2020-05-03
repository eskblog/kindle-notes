"""how it looks in the file:
==========
Booktitle
- Your Highlight on page 25-25 | Added on Sunday, January 1, 2017 9:24:30 PM

its project is to selfinvest in ways that enhance its value or to attract investors through constant attention to its actual or figurative credit rating, and to do this across every sphere of its existence. 36
==========


How to USE THIS:

python3.7 "Book Title" clippingspath(optional) targetpath(optional) filename_suffix

The Book Title can be part of the book title--the tool will get any book that includes the "Book Title" string in its title, so be as specific as necessary to avoid getting multiple books.



"""

from collections import defaultdict

class KindleNote:

    booktitle = ""
    text = ""
    date = "" #save date as string for simplicity
    kind = ""
    location = 0

    def __init__(self, booktitle, locations, kind, text, date = "n/d"):
        self.booktitle = booktitle
        self.locations = locations #starting and ending locations
        self.kind = kind
        self.date = date
        self.text = text

def notesAsStringsList(filepath):
    """returns a clippings file as a list of strings, one for each entry"""
    with open(filepath, 'r') as f:
        txt = f.read()
        entries = txt.split("==========\n")
    return entries

def getOnlyOneBooksStrings(booktitle, entries):
    book_entries = []
    for entry in entries:
        if len(entry) != 0 and booktitle in entry.splitlines()[0]: #if it's the right book title
            book_entries.append(entry)
    if len(book_entries)==0: #notify if no entries were found
        print("no entries found for book: {}".format(booktitle))
    return book_entries

def getTitle(entrystring):
    """get the title, minus outside whitespaces"""
    return entrystring.splitlines()[0].strip()

def getKind(entrystring):
    """from the relevant line in the entry string, get if it's a "bookmark" "clipping" "highlight" or "comment" """

    line = entrystring.splitlines()[1]

    if "Highlight" in line:
        return "highlight"
    if "Note" in line:
        return "comment"
    if "Bookmark" in line:
        return "bookmark"
    if "Clipping" in line:
        return "clipping"
    else:
        return "unknown kind"

def getLocations(entrystring):
    """from the relevant line in the entry string, get locations, a list of 1 or 2 entries
     There are several options here.
     (a) it just has Location XX-YY, in which case we want [XX, YY]
     (b) it has just Location XX, in which case we want [XX}
     (c) it just has page XX-YY (a pdf, likely), and we just use page as location [XX, YY]
     (d) it just has page XX, so we want [XX]
     (e) it has both page and Location, so likely an "official" book -- we will use locations(s) by above logic"""
    line = entrystring.splitlines()[1]

    #first, we isolate the number(s) as a string:
    numberstring = ""
    if "Location" in line:
        numberstring = line.split("Location")[1].split()[0] #split at word "Location" then get first word after that
    elif "page" in line: #if it doesn't have a Location, we do page
        numberstring = line.split("page")[1].split()[0] #split at word "page" then get first word after that
    else:
        numberstring = "ALERT: no page or location found in entry!"
        print(numberstring)
        return 0 #we return no location. Theoretically this way we can still use the note for something


    #now, we get the numerical values as a list,  either "XX, YY" or "XX".
    locations = numberstring.split("-")#turn it into a list of 1 or 2 locations
    for i in range(len(locations)):
        try:
            locations[i] = int(locations[i]) #turn it into integers
        except: #e.g. when location is a roman-numeral page from intro
            locations[i] = 0 #for now, we don't convert roman numerals but just assign loc 0


    return locations


def getText(entrystring):
    """from the relevant line in the entry string, get the text """
    return entrystring.splitlines()[3]

def locationsExtractor(listofKindleNotes):
    """given a list of kindle notes, extracts their locations (both starting and ending) as a list"""
    loclist = set()
    for note in listofKindleNotes:
        for location in note.locations: #check each note's locations
            loclist.add(location)
    return loclist


def bookToKindleNotes(booktitle, clippingspath):
    """For a given book and clippings file, returns a dictionary of list of KindleNotes, key = locations range as list of 1 or 2 locations"""

    notesdict = defaultdict(list)

    entries_as_strings = getOnlyOneBooksStrings(booktitle, notesAsStringsList(clippingspath))

    for e in entries_as_strings:

        entrylocation = getLocations(e)[-1] #we assume it's going to be the second location, if two members

        #BUT if e is a "comment", we need to check if there's already a highlight or note with its location as either starting or ending point
        if getKind(e) == "comment" and len(notesdict) != 0:
            for location, notes in notesdict.items(): #go through existing dictionary
                if entrylocation in locationsExtractor(notes): #if this comment matches an existing note's range of locations
                    entrylocation = location #then we will just save this comment to that existing note's's dict entry

        notesdict[entrylocation].append(KindleNote(getTitle(e), getLocations(e), getKind(e), getText(e)))

    return notesdict


def clippingsToBookTxtFile(booktitle, clippingspath="/Volumes/Kindle/documents/My Clippings.txt", targetdirectory="output", filenamesuffix=""):
    """Outputs notes from clippingspath for booktitle, to targetdirectory as booktitle.txt. filenamesuffix can help differentiate it from existing txt files with same filename"""
    outputfilename = booktitle+filenamesuffix+".txt"
    outputfile = open(targetdirectory+"/"+outputfilename, "w")
    notesdict = bookToKindleNotes(booktitle, clippingspath)
    outputfile.write(booktitle+ " - NOTES:\n\n")
    for location, notes in sorted(notesdict.items()):
        outputfile.write("Location {}:\n".format(location))
        for note in notes:
            if note.kind == "highlight":
                outputfile.write("\"" + note.text + "\""+"\n")
            elif note.kind == "comment":
                outputfile.write("NOTE: "+ note.text+"\n")
        outputfile.write("\n\n")  # after each location, an empty ßline
    outputfile.close()

def setOfBookTitles(filepath):
    listofstrings = notesAsStringsList(filepath)
    books = set()
    for string in listofstrings:
        try:
            books.add(getTitle(string))
        except:
            pass
    return sorted(books)

