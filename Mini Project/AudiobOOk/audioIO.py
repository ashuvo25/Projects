
# pdf to audio book using pypdf2 and pyttsx3 tkinter

import pyttsx3 as pt
from PyPDF2 import PdfReader
from tkinter.filedialog import *

books = askopenfilename()
pdf_reader = PdfReader(books)
indx = len(pdf_reader.pages)
# print(indx)
print("Total Pages:", indx)
audi0 = pt.init()
for num in range(0, indx):
        pg = pdf_reader.pages[num]
        strng = pg.extract_text()
        audi0.say(strng)
        audi0.runAndWait()

        while True:
            user_input = input("Press 'p' to pause, 'r' to resume, or 'q' to quit: ").lower()
            if user_input == 'p':
                audi0.stop()
                print("Playback Paused.")
            elif user_input == 'r':
                break 
            elif user_input == 'q':
                audi0.stop()
                exit()







