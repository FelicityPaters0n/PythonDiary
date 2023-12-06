import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkcalendar import Calendar
import csv
from datetime import datetime


dark_bg_color = "#31304D"
light_text_color = "#F0ECE5"
accent_color = "#B6BBC4"  
input_bg_color = "#ffffff"  
input_fg_color = "#31304D"  
button_bg_color = "#31304D"  
button_fg_color = "#F0ECE5"
cal_greyed_out_colour = "#595959"
window_width = 800
window_height = 850

app = tk.Tk()
app.title("Digital Diary")
csvPath = "./data.csv"

style = ttk.Style()
style.theme_use('clam')
style.configure("Custom.TEntry", background=input_bg_color, foreground=input_fg_color, fieldbackground=input_bg_color, borderwidth=2)
style.configure("Custom.TCombobox", fieldbackground=input_bg_color, background=input_fg_color, foreground=input_fg_color)
style.configure("Custom.TButton", background=button_bg_color, foreground=button_fg_color, font=("Arial", 12))
style.map("Custom.TButton",
    background=[("active", "#B6BBC4")],  
    foreground=[("active", "#c7ffdc")]  
)
style.configure("TLabel",background =dark_bg_color, foreground=light_text_color, font=("Arial", 12))
canvas = tk.Canvas(app, bg=dark_bg_color)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(app, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

frame = ttk.Frame(canvas, style="TFrame")
style.configure("TFrame", background=dark_bg_color)

frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

def on_date_select(event=None):
    date = cal.selection_get() if event else datetime.today()
    formatted_date = date.strftime("%d %B, %Y") 
    selected_date_label.config(text=formatted_date)
    entry = data.get(date.strftime("%Y-%m-%d"))

    if entry:
        mood_entry.set(entry['Mood'])
        thoughts_entry.delete("1.0", tk.END)
        thoughts_entry.insert(tk.END, entry['Thoughts'])
        learning_entry.set(entry['Learning'])
        physical_activity_entry.set(entry['PhysicalActivity'])
        favorite_media_entry.delete(0, tk.END)
        favorite_media_entry.insert(0, entry['FavoriteMedia'])
        media_type_entry.set(entry.get('MediaType', ''))
        friend_of_the_day_entry.delete(0, tk.END)
        friend_of_the_day_entry.insert(0, entry['FriendOfTheDay'])
        food_healthiness_entry.set(entry['FoodHealthiness'])
        spend_entry.delete(0, tk.END)
        spend_entry.insert(0, entry['Spend'])
        grateful_for_entry.delete(0, tk.END)
        grateful_for_entry.insert(0, entry['GratefulFor'])
        sleep_entry.set(entry['Sleep'])
    else:
        # Clear all fields if no entry for the selected date
        mood_entry.set('')
        thoughts_entry.delete("1.0", tk.END)
        learning_entry.set('')
        physical_activity_entry.set('')
        favorite_media_entry.delete(0, tk.END)
        media_type_entry.set('')
        friend_of_the_day_entry.delete(0, tk.END)
        food_healthiness_entry.set('')
        spend_entry.delete(0, tk.END)
        grateful_for_entry.delete(0, tk.END)
        sleep_entry.set('')


def save_data():
    date = cal.selection_get()
    if not date:
        messagebox.showerror("No Date Selected", "Please select a date.")
        return
    entry = {
        'Date': date.strftime("%Y-%m-%d"),
        'Mood': mood_entry.get(),
        'Thoughts': thoughts_entry.get("1.0", tk.END).strip(),  
        'Learning': learning_entry.get(),
        'PhysicalActivity': physical_activity_entry.get(),
        'FavoriteMedia': favorite_media_entry.get(),
        'MediaType': media_type_entry.get(),  
        'FriendOfTheDay': friend_of_the_day_entry.get(),
        'FoodHealthiness': food_healthiness_entry.get(),
        'Spend': spend_entry.get(),
        'GratefulFor': grateful_for_entry.get(),
        'Sleep': sleep_entry.get()
    }
    data[date.strftime("%Y-%m-%d")] = entry
    save_to_file()


def load_data():
    try:
        with open(csvPath, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data[row['Date']] = row
    except FileNotFoundError:
        pass


def save_to_file():
    with open(csvPath, 'w', newline='') as file:
        fieldnames = ['Date', 'Mood', 'Thoughts', 'Learning', 'PhysicalActivity', 'FavoriteMedia', 'MediaType', 'FriendOfTheDay', 'FoodHealthiness', 'Spend', 'GratefulFor', 'Sleep']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data.values():
            writer.writerow(entry)


def set_to_today():
    today = datetime.today().date()
    cal.selection_set(today)
    on_date_select() 

def create_label_entry(parent, label, entry_class=ttk.Entry, style="Custom.TEntry", **entry_kwargs):
    frame = ttk.Frame(parent, style="TFrame")
    frame.pack(fill="x", padx=10, pady=2)

    label_widget = ttk.Label(frame, text=label, style="Custom.TLabel")
    label_widget.pack(side=tk.LEFT, padx=(10, 5), anchor="w")

    if entry_class == scrolledtext.ScrolledText:
        entry = entry_class(frame, font=("Arial", 12), bg=input_bg_color, fg=input_fg_color, insertbackground=input_fg_color)
    else:
        entry = entry_class(frame, style=style, **entry_kwargs)

    entry.pack(side=tk.RIGHT, padx=(5, 10),pady=(3), fill="both", expand=True)
    return entry




data = {}
load_data()
app.configure(bg=dark_bg_color)

# Calendar
calendar_font = ("Arial", 20) 
cal = Calendar(frame, selectmode='day', background=dark_bg_color, foreground=light_text_color, headersbackground=dark_bg_color, selectbackground=accent_color, normalbackground=dark_bg_color, weekendbackground=dark_bg_color, othermonthwebackground=dark_bg_color, bordercolor=light_text_color, othermonthforeground=cal_greyed_out_colour,othermonthweforeground=cal_greyed_out_colour,othermonthbackground=dark_bg_color, normalforeground=light_text_color, weekendforeground=light_text_color, headersforeground=light_text_color, showweeknumbers=False, font=calendar_font)
cal.pack(pady=20, padx=10, fill="both", expand=True)
cal.bind("<<CalendarSelected>>", on_date_select)

today_button = ttk.Button(frame, text="Today", command=set_to_today, style="Custom.TButton")
today_button.pack(pady=10)

selected_date_label = tk.Label(frame, text="Select a date", bg=dark_bg_color, fg= light_text_color,font=("Arial", 20),pady=2)
selected_date_label.pack()

mood_values = [str(i) for i in range(1, 6)] 
mood_entry = create_label_entry(frame, "Mood (1-5):", ttk.Combobox, values=mood_values, state="readonly")

thoughts_entry = create_label_entry(frame, "Any thoughts on the day:", scrolledtext.ScrolledText, wrap=tk.WORD, width=40)
thoughts_entry.configure(height=3)

learning_options = ["Web Dev", "Machine Learning", "Data analysis","Cyber Security","Cloud Computing","Mobile Dev","General Coding","None :("] 

learning_entry = create_label_entry(frame, "What I focused on learning:", ttk.Combobox, values=learning_options, state="readonly")

physical_activity_options = ["None", "Walk", "Worked out-Legs","Worked out-Arms", "Worked out-Core","Worked out-General","Active Day","Played sport"]  
physical_activity_entry = create_label_entry(frame, "Physical Activity:", ttk.Combobox, values=physical_activity_options, state="readonly")

favorite_media_entry = create_label_entry(frame, "Favorite Media:")

media_type_options = ["Book", "Movie", "TV Show", "Podcast", "Music", "Article", "Youtube Video","Other"]
media_type_entry = create_label_entry(frame, "Type of Media:", ttk.Combobox, values=media_type_options, state="readonly")

friend_of_the_day_entry = create_label_entry(frame, "Friend of the Day:")

food_healthiness_values = [str(i) for i in range(1, 6)] 
food_healthiness_entry = create_label_entry(frame, "Food Healthiness (1-5):", ttk.Combobox, values=food_healthiness_values, state="readonly")

spend_entry = create_label_entry(frame, "$ Spent:")

grateful_for_entry = create_label_entry(frame, "Something I'm grateful For:")

sleep_values = [str(i / 2) for i in range(0, 21)] + ["10.5+"]
sleep_entry = create_label_entry(frame, "Sleep (hours):", ttk.Combobox, values=sleep_values, state="readonly")

save_button = ttk.Button(frame, text='Save', command=save_data, style="Custom.TButton")
save_button.pack(pady=10)


on_date_select()



canvas.configure(scrollregion=canvas.bbox("all"))
app.geometry(f"{window_width}x{window_height}")
app.resizable(False, False)
app.mainloop()