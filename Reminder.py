from tkinter import *
from tkinter import ttk
from plyer import notification
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tktimepicker import SpinTimePickerModern
from tktimepicker import constants
from dateutil.relativedelta import relativedelta
from datetime import timedelta
import datetime
import os
import time
import math


containerBg = "#0D0D0D" 
sidebarBg = "#1a1c1e"  
textbg = "#212121" 

class ReminderApp:
    def __init__(self, container):
        self.container = container
        self.clearFrame(self.container)

        navigationFrame = Frame(
            self.container,
            height=70,
            bg=containerBg
            )
        navigationFrame.pack(fill=X,side=TOP)
        
        self.add_icon = Image.open('icon/Add.png')
        self.add_icon = self.add_icon.resize((200,35))
        self.add_icon = ImageTk.PhotoImage(self.add_icon)
        btAdd = Button(
            navigationFrame,
            text="Add New Reminder",
            fg="white",
            font=("Times", 12, "bold"),
            compound=CENTER,
            image=self.add_icon,
            bg=containerBg,
            activebackground=containerBg,
            bd=0,
            command=lambda: self.create_new_reminder()
        )
        btAdd.pack(side=RIGHT,padx=10,pady=10)

        lbReminder = Label(
            navigationFrame,
            text="Reminder",
            fg="white",
            font=("Times", 20, "bold"),
            bg=containerBg,
            activebackground=containerBg,
            bd=0,
        )
        lbReminder.pack(side=LEFT,padx=20,pady=10)

        self.treeTodayFrame_expanded = True
        self.treeTmrFrame_expanded = False
        self.treeUpcomingFrame_expanded = False
        self.is_today_icon_rotated = False
        self.is_tmr_icon_rotated = False            
        self.is_upcoming_icon_rotated =  False
        self.treeFrame_min_height = 50
        self.treeFrame_max_height = 230

        tableFrame = Frame(
            self.container,
            width=900,
            height=750,
            bg=containerBg
            )
        tableFrame.pack(side=LEFT,anchor=NW)
        tableFrame.pack_propagate(False)

        self.treeTodayFrame = Frame(
            tableFrame,
            height=self.treeFrame_max_height,
            width= 900,
            bg=containerBg,
            )
        self.treeTodayFrame.pack()
        self.treeTodayFrame.pack_propagate(False)

        self.tableNavToday = Frame(
            self.treeTodayFrame,
            height=50,
            bg=containerBg,
            )
        self.tableNavToday.pack(side=TOP,fill=X)
        self.tableNavToday.pack_propagate(False)

        self.btopentreeToday = Button(
            self.tableNavToday,
            text="Today ",
            fg="white",
            font=("Arial", 20),
            bg=containerBg,
            activebackground=containerBg,
            bd=0,
            command= lambda : [self.animate_frame(window = self.container,frame=self.treeTodayFrame,max_height=self.treeFrame_max_height,min_height=self.treeFrame_min_height,frame_status=self.treeTodayFrame_expanded),self.rotate_arrow(frame=self.tableNavToday,icon_status = self.is_today_icon_rotated,label=self.downIconToday,iconPath = 'icon/up.png')]
        )
        self.btopentreeToday.pack(side=LEFT,anchor=NW,padx=(25,0))

        self.downToday_icon = Image.open('icon/up.png')
        self.downToday_icon = self.downToday_icon.resize((30,30))
        self.downToday_icon = ImageTk.PhotoImage(self.downToday_icon)
        self.downIconToday = Label(
            self.tableNavToday,
            image=self.downToday_icon,
            bg=containerBg,
        )
        self.downIconToday.pack(side=LEFT,anchor=NW,pady=10)

        self.treeTmrFrame = Frame(
            tableFrame,
            height=self.treeFrame_min_height,
            width= 900,
            bg=containerBg,
            )
        self.treeTmrFrame.pack()
        self.treeTmrFrame.pack_propagate(False)

        self.tableNavTmr = Frame(
            self.treeTmrFrame,
            height=50,
            bg=containerBg,
            )
        self.tableNavTmr.pack(side=TOP,fill=X)
        self.tableNavTmr.pack_propagate(False)

        self.btopentreeTmr = Button(
            self.tableNavTmr,
            text="Tomorrow",
            fg="white",
            font=("Arial", 20),
            bg=containerBg,
            activebackground=containerBg,
            bd=0,
            command= lambda : [self.animate_frame(window = self.container,frame=self.treeTmrFrame,max_height=self.treeFrame_max_height,min_height=self.treeFrame_min_height,frame_status=self.treeTmrFrame_expanded),self.rotate_arrow(frame=self.tableNavTmr,icon_status = self.is_tmr_icon_rotated,label=self.downIconTmr,iconPath='icon/down.png')]
        )
        self.btopentreeTmr.pack(side=LEFT,anchor=NW,padx=(25,0))

        self.downTmr_icon = Image.open('icon/down.png')
        self.downTmr_icon = self.downTmr_icon.resize((30,30))
        self.downTmr_icon = ImageTk.PhotoImage(self.downTmr_icon)

        self.downIconTmr = Label(
            self.tableNavTmr,
            image=self.downTmr_icon,
            bg=containerBg,
        )
        self.downIconTmr.pack(side=LEFT,anchor=NW,pady=10)

        self.treeUpcomingFrame = Frame(
            tableFrame,
            height=self.treeFrame_min_height,
            width= 900,
            bg=containerBg,
            )
        self.treeUpcomingFrame.pack()
        self.treeUpcomingFrame.pack_propagate(False)

        self.tableNavUpcoming = Frame(
            self.treeUpcomingFrame,
            height=50,
            bg=containerBg,
            )
        self.tableNavUpcoming.pack(side=TOP,fill=X)
        self.tableNavUpcoming.pack_propagate(False)

        self.btopentreeUpcoming = Button(
            self.tableNavUpcoming,
            text="Upcoming",
            fg="white",
            font=("Arial", 20),
            bg=containerBg,
            activebackground=containerBg,
            bd=0,
            command= lambda : [self.animate_frame(window = self.container,frame=self.treeUpcomingFrame,max_height=self.treeFrame_max_height,min_height=self.treeFrame_min_height,frame_status=self.treeUpcomingFrame_expanded),self.rotate_arrow(frame=self.tableNavUpcoming,icon_status = self.is_upcoming_icon_rotated,label=self.downIconUpcoming,iconPath='icon/down.png')]
        )
        self.btopentreeUpcoming.pack(side=LEFT,anchor=NW,padx=(25,0))

        self.downUpcoming_icon = Image.open('icon/down.png')
        self.downUpcoming_icon = self.downUpcoming_icon.resize((30,30))
        self.downUpcoming_icon = ImageTk.PhotoImage(self.downUpcoming_icon)

        self.downIconUpcoming = Label(
            self.tableNavUpcoming,
            image=self.downUpcoming_icon,
            bg=containerBg,
        )
        self.downIconUpcoming.pack(side=LEFT,anchor=NW,pady=10)

        if not os.path.exists("Reminder_Data_Record.txt"):
            with open("Reminder_Data_Record.txt",'w') as file:
                file.write("")
        
        self.style = ttk.Style()
        self.style.theme_use("default")
        
        self.style.configure(
            "Custom.Treeview",
            background=containerBg,      
            fieldbackground=containerBg, 
            foreground="white",          
            font=('Arial', 13),
        )

        # Style for Treeview headers
        self.style.configure(
            "Custom.Treeview.Heading",
            background=sidebarBg,   
            foreground='white',         
            font=('Arial', 14, 'bold'), 
        )
        
        self.treeToday = ttk.Treeview(
            self.treeTodayFrame,
            height= 10,
            style="Custom.Treeview",
            columns = ('Title', 'Description', 'Date', 'Time', 'Recurrence Type','Status'),
            show = 'headings',
        )

        self.treeTmr = ttk.Treeview(
            self.treeTmrFrame,
            height= 10,
            style="Custom.Treeview",
            columns = ('Title', 'Description', 'Date', 'Time', 'Recurrence Type','Status'),
            show = 'headings',
        )

        self.treeUpcoming = ttk.Treeview(
            self.treeUpcomingFrame,
            height= 10,
            style="Custom.Treeview",
            columns = ('Title', 'Description', 'Date', 'Time', 'Recurrence Type','Status'),
            show = 'headings',
        )

        self.clockScreen_height = 600
        self.clockScreen_width = 545

        self.clockFrame = Canvas(
            self.container,
            width=self.clockScreen_width,
            height=self.clockScreen_height,
            bg=containerBg,
            )
        self.clockFrame.pack(side=LEFT,anchor=NE)
        self.clockFrame.pack_propagate(False)
        
        self.create_table(tree=self.treeToday,frame=self.treeTodayFrame)
        self.create_table(tree=self.treeTmr,frame=self.treeTmrFrame)
        self.create_table(tree=self.treeUpcoming,frame=self.treeUpcomingFrame)

        self.current_date = datetime.date.today()
        self.current_year = self.current_date.year
        self.current_month = self.current_date.month 
        self.current_day = self.current_date.day
        self.current_hour = int(time.strftime("%H"))
        self.current_minute = int(time.strftime("%M"))
        self.current_sec = int(time.strftime("%S"))

        self.digitalClock = Label(
            self.clockFrame,
            text="",
            fg = "white",
            font=("Arial", 30),
            bg = containerBg
        ) 
        self.digitalClock.pack(side=BOTTOM,pady=30)

        self.recurring()
        self.Arrange_date()
        self.clock()

    def clearFrame(self, container):
        for widget in container.winfo_children():
            widget.destroy()

    def create_new_reminder(self):
        self.window = Toplevel(self.container)
        self.window.title("Add New Reminder")
        self.window.geometry("500x600")
        self.window.configure(bg=containerBg)

        content_Frame = Frame(
            self.window,
            height=600,
            width=500,
            bg=containerBg,
        )
        content_Frame.pack(fill=BOTH)

        lbTitle = Label(
            content_Frame,
            text="TITLE:",
            font=("Times", 15),
            fg="white",
            bg=containerBg
        )
        lbTitle.pack(pady=10)

        self.inputTitle = Text(
            content_Frame,
            bd=0,
            fg="white",
            font=("Times", 15),
            bg=textbg,
            width=40,
            height=2,
            insertbackground="white"
        )
        self.inputTitle.pack()

        lbDescription = Label(
            content_Frame,
            text="DESCRIPTION:",
            font=("Times", 15),
            fg="white",
            bg=containerBg
        )
        lbDescription.pack(pady=10)

        self.inputDescription = Text(
            content_Frame,
            bd=0,
            fg="white",
            font=("Times", 15),
            bg=textbg,
            width=40,
            height=2,
            insertbackground="white"
        )
        self.inputDescription.pack()

        lbDate = Label(
            self.window,
            text="DATE:",
            font=("Times", 15),
            fg="white",
            bg=containerBg
        )
        lbDate.pack(pady=10)

        self.date_var = StringVar()
        self.date_entry = DateEntry(
            self.window, 
            width=30,
            font=("Times", 10),
            textvariable=self.date_var, 
            date_pattern='dd/MM/yyyy',
            showweeknumbers=False,
            weekendbackground="white",
            weekendforeground="black",
            othermonthwebackground="white",
            state="readonly"
        )
        self.date_entry.pack()

        self.setTimeFrame_expanded = False
        self.setTimeFrame_min_height = 50
        self.setTimeFrame_max_height = 300

        self.setTimeFrame = Frame(
            self.window,
            height=self.setTimeFrame_min_height,
            bg=containerBg,
        )
        self.setTimeFrame.pack(fill=X)
        self.setTimeFrame.pack_propagate(FALSE)

        self.isCheckboxTick = IntVar()
        setTimeCheckbox = Checkbutton(
            self.setTimeFrame,
            text="Set Time",
            font=("Times", 20),
            fg="white",
            command=lambda: self.animate_frame(window = self.window, frame=self.setTimeFrame,max_height=self.setTimeFrame_max_height,min_height = self.setTimeFrame_min_height,frame_status =self.setTimeFrame_expanded),
            bg=containerBg,
            activebackground=containerBg,
            selectcolor="black",
            variable=self.isCheckboxTick,
            onvalue=1,
            offvalue=0,
        )
        setTimeCheckbox.pack()


        lbTime = Label(
            self.setTimeFrame,
            text="TIME:",
            font=("Times", 15),
            fg="white",
            bg=containerBg
        )
        lbTime.pack(pady=10)

        self.time_picker = SpinTimePickerModern(self.setTimeFrame)
        self.time_picker.addAll(constants.HOURS12, ["{:02d}".format(i) for i in range(60)])
        self.time_picker.configureAll(
            bg="#212121",         
            height=1, 
            fg="#ffffff",          
            font=("Times", 16), 
            hoverbg="#2e2d2d",     
            hovercolor="#ffffff",  
            clickedbg="#404040",   
            clickedcolor="#d73333",
        )
        self.time_picker.configure_separator(bg="#212121", fg="#ffffff")
        self.time_picker.pack()

        lbRecurring = Label(
            self.setTimeFrame,
            text="RECURRING:",
            font=("Times", 15),
            fg="white",
            bg=containerBg
        )
        lbRecurring.pack(pady=10)

        self.recurrence_type = ["Don't repeat", "Everyday", "Every week", "Every month", "Every year"]
        self.setrecurringCombobox = ttk.Combobox(self.setTimeFrame, values=self.recurrence_type, font=("Times", 10), width=30,state="readonly")
        self.setrecurringCombobox.set("Don't repeat")
        self.setrecurringCombobox.pack()

        btSubmit = Button(
            self.window,
            text="SUBMIT",
            fg="BLACK",
            font=("Times", 12, "bold"),
            bg="WHITE",
            activebackground=containerBg,
            bd=0,
            command=lambda: self.set_messagebox()
        )
        btSubmit.pack()

    def set_messagebox(self):
        self.title = self.inputTitle.get("1.0", 'end-1c')
        self.description = self.inputDescription.get("1.0", 'end-1c')
        self.date = self.date_var.get()
        self.selected_time = self.time_picker.time()
        self.recurrence_type = self.setrecurringCombobox.get()
        self.isCheckboxTick_type = self.isCheckboxTick.get()

        self.selected_date = self.date_entry.get_date()
        self.selected_year = self.selected_date.year
        self.selected_month = self.selected_date.month
        self.selected_day = self.selected_date.day
        
        self.selected_minute = self.selected_time[1]
        
        if  self.selected_time[2]== "AM" and self.selected_time[0] == 12:
            self.selected_hour = 0
        elif  self.selected_time[2]== "PM" and self.selected_time[0] == 12:
            self. selected_hour = 12
        elif self.selected_time[2]== "PM":
            self.selected_hour = self.selected_time[0] + 12
        else:
            self.selected_hour = self.selected_time[0]
        
        if self.selected_year < self.current_year or (self.selected_year == self.current_year and self.selected_month < self.current_month) or (self.selected_year == self.current_year and self.selected_month == self.current_month and self.selected_day < self.current_day):
            messagebox.showerror("Alert", "You must enter a valid date!")
        elif self.isCheckboxTick_type and ((self.selected_date == self.current_date and self.selected_hour < self.current_hour) or (self.selected_date == self.current_date and self.selected_hour == self.current_hour and self.selected_minute < self.current_minute)) :
            messagebox.showerror("Alert", "You must enter a valid time!")
        elif self.title.strip() == "" or self.description.strip() == "":
            messagebox.showerror("Alert", "Title and description are required!")
        else:
            response = messagebox.askyesno("Notifier Set", "Set notification?")
            if response:
                self.selected_sec = int(time.strftime("%S"))
                self.savedata()
                self.recurring()
                self.Arrange_date()
                self.window.destroy()
                self.set_notification()

    def set_notification(self):
        self.update_datetime()
        self.update_file()
        self.update_data = ""

        for i in range(self.reminderListRow):
            if self.isCheckboxTick_type and (str(self.reminderList[i][2]) == self.current_date_updated and str(self.reminderList[i][3]) == self.current_time_updated and self.reminderList[i][5]=="Inactive"):
                notification.notify(
                    title=self.reminderList[i][0],
                    message=self.reminderList[i][1],
                    app_name="Notifier", 
                    app_icon="icon/ico.ico",
                    toast=True,
                    timeout=10
                )
                self.reminderList[i][5] = "Active"
            elif not self.isCheckboxTick_type and (str(self.reminderList[i][2]) == self.current_date_updated) and self.reminderList[i][5]=="Inactive":
                notification.notify(
                    title=self.reminderList[i][0],
                    message=self.reminderList[i][1],
                    app_name="Notifier", 
                    app_icon="icon/ico.ico",
                    toast=True,
                    timeout=10
                )
                self.reminderList[i][5] = "Active"

        with open("Reminder_Data_Record.txt", 'w') as file:
            for i in range(self.reminderListRow):
                self.update_data = f"TITLE | {self.reminderList[i][0]} \nDESCRIPTION | {self.reminderList[i][1]} \nDATE | {self.reminderList[i][2]} \nTIME | {self.reminderList[i][3]} \nRECURRENCE TYPE | {self.reminderList[i][4]}\nSTATUS | {self.reminderList[i][5]}\n\n"
                file.write(self.update_data)
        file.close()
        self.Arrange_date()
        self.container.after(1000, self.set_notification)

    def update_file(self):
        self.reminderList = []
        with open("Reminder_Data_Record.txt", 'r') as file:
            valueList = [None for _ in range(6)]
            lines = file.readlines()    
            i = 0
        
            for line in lines:
                parts = line.strip("\n").split("|")
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if key == "TITLE":
                        valueList[0] = value
                    elif key == "DESCRIPTION":
                        valueList[1] = value 
                    elif key == "DATE":
                        valueList[2] = value
                    elif key == "TIME":
                        valueList[3] = value
                    elif key == "RECURRENCE TYPE":
                        valueList[4] = value
                    else:
                        valueList[5] = value
                    i += 1
                    if i == 6:
                        i = 0
                        self.reminderList.append(valueList)
                        valueList = [None] * 6
            self.reminderListRow = len(self.reminderList)

    def update_datetime(self):
        self.current_time_updated = time.strftime("%I:%M %p")
        self.current_date_updated = datetime.date.today().strftime("%d/%m/%Y")
        self.container.after(1000, self.update_datetime)
    
    def savedata(self):
        match self.isCheckboxTick_type :
            case 1:
                data = f"TITLE | {self.title} \nDESCRIPTION | {self.description} \nDATE | {self.date} \nTIME | {"{:02d}:{:02d} {}".format(*self.selected_time)} \nRECURRENCE TYPE | {self.recurrence_type}\nSTATUS | Inactive\n\n"
            case 0:
                data = f"TITLE | {self.title} \nDESCRIPTION | {self.description} \nDATE | {self.date} \nTIME |  \nRECURRENCE TYPE | {self.recurrence_type}\nSTATUS | Inactive\n\n"
        with open("Reminder_Data_Record.txt", 'a') as file:
            file.write(data)
        file.close()

    def recurring(self):
        self.update_file()

        for i in range(self.reminderListRow):
            self.current_reminder_date = datetime.datetime.strptime(self.reminderList[i][2], "%d/%m/%Y").date()
            if  self.current_reminder_date <  self.current_date  and self.reminderList[i][4] != "Don't repeat":
                self.recurrence_title = self.reminderList[i][0]
                self.recurrence_description = self.reminderList[i][1]
                self.recurrence_time = self.reminderList[i][3]
                self.recurrence_recurrence_type = self.reminderList[i][4]
                self.recurrence_status = self.reminderList[i][5]

                if self.recurrence_recurrence_type == "Every year":
                    self.recurrence_date = self.current_reminder_date + relativedelta(years=1)
                elif self.recurrence_recurrence_type == "Every month":
                    self.recurrence_date = self.current_reminder_date + relativedelta(months=1)
                elif self.recurrence_recurrence_type == "Every week":
                    self.recurrence_date = self.current_reminder_date + timedelta(weeks=1)
                else:
                    self.recurrence_date = self.current_reminder_date + timedelta(days=1)
                
                with open("Reminder_Data_Record.txt", 'r') as file:
                    existing_records = file.read()
                info = f"TITLE | {self.recurrence_title} \nDESCRIPTION | {self.recurrence_description} \nDATE | {self.recurrence_date.strftime('%d/%m/%Y')} \nTIME | {self.recurrence_time} \nRECURRENCE TYPE | {self.recurrence_recurrence_type}\nSTATUS | {self.recurrence_status}\n\n"
                if info != existing_records :
                    with open("Reminder_Data_Record.txt", 'a') as file:
                        file.write(info)
                    file.close()
    
    def create_table(self,tree,frame):
        match tree:
            case self.treeToday:
                mouseScroll = self.Mouse_Scroll_Today
            case self.treeTmr:
                mouseScroll = self.Mouse_Scroll_Tmr
            case _:
                mouseScroll = self.Mouse_Scroll_Upcoming

        tree.heading('Title', text='Title')
        tree.heading('Description', text='Description')
        tree.heading('Date', text='Date')
        tree.heading('Time', text='Time')
        tree.heading('Recurrence Type', text='Recurrence Type')
        tree.heading('Status', text='Status')
        
        tree.column('Title', anchor=CENTER, width=145)
        tree.column('Description', anchor=CENTER, width=145)
        tree.column('Date', anchor=CENTER, width=30)
        tree.column('Time', anchor=CENTER, width=25)
        tree.column('Recurrence Type', anchor=CENTER, width=130)
        tree.column('Status', anchor=CENTER, width=20)
        tree.pack(side=LEFT, fill=X, expand=True,padx=40,pady=10)
        
        # Add scrollbar and define the mouse
        self.v_scroll = ttk.Scrollbar(frame,orient=VERTICAL,command=tree.yview)
        self.treeToday.bind("<MouseWheel>", mouseScroll)

    def Arrange_date(self):
        self.update_file()
        self.delete_tree(tree=self.treeToday)
        self.delete_tree(tree=self.treeTmr)
        self.delete_tree(tree=self.treeUpcoming)

        for i in range(self.reminderListRow):
            self.reminder_date = datetime.datetime.strptime(self.reminderList[i][2], "%d/%m/%Y").date()
            difference_in_dates = self.reminder_date - self.current_date
            match difference_in_dates:
                case timedelta(days=0):
                    self.update_tree(tree=self.treeToday,title=self.reminderList[i][0], description=self.reminderList[i][1], date=self.reminderList[i][2], time=self.reminderList[i][3],recurrence_type=self.reminderList[i][4],status=self.reminderList[i][5])
                case timedelta(days=1):
                    self.update_tree(tree=self.treeTmr,title=self.reminderList[i][0], description=self.reminderList[i][1], date=self.reminderList[i][2], time=self.reminderList[i][3],recurrence_type=self.reminderList[i][4],status=self.reminderList[i][5])
                case timedelta(days=d) if d > 1:
                    self.update_tree(tree=self.treeUpcoming,title=self.reminderList[i][0], description=self.reminderList[i][1], date=self.reminderList[i][2], time=self.reminderList[i][3],recurrence_type=self.reminderList[i][4],status=self.reminderList[i][5])
    
    def delete_tree(self,tree):
        for row in tree.get_children():
            tree.delete(row)

    def update_tree(self,tree,title,description,date,time,recurrence_type,status):
        tree.insert('', END, values=(title,description,date,time,recurrence_type,status))
        
    def Mouse_Scroll_Today(self,event):
        self.treeToday.yview_scroll(-1 * (event.delta // 120), "units")
    
    def Mouse_Scroll_Tmr(self,event):
        self.treeTmr.yview_scroll(-1 * (event.delta // 120), "units")
    
    def Mouse_Scroll_Upcoming(self,event):
        self.treeUpcoming.yview_scroll(-1 * (event.delta // 120), "units")

    def animate_frame( self,window,frame,max_height,min_height,frame_status):
        if not frame_status:
            for height in range(min_height, max_height + 1, 10):
                frame.config(height=height)
                window.update()
        else:
            for height in range(max_height,min_height - 1, -10):
                frame.config(height=height)
                window.update()
        
        match frame:
            case self.treeTodayFrame:
                self.treeTodayFrame_expanded = not self.treeTodayFrame_expanded
            case self.treeTmrFrame:
                self.treeTmrFrame_expanded = not self.treeTmrFrame_expanded
            case self.treeUpcomingFrame:
                self.treeUpcomingFrame_expanded = not self.treeUpcomingFrame_expanded
            case self.setTimeFrame:
                self.setTimeFrame_expanded = not self.setTimeFrame_expanded
            case _:
                pass
    
    def rotate_arrow( self,frame,icon_status,label,iconPath):
        icon = Image.open(iconPath)
        icon = icon.resize((30,30))
        
        if not icon_status:
            self.rotated_icon = icon.rotate(angle=180)
        else:
            self.rotated_icon = icon
        
        match frame:
            case self.tableNavToday:
                self.is_today_icon_rotated = not self.is_today_icon_rotated
            case self.tableNavTmr:
                self.is_tmr_icon_rotated = not self.is_tmr_icon_rotated           
            case self.tableNavUpcoming:
                self.is_upcoming_icon_rotated = not self.is_upcoming_icon_rotated 
            case _:
                pass

        self.update_icon = ImageTk.PhotoImage(self.rotated_icon)
        label.config(image=self.update_icon)
        label.image = self.update_icon  
        frame.update()

    def clock(self):
        self.clockFrame.delete("all")
        self.display_ampm = time.strftime("%p")
        self.draw_markings()
        self.curr_time = time.strftime('%I%M%S', time.localtime(time.time()))
        self.display_ampm = time.strftime("%p")
        self.drawClock_second = int(self.curr_time[4]) * 10 + int(self.curr_time[5])
        self.drawClock_minutes = int(self.curr_time[2]) * 10 + int(self.curr_time[3])
        self.drawClock_hours = int(self.curr_time[0]) * 10 + int(self.curr_time[1])
        # Draw arcs
        self.arc((self.clockScreen_width // 2, self.clockScreen_height // 2), 200, 0, self.drawClock_second * 6, 11, "#BCA34B" )
        self.arc((self.clockScreen_width // 2, self.clockScreen_height // 2), 180, 0, self.drawClock_minutes * 6, 11, "#BC744B")
        self.arc((self.clockScreen_width // 2, self.clockScreen_height // 2), 160, 0, self.drawClock_hours * 30, 11, "#37567B")

        # Draw clock hands
        self.clock_hand((self.clockScreen_width // 2, self.clockScreen_height // 2), 140, self.drawClock_second * 6, 5,"#BCA34B")
        self.clock_hand((self.clockScreen_width // 2, self.clockScreen_height // 2), 120, self.drawClock_minutes * 6, 5, "#BC744B")
        self.clock_hand((self.clockScreen_width // 2, self.clockScreen_height // 2), 100, self.drawClock_hours * 30, 5, "#37567B")
        self.digitalClock.config(text="{:02d}:{:02d}:{:02d} {}".format(self.drawClock_hours, self.drawClock_minutes, self.drawClock_second, self.display_ampm))
        self.clockFrame.after(1000,self.clock)

    def draw_markings(self):
        d = 100
        d2 = 10
        for i in range(0, 360, 30):
            # start point
            x1 = self.clockScreen_width // 2 + d * math.cos(math.radians(i))
            y1 = self.clockScreen_height // 2 + d * math.sin(math.radians(i))
            # end point
            x2 = x1 + d2 * math.cos(math.radians(i))
            y2 = y1 + d2 * math.sin(math.radians(i))
            self.clockFrame.create_line(x1, y1, x2, y2, fill="white", width=5)

    def arc(self,center, radius, start, end, thickness, color):
            x0 = center[0] - radius
            y0 = center[1] - radius
            x1 = center[0] + radius
            y1 = center[1] + radius

            adjusted_start = (start + 90) % 360  
    
            self.clockFrame.create_arc(
                x0, y0, x1, y1,
                start=adjusted_start,
                extent= start - end,
                outline=color,
                width=thickness,
                style="arc"
            )
    
    def clock_hand(self,center, radius, angle, thickness, color):
        x = center[0] + radius * math.cos(math.radians(angle - 90))
        y = center[1] + radius * math.sin(math.radians(angle - 90))
        self.clockFrame.create_line(
        center[0], center[1], x, y,
        fill=color,
        width=thickness
    )
        

def reminder(): 
    app = ReminderApp()
    app.run()

if __name__ == "__main__":
    reminder()