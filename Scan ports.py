# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 16:25:12 2023

@author: a.kalachev
"""
import socket
import datetime
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext

###########################################################################################################################
# Список портов для сканирования
def get_ports():
    
    ports = list()
    
    rng=txt_p.get()
    
    if rng=="0" or rng=="":
        ports=[20, 21, 22, 23, 25, 42, 43, 53, 67, 69, 80, 110, 115, 123, 137, 138, 139, 143, 161, 179, 443, 445, 514, 
               515, 993, 995, 1080, 1194, 1433, 1702, 1723, 3128, 3268, 3306, 3389, 5432, 5060, 5900, 5938, 8080, 10000, 20000]
    else:
        for i in range(1, int(rng)+1):
            ports.append(i)
    return ports

###########################################################################################################################

def scan_from_file(list_of_ports):
    
    btn.configure(state=DISABLED)
    
    bar=Progressbar(wnd, length=300, mode='determinate', maximum=len(list_of_ports))
    bar.grid(column=1, row=4)
    
    #Записываем время начала
    time_start=datetime.datetime.now()
    
    with open("Result.txt", "a", encoding="utf-8") as file_d:
        file_d.truncate(0) #Очищаем файл результатов
        file_d.write(f"\nНачало сканирования {str(time_start)}\n")

    txt_out.insert(INSERT, f"\nНачало сканирования {str(time_start)}\n")
    
    #Читаем хосты из файла
    with open("Hosts.txt", "r", encoding="utf-8") as h:
        hosts=h.readlines()
         
    # В цикле перебираем порты из списка
    for host in hosts:
        for port in list_of_ports:
        
            lbl_d.configure(text=str(port))
            bar.configure(value=port)
            
        # Создаем сокет
            s = socket.socket()
            
        # Ставим тайм-аут
            s.settimeout(0.01)
    
        # Ловим ошибки
            try:
                
        # Пробуем соединиться, хост и порт передаем как кортеж
                s.connect((host.rstrip(), port))
               
        # Если соединение вызвало ошибку
            except socket.error as error:
                if chk_state_a.get()==1:
                    with open("Result.txt", "a", encoding="utf-8") as file_err:
                        file_err.write(f"{error} {host.rstrip()}:{str(port)}"+"\n"+"---------------------------------"+"\n")

        #Если соединение установлено    
            else:
                with open("Result.txt", "a", encoding="utf-8") as file_s:
                    file_s.write(f"{host.rstrip()}:{port} порт активен"+"\n"+"---------------------------------"+"\n")

        # Закрываем соединение
            s.close()
            
            wnd.update()
        
    time_stop=datetime.datetime.now()
    
    txt_out.insert(INSERT, f"Сканирование завершено {str(time_stop)}\n")
    txt_out.insert(INSERT, f"за {str(time_stop-time_start)}")
    
    with open("Result.txt", "a", encoding="utf-8") as end:
        end.write(f"Сканирование завершено за {str(time_stop-time_start)}")
        
    btn.configure(state=ACTIVE)
###########################################################################################################################

def scan_from_form(host, list_of_ports):
    
    btn.configure(state=DISABLED)
    
    bar=Progressbar(wnd, length=300, mode='determinate', maximum=len(list_of_ports))
    bar.grid(column=1, row=4)
    
    #Записываем время начала
    time_start=datetime.datetime.now()
    txt_out.insert(INSERT, f"\nНачало сканирования {str(time_start)}\n")
    
    #Читаем хост из формы
    hst=host
         
    # В цикле перебираем порты из списка
    for port in list_of_ports:
        
        lbl_d.configure(text=str(port))
        bar.configure(value=port)

        # Создаем сокет
        s = socket.socket()
            
        # Ставим тайм-аут
        s.settimeout(0.01)
    
        # Ловим ошибки
        try:
                
        # Пробуем соединиться, хост и порт передаем как кортеж
            s.connect((hst.rstrip(), port))
               
        # Если соединение вызвало ошибку
        except socket.error as error:
            if chk_state_a.get()==1:
                txt_out.insert(INSERT, f"{error} {hst.rstrip()}:{str(port)}"+"\n"+"---------------------------------"+"\n")

        #Если соединение установлено    
        else:
            txt_out.insert(INSERT, f"\n{hst.rstrip()}:{port} порт активен"+"\n"+"---------------------------------"+"\n")
            
        # Закрываем соединение
        s.close()
        
        wnd.update()

    time_stop=datetime.datetime.now()
    
    txt_out.insert(INSERT, f"Сканирование завершено {str(time_stop)}\n")
    txt_out.insert(INSERT, f"за {str(time_stop-time_start)}")
    
    btn.configure(state=ACTIVE)
###########################################################################################################################
def click_chk_h():
    if chk_state.get()==1:
        txt_h.delete(0, END)
        txt_h.configure(state=DISABLED)
    else:
        txt_h.configure(state=ACTIVE)
###########################################################################################################################        
def click_start():
    ports=get_ports()
    
    if chk_state.get()==1:
        txt_out.delete(1.0, END)
        scan_from_file(ports)
    else:
        host=txt_h.get()
        txt_out.delete(1.0, END)
        scan_from_form(host, ports)
###########################################################################################################################
def click_chk_p():
    if chk_state_p.get()==0:
        txt_p.delete(0, END)
        txt_p.configure(state=DISABLED)
    else:
        txt_p.configure(state=ACTIVE)
        txt_p.focus_set()
###########################################################################################################################
def call(event):
    ports=get_ports()
    
    if chk_state.get()==1:
        txt_out.delete(1.0, END)
        scan_from_file(ports)
    else:
        host=txt_h.get()
        txt_out.delete(1.0, END)
        scan_from_form(host, ports)
###########################################################################################################################

#GUI
wnd=Tk()
wnd.geometry("590x460")
wnd.title("Port scan")
wnd.bind('<Return>', call)

chk_state=IntVar()
chk_state_a=IntVar()
chk_state_p=IntVar()
#dbg=StringVar()

lbl_h=Label(wnd, text="Host:")
lbl_h.grid(column=0, row=0)

lbl_d=Label(wnd)
lbl_d.grid(column=2, row=4)

txt_h=Entry(wnd, width=15)
txt_h.grid(column=1, row=0)
txt_h.focus_set()

txt_p=Entry(wnd, width=15, state=DISABLED)
txt_p.grid(column=1, row=3)

chk_state.set(0)
chk_h=Checkbutton(wnd, text="From file to file", variable=chk_state, onvalue=1, offvalue=0, command=click_chk_h)
chk_h.grid(column=0, row=1)

chk_state_a.set(1)
chk_a=Checkbutton(wnd, text="Show nonactive", variable=chk_state_a, onvalue=1, offvalue=0)
chk_a.grid(column=2, row=1)

chk_state_p.set(0)
chk_p=Checkbutton(wnd, text="Port range", variable=chk_state_p, onvalue=1, offvalue=0, command=click_chk_p)
chk_p.grid(column=0, row=3)

txt_out=scrolledtext.ScrolledText(wnd, width=50, font=("Calirby", 9), fg="green")
txt_out.grid(column=1, row=2)

btn=Button(text="Start", command=click_start)
btn.grid(column=2, row=0)
    
wnd.mainloop()


