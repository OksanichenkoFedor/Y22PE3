from tkinter import Tk, W, E, BOTH, ttk, messagebox
import tkinter as tk
from tkinter.ttk import Frame, Button, Entry, Style, Label, Radiobutton
import plot, backend


import config


class PE3_Frame(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Серый ящик на переменном токе")
        #Style().configure("TFrame", background="#333")
        self.pack(fill=BOTH, expand=True)

        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

        self.columnconfigure(2, pad=5)
        self.rowconfigure(2, pad=5)

        self.plotF = plot.PlotFrame(self)
        self.b = blockPE3(self)

        self.plotF.grid(row=0, column=0)
        self.b.grid(row=0, column=1)

        #self.pack()


class blockPE3(Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.print_type = tk.IntVar()
        self.R1 = tk.StringVar()
        self.w_start = tk.StringVar()
        self.w_end = tk.StringVar()
        self.w_step = tk.StringVar()

        self.print_type.set(config.type_of_print_E)

        self.columnconfigure(1, pad=3)
        self.rowconfigure(8, pad=3)

        # подпись
        self.tot_lbl = Label(self, text="Парметры", width=config.label_width_E2)
        self.tot_lbl.grid(row=0, column=0, columnspan=2)
        # поля для параметров
        self.R1_lbl = Label(self, text="R1:", width=config.label_width_E2)
        self.R1_lbl.grid(row=1, column=0)
        self.R1_ent = Entry(self, textvariable=self.R1)
        self.R1.set(config.glob_E_R1)
        self.R1_ent.grid(row=1, column=1)

        self.w_start_lbl = Label(self, text="w(стартовая):", width=config.label_width_E2)
        self.w_start_lbl.grid(row=2, column=0)
        self.w_start_ent = Entry(self, textvariable=self.w_start)
        self.w_start.set(config.start_w)
        self.w_start_ent.grid(row=2, column=1)

        self.w_step_lbl = Label(self, text="Шаг w:", width=config.label_width_E2)
        self.w_step_lbl.grid(row=3, column=0)
        self.w_step_ent = Entry(self, textvariable=self.w_step)
        self.w_step.set(config.step_w)
        self.w_step_ent.grid(row=3, column=1)

        self.w_end_lbl = Label(self, text="w(конечная):", width=config.label_width_E2)
        self.w_end_lbl.grid(row=4, column=0)
        self.w_end_ent = Entry(self, textvariable=self.w_end)
        self.w_end.set(config.end_w)
        self.w_end_ent.grid(row=4, column=1)
        # кнопка для построения
        self.count_but = Button(self, text="Посчитать частотные характеристики", command=self.compile)
        self.count_but.grid(row=5, column=0, columnspan=2)
        # шкала прогресса
        self.progress = ttk.Progressbar(self, orient="horizontal", maximum=config.full_number, mode="determinate")
        self.progress.grid(row=6, column=0, columnspan=2)
        # выбор того, что будем строить на графике
        self.print_U = Radiobutton(self, text="Построить U", value=0, variable=self.print_type, command = self.change_type)
        self.print_U.grid(row=7, column=0)

        self.print_I = Radiobutton(self, text="Построить I", value=1, variable=self.print_type, command = self.change_type)
        self.print_I.grid(row=7, column=1)

    def compile(self):
        config.curr_drawing = "E"
        try:

            config.glob_E_R1 = float(self.R1.get())
            config.start_w = float(self.w_start.get())
            config.step_w = float(self.w_step.get())
            config.end_w = float(self.w_end.get())
            if config.step_w <= 0.0:
                raise Exception("")
            if config.end_w < config.start_w:
                raise Exception("")
            if config.start_w <= 0.0:
                raise Exception("")
            self.master.plotF.plot(self.progress)
        except Exception as e:
            print(e)
            messagebox.showinfo("Error", "Некорректный ввод")

    def change_type(self):
        config.type_of_print_E = self.print_type.get()
        if config.curr_drawing == "E":
            self.master.plotF.replot()

