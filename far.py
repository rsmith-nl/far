#!/usr/bin/env python3
# file: far.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-02-27 23:38:17 +0100
# Last modified: 2018-02-28 21:31:13 +0100
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to far.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.font import nametofont
import os
import shutil
import sys

__version__ = '0.1'


class FarUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self, None)
        self.running = False
        self.finditer = None
        self.rootdir = tk.StringVar()
        self.findname = tk.StringVar()
        self.replacement = tk.StringVar()
        self.create_window()

    def create_window(self):
        """Create the GUI"""
        # Set the font.
        default_font = nametofont("TkDefaultFont")
        default_font.configure(size=12)
        self.option_add("*Font", default_font)
        # General commands and bindings
        self.bind_all('q', self.quit_cb)
        self.wm_title('Find and Replace v' + __version__)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)
        #self.resizable(False, False)
        # First row
        ftxt = ttk.Label(self, text='Find:')
        ftxt.grid(row=0, column=0, sticky='w')
        fe = ttk.Entry(self, justify='left', textvariable=self.findname)
        fe.grid(row=0, column=1, sticky='ew')
        self.find = fe
        # Second row
        treetxt = ttk.Label(self, text='In tree:')
        treetxt.grid(row=1, column=0, sticky='w')
        te = ttk.Entry(self, justify='left', textvariable=self.rootdir, state=tk.DISABLED)
        te.grid(row=1, column=1, sticky='ew')
        tb = ttk.Button(self, text="browse...", command=self.tree_cb)
        tb.grid(row=1, column=2, columnspan=2, sticky='ew')
        self.tree = te
        # Third row
        reptxt = ttk.Label(self, text='Replace with:')
        reptxt.grid(row=2, column=0, sticky='w')
        re = ttk.Entry(self, justify='left', textvariable=self.replacement, state=tk.DISABLED)
        re.grid(row=2, column=1, sticky='ew')
        rb = ttk.Button(self, text="browse...", command=self.replace_cb)
        rb.grid(row=2, column=2, columnspan=2, sticky='ew')
        self.replace = re
        # Fourth row
        run = ttk.Button(self, text="run", command=self.start_replace)
        run.grid(row=3, column=0, sticky='w')
        qb = ttk.Button(self, text="quit", command=self.destroy)
        qb.grid(row=3, column=1, sticky='w')
        self.runbutton = run
        # Fifth row
        message = tk.Text(self, height=4)
        message.grid(row=4, column=0, columnspan=3, sticky='nsew')
        s = ttk.Scrollbar(self, command=message.yview)
        s.grid(row=4, column=3, sticky='nse')
        message['yscrollcommand'] = s.set
        self.message = message

    def quit_cb(self, event):
        """
        Callback to handle quitting.

        This is necessary since the quit method does not take arguments.
        """
        self.running = False
        self.quit()

    def tree_cb(self):
        rootdir = filedialog.askdirectory(
            parent=self,
            title='Directory where to start looking',
            mustexist=True
        )
        self.rootdir.set(rootdir)

    def replace_cb(self):
        replacement = filedialog.askopenfilename(
            parent=self,
            title='Replacement file'
        )
        self.replacement.set(replacement)

    def start_replace(self):
        rootdir = self.rootdir.get()
        filename = self.findname.get()
        replacement = self.replacement.get()
        if self.running or not rootdir or not filename or not replacement:
            self.message.delete('1.0', tk.END)
            self.message.insert(tk.END, 'Missing data!')
            return
        self.running = True
        self.message.delete('1.0', tk.END)
        self.message.insert(tk.END, 'Starting replacement\n')
        self.runbutton['state'] = tk.DISABLED
        self.finditer = os.walk(rootdir)
        self.after(5, self.replace_step)

    def replace_step(self):
        try:
            path, _, files = self.finditer.send(None)
            rootlen = len(self.rootdir.get())+1
            if len(path) > rootlen and path[rootlen] != '.':
                filename = self.findname.get()
                if filename in files:
                    source = self.replacement.get()
                    dest = path + os.sep + filename
                    # shutil.copy2(source, dest)
                    self.message.insert(tk.END, "Replacing '{}' by '{}'\n".format(dest, source))
                # else:
                    # self.message.insert(tk.END, "Nothing found in '{}'.\n".format(path))
            self.after(5, self.replace_step)
        except StopIteration:
            self.running = False
            self.runbutton['state'] = tk.NORMAL
            self.message.insert(tk.END, 'Finished replacement\n')


def main():
    """Main entry point for far.py"""
    root = FarUI()
    root.mainloop()


if __name__ == '__main__':
    # Detach from terminal
    if os.name == 'posix':
        if os.fork():
            sys.exit()
    # Run the program.
    main()
