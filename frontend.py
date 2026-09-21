import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr

from backend import (
    analyze_complaint,
    get_history,
    delete_history
)


# =========================================================
# COLORS
# =========================================================

BG = "#061B46"
SIDEBAR = "#082B67"
HEADER = "#0878E8"
ROYAL_BLUE = "#2563EB"

INPUT_BG = "#0B3475"
CARD_BG = "#0B2F69"

WHITE = "#FFFFFF"
LIGHT_BLUE = "#BDEBFF"
CYAN = "#00D9FF"

PURPLE = "#7C3AED"
GREEN = "#20E0A0"
RED = "#FF3B6B"


# =========================================================
# GLOBAL VARIABLES
# =========================================================

root = None
main_area = None
history_list = None
complaint_box = None

last_result = {
    "category": "—",
    "issue": "—",
    "solution": "—"
}


# =========================================================
# CATEGORY DETAILS
# =========================================================

categories = [
    ("▣", "Laptop / Computer Issues", "#38BDF8"),
    ("▯", "Mobile / Phone Issues", "#C084FC"),
    ("◉", "Internet / Network Issues", "#22D3EE"),
    ("◈", "App / Website Issues", "#FB923C"),
    ("▤", "Payment Issues", "#4ADE80"),
    ("▱", "Delivery Issues", "#F87171"),
    ("♨", "Food Issues", "#FBBF24"),
    ("●", "Account Issues", "#818CF8"),
    ("♙", "Security / Privacy Issues", "#FB7185"),
    ("?", "Other Issues", "#38BDF8")
]


# =========================================================
# CLEAR SCREEN
# =========================================================

def clear_screen():
    for widget in main_area.winfo_children():
        widget.destroy()


# =========================================================
# HEADER
# =========================================================

def create_header():

    header = tk.Frame(
        main_area,
        bg=HEADER,
        height=105
    )

    header.pack(fill="x", side="top")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="⬡",
        font=("Segoe UI", 38, "bold"),
        fg=WHITE,
        bg=HEADER
    ).pack(side="left", padx=(25, 10))

    title_frame = tk.Frame(
        header,
        bg=HEADER
    )

    title_frame.pack(side="left", pady=15)

    tk.Label(
        title_frame,
        text="SMART COMPLAINT ANALYZER",
        font=("Segoe UI", 27, "bold"),
        fg=WHITE,
        bg=HEADER
    ).pack(anchor="w")

    tk.Label(
        title_frame,
        text="Your complaint. Our solution.",
        font=("Segoe UI", 11),
        fg=LIGHT_BLUE,
        bg=HEADER
    ).pack(anchor="w")

    nav_frame = tk.Frame(
        header,
        bg=HEADER
    )

    nav_frame.pack(
        side="right",
        padx=25
    )

    tk.Button(
        nav_frame,
        text="⌂  Home",
        command=show_home,
        font=("Segoe UI", 11, "bold"),
        fg=WHITE,
        bg=HEADER,
        activebackground=HEADER,
        activeforeground=WHITE,
        bd=0,
        cursor="hand2"
    ).pack(side="left", padx=12)

    tk.Button(
        nav_frame,
        text="▦  Dashboard",
        command=show_dashboard,
        font=("Segoe UI", 11, "bold"),
        fg=WHITE,
        bg=HEADER,
        activebackground=HEADER,
        activeforeground=WHITE,
        bd=0,
        cursor="hand2"
    ).pack(side="left", padx=12)

    tk.Button(
        nav_frame,
        text="⏻  Exit",
        command=root.destroy,
        font=("Segoe UI", 11, "bold"),
        fg=WHITE,
        bg=HEADER,
        activebackground=HEADER,
        activeforeground=WHITE,
        bd=0,
        cursor="hand2"
    ).pack(side="left", padx=12)


# =========================================================
# SIDEBAR
# =========================================================

def create_sidebar():

    sidebar = tk.Frame(
        main_area,
        bg=SIDEBAR,
        width=320
    )

    sidebar.pack(
        side="left",
        fill="y"
    )

    sidebar.pack_propagate(False)

    tk.Label(
        sidebar,
        text="◆  QUICK HELP",
        font=("Segoe UI", 15, "bold"),
        fg=CYAN,
        bg=SIDEBAR
    ).pack(
        anchor="w",
        padx=25,
        pady=(25, 15)
    )

    # ---------------- CATEGORIES ----------------

    for symbol, name, color in categories:

        row = tk.Frame(
            sidebar,
            bg=SIDEBAR,
            height=45
        )

        row.pack(
            fill="x",
            padx=15,
            pady=2
        )

        row.pack_propagate(False)

        icon = tk.Label(
            row,
            text=symbol,
            font=("Segoe UI Symbol", 19, "bold"),
            fg=color,
            bg=SIDEBAR,
            width=3
        )

        icon.pack(side="left")

        label = tk.Label(
            row,
            text=name,
            font=("Segoe UI", 10, "bold"),
            fg=WHITE,
            bg=SIDEBAR
        )

        label.pack(side="left")

        arrow = tk.Label(
            row,
            text="›",
            font=("Segoe UI", 17, "bold"),
            fg=CYAN,
            bg=SIDEBAR
        )

        arrow.pack(
            side="right",
            padx=10
        )

        row.bind(
            "<Button-1>",
            lambda event, n=name: category_click(n)
        )

        icon.bind(
            "<Button-1>",
            lambda event, n=name: category_click(n)
        )

        label.bind(
            "<Button-1>",
            lambda event, n=name: category_click(n)
        )

    # ---------------- SEPARATOR ----------------

    tk.Frame(
        sidebar,
        bg="#174B91",
        height=2
    ).pack(
        fill="x",
        pady=(18, 0)
    )

    # ---------------- SEARCH HISTORY ----------------

    tk.Label(
        sidebar,
        text="◷  SEARCH HISTORY",
        font=("Segoe UI", 14, "bold"),
        fg=LIGHT_BLUE,
        bg=SIDEBAR
    ).pack(
        anchor="w",
        padx=25,
        pady=(18, 10)
    )

    history_frame = tk.Frame(
        sidebar,
        bg=SIDEBAR
    )

    history_frame.pack(
        fill="both",
        expand=True,
        padx=18
    )

    scrollbar = tk.Scrollbar(
        history_frame
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    global history_list

    history_list = tk.Listbox(
        history_frame,
        bg="#08285F",
        fg=WHITE,
        selectbackground=ROYAL_BLUE,
        selectforeground=WHITE,
        font=("Segoe UI", 9),
        bd=1,
        relief="solid",
        highlightthickness=0,
        yscrollcommand=scrollbar.set
    )

    history_list.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.config(
        command=history_list.yview
    )

    history_list.bind(
        "<<ListboxSelect>>",
        history_selected
    )

    # ---------------- DELETE BUTTON ----------------

    tk.Button(
        sidebar,
        text="🗑  DELETE SELECTED",
        command=delete_selected,
        font=("Segoe UI", 10, "bold"),
        fg=WHITE,
        bg=RED,
        activebackground="#E11D48",
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        height=2
    ).pack(
        fill="x",
        padx=18,
        pady=18
    )

    load_history()


# =========================================================
# CATEGORY CLICK
# =========================================================

def category_click(category):

    if complaint_box:

        complaint_box.delete(
            "1.0",
            "end"
        )

        complaint_box.insert(
            "1.0",
            "My problem is related to " + category
        )

        complaint_box.focus()


# =========================================================
# HOME SCREEN
# =========================================================

def show_home():

    clear_screen()

    create_header()
    create_sidebar()

    content = tk.Frame(
        main_area,
        bg=BG
    )

    content.pack(
        side="left",
        fill="both",
        expand=True
    )

    # ---------------- HEADING ----------------

    heading_frame = tk.Frame(
        content,
        bg=BG
    )

    heading_frame.pack(
        fill="x",
        padx=35,
        pady=(35, 10)
    )

    tk.Label(
        heading_frame,
        text="●●●",
        font=("Segoe UI", 20, "bold"),
        fg=CYAN,
        bg=BG
    ).pack(
        side="left",
        padx=(0, 15)
    )

    tk.Label(
        heading_frame,
        text="What's the Problem?",
        font=("Segoe UI", 28, "bold"),
        fg=WHITE,
        bg=BG
    ).pack(
        side="left"
    )

    tk.Label(
        content,
        text="Describe your complaint in detail. Be as specific as possible.",
        font=("Segoe UI", 11),
        fg=LIGHT_BLUE,
        bg=BG
    ).pack(
        anchor="w",
        padx=90
    )

    # ---------------- COMPLAINT BOX ----------------

    global complaint_box

    complaint_box = tk.Text(
        content,
        height=6,
        font=("Segoe UI", 12),
        bg=INPUT_BG,
        fg=WHITE,
        insertbackground=WHITE,
        bd=2,
        relief="solid",
        highlightthickness=1,
        highlightbackground=ROYAL_BLUE,
        highlightcolor=CYAN,
        wrap="word"
    )

    complaint_box.pack(
        fill="x",
        padx=35,
        pady=(25, 12)
    )

    complaint_box.insert(
        "1.0",
        "Type your complaint here..."
    )

    complaint_box.bind(
        "<FocusIn>",
        remove_placeholder
    )

    # ---------------- BUTTONS ----------------

    button_frame = tk.Frame(
        content,
        bg=BG
    )

    button_frame.pack(
        anchor="w",
        padx=35,
        pady=10
    )

    # ANALYZE

    tk.Button(
        button_frame,
        text="⌕  ANALYZE COMPLAINT",
        command=analyze_button,
        font=("Segoe UI", 11, "bold"),
        fg=WHITE,
        bg=CYAN,
        activebackground="#06B6D4",
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        width=20,
        height=2
    ).pack(
        side="left",
        padx=(0, 12)
    )

    # CLEAR

    tk.Button(
        button_frame,
        text="⟳  CLEAR",
        command=clear_complaint,
        font=("Segoe UI", 11, "bold"),
        fg=WHITE,
        bg=PURPLE,
        activebackground="#6D28D9",
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        width=12,
        height=2
    ).pack(
        side="left",
        padx=(0, 12)
    )

    # BACK

    tk.Button(
        button_frame,
        text="←  BACK",
        command=show_welcome,
        font=("Segoe UI", 11, "bold"),
        fg=WHITE,
        bg=ROYAL_BLUE,
        activebackground="#1D4ED8",
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        width=12,
        height=2
    ).pack(
        side="left",
        padx=(0, 12)
    )

    # VOICE - BACK BUTTON PAKKANA

    tk.Button(
        button_frame,
        text="🎤  VOICE",
        command=speak_complaint,
        font=("Segoe UI", 11, "bold"),
        fg=WHITE,
        bg=GREEN,
        activebackground="#10B981",
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        width=12,
        height=2
    ).pack(
        side="left"
    )

    # ---------------- BOTTOM AREA ----------------

    bottom = tk.Frame(
        content,
        bg=BG
    )

    bottom.pack(
        fill="both",
        expand=True
    )

    tk.Label(
        bottom,
        text="▣",
        font=("Segoe UI Symbol", 65),
        fg=CYAN,
        bg=BG
    ).pack(
        pady=(35, 5)
    )

    tk.Label(
        bottom,
        text="Better Analysis   •   Faster Solutions   •   Safer You",
        font=("Segoe UI", 13, "bold"),
        fg=WHITE,
        bg=BG
    ).pack()


# =========================================================
# VOICE COMPLAINT
# =========================================================

def speak_complaint():

    try:

        recognizer = sr.Recognizer()

        messagebox.showinfo(
            "Voice Complaint",
            "Click OK and speak your complaint clearly."
        )

        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            print("Listening...")

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        complaint = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        complaint_box.delete(
            "1.0",
            "end"
        )

        complaint_box.insert(
            "1.0",
            complaint
        )

        complaint_box.focus()

    except sr.WaitTimeoutError:

        messagebox.showwarning(
            "Voice Input",
            "No voice detected. Please try again."
        )

    except sr.UnknownValueError:

        messagebox.showwarning(
            "Voice Input",
            "Sorry, I could not understand your voice."
        )

    except sr.RequestError:

        messagebox.showerror(
            "Voice Error",
            "Speech recognition service is unavailable.\n"
            "Please check your internet connection."
        )

    except Exception as e:

        messagebox.showerror(
            "Voice Error",
            str(e)
        )


# =========================================================
# REMOVE PLACEHOLDER
# =========================================================

def remove_placeholder(event):

    if complaint_box.get(
        "1.0",
        "end-1c"
    ) == "Type your complaint here...":

        complaint_box.delete(
            "1.0",
            "end"
        )


# =========================================================
# CLEAR COMPLAINT
# =========================================================

def clear_complaint():

    complaint_box.delete(
        "1.0",
        "end"
    )


# =========================================================
# ANALYZE BUTTON
# =========================================================

def analyze_button():

    complaint = complaint_box.get(
        "1.0",
        "end-1c"
    ).strip()

    if not complaint:

        messagebox.showwarning(
            "Input Required",
            "Please enter your complaint."
        )

        return

    if complaint == "Type your complaint here...":

        messagebox.showwarning(
            "Input Required",
            "Please enter your complaint."
        )

        return

    try:

        result = analyze_complaint(
            complaint
        )

        global last_result

        if isinstance(result, dict):

            last_result = {
                "category": result.get(
                    "category",
                    "—"
                ),
                "issue": result.get(
                    "issue",
                    "—"
                ),
                "solution": result.get(
                    "solution",
                    "—"
                )
            }

        else:

            last_result = {
                "category": result[0],
                "issue": result[1],
                "solution": result[2]
            }

        load_history()

        messagebox.showinfo(
            "Analysis Complete",
            "Complaint analyzed successfully.\n\n"
            "Click Dashboard to view the Analysis Result."
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# =========================================================
# DASHBOARD SCREEN
# =========================================================

def show_dashboard():

    clear_screen()

    create_header()
    create_sidebar()

    dashboard = tk.Frame(
        main_area,
        bg=BG
    )

    dashboard.pack(
        side="left",
        fill="both",
        expand=True
    )

    tk.Label(
        dashboard,
        text="✦  ANALYSIS RESULT",
        font=("Segoe UI", 28, "bold"),
        fg=WHITE,
        bg=BG
    ).pack(
        anchor="w",
        padx=40,
        pady=(40, 25)
    )

    create_result_card(
        dashboard,
        "●",
        "CATEGORY",
        last_result["category"],
        CYAN
    )

    create_result_card(
        dashboard,
        "⚠",
        "ISSUE",
        last_result["issue"],
        "#A78BFA"
    )

    create_result_card(
        dashboard,
        "●",
        "SOLUTION",
        last_result["solution"],
        GREEN,
        big=True
    )


# =========================================================
# RESULT CARD
# =========================================================

def create_result_card(
    parent,
    icon,
    title,
    value,
    color,
    big=False
):

    card = tk.Frame(
        parent,
        bg=CARD_BG,
        highlightbackground=ROYAL_BLUE,
        highlightthickness=1
    )

    card.pack(
        fill="x",
        padx=40,
        pady=10
    )

    tk.Label(
        card,
        text=icon,
        font=("Segoe UI", 25, "bold"),
        fg=color,
        bg=CARD_BG,
        width=3
    ).pack(
        side="left",
        padx=(15, 5),
        pady=15
    )

    text_frame = tk.Frame(
        card,
        bg=CARD_BG
    )

    text_frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=10,
        pady=15
    )

    tk.Label(
        text_frame,
        text=title,
        font=("Segoe UI", 12, "bold"),
        fg=color,
        bg=CARD_BG
    ).pack(
        anchor="w"
    )

    tk.Label(
        text_frame,
        text=value,
        font=("Segoe UI", 13 if big else 15, "bold"),
        fg=WHITE,
        bg=CARD_BG,
        wraplength=700,
        justify="left"
    ).pack(
        anchor="w",
        pady=(7, 0)
    )


# =========================================================
# LOAD HISTORY
# =========================================================

def load_history():

    if history_list is None:
        return

    history_list.delete(
        0,
        "end"
    )

    try:

        rows = get_history()

        for row in rows:

            complaint_id = row[0]
            complaint = row[1]

            short_text = complaint.replace(
                "\n",
                " "
            )

            if len(short_text) > 30:
                short_text = short_text[:30] + "..."

            history_list.insert(
                "end",
                f"[{complaint_id}] {short_text}"
            )

    except Exception as e:

        print(
            "History Error:",
            e
        )


# =========================================================
# HISTORY SELECTED
# =========================================================

def history_selected(event):

    selection = history_list.curselection()

    if not selection:
        return

    index = selection[0]

    try:

        rows = get_history()

        if index >= len(rows):
            return

        row = rows[index]

        complaint = row[1]
        category = row[2]
        issue = row[3]
        solution = row[4]

        global last_result

        last_result = {
            "category": category,
            "issue": issue,
            "solution": solution
        }

        if complaint_box:

            complaint_box.delete(
                "1.0",
                "end"
            )

            complaint_box.insert(
                "1.0",
                complaint
            )

    except Exception as e:

        print(
            "History selection error:",
            e
        )


# =========================================================
# DELETE SELECTED HISTORY
# =========================================================

def delete_selected():

    selection = history_list.curselection()

    if not selection:

        messagebox.showwarning(
            "Select History",
            "Please select a complaint from Search History."
        )

        return

    selected_text = history_list.get(
        selection[0]
    )

    try:

        complaint_id = int(
            selected_text.split("]")[0].replace(
                "[",
                ""
            )
        )

        confirm = messagebox.askyesno(
            "Delete Complaint",
            "Do you want to delete this complaint?"
        )

        if not confirm:
            return

        success = delete_history(
            complaint_id
        )

        if success:

            load_history()

            messagebox.showinfo(
                "Deleted",
                "Complaint deleted successfully."
            )

        else:

            messagebox.showerror(
                "Error",
                "Complaint could not be deleted."
            )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# =========================================================
# WELCOME SCREEN
# =========================================================

def show_welcome():

    clear_screen()

    welcome = tk.Frame(
        main_area,
        bg=BG
    )

    welcome.pack(
        fill="both",
        expand=True
    )

    tk.Label(
        welcome,
        text="⬡",
        font=("Segoe UI", 80, "bold"),
        fg=CYAN,
        bg=BG
    ).pack(
        pady=(100, 10)
    )

    tk.Label(
        welcome,
        text="SMART COMPLAINT ANALYZER",
        font=("Segoe UI", 32, "bold"),
        fg=WHITE,
        bg=BG
    ).pack()

    tk.Label(
        welcome,
        text="Your complaint. Our solution.",
        font=("Segoe UI", 15),
        fg=LIGHT_BLUE,
        bg=BG
    ).pack(
        pady=10
    )

    tk.Button(
        welcome,
        text="GET STARTED  →",
        command=show_home,
        font=("Segoe UI", 14, "bold"),
        fg=WHITE,
        bg=ROYAL_BLUE,
        activebackground="#1D4ED8",
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        width=20,
        height=2
    ).pack(
        pady=25
    )


# =========================================================
# START GUI
# =========================================================

def start_gui():

    global root, main_area

    root = tk.Tk()

    root.title(
        "Smart Complaint Analyzer"
    )

    root.geometry(
        "1250x750"
    )

    root.minsize(
        1000,
        650
    )

    root.configure(
        bg=BG
    )

    main_area = tk.Frame(
        root,
        bg=BG
    )

    main_area.pack(
        fill="both",
        expand=True
    )

    show_welcome()

    root.mainloop()