import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

class NotesOrganizer:
    def __init__(self, container):
        # Initialize constants and default values
        self.BG_COLOR = "#181818"
        self.SIDEBAR_COLOR = "#212121"
        self.ACTIVE_COLOUR = "#383838"
        self.FONT_MAIN = ("Arial",16,"bold")
        self.FONT_SUB = ("Arial",12,"bold")
        self.FONT_BUTTON = ("Arial",10,"bold")
        self.FONT_BIG = ("Arial", 20, "bold")
        self.File_Path = "Note.txt"
        self.Edit_File = False
        self.image_file_location = 'None'
        
        self.container = container

        # Perform initial setup
        self.Check_Note()
        self.Main_Menu()
 
    def Main_Menu(self):
        """Create the main menu layout."""
        self.Edit_File = False
        self.Clear_Frame()
        self.Load_Notepad()

        # Top navigation bar
        self.top_Navigator = tk.Frame(self.container, height=60, bg='#181818')
        self.top_Navigator.pack(side=tk.TOP, fill=tk.X)
        self.top_Navigator.pack_propagate(False)
        
        # Frame for the notes table
        self.tree_Frame = tk.Frame(self.container, height=600,width=1350, bg='white')
        self.tree_Frame.pack(pady=30)
        self.tree_Frame.pack_propagate(False)
        
        # Configure styles for the treeview
        self.style = ttk.Style()
        self.style.theme_use("default")

        # Add button to create a new note
        add_Note = tk.Button(self.top_Navigator, 
                             text='➕', 
                             bg='#181818', 
                             font=self.FONT_MAIN, 
                             fg='white', width=2, height=25, 
                             borderwidth=0, activebackground='#181818', 
                             activeforeground='white', 
                             command=lambda: self.Add_button_function())
        add_Note.pack(side=tk.RIGHT, pady=20,padx=50)
        
        # Main label for the application
        label = tk.Label(self.top_Navigator, text="Note Organizer", bg="#181818", fg="white", font=("Arial Rounded MT Bold", 14))
        label.pack(pady=20)
        
        # Configure treeview styles
        self.style.configure(
            "Custom.Treeview",
            background=self.SIDEBAR_COLOR,      
            fieldbackground=self.SIDEBAR_COLOR, 
            foreground="white",          
            font=('Arial', 13)
        )
        
        # Configure treeview heading styles
        self.style.configure(
            "Custom.Treeview.Heading",
            background=self.SIDEBAR_COLOR,   
            foreground='white',         
            font=('Arial', 14, 'bold'), 
        )
        
        # Create treeview widget
        self.tree = ttk.Treeview(
            self.tree_Frame,
            style="Custom.Treeview",
            columns=("Category", "Tag", "Text"),
            show = "headings"
        )
        
        # Define headings for the treeview
        self.tree.heading("Category", text="Category")
        self.tree.heading("Tag", text="Tag")
        self.tree.heading("Text", text="Text")
        
        # Configure column properties
        self.tree.column("Category", anchor=tk.CENTER, width=50)
        self.tree.column("Tag", anchor=tk.CENTER, width=200)
        self.tree.column("Text", anchor=tk.CENTER, width=500)
        self.tree.pack(expand=True, fill=tk.BOTH)
        
        # Load notes into the treeview
        self.Load_Into_Tree()
        
        # Create a right-click context menu for the treeview
        self.rg_Click_Menu = tk.Menu(self.container, tearoff=0)
        self.rg_Click_Menu.add_command(label="Edit", command=self.Open_Note)
        self.rg_Click_Menu.add_command(label="Delete", command=self.Delete_Note)
        
        # Bind right-click menu to the treeview
        self.tree.bind("<Button-3>", self.Right_Click_Menu)

    def Add_button_function(self):
        """Open the interface to add a new note."""
        self.Clear_Frame()
        open_new_window = self.container

        # Top sidebar frame for adding note options
        Top_sidebar_frame = tk.Frame(open_new_window, height=60, bg='#181818')
        Top_sidebar_frame.pack(side="top", fill="x")

        # Label for selecting a category
        category_label = tk.Label(
            Top_sidebar_frame, 
            text="Select Category:", 
            font=self.FONT_MAIN,
            bg='#181818', 
            fg='white')
        category_label.pack(side="left", padx=20, pady=10)

        # Dropdown menu for category selection
        category_type = tk.StringVar()
        self.category_dropdown = ttk.Combobox(
            Top_sidebar_frame, 
            textvariable=category_type,
            values=["Financial Plans", "Investment Opportunities", "Receipts"],
            state="readonly",  # Prevents manual text entry
            width=30,
            style="Custom.TCombobox"
            )
        self.category_dropdown.pack(side="left", padx=10, pady=10)

        # Button to insert an image
        def no_image_button_click():
            self.insert_picture()

        Picture_button = tk.Button(
            Top_sidebar_frame, 
            text="🖼️", 
            font=(40),
            bg='#181818', 
            fg='white', 
            borderwidth=0,
            activebackground='#202020',
            command=no_image_button_click
            )
        Picture_button.pack(side="right", pady=10, padx=10)

        # Save button to save the note
        save_buttonn = tk.Button(
            Top_sidebar_frame,
            text="💾",
            font=(40),
            bg="#181818",
            fg="white",
            borderwidth=0,
            activebackground="#202020",
            command=lambda: (self.save_note())
        )   
        save_buttonn.pack(side="right", pady=15, padx=30)
        
        # Label for entering tags
        tag_text_box_label = tk.Label(
            open_new_window,
            text="Tags: ",
            font=self.FONT_MAIN,
            bg="#0D0D0D",
            fg="white"
        )
        tag_text_box_label.pack(pady=10)

        # Text box for entering tags
        self.tag_text_box = tk.Text(
            open_new_window,
            height=3,
            width=123,
            bg="#292929", 
            fg="white",
            font=("Arial", 14),
            wrap=tk.WORD,
            borderwidth=2,
            relief=tk.SUNKEN, #Border style
            insertbackground='white' # Use to change the colour of the mouse to white
        )
        self.tag_text_box.pack(padx=10, pady=(5, 10))

        # Label for entering the note text
        note_text_box_label = tk.Label(
            open_new_window,
            text="Note: ",
            font=self.FONT_MAIN,
            bg="#0D0D0D",
            fg="white"
        )
        note_text_box_label.pack(pady=10)

        # Text box for entering the note content
        self.note_text_box = tk.Text(
            open_new_window,
            height=30,
            width=150,
            bg="#292929", 
            fg="white",
            font=("Arial", 14),
            wrap=tk.WORD,
            borderwidth=2,
            relief=tk.SUNKEN, #Border style
            insertbackground='white'
        )
        self.note_text_box.pack(padx=10, pady=(5, 10))

    def insert_picture(self):
        """Insert an image into the note."""
        file_Path = filedialog.askopenfilename(
            title='Select Image', 
            filetype=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        self.image_file_location = file_Path

        if not file_Path:
            return
        
        try:
            # Open the image
            img = Image.open(self.image_file_location)

            # Resize image if it's too large 
            max_width = 600
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)
            # Convert to photo image
            photo = ImageTk.PhotoImage(img)
            # Insert picture into note_text_box
            self.note_text_box.image_create(tk.END, image=photo)
            # Keep a reference to prevent garbage collection
            if not hasattr(self.note_text_box, 'images'):
                self.note_text_box.images = []
            self.note_text_box.images.append(photo)

            # Insert a newline after Image
            self.note_text_box.insert(tk.END, '\n')

        except Exception as e:
            messagebox.showerror("Error", f"Could not open image: {str(e)}")
    
    def save_note(self):
        """Save the current note to the file."""
        # Get category
        category = self.category_dropdown.get()
        # Get tags
        tags_content = self.tag_text_box.get(1.0, tk.END).strip()
        #Get the note content
        note_content = repr(self.note_text_box.get(1.0, tk.END).strip())
        if self.Edit_File == True:
            # Update existing note if in edit mode
            if note_content and tags_content and category:
                for i in range(len(self.tree_Data)):
                    if self.tree_Data[i][0] == self.values[0] and self.tree_Data[i][1] == self.values[1] and self.tree_Data[i][2] == self.values[2]:
                        self.tree_Data[i][0] = category
                        self.tree_Data[i][1] = tags_content
                        self.tree_Data[i][2] = note_content
                        if self.image_file_location != 'None':
                            self.tree_Data[i][3] = self.image_file_location
                        else:
                            self.tree_Data[i][3] = self.values[3]

                with open(self.File_Path, 'w') as file:
                    for i in range(len(self.tree_Data)):
                        data = (
                            f"Category| {self.tree_Data[i][0]}\nTags| {self.tree_Data[i][1]}\nText| {self.tree_Data[i][2]}\nimage_path| {self.tree_Data[i][3]}"
                        )
                        for item in data:
                            file.write(item)
                        file.write('\n\n')
                    messagebox.showinfo("Success","File saved successfully!")
                self.Edit_File = False
                self.Main_Menu()
            else:
                messagebox.showerror("Error", "The note is incomplete!")
        else:
            # Save a new note
            if note_content and tags_content and category:
                data={
                    f"Category| {category}\nTags| {tags_content}\nText| {note_content}\nimage_path| {self.image_file_location}" 
                }
                with open(self.File_Path, 'a') as file:
                    for item in data:
                        file.write(item)
                    file.write('\n\n')
                    file.close()
                messagebox.showinfo("Success","File saved successfully!")
                self.Edit_File = False
                self.Main_Menu()
            else:
                messagebox.showerror("Error", "The note is incomplete!")

    def Open_Note(self):
        """Open a selected note for editing."""
        self.Edit_File = True
        # Get the selected item from the tree view
        self.selected_Data = self.tree.selection()
        self.values = self.tree.item(self.selected_Data, "values")
        self.Load_Notepad()
        self.Add_button_function()
        
        data=[' ', ' ', ' ', None]
        # Read the file and parse its content to load the selected note
        with open(self.File_Path) as file:
            for line in file:
                var1 = line.split("| ")
                if len(var1) == 2:
                    key = var1[0].strip()
                    value = var1[1].strip()
                    if key == "Category":
                        data[0] = value
                    elif key == "Tags":
                        data[1] = value
                    elif key == "Text":
                        data[2] = value
                    elif key == 'image_path':
                        # Match image path with the selected tree view item
                        if data[0]== self.values[0] and data[1] == self.values[1] and data[2] == self.values[2]:
                            data[3] = value
                        
            self.note_text_box.delete(1.0, tk.END)
            # Load image if associated with the note
            if data[3] != 'None':
                img = Image.open(data[3])
                
                # Resize image if it exceeds the maximum width
                max_width = 600
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.LANCZOS)
                
                photo = ImageTk.PhotoImage(img)
                # Insert the image into the note text box
                self.note_text_box.image_create(tk.END, image=photo)
                
                # Keep references to prevent garbage collection
                if not hasattr(self.note_text_box, 'images'):
                    self.note_text_box.images = []
                self.note_text_box.images.append(photo)
                self.note_text_box.insert(tk.END, '\n')
            
            # Load category, tags, and text content into their respective widgets
            self.category_dropdown.set(self.values[0])
            self.tag_text_box.delete(1.0, tk.END)
            self.tag_text_box.insert(tk.END, self.values[1])
            self.note_text_box.insert(tk.END, eval(self.values[2])) 

    def Clear_Frame(self):
        """Clear all widgets in the main container."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def Mouse_Scroll(self,event):
        """Enable mouse scrolling for the tree view."""
        self.tree.yview_scroll((event.delta // 120), "units")
        
    def Load_Notepad(self):
        """Load notes from the file into memory."""
        i = 0
        self.tree_Data=[]
        data=[' ', ' ', ' ', ' ']
        # Read and parse file data
        with open(self.File_Path) as file:
            for line in file:
                var1 = line.split("| ")
                if len(var1) == 2:
                    key = var1[0].strip()
                    value = var1[1].strip()
                    if key == "Category":
                        data[0] = value
                        i += 1
                    elif key == "Tags":
                        data[1] = value
                        i += 1
                    elif key == "Text":
                        data[2] = value
                        i += 1
                    elif key == "image_path":
                        data[3] = value
                        i += 1
                if i == 4:
                    self.tree_Data.append(data)
                    data = ['']*4
                    i = 0
    
    def Load_Into_Tree(self):
        """Populate the tree view with loaded notes."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i in range(len(self.tree_Data)):
            self.tree.insert('', tk.END, values=(self.tree_Data[i][0], self.tree_Data[i][1], self.tree_Data[i][2]))
    
    def Right_Click_Menu(self, event):
        """Display a context menu on right-click in the tree view."""
        row_Id = self.tree.identify_row(event.y)
        if row_Id:
            self.tree.selection_set(row_Id)
            self.rg_Click_Menu.post(event.x_root, event.y_root)
            

    def Check_Note(self):
        """Check if the note file exists, and initialize it if empty."""
        if not os.path.exists(self.File_Path):
            with open(self.File_Path, 'w') as file:
                file.write(" ")
    
    def Delete_Note(self):
        """Delete the selected note from the tree view and file."""
        selected_Data = self.tree.selection()
        self.tree.delete(selected_Data)
        self.Update_Note()
        
    def Update_Note(self):
        """Update the note file with the current tree view data."""
        rows = self.tree.get_children()
        data = []
        for row in rows:
            data.append(self.tree.item(row, "values"))
        
        with open(self.File_Path, 'w') as file:
            for tree_item in self.tree_Data:
                tree_category, tree_tag, tree_text, image_path = tree_item
                
                exists_in_data = any(
                    tree_category == d[0] and tree_tag == d[1] and tree_text == d[2]
                    for d in data
                )
                if exists_in_data:
                    file_data = (
                        f"Category| {tree_category}\n"
                        f"Tags| {tree_tag}\n"
                        f"Text| {tree_text}\n"
                        f"image_path| {image_path}\n\n"
                    )
                    file.write(file_data)

def note():
    """Run the Notes Organizer application."""
    app = NotesOrganizer()
    app.run()
