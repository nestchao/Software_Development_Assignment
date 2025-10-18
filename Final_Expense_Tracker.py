from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkcalendar import Calendar
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import Toplevel, Label, messagebox
import time

class Expense_Tracker:
#--------------------------------------------------------------
    def __init__(self, container):
        # Basic initialization of the UI settings and paths
        self.BG_COLOR = "#181818"
        self.SIDEBAR_COLOR = "#212121"
        self.ACTIVE_COLOUR = "#383838"
        self.FONT_MAIN = ("Arial",16,"bold")
        self.FONT_SUB = ("Arial",12,"bold")
        self.FONT_BUTTON = ("Arial",10,"bold")
        self.FONT_BIG = ("Arial", 20, "bold")
        
        # Paths for images and icons used in the app
        self.Photo_Path = "Expense_Tracker_Photo"
        self.P_Blue_Rectangle = "Expense_Tracker_Photo/Blue Rectangle.png"
        self.P_Expense_Icon_Path = ["Expense_Tracker_Photo/Food_Icon.png","Expense_Tracker_Photo/Bus_Icon.png","Expense_Tracker_Photo/Tissue_Icon.png","Expense_Tracker_Photo/Home_Icon.png", "Expense_Tracker_Photo/Utilities_Icon.png","Expense_Tracker_Photo/Education_Icon.png","Expense_Tracker_Photo/Entertaiment_Icon.png", "Expense_Tracker_Photo/Other_Icon.png"]
        self.P_Black_Square = "Expense_Tracker_Photo/Black_Rectangle.png"
        self.P_Account_Icon_Path = ['Expense_Tracker_Photo/Cash_Icon.png','Expense_Tracker_Photo/Touch_N_Go_Icon.png', 'Expense_Tracker_Photo/Debit_Card_Icon.png', 'Expense_Tracker_Photo/Bank_Icon.png']
        self.P_Income_Icon_Path = ["Expense_Tracker_Photo/Income_Icon.png","Expense_Tracker_Photo/Stock_Icon.png","Expense_Tracker_Photo/Allowance_Icon.png","Expense_Tracker_Photo/Other_Icon.png"]
        self.P_Black_Rectangle = ["Expense_Tracker_Photo/Black_Rectangle1.png"]
        
        # File paths for storing data
        self.N_Income_History_File = "Expense_Tracker_Data/Income_History.txt"
        self.N_Expense_History_File = "Expense_Tracker_Data/Expense_History.txt"
        self.N_Assets_File = "Expense_Tracker_Data/Assets.txt"
        self.N_Expense_File = "Expense_Tracker_Data/Expense.txt"
        
        # Categories for accounts, expenses, and income
        self.account_Type = ['Cash','E-wallet','Debit Card','Bank']
        self.expense_Category = ["Food", "Transport", "Daily Necessities", "Housing Expense", "Utilities", "Education", "Entertaiment", "Other"]
        self.expense_Category_Short = ["Food", "Transport", "Daily", "Housing", "Utilities", "Education", "Entertaiment", "Other"]
        self.income_Category = ["Income","Stock","Allowance","Other"]
        self.assetsLst = [" ", " ", " "," "," "," "]
        
       # Initialize button references for highlighting
        self.ACTIVE_BUTTON1 = None
        self.ACTIVE_BUTTON2 = None
        
        # Initialize sidebar and window
        #self.sidebar_Frame = sidebar
        self.window = container

        # self.Clear_Sidebar()
        # self.Sidebar()
        self.Create_Center_Content()


#--------------------------------------------------------------
    def Create_Center_Content(self):
        # Clears the current frame and loads data into the UI
        self.Clear_Frame()
        self.Check_Data()
        self.Load_Expense_And_Income()
        
        self.Full_Frame = Frame(self.window,width=1920,height=1080,bg='white')
        self.Full_Frame.pack(side=LEFT,fill=Y)
        self.Full_Frame.pack_propagate(False)
        self.Full_Frame.grid_propagate(False)

        # Clear the full frame and set up top navigation bar
        self.Clear_Full_Frame()

        self.top_Navigator =Frame(self.Full_Frame,height=50,width=1920,bg=self.SIDEBAR_COLOR)
        self.top_Navigator.pack(side=TOP, fill=X)
        self.top_Navigator.pack_propagate(False)
        self.top_Navigator.grid_propagate(False)
        
        # Load blue rectangle image and add 'Add a new bill' button
        self.Load_Image(self.P_Blue_Rectangle,150,30)
        #Create a button to create a new bill
        self.add_New_Bill = Button(
            self.top_Navigator,
            text="Add New Expense",
            font=self.FONT_BUTTON,
            bg=self.SIDEBAR_COLOR,
            fg="white",
            borderwidth=0,
            image=self.img,
            compound="center",
            activebackground=self.SIDEBAR_COLOR,
            activeforeground="white",
            command=self.Add_New_Bill
            )
        self.add_New_Bill.image = self.img
        self.add_New_Bill.pack(side=RIGHT, fill=X, padx=30)
        
        # Set up middle frame to hold the main content
        self.Middle_Frame = Frame(self.Full_Frame, bg=self.BG_COLOR, width=1920,height=1080)
        self.Middle_Frame.pack(side=LEFT, fill=Y)
        
        self.top5_high_exp_type = [" ", " ", " ", " ", " "]
        self.Load_Expense_And_Income()
        
        # Reposition top navigator and middle frame
        self.top_Navigator.pack_forget()
        self.Middle_Frame.pack_forget()
        self.top_Navigator.pack(side=TOP, fill=X)
        self.top_Navigator.pack_propagate(False)
        self.top_Navigator.grid_propagate(False)
        self.Middle_Frame.pack(side=LEFT, fill=Y)
        self.Clear_Middle_Frame()
        
        # Print total expense label and amount
        self.Load_Image('Expense_Tracker_Photo/Black_Rectangle1.png',1455,130)
        black_rectangle = Label(self.Middle_Frame,image=self.img,bg=self.BG_COLOR, fg='#D7D7D7', text="Total Expenses\n\n\n",compound=CENTER,font=self.FONT_MAIN)
        black_rectangle.image = self.img
        black_rectangle.place(x=10,y=10)
        
        ttl_exp_frm = Frame(self.Middle_Frame, bg=self.SIDEBAR_COLOR,width=100,height=50)
        ttl_exp_frm.place(x=680,y=80)
        
        ttl_exp_amt = Label(ttl_exp_frm,text=f"{self.total_Expense:.2f}",
                            bg=self.SIDEBAR_COLOR,
                            fg='white',
                            font=("Arial",24,"bold"))
        ttl_exp_amt.grid()
        
        # Grey rectangle and expense history area
        self.Load_Image("Expense_Tracker_Photo/Black_Rectangle2.png",1455,600)
        center_Content_Rectangle = Label(self.Middle_Frame,image=self.img,bg=self.BG_COLOR)
        center_Content_Rectangle.image = self.img
        center_Content_Rectangle.place(x=15,y=155)
        
        print_exp_history_frame = Frame(self.Middle_Frame,width=800,height=400,bg=self.SIDEBAR_COLOR)
        print_exp_history_frame.place(x=40,y=240)
        print_exp_history_frame.pack_propagate(False)
        
        # Treeview to show the expense history
        self.style = ttk.Style()
        self.style.theme_use("default")
        
        self.style.configure(
            "Custom.Treeview",
            background=self.SIDEBAR_COLOR,      
            fieldbackground=self.SIDEBAR_COLOR, 
            foreground="white",          
            font=('Arial', 13)
        )

        # Style for Treeview headers
        self.style.configure(
            "Custom.Treeview.Heading",
            background=self.SIDEBAR_COLOR,   
            foreground='white',         
            font=('Arial', 14, 'bold'), 
        )
        
        self.tree = ttk.Treeview(
            print_exp_history_frame,
            style="Custom.Treeview",
            columns = ('Date', 'Amount', 'Payment Method', 'Category', 'Remarks'),
            show = 'headings',
        )
        
        # Treeview column headers
        self.tree.heading('Date', text='Date')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Payment Method', text='Payment Method')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Remarks', text='Remarks')
        
        # Treeview column settings
        self.tree.column('Date', anchor=CENTER, width=25)
        self.tree.column('Amount', anchor=CENTER, width=30)
        self.tree.column('Payment Method', anchor=CENTER, width=5)
        self.tree.column('Category', anchor=CENTER, width=75)
        self.tree.column('Remarks', anchor=CENTER, width=150)
        self.tree.pack(expand=True, fill=BOTH)
        
        # Scrollbar and mouse wheel interaction
        self.v_scroll = ttk.Scrollbar(print_exp_history_frame,orient=VERTICAL,command=self.tree.yview)
        self.tree.bind("<MouseWheel>", self.Mouse_Scroll)
        
        # Load data into the treeview
        self.load_data_into_tree()
        
         # Right-click menu for editing or deleting records
        self.rg_Click_Menu = Menu(self.Middle_Frame,tearoff=0)
        self.rg_Click_Menu.add_command(label="Edit", command=self.Edit_Data)
        self.rg_Click_Menu.add_command(label="Delete", command=self.Delete_Data)
        
        # Bind right-click menu to treeview
        self.tree.bind("<Button-3>", self.Right_Click)  
        
        expense_category_not0 = []
        expense_amount_not0 = []
        
        for i in range(len(self.expense_Category_Short)):
            key = self.expense_Category_Short[i]
            value = self.expense_Amount_Dict.get(key)
            if value != 0 and value != None:
                expense_category_not0.append(key)
                expense_amount_not0.append(value)
            
        # Pie chart for expense categories
        fig = Figure(figsize=(5,5), dpi=110) # Size of the pie chart
        fig.patch.set_facecolor(self.SIDEBAR_COLOR)
        ax = fig.add_subplot(111)
        ax.pie(expense_amount_not0, labels=expense_category_not0,autopct='%1.1f%%', startangle=90)
        for text in ax.texts:
            text.set_color('white')
            text.set_fontsize(10)
        
        # Draw pie chart onto the canvas
        canvas=FigureCanvasTkAgg(fig,master=self.Middle_Frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=870,y=170)
        
        # Labels for expense history and top expenses
        print_Expense_History = Label(self.Middle_Frame,text="Expense History", font=self.FONT_BIG, bg=self.SIDEBAR_COLOR,fg='white')
        print_Expense_History.place(x=50,y=190)
        
        print_Top5_Exp = Label(self.Middle_Frame,text="Expense Breakdown", font=self.FONT_BIG, bg=self.SIDEBAR_COLOR,fg='white')
        print_Top5_Exp.place(x=1030,y=190)


#--------------------------------------------------------------
    def Add_New_Bill(self):
        # Open the 'Add New Bill' interface
        self.top_Navigator.pack_forget()
        self.Clear_Middle_Frame()
        
        # Button to close or navigate back
        print_Close_Button = Button(self.Middle_Frame,text="x",fg="white",bg=self.BG_COLOR,font=("Arial",20,"bold"),activebackground=self.ACTIVE_COLOUR,activeforeground="white",borderwidth=0,width=3,height=1,command=self.Create_Center_Content)
        print_Close_Button.place(x=10,y=2)

        show_Choose_Expense_Category = Label(self.Middle_Frame, fg="white",bg=self.BG_COLOR,font=("Arial",12,"bold"), text="Choose Expense Category:")
        show_Choose_Expense_Category.place(x=100,y=60)
        
        # Buttons for Expense and Income types
        print_Expense= Button(self.Middle_Frame,text="Expense",fg="#E73D41",bg=self.BG_COLOR,font=self.FONT_SUB,activebackground=self.ACTIVE_COLOUR,activeforeground="#E73D41",borderwidth=0)
        print_Expense.place(x=550,y=10)
    
        print_Income = Button(self.Middle_Frame, text="Income",fg="white",bg=self.BG_COLOR,font=self.FONT_SUB,activebackground=self.ACTIVE_COLOUR,activeforeground="white",borderwidth=0,command=self.Add_Income)
        print_Income.place(x=750,y=10)
        
        # Display buttons for expense categories
        i = 0
        j = 0
        for i in range(0,8):
            self.Load_Image(self.P_Expense_Icon_Path[i],30,30)
            expense_button = Button(
                self.Middle_Frame,
                text = f"{self.expense_Category[i]}",
                font=("Arial",14,"bold"),
                bg=self.SIDEBAR_COLOR,
                fg="white",
                image=self.img,
                compound=TOP,
                relief=FLAT,
                activebackground=self.SIDEBAR_COLOR,
                activeforeground='white',
                width=200,
                height=100,
                borderwidth=0,
                )
            expense_button.image=self.img
            if i > 3:
                expense_button.place(x=100+(j*300),y=210)
                j+=1
            else:
                expense_button.place(x=100+(i*300),y=100)
            expense_button.config(command=lambda button=expense_button, ic=self.expense_Category[i]: [self.Highlight_Button1(button),self.Store_Assets1(category=ic)])
        
        # Account selection labels
        print_Account_Type = Label(self.Middle_Frame,text="Select Payment Method:",bg=self.BG_COLOR,font=self.FONT_MAIN,fg='white')
        print_Account_Type.place(x=50,y=340)
        
        for i in range(0,4):
            self.Load_Image(self.P_Account_Icon_Path[i],60,60)
            account_Label = Button(self.Middle_Frame,
                                  image=self.img,
                                  text=f"           {self.account_Type[i]}",
                                  compound=LEFT,
                                  font=self.FONT_MAIN,
                                  fg='white',
                                  bg=self.SIDEBAR_COLOR,
                                  borderwidth=0,
                                  activeforeground='white',
                                  activebackground=self.SIDEBAR_COLOR,
                                  width=250,
                                  anchor='w'
                                  )
            account_Label.image = self.img
            account_Label.place(x=40,y=380+(i*80))
            account_Label.config(command=lambda button=account_Label,x=self.account_Type[i]: [self.Highlight_Button2(button),self.Store_Assets1(account= x)])
        
        show_Enter_Description = Label(self.Middle_Frame, bg=self.BG_COLOR, fg='white', font = self.FONT_MAIN, text='Enter Expenses Remark:')
        show_Enter_Description.place(x=730,y=400)

        # Create entry to enter description
        description_Entry = Entry(self.Middle_Frame,bg=self.BG_COLOR,fg='grey',borderwidth=0,font=self.FONT_MAIN,insertbackground='white')
        description_Entry.insert(0, "Description")
        description_Entry.bind("<FocusIn>",self.Saving_Description_Entry_Clear)
        description_Entry.bind("<FocusOut>",self.Saving_Description_Entry_Restore)
        description_Entry.place(x=990,y=403)
        
        show_Enter_Expense = Label(self.Middle_Frame, bg=self.BG_COLOR,fg='white',borderwidth=0,font=self.FONT_MAIN, text="Enter Expense Amount:")
        show_Enter_Expense.place(x=740, y=500)

        # Create entry to input amount
        money_Entry = Entry(self.Middle_Frame,bg=self.BG_COLOR,fg='#F5494D',borderwidth=0,font=self.FONT_MAIN, insertbackground='#F5494D')
        money_Entry.insert(0, "0.00")
        money_Entry.bind("<FocusIn>",self.Expense_Money_Entry_Clear)
        money_Entry.bind("<FocusOut>",self.Expense_Money_Entry_Restore)
        money_Entry.place(x=990,y=500)

        show_Enter_Date = Label(self.Middle_Frame,bg=self.BG_COLOR,fg='white',font=self.FONT_MAIN, text="Choose Date:")
        show_Enter_Date.place(x=350, y=340)

        #Create date to input date
        calendar = Calendar(self.Middle_Frame,
                            background=self.SIDEBAR_COLOR,  
                            foreground="white",  
                            bordercolor=self.SIDEBAR_COLOR,  
                            headersbackground=self.SIDEBAR_COLOR,  
                            headersforeground="white",  
                            weekendbackground=self.SIDEBAR_COLOR,  
                            weekendforeground="white",
                            normalbackground= self.SIDEBAR_COLOR,
                            normalforeground='white',
                            othermonthbackground=self.SIDEBAR_COLOR,
                            othermonthforeground="white",
                            font=self.FONT_SUB,
                            showothermonthdays=False,
                            showweeknumbers=False,
                            date_pattern="dd/mm/yyyy"
                            )
        calendar.place(x=350,y=375,width=350,height=330)
        
        #Print the button to update the assets
        self.Load_Image(self.P_Blue_Rectangle,150,30)
        
        # Create button to update assets (Expense)
        input_Expense = Button(
            self.Middle_Frame,
            text="Update Expense",
            font=self.FONT_BUTTON,
            bg=self.BG_COLOR,
            fg='white',
            borderwidth=0,
            image=self.img,
            compound='center',
            activebackground=self.BG_COLOR,
            activeforeground='white',
        command=lambda: self.Store_Assets2(description_Entry.get(), money_Entry.get(), calendar.get_date(),'Expense')
        )
        input_Expense.image = self.img
        input_Expense.place(x=1285,y=9) # Position on screen


#--------------------------------------------------------------        
    # Function to add income
    def Add_Income(self):
        self.Clear_Middle_Frame()   # Clear current content on the middle frame   
            
        # Close button for the frame
        print_Close_Button = Button(self.Middle_Frame,text="x",fg="white",bg=self.BG_COLOR,font=("Arial",20,"bold"),activebackground=self.ACTIVE_COLOUR,activeforeground="white",borderwidth=0,width=3,height=1,command=self.Create_Center_Content)
        print_Close_Button.place(x=10,y=2)
        
        show_Choose_Income_Category = Label(self.Middle_Frame, fg="white",bg=self.BG_COLOR,font=("Arial",12,"bold"), text="Choose Income Category:")
        show_Choose_Income_Category.place(x=80,y=90)
        
        # Button to switch to "Expense" section
        print_Expense= Button(self.Middle_Frame,text="Expense",fg="white",bg=self.BG_COLOR,font=self.FONT_SUB,activebackground=self.ACTIVE_COLOUR,activeforeground="white",borderwidth=0, command=self.Add_New_Bill)
        print_Expense.place(x=550,y=10)

        # Button to switch to "Income" section
        print_Income = Button(self.Middle_Frame, text="Income",fg="#2CC684",bg=self.BG_COLOR,font=self.FONT_SUB,activebackground=self.ACTIVE_COLOUR,activeforeground="#2CC684",borderwidth=0)
        print_Income.place(x=750,y=10)
        
        # Loop to display income category buttons
        i = 0
        for i in range(0,4):
            self.Load_Image(self.P_Income_Icon_Path[i],30,30)
            income_button = Button(
                self.Middle_Frame,
                text=f"{self.income_Category[i]}",
                font=("Arial",14,"bold"),
                bg=self.SIDEBAR_COLOR,
                fg="white",
                image=self.img,
                compound=TOP,
                relief=FLAT,
                activebackground=self.SIDEBAR_COLOR,
                activeforeground='white',
                width=300,
                height=105,
                borderwidth=0
            )
            income_button.image = self.img
            income_button.place(x=75+(i*350),y=150)
            income_button.config(command=lambda ic=self.income_Category[i], bt=income_button: [self.Store_Assets1(category=ic),self.Highlight_Button1(bt)])
        
        # Create background square for account selection
        
        # Label for account type selection
        print_Account_Type = Label(self.Middle_Frame,text="Select Payment Method:",bg=self.BG_COLOR,font=self.FONT_MAIN,fg='white')
        print_Account_Type.place(x=50,y=340)
        
        # Loop to display account type buttons
        for i in range(0,4):
            self.Load_Image(self.P_Account_Icon_Path[i],60,60)
            account_Label = Button(self.Middle_Frame,
                                  image=self.img,
                                  text=f"           {self.account_Type[i]}",
                                  compound=LEFT,
                                  font=self.FONT_MAIN,
                                  fg='white',
                                  bg=self.SIDEBAR_COLOR,
                                  borderwidth=0,
                                  activeforeground='white',
                                  activebackground=self.SIDEBAR_COLOR,
                                  width=250,
                                  anchor='w'
                                  )
            account_Label.image = self.img
            account_Label.place(x=40,y=380+(i*80))  # Position dynamically
            account_Label.config(command=lambda button=account_Label,x=self.account_Type[i]: [self.Highlight_Button2(button),self.Store_Assets1(account= x)])   # Store account data when clicked

        show_Income_Description = Label(self.Middle_Frame, bg=self.BG_COLOR, fg='white', font = self.FONT_MAIN, text='Enter Income Remark:')
        show_Income_Description.place(x=730,y=400)

        # Create entry to enter description
        description_Entry = Entry(self.Middle_Frame,bg=self.BG_COLOR,fg='grey',borderwidth=0,font=self.FONT_MAIN, insertbackground='white')
        description_Entry.insert(0, "Description")
        description_Entry.bind("<FocusIn>",self.Saving_Description_Entry_Clear)
        description_Entry.bind("<FocusOut>",self.Saving_Description_Entry_Restore)
        description_Entry.place(x=965,y=403)
        
        show_Enter_Income = Label(self.Middle_Frame, bg=self.BG_COLOR,fg='white',borderwidth=0,font=self.FONT_MAIN, text="Enter Income Amount:")
        show_Enter_Income.place(x=740, y=500)

        # Create entry to input amount
        money_Entry = Entry(self.Middle_Frame,bg=self.BG_COLOR,fg='#3DD393',borderwidth=0,font=self.FONT_MAIN, insertbackground='#3DD393')
        money_Entry.insert(0, "0.00")
        money_Entry.bind("<FocusIn>",self.Saving_Money_Entry_Clear)
        money_Entry.bind("<FocusOut>",self.Saving_Money_Entry_Restore)
        money_Entry.place(x=980,y=500)

        show_Enter_Date = Label(self.Middle_Frame,bg=self.BG_COLOR,fg='white',font=self.FONT_MAIN, text="Choose Date:")
        show_Enter_Date.place(x=350, y=340)

        # Create calendar to input date
        calendar = Calendar(self.Middle_Frame,
                            background=self.SIDEBAR_COLOR,  
                            foreground="white",  
                            bordercolor=self.SIDEBAR_COLOR,  
                            headersbackground=self.SIDEBAR_COLOR,  
                            headersforeground="white",
                            weekendbackground=self.SIDEBAR_COLOR,  
                            weekendforeground="white",
                            normalbackground= self.SIDEBAR_COLOR,
                            normalforeground='white',
                            othermonthbackground=self.SIDEBAR_COLOR,
                            othermonthforeground="white",
                            showothermonthdays=False,
                            font=self.FONT_SUB,
                            showweeknumbers=False,
                            date_pattern="dd/mm/yyyy" 
                            )
        calendar.place(x=350,y=375,width=350,height=300)
        
        #Print the button to update the assets
        self.Load_Image(self.P_Blue_Rectangle,150,30)
        
        # Button to update assets (Income)
        input_Income = Button(
            self.Middle_Frame,
            text="Update Assets",
            font=self.FONT_BUTTON,
            bg=self.BG_COLOR,
            fg='white',
            borderwidth=0,
            image=self.img,
            compound='center',
            activebackground=self.BG_COLOR,
            activeforeground='white',
            command=lambda: self.Store_Assets2(description_Entry.get(), money_Entry.get(), calendar.get_date(),'Income')
        )
        input_Income.image = self.img
        input_Income.place(x=1285,y=9)  # Position on screen
        

#Call function at below
#--------------------------------------------------------------
    # Use to initialize the image by resizing and converting it for Tkinter display
    def Load_Image(self, image_Path, image_Width, image_Height):
        self.img = Image.open(image_Path)
        self.img = self.img.resize((image_Width,image_Height))
        self.img = ImageTk.PhotoImage(self.img)
        
#--------------------------------------------------------------      
    # Clear the entry if the default 'Description' text is present
    def Saving_Description_Entry_Clear(self,event):
        widget = event.widget
        if widget.get() == "Description":
            widget.delete(0,END)
            widget.config(fg="white")
    
#--------------------------------------------------------------
    # Check and create necessary files if they do not exist
    def Saving_Description_Entry_Restore(self,event):
        widget = event.widget
        if not widget.get():
            widget.insert(0, "Description")
            widget.config(fg='white')
    
    
#--------------------------------------------------------------
    # Clear the entry if the default "0.00" text is present    
    def Saving_Money_Entry_Clear(self,event):
        widget = event.widget
        if widget.get() == "0.00":
            widget.delete(0,END)
            widget.config(fg="#3DD393")
    
    
#--------------------------------------------------------------  
    # Restore the default "0.00" text if the entry is empty  
    def Saving_Money_Entry_Restore(self,event):
        widget = event.widget
        if not widget.get():
            widget.insert(0, "0.00")
            widget.config(fg='#3DD393')


#--------------------------------------------------------------
    # Check and create necessary files if they do not exist
    def Check_Data(self):
        
        if not os.path.exists(self.N_Income_History_File):
            with open(self.N_Income_History_File,'w') as file:
                file.write("")
        
        if not os.path.exists(self.N_Expense_History_File):
            with open(self.N_Expense_History_File,'w') as file:
                file.write("")
                
        if not os.path.exists(self.N_Assets_File):
            with open(self.N_Assets_File,'w') as file:
                file.write("")
        
        if not os.path.exists(self.N_Expense_File):
            with open(self.N_Expense_File,'w') as file:
                file.write("")
                

#--------------------------------------------------------------
    # Clear all widgets in the middle frame
    def Clear_Frame(self):
        for widget in self.window.winfo_children():
            widget.destroy()


#--------------------------------------------------------------
    # Clear all widgets in the sidebar area
    def Clear_Navigator(self):
        for widget in self.top_Navigator.winfo_children():
            widget.destroy()
            

#--------------------------------------------------------------
    # Clear all widgets in the sidebar area
    def Clear_Sidebar(self):
        for widget in self.dsd.winfo_children():
            widget.destroy()
            
            
#--------------------------------------------------------------
    # Clear all widgets in the middle frame and reset button states
    def Clear_Middle_Frame(self):
        for widget in self.Middle_Frame.winfo_children():
            widget.destroy()
        
        # After press into the new bill and quit it the button need to reset
        # Otherwise the button won't be highlighted anymore
        self.ACTIVE_BUTTON1 = None
        self.ACTIVE_BUTTON2 = None


#--------------------------------------------------------------
    # Clear all widgets in the full frame
    def Clear_Full_Frame(self):
        for widget in self.Full_Frame.winfo_children():
            widget.destroy()


#-------------------------------------------------------------- 
    # Clear all widgets in the sidebar frame       
    def Clear_Sidebar(self):
        for widget in self.sidebar_Frame.winfo_children():
            widget.destroy()


#--------------------------------------------------------------      
    # Clear the entry if the default 'Description' text is present
    def Saving_Description_Entry_Clear(self,event):
        widget = event.widget
        if widget.get() == "Description":
            widget.delete(0,END)
            widget.config(fg="grey")
    
    
#--------------------------------------------------------------
    # Restore the default 'Description' text if the entry is empty
    def Saving_Description_Entry_Restore(self,event):
        widget = event.widget
        if not widget.get():
            widget.insert(0, "Description")
            widget.config(fg='grey')
    
    
#--------------------------------------------------------------   
    # Clear the entry if the default "0.00" text is present 
    def Saving_Money_Entry_Clear(self,event):
        widget = event.widget
        if widget.get() == "0.00":
            widget.delete(0,END)
            widget.config(fg="#3DD393")
    
    
#--------------------------------------------------------------  
    # Restore the default "0.00" text if the entry is empty  
    def Saving_Money_Entry_Restore(self,event):
        widget = event.widget
        if not widget.get():
            widget.insert(0, "0.00")
            widget.config(fg='#3DD393')


#-------------------------------------------------------------- 
    # Clear the entry if the default "0.00" text is present for expenses    
    def Expense_Money_Entry_Clear(self,event):
        widget=event.widget
        if widget.get() == "0.00":
            widget.delete(0, END)
            widget.config(fg="#F5494D")
            
            
#-------------------------------------------------------------- 
    # Restore the default "0.00" text if the entry is empty for expenses
    def Expense_Money_Entry_Restore(self,event):
        widget=event.widget
        if not widget.get():
            widget.insert(0, "0.00")
            widget.config(fg="#F5494D")
            
            
#--------------------------------------------------------------  
    # Highlight Button1 and reset the previously active button  
    def Highlight_Button1(self, new_Button1):
        if self.ACTIVE_BUTTON1 is not None:
            self.ACTIVE_BUTTON1.config(bg=self.SIDEBAR_COLOR)
        new_Button1.config(bg="#454545") 
        self.ACTIVE_BUTTON1 = new_Button1

    
#--------------------------------------------------------------
    # Highlight Button2 and reset the previously active button    
    def Highlight_Button2(self,new_Button2):
        if self.ACTIVE_BUTTON2 is not None:
            self.ACTIVE_BUTTON2.config(bg=self.SIDEBAR_COLOR)
        new_Button2.config(bg="#454545") 
        self.ACTIVE_BUTTON2 = new_Button2
        

#--------------------------------------------------------------
    def Load_Expense_And_Income(self):
        # Initialize expense amounts and related data structures
        self.expense_Amount = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.expense_Amount_Dict = {}
        self.income_Amount_Dict = {}
        self.top5_high_exp = [0.00,0.00,0.00,0.00,0.00]
        self.top5_low_exp = [0.00,0.00,0.00,0.00]
        self.total_Expense = 0

        # Load expense data from file
        with open(self.N_Expense_File,'r') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.split(":")
            if len(parts) == 2:
                key = parts[0].strip()
                value_str = parts[1].strip()
                
                value = float(value_str)
                # Map expense categories to specific indices
                if key == 'Food':
                    self.expense_Amount_Dict[key] = value
                    self.expense_Amount[0] = value
                elif key == 'Transport':
                    self.expense_Amount_Dict[key] = value
                    self.expense_Amount[1] = value
                elif key == 'Daily':
                    self.expense_Amount_Dict[key] = value
                    self.expense_Amount[2] = value
                elif key == 'Housing':
                    self.expense_Amount_Dict[key] = value
                    self.expense_Amount[3] = value
                elif key == 'Utilities':
                    self.expense_Amount_Dict[key] = value
                    self.expense_Amount[4] = value
                elif key == 'Education':
                    self.expense_Amount_Dict[key] = value
                    self.expense_Amount[5] = value
                elif key == 'Entertaiment':
                    self.expense_Amount_Dict[key] = value
                    self.expense_Amount[6] = value
                elif key == 'Other':
                    self.expense_Amount_Dict[key] = value
                    self.expense_Amount[7] = value
                                  
        # Calculate total expenses
        for i in range(0,8):
            self.total_Expense += self.expense_Amount[i]
    
        # Find the top 5 highest and lowest expenses
        self.top5_high_exp = sorted(self.expense_Amount,reverse=True)[:5]
        self.top5_low_exp = sorted(self.expense_Amount)[:4]
        
        # Load income data from assets file
        self.income_Amount = [0.00,0.00,0.00,0.00]
        self.Total_Assets = 0
    
        with open(self.N_Assets_File,'r') as file:
            lines = file.readlines()
            
        for line in lines:
            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                value_str = parts[1].strip()

                value = float(value_str)
                # Map income categories to specific indices
                if key == 'Cash':
                    self.income_Amount_Dict[key] = value
                    self.income_Amount[0] = value
                elif key == 'E-wallet':
                    self.income_Amount_Dict[key] = value
                    self.income_Amount[1] = value
                elif key == 'Debit Card':
                    self.income_Amount_Dict[key] = value
                    self.income_Amount[2] = value
                elif key == 'Bank':
                    self.income_Amount_Dict[key] = value
                    self.income_Amount[3] = value

        # Calculate total assets
        for i in range(0,4):
            self.Total_Assets += self.income_Amount[i]

#--------------------------------------------------------------
    def load_data_into_tree(self):
        # Clear existing rows in the tree view
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = []
        # Read expense history from file and parse data
        with open(self.N_Expense_History_File, 'r') as file:
            record = {}
            for line in file:
                line = line.strip()  
                if not line:  
                    if record:  
                        date = record.get("Date", "")
                        amount = record.get("Amount", "")
                        account = record.get("Account", "")
                        category = record.get("Category", "")
                        description = record.get("Description", "")
                        data.append({
                            "Date": date,
                            "Amount": amount,
                            "Account": account,
                            "Category": category,
                            "Description": description,
                        })
                        record = {}  
                else:
                    if ": " in line:    # Parse key-value pairs
                        key, value = line.split(": ", 1)
                        record[key] = value

        # Sort data by date in descending order
        data.sort(key=lambda x: datetime.strptime(x["Date"], "%d/%m/%Y"),reverse=True)

        # Insert parsed data into the tree view
        for record in data:
            self.tree.insert('', END, values=(record["Date"], record["Amount"], record["Account"], record["Category"], record["Description"]))


#--------------------------------------------------------------
    # Store category and account information
    def Store_Assets1(self, category=None, account=None):
        if category is not None:
            self.assetsLst[1] = f"Category: {category} "
        if account is not None:
            self.assetsLst[4] = f"Account: {account} "


#--------------------------------------------------------------
    # Store description, amount, and date information
    def Store_Assets2(self,description=None, amount=None, date=None,category=None):
        # Validate input data
        if amount.isalpha() == 1 or self.ACTIVE_BUTTON1 == None or self.ACTIVE_BUTTON2 == None and amount>0:
            messagebox.showerror("Error", "Please fill it correctly")
            return
        
        amount = float(amount)
        
        if amount < 1:
            messagebox.showerror("Error", "Please fill integer number")
            return

        # Set description to 'Description' if not provided
        if description != 'Description':
            self.assetsLst[2] = f"Description: {description}"
        else:
            self.assetsLst[2] = f"Description: "
        
        # Validate and adjust amounts based on category
        if category == 'Expense':    
            different_acc = self.assetsLst[4].split(":")[1].strip()
            if different_acc == 'Cash':
                differentiate_acc = 0
            elif different_acc == 'E-wallet':
                differentiate_acc = 1
            elif different_acc == 'Debit Card':
                differentiate_acc = 2
            elif different_acc == 'Bank':
                differentiate_acc = 3
            
            # if self.income_Amount[differentiate_acc] > float(amount):
            #     self.assetsLst[3] = f"Amount: {amount} "
            # else:
            #     messagebox.showerror("Invalid Input", "You don't have enough assets")
            #     return
        
        self.assetsLst[3] = f"Amount: {amount} "
        self.assetsLst[0] = f"Date: {date} "
        
        # Determine category and update corresponding amounts
        different_acc = self.assetsLst[4].split(":")[1].strip()
        amount = float(self.assetsLst[3].split(":")[1])
        
        #Categorize if it is income or not then sum it and store it into Income.txt 
        if category == "Income":
            formula = 1
        else:
            formula = -1
            
        if different_acc == 'Cash':
            self.income_Amount[0] += formula * amount
        elif different_acc == 'E-wallet':
            self.income_Amount[1] += formula * amount
        elif different_acc == 'Debit Card':
            self.income_Amount[2] += formula * amount
        elif different_acc == 'Bank':
            self.income_Amount[3] += formula * amount
        
        # Append to history file
        if category =='Income':
            with open(self.N_Income_History_File, 'a') as file:
                for item in self.assetsLst:
                    file.write(item+'\n')
            file.close()
        else:
        # Update assets file
            with open(self.N_Expense_History_File, 'a') as file:
                for item in self.assetsLst:
                    file.write(item+'\n')
            file.close()
        
        data = f"Cash: {self.income_Amount[0]:.2f}\nE-wallet: {self.income_Amount[1]:.2f}\nDebit Card: {self.income_Amount[2]:.2f}\nBank: {self.income_Amount[3]:.2f}"
        
        with open(self.N_Assets_File, 'w') as file:
            file.write(data)
        file.close()
        
        if category == 'Expense':
            expense_Category = self.assetsLst[1].split(":")[1].strip()
            expense_Category_No = self.expense_Category.index(expense_Category)
            self.expense_Amount[expense_Category_No] += amount
            
            data = f"Food: {self.expense_Amount[0]:.2f}\nTransport: {self.expense_Amount[1]:.2f}\nDaily: {self.expense_Amount[2]:.2f}\nHousing: {self.expense_Amount[3]:.2f}\nUtilities: {self.expense_Amount[4]:.2f}\nEducation: {self.expense_Amount[5]:.2f}\nEntertaiment: {self.expense_Amount[6]:.2f}\nOther: {self.expense_Amount[7]:.2f}"
        
            with open(self.N_Expense_File, 'w')as file:
                file.write(data)
            file.close()
        
        self.Create_Center_Content()


#--------------------------------------------------------------
    def Save_Income_Account(self):
        # Prepare data string representing income amounts by category
        data = f"Cash: {self.income_Amount[0]:.2f}\nE-wallet: {self.income_Amount[1]:.2f}\nDebit Card: {self.income_Amount[2]:.2f}\nBank: {self.income_Amount[3]:.2f}"

        # Write income data to file
        with open(self.N_Assets_File, 'w') as file:
            file.write(data)
        file.close()


#--------------------------------------------------------------
    def Save_Expense_Account(self):
        # Prepare data string representing expense amounts by category
        data = f"Food: {self.expense_Amount[0]:.2f}\nTransport: {self.expense_Amount[1]:.2f}\nDaily: {self.expense_Amount[2]:.2f}\nHousing: {self.expense_Amount[3]:.2f}\nUtilities: {self.expense_Amount[4]:.2f}\nEducation: {self.expense_Amount[5]:.2f}\nEntertaiment: {self.expense_Amount[6]:.2f}\nOther: {self.expense_Amount[7]:.2f}"
        
        # Write expense data to file
        with open(self.N_Expense_File, 'w')as file:
            file.write(data)
        file.close()
    

#--------------------------------------------------------------
    def Animate_Bar_Chart(self, frame,min,max): 
         # Gradually increase the width of the frame to create an animation effect
        for height in range(min, max + 1, 5):
            frame.config(width=height)
            self.window.update()
            time.sleep(0.01)


#--------------------------------------------------------------
    def Mouse_Scroll(self,event):
        # Scroll the tree view vertically based on mouse wheel input
        self.tree.yview_scroll((event.delta // 120), "units")


#--------------------------------------------------------------
    def Right_Click(self,event):
        # Identify the row in the tree view under the cursor
        row_Id = self.tree.identify_row(event.y)
        if row_Id:
            self.tree.selection_set(row_Id) # Select the identified row
            self.rg_Click_Menu.post(event.x_root, event.y_root) # Display context menu

#--------------------------------------------------------------
    def Edit_Data(self):
        # Get the selected row in the tree view
        self.selected_Data = self.tree.selection()
        
        # Retrieve the values of the selected row
        values = self.tree.item(self.selected_Data, "values")
        
        # Open the edit window with the selected row's values
        self.Open_Edit_Window(values)


#--------------------------------------------------------------
    def Open_Edit_Window(self, values):
        # Create a new top-level window for editing data
        Edit_Window = Toplevel(self.window)
        Edit_Window.title("Edit data")
        
        # Create and configure widgets for editing each field
        prt_Date = Label(Edit_Window, text="Date (DD/MM/YYYY): ")
        prt_Date.grid(row=0,column=0,padx=10,pady=5)
        date_Entry = DateEntry(Edit_Window, width=20, state="readonly", date_pattern="dd/mm/yyyy")
        date_Entry.delete(0,"end")
        date_Entry.insert(0, values[0])
        date_Entry.grid(row=0,column=1,padx=10,pady=5)
        
        # Use to print the amount and edit the amount
        prt_Amount = Label(Edit_Window, text="Amount: ")
        prt_Amount.grid(row=1,column=0,padx=10,pady=5)
        amount_Entry = Entry(Edit_Window, width=22)
        amount_Entry.insert(0, values[1])
        amount_Entry.grid(row=1,column=1,padx=10,pady=5)
        
        prt_Acc = Label(Edit_Window, text="Account")
        prt_Acc.grid(row=2,column=0, padx=10, pady=5)
        acc_Entry = ttk.Combobox(Edit_Window, values=self.account_Type, state="readonly")
        acc_Entry.set(values[2])
        acc_Entry.grid(row=2,column=1, padx=10,pady=5)
        
        # Use to print the category and the 
        prt_Category = Label(Edit_Window, text="Category: ")
        prt_Category.grid(row=3,column=0,padx=10,pady=5)
        category_Entry = ttk.Combobox(Edit_Window, values=self.expense_Category, state="readonly")
        category_Entry.set(values[3])
        category_Entry.grid(row=3,column=1,padx=10,pady=5)
        
        # Use to print the description and let user to edit
        prt_Description = Label(Edit_Window, text="Description: ")
        prt_Description.grid(row=4,column=0,padx=10,pady=5)
        description_Entry = Entry(Edit_Window, width=22)
        description_Entry.insert(0, values[4])
        description_Entry.grid(row=4,column=1,padx=10,pady=5)

        # Print save button to store 
        save_Button = Button(Edit_Window, text="Save",
                             command=lambda: self.Store_Editted_Data(date_Entry.get(),
                                                                     amount_Entry.get(),
                                                                     acc_Entry.get(),
                                                                     category_Entry.get(),
                                                                     description_Entry.get(),
                                                                     Edit_Window,
                                                                     values))
        save_Button.grid(row=5,column=0,columnspan=2,pady=20)


#--------------------------------------------------------------
    def Store_Editted_Data(self, date, amount, account, category, description, edit_window, original_values):
        # Validate that the amount is a numeric value
        if amount.isalpha == 1:
            messagebox.showerror("Invalid Input", "Please input number only")
     
        # Update the tree view item with the new values
        self.tree.item(self.selected_Data, values=(date, amount, account, category, description))
        
        amount = float(amount)
        original_Exp_Amount = float(original_values[1])
        original_Account = original_values[2]
        original_Category = original_values[3]
        
        if account == original_Account:
            # If category remains the same
            if category == original_Category:
                # Adjust account balance based on amount change
                account_No = self.account_Type.index(account)
                expense_no = self.expense_Category.index(category)
                
                # If new amount is higher
                if amount > original_Exp_Amount:
                    difference_exp = amount - original_Exp_Amount
                    
                    # Check if enough balance exists
                    if self.income_Amount[account_No] >= difference_exp:
                        self.income_Amount[account_No] -= difference_exp
                        self.expense_Amount[expense_no] += difference_exp
                    else:
                        messagebox.showerror("Invalid Input", "You don't have enough assets")
                        return
                
                # If new amount is lower
                elif amount < original_Exp_Amount:
                    difference_exp = original_Exp_Amount - amount
                    self.income_Amount[account_No] += difference_exp
                    self.expense_Amount[expense_no] -= difference_exp
            
            # If category changes
            else:
                # Remove amount from original category
                original_expense_No = self.expense_Category.index(original_Category)
                self.expense_Amount[original_expense_No] -= original_Exp_Amount
                
                # Add amount to new category
                new_expense_No = self.expense_Category.index(category)
                self.expense_Amount[new_expense_No] += amount
        
        # If account changes
        else:
            # Remove from original account and category
            original_account_No = self.account_Type.index(original_Account)
            original_expense_No = self.expense_Category.index(original_Category)
            
            # Check if new account has enough balance
            new_account_No = self.account_Type.index(account)
            if self.income_Amount[new_account_No] >= amount:
                # Adjust original account
                self.income_Amount[original_account_No] += original_Exp_Amount
                
                # Adjust new account
                self.income_Amount[new_account_No] -= amount
                
                # Adjust categories
                self.expense_Amount[original_expense_No] -= original_Exp_Amount
                
                # Add to new category if different
                if category != original_Category:
                    new_expense_No = self.expense_Category.index(category)
                    self.expense_Amount[new_expense_No] += amount
                else:
                    self.expense_Amount[original_expense_No] += amount
            else:
                messagebox.showerror("Invalid Input", "Insufficient balance in the selected account")
                return
            
        # Save updated accounts
        self.Save_Income_Account()
        self.Save_Expense_Account()
        self.Update_Expense_History()
        #Close the edit window
        edit_window.destroy()


#--------------------------------------------------------------
    def Delete_Data(self):
        # Get the selected row in the tree view
        selected_Data = self.tree.selection()
        
        # Retrieve values of the selected row
        values = self.tree.item(selected_Data, "values")
        
        # Delete the selected row from the tree view
        self.tree.delete(selected_Data)
        
        amount = float(values[1])
        account = values[2]
        expense = values[3]
        account_No = self.account_Type.index(account)
        expense_No = self.expense_Category.index(expense)
        self.income_Amount[account_No] += amount
        self.expense_Amount[expense_No] -= amount
        
        self.Save_Income_Account()
        self.Save_Expense_Account()
        self.Update_Expense_History()

#--------------------------------------------------------------
    def Update_Expense_History(self):
        # Collect all rows from the tree view
        rows = self.tree.get_children()
        data=[]
        for row in rows:
            data.append(self.tree.item(row, "values"))
        
        # Write expense history to a file
        with open(self.N_Expense_History_File, 'w') as file:
            for record in data:
                file.write(f"Date: {record[0]}\nCategory: {record[3]}\nDescription: {record[4]}\nAmount: {record[1]}\nAccount: {record[2]}\n\n")
        
        self.Create_Center_Content()
        
        

    def Open_Assets_Page(self):
        # Clear and configure frames for the assets page
        self.top_Navigator.forget()
        self.Clear_Middle_Frame()
        
        # Create a navigation bar at the top of the assets page
        assets_Page_Navigator = Frame(self.Middle_Frame,height=65,width=1920,bg=self.SIDEBAR_COLOR)
        assets_Page_Navigator.grid(row=0,column=0)
        print_Assets = Label(assets_Page_Navigator,text="Income",fg="white",bg=self.SIDEBAR_COLOR,font=self.FONT_BIG)
        print_Assets.place(x=675,y=15)

        # Add a label to display "Assets" in the navigation bar
        self.Load_Image("Expense_Tracker_Photo/Black_Rectangle1.png",1425,130)
        assests_Page_Top_Frame_Rectangle = Label(self.Middle_Frame,image=self.img,bg=self.BG_COLOR)
        assests_Page_Top_Frame_Rectangle.image = self.img
        assests_Page_Top_Frame_Rectangle.place(x=15,y=75)
        
        # Display the "Net Assets" label in the top middle
        print_Total_Assets = Label(
            self.Middle_Frame,
            text=("Total Income"),
            bg=self.SIDEBAR_COLOR,
            font=self.FONT_MAIN,
            fg='#D7D7D7'
        )
        print_Total_Assets.place(x=660, y=100)
        
        # Create a frame to hold the total assets amount
        ttl_inc_frm = Frame(self.Middle_Frame, bg=self.SIDEBAR_COLOR, width=100,height=50)
        ttl_inc_frm.place(x=655,y=130)
        
        # Display the total assets amount
        ttl_inc_amt = Label(ttl_inc_frm, 
                            text=f"{self.Total_Assets:.2f}",
                            bg=self.SIDEBAR_COLOR,
                            fg='white',
                            font=("Arial",24,"bold")
                            )
        ttl_inc_amt.grid()
        
        # Load and display a larger decorative image in the middle of the page
        self.Load_Image("Expense_Tracker_Photo/Black_Rectangle2.png",1425,600)
        self.img_Frame = Label(self.Middle_Frame,image=self.img,bg=self.BG_COLOR)
        self.img_Frame.image = self.img
        self.img_Frame.place(x=15,y=220)
        
        # Add a label for "Asset Type" in the top-left corner
        assets_Types = Label(self.Middle_Frame, text="Asset Type",bg=self.SIDEBAR_COLOR,font=self.FONT_BIG,fg="white")
        assets_Types.place(x=45,y=240)
        
        # Create a frame for displaying account balances
        frame_Print_Acc_Balance = Frame(self.Middle_Frame,bg=self.SIDEBAR_COLOR,width=200,height=1080)
        frame_Print_Acc_Balance.place(x=550,y=275)
        
        # Loop to display account icons, types, and balances
        for i in range(0,4):
            # Load and display account icons
            self.Load_Image(self.P_Account_Icon_Path[i],50,50)
            account_Icon_Frame = Label(self.Middle_Frame,image=self.img,bg=self.SIDEBAR_COLOR)
            account_Icon_Frame.image = self.img
            account_Icon_Frame.place(x=50,y=300+(i*110))
            
            # Display account type names
            print_Account_Type = Label(self.Middle_Frame,text=self.account_Type[i],bg=self.SIDEBAR_COLOR,fg='white',font=self.FONT_BIG)
            print_Account_Type.place(x=175,y=310+(i*110))
            
            # Display "RM" currency label for account balances
            print_RM_Account_Balance = Label(self.Middle_Frame,text='RM',bg=self.SIDEBAR_COLOR,fg='white',font=self.FONT_BIG)
            print_RM_Account_Balance.place(x=525,y=310+(i*110))
            
            # Display the account balances
            print_Account_Balance = Label(frame_Print_Acc_Balance,text=f"{self.income_Amount[i]:.2f}",bg=self.SIDEBAR_COLOR,fg='white',font=self.FONT_BIG)
            print_Account_Balance.grid(row=i,column=0,pady=36,padx=50,sticky='e')

        income_category_not0 = []
        income_amount_not0 = []

        for i in range(len(self.income_Category)):
            key = self.account_Type[i]
            value = self.income_Amount_Dict.get(key)
            if value != None and value > 0:
                income_category_not0.append(key)
                income_amount_not0.append(value)

        # Create a pie chart to visualize account balances
        fig = Figure(figsize=(5, 5), dpi=110)
        fig.patch.set_facecolor(self.SIDEBAR_COLOR)  #Set the colour same with the background colour 
        ax = fig.add_subplot(111)
        ax.pie(income_amount_not0, labels=income_category_not0, autopct='%1.1f%%', startangle=90)
        
        # Customize text color and font size in the pie chart
        for text in ax.texts:
            text.set_color('white')
            text.set_fontsize(10)
        
        # Add the pie chart to the frame
        canvas = FigureCanvasTkAgg(fig, master=self.Middle_Frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=870,y=240)
        
        # Add a label for the pie chart
        print_Acc_Balance_Pie_Chart = Label(self.Middle_Frame, text="Balances",bg=self.SIDEBAR_COLOR,font=self.FONT_BIG,fg="white")
        print_Acc_Balance_Pie_Chart.place(x=1090,y=240)