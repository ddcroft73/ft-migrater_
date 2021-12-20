
""" toolTips.py
gives a Tkinter widget a tooltip as the mouse is above the widget
tested with Python27 and Python34  by  vegaseat  09sep2014
www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter
Modified to include a delay time by Victor Zaccardo, 25mar16

Modified to include realtime contents by DCroft @HobblinCobbler 22Nov2021
"""
import tkinter as tk

class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 220   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.__enter)
        self.widget.bind("<Leave>", self.__leave)
        self.widget.bind("<ButtonPress>", self.__leave)
        self.id = None
        self.tw = None

    def __enter(self, event=None):
        self.__schedule()

    def __leave(self, event=None):
        self.__unschedule()
        self.__hidetip()

    def __schedule(self):
        self.__unschedule()
        self.id = self.widget.after(self.waittime, self.__showtip)

    def __unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def __showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def __hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()