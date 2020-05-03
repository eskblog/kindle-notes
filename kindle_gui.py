import tkinter as tk
from tkinter import filedialog
import vacuum as vac #so we can call methods from vacuum.py



class KindleApp:

    def __init__(self, master):

        #create the frame within which this is all taking place
        frame = tk.Frame(master)
        frame.pack() #this makes the frame visible

        #create widgets
        self.create_widgets(frame)

    def create_widgets(self, frame):

        #place logo image (code from effbot tkinter website)

        from PIL import Image, ImageTk

        image = Image.open("logo.png")
        image = image.resize((300, 150))
        photo = ImageTk.PhotoImage(image)
        logo_label = tk.Label(frame, image=photo)
        logo_label.image = photo  # keep a reference!
        logo_label.pack(side=tk.TOP)

        #CREATE EACH STEP:
        self.create_step1(frame)
        self.create_step2(frame)
        self.create_step3(frame)



        # GAPGAPGAP
        self.gap = tk.Label(frame, justify=tk.LEFT, font=("Helvetica", 16),
                                   text="\n\n")
        self.gap.pack(side=tk.TOP)



        #Export button. We use lambda so that we can pass arguments with the command parameter
        self.export = tk.Button(frame, text="Export", pady = 20,
                          command=self.export_clippings)

                # lambda: vac.clippingsToBookTxtFile(
                #           booktitle=self.booktitle.get(), #pass selected book title
                #           clippingspath=self.clippings_e.get(), #
                #           targetdirectory=self.output_e.get()
                #
                #                   ))

        self.export.pack()


        #STATUS bar for output of text
        self.statustitle = tk.Label(frame, justify=tk.LEFT,
                                    text = "STATUS:", fg="green")
        self.statustitle.pack(side=tk.LEFT)

        self.statustext = tk.StringVar() #this is what is later updated
        self.statuslabel = tk.Label(frame, textvariable=self.statustext,
                                    justify=tk.LEFT, fg="black")
        self.statuslabel.pack(side=tk.LEFT)


    def create_step1(self, frame):
        self.step1 = tk.Label(frame, justify=tk.LEFT, font=("Helvetica", 22),
                              text="\nStep 1:")
        self.step1.pack(side=tk.TOP)

        # ask for the clippings directory
        self.clippings_ask = tk.Label(frame, justify=tk.CENTER, font=("Helvetica", 16),
                                      text="Where are the clippings?\n(If the below file path is correct, skip this step)")
        self.clippings_ask.pack(side=tk.TOP)

        # select clippings file path
        self.open_clip = tk.Button(frame, text="choose clippings file",
                                   fg="blue",
                                   command=self.getClippingsFilePath)
        self.open_clip.pack(side=tk.TOP)

        # enter the clippings directory
        self.clippings_e = tk.Entry(frame, width=40)
        self.clippings_e.pack(side=tk.TOP)
        self.clippings_e.insert(0, "/Volumes/Kindle/documents/My Clippings.txt")

    def create_step2(self, frame):

        # STEP 2:
        self.step2 = tk.Label(frame, justify=tk.LEFT, font=("Helvetica", 22),
                              text="\n\nStep 2:")
        self.step2.pack(side=tk.TOP)

        # ask for the book title
        self.book_ask = tk.Label(frame, justify=tk.LEFT, font=("Helvetica", 16),
                                 text="Which book to import clippings for?")
        self.book_ask.pack(side=tk.TOP)

        # create button for loading book titles:
        self.booktitles = tk.Button(frame, text="load book titles",
                                    command=lambda:
                                    self.loadBookTitles(self.clippings_e.get()))
        self.booktitles.pack()

        #dropdown menu
        self.booktitle = tk.StringVar(frame)  # the VARIABLE gets assigned ot this menu
        self.booktitle.set("Choose Book")  # "Default" value
        self.option = tk.OptionMenu(frame, self.booktitle, "1", "2", "3")
        self.option.pack()

    def create_step3(self, frame):
        # STEP 3:
        self.step3 = tk.Label(frame, justify=tk.LEFT, font=("Helvetica", 22),
                              text="\n\nStep 3:")
        self.step3.pack(side=tk.TOP)

        # ask for the output directory path
        self.output_ask = tk.Label(frame, justify=tk.LEFT, font=("Helvetica", 16),
                                   text="Where to save the .txt file?")
        self.output_ask.pack(side=tk.TOP)

        # select output directory
        self.select_dir = tk.Button(frame, text="choose output directory",
                                    fg="brown",
                                    command=self.getOutputDirectory)
        self.select_dir.pack(side=tk.TOP)

        # enter output directory path
        self.output_e = tk.Entry(frame)
        self.output_e.pack(side=tk.TOP)

    def print_inputs(self):
        """For testing purposes only"""
        print("Input: {} \nBook: {}\nOutput: {}".format(
            self.clippings_e.get(), self.title_e.get(), self.output_e.get()))

    def getClippingsFilePath(self):
        filename = filedialog.askopenfilename()
        self.clippings_e.delete(0, tk.END)
        self.clippings_e.insert(0, filename)

    def loadBookTitles(self, clippingspath):
        """From clippings file, get book titles and update the options menu with those titles"""
        try:
            books_set = vac.setOfBookTitles(clippingspath)


            menu = self.option['menu'] #get drop down menu
            menu.delete(0, 'end') #delete contents

            for title in books_set:
                menu.add_command(label=title,
                        command=lambda x=title: self.setBook(self.booktitle, x))
                            # this makes sure the selected book title is actually CHANGED

            self.option.update_idletasks()
            self.outputtext("Books loaded. Now choose a book", replace=True)
        except: #if can't get books
            self.outputtext("Couldn't get book titles from clippings file!")

    def setBook(self, variable, newvalue):
        """This is used to make sure clicking a book title actually changes the
        selected book title"""
        variable.set(newvalue)
        self.outputtext("Book \'"+newvalue[:10]+"...\' loaded. \nNow choose export destination.",
                        replace=True)

    def outputtext(self, text, replace=False):
        """Modifies StringVar associated with the output label,
        thereby printing text."""
        if replace:
            self.statustext.set(text)
        else:
            self.statustext.set(self.statustext.get() + "\n" + text)
        self.statuslabel.update_idletasks()


    def export_clippings(self):

        vac.clippingsToBookTxtFile(
                    booktitle=self.booktitle.get(),  # pass selected book title
                    clippingspath=self.clippings_e.get(),  #
                    targetdirectory=self.output_e.get()
                )
        self.outputtext("Export done. Check if file is there.", replace=True)




    def getOutputDirectory(self):
        filename = filedialog.askdirectory()
        self.output_e.delete(0, tk.END) #once obtained, replace the entry field with it
        self.output_e.insert(0, filename)



window = tk.Tk()
window.title('Kindle Clippings Importer')

app = KindleApp(window)
window.mainloop()
window.destroy()
