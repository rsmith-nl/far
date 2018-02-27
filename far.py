#!/usr/bin/env python3
# file: far.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-02-27 23:38:17 +0100
# Last modified: 2018-02-28 00:03:56 +0100
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to far.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

import tkinter as tk
from tkinter import ttk
from tkinter.font import nametofont
import os
import sys

__version__ = '0.1'


class FarUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self, None)
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
        self.resizable(False, False)
        # First row
        ftxt = ttk.Label(self, text='Find:')
        ftxt.grid(row=0, column=0, sticky='w')
        fe = ttk.Entry(self, justify='left')
        fe.grid(row=0, column=1, sticky='ew')
        self.find = fe
        # Second row
        treetxt = ttk.Label(self, text='In tree:')
        treetxt.grid(row=1, column=0, sticky='w')
        te = ttk.Entry(self, justify='left')
        te.grid(row=1, column=1, sticky='ew')
        tb = ttk.Button(self, text="browse...")
        tb.grid(row=1, column=2, sticky='ew')
        self.tree = te
        # Third row
        reptxt = ttk.Label(self, text='Replace with:')
        reptxt.grid(row=2, column=0, sticky='w')
        re = ttk.Entry(self, justify='left')
        re.grid(row=2, column=1, sticky='ew')
        rb = ttk.Button(self, text="browse...")
        rb.grid(row=2, column=2, sticky='ew')
        self.replace = re
        # Fourth row
        run = ttk.Button(self, text="run", command=self.on_run)
        run.grid(row=3, column=0, sticky='w')
        qb = ttk.Button(self, text="quit", command=self.destroy)
        qb.grid(row=3, column=1, sticky='w')

    def quit_cb(self, event):
        """
        Callback to handle quitting.

        This is necessary since the quit method does not take arguments.
        """
        self.quit()

    def on_run(self):
        pass


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
