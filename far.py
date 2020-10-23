#!/usr/bin/env python3
# file: far.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2018-02-27T23:38:17+0100
# Last modified: 2019-07-25T21:59:05+0200

from tkinter import filedialog
from tkinter import ttk
from tkinter.font import nametofont
import argparse
import os
import shutil
import sys
import tkinter as tk

__version__ = "2019.07.25"


class FarUI(tk.Tk):
    def __init__(self, rootdir="", findname="", replacement=""):
        tk.Tk.__init__(self, None)
        self.running = False
        self.finditer = None
        self.create_window()
        self.tree["text"] = rootdir
        self.find.insert(0, findname)
        self.replace["text"] = replacement

    def create_window(self):
        """Create the GUI"""
        # Set the font.
        default_font = nametofont("TkDefaultFont")
        default_font.configure(size=12)
        self.option_add("*Font", default_font)
        # General commands and bindings
        self.bind_all("q", self.quit_cb)
        self.wm_title("Find and Replace v" + __version__)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(4, weight=1)
        # First row
        ftxt = ttk.Label(self, text="Find:")
        ftxt.grid(row=0, column=0, sticky="w")
        fe = ttk.Entry(self, justify="left")
        fe.grid(row=0, column=1, columnspan=4, sticky="ew")
        self.find = fe
        # Second row
        treetxt = ttk.Label(self, text="In tree:")
        treetxt.grid(row=1, column=0, sticky="w")
        te = ttk.Label(self, justify="left")
        te.grid(row=1, column=1, columnspan=4, sticky="ew")
        tb = ttk.Button(self, text="browse...", command=self.tree_cb)
        tb.grid(row=1, column=5, columnspan=2, sticky="ew")
        self.tree = te
        # Third row
        reptxt = ttk.Label(self, text="Replace with:")
        reptxt.grid(row=2, column=0, sticky="w")
        re = ttk.Label(self, justify="left")
        re.grid(row=2, column=1, columnspan=4, sticky="ew")
        rb = ttk.Button(self, text="browse...", command=self.replace_cb)
        rb.grid(row=2, column=5, columnspan=2, sticky="ew")
        self.replace = re
        # Fourth row
        run = ttk.Button(self, text="run", command=self.start_replace_cb)
        run.grid(row=3, column=0, sticky="ew")
        stop = ttk.Button(
            self, text="stop", command=self.stop_replace_cb, state=tk.DISABLED
        )
        stop.grid(row=3, column=1, sticky="w")
        self.runbutton = run
        self.stopbutton = stop
        qb = ttk.Button(self, text="quit", command=self.destroy)
        qb.grid(row=3, column=2, sticky="w")
        ttk.Label(self, justify="left", text="Progress: ").grid(
            row=3, column=3, sticky="w"
        )
        progress = ttk.Label(self, justify="left", text="None")
        progress.grid(row=3, column=4, columnspan=2, sticky="ew")
        self.progress = progress
        # Fifth row
        message = tk.Text(self, height=4)
        message.grid(row=4, column=0, columnspan=6, sticky="nsew")
        s = ttk.Scrollbar(self, command=message.yview)
        s.grid(row=4, column=6, sticky="nse")
        message["yscrollcommand"] = s.set
        self.message = message

    def quit_cb(self, event):
        """
        Callback to handle quitting.

        This is necessary since the quit method does not take arguments.
        """
        self.running = False
        self.destroy()

    def tree_cb(self):
        rootdir = filedialog.askdirectory(
            parent=self, title="Directory where to start looking", mustexist=True
        )
        self.tree["text"] = rootdir

    def replace_cb(self):
        replacement = filedialog.askopenfilename(parent=self, title="Replacement file")
        self.replace["text"] = replacement

    def start_replace_cb(self):
        rootdir = self.tree["text"]
        filename = self.find.get()
        replacement = self.replace["text"]
        if self.running or not rootdir or not filename or not replacement:
            self.message.delete("1.0", tk.END)
            self.message.insert(tk.END, "Missing data!")
            return
        self.running = True
        self.message.delete("1.0", tk.END)
        self.message.insert(tk.END, "Starting replacement\n")
        self.runbutton["state"] = tk.DISABLED
        self.stopbutton["state"] = tk.NORMAL
        self.finditer = os.walk(rootdir)
        self.after(1, self.replace_step)

    def replace_step(self):
        if not self.running:
            return
        try:
            path, _, files = self.finditer.send(None)
            rootlen = len(self.tree["text"]) + 1
            # Skip known revision control systems directories.
            for skip in (".git", ".hg", ".svn", ".cvs", ".rcs"):
                if skip in path:
                    self.progress["text"] = "skipping " + path[rootlen:]
                    return
            if len(path) > rootlen and path[rootlen] != ".":
                self.progress["text"] = "processing " + path[rootlen:]
                filename = self.find.get()
                if filename in files:
                    original = path + os.sep + filename
                    replacement = self.replace["text"]
                    repfile = os.path.basename(replacement)
                    dest = path + os.sep + repfile
                    self.message.insert(tk.END, "Removing '{}'\n".format(original))
                    os.remove(original)
                    self.message.insert(
                        tk.END, "Copying '{}' to '{}'\n".format(replacement, dest)
                    )
                    shutil.copy2(replacement, dest)
            self.after(1, self.replace_step)
        except StopIteration:
            self.stop()
            self.message.insert(tk.END, "Finished replacement.\n")

    def stop(self):
        self.running = False
        self.finditer = None
        self.runbutton["state"] = tk.NORMAL
        self.stopbutton["state"] = tk.DISABLED
        self.progress["text"] = "None"

    def stop_replace_cb(self):
        self.stop()
        self.message.insert(tk.END, "Replacement stopped by user.\n")


def main():
    """Main entry point for far.py"""
    # Parse the arguments.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-d",
        "--rootdir",
        type=str,
        default=os.getcwd(),
        help="Directory to start looking in.",
    )
    parser.add_argument(
        "-f", "--findname", type=str, default="", help="Name of the file to find."
    )
    parser.add_argument(
        "-r",
        "--replacement",
        type=str,
        default="",
        help="Path of the replacement file.",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args(sys.argv[1:])
    if not args.rootdir.startswith(os.sep):
        args.rootdir = os.getcwd() + os.sep + args.rootdir
    # Create the UI.
    root = FarUI(args.rootdir, args.findname, args.replacement)
    root.mainloop()


if __name__ == "__main__":
    # Detach from the terminal on POSIX systems.
    if os.name == "posix":
        if os.fork():
            sys.exit()
    # Run the program.
    main()
