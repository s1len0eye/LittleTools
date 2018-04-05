"""
日常任务管理
使用菜单中的add task添加任务到task_database
使用菜单中的list all tasks显示task_database中所有任务
界面中的按钮显示当前待完成任务，点击表示已完成，并更新新的任务

author: s1len0eye(@gmail.com)
date: 2018/4/5
"""

import tkinter as tk
import tkinter.font
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.current_task = tk.StringVar()
        self.master.title('Task')
        self.loadTasks()
        self.grid()
        self.createMenu()
        self.createWidgets()
        
    def loadTasks(self):
        """
        从本地文件tasts.txt中导入current_task和task_database
        如果不存在就初始化两个值
        """
        try:
            with open('tasks.txt', 'br') as f_obj:
                tasks = pickle.load(f_obj)
                self.current_task.set(tasks['current_task'])
                self.task_database = set(tasks['task_database'])
                #print(self.task_database)
        except Exception as e:
            #print(e)
            self.current_task.set("Please add task") 
            self.task_database = set()
            
    def createMenu(self):
        """
        创建菜单
        action -> add task, list all tasks
        """
        top = self.winfo_toplevel()
        self.menubar = tk.Menu(top)
        top['menu'] = self.menubar
        
        self.actionMenu = tk.Menu(self.menubar, tearoff=0)
        self.actionMenu.add_command(label='Add Task', command=self.__addTask)
        self.actionMenu.add_command(label='List All Tasks', command=self.__showAllTasks)
        self.menubar.add_cascade(label='Action', menu=self.actionMenu)

    def saveTasks(self):
        """
        将current_task和task_database保存到本地文件tasks.txt
        """
        tasks = {'current_task': self.current_task.get(),
                'task_database': self.task_database,}
        try:
            with open('tasks.txt', 'bw') as f_obj:
                pickle.dump(tasks, f_obj)
        except Exception as e:
            #print(e)
            messagebox.showinfo('Fail', "Fail to save task in local file. \nPlease contact the author(s1len0eye@gmail.com)")
            
    
    def setCurrentTask(self):
        """
        更新current_task，并更新本地tasks.txt文件
        """
        try:
            self.current_task.set(self.task_database.pop())
        except:
            self.current_task.set("Please add task") 
        finally:
            self.saveTasks()
        
    def createWidgets(self):
        """
        创建当前任务按钮
        """
        font =  tkinter.font.Font(family='Helvetica', size=36, weight='bold')
        self.button = tk.Button(self, textvariable=self.current_task, font=font, command=self.__buttonHandler)
        self.button.grid()

    def __addTask(self):
        """
        添加新的任务到task_database并更新本地tasks.txt文件  
        """
        new_task = simpledialog.askstring(title='Input Task', prompt='Enter a new task: ')
        if new_task:
            self.task_database.add(new_task)
            self.saveTasks()
        if self.current_task.get() == "Please add task":
            self.setCurrentTask()
                
        
    def __buttonHandler(self):
        self.setCurrentTask()
        
    def __showAllTasks(self):
        """
        弹出新窗口显示所有任务
        """
        tasks = ''
        for task in self.task_database:
            tasks += task + '\n'
        if tasks:
            messagebox.showinfo('All Tasks', tasks)
        else:
            messagebox.showinfo('All Tasks', "No task yet.")

app = Application()
app.mainloop()   