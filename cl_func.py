task_read = []
code_read = []
task_in = ['',['planning'],['implementation',['R & D',['research'],['development']],['documentation']],['cleanup']]
code_in = ["00:00:00:00",["00:00:01:00"],["00:00:03:00",["00:00:02:00",["00:00:01:00"],["00:00:01:00"]],["00:00:01:00"]],["00:00:02:00"]]

def save_tasklist():
    update_arrays()
    file = open(path,'w')
    file.write(str(task_write) + "\n" + str(code_write))
    file.close()
    print(task_write)
    print(code_write)

def load_tasklist(path = 'default.txt'):
    file = open(path,'r')
    task_read = eval(file.readline())
    print(task_read)
    code_read = eval(file.readline())
    print(code_read)
    file.close()
    return task_read, code_read

