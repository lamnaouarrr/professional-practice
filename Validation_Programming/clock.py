import time
from datetime import datetime
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance

#function to update the time and date
def update_date_time():
    currDate = datetime.now().strftime('%Y-%m-%d')
    currTime = time.strftime('%H:%M:%S')
    date_label.config(text=currDate)
    time_label.config(text=currTime)
    root.after(1000, update_date_time)

#create the main application window
root = tk.Tk()
root.title("CyberPunk Clock made by LAMNAOUAR Ayoub")
root.geometry("500x250")
root.resizable(False, False)

#load the custom icon
icon_path = 'C:/Users/ayoub/Desktop/CST Bachelor\'s degree at WIT/semester 6/professional practice/professional-practice-codes/Validation_Programming/hourglass-outline.png'
icon_image = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(True, icon_photo)

#create a canvas widget
canvas = tk.Canvas(root, width=500, height=250)
canvas.pack(fill="both", expand=True)

#load the background image
bg_image = Image.open('C:/Users/ayoub/Desktop/CST Bachelor\'s degree at WIT/semester 6/professional practice/professional-practice-codes/Validation_Programming/hourglass-cyberpunk.png')
bg_image = bg_image.resize((500, 250), Image.LANCZOS)  # Resize to match the canvas size

#create a darker version of the image
enhancer = ImageEnhance.Brightness(bg_image)
dark_bg_image = enhancer.enhance(0.5)  # Adjust the brightness level to make it darker
bg_photo = ImageTk.PhotoImage(dark_bg_image)

#place the image on the canvas
canvas.create_image(0, 0, image=bg_photo, anchor='nw')

#create a label to display the current date and place it on the canvas
date_label = tk.Label(canvas, text="", font=('Courier New', 20, 'bold'), fg='#45F08C', bg='#0f0f0f', padx=10, pady=5, bd=2, relief="solid", highlightbackground='#F21DDD', highlightcolor='#F21DDD', highlightthickness=2)
canvas.create_window(250, 70, window=date_label, anchor='center')

#create a label to display the current time and place it on the canvas
time_label = tk.Label(canvas, text="", font=('Courier New', 40, 'bold'), fg='cyan', bg='#0f0f0f', padx=10, pady=5, bd=2, relief="solid", highlightbackground='#F21DDD', highlightcolor='#F21DDD', highlightthickness=2)
canvas.create_window(250, 150, window=time_label, anchor='center')

#call the update function once to start the loop
update_date_time()

#run the main event loop
root.mainloop()
