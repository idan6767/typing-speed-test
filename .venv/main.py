import tkinter as tk
import requests
import random
from pygame import mixer

total_words = 0
total_characters = 0
user_words_list = []
game_is_on = "welcome_screen"
# Initialize the time remaining (in seconds)
time_remaining = 60
# Define initial_time
initial_time = 60


def play_sound(sound):
    mixer.init()
    mixer.music.load(sound)
    mixer.music.play()


def get_random_lyrics():
    artist = "Coldplay"
    title_list = ["Paradise", "Kaleidoscope", "Ink", "Adventure of a Lifetime", "Always in My Head", "Amazing Day", "Amsterdam"]
    api_url = f"https://api.lyrics.ovh/v1/{artist}/{random.choice(title_list)}"
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    if 'error' in data:
        return None
    else:
        text = text_cleaner(str(data['lyrics']))
        return text


def text_cleaner(text):
    splitted_text = text.split('\n')[1:]
    empty_line_filter = [line for line in splitted_text if line.strip()]
    result_string = '\n'.join(empty_line_filter)

    chars_to_remove = [",", ":", ";", "!", ".", "'", "?", '"', '\\n']

    for char in chars_to_remove:
        result_string = result_string.replace(char, '')
    text = result_string.lower()[:350]
    return text


text = get_random_lyrics()
text_list = text.split()


def block_typing(event):
    return "break"


# Window
window = tk.Tk()
window.title("Typing Speed Test")
window.minsize(300, 5)
window.config(padx=60, pady=60, bg="#31363F")
# Lock window size
window.resizable(False, False)
window.geometry("+50+20")

# Canvas
canvas = tk.Canvas
my_canvas = canvas(width=60, height=40, bg="black", highlightthickness=0)

# Labels
label = tk.Label
title_label = label(text="Typing Speed Test".capitalize(), bg="#31363F", fg="white", font=("arial", 22, "bold"))
subtitle_label = label(text="sample text".capitalize(), bg="#31363F", fg="white", font=("arial", 12, "bold"))
sample_text = tk.Text(window, bg="#31363F", width=50, height=16, fg="white", font=("arial", 14, "bold"))
sample_text.bind("<KeyPress>", block_typing)
user_text_label = label(text="insert text to test your typing speed".capitalize(), bg="#31363F", fg="white", font=("arial", 10, "bold"))
manual_text = label(text="How fast are your fingers?\n Do the one-minute typing test to find out!\n\n"
                         " Press the space bar after"
                         " each word.\n At the end, you'll get your typing speed\n in CPM and WPM.\n\nGood luck!".capitalize(),
                    bg="#31363F", fg="white", font=("arial", 13, "bold"))
final_score_title = label(text="final score".capitalize(), bg="#31363F", fg="white", font=("arial", 15, "bold"))
final_score = label(bg="#31363F", fg="white", font=("arial", 14, "bold"))

# Entry
user_text_entry = tk.Entry(width=15, bg="silver", fg="black", justify='center', font=("Arial", 20))


# Text Highlight
def highlight_word_by_word(text_widget):
    words = user_words_list
    start_index = "1.0"

    for word in words:
        end_index = f"{start_index}+{len(word)}c"
        text_widget.tag_add("highlight", start_index, end_index)  # Add a tag to highlight the word
        start_index = end_index + "+1c"


# Insert text into the Text widget
sample_text.tag_configure('left', justify='left')
sample_text.tag_add('left', '1.0', 'end')
sample_text.insert("1.0", text, "left")

# Configure a tag for highlighting
sample_text.tag_configure("highlight", background="green")


timer_label = tk.Label(window, text=f"Time Remaining: {time_remaining}", font=("Arial", 13), bg="#31363F", fg="white")
if game_is_on == True:
    final_score.configure(text=f"WPM Score: {total_words}   |   CPM Score: {total_characters}")


# countdown
def update_timer():
    global time_remaining
    global game_is_on
    if time_remaining > 0:
        time_remaining -= 1
        timer_label.config(text=f"Time Remaining: {time_remaining}")
        window.after(1000, update_timer)  # Schedule the update_timer function to run after 1 second (1000 milliseconds)
    else:
        timer_label.config(text="Time's up!")
        user_text_entry.config(state="disabled")
        game_is_on = False


def remove_highlights():
    sample_text.tag_remove("highlight", "1.0", "end")


def reset_timer():
    global time_remaining, game_is_on, total_words, total_characters, text_list
    play_sound("sound/start_game_sound.mp3")
    game_is_on = True
    random_lyrics = get_random_lyrics()
    text_list = random_lyrics.split()
    sample_text.insert("1.0", random_lyrics, 'left')
    final_score.configure(text=f"WPM Score: 0   |   CPM Score: 0")
    user_text_entry.config(state="normal")
    user_text_entry.delete(0, tk.END)
    time_remaining = initial_time
    timer_label.config(text=f"Time Remaining: {time_remaining}")
    user_words_list.clear()
    remove_highlights()
    total_words = 0
    total_characters = 0
    window.after(1500, update_timer)


# Buttons
reset_timer_button = tk.Button(text="Play Again?", command=reset_timer)
start_game_button = tk.Button(text="New Game!", command=reset_timer)


# check if "space" key has pressed
def key_pressed(event):
    global total_words, total_characters
    if event.keysym == 'space':
        print_input()
        final_score.configure(text=f"WPM Score: {total_words}   |   CPM Score: {total_characters}")


# print user text input
def print_input():
    input = user_text_entry.get()[:-1].lower()
    user_text_entry.delete(0, tk.END)

    if input == text_list[0]:
        play_sound("sound/click_sound.mp3")
        user_words_list.append(input)
        input_sum(len(user_words_list), len(input))
        text_list.pop(text_list.index(input))
        sample_text.config()
        highlight_word_by_word(sample_text)
    elif input != text_list[0]:
        play_sound("sound/error_sound.mp3")


# update words and characters sum
def input_sum(words, characters):
    global total_words, total_characters
    total_words = words
    total_characters += characters


window.bind("<Key>", key_pressed)

# Label Creation
lbl = tk.Label(window, text = "")

# configuring
title_label.config(padx=0, pady=20)
user_text_label.config(padx=0, pady=20)
timer_label.config(padx=0, pady=10)
start_game_button.config(padx=20, pady=10)
manual_text.config(padx=0, pady=25)
final_score.config(padx=0, pady=15)
final_score_title.config(padx=0, pady=20)

# Grid
title_label.grid(column=1, row=0)


def check_game_status():
    if time_remaining == 0 and game_is_on == True:
        play_sound("sound/finish_sound.mp3")
    if game_is_on == True:
        manual_text.grid_forget()
        start_game_button.grid_forget()
        reset_timer_button.grid_forget()
        final_score_title.grid_forget()
        subtitle_label.grid(column=1, row=2)
        sample_text.grid(column=1, row=3)
        user_text_label.grid(column=1, row=4)
        user_text_entry.grid(column=1, row=5)
        user_text_entry.focus_set()
        timer_label.grid(column=1, row=6)
        final_score.grid(column=1, row=8)
    elif game_is_on == False:
        timer_label.grid_forget()
        user_text_label.grid_forget()
        user_text_entry.grid_forget()
        final_score_title.grid(column=1, row=7)
        reset_timer_button.grid(column=1, row=9)
    elif game_is_on == "welcome_screen":
        manual_text.grid(column=1, row=1)
        start_game_button.grid(column=1, row=2)
    window.after(1000, check_game_status)


check_game_status()
window.mainloop()
