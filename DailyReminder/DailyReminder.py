"""
日常任务管理
使用菜单中的add task(l/s)添加任务到long_task_database/short_task_database
使用菜单中的list all tasks显示database中所有任务
界面中的上方按钮显示当前待完成长期任务，下方显示待完成短期任务，点击表示已完成，并更新新的任务

author: s1len0eye(@gmail.com)
date: 2018/4/9
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
        #self.current_task = tk.StringVar()
        self.long_task = tk.StringVar()
        self.short_task = tk.StringVar()
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
                #self.current_task.set(tasks['current_task'])
                self.long_task.set(tasks['long_task'])
                self.short_task.set(tasks['short_task'])
                self.long_task_database = set(tasks['long_task_database'])
                self.short_task_database = set(tasks['short_task_database'])
                #print(self.task_database)
        except Exception as e:
            #print(e)
            self.long_task.set("Please add long-term task") 
            self.short_task.set("Please add short-term task") 
            self.long_task_database = set()
            self.short_task_database = set()
            
    def createMenu(self):
        """
        创建菜单
        action -> add task(l/s), list all tasks
        """
        top = self.winfo_toplevel()
        self.menubar = tk.Menu(top)
        top['menu'] = self.menubar
        
        self.actionMenu = tk.Menu(self.menubar, tearoff=0)
        self.actionMenu.add_command(label='Add Task(L)', command=self.__addLongTask)
        self.actionMenu.add_command(label='Add Task(S)', command=self.__addShortTask)
        self.actionMenu.add_command(label='List All Tasks', command=self.__showAllTasks)
        self.menubar.add_cascade(label='Action', menu=self.actionMenu)

    def saveTasks(self):
        """
        将current_task和task_database保存到本地文件tasks.txt
        """
        tasks = {'long_task': self.long_task.get(),
                'short_task': self.short_task.get(),
                'long_task_database': self.long_task_database,
                'short_task_database': self.short_task_database,}
        try:
            with open('tasks.txt', 'bw') as f_obj:
                pickle.dump(tasks, f_obj)
        except Exception as e:
            #print(e)
            messagebox.showinfo('Fail', "Fail to save task in local file. \nPlease contact the author(s1len0eye@gmail.com)")
            
    def setLongTask(self):
        """
        更新long_task，并更新本地tasks.txt文件
        """
        try:
            self.long_task.set(self.long_task_database.pop())
        except:
            self.long_task.set("Please add long-term task") 
        finally:
            self.saveTasks()
            
    def setShortTask(self):
        """
        更新short_task，并更新本地tasks.txt文件
        """
        try:
            self.short_task.set(self.short_task_database.pop())
        except:
            self.short_task.set("Please add short-term task") 
        finally:
            self.saveTasks()
        
    def createWidgets(self):
        """
        创建当前任务按钮
        """
        font = tkinter.font.Font(family='Courier', size=12, weight='bold')
        self.button1 = tk.Button(self, textvariable=self.long_task, font=font, wraplength=500, height=2, width = 50, command=self.__longButtonHandler)
        self.button1.grid()
        self.button2 = tk.Button(self, textvariable=self.short_task, font=font, wraplength=500, height=2, width = 50, command=self.__shortButtonHandler)
        self.button2.grid()

    def __addLongTask(self):
        """
        添加新的任务到long_task_database并更新本地tasks.txt文件  
        """
        new_task = simpledialog.askstring(title='Input Long-Term Task', prompt='Enter a new long-term task: ')
        if new_task:
            self.long_task_database.add(new_task)
            self.saveTasks()
        if self.long_task.get() == "Please add long-term task":
            self.setLongTask()
            
    def __addShortTask(self):
        """
        添加新的任务到short_task_database并更新本地tasks.txt文件  
        """
        new_task = simpledialog.askstring(title='Input Short-Term Task', prompt='Enter a new short-term task: ')
        if new_task:
            self.short_task_database.add(new_task)
            self.saveTasks()
        if self.short_task.get() == "Please add short-term task":
            self.setShortTask()
                       
    def __longButtonHandler(self):
        self.setLongTask()
        
    def __shortButtonHandler(self):
        self.setShortTask()
        
    def __showAllTasks(self):
        """
        弹出新窗口显示所有任务
        """
        tasks = 'Long-Term Tasks:\n'
        for task in self.long_task_database:
            tasks += task + '\n'
        tasks += '\nShort-Term Tasks:\n'
        for task in self.short_task_database:
            tasks += task + '\n'
        if tasks:
            messagebox.showinfo('All Tasks', tasks)
        else:
            messagebox.showinfo('All Tasks', "No task yet.")

app = Application()
app.mainloop()   