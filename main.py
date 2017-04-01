import time
from tkinter import *
from tkinter import ttk

root = Tk()
task_arr = ['',['eat'],['drink',['liquor',['scotch'],['tequila']],['beer']],['be merry']]
time_arr = [0,[1],[3,[2,[1],[1]],[1]],[3]]
temp_task = ['']
temp_time = [0]
lvl_arr = []
parent_arr = ['']
newitem_inc = 0

def populate_tree():
    d = task_arr
    e = time_arr
    for i in lvl_arr:
        d = d[i]
        e = e[i]
    for t in range(1,len(d)):
        parent_arr.append(tree.insert(parent_arr[-1], 'end', text=d[t][0], values=(e[t][0])))
        if len(d[t]) > 0:
            lvl_arr.append(t)
            populate_tree()
            lvl_arr.pop()
        parent_arr.pop()

def append_tree():
    global newitem_inc
    id = tree.insert(tree.selection()[0], 'end', text="new item " + str(newitem_inc), values=(0))
    newitem_inc += 1
    tree.see(id)

def update_arrays():
    d = temp_task
    e = temp_time

    return 0

content = ttk.Frame(root, padding=(3,3,12,12))
tree = ttk.Treeview(content, columns=('Time'))
populate_tree()
namelbl = ttk.Label(content, text="Name")
name = ttk.Entry(content)

onevar = BooleanVar()
twovar = BooleanVar()
threevar = BooleanVar()
onevar.set(True)
twovar.set(False)
threevar.set(True)

one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
three = ttk.Checkbutton(content, text="Three", variable=threevar, \
    onvalue=True)
ok = ttk.Button(content, text="Okay", command=append_tree)
cancel = ttk.Button(content, text="Cancel")

content.grid(column=0, row=0, sticky=(N, S, E, W))
tree.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), padx=5)
name.grid(column=3, row=1, columnspan=2, sticky=(N, E, W), pady=5, padx=5)
one.grid(column=0, row=3)
two.grid(column=1, row=3)
three.grid(column=2, row=3)
ok.grid(column=3, row=3)
cancel.grid(column=4, row=3)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)

tree.bind('<<TreeviewSelect>>', \
    lambda e: print(tree.get_children(tree.selection())))

root.mainloop()
