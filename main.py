import mouse
import keyboard
import time
import tkinter as tk

app = tk.Tk()
app.geometry("400x400")
app.configure(bg='black')
app.title('MouseMacro')
app.columnconfigure(0)
app.columnconfigure(1)
app.rowconfigure(0)
app.rowconfigure(1, weight=1, minsize=50)
app.rowconfigure(2)
app.rowconfigure(3)
app.rowconfigure(4)
app.rowconfigure(5)

content = tk.Frame(app, bg="white", padx=50, pady=0)
content.pack()

# Variables
recording = False
looping = False
coordinate_list = []
speed_factor = 10
speed_factor_input = tk.StringVar()

# Functions
def start_recording():
    global recording
    print("recording started")
    set_recording_text(True)
    recording = True

def stop_recording():
    global recording
    print("recording stopped")
    recording = False

def check_for_stop():
    global recording
    global recording_text

    if recording == True:
        print("waiting for input")
        mouse.wait('left')
        print("unblocked")

        set_recording_text(False)

        recording = False
        coordinate_list.append(mouse.get_position())
    
    app.after(100, check_for_stop)

def toggle_loop():
    global looping

    if looping == True:
        looping = False
        set_looping_text(False)
    else:
        looping = True
        set_looping_text(True)

def set_recording_text(active):
    if active == True:
        recording_text.config(text="Recording")
    else:
        recording_text.config(text="")

def set_looping_text(active):
    if active == True:
        looping_text.config(text="Looping")
    else:
        looping_text.config(text="")

def play_recording():
    print("playing mouse sequence")
    global coordinate_list
    global looping

    if looping == True:
        while True:
            for coordinates in coordinate_list:
                xcor = coordinates[0]
                ycor = coordinates[1]
                mouse.move(xcor, ycor)
                mouse.click(button='left')
                time.sleep(1 / get_speed_factor())
            if keyboard.is_pressed('esc'):
                coordinate_list.clear()
                break
    else:
        for coordinates in coordinate_list:
            xcor = coordinates[0]
            ycor = coordinates[1]
            mouse.move(xcor, ycor)
            mouse.click(button='left')
            time.sleep(1 / get_speed_factor())
        coordinate_list.clear()

def get_speed_factor():
    global speed_factor_input
    global speed_factor

    speed_factor_val = speed_factor_input.get()

    if speed_factor_val.isdigit() == True:
        if int(speed_factor_val) > 0:
            speed_factor = int(speed_factor_input.get())

    return speed_factor

def quit_application():
    app.quit()

# Buttons
quit_button = tk.Button(content, bg="white", text="Quit", width=5, command=quit_application).grid(row=4, column=0, pady=20, columnspan=2)

# Text
title_text = tk.Label(content, bg="white", fg="black", font=("Lexend", 20, "normal"), text="Mouse Macro", relief="raised")
title_text.grid(row=0, column=0, pady=(20, 50), columnspan=2)

speed_factor_text = tk.Label(content, bg="white", fg="black", font=("Lexend", 10, "normal"), text="Speed Factor:")
speed_factor_text.grid(row=3, column=0)

recording_text = tk.Label(content, bg="white", fg="red", font=("Lexend", 10, "normal"), text="Recording")
recording_text.grid(row=1, column=0, pady=10, columnspan=2)
set_recording_text(False)

looping_text = tk.Label(content, bg="white", fg="green", font=("Lexend", 10, "normal"), text="Looping")
looping_text.grid(row=2, column=0, pady=10, columnspan=2)
set_looping_text(False)

# Entry Fields
speed_entry = tk.Entry(content, bg="white", textvariable=speed_factor_input, justify="center").grid(row=3, column=1)

if __name__ == "__main__":  
    print("MouseMacro enabled")

    keyboard.add_hotkey('ctrl+alt+r', start_recording)
    keyboard.add_hotkey('ctrl+alt+p', play_recording)
    keyboard.add_hotkey('ctrl+alt+l', toggle_loop)

check_for_stop()

app.mainloop()