import os
import tkinter
from tkinter import filedialog
from application.pdf.pdf_helper import merge_all

def list_swap(li, a, b):
    """ Swap index a and b within list li"""
    li[a], li[b] = li[b], li[a]


class App(tkinter.Tk):
    def __init__(self, parent, app_dir):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent

        # var declaration
        self.app_dir = app_dir
        self.filenames = []  # tyoe: list[str]
        self.list_files = None  # type: tkinter.Listbox

        # init
        self.initialize()

    def initialize(self):
        # set the app size
        self.geometry("500x500")

        # set up app grid spacing
        self.grid()

        # create filename list
        # TODO should this only show the file name not the whole path?
        self.list_files = tkinter.Listbox(self, width=50)
        self.list_files.grid(column=0, row=0)
        self.insert_temp_list()
        self.update_listbox()

        # create file input button
        button_import = tkinter.Button(self, text='Import', command=self._get_files)
        button_import.grid(column=1, row=0)

        # create file movement button
        button_up = tkinter.Button(self, text='up', command=self._list_move_up)
        button_up.grid(column=1, row=1)
        button_down = tkinter.Button(self, text='Down', command=self._list_move_down)
        button_down.grid(column=2, row=1)

        # create remove button
        button_remove = tkinter.Button(self, text='remove', command=self._list_remove)
        button_remove.grid(column=3, row=1)

        # create merge button
        button_merge = tkinter.Button(self, text='Merge!', command=self._merge)
        button_merge.grid(column=1, row=2)

    def insert_temp_list(self):
        self.filenames = ['cat.pdf', 'dog.pdf', 'meow.pdf']
        self.update_listbox()


    def _get_files(self):
        """ Prompt the user for the files that they wish to merge. All files are added to a list """

        # a list of filetype tuples (filename, extension)
        filetypes = [("pdf files", "*.pdf")]

        # Read in the selected files
        filenames = filedialog.askopenfilenames(
            initialdir=self.app_dir,
            title="Select pdf's to merge. Ctrl + click for multiple",
            filetypes=filetypes
        )

        # add files
        for filename in filenames:
            self.filenames.append(filename)
        self.update_listbox()


    def update_listbox(self):
        """ Redraws the listbox to show self.filenames """
        if len(self.filenames) > 0:
            # delete all items
            self.list_files.delete(0, tkinter.END)

            # add list items. last name only
            for filename in self.filenames:
                self.list_files.insert(tkinter.END, os.path.basename(filename))
        else:
            self.list_files.insert(0, 'None')

    def _list_move_up(self):
        index = self.get_selected_index()
        if (index is not None) and (index != 0):
            up = index - 1
            # swap elements upwards
            list_swap(self.filenames, index, up)
            self.update_listbox()

            # set the cursor position within the list
            self.list_files.activate(up)
            self.list_files.select_set(up)

    def _list_move_down(self):
        index = self.get_selected_index()
        if (index is not None) and (index != len(self.filenames) - 1):
            down = index + 1
            # swap elements downwards
            list_swap(self.filenames, index, down)
            self.update_listbox()

            # set the cursor position within the list
            self.list_files.activate(down)
            self.list_files.select_set(down)

    def _list_remove(self):
        index = self.get_selected_index()
        if index is not None:
            self.filenames.pop(index)
            self.update_listbox()

    def get_selected_index(self):
        selected = self.list_files.curselection()
        if len(selected) > 0:
            return selected[0]
        return None

    def _merge(self):
        """ Callback for when files all pdf files are ready to be merged """
        # check if any pdfs have been selected
        if len(self.filenames) == 0:
            print('No files have been selected. Nothing that can be done')
            return

        print('going to merge the following')
        print(self.filenames)


        # prompt the user for an output file name
        #TODO add a pop up for the output file name through a pop up file window
        output = os.path.join(self.app_dir, 'output.pdf')

        # Run merge for all the files
        merge_all(self.filenames, output)


