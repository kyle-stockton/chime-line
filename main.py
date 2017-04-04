import time
from tkinter import *
from tkinter import ttk
from pygame import mixer

default_timecode = "00:00:00:05"
task_read = ['',['New task 1']]
code_read = ["00:00:00:00",[default_timecode]]
lvl_arr = []
parent_arr = ['']
del_arr = []
newitem_inc = 1
mixer.init()
mixer.music.load('Alarm01.wav')
root = Tk()

# reads existing arrays and generates task tree
def populate_tree():
    global t0
    task_temp = task_read
    code_temp = code_read

    for i in lvl_arr:
        task_temp = task_temp[i]
        code_temp = code_temp[i]
    for t in range(1,len(task_temp)):
        id = tree.insert(parent_arr[-1], 'end', \
            text=task_temp[t][0], values=(code_temp[t][0]))
        if len(task_temp[t]) > 0:
            parent_arr.append(id)
            lvl_arr.append(t)
            populate_tree()
            lvl_arr.pop()
            parent_arr.pop()

# creates new leaf in task tree    
def append_tree():
    global newitem_inc
    newitem_inc += 1
    id = tree.insert(tree.selection()[0], 'end', text="New task " + str(newitem_inc), values=(default_timecode))
    update_parent(id)
    tree.see(id)

# clears pane display and calls methods to repopulate
def display_tasks(event):
    for k in del_arr:
        k.destroy()
    del_arr.clear()
    # get ancestry of selected tasks
    display_hierarchy(tree.selection())
    # get selected task and siblings
    display_children(tree.parent(tree.selection()), siblings)
    # get children of selected task
    display_children(tree.selection(), children)
    print(tree.parent(tree.selection()))
    return 0

# recursively populates hierarchy frame
def display_hierarchy(task):
    if tree.parent(task) != '':
        # determines row number
        i = 0
        s = task
        while s != '':
            i += 1
            s = tree.parent(s) 
        # passes arguments to task_details for current level 
        task_details(tree.parent(task), hierarchy, i)
        # calls self for next level up
        display_hierarchy(tree.parent(task))
    return 0

# populates children frame and sibling frame (using parent of selected task)
def display_children(task, frame):
    i = 0
    for t in tree.get_children(task):
        task_details(t, frame, i)
        i += 1
    return 0

# alternate method to populate siblings frame
def display_siblings(task):
    i = 1
    for t in tree.get_children(tree.parent(task)):
        if t == task:
            task_details(t, siblings, 0)
        else:
            task_details(t, siblings, i)
        i += 1
    return 0

# creates a single task entry in paned view
def task_details(task, frame, row_num):
    id = ttk.Label(frame, width=100, \
        text=tree.item(task,'text'), anchor=NE, relief='raised')
    task_lbl = ttk.Label(id, text="Task:").grid(column=0, row=0)
    task_e = ttk.Entry(id, textvariable = tree.item(task,'text'))
    task_e.grid(column=1,row=0)
    task_e.bind('<Return>',lambda e: print(tree.item(task, text=task_e.get())))
    code_lbl = ttk.Label(id, text="Time:").grid(column=2, row=0)
    code_e = ttk.Entry(id, textvariable = tree.set(task,'Time'))
    code_e.grid(column=3,row=0)
    code_e.bind('<Return>',lambda e: print(update_entry(task,code_e.get())))
    id.grid(column=0, row=row_num)
    del_arr.append(id)
    return 0

# updates timecode for corresponding task
def update_entry(task, time):
    tree.set(task,'Time',time)
    update_parent(tree.parent(task))
    return 0

# updates timecode for corresponding task according to changes to children
def update_parent(task):
    if task != '':
        i = 0
        for t in tree.get_children(task):
            i += convert_to_seconds(tree.set(t,'Time'))
        p = max(i, convert_to_seconds(tree.set(task, 'Time')))
        tree.set(task, 'Time', convert_to_timecode(p))
        update_parent(tree.parent(task))
    return 0

# converts timecode to number of seconds
def convert_to_seconds(t):
    arr = list(map(int, t.split(':')))
    return arr[0] * 86400 + arr[1] * 3600 + arr[2] * 60 + arr[3]

# converts number of seconds to timecode
def convert_to_timecode(t):
    s = t % 60
    t = (t-s) // 60
    m = t % 60
    t = (t-m) // 60
    h = t % 24
    d = (t-h) // 24
    return "{:02d}:{:02d}:{:02d}:{:02d}".format(d,h,m,s)

# calls countdown method as part of tk loop
def countdown_loop():
    countdown('')
    root.after(1000, countdown_loop)

# calculates incremental change in time remaining and updates relevant fields
def countdown(task):
    for t in tree.get_children(task):
        if tree.set(t, 'Time') != "00:00:00:00":
            i = convert_to_seconds(tree.set(t,'Time'))
            i -= 1
            tree.set(t, 'Time', convert_to_timecode(i))
            if i == 0:
                mixer.music.play()
            if len(tree.get_children(t)) > 0:
                countdown(t)
            break

content = ttk.Frame(root, padding=(3,3,12,12))

# create and populate tree view
tree = ttk.Treeview(content, columns=('Time'))
populate_tree()

# create paned view
details = ttk.PanedWindow(content, orient=VERTICAL)
hier_lbl = ttk.LabelFrame(details, text="Hierarchy", width=100, height=50)
hierarchy = Canvas(hier_lbl, height=150)
hier_scroll = ttk.Scrollbar(hier_lbl, orient=VERTICAL, command=hierarchy.yview)
hierarchy.configure(yscrollcommand=hier_scroll.set)
sibs_lbl = ttk.LabelFrame(details, text="Siblings", width=100, height=50)
siblings = Canvas(sibs_lbl, height=150)
sibs_scroll = ttk.Scrollbar(sibs_lbl, orient=VERTICAL, command=hierarchy.yview)
chil_lbl = ttk.LabelFrame(details, text="Children", width=100, height=50)
children = Canvas(chil_lbl, height=150)
chil_scroll = ttk.Scrollbar(chil_lbl, orient=VERTICAL, command=hierarchy.yview)
details.add(hier_lbl)
details.add(sibs_lbl)
details.add(chil_lbl)

# create buttons
new_button = ttk.Button(content, text="Add", command=append_tree)
start_button = ttk.Button(content, text="Start", command=countdown_loop)

# grid configuration of constant elements
content.grid(column=0, row=0, sticky=(N, S, E, W))
tree.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
details.grid(column=3, row=0, columnspan=2, rowspan=2, \
    sticky=(N, W), padx =5, pady=5)

hierarchy.grid(column=0, row=0, sticky=(N, S, E, W))
hier_scroll.grid(column=1, row=0, sticky=(N, S, E))
siblings.grid(column=0, row=1, sticky=(N, S, E, W))
sibs_scroll.grid(column=1, row=1, sticky=(N, S, E))
children.grid(column=0, row=2, sticky=(N, S, E, W))
chil_scroll.grid(column=1, row=2, sticky=(N, S, E))

new_button.grid(column=3, row=3)
start_button.grid(column=4, row=3)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)

tree.bind('<<TreeviewSelect>>', display_tasks)

root.mainloop()



def update_arrays():
    task_temp = task_write
    code_temp = code_write
    for i in lvl_arr:
        task_temp = task_temp[i]
        code_temp = code_temp[i]
    for c in tree.get_children(parent_arr[-1]):
        task_temp.append([tree.item(c,'text')])
        code_temp.append([int(tree.item(c,'values'[0])[0])])
        if len(tree.get_children(c)) > 0:
            parent_arr.append(c)
            lvl_arr.append(tree.index(c)+1)
            update_arrays()
            lvl_arr.pop()
            parent_arr.pop()

def task_details_spinbox(task,row_num):
    id = ttk.Label(hierarchy, width=100, \
        text=tree.item(task,'text'), anchor=NE, relief='raised')
    src_lbl = ttk.Label(id, text=task)
    entry = ttk.Entry(id, textvariable = tree.item(task,'text'))
    entry.grid(column=0,row=0)
    entry.bind('<KeyPress>',lambda e: print(tree.item(task, text=entry.get())))
    d_lbl = ttk.Label(id, text='Days').grid(column=0, row=1)
    d_box = Spinbox(id, from_=0, to=59, wrap=True)
    d_box.grid(column=0, row=2)
    h_lbl = ttk.Label(id, text='Hours').grid(column=1, row=1)
    h_box = Spinbox(id, from_=0, to=59, wrap=True)
    h_box.grid(column=1, row=2)
    m_lbl = ttk.Label(id, text='Minutes').grid(column=2, row=1)
    m_box = Spinbox(id, from_=0, to=59, wrap=True)
    m_box.grid(column=2, row=2)
    s_lbl = ttk.Label(id, text='Seconds').grid(column=3, row=1)
    s_box = Spinbox(id, from_=0, to=59, wrap=True)
    s_box.grid(column=3, row=2)
    id.bind('<Enter>',assign_vars(task,d_box,h_box,m_box,s_box))
    id.bind('<Leave>',clear_vars(task,d_box,h_box,m_box,s_box))
    id.grid(column=0, row=row_num)
    del_arr.append(id)
    return 0

