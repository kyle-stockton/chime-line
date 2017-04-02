task_read = []
time_read = []
task_in = ['',['eat'],['drink',['liquor',['scotch'],['tequila']],['beer']],['be merry']]
time_in = [0,[1],[3,[2,[1],[1]],[1]],[3]]

def save_tasklist():
    update_arrays()
    file = open(path,'w')
    file.write(str(task_write) + "\n" + str(time_write))
    file.close()
    print(task_write)
    print(time_write)

def load_tasklist(path = 'default.txt'):
    file = open(path,'r')
    task_read = eval(file.readline())
    print(task_read)
    time_read = eval(file.readline())
    print(time_read)
    file.close()
    return task_read, time_read

