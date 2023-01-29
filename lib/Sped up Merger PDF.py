import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from pypdf import PdfMerger
from tkinter import *
root = tk.Tk()
root.geometry("1100x603")


selected_pdfs = tk.Label(root,text='0 Selected PDFs')
pdfs=[]
merger = PdfMerger()
listbox = tk.Listbox(root)
listbox.grid(column=3,row=1)
List_box = tk.Listbox(width=90)
List_box.grid(column=4, row=1,columnspan=2)
def move_up():
    global pdfs
    selected_item = listbox.curselection()
    if selected_item:
        if selected_item[0] > 0:
            item = listbox.get(selected_item)
            index = selected_item[0]
            print(index)
            listbox.delete(selected_item)
            listbox.insert(index - 1, item)
            listbox.activate(index - 1)
            listbox.selection_clear(0, END)
            listbox.activate(index - 1)
            listbox.selection_set(index - 1, last=None)
            removed_item = pdfs.pop(index-1)
            print(removed_item)
            pdfs.insert(index, removed_item)

            for i in range(listbox.size()):
                List_box.delete(0)
            for path in pdfs:
                List_box.insert(END, path)

def move_down():
    global pdfs
    selected_item = listbox.curselection()
    if selected_item:
        if selected_item[0] < listbox.size() - 1:
            item = listbox.get(selected_item)
            index = selected_item[0]
            listbox.delete(selected_item)
            listbox.insert(index + 1, item)
            listbox.activate(index + 1)
            listbox.selection_clear(0, END)
            listbox.activate(index + 1)
            listbox.selection_set(index + 1, last=None)
            removed_item = pdfs[index]
            pdfs.pop(index)
            pdfs.insert(index+1, removed_item)
            for i in range(listbox.size()):
                        List_box.delete(0)
            for path in pdfs:
                List_box.insert(END, path)
move_up_button = tk.Button(root, text="Move Up", command=move_up,width=15,height=2)
move_up_button.grid(column=3,row=3)
move_down_button = tk.Button(root, text="Move Down", command=move_down,width=15,height=2)
move_down_button.grid(column=3,row=4)
def error():
    messagebox.showinfo(title="error", message="You have selected PDFs")
def select_pdfs():
    selection_reset()
    global pdfs,order
    if len(pdfs)!=0:
        pdfs.clear()
    order=""
    pdfs = filedialog.askopenfilenames(title="Select PDFs to merge", filetypes=[("PDF files", "*.pdf")])
    pdfs = list(pdfs)
    if not pdfs:
        return
    for path in pdfs:
        file_name = path.split("/")[-1]
        order += f"{file_name}\n"
        listbox.insert(END, file_name)
        List_box.insert(END,path)
    selected_pdfs.config(text=f"{len(pdfs)} selected PDFs",bg="#40E0D0")
    select_pdf_button.config(text="PDFs selected",bg="green")

    add_button.grid(column=1, row=3)

    merge_button.grid(column=4, row=3)

    reset_button.grid(column=1, row=5)
def save():
    print(pdfs)
    for pdf in pdfs:
        merger.append(pdf)
    save_location = filedialog.asksaveasfilename(title="Save merged PDF as", defaultextension=".pdf")
    if not save_location:
        return
    merger.write(save_location)
    messagebox.showinfo(title="Sucess", message=f"Your PDF Files have succesfully merged into{save_location}")
def show_order():
    print(pdfs)
    messagebox.showinfo(title="order",message="\n".join(pdfs))
def reset():
    global pdfs, order,merge_button,add_button,reset_button
    pdfs.clear()
    order = ""
    listbox.delete(0, END)
    selected_pdfs.config(text="0 Selected PDFs")
    select_pdf_button.config(text="Select PDFs", bg="white")
    for i in range(List_box.size()):
        List_box.delete(0)
    add_button.grid_remove()
    merge_button.grid_remove()
    reset_button.grid_remove()
def selection_reset():
    global pdfs, order
    pdfs.clear()
    order = ""
    listbox.delete(0, END)
    selected_pdfs.config(text="0 Selected PDFs")
    select_pdf_button.config(text="Select PDFs", bg="white")
    for i in range(List_box.size()):
        List_box.delete(0)
def delete_pdf():
    global pdfs
    selected_item = listbox.curselection()
    if selected_item:
        index = selected_item[0]
        listbox.delete(selected_item)
        pdfs.pop(index)
        for i in range(List_box.size()):
            List_box.delete(0)
        for path in pdfs:
            List_box.insert(END, path)
        selected_pdfs.config(text=f"{len(pdfs)} selected PDFs",bg="#40E0D0")
        file_label.config(text=f'This is the path to the {len(pdfs)} selected PDF files')
    else:
        messagebox.showinfo(title="error", message="You must first select a pdf to delete")
def add_pdf():
    global pdfs,order
    pdfs_to_add = filedialog.askopenfilenames(title="Select PDFs to merge", filetypes=[("PDF files", "*.pdf")])
    pdfs_added = list(pdfs_to_add)
    for i in pdfs_added:
        pdfs.append(i)
        print(i)
    for path in pdfs_added:
        file_name = path.split("/")[-1]
        order += f"{file_name}\n"
        listbox.insert(END, file_name)
        List_box.insert(END,path)
    selected_pdfs.config(text=f"{len(pdfs)} selected PDFs", bg="#40E0D0")
root.title("Merge PDFs")
select_pdf_button = tk.Button(root, text="Select PDFs", height= 2, width=15,bg="red", command=select_pdfs)
merge_button = tk.Button(root, text="Merge PDF Files", height=2, width=15, command=save, bg="green")
reset_button = tk.Button(root, text="Reset", command=reset, height=2, width=15, bg="red")
select_pdf_button.grid(column=1, row=1)
selected_pdfs.grid(column=2,row=1)

add_button = tk.Button(root, text="Add PDF Files", height=2, width=15, command=add_pdf)
delete_pdf_button = tk.Button(root, text="Delete Selected PDF",height=2, width=15, command=delete_pdf)
delete_pdf_button.grid(column=1,row=2)
myfont = ("Helvetica", 16)
move_up_label = tk.Label(root, text="MOVE Up-Moves the selected PDF up in the list.", font=myfont)
move_up_label.grid(column=4, row=12)

move_down_label = tk.Label(root, text="MOVE Down-Moves the selected PDF down in the list.", font=myfont)
move_down_label.grid(column=4, row=13)

select_pdf_label = tk.Label(root, text="Select - Selects  the PDF files you want to merge.", font=myfont)
select_pdf_label.grid(column=4, row=9)

delete_pdf_label = tk.Label(root, text="Delete Selected PDF - Deletes the selected PDF from the list.", font=myfont)
delete_pdf_label.grid(column=4, row=10)

delete_pdf_label = tk.Label(root, text="Add PDF - Adds PDF files to the current list.", font=myfont)
delete_pdf_label.grid(column=4, row=11)

merge_pdf_label = tk.Label(root, text="Merge-Merges the selected PDFs into one PDF.", font=myfont)
merge_pdf_label.grid(column=4, row=12)

file_label = tk.Label(root,text="This is the path to the selected PDF files",font=myfont)
file_label.grid(column=4,row=2)

order_label = tk.Label(root, text="PDF order(Starts from the top)",font=myfont)
order_label.grid(column=3,row=2)
root.mainloop()
