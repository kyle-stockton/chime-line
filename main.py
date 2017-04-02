import time
from tkinter import *
from tkinter import ttk
from cl_func import *

t0 = time.time()
root = Tk()
task_read, time_read = load_tasklist()
flat_dict = {'':0}
task_write = ['']
time_write = [0]
lvl_arr = []
parent_arr = ['']
newitem_inc = 0


def populate_tree():
    global t0
    task_temp = task_read
    time_temp = time_read
    print(lvl_arr)
    for i in lvl_arr:
        task_temp = task_temp[i]
        time_temp = time_temp[i]
    for t in range(1,len(task_temp)):
        print("Adding " + task_temp[t][0])
        id = tree.insert(parent_arr[-1], 'end', \
            text=task_temp[t][0])
        flat_dict[id] = t0 + (time_temp[t][0] * 3600)
        if len(task_temp[t]) > 0:
            parent_arr.append(id)
            lvl_arr.append(t)
            populate_tree()
            lvl_arr.pop()
            parent_arr.pop()
    print("Done")

def update_arrays():
    task_temp = task_write
    time_temp = time_write
    for i in lvl_arr:
        task_temp = task_temp[i]
        time_temp = time_temp[i]
    for c in tree.get_children(parent_arr[-1]):
        task_temp.append([tree.item(c,'text')])
        time_temp.append([int(tree.item(c,'values'[0])[0])])
        if len(tree.get_children(c)) > 0:
            parent_arr.append(c)
            lvl_arr.append(tree.index(c)+1)
            update_arrays()
            lvl_arr.pop()
            parent_arr.pop()
    
def append_tree():
    global newitem_inc
    id = tree.insert(tree.selection()[0], 'end', text="new item " + str(newitem_inc), values=(0))
    newitem_inc += 1
    tree.see(id)

def countdown():
    for f in flat_dict:
        t = int(flat_dict[f] - time.time())
        s = t % 60
        t = (t-s) // 60
        m = t % 60
        t = (t-m) // 60
        h = t % 24
        d = (t-h) // 24
        tree.set(f, 'Time', "{:02d}:{:02d}:{:02d}:{:02d}".format(d,h,m,s))

def countdown_loop():
    countdown()
    root.after(500, countdown_loop)


def task_details():

    return 0

content = ttk.Frame(root, padding=(3,3,12,12))
tree = ttk.Treeview(content, columns=('Time'))
tree.set('', 'Time', t0 + (7 * 3600)) 
populate_tree()
namelbl = ttk.Label(content, text="Name")
name = ttk.Entry(content)
print(flat_dict)
countdown_loop()

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
new_button = ttk.Button(content, text="Add", command=append_tree)
save_button = ttk.Button(content, text="Save", command=save_tasklist)

content.grid(column=0, row=0, sticky=(N, S, E, W))
tree.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), padx=5)
name.grid(column=3, row=1, columnspan=2, sticky=(N, E, W), pady=5, padx=5)
one.grid(column=0, row=3)
two.grid(column=1, row=3)
three.grid(column=2, row=3)
new_button.grid(column=3, row=3)
save_button.grid(column=4, row=3)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)

tree.bind('<<TreeviewSelect>>', \
    lambda e: print(tree.item(tree.selection())))

root.mainloop()
