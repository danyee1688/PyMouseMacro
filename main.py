import mouse
import keyboard
import time
import tkinter as tk

# Set root app configurations
app = tk.Tk()
app.geometry("310x420")
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
app.rowconfigure(6)
app.rowconfigure(7)
app.rowconfigure(8)
app.resizable(False, False)

# Pack frame to house UI components
content = tk.Frame(app, bg="white", padx=50, pady=50)
content.pack()

# Variables
recording = False
looping = False
coordinate_list = []
speed_factor = 10
speed_factor_input = tk.StringVar()

# ========================================================================================================================================= 
# FUNCTIONS
# ========================================================================================================================================= 

# Start recording by setting boolean to true
def start_recording():
    global recording
    set_recording_text(True)
    recording = True

# Stop recording by setting boolean to false
def stop_recording():
    global recording
    recording = False

# Check for whether or not to stop recording 
# Waits for left mouse button input
# Blocking
def check_for_stop():
    global recording
    global recording_text

    if recording == True:
        mouse.wait('left')

        set_recording_text(False)

        recording = False
        coordinate_list.append(mouse.get_position())
    
    app.after(100, check_for_stop)

# Toggles looping boolean and display text as necessary
def toggle_loop():
    global looping

    if looping == True:
        looping = False
        set_looping_text(False)
    else:
        looping = True
        set_looping_text(True)

# Hides or shows recording text based on argument
def set_recording_text(active):
    if active == True:
        recording_text.config(text="Recording")
    else:
        recording_text.config(text="")

# Hides or shows looping text based on argument
def set_looping_text(active):
    if active == True:
        looping_text.config(text="Looping")
    else:
        looping_text.config(text="")

# Plays the sequence of recorded clicks
def play_recording():
    global coordinate_list
    global looping

    # Checks to see if looping condition is met
    # If looping, the mouse continues to click in the recorded pattern
    # until stopped via the Escape key
    if looping == True:
        while True:
            move_mouse()
            if keyboard.is_pressed('esc'):
                coordinate_list.clear()
                break
    # Otherwise, only play recorded pattern once
    else:
        move_mouse()
        coordinate_list.clear()

# Move mouse according to coordinate list
# Mouse movement speed is adjusted by speed factor
def move_mouse():
    global coordinate_list

    for coordinates in coordinate_list:
        xcor = coordinates[0]
        ycor = coordinates[1]
        mouse.move(xcor, ycor)
        mouse.click(button='left')
        time.sleep(1 / get_speed_factor())

# Determine whether or not the value in the speed factor
# entry field is valid, and then returns the speed factor
def get_speed_factor():
    global speed_factor_input
    global speed_factor

    speed_factor_val = speed_factor_input.get()

    if speed_factor_val.isdigit() == True:
        if int(speed_factor_val) > 0:
            speed_factor = int(speed_factor_input.get())

    return speed_factor

# Quits the application
def quit_application():
    app.quit()

# ========================================================================================================================================= 
# WIDGETS
# ========================================================================================================================================= 

# Buttons
quit_button = tk.Button(content, bg="white", text="Quit", width=5, command=quit_application).grid(row=8, column=0, pady=(30, 20), columnspan=2)

# Text
title_text = tk.Label(content, bg="white", fg="black", font=("Lexend", 20, "normal"), text="Mouse Macro")
title_text.grid(row=0, column=0, pady=(0, 30), columnspan=2)

speed_factor_text = tk.Label(content, bg="white", fg="black", font=("Lexend", 10, "normal"), text="Speed Factor:")
speed_factor_text.grid(row=3, column=0)

recording_text = tk.Label(content, bg="white", fg="red", font=("Lexend", 10, "normal"), text="Recording")
recording_text.grid(row=1, column=0, columnspan=2)

looping_text = tk.Label(content, bg="white", fg="green", font=("Lexend", 10, "normal"), text="Looping")
looping_text.grid(row=2, column=0, columnspan=2)

controls_text_1 = tk.Label(content, bg="white", fg="black", font=("Lexend", 8, "normal"), text="CTRL+ALT+R to start recording")
controls_text_1.grid(row=4, column=0, columnspan=2)
controls_text_2 = tk.Label(content, bg="white", fg="black", font=("Lexend", 8, "normal"), text="CTRL+ALT+P to play recording")
controls_text_2.grid(row=5, column=0, columnspan=2)
controls_text_3 = tk.Label(content, bg="white", fg="black", font=("Lexend", 8, "normal"), text="CTRL+ALT+L to toggle looping")
controls_text_3.grid(row=6, column=0, columnspan=2)
controls_text_4 = tk.Label(content, bg="white", fg="black", font=("Lexend", 8, "normal"), text="Hold ESC to end loop")
controls_text_4.grid(row=7, column=0, columnspan=2)

# Entry Fields
speed_entry = tk.Entry(content, bg="white", textvariable=speed_factor_input, justify="left").grid(row=3, column=1, pady=20)

# ========================================================================================================================================= 
# FUNCTION CALLS
# ========================================================================================================================================= 

if __name__ == "__main__":  
    # Add hotkeys for corresponding action
    keyboard.add_hotkey('ctrl+alt+r', start_recording)
    keyboard.add_hotkey('ctrl+alt+p', play_recording)
    keyboard.add_hotkey('ctrl+alt+l', toggle_loop)

# Initial function calls
check_for_stop()

# Hide text
set_looping_text(False) 
set_recording_text(False)

app.mainloop()