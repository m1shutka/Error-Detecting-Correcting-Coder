from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from ErrorCorrectingCoder import ErrorCorrectingCoder

def calculate_len(text):
    return len(text.replace(' ', ''))

def save_result(result):
    with open("result.txt", "w", encoding="UTF-8") as file_out:
                print(result, file=file_out)

def open_info(deffect):
    if mode.get() == 0:
        showinfo(title="Информация", message=f"Закодированная последовательность\nпомещена в файл <<result.txt>>")
    else:
        if len(deffect) == 0:
            showinfo(title="Информация", message=f"Декодированная последовательность\nпомещена в файл <<result.txt>>")
        else:
            s = ''
            for i in deffect:
                s += i + '\n'
            showinfo(title="Информация", message=f"Декодированная последовательность\nпомещена в файл <<result.txt>>.\nДеффектные слова:\n{s}")

def open_error(text): 
    showerror(title="Ошибка", message=text)

def get_table(Coder):
    data = []
    sym = Coder.get_alphabet()
    code = Coder.get_code()
    subcode = Coder.get_subcode()
    for i in range(len(sym)):
        cont = []
        cont.append(str(sym[i]))
        cont.append(str(code[i]))
        cont.append(str(subcode[i]))
        data.append(tuple(cont))
    return data

def set_table(Coder):
    data = get_table(Coder)
    for i in range(len(data)):
        tree.item(f"{i}", values=data[i])

def create_table(Coder):
    data = get_table(Coder)
    tree.heading("symbol", text="Символ")
    tree.heading("code", text="Код")
    tree.heading("subcode", text="Защищенный код")
 
    for i in range(len(data)):
        tree.insert(parent = '', index = END, iid = f"{i}", values=data[i])

def select_mode():
    combobox2.set('')
    btn_start['state'] = "disabled"
    if mode.get() == 0:
        combobox2['values'] = ["encode1", "encode2", "encode3"]
    elif mode.get() == 1:
        combobox2['values'] = ["decode1", "decode2", "decode3"]

def select_file(event):
    btn_start['state'] = "enabled"

def click_start():
    deffect = []
    if mode.get() == 0:
        error, result = Coder.encode(combobox2.get()+".txt")
    elif mode.get() == 1:
        error, deffect, result = Coder.decode(combobox2.get()+".txt")
    if error == '':
        open_info(deffect)
        save_result(result)
    else:
        open_error(error)

if  __name__ == "__main__":
    Coder = ErrorCorrectingCoder()
    root = Tk()     
    root.title("Кодировщик с исправлением ошибок")     
    root.geometry("460x330+740+270")    
    root.resizable(False, False)

    columns = ("symbol", "code", "subcode")
    tree = ttk.Treeview(columns=columns, show="headings")
    tree.column("#1", stretch=NO, width=140)
    tree.column("#2", stretch=NO, width=140)
    tree.column("#3", stretch=NO, width=140)
    tree.place(x=20, y=20, height = 170)
    scrollbar = ttk.Scrollbar(orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.place(x=442, y=20, height = 170)
    create_table(Coder)

    mode = IntVar(value=0)
    header = ttk.Label(text = "Режим:", font=("Arial", 10))
    header.place(x=20, y=230)
    btn1 = ttk.Radiobutton(text="Кодирование", value=0, variable=mode, command=select_mode)
    btn1.place(x=20, y=255)
    btn2= ttk.Radiobutton(text="Декодирование", value=1, variable=mode, command=select_mode)
    btn2.place(x=20, y=283)

    files = ["encode1", "encode2", "encode3"]
    label = ttk.Label(text = "Исходный файл:", font=("Arial", 10))
    label.place(x=300, y=230)
    combobox2 = ttk.Combobox(values=files, state="readonly")
    combobox2.place(x=300, y=255)
    combobox2.bind("<<ComboboxSelected>>", select_file)
   
    btn_start = ttk.Button(text="Стартуем", state=["disabled"], command=click_start, width = 22)
    btn_start.place(x=300, y=283)

    root.mainloop()