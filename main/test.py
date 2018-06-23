#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import tkinter


class simpleapp_tk(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entry = tkinter.Entry(self)
        self.entry.grid(column=0, row=0, sticky='EW')

        button = tkinter.Button(self, text=u"Click me !")
        button.grid(column=1, row=0)


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('my application')
    app.mainloop()
