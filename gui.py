from tkinter import *
from customtkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
import familytree as ft
from pathlib import Path

set_appearance_mode("System")
set_default_color_theme("blue") 

app = CTk()
app.title('Family Tree Generator - Kshitij Khandelwal')
scrollable_frame_main = CTkScrollableFrame(app,width=app.winfo_screenwidth()-23,height=app.winfo_screenheight())
scrollable_frame_main.grid_columnconfigure((0,1,2), weight=1)
name= CTkLabel(master=scrollable_frame_main,text='Welcome to the Family Tree Generator',font=('Arial',60),corner_radius=10,fg_color='#0087f2',width=app.winfo_screenwidth()-23,height=100)
name.grid(row=0, column=0,pady=10,padx=10, sticky="ew",columnspan=2)

def gen_img():
    getfile=filedialog.askopenfilename(initialdir='shell:MyComputerFolder', title='Select a file', filetypes=(("excel files", "*.xlsx"),("excel files", "*.xls")))
    ft.CreateTree(getfile)
    desktop_path = Path.home() / "Desktop"
    img_path = desktop_path / "familytree.png"
    myimg=ImageTk.PhotoImage(file=img_path)
    my_label.configure(image=myimg)
    my_label.image = myimg

HowTo= CTkLabel(master=scrollable_frame_main,text='How to use:',font=('Arial',40),corner_radius=10,width=app.winfo_screenwidth())
HowTo.grid(column=0,row=1,padx=20,columnspan=2,sticky='ew')

scrollable_frame_secondary=CTkScrollableFrame(scrollable_frame_main,width=app.winfo_screenwidth()-30,height=360,fg_color='#444950',label_anchor='w')
scrollable_frame_secondary.grid_columnconfigure((0,1,2), weight=1)
scrollable_frame_secondary.grid(row=2,column=0,sticky='ew',columnspan=2,pady=10,padx=20)

method1_l1=CTkLabel(scrollable_frame_secondary,
                    text='It involves uploading an excel file with fields in a specified fields in the format as shown below:',
                    corner_radius=10,font=('Arial',20),anchor='w')
method1_img=CTkImage(Image.open("table.png"),size=(app.winfo_screenwidth()-200,200))
table_img=CTkLabel(master=scrollable_frame_secondary,image=method1_img,text='',corner_radius=100)
method1_l2=CTkLabel(scrollable_frame_secondary,
                    text=
                    '\u2022'+' ID: It is the combination of the first 2 characters of the first and last name of the family member.'+'\n'+
                    '\u2022'+' S: The sex(gender) of the member must be specified only using \"M\" (Male) or \"F\" (Female).'+'\n'+
                    '\u2022'+' DoB: This field contains the Date of Birth of the member in the format- DDMMYY'+'\n'+
                    '\u2022'+' DoD: This field contains the Date of Death of the member in the format- DDMMYY'+'\n'+
                    '\u2022'+' FatherID: Contains the ID of the father.'+'\n'+
                    '\u2022'+' MotherID: Contains the ID of the mother.'+'\n'+
                    '\u2022'+' SpouseID: It is the combination of the first 2 characters of both spouses. It must be the same for both spouses.'+'\n'+'\n'
                    'NOTE: Any fields that are not applicable to the particular member must be left empty.'+'\n'+'\n'+
                    'After the file has been created, click on the \"Select a file\" button and select the file from where it has been saved.',
                    corner_radius=10,font=('Arial',20),anchor='w',justify='left')

method1_l1.grid(column=0,row=1,padx=20,pady=10,columnspan=3,sticky='ew')
table_img.grid(row=2,column=0,columnspan=3)
method1_l2.grid(row=3,pady=10,padx=20,columnspan=3,sticky='ew')


selectButton = CTkButton(master=scrollable_frame_main, text='Select a file', command= gen_img,fg_color='#0087f2',font=('Arial',20),height=50,width=200,anchor='center')
selectButton.grid(row=3,column=0,padx=20,pady=5,columnspan=2)
my_label = CTkLabel(scrollable_frame_main,text='',corner_radius=10)
my_label.grid(columnspan=3,pady=20)

scrollable_frame_main.pack()


app.mainloop()