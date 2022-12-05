from SentenceExtraction import *
from Keywords import *

import os
from tkinter import *


class UI(SentenceExtraction, Keywords):
    @classmethod
    def create_root(self):
        self.root = Tk()
        self.root.geometry("1000x500+200+100")
        self.root.title("Essay Generator")

    def Labels(self):
        Label(self.root, text='Имеющиеся файлы', font='Calibri 12').grid(row=0, column=0)
        Label(self.root, text='Сгенерированные файлы\nметодом Sentence Extraction', font='Calibri 12').grid(row=0,
                                                                                                            column=2)
        Label(self.root, text='Сгенерированные файлы\nметодом Keywords', font='Calibri 12').grid(row=0, column=3)

    def callback(self, filename):
        os.system(f"{self.full_files_path}{filename}")

    def callback1(self, filename):
        os.system(f"{self.full_SentenceExtraction_path}{filename}")

    def callback2(self, filename):
        os.system(f"{self.full_keywords_path}{filename}")

    def Buttons(self):
        # opening buttons of stock files
        row = 0
        for filename in self.filenames:
            row += 1
            Button(self.root, text=str(filename), command=lambda i=filename: self.callback(i), font='Calibri 12',
                   width=15).grid(row=row, column=0, sticky=W)

        # generate and display files button
        Button(self.root, text='Сгенерировать', font='Calibri 12', command=self.generate).grid(row=1, column=1)

    def generate(self):
        self.get_sentences()
        self.show_generated_sentence_extraction()
        self.get_words()
        self.show_generated_keywords()

    def show_generated_sentence_extraction(self):
        row = 0
        for filename in self.filenames:
            row += 1
            Button(self.root, text=str(filename), command=lambda i=filename: self.callback1(i), font='Calibri 12',
                   width=15).grid(row=row, column=2, sticky=W)

    def show_generated_keywords(self):
        row = 0
        for filename in self.filenames:
            row += 1
            Button(self.root, text=str(filename), command=lambda i=filename: self.callback2(i), font='Calibri 12',
                   width=15).grid(row=row, column=3, sticky=W)

    def run_ui(self):
        self.root.mainloop()
