from socket import *
from threading import *
from tkinter import *
from tkinter.ttk import Combobox
import time

count = 1
name = ''
messages = []
menschen = []
names = ['Everyone']
public = [True]

class SEntry(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', font=('Georgia', 13)):
        super().__init__(master)

        self.font = font

        self['font'] = self.font

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
    def reset(self):
        self.delete(0, END)
        self.put_placeholder()
    def change(self, new_placeholder):
        self.new_placeholder = new_placeholder
        self.placeholder = self.new_placeholder
        self.put_placeholder

def connect():
    global network
    global ip
    network = socket(AF_INET, SOCK_STREAM)

    ip = '25.38.47.91'

    port = 1111

    network.connect((ip, port))

def read():
    while True:
        gelen_mesaj = network.recv(100).decode("utf-8")
        if '$' in gelen_mesaj and 'Nano' in gelen_mesaj and 'Line' in gelen_mesaj:
            menschen.append(gelen_mesaj)
            msg = gelen_mesaj[(gelen_mesaj.index('Nano')+4):(gelen_mesaj.index('Line'))]
            if msg == name:
                pass
            else:
                names.append(msg)
            combo['values']=tuple(names)
        elif '$' in gelen_mesaj and 'Nano' in gelen_mesaj and 'Direct' in gelen_mesaj:
            if not public[0]:
                listbox.insert(END, '--Direct--')
            msg = gelen_mesaj[(gelen_mesaj.index('Nano')+4):(gelen_mesaj.index('Direct'))]
            message = msg.split(': ')
            sender = message[0]
            combo.delete(0, END)
            combo.insert(0, sender)
            public[0]=True
        else:
            if public[0]:
                listbox.insert(END, '---Public---')
                public[0]=False
            msg = gelen_mesaj
        listbox.insert(END, msg)

def send_to(a, b):
    global count
    global name
    if combo.get() == 'Everyone' or combo.get() == '':
        if count == 1:
            name = a
            entry.change('Message')
            network.send(bytes(f'$Nano{name}Line$', 'utf-8'))
            count+=1
            b.reset()
        else:
            if a != 'Message':
                b.reset()
                b.focus()
                network.send(bytes('Everyone|'+name+': '+a, "utf-8"))
    else:
        network.send(bytes(combo.get()+'|'+name+': '+a, 'utf-8'))
        entry.reset()
connect()

pencere = Tk()

pencere.geometry('440x550')

pencere.config(bg="darkBlue")

pencere.title('Client')

pencere.resizable(False, False)

frame = Frame(pencere)

listbox = Listbox(frame, font=('Calibri (Body)', 28, 'normal'))

scrollbar = Scrollbar(frame, orient="vertical", command=listbox.yview)

listbox.config(yscrollcommand=scrollbar.set, selectmode=MULTIPLE)

entry = SEntry(pencere, font=('Georgia', 18, 'normal'), placeholder="Name")

button = Button(pencere, text="Send!", font=('Georgia', 18, 'normal'), width=8, command=lambda:send_to(entry.get(), entry))

combo = Combobox(pencere, width=30, font=('Calibri (Body)', 14))

combo['values']=tuple(names)

t1 = Thread(target=read)
t1.start()

#location
frame.pack()
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(side=LEFT)
combo.place(y=440)
entry.place(y=483)
button.place(y=477, x=310)

pencere.mainloop()
