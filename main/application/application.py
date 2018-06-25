import os
import tkinter
from tkinter import Frame, Label, filedialog, Listbox
from application.pdf.pdf_helper import merge_all

def list_swap(li, a, b):
    """ Swap index a and b within list li"""
    li[a], li[b] = li[b], li[a]

WIDTH = 250
HEIGHT = 250


class App(tkinter.Tk):
    def __init__(self, parent, app_dir):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent

        # var declaration
        self.app_dir = app_dir
        self.filenames = []  # tyoe: list[str]
        self.file_list = None  # type: tkinter.Listbox
        self.output = os.path.join(app_dir, 'output.pdf')  # type: str

        # init
        self.initialize()

    def initialize(self):
        # set the app size
        self.geometry("{}x{}".format(WIDTH, HEIGHT))

        # create frames
        left_frame = Frame(self, bg='cyan', width=WIDTH//2, height=HEIGHT, pady=3)
        right_frame = Frame(self, bg='lavender', width=WIDTH//2, height=HEIGHT, pady=3)

        # layout all main containers with some scale
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # stick frames to positions (side by side)
        left_frame.grid(row=0, column=0, sticky='nsew')
        right_frame.grid(row=0, column=1, sticky='nsew')

        # create widgets
        label_pdf = Label(left_frame, text='PDFs')
        self.file_list = Listbox(left_frame)

        label_cmds = Label(right_frame, text='Commands')
        button_import = tkinter.Button(right_frame, text='Import', command=self._get_files)
        button_up = tkinter.Button(right_frame, text='up', command=self._list_move_up)
        button_down = tkinter.Button(right_frame, text='Down', command=self._list_move_down)
        button_remove = tkinter.Button(right_frame, text='remove', command=self._list_remove)
        button_merge = tkinter.Button(right_frame, text='Merge!', command=self._merge)

        # layout widgets
        label_pdf.grid(row=0, column=0)
        self.file_list.grid(row=1, column=0)

        label_cmds.grid(row=0, column=1)
        button_import.grid(row=1, column=1)
        button_up.grid(row=2, column=1)
        button_down.grid(row=3, column=1)
        button_remove.grid(row=4, column=1)
        button_merge.grid(row=5, column=1)

        self.update_listbox()

    def insert_temp_list(self):
        """ Temp list for debugging """
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
        # delete all elements from list
        self.file_list.delete(0, tkinter.END)

        # add list items. last name only
        for filename in self.filenames:
            self.file_list.insert(tkinter.END, os.path.basename(filename))

    def _list_move_up(self):
        """ Move the selected element up if possible """
        index = self.get_selected_index()
        if (index is not None) and (index != 0):
            up = index - 1
            # swap elements upwards
            list_swap(self.filenames, index, up)
            self.update_listbox()

            # set the cursor position within the list
            self.select_line(up)

    def _list_move_down(self):
        """ Move the selected element down if possible """
        index = self.get_selected_index()
        if (index is not None) and (index != len(self.filenames) - 1):
            down = index + 1
            # swap elements downwards
            list_swap(self.filenames, index, down)
            self.update_listbox()

            # set the cursor position within the list
            self.select_line(down)

    def _list_remove(self):
        """
        Remove the selected item
        * if not selected, nothing happens
        * if possible the selection cursor does not move
        * if you are removing the latest element the selection moves back one
        * if you remove the last element, nothing is selected
        """

        index = self.get_selected_index()

        # ensure something is selected
        if index is None:
            return

        # remove element
        self.filenames.pop(index)
        self.update_listbox()

        # work out where the cursor should be
        max_pos = len(self.filenames)

        if index < max_pos:
            self.select_line(index)
        elif max_pos != 0:
            self.select_line(index - 1)

    def select_line(self, index):
        """ select a line within self.file_list if the index makes sense """
        if index < len(self.filenames):
            self.file_list.activate(index)
            self.file_list.select_set(index)

    def get_selected_index(self):
        """
        Return the index of the element selected in self.file_list.
        None if nothing is selected
        """
        selected = self.file_list.curselection()
        if len(selected) > 0:
            return selected[0]
        return None

    def _merge(self):
        """ Callback for when files all pdf files are ready to be merged """
        # check if any pdfs have been selected
        if len(self.filenames) == 0:
            print('No files have been selected. Nothing that can be done')
            return

        # prompt the user for the output file name
        self.set_output_file_name()

        # Run merge for all the files
        merge_all(self.filenames, self.output)


    def set_output_file_name(self):
        """ Prompts the user to select the output file name """
        # a list of filetype tuples (filename, extension)
        filetypes = [("pdf files", "*.pdf")]

        # Read in the user desired file location
        output = filedialog.asksaveasfilename(
            initialdir=self.app_dir,
            title="Output merged",
            filetypes=filetypes
        )

        # check if the extension is actually pdf (fix shorthanding)
        self.output = output if output.endswith('pdf') else (output + '.pdf')


