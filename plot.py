import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
import config
import backend
from scipy.fft import fft, fftfreq
import numpy as np
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk



from matplotlib.figure import Figure

class PlotFrame(tk.Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.f = Figure(figsize=(10, 5), dpi=100, tight_layout=True)
        self.a = self.f.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, columnspan=2)

        self.toolbarFrame = tk.Frame(master=self)
        self.toolbarFrame.grid(row=1, columnspan=2, sticky="w")
        self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)

    def plot(self, progress):
        if config.curr_drawing in ["A", "B", "C", "D", "E"]:
            if config.curr_drawing == "A":
                backend.default_eq(backend.punkt_A, progress)
            elif config.curr_drawing == "B":
                backend.default_eq(backend.punkt_B, progress)
                backend.count_furie()
            elif config.curr_drawing == "C":
                backend.default_eq(backend.punkt_C, progress)
            elif config.curr_drawing == "D":
                backend.default_eq(backend.punkt_D, progress)
            elif config.curr_drawing == "E":
                backend.count_AC_contur(progress)
            self.replot()
        else:
            print("Incorrect current drawing")

    def replot(self):
        self.a.clear()
        self.a.grid()
        if config.curr_drawing == "B":
            if config.type_of_B == 0:
                self.a.plot(config.data["t"], config.data["x"], color='b')
                self.a.set_ylabel("x")
                self.a.set_xlabel("Время")
                self.a.set_title(backend.plot_text(), fontsize=config.plot_fontsize)
            else:
                self.a.plot(config.data["furie_freq"], config.data["furie_ampl"], color='b')
                self.a.set_ylabel("Амплитуда")
                self.a.set_xlabel("Частота")
                self.a.set_title(backend.plot_text(), fontsize=config.plot_fontsize)
        elif config.curr_drawing == "E":
            if config.type_of_print_E == 0:
                self.a.plot(config.data["w"], config.data["w_U"], color='b')
                self.a.set_ylabel("Амплитуда напряжения")
                self.a.set_xlabel("Угловая частота")
                self.a.set_title(backend.plot_text(), fontsize=config.plot_fontsize)
            else:
                self.a.plot(config.data["w"], config.data["w_I"], color='b')
                self.a.set_ylabel("Амплитуда тока")
                self.a.set_xlabel("Угловая частота")
                self.a.set_title(backend.plot_text(), fontsize=config.plot_fontsize)
        else:
            self.a.plot(config.data["t"], config.data["x"], color='b')
            self.a.set_ylabel("x")
            self.a.set_xlabel("Время")
            self.a.set_title(backend.plot_text(), fontsize=config.plot_fontsize)

        self.canvas.draw()
