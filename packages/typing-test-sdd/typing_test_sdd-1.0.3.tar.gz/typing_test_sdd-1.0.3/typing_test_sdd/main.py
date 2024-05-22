# Basic Import Functions
import tkinter as tk
import customtkinter as ctk
import PIL.Image
import random
from pathlib import Path
import json
from os import path


# Initialize a variable to store the ID of the scheduled update
timer_update_id = None


# Defining Commands - Making Main Frame, All Widgets in 2nd Window, Each widget placed here will be represened in the main window
def create_typing():
    global current_word_label, container, typing_container, text_container, current_text, typing_box, container, timer_label, test_time, len_time, wpm_label, Textspeech, check_var, Back, Restart_button, timer_label, is_on_main_window, is_on_typing_window, scale
    is_on_main_window = False
    is_on_typing_window = True
    
    # Clearing Frame
    for widget in main_window.winfo_children():  # Emptying out frame
        widget.place_forget()
    main_window.pack_forget()

    root.geometry("1400x700")
    container = ctk.CTkFrame(root)
    container.pack(expand=True, fill="both")
    
    typing_container = ctk.CTkFrame(container)
    typing_container.place(
        relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="c"
    )
    main_image = PIL.Image.open(Path(__file__).resolve().parents[0] / path.join("Assets", "main_image.png"))
    dummy_widget1 = ctk.CTkLabel(
        typing_container,
        text="",
        image=ctk.CTkImage(main_image, size=(1400, 700)),
    )
    dummy_widget1.pack()
    text_container = ctk.CTkFrame(
        typing_container, border_width=5, border_color="#767272"
    )
    text_container.place(
        relx=0.5, rely=0.05, relwidth=0.9, relheight=0.45, anchor="n"
    )
    settings_container = ctk.CTkFrame(    
        typing_container, border_width=5, border_color="#767272", height=280
    )
    settings_container.place(relx=0.87, rely=0.75, anchor="c")
    # Label for the WPM counter
    wpm_label = ctk.CTkLabel(
        typing_container,
        text="WPM: ",
        corner_radius=100,
        fg_color="grey",
        text_color="black",
    )
    wpm_label.place(in_=typing_container, relx=0.1, rely=0.07)

    Back = ctk.CTkButton(
        container,
        text="← Go Back (Esc)",
        command=go_back,
        corner_radius=100,
        fg_color="white",
        text_color="black",
    )
    Back.place(relx=0.1)

    current_word_label = ctk.CTkLabel(
        text_container,
        text=" ".join(sampled_words[0:3]),
        font=ctk.CTkFont(size=40),
    )
    current_word_label.place(relx=0.5, rely=0.5, anchor="c")

    timer_label = ctk.CTkLabel(
        text_container, text=f"Time left: {timer_seconds} seconds"
    )
    timer_label.place(relx=0.5, rely=0.7, anchor="c")

    current_text = ""
    typing_box = ctk.CTkEntry(
        typing_container,
        placeholder_text="   Click Box To Begin",
        font=ctk.CTkFont(size=20),
    )
    typing_box.bind("<KeyRelease>", on_key_press)
    typing_box.place(
        relx=0.5, rely=0.91, anchor="c", relheigh=0.1, relwidth=0.3
    )
    typing_box.focus()

    # Options for Length of Time the Test is for
    len_time = ctk.CTkOptionMenu(
        settings_container,
        values=["10", "30", "60"],
        command=test_time,
        button_color="black",
        fg_color="grey",
    )
    len_time.grid(column=0, row=1, pady=6, padx=10)
    len_time.configure(state="disable")
    len_time_label = ctk.CTkLabel(
        settings_container,
        text="Seconds",
        corner_radius=100,
        fg_color="grey",
        text_color="black",
    )
    len_time_label.grid(column=0, row=0, pady=8, padx=10)

    modes = ctk.CTkOptionMenu(
        settings_container,
        values=["dark", "light", "system"],
        command=ctk.set_appearance_mode,
        button_color="black",
        fg_color="grey",
    )
    modes.grid(column=0, row=3, pady=6, padx=10)
    modes_label = ctk.CTkLabel(
        settings_container,
        text="Modes",
        corner_radius=100,
        fg_color="grey",
        text_color="black",
    )
    modes_label.grid(column=0, row=2, pady=6, padx=10)
    modes.set("system")
    modes.set(ctk.get_appearance_mode())

    scale = ctk.CTkOptionMenu(
        settings_container,
        values=["0.75", "1.0", "1.25"],
        command=scaling,
        button_color="black",
        fg_color="grey",
    )
    scale.grid(column=0, row=5, pady=8, padx=10)
    scale_label = ctk.CTkLabel(
        settings_container,
        text="UI Scale",
        corner_radius=100,
        fg_color="grey",
        text_color="black",
    )
    scale_label.grid(column=0, row=4, pady=6, padx=10)
    scale.set(current_scaling)
    

  
    Restart_button = ctk.CTkButton(
        typing_container,
        text="Restart (Enter)",
        command=restart,
        fg_color="grey",
        text_color="black",
    )
    Restart_button.place(relx=0.5, rely=0.80, anchor="c")


def test_time(value):
    global timer_seconds
    timer_label.configure(text=f"Time left: {str(value)} seconds")
    timer_seconds = int(value)


def scaling(value):
    global current_scaling
    current_scaling = value
    ctk.set_widget_scaling(float(value))


# Function that commands the Go Back Button
def go_back():
    container.pack_forget()  # Forget the current window
    root.geometry("1400x700")  # Adjust window size
    make_main_window()  # Have to remake content who knows why!!!
    place_main_window_content()


# Function that commands when the first word is written right
def on_key_press(e):
    global score, sampled_words
    current_text = typing_box.get()
    if current_text.strip() == sampled_words[0]:
        sampled_words.pop(0)
        update_current_word()
        typing_box.configure(
            placeholder_text=" ".join(sampled_words[0:3])
        )  # More than 1 word on the screen
        typing_box.delete(0, ctk.END)
        score += 1
        if timer_seconds > 0:
            update_timer()


# Command for the restart button that occurs when time is up
def restart():
    global score, timer_seconds, timer_choice, len_time, root
    score = 0
    timer_seconds = int(len_time.get())
    timer_label.configure(text=f"Time left: {timer_seconds} seconds")
    typing_box.configure(state="normal")
    typing_box.delete(0, ctk.END)
    if timer_update_id:
        root.after_cancel(timer_update_id)


# Updated word as the word is spelt right
def update_current_word():
    current_word_label.configure(text=" ".join(sampled_words[0:3]))


# Receives word from JSON File "Words"
def get_words():
    global sampled_words
    with open(Path(__file__).resolve().parents[0] / "words.json") as file:
        words = json.load(file)
        sampled_words = random.sample(words, 100)


# Countdown Timer
def update_timer():
    global timer_seconds, timer_update_id, score, Restart_button
    if timer_seconds > 0:
        timer_seconds -= 1
        timer_label.configure(text=f"Time left: {timer_seconds} seconds")
        # Cancel the previous scheduled update
        if timer_update_id:
            root.after_cancel(timer_update_id)
        # Schedule the next update
        timer_update_id = root.after(1000, update_timer)
    else:
        timer_label.configure(text="Time's up!")
        value = int(len_time.get())
        if value == 10:
            wpm_label.configure(text=f"WPM: {score * 6} ")

        elif value == 30:
            wpm_label.configure(text=f"WPM: {score * 2} ")
        else:
            wpm_label.configure(text=f"WPM: {score} ")
        typing_box.configure(state="disable")


def invoke_begin():
    Begin_TTH.invoke()


# Starts timer
def start_timer(duration):
    global timer_seconds
    timer_seconds = duration
    update_timer()


# Command that remakes the main window content after the Back Button is pressed
def place_main_window_content():
    main_window.pack(expand=True, fill="both")
    dummy_widget.pack()
    Welcome_TTH.place(relx=0.5, rely=0.2, anchor="c")
    Begin_TTH.place(relx=0.5, rely=0.4, anchor="c")
    EndProgram.place(relx=0.5, rely=0.6, anchor="c")
    Credits.place(relx=0.5, rely=0.5, anchor="c")


# Credits Function
def credits():
    tk.messagebox.showinfo("Credits", "Made by Gaurav 12SDD2")


# Main Window Content - Frame Buttons labels etc
def make_main_window():
    # Pop Up-Window - Begin Touch Type Helper
    global root, main_window, Welcome_TTH, Begin_TTH, Credits, dummy_widget, EndProgram, is_on_main_window, is_on_typing_window
    is_on_main_window = True
    is_on_typing_window = False
    
    # main_window
    main_window = ctk.CTkFrame(
        root, width=400, height=500, border_width=10
    )  # border_color = "#13141F") )

    dummy_widget = ctk.CTkLabel(
        main_window,
        text="",
        image=ctk.CTkImage(
            PIL.Image.open(
                Path(__file__).resolve().parents[0] / path.join("Assets", "polka.png")
            ),
            size=(1400, 700),
        ),
    )

    # Labels Used
    Welcome_TTH = ctk.CTkLabel(
        main_window,
        text="Welcome to the Touch Type Helper",
        font=("Work Sans", 24),
        fg_color="#272626",
        text_color= "white",
        corner_radius=1,
    )

    # Buttons
    Begin_TTH = ctk.CTkButton(
        main_window,
        text="Begin (⇧ + ↵)",
        font=("Arial", 16),
        fg_color="#272626",
        command=create_typing,
    )

    EndProgram = ctk.CTkButton(
        main_window,
        text="End Program (⇧ + Esc)",
        font=("Arial", 16),
        fg_color="#272626",
        command=root.destroy,
    )

    Credits = ctk.CTkButton(
        main_window,
        text="Credits",
        font=("Arial", 16),
        fg_color="#272626",
        command=credits,
    )



def keybind(button, action):
    global is_on_main_window, is_on_typing_window
    if action in actions[0:2] and is_on_main_window:
        button.invoke()
    elif action in actions[2:4] and is_on_typing_window:
        button.invoke()

def start_app():
    try:
        global current_scaling, timer_seconds, score, root, timer_choice, is_on_main_window, is_on_typing_window, scale, actions 
        get_words()
        timer_seconds = 10
        score = 0  # Keeps score on how many words are right
        is_on_main_window = False
        is_on_typing_window = False
        actions = ["to_typing_window", "do_exit", "do_restart", "to_main_window"]
        current_scaling = "1.0"

        root = ctk.CTk()
        root.geometry("1400x700")
        root.title("Touch Typing Helper - Gaurav Surve")
        make_main_window()
        place_main_window_content()
        root.bind("<Shift-Return>", lambda e: keybind(Begin_TTH, actions[0]))
        root.bind("<Shift-Escape>", lambda e: keybind(EndProgram, actions[1]))
        root.bind("<Return>", lambda e: keybind(Restart_button, actions[2]))
        root.bind("<Escape>", lambda e: keybind(Back, actions[3]))
        root.mainloop()

    except Exception as ex:
        with open ("test.txt", "x") as f:
            f.write(f"{type(ex).__name__} {ex}")

# Main variables for when program is started
if __name__ == "__main__":
    start_app()
