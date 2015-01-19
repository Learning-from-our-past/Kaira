# -*- coding: utf-8 -*-
from Tkinter import *
from highlightText import CustomText
from dialog import Dialog
from lxml import etree

class Application(Frame):

    objectList = []
    currentPrevious = None
    currentChild = None
    highlightPatternKot = u'Kot|kot'
    highlightPatternPso = u'Pso|pso'
    highlightPatternSot = u'Sotarvo|sotarvo|SOIarvo'
    highlightPatternLapset = u'Lapset|lapset|lapsel|Poika|poika|Tytär|tytär|tylär'
    callback = None



    def createWidgets(self):

        self.pack(fill=BOTH, expand=1)
        self.columnconfigure(1, weight=1, minsize=200)
        self.columnconfigure(3)
        self.columnconfigure(4)

        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, weight=1)

        lbl = Label(self, text="Chunk")
        lbl.grid(sticky=W, pady=4, padx=5)


        self.textareaPrevious = Text(self)
        self.textareaPrevious.config(bg="black", fg="white", insertbackground="white")
        self.textareaPrevious.grid(row=1, column=0, columnspan=2, rowspan=4,
            padx=5, sticky=E+W+S+N)


        self.textarea = CustomText(self)
        self.textarea.tag_configure("kot", background="#ff0000")
        self.textarea.tag_configure("pso", background="#ff99cc")
        self.textarea.tag_configure("sotarvo", background="#4584d3")
        self.textarea.tag_configure("lapset", background="#488627")
        self.textarea.grid(row=5, column=0, columnspan=2, rowspan=4,
            padx=5, sticky=E+W+S+N)


        #LISTBOX
        self.lb = Listbox(self)

        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.config(command=self.lb.yview)
        scrollbar.grid(column=3, row=2, rowspan=3,sticky=N+S)

        self.lb.config(yscrollcommand=scrollbar.set, width=50, selectmode=EXTENDED)
        self.lb.grid(row=2, rowspan=3, column=2,columnspan=1, sticky=N+E+S+W)
        for i in self.objectList:

            self.lb.insert(END, i["child"].text)

        #bind slot
        self.lb.bind("<<ListboxSelect>>", self.onSelect)


        #buttons
        buttonframe = Frame(self)
        #buttonframe.place(x=200,y=300)
        buttonframe.grid(row=5, column=2, padx=5, sticky=N)

        hbtn = Button(buttonframe, text=" Save ", command=self.saveChildModifications)
        hbtn.pack(side=LEFT)
        #hbtn.grid(row=5, column=3, padx=5, sticky=N+E+S)

        obtn = Button(buttonframe, text="Combine", command=self.combineChildren)
        #obtn.grid(row=5, column=2,sticky=N+E+S)
        obtn.pack(side=LEFT)

        nbtn = Button(buttonframe, text="New", command=self.newChild)
        #nbtn.grid(row=5, column=1,sticky=N+E+S)
        nbtn.pack(side=LEFT)

    def newChild(self):
        print "NEW"
        d = Dialog(self.master, "Dialog")
        if len(d.result) > 8:
            child = etree.SubElement(self.xmldocument, "PERSON")
            child.text = d.result
            child.attrib["createdFromEditor"] = "True"

    def saveChildModifications(self):
        #take the child at question:
        self.currentChild["child"].text = self.textarea.get(1.0, END)
        self.currentChild["child"].attrib["checked"] = "True"
        print self.currentChild["child"].text
        #save changes to previous too
        self.currentPrevious.text = self.textareaPrevious.get(1.0, END)


    def combineChildren(self):
        newtxt = self.textareaPrevious.get(1.0, END).strip('\n') + " " + self.textarea.get(1.0, END).strip('\n')
        self.currentChild["child"].text = newtxt
        self.currentChild["child"].attrib["combined"] = "True"
        self.xmldocument.remove(self.currentPrevious)
        print self.currentChild["child"].text


    def onSelect(self, val):

        #set text of this child to textfield
        sender = val.widget         #get sender of the event
        idx = sender.curselection() #get index of selection
        value = self.objectList[idx[0]]["child"].text #sender.get(idx)     #get actual value of selection
        self.currentChild = self.objectList[idx[0]]
        self.textarea.delete(1.0, END)
        self.textarea.insert(INSERT,value)


        self.textarea.highlight_pattern(self.highlightPatternKot, "kot", length=3, regexp=True)
        self.textarea.highlight_pattern(self.highlightPatternPso, "pso", length=3, regexp=True)
        self.textarea.highlight_pattern(self.highlightPatternSot, "sotarvo", length=7, regexp=True)
        self.textarea.highlight_pattern(self.highlightPatternLapset, "lapset", length=6, regexp=True)

        #find previous child's text
        self.currentPrevious = self.currentChild["child"].getprevious()
        print self.currentPrevious.text
        self.textareaPrevious.delete(1.0, END)

        self.textareaPrevious.insert(INSERT,self.currentPrevious.text)


    def __init__(self, objectList, xmldocument, master=None):
        Frame.__init__(self, master)
        self.master.protocol("WM_DELETE_WINDOW", self.closeHandler)
        self.objectList = objectList
        self.xmldocument = xmldocument
        self.parent = master
        self.createWidgets()

    def closeHandler(self):
        print "Sulje combinetool"
        self.master.destroy()
        self.callback()


def startGUI(objectList, xmldocument, callback):
    root = Tk()
    root.geometry("800x800+300+100")
    root.title("Fixtool")
    app = Application(objectList,xmldocument, master=root)
    app.callback = callback
    app.mainloop()
    #root.destroy()