import tkinter as tk  
from tkinter import ttk
from PIL import Image, ImageTk
from pygame import mixer

# function to add sound at correct answer (the sound file is attached in the comment section)
def play_correctans_effect():
    mixer.init()
    mixer.music.load("correctans.wav")  
    mixer.music.play()


# function to add sound at incorrect answer (the sound file is attached in the comment section)
def play_wrongans_effect():
    mixer.init()
    mixer.music.load("wrongans.wav") 
    mixer.music.play()


# function to add sound at level complete (the sound file is attached in the comment section)
def play_level_effect():
    mixer.init()
    mixer.music.load("levelwin.wav") 
    mixer.music.play()


# function to show the first page
def switch_to_specific_page(page):
    page.tkraise()
    page.grid(row=0, column=0, sticky="nsew")
    if page == front_page:
        create_front_page()
        page.after(1000, root.destroy)


# function to switch frames
def switch_pages(page1, page2):
    global level, hint
    page1.grid_forget()
    for widget in page1.winfo_children():
        widget.destroy()
    page2.grid(row=0,column=0, sticky="nsew")
    if page2 == instruction_page:
        create_instruction_page()
    elif page2 == name_page:
        create_name_page()
    elif page2 == background_page:
        level += 1
        create_background_page()
    elif page2 == clue_page1:
        create_clue_page1()
    elif page2 == clue_page2:
        create_clue_page2()
    elif page2 == clue_page3:
        create_clue_page3()
    elif page2 == conclusion_page:
        create_conclusion_page()
    elif page2 == congrats_page:
        create_congrats_page()


# function to create a submit button
def submit_button(page, entry):
    submit_btn = tk.Button(page,text= "Submit", command=lambda:on_submit(page, entry, submit_btn), font="Raleway", bg="black", fg= "white", width= 10, height=1 )
    submit_btn.grid(row=1, column=0, padx=5, pady=5, sticky="n")       


# funtion to create label for displaying messages
def message_label(page, reason):
    msg = tk.Label(page, text="", font=("Raleway",10))
    msg.grid(row=3, column=0, pady=5)
    if reason == "hint":
        msg.config(text="No hints remaining!", font=("Raleway",12))
    elif reason == "reveal":
        msg.config(text="You have already used this option once.", font=("Raleway",12))
    elif reason == "correct ans":
        msg.config(text="Correct!", font=("Raleway",12))
        play_correctans_effect()
    elif reason == "incorrect ans":
        msg.config(text="Incorrect. Try Again!", font=("Raleway",12))
        play_wrongans_effect()
    elif reason == "incorrect option":
        msg.config(text="Please choose a valid option.", font=("Raleway",12))

    page.after(5000, msg.destroy)


# function to decide what to do when submit button is pressed
def on_submit(page, entry, submit_btn):
    global playername
    answer = tk.Label(page, text="")
    answer.grid(row=2, column=0,padx= 10, pady=5)
    if page == name_page:
        playername = entry.get()
        if playername == "" or playername == "Enter Your Name.":
            answer.config(text="Please enter your name.", font="Raleway")
        else:
            switch_pages(name_page, instruction_page)
    elif page == clue_page1:
        choice = entry.get()
        handle_option(page, choice, submit_btn, entry)
    elif page == clue_page2:
        choice = entry.get()
        handle_option(page, choice, submit_btn, entry)
    elif page == clue_page3:
        choice = entry.get()
        handle_option(page, choice, submit_btn, entry)


# function to remove text once user starts typing
def on_key_press(entry_widget, watermark, event):
    current_text = entry_widget.get()
    if current_text == watermark:
        entry_widget.delete(0, tk.END)

    
# function to create a check answer button
def check_button(page, level, riddle_entry, submit_btn):
    check_btn = tk.Button(page,text= "Check answer", command=lambda:check_answer(page, level, riddle_entry, submit_btn, check_btn), font="Raleway", bg="black", fg= "white", width= 15, height= 1 )
    check_btn.grid(row=2, column=0, padx=40, pady=10, sticky="e") 


# function to handle options 
def handle_option(page, choice, submit_btn, entry):
    global level, hint, answer_reveal
    choice = choice.upper().strip()
    riddle_entry = ttk.Entry(page, width=30, font=("Raleway", 10))
    if choice == "A":
        riddle_prompt = "Your answer"
        riddle_entry.insert(0, riddle_prompt)
        riddle_entry.bind("<FocusIn>", lambda event, entry=riddle_entry, text=riddle_prompt: on_key_press(entry, text, event))
        riddle_entry.grid(row=2, column=0, pady=5)
        check_button(page, level, riddle_entry, submit_btn)
    elif choice == "B":
        if hint == 0:
            message_label(page, "hint")
        else:
            if level == 1:
                if page == clue_page1:
                    hint1a(clue_page1)
                elif page == clue_page2:
                    hint1b(clue_page2)
                elif page == clue_page3:
                    hint1c(clue_page3)
            elif level == 2:
                if page == clue_page1:
                    hint2a(clue_page1)
                elif page == clue_page2:
                    hint2b(clue_page2)
                elif page == clue_page3:
                    hint2c(clue_page3)
            elif level == 3:
                if page == clue_page1:
                    hint3a(clue_page1)
                elif page == clue_page2:
                    hint3b(clue_page2)
                elif page == clue_page3:
                    hint3c(clue_page3)
        
    elif choice == "C":
        if answer_reveal == 1:
            message_label(page, "reveal")  
        else:
            answer_reveal += 1
            reveal_answer(page, level)
            submit_btn.config(state="disabled")
            entry.config(state= "disabled")
            next_btn = tk.Button(page, text="Next", command=lambda:switch_pages(clue_page1, clue_page2), font="Raleway", bg="black", fg= "white", width= 10, height=1)
            next_btn.grid(row=3, column=0, padx=10, pady=10, sticky="e")   
  
    elif choice == "D":
        switch_to_specific_page(front_page)
    else:
        message_label(page, "incorrect option")


# function to check answer from user (uses dictionary)
def check_answer(page, level, riddle_entry, submit_btn, check_btn):
    flag = False
    answer_dict = {'1-R1':'N2', '1-R2' : ['MOTHER', 'MUM', 'MOM', 'MUMMY', 'MAA'], '1-R3' :'SHADOW', '2-R1':'RED', '2-R2':'JAYDEN', '2-R3':'TON',
'3-R1':['E', 'MAID ELANOR', 'ELANOR', 'MAID'], '3-R2':'HEART', '3-R3': 'PENCIL' }
    riddleanswer = riddle_entry.get()
    if level == 1:
        if page == clue_page1:
            key = "1-R1"
            if riddleanswer != answer_dict[key]:
                message_label(page, "incorrect ans")
            else:
                message_label(page, "correct ans")
                submit_btn.config(state="disabled")
                check_btn.config(state="disabled")
                next_btn = tk.Button(page, text="Next", command=lambda:switch_pages(clue_page1, clue_page2), font="Raleway", bg="black", fg= "white", width= 10, height=1)
                next_btn.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        elif page == clue_page2:
            riddleanswer = riddleanswer.upper()
            key = "1-R2"
            for i in answer_dict[key]:
                if i == riddleanswer:
                    message_label(page, "correct ans") 
                    flag = True
                    submit_btn.config(state="disabled")
                    check_btn.config(state="disabled")
                    next_btn = tk.Button(page, text="Next", command=lambda:switch_pages(clue_page2, clue_page3), font="Raleway", bg="black", fg= "white", width= 10, height=1)
                    next_btn.grid(row=3, column=0, padx=10, pady=10, sticky="e")
            if flag == False:
                message_label(page, "incorrect ans")       
        elif page == clue_page3:
            riddleanswer = riddleanswer.upper()
            key = "1-R3"
            if riddleanswer == answer_dict[key]:
                message_label(page, "correct ans")
                submit_btn.config(state="disabled")
                check_btn.config(state="disabled")
                next_btn = tk.Button(page, text="Next", command=lambda:switch_pages(clue_page3, conclusion_page), font="Raleway", bg="black", fg= "white", width= 10, height=1)
                next_btn.grid(row=3, column=0, padx=10, pady=10, sticky="e")
            else:
                message_label(page, "incorrect ans") 
    elif level == 2:
        if page == clue_page1:
            riddleanswer = riddleanswer.upper()
            key = "2-R1"
            if riddleanswer != answer_dict[key]:
                message_label(page, "incorrect ans")
            else:
                message_label(page, "correct ans")
                submit_btn.config(state="disabled")
                check_btn.config(state="disabled")
                next_btn = tk.Button(page, text="Next", command=lambda:switch_pages(clue_page1, clue_page2), font="Raleway", bg="black", fg= "white", width= 10, height=1)
                next_btn.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        elif page == clue_page2:
            riddleanswer = riddleanswer.upper()
            key = "2-R2"
            if riddleanswer != answer_dict[key]:
                message_label(page, "incorrect ans")
            else:
                message_label(page, "correct ans")
                submit_btn.config(state="disabled")
                check_btn.config(state="disabled")
                next_btn = tk.Button(page, text="Next", command=lambda:switch_pages(clue_page2, clue_page3), font="Raleway", bg="black", fg= "white", width= 10, height=1)
                next_btn.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        elif page == clue_page3:
            riddleanswer = riddleanswer.upper()
            key = "2-R3"
            if riddleanswer == answer_dict[key]:
                message_label(page, "correct ans") 
                submit_btn.config(state="disabled")
                check_btn.config(state="disabled")
                next_btn = tk.Button(page, text="Next", command=lambda:switch_pages(clue_page3, conclusion_page), font="Raleway", bg="black", fg= "white", width= 10, height=1)
                next_btn.grid(row=3, column=0, padx=10, pady=10, sticky="e")
            else:
                message_label(page, "incorrect ans") 
    elif level == 3:
        if page == clue_page1:
            riddleanswer = riddleanswer.upper()
            key = "3-R1"
            for i in answer_dict[key]:
                if i == riddleanswer:
                    message_label(page, "correct ans") 
                    flag = True
                    submit_btn.config(state="disabled")
                    check_btn.config(state="disabled")
                    next_btn = tk.Button(page, text="Next", command=lambda:switch_pages(clue_page1, clue_page2), font="Raleway", bg="black", fg= "white", width= 10, height=1)
                    next_btn.grid(row=3, column=0, padx=10, pady=10, sticky="e")
            if flag == False:
                message_label(page, "incorrect ans")
        elif page == clue_page2:
            riddleanswer = riddleanswer.upper()
            key = "3-R2"
            if riddleanswer != answer_dict[key]:
                message_label(page, "incorrect ans")
            else:
                message_label(page, "correct ans")
                submit_btn.config(state="disabled")
                check_btn.config(state="disabled")
                next_btn = tk.Button(page, text="Next", command=lambda:switch_pages(clue_page2, clue_page3), font="Raleway", bg="black", fg= "white", width= 10, height=1)
                next_btn.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        elif page == clue_page3:
            riddleanswer = riddleanswer.upper()
            key = "3-R3"
            if riddleanswer == answer_dict[key]:
                message_label(page, "correct ans") 
                submit_btn.config(state="disabled")
                check_btn.config(state="disabled")
                next_btn = tk.Button(page, text="Next", command=lambda:switch_pages(clue_page3, conclusion_page), font="Raleway", bg="black", fg= "white", width= 10, height=1)
                next_btn.grid(row=3, column=0, padx=10, pady=10, sticky="e")
            else:
                message_label(page, "incorrect ans") 


# funtion that reveals answer and then switches to next page after 3 sec
def reveal_answer(page, level):
    answer_dict = {'1-R1':'N2', '1-R2' : 'MOTHER', '1-R3' :'SHADOW', '2-R1':'RED', '2-R2':'JAYDEN', '2-R3':'TON',
'3-R1':'MAID ELANOR', '3-R2':'HEART', '3-R3': 'PENCIL' }
    correctans = tk.Label(page, text="")
    correctans.grid(row=3, column=0, pady=5)
    if level == 1:
        if page == clue_page1:
            key = '1-R1'
            correctans.config(text= 'Correct answer is ' + answer_dict[key], font=("Raleway", 10))
            page.after(3000, lambda: switch_pages(page, clue_page2))
        elif page == clue_page2:
            key = '1-R2'
            correctans.config(text= 'Correct answer is ' + answer_dict[key], font=("Raleway", 10))
            page.after(3000, lambda: switch_pages(page, clue_page3))
        elif page == clue_page3:
            key = '1-R3'
            correctans.config(text= 'Correct answer is ' + answer_dict[key], font=("Raleway", 10))
            page.after(3000, lambda: switch_pages(page, conclusion_page))
    elif level == 2:
        if page == clue_page1:
            key = '2-R1'
            correctans.config(text = 'Correct answer is ' + answer_dict[key], font=("Raleway", 10))
            page.after(3000, lambda: switch_pages(page, clue_page2))
        elif page == clue_page2:
            key = '2-R2'
            correctans.config(text = 'Correct answer is ' + answer_dict[key], font=("Raleway", 10))
            page.after(3000, lambda: switch_pages(page, clue_page3))
        elif page == clue_page3:
            key = '2-R3'
            correctans.config(text = 'Correct answer is ' + answer_dict[key], font=("Raleway", 10))
            page.after(3000, lambda: switch_pages(page, conclusion_page))
    elif level == 3:
        if page == clue_page1:
            key = '3-R1'
            correctans.config(text = 'Correct answer is ' + answer_dict[key], font=("Raleway", 10))
            page.after(3000, lambda: switch_pages(page, clue_page2))
        elif page == clue_page2:
            key = '3-R2'
            correctans.config(text = 'Correct answer is ' + answer_dict[key], font=("Raleway", 10))
            page.after(3000, lambda: switch_pages(page, clue_page3))
        elif page == clue_page3:
            key = '3-R3'
            correctans.config(text = 'Correct answer is ' + answer_dict[key], font=("Raleway", 10))
            page.after(3000, lambda: switch_pages(page, conclusion_page))


# recursive function to convert binary number into denary as a clue for riddle 1 of level 1
def bin_to_den(binarystr):
    if binarystr == "":
        return 0
    else:
        return (int(binarystr[0]) * (2**(len(binarystr)- 1))) + (bin_to_den(binarystr[1:]))


# Hint for first clue of level 1 (calls recursive function)
def hint1a(page):
    global hint, hint1acall
    hint1acall += 1
    if hint1acall == 1:
        hint -= 1
    denary = bin_to_den("01001110")
    hint_label = tk.Label(page, text= f"""Your hint is: \n -Denary equivalent of the first binary number is {denary}. Now covert the other number into
denary as well and then use the ASCII table to find corresponding characters.\n Now try answering the riddle.""", font=("Raleway", 10), fg="black")
    hint_label.grid(row=2, column=0,pady=5)
    page.after(10000, hint_label.destroy)


# Hint for second clue of level 1
def hint1b(page):
    global hint, hint1bcall
    hint1bcall += 1
    if hint1bcall == 1:
        hint -= 1
    hint_label = tk.Label(page, text="Your hint is: \n A child's primary caretaker, Father and a ......\n Now try answering the riddle.", font=("Raleway", 10), fg="black")
    hint_label.grid(row=2, column=0,pady=5)
    page.after(8000, hint_label.destroy)
    

# Hint for third clue of level 1
def hint1c(page):
    global hint, hint1ccall
    hint1ccall += 1
    if hint1ccall == 1:
        hint -= 1
    hint_label = tk.Label(page, text="Your hint is: \n Stand under the light and look behind, what do you see? \n Now try answering the riddle.", font=("Raleway", 10), fg="black")
    hint_label.grid(row=2, column=0,pady=5)
    page.after(8000, hint_label.destroy)
    

# Hint for first clue of level 2
def hint2a(page):
    global hint, hint2acall
    hint2acall += 1
    if hint2acall == 1:
        hint -= 1
    hint_label = tk.Label(page, text="Your hint is: \n -According to the morse code decoder ._. = R.\n Now try answering the riddle.", font=("Raleway", 10), fg="black")
    hint_label.grid(row=2, column=0,pady=5)
    page.after(8000, hint_label.destroy)


# Hint for second clue of level 2 (uses nested lists and iteration)
def hint2b(page):
    global hint, hint2bcall
    hint2bcall += 1
    if hint2bcall == 1:
        hint -= 1
    keypad = [ [2, 'abc'], [3, 'def'], [4, 'ghi'], [5, 'jkl'], [6, 'mno'], [9, 'wxyz'] ]
    widthK = 25
    heightK = 25

    canvas = tk.Canvas(page, width= len(keypad)* widthK, height= len(keypad)* heightK , bg="white")
    canvas.grid(row=2, column=0,pady=5)
    for i, row in enumerate(keypad):
        for j, element in enumerate(row):
            x = j * widthK
            y = i * heightK
            canvas.create_text(x + widthK // 2, y + heightK // 2, text=str(element))

    page.after(10000, canvas.destroy)


# Hint for third clue of level 2
def hint2c(page):
    global hint, hint2ccall
    hint2ccall += 1
    if hint2ccall == 1:
        hint -= 1
    hint_label = tk.Label(page, text="Your hint is: \n Think about a unit of weight that is commonly used and sounds like a word that means 'not heavy'. It's a straightforward word play involving the reversal of letters.\n Now try answering the riddle.", font=("Raleway", 10), fg="black")
    hint_label.grid(row=2, column=0,pady=5)
    page.after(8000, hint_label.destroy)


# Hint for first clue of level 3 (uses dict)
def hint3a(page):
    global hint, hint3acall
    hint3acall += 1
    if hint3acall == 1:
        hint -= 1
    ndict = {}
    paragraph = """“This too shall pass”, but the question is, does it ever? Time heals you; 
it gives you a moment to look back and see things from a new perspective, but it doesn't let 
you forget what happened. Especially the feelings that you felt; of joy, sorrow, and regret. 
Painful memories which can't be forgotten, remain as a scar always remembered.""" #(using triple quotes to create a multiline string)
    paragraph = paragraph.lower()
    for x in paragraph:
        if x.isalpha():
            if x in ndict:
                ndict[x] += 1
            else:
                ndict[x] = 1
            
    t = max(ndict.values())
    for k,v in ndict.items():
        if v == t:
            maxletter = k

    hint_label = tk.Label(page, text= f"Your hint is: \n The letter that appears most in this paragraph is {maxletter.upper()} \n Now try answering the riddle.", font=("Raleway", 10), fg="black")
    hint_label.grid(row=2, column=0,pady=5)
    page.after(8000, hint_label.destroy)


# Hint for second clue of level 3
def hint3b(page):
    global hint, hint3bcall
    hint3bcall += 1
    if hint3bcall == 1:
        hint -= 1
    hint_label = tk.Label(page, text= f"Your hint is: \n Layla was stabbed in the .....\n Now try answering the riddle.", font=("Raleway", 10), fg="black")
    hint_label.grid(row=2, column=0,pady=5)
    page.after(8000, hint_label.destroy)
    

# recursive function to reverse the answer as a clue for riddle 3 of level 3
def reverse_str(string):
    if string == "":
        return string
    else:
        return reverse_str(string[1:]) + string[0]


# Hint for third clue of level 3
def hint3c(page):
    global hint, hint3ccall
    hint3ccall += 1
    if hint3ccall == 1:
        hint -= 1
    reverse_ans = reverse_str("pencil")
    hint_label = tk.Label(page, text= f"Your hint is: {reverse_ans.upper()}\nFind the reverse of this word. It might hold the answer to your riddle.", font=("Raleway", 10), fg="black")
    hint_label.grid(row=2, column=0,pady=5)
    page.after(10000, hint_label.destroy)



# funtion to add widgets to front page (image used is attached in the comment section)
def create_front_page():
# to make sure that widgets expand when window resized
    front_page.columnconfigure(0, weight=1)
    front_page.rowconfigure(0,weight=1)

# adding image
    logo = Image.open("bg.jpg")
    label_width = 900
    label_height = 670
    logo = logo.resize((label_width, label_height))
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(front_page, image=logo, width=label_width, height=label_height)
    logo_label.image = logo
    logo_label.grid(column=0, row=1)
    

# adding button
    getstarted_text = tk.StringVar()
    getstarted_btn = tk.Button(front_page, textvariable=getstarted_text, command=lambda:switch_pages(front_page,name_page), font="Raleway", bg="black", fg= "white", width= 10, height= 2 )
    getstarted_text.set("Let's Begin")
    getstarted_btn.place(relx=0.5, rely=0.935, anchor=tk.CENTER)


# funtion to add widgets to instruction page
def create_instruction_page():
    global playername
# to make sure that widgets expand when window resized
    instruction_page.columnconfigure(0, weight=1)
    instruction_page.rowconfigure(0,weight=1)

# adding text
    instructions = tk.Text(instruction_page, wrap=tk.WORD, width=75, height=20, bg="#D2B48C", fg="black",  font="Raleway")
    instructions.grid(row=0, column=0, padx =15, pady=15, sticky="n")
    instructions.tag_configure("center", justify='center')
    ins = """Welcome, detective """+ playername.upper() +""" ! Brace yourself, as the only thing more dangerous than the culprit is the fun you're about to have! Keep the following instructions in mind as you move forward:\n
- At the start of every round, you will be given a background of the murder mystery along with a suspect profile.
- Each Round has a total of 3 queries you need to solve.
- There are a total of 3 Rounds, each with an increasing level of difficulty.
- Keep in mind that you have a total of 3 hints which you can use at any point during the game. However, only 1 hint is available for a specific query, you will not get multiple hints for the same riddle.
- Remember, that you also have an option to reveal the answer, which you can use only once throughout the entire game.
\nGood luck and may time reveal clues that are in your favor!\n\nResources you might need to refer to:
- ASCII Table
- Morse Code Decoder
- Phone Keypad"""

    instructions.insert(tk.END, ins)
    instructions.config(state=tk.DISABLED)
    
# adding buttons
    go_forward_btn = tk.Button(instruction_page, text="Start", command=lambda:switch_pages(instruction_page, background_page), font="Raleway", bg="black", fg= "white", width= 10, height= 1)
    go_forward_btn.grid(row=1, column=0, padx=15, pady=15, sticky="e")


# function to add widgets to name page
def create_name_page():
# to make sure that widgets expand when window resized
    name_page.columnconfigure(0, weight=1)
    name_page.rowconfigure(0,weight=1)

# create entry for player name
    name_prompt = "Enter Your Name."
    name_entry = ttk.Entry(name_page, width=50, font=("Raleway",12))
    name_entry.insert(0, name_prompt)
    name_entry.bind("<FocusIn>", lambda event, entry=name_entry, text=name_prompt: on_key_press(entry, text, event))
    name_entry.grid(row=0, column=0, padx=20, pady=20)

# adding buttons
    submit_button(name_page, name_entry)


# function to add widgets to background page
def create_background_page():
    global level
# to make sure that widgets expand when window resized
    background_page.columnconfigure(0, weight=1)
    background_page.rowconfigure(0,weight=1)

# adding the background
    profile = tk.Text(background_page, wrap=tk.WORD, width=105, height=25, bg="#D2B48C", fg="black", font="Raleway")
    profile.grid(row=0, column=0, padx =15, pady=15, sticky="n")
    profile.tag_configure("center", justify='center')
    if level == 1:
        background1 = """Round 1: The Gingerbread Man\n
Background:
7:32 in the afternoon on 24th December 2022, a day before Christmas. Lia walked in the library as she dusted off her jacket 
covered with snow; she was earlier than usual. With what seemed to be a letter in her hand, she cheerfully marched up the stairs 
of the empty library. The owner of the library, an old woman, opened the library at 8:30 p.m as per the long-held tradition of 
winter night reading sessions in their small, but lively town. Grumpy yet kind, the old woman, Ms. Agatha was known for her cold 
smile and warm gingerbread cookies she made. At 7:45 p.m. loud ambulance noises were heard all over, Ms.Agatha was dead. 
Lia was the one who reported her dead body which was found on the rocking chair she used to sit in, with a plate of freshly 
made gingerbread cookies on the table on the side. Devastated for her death to be ruled as natural, Lia decided to take the 
matter in her own hands as she knew somethings was off. Your task is to help Lia solve a mystery as Ms. Agatha left with a
note “My Murderer, tell noone and find him Lia”. 
\nCharacter Profile:
- Mr. James: The “Mr. Rich” of the town who is known for the suits he wears along with an old pendant. Everyone wonders why he lives in the small town despite having enough resources to move into the city.
- Lady Carolina: Ms. Agatha's childhood friend, known for gossiping in the town. Both of them were very close, but could that mean something?
- Mr. Danny: The department store owner in the same lane as the library, wanting to expand his business. 
- Poppy: A poor sophomore who is always seen in the library, everyone was shocked as he got a new car a week before the death.
- Mr. Harry: The landlord who everyone fears, known to go to long lengths if rent isn't paid on time.
- Mr. Charlie: Ms. Agatha's ex-husband who always gambles and was seen arguing with her a few times in the library."""
        
        profile.insert(tk.END, background1)
    elif level == 2:
        background2 = """Round 2: The Red Thread of Fate\n
Background:
In Chinese methodology, there is a belief that if two people are destined to be together they are connected by an invisible red thread. And if two people are connected by this red thread, they are destined lovers,and this magical cord may stretch or tangle but can never break. Known for portraying the famous role of “Loona” who met a tragic end as she was betrayed by her lover, the
actress playing the role, “Starley” shined as beautiful as ever on the red carpet of the annual award show. Every eye was in envy of her stardom as she walked on the stage to collect the award for the best actress. Her pictures in the silk red dress surfaced online that night and every headline was about how she gained success in less than a year. However, to everyone's surprise, Starley was 
found dead in the same red dress in her high rise apartment the next morning. It was 9:45 am when her body was reported by her neighbor, Ms.Christie, who decided to check up on her as she arrived late that night. Starley laid still on the white couch, which was stained by blood, there were two glasses on the table along with a blood-stained knife. Autopsy revealed excessively bleeding to be 
the cause of her death. Follow along the case to find who the murderer is.\n
Character Profile:
- CEO Harry: Starley was signed under his entertainment label. Known to be harsh to every other actor but favored Starley. Starley's overnight stardom was majorly because of him. Some people speculated about his feelings for Starley.
- Actress Jammie: Known for her diverse acting roles she played starting at the age of 9. Signed under the same label as Starley and lost the award of the best actress to her at the awards night. 
- Neighbour Christie: A kind old lady who genuinely cared about Starley. Was the first person to call the cops after seeing Starley's dead body.
- Actor Jayden: Starley was rumored to star in with him in her upcoming movie, however, these rumors were short-lived as his label denied the rumors. 
- Mother Layla: The President of one of the richest tech firms, also Starley's stepmother. She didn't have an ideal relationship with her stepdaughter."""
        
        profile.insert(tk.END, background2)
    elif level == 3:
        background3 = """Round 3: Rock-A-Bye-Baby\n
Background: 
Macbeth's greed and revenge fueled him to commit murders that eventually led to his downfall. Greed. Revenge. Two of 
the most selfish human desires. At what lengths can a human go to fulfill these desires? “Rock-A-Bye-Baby, Rock-a-Bye", 
the lullaby hummed by the doll which Mr. Paterson gifted Layla on her 3rd birthday echoed through the long hallway of
Paterson Family's Grand Mansion. The night was peaceful as the moon vanished behind the clouds; however, this tranquility
was soon broken. It was 10:05 p.m. when a black Mercedes abruptly stopped at the gate, as Mr. and Mrs. Paterson hurriedly
entered the mansion dressed in their formal attire. They had rushed back from the official heir ceremony in which 
Layla was supposed to be declared as the future heiress of the renowned “Paterson” empire. However, the 5-year-old
Layla was dead. Her body was reported by her nanny who went to the kitchen to grab food for her but returned to the
horrifying sight of Layla covered in red with what seemed to be a pencil stabbed directly at her heart. To unravel the
murder of Layla, your task is to complete the riddles.\n
Character Profile:
- Mrs. Paterson: Mr. Paterson's second wife, who he married shortly after Layla's mother died. She was always aggressive towards Layla and wanted her child to be the future heir to the Paterson empire.
- Uncle Joseph: Layla's Uncle who had a huge fight with Mr. Paterson over their father's inheritance. 
- Aunt Teressa: A kind lady (or was she?), who was disapproved of by Joseph's family because of her family background.
- Nanny Angelina: She treated Layla like her own daughter. She was hired by Mr. Paterson's first wife due to her experience with babies.
- Maid Elanor: She was arrogant as she was favored by Mrs. Paterson and was known to run errands for her.
- Chef Oliver: A new chef hired by Mr. Paterson to cook meals for Layla."""
        
        profile.insert(tk.END, background3)
    
    profile.config(state=tk.DISABLED)


# adding the next button
    next_btn = tk.Button(background_page, text="Next", command=lambda:switch_pages(background_page, clue_page1), font="Raleway", bg="black", fg= "white", width= 10, height=1)
    next_btn.grid(row=1, column=0, padx=15, pady=15, sticky="e")


# function to add widgets to first clue page for all levels
def create_clue_page1():
    global level
# to make sure that widgets expand when window resized
    clue_page1.columnconfigure(0, weight=1)
    clue_page1.rowconfigure(0,weight=1)

# print riddle on the screen based on the level and clue
    text = tk.Text(clue_page1, wrap=tk.WORD, width=80, height=18, bg="#D2B48C", fg="black", font="Raleway")
    text.grid(row=0, column=0, pady=19, sticky="n")
    text.tag_configure("center", justify='center')
    if level == 1:
        riddle11 = """RIDDLE 1: \nLia carefully analyzes the note Ms. Agatha left for her; she notices something is off. As she is 
someone who is good at solving riddles, she keeps the note under UV and finds a hidden 
message. She is a computer science major, so immediately recognizes the binary code. Convert 
the following code into characters to help her solve this riddle:
                            Beyond the binary whispers, where zeros dance with ones
                            In the realm of pixels, where secrets are spun. 
                            Follow the code's silent hum, a digital path untold. 
                            Unravel the cipher, let the mystery unfold.\n
Cipher: 01001110 00110010 \n\nChoose one of the options from below:
 A) Answer the riddle \n B) Use Hint \n C) Reveal Answer \n D) Exit Game """
        
        text.insert(tk.END, riddle11)

    elif level == 2:
        riddle12 = """RIDDLE 1: \nCEO Harry became the prime suspect as his fingerprints were found on one of the glasses found in 
Starley's apartment. Despite being investigated he remained silent throughout. However, the detectives found a locker in his apartment, the password was written in morse code in his diary. Your task is to help decipher it.
\nCode: ._.  .  _.. \n\nChoose one of the options from below:
 A) Answer the riddle \n B) Use Hint \n C) Reveal Answer \n D) Exit Game """

        text.insert(tk.END, riddle12)
        
    elif level == 3:
        riddle13 = """Riddle 1:\nRay, the detective who undertook Layla's case got no leads from the primary murder weapon, the pencil, that they found. However, on the night of Layla's birthday, a knife was also 
discovered under her bed. Upon investigating it, a few fingerprints were found. Even though the fingerprints weren't traceable, the investigation unit reported that it was held by a left-handed 
person. Ray digged deep into the murder suspects and found 3 people to be left-handed: Chef Oliver, Maid Elanor, and Aunty Teressa. Your task is to find who among these people held the knife, 
this by finding the most frequently used initial of the murder suspect in the following paragraph:  
                            “This too shall pass”, but the question is, does it ever? 
                            Time heals you; it gives you a moment to look back and 
                            see things from a new perspective, but it doesn't let you 
                            forget what happened. Especially the feelings that you felt:
                            of joy, sorrow, and regret. Painful memories which can't be 
                            forgotten, remain as a scar always remembered. \n\nChoose one of the options from below:
 A) Answer the riddle \n B) Use Hint \n C) Reveal Answer \n D) Exit Game """

        text.insert(tk.END, riddle13)
        
    text.config(state=tk.DISABLED)
    
   

# printing options
    ans_prompt = "Enter Your Choice"
    ans_entry = ttk.Entry(clue_page1, width=30, font=("Raleway, 12"))
    ans_entry.insert(0, ans_prompt)
    ans_entry.bind("<FocusIn>", lambda event, entry=ans_entry, text=ans_prompt: on_key_press(entry, text, event))
    ans_entry.grid(row=0, column=0, pady=5, sticky="s")
    
# adding submit button
    submit_button(clue_page1, ans_entry)
  

# function to add widgets to second clue page for all levels
def create_clue_page2():
    global level
# to make sure that widgets expand when window resized
    clue_page2.columnconfigure(0, weight=1)
    clue_page2.rowconfigure(0,weight=1)

# print riddle on the screen based on the level 
    text = tk.Text(clue_page2, wrap=tk.WORD, width=110, height=18, bg="#D2B48C", fg="black", font="Raleway")
    text.grid(row=0, column=0, pady=19, sticky="n")
    text.tag_configure("center", justify='center')
    if level == 1:
        riddle21 = """Riddle 2:\nLia being the detective she is, immediately understands “N2” means the shelf and row number in the library. As she traces it in the library, 
she finds a book named “The Gingerbread Man” in place of the said shelf and row number. She reads through the book but finds nothing odd, except the lavender symbol made at the end of the book. She remembers seeing Mr. James wearing the pendant with the same lavender symbol. When she tries to inquire about him, she finds that he left the town shortly after Ms. Agatha's death. Feeling disappointed, Lia goes to library again to find any clues that she overlooked. While sitting on the rocking chair, she looks at the painting on the wall. It has the same lavender made on it! She removes the painting and finds a locker hidden inside the wall. It has a password. Help her find the password.
                                        In love's embrace, a lifelong guide, Tender care with arms open wide.                                
                                        Wisdom woven in life's gentle tether, Who am I, in any stormy weather?
                                        From lullabies that sweetly sing, To comforting words that gently bring.
                                        An eternal bond that none other could be, What, dear friend, is the answer to me?
\nChoose one of the options from below:
 A) Answer the riddle \n B) Use Hint \n C) Reveal Answer \n D) Exit Game """
        
        text.insert(tk.END, riddle21)
        
    elif level == 2:
        riddle22 = """Riddle 2:\nStarley's cellphone along with a few medical reports were found in the locker. The medical reports claimed that Starley had depression, 
and it included prescriptions of medicine which she was taking. Upon opening the smart phone, the detectives found messages from Actress Jammie who expressed anger and threatened to reveal to the press that Harry was partial to her out of love, and her stepmother Layla, who congratulated her and invited her over to a meal. There was also an unsaved number who Starley called a few times before she was found dead. Your task is to find who among the suspects was she calling to, you have the following clue:
                                                        Among the suspects, a puzzle to unbind, 
                                                        In the digits' dance, the answer you'll find. 
                                                        Seek the one where the sun's rays may play, 
                                                        In the middle of the night, not leading astray.
\nPhone Number: 529336\n\nChoose one of the options from below:
 A) Answer the riddle \n B) Use Hint \n C) Reveal Answer \n D) Exit Game """

        text.insert(tk.END, riddle22)
        
    elif level == 3:
        riddle23 = """Riddle 2:\nMaid Elanor was fired shortly after Layla's death, upon Ray's visit to the Grand Mansion, she was left flabbergasted. After a formal 
investigation, it was found that she attempted to murder Layla on Mrs. Paterson's command but wasn't successful. Mrs. Paterson desired 
her yet-to-be-born child to inherit the family, and Layla stood in the way of that plan. The night was ideal for carrying out the plan
since she was away with Mr. Paterson, minimizing suspicion. Consequently, she assigned Elanor this responsibility in exchange for a 
huge sum of money. It was 09:25 p.m. when Elanor entered Layla's room, but she was already dead. Took by surprise, she accidentally 
dropped the knife that she had in her hand as she heard approaching footsteps. However, she pointed out that when she was entering the 
room, she saw a shadow of a man before her. Joseph and Oliver being the only male victims were suspected by Ray as he got this next 
piece of information. Solve the following riddle to find out whose shadow Elanor saw.
\nWhat can be touched but can never be seen?\n\nChoose one of the options from below:
 A) Answer the riddle \n B) Use Hint \n C) Reveal Answer \n D) Exit Game  """

        text.insert(tk.END, riddle23)

    text.config(state=tk.DISABLED)
# printing options
    ans_prompt = "Enter Your Choice"
    ans_entry = ttk.Entry(clue_page2, width=30, font=("Raleway, 12"))
    ans_entry.insert(0, ans_prompt)
    ans_entry.bind("<FocusIn>", lambda event, entry=ans_entry, text=ans_prompt: on_key_press(entry, text, event))
    ans_entry.grid(row=0, column=0, pady=5, sticky="s")
    
# adding submit button
    submit_button(clue_page2, ans_entry)


# function to add widgets to third clue page for all levels
def create_clue_page3():
    global level
# to make sure that widgets expand when window resized
    clue_page3.columnconfigure(0, weight=1)
    clue_page3.rowconfigure(0,weight=1)

# print riddle on the screen based on the level 
    text = tk.Text(clue_page3, wrap=tk.WORD, width=100, height=18, bg="#D2B48C", fg="black", font="Raleway")
    text.grid(row=0, column=0, padx= 10, pady=19, sticky="n")
    text.tag_configure("center", justify='center')
    if level == 1:
        riddle31 = """Riddle 3:\nAs she cracks the password to the safe, she finds documents. It contains a birth certificate of a boy, adoption papers, and a few threats. The threats read to empty the library as soon as possible. Feeling puzzled she goes through each document. 
She notices that the threats are written in red ink, which is only available at one shop, this runned by Ms. Agatha's best friend, Ms. Caroline. To know who bought the red ink, she needs to solve a riddle given by her. Help her solve it.
                                    In twilight's cloak, I silently roam, Whispering secrets of an ancient tome.
                                    I'm where the night and day entwine, Yet vanish with the morning shine.
                                    I have no voice, no shape, no face, Yet leave my mark in every place.
                                                        What am I, in nature's grand riddle?                                  
 \n\nChoose one of the options from below:
 A) Answer the riddle \n B) Use Hint \n C) Reveal Answer \n D) Exit Game """
        
        text.insert(tk.END, riddle31)
        
    elif level == 2:
        riddle32 = """Riddle 3:\nThe number's owner was found to be Jayden. After investigating him it was revealed that Starley and Jayden were childhood 
sweethearts, and they were together for a long time before Jayden decided to start his acting career after which they lost 
contact. Starley, in search of finding him, met Harry who was looking for actors for his upcoming film, and casted Starley 
due to her charming looks. Starley decided the only way for her to get close to Jayden was doing the thing he was
passionate about, and hence she kept acting under Harry's label despite knowing how he felt, as she was confident that 
this way, she would be able to meet Jayden one day. She was delighted to know that they would be starring in the same 
film, but her heart broke when Jayden refused to play a role alongside her. To know who killed Starley, you must first
answer the following riddle:
\n"Forward I am heavy, but backward I am not. What am I?\n\nChoose one of the options from below:
 A) Answer the riddle \n B) Use Hint \n C) Reveal Answer \n D) Exit Game"""

        text.insert(tk.END, riddle32)
        
    elif level == 3:
        riddle33 = """Riddle 3:\nAfter a thorough investigation with the two suspects, Ray found that the shadow Elanor saw was of Chef Oliver. Oliver
revealed that he was hired by Teressa to keep an eye on Layla. And on that night, she ordered Oliver to poison Layla's food 
as she saw this as the perfect opportunity to get back at the Paterson's family.. Killing the heir seemed the perfect revenge 
to all the struggles she faced However, Oliver revealed that when he entered the room at 9:20 p.m. to give Layla her food as
usual, Layla was already dead. Upon hearing this, Ray was thoroughly puzzled. However, he recollected something which 
could possibly be the answer to all this. To find out about the murderer, solve the following riddle:
\nI'm taken from a mine, and shut up in a wooden case, from which I'm never released, and yet I am used by almost every person. What am I?
 \nChoose one of the options from below:
 A) Answer the riddle \n B) Use Hint \n C) Reveal Answer \n D) Exit Game  """

        text.insert(tk.END, riddle33)
    
    text.config(state=tk.DISABLED)

# printing options
    ans_prompt = "Enter Your Choice"
    ans_entry = ttk.Entry(clue_page3, width=30, font=("Raleway, 12"))
    ans_entry.insert(0, ans_prompt)
    ans_entry.bind("<FocusIn>", lambda event, entry=ans_entry, text=ans_prompt: on_key_press(entry, text, event))
    ans_entry.grid(row=0, column=0, pady=5, sticky="s")
    
# adding submit button
    submit_button(clue_page3, ans_entry)


# function to add widgets to conclusion page for all levels
def create_conclusion_page():
    global level
# to make sure that widgets expand when window resized
    conclusion_page.columnconfigure(0, weight=1)
    conclusion_page.rowconfigure(0,weight=1)

# adding the final statement
    truth = tk.Text(conclusion_page, wrap=tk.WORD, width=85, height=19, bg="#D2B48C", fg="black", font="Raleway")
    truth.grid(row=0, column=0, padx =15, pady=15, sticky="n")
    truth.tag_configure("center", justify='center')
    if level == 1:
        truth1 = """The Truth:\n\nUpon unraveling the puzzle, Ms. Caroline, the store owner, discloses that the primary buyer of the red ink 
that Lia is seeking is Mr. Danny, the owner of the department store. Step by step, Lia pieces together the 
clues, leading to a revelation: The landlord Mr. Harry, had been pressuring Mr. Danny to vacate his 
department store, as he wishes it to be runned by his son. Mr. Danny wanted to keep his department 
store running; hence, he kept an eye on the library given its strategic location. After facing multiple refusals 
from Ms. Agatha, he paid Poppy, the financially struggling sophomore, to keep an eye on her. One day 
she found Ms. Agatha arguing with her ex-husband about the child they gave up for adoption-Mr. James.
Upon learning this, she shares the information with Mr. Danny, who then threatens Ms. Agatha. He 
insists she reveal to his son, currently searching for his mother in the town, that she is his 
biological mother. Aware of Mr. Danny's determination to acquire the library, Ms. Agatha, fearing the
lengths he would go to, leaves a note for Lia. Unfortunately, her fate is sealed as Mr. Danny poisons 
the gingerbread cookies she made to give to James. """ 
        truth.insert(tk.END, truth1)
    
    elif level == 2:
        truth2 = """The Truth:\n\nOn the night of the award show after Starley received her award, she went to look for Jayden. She found 
him backstage where Jayden gave her an unfamiliar look, however, she brushed it off and passed a big 
smile to him. But before she could express anything, Jayden told her about his marriage. Left utterly 
speechless, she rushed back home where Harry followed her. He tried to calm her down as she cried 
and kept repeating the same words that Jayden broke his promise. He made coffee for her and left when 
she fell asleep. That night, after Harry left, Starley took her own life. She met the same fate as her 
famous role “Loona”, who wasn't left with a purpose after being betrayed by the person she loved the
most, who she thought she was connected to by a red thread. The red string of fate which was her hope
 ended up being the cause of her death."""
        truth.insert(tk.END, truth2)
    
    elif level == 3:
        truth3 = """The Truth:\n\nLayla wasn't born yet when Nanny Angelina's daughter died. She died of a rare heart disease, which could've been cured if Mr. Paterson wouldn't have used his connections with the higher authority to 
transplant the donor's heart in his first wife, instead of Angelina's daughter. Anger filled Angelina 
as she also developed multiple-personality disorder. Determined to take her revenge, she applied for the
being Layla's nanny after she was born. Over time she grew a strong bond with Layla,however Layla also 
reminded her of the daughter she had lost. It had been 5 years, and she was looking for the time to get 
back. The night when Layla was supposed to be declared as the future heiress was also her daughter's 
death anniversary, it is when she killed Layla under her different personality with a pencil she found 
in Layla's room. Getting a grip after what she had done, she hurriedly left the room. This was when Chef
Oliver came to the room, after which Maid Elanor followed. Ray realized that Angelina was the murderer 
after Oliver revealed that he was the one who brought food to her, contradicting Angelina's official stand.
On that night, Layla's death was already pre-destined, be it in the hands of Angelina, Oliver or Elanor. 
Just like one interpretation of "Rock-A-Bye Baby" suggests a death wish, hoping for the replacement of 
King James II's infant son with a Protestant king, humanity experienced three deaths that night. Time 
may never heal the scar in Angelina's heart, the anger which filled Teressa, nor the greed which filled
Mrs. Paterson heart. But what time can do is make them realize the destructive nature of human greed
and revenge."""
        truth.insert(tk.END, truth3)
    
    truth.config(state=tk.DISABLED)

# adding the next button
    next_btn = tk.Button(conclusion_page, text="Next", command=lambda:switch_pages(conclusion_page, congrats_page), font="Raleway", bg="black", fg= "white", width= 10, height=1)
    next_btn.grid(row=3, column=0, padx=10, pady=10, sticky="e") 


# function to add widgets to congratulations page for clearing levels
def create_congrats_page():
    global level, playername
# to make sure that widgets expand when window resized
    congrats_page.columnconfigure(0, weight=1)
    congrats_page.rowconfigure(0,weight=1)

# adding congratulatory message
    if level == 1 or level ==2:
        successmsg = tk.Label(congrats_page, text="Congratulations,\n You have successfully completed Level "+ str(level), font=("Georgia",25), bg="#D2B48C", fg="black")
        successmsg.grid(row=0, column=0, padx=20, pady=20)
        play_level_effect()

# adding the next button
        next_btn = tk.Button(congrats_page, text="Next Level", command=lambda:switch_pages(congrats_page, background_page), font="Raleway", bg="black", fg= "white", width= 13, height=1)
        next_btn.grid(row=0, column=1, padx=15, pady=15, sticky="se")

        go_back_btn = tk.Button(congrats_page, text= "Exit Game", command=lambda:switch_to_specific_page(front_page), font="Raleway", bg="black", fg= "white", width= 13, height= 1)
        go_back_btn.grid(row=0, column=0, padx=15, pady=15, sticky="se")

    elif level == 3:
        successmsg = tk.Label(congrats_page, text=f"Congratulations {playername} !\n You have successfully completed all the rounds of the Murder Mystery!", font=("Georgia",25), bg="#D2B48C", fg="black")
        successmsg.grid(row=0, column=0, padx=20, pady=20)
        play_level_effect()

        go_back_btn = tk.Button(congrats_page, text= "Exit Game", command=lambda:switch_to_specific_page(front_page), font="Raleway", bg="black", fg= "white", width= 13, height= 1)
        go_back_btn.grid(row=0, column=0, padx=15, pady=15, sticky="se")





# creating tkinter screen
root = tk.Tk()
root.grid_columnconfigure(0,weight=1)
root.grid_rowconfigure(0,weight=1)
root.title("HnS Murder Mystery Game")

# initialising global variables
level = 0
hint = 3
answer_reveal = 0
playername = ""

# initialising counters to keep track of how many times hint function is called. If the same function is 
# called more than once then remaining hints will not be decremented as no new hint is displayed.
hint1acall = 0
hint1bcall = 0
hint1ccall = 0
hint2acall = 0
hint2bcall = 0
hint2ccall = 0
hint3acall = 0
hint3bcall = 0
hint3ccall = 0

# creating front page and calling to add widgets
front_page = tk.Frame(root, bg="#D2B48C", width=1000, height=700)
front_page.grid(row=0, column=0, sticky="nsew")
front_page.columnconfigure(0, weight=1)
front_page.rowconfigure(0,weight=1)
create_front_page()

# creating instruction page
instruction_page = tk.Frame(root, bg="#D2B48C", width=1000, height=700)

# creating name page
name_page = tk.Frame(root, bg="#D2B48C", width=1000, height=700)

#creating background page
background_page = tk.Frame(root, bg="#D2B48C", width=1000, height=700)

# creating first clue page for all levels
clue_page1 = tk.Frame(root, bg="#D2B48C", width=1000, height=700)

# creating second clue page for all levels
clue_page2 = tk.Frame(root, bg="#D2B48C", width=1000, height=700)

# creating third clue page for all levels
clue_page3 = tk.Frame(root, bg="#D2B48C", width=1000, height=700)

# creating the page containing truth for all levels
conclusion_page = tk.Frame(root, bg="#D2B48C", width=1000, height=700)

# creating the congratulatory page 
congrats_page = tk.Frame(root, bg="#D2B48C", width=1000, height=700)

root.mainloop()

