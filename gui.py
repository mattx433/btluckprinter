import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from luckprinter import D11sPrinter
import escpos.printer

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.connected = False
        self.dummy = escpos.printer.Dummy(profile="default")
        self.pack()
        self.gridframe = ttk.Frame(self, padding=10)
        self.gridframe.grid()
        ttk.Label(self.gridframe, text="Port").grid(column=0, row=0)
        self.connvar = tk.StringVar()
        if os.name == "nt":
            self.connvar.set("COM7")
        else:
            self.connvar.set("/dev/rfcomm0")
        self.conntext = tk.StringVar()
        self.conntext.set("Connect")
        self.connentry = ttk.Entry(self.gridframe, textvariable=self.connvar).grid(column=1, row=0)
        self.connbtn = ttk.Button(self.gridframe, textvariable=self.conntext, command=self.connect).grid(column=2, row=0)
        ttk.Label(self.gridframe, text="File").grid(column=0, row=1)
        self.filevar = tk.StringVar()
        self.filevar.set("test.png")
        self.fileentry = ttk.Entry(self.gridframe, textvariable=self.filevar).grid(column=1, row=1)
        self.filebtn = ttk.Button(self.gridframe, text="Browse", command=self.browse).grid(column=2, row=1)
        self.batvar = tk.StringVar()
        self.batvar.set("??%")
        ttk.Label(self.gridframe, textvariable=self.batvar).grid(column=0, row=2)
        self.feedbtn = ttk.Button(self.gridframe, text="Feed", command=self.feed).grid(column=1, row=2)
        self.printbtn = ttk.Button(self.gridframe, text="Print", command=self.print).grid(column=2, row=2)
    def connect(self):
        if not self.connected:
            self.printer = D11sPrinter(self.connvar.get())
            self.printer.open()
            self.batvar.set(f"{self.printer.get_battery()}%")
            self.conntext.set("Disconnect")
        else:
            self.printer.close()
            self.batvar.set("??%")
            self.conntext.set("Connect")
        self.connected = not self.connected
    def browse(self):
        fn = askopenfilename()
        if fn:
            self.filevar.set(fn)
    def feed(self):
        if self.connected:
            if not self.printer.get_paper():
                showerror("Error", "No paper")
                return
            self.printer.feed_label()
    def print(self):
        if self.connected:
            if not self.printer.get_paper():
                showerror("Error", "No paper")
                return
            self.printer.set_density()
            self.printer.set_label_paper()
            self.printer.enable_printer()
            self.dummy.clear()
            self.dummy.image(self.filevar.get())
            self.printer.device.write(self.dummy.output)
            self.printer.finish()
            self.printer.device.flush()

root = tk.Tk()
root.title("Label Printer")
app = App(root)
app.mainloop()