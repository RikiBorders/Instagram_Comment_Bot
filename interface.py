
from tkinter import *
from source import *
import threading
import os
import shared
import mysql.connector
import subprocess

def main():
    '''main interface function'''
    global in_use_accounts

    threads = [] #List of all threads (one bot per thread)
    in_use_accounts = [] #list of all accounts in use

    root=Tk()
    root.title('RKAB Auto-Comment Bot')
    root.resizable(False, False)
    root.configure(bg="#4a5254")

    #Setup icon
    root.iconbitmap('icon.ico')

    vscrollbar = Scrollbar(root)

    main_canvas = Canvas(root,width=400,height=300,background="#4a5254",yscrollcommand=vscrollbar.set)

    vscrollbar.config(command=main_canvas.yview)
    vscrollbar.pack(side=RIGHT, fill=Y)

    main_frame = Frame(main_canvas) #Create the frame which will hold the widgets
    main_frame.config(background="#4a5254")

    main_canvas.pack(side="left", fill="both", expand=True)

    #Updated the window creation
    main_canvas.create_window(0,0,window=main_frame, anchor='nw')

    #Credits
    Label(main_frame,wraplength=350,text="Bot developed by Riki Borders",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=235,pady=0,sticky=W)
    Label(main_frame,wraplength=350,text="subscribe on youtube: redacted",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=1,column=0,padx=235,pady=0,sticky=W)

    #Add widgets to the frame
    Label(main_frame,wraplength=350,text="Begin commenting",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=10,pady=5,sticky=W)
    Button(main_frame, text="Go", command=lambda: create_bot_thread(threads)).grid(row=0,column=0,padx=150,pady=10,sticky=W)

    #Add new comment
    Label(main_frame,wraplength=350,text="Add comment:",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=1,column=0,padx=10,sticky=W)
    comment = Entry(main_frame, width = 30, bg = 'white')
    comment.grid(row=2,column=0,padx=10,rowspan=1,sticky=W)
    Button(main_frame, text="Add", command=lambda: update_data(comment.get(), 'comment')).grid(row=2,column=0,padx=210,sticky=W)

    #View Commented Posts
    Label(main_frame,wraplength=350,text="View commented posts",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=4,column=0,padx=10,pady=5,sticky=W)
    Button(main_frame, text="Go", command=lambda: view_commented_list()).grid(row=4,column=0,padx=150,sticky=W)

    #View hashtags
    Label(main_frame,wraplength=350,text="View hashtags",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=5,column=0,padx=10,pady=5,sticky=W)
    Button(main_frame, text="Go", command=lambda: view_hashtags()).grid(row=5,column=0,padx=150,sticky=W)

    #add hashtag
    Label(main_frame,wraplength=350,text="Add hashtag (do not include '#'):",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=6,column=0,padx=10,pady=5,sticky=W)
    hashtag = Entry(main_frame, width = 30, bg = 'white')
    hashtag.grid(row=7,column=0,padx=10,rowspan=1,sticky=W)
    Button(main_frame, text="Add", command=lambda: update_data(hashtag.get(), 'hashtag')).grid(row=7,column=0,padx=210,sticky=W)

    #Add target account
    Label(main_frame,wraplength=350,text="Add target account (username):",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=8,column=0,padx=10,sticky=W)
    Label(main_frame,wraplength=350,text="*Target accounts are accounts whos posts you will comment on",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=9,column=0,padx=10,sticky=W)
    targ_acc = Entry(main_frame, width = 30, bg = 'white')
    targ_acc.grid(row=10,column=0,padx=10,rowspan=1,sticky=W)
    Button(main_frame, text="Add", command=lambda: update_data(targ_acc.get(), 'add_target')).grid(row=10,column=0,padx=210,sticky=W)

    #Manage accounts
    Label(main_frame,wraplength=350,text="Manage accounts",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=11,column=0,padx=10,pady=5,sticky=W)
    Button(main_frame, text="Go", command=lambda: manage_accounts()).grid(row=11,column=0,padx=120,sticky=W)

    #Magae comments
    Label(main_frame,wraplength=350,text="Manage comments",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=12,column=0,padx=10,pady=5,sticky=W)
    Button(main_frame, text="Go", command=lambda: manage_comments()).grid(row=12,column=0,padx=120,sticky=W)

    #Manage modes
    Label(main_frame,wraplength=350,text="Manage modes",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=13,column=0,padx=10,pady=5,sticky=W)
    Button(main_frame, text="Go", command=lambda: manage_modes()).grid(row=13,column=0,padx=120,sticky=W)

    #Manage targets
    Label(main_frame,wraplength=350,text="Manage targets",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=14,column=0,padx=10,pady=5,sticky=W)
    Button(main_frame, text="Go", command=lambda: manage_targets()).grid(row=14,column=0,padx=120,sticky=W)

    #View Logs
    Label(main_frame,wraplength=350,text="View console log",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=15,column=0,padx=10,pady=5,sticky=W)
    Button(main_frame, text="Go", command=lambda: view_console_log()).grid(row=15,column=0,padx=120,sticky=W)

    #View Settings
    Label(main_frame,wraplength=350,text="Settings",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=16,column=0,padx=10,pady=5,sticky=W)
    Button(main_frame, text="Go", command=lambda: view_settings()).grid(row=16,column=0,padx=120,sticky=W)

    #Update the screen before calculating the scrollregion
    root.update()
    main_canvas.config(scrollregion=main_canvas.bbox("all"))
    root.mainloop()


def toggle_console_off(top):
    '''Toggle console off'''
    shared.console_open = False
    top.destroy()


def view_settings():
    '''Display Settings Panel'''
    global refresh_timer
    global refresh_mode_label
    global behavior_label
    global current_age_label
    global acc_swap_label
    global fullscreen_label

    #Setup up new 'root' window
    top = Toplevel()
    top.title('Settings')
    top.resizable(False, False)
    top.configure(bg="#4a5254")

    #Setup icon
    top.iconbitmap('icon.ico')

    #Setup scrolling
    vscrollbar = Scrollbar(top)

    settings_canvas = Canvas(top,width=500,height=300,background="#4a5254",yscrollcommand=vscrollbar.set)

    vscrollbar.config(command=settings_canvas.yview)
    vscrollbar.pack(side=RIGHT, fill=Y)

    settings_frame = Frame(settings_canvas) #Create the frame which will hold the widgets
    settings_frame.config(background="#4a5254")

    settings_canvas.pack(side="left", fill="both", expand=True)

    #Updated the window creation
    settings_canvas.create_window(0,0,window=settings_frame, anchor='nw')

    #Get refresh rate & any other setting values
    current_refresh_rate = get_refresh_timer()
    refresh_mode = get_refresh_mode()
    current_feed_behavior = get_feed_behavior()
    current_age_limit = get_age_limiter()
    current_swap_timer = get_account_swap_timer()
    current_fullscreen = get_fullscreen_setting()

    #Settings title
    Label(settings_frame,wraplength=350,text="Manage General Bot Settings",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=185,sticky=N)

    #Set refresh timer (feed mode)
    Label(settings_frame,wraplength=350,text="Set refresh rate (seconds):",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=1,column=0,padx=10,sticky=W)
    timer = Entry(settings_frame, width = 10, bg = 'white')
    timer.grid(row=2,column=0,padx=10,rowspan=1,sticky=W)
    Button(settings_frame, text="Set", command=lambda: set_refresh_timer(timer.get())).grid(row=2,column=0,padx=85,sticky=W)

    refresh_timer = Label(settings_frame,wraplength=350,text=f"*Current refresh rate: {current_refresh_rate}",fg="#F23636",anchor=NW,background="#4a5254")
    refresh_timer.grid(row=3,column=0,padx=10,sticky=W)

    #Make viewing refresh rate more simple (convert true to on, vice versa)
    if refresh_mode == 'True':
        display_flag = 'on'
    else:
        display_flag = 'off'

    toggle_refresh_mode_label = Label(settings_frame,wraplength=350,text="Toggle Refresh mode on/off:",fg="#e8e8e8",anchor=NW,background="#4a5254")
    toggle_refresh_mode_label.grid(row=4,column=0,padx=10,sticky=W)

    refresh_mode_label = Label(settings_frame,wraplength=350,text=f"*Rapid Refresh: {display_flag}",fg="#F23636",anchor=NW,background="#4a5254")
    refresh_mode_label.grid(row=5,column=0,padx=10,sticky=W)

    Button(settings_frame, text="Toggle", command=lambda: toggle_refresh_mode()).grid(row=5,column=0,padx=120,pady=10,sticky=W)

    #Feed Behavior
    Label(settings_frame,wraplength=350,text="Feed Behavior:",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=6,column=0,padx=10,sticky=W)
    Button(settings_frame, text="Top Comment", command=lambda: set_feed_behavior('top')).grid(row=7,column=0,padx=10,pady=10,sticky=W)
    Button(settings_frame, text="Normal", command=lambda: set_feed_behavior('normal')).grid(row=7,column=0,padx=110,pady=10,sticky=W)

    behavior_label = Label(settings_frame,wraplength=350,text=f"*Current feed behavior: {current_feed_behavior}",fg="#F23636",anchor=NW,background="#4a5254")
    behavior_label.grid(row=8,column=0,padx=10,sticky=W)

    #age limiter
    Label(settings_frame,wraplength=350,text="Set feed mode post-age limiter (seconds):",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=9,column=0,padx=10,sticky=W)
    age_entry = Entry(settings_frame, width = 10, bg = 'white')
    age_entry.grid(row=10,column=0,padx=10,rowspan=1,sticky=W)
    Button(settings_frame, text="Set", command=lambda: set_age_limiter(age_entry.get())).grid(row=10,column=0,padx=85,pady=10,sticky=W)

    current_age_label = Label(settings_frame,wraplength=350,text=f"*Current post age-limit: {current_age_limit}",fg="#F23636",anchor=NW,background="#4a5254")
    current_age_label.grid(row=11,column=0,padx=10,sticky=W)

    #account swap timer
    Label(settings_frame,wraplength=350,text="Set time interval to swap accounts in"+
                                             " feed mode (seconds):",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=12,column=0,padx=10,sticky=W)
    acc_swap_entry = Entry(settings_frame, width = 10, bg = 'white')
    acc_swap_entry.grid(row=13,column=0,padx=10,rowspan=1,sticky=W)
    Button(settings_frame, text="Set", command=lambda: set_account_swap_timer(acc_swap_entry.get())).grid(row=13,column=0,padx=85,pady=10,sticky=W)

    acc_swap_label = Label(settings_frame,wraplength=350,text=f"*Current swap timer: {current_swap_timer}",fg="#F23636",anchor=NW,background="#4a5254")
    acc_swap_label.grid(row=14,column=0,padx=10,sticky=W)

    #fullscreen option
    Label(settings_frame,wraplength=350,text="Toggle fullscreen mode (if the bot is freezing,"+
                                             " try to turn this setting on)",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=15,column=0,padx=10,sticky=W)

    fullscreen_label = Label(settings_frame,wraplength=350,text=f"*Fullscreen: {current_fullscreen}",fg="#F23636",anchor=W,background="#4a5254")
    fullscreen_label.grid(row=16,column=0,padx=10,sticky=W)

    Button(settings_frame, text="Toggle", command=lambda: toggle_fullscreen()).grid(row=16,column=0,padx=110,pady=10,sticky=W)

    top.update()
    settings_canvas.config(scrollregion=settings_canvas.bbox("all"))


def toggle_fullscreen():
    '''Toggle fullscreen setting in config.txt'''

    with open('config.txt', 'r') as f:
        lines = f.readlines()

    #Rewrite file & toggle fullscreen setting
    with open('config.txt', 'w') as f:

        for line in lines:
            #Check for fullscreen setting
            if line.strip('\n') == 'fullscreen=True':
                line = 'fullscreen=False\n'
                fullscreen_label.config(text='*Fullscreen: Off')
                f.write(line)

            elif line.strip('\n') == 'fullscreen=False':
                line = 'fullscreen=True\n'
                fullscreen_label.config(text='*Fullscreen: On')
                f.write(line)

            else:
                f.write(line)


def get_fullscreen_setting():
    '''Get the current fullscreen setting
        ARGS:
            None
        RETURNS:
            str:setting: whether fullscreen mode is on/off
    '''

    with open('config.txt', 'r') as f:
        lines = f.readlines()

    for line in lines:
        #Identify fullscreen setting, & convert to 'on' or 'off' (for easier reading)
        if 'fullscreen' in line:
            setting = line[11:].strip('\n')

            if setting == 'True':
                setting = 'On'
            else:
                setting = 'Off'

    return setting


def view_console_log():
    '''Display bot status to the user'''
    global console_text
    global console_canvas
    global console_frame
    global console_top
    shared.console_open = True

    #Setup up new 'root' window
    console_top = Toplevel()
    console_top.title('Console')
    console_top.resizable(False, False)
    console_top.configure(bg="#4a5254")

    #Setup icon
    console_top.iconbitmap('icon.ico')

    #Setup scrolling
    vscrollbar = Scrollbar(console_top)

    console_canvas = Canvas(console_top,width=500,height=300,background="#4a5254",yscrollcommand=vscrollbar.set)

    vscrollbar.config(command=console_canvas.yview)
    vscrollbar.pack(side=RIGHT, fill=Y)

    console_frame = Frame(console_canvas) #Create the frame which will hold the widgets
    console_frame.config(background="#4a5254")

    console_canvas.pack(side="left", fill="both", expand=True)

    #Updated the window creation
    console_canvas.create_window(0,0,window=console_frame, anchor='nw')

    header_text = "This panel displays all actions taken by active comment bots. Console logs are reset everytime the program is run."
    Label(console_frame,wraplength=350,text=header_text,fg="#e8e8e8",anchor=N,background="#4a5254").grid(row=0,column=0,padx=100,pady=5,sticky=W)

    #Prepare label to display console messages
    console_text = Label(console_frame,wraplength=400,text=shared.console_msgs,fg="#e8e8e8",anchor=W,justify=LEFT,background="#4a5254")
    console_text.grid(row=1,column=0,padx=5,sticky=W)


    console_top.protocol("WM_DELETE_WINDOW", lambda arg=console_top: toggle_console_off(console_top))
    console_top.update()
    console_canvas.config(scrollregion=console_canvas.bbox("all"))


def manage_accounts():
    '''Open a new window displaying account details'''

    #Setup up new 'root' window
    top = Toplevel()
    top.title('Account Manager')
    top.resizable(False, False)
    top.configure(bg="#4a5254")

    #Setup icon
    top.iconbitmap('icon.ico')

    #Setup scrolling
    vscrollbar = Scrollbar(top)

    account_canvas = Canvas(top,width=400,height=300,background="#4a5254",yscrollcommand=vscrollbar.set)

    vscrollbar.config(command=account_canvas.yview)
    vscrollbar.pack(side=RIGHT, fill=Y)

    account_frame = Frame(account_canvas) #Create the frame which will hold the widgets
    account_frame.config(background="#4a5254")

    account_canvas.pack(side="left", fill="both", expand=True)

    #Updated the window creation
    account_canvas.create_window(0,0,window=account_frame, anchor='nw')

    #Add account
    Label(account_frame,wraplength=350,text="Add account:",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=10,sticky=W)
    Label(account_frame,wraplength=350,text="Username:",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=1,column=0,padx=10,sticky=W)
    username = Entry(account_frame, width = 30, bg = 'white')
    username.grid(row=1,column=0,padx=100,rowspan=1,sticky=W)

    Label(account_frame,wraplength=350,text="Password:",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=2,column=0,padx=10,sticky=W)
    password = Entry(account_frame, width = 30, bg = 'white')
    password.grid(row=2,column=0,padx=100,rowspan=1,sticky=W)
    Button(account_frame, text="Add", command=lambda: add_account(username.get(),password.get(), account_frame, account_canvas, top)).grid(row=2,column=0,padx=300,sticky=W)

    #Display accounts
    counter = 3
    with open('accounts.txt', 'r') as f:
        lines = f.readlines()

        for count, line in enumerate(lines):
            #Split up password and username data
            user, pword = line[:line.find(':')], line[line.find(':')+1:]

            u_label = Label(account_frame,wraplength=400,text=f"{count+1}.  Username: {user}",fg="#e8e8e8",anchor=NW,background="#4a5254")
            u_label.grid(row=counter,column=0,padx=10,sticky=W)
            counter += 1
            p_label = Label(account_frame,wraplength=400,text=f"     Password: {pword}",fg="#e8e8e8",anchor=NW,background="#4a5254")
            p_label.grid(row=counter,column=0,padx=10,sticky=W)

            Button(account_frame,text="Remove",command=lambda line=line: remove_file_item(line,'account', account_frame, account_canvas, top)).grid(row=counter,column=0,padx=340,sticky=W)

            counter += 1

    Label(account_frame,wraplength=350,text="Clear accounts (Cannot be undone):",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=counter,column=0,padx=10,pady=10,sticky=W)
    Button(account_frame, text="Clear", command=lambda: clear_file('accounts')).grid(row=counter,column=0,padx=230,pady=10,sticky=W)

    top.update()
    account_canvas.config(scrollregion=account_canvas.bbox("all"))


def manage_comments():
    '''Open a new window displaying the comment list'''
    #Setup up new 'root' window
    top = Toplevel()
    top.title('Comment Manager')
    top.resizable(False, False)
    top.configure(bg="#4a5254")

    #Setup icon
    top.iconbitmap('icon.ico')

    #Setup scrolling
    vscrollbar = Scrollbar(top)

    comment_canvas = Canvas(top,width=400,height=300,background="#4a5254",yscrollcommand=vscrollbar.set)

    vscrollbar.config(command=comment_canvas.yview)
    vscrollbar.pack(side=RIGHT, fill=Y)

    comment_frame = Frame(comment_canvas) #Create the frame which will hold the widgets
    comment_frame.config(background="#4a5254")

    comment_canvas.pack(side="left", fill="both", expand=True)

    #Updated the window creation
    comment_canvas.create_window(0,0,window=comment_frame, anchor='nw')

    Label(comment_frame,wraplength=350,fg="#e8e8e8",text="You can view your comment list in this menu. Each comment "+
    "displayed can be used to comment on a post. Comments are selected randomly for each post.",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=10,sticky=W)

    #Display all comments
    counter = 1
    with open('comments.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for count, line in enumerate(lines):
            label = Label(comment_frame,wraplength=400,text=f"{count+1}.  {line}",fg="#e8e8e8",anchor=NW,background="#4a5254")
            label.grid(row=counter,column=0,padx=10,sticky=W)
            Button(comment_frame, text="Remove", command=lambda line=line: remove_file_item(line,'comment', comment_frame, comment_canvas, top)).grid(row=counter,column=0,padx=340,sticky=W)
            counter += 1

    #Allow for clearing of the file
    Label(comment_frame,wraplength=350,fg="#e8e8e8",text="Clear comments (cannot be undone): ",anchor=NW,background="#4a5254").grid(row=counter,column=0,padx=10,sticky=W)
    Button(comment_frame, text="Clear", command=lambda: clear_file('comments')).grid(row=counter,column=0,padx=230,pady=10,sticky=W)

    top.update()
    comment_canvas.config(scrollregion=comment_canvas.bbox("all"))


def manage_modes():
    '''Open a new window displaying comment modes'''
    global active_mode_label #allow for realtime modifications

    #Setup up new 'root' window
    top = Toplevel()
    top.title('Mode Manager')
    top.resizable(False, False)
    top.configure(bg="#4a5254")

    #Setup icon
    top.iconbitmap('icon.ico')

    #Setup scrolling
    vscrollbar = Scrollbar(top)

    mode_canvas = Canvas(top,width=400,height=400,background="#4a5254",yscrollcommand=vscrollbar.set)

    vscrollbar.config(command=mode_canvas.yview)
    vscrollbar.pack(side=RIGHT, fill=Y)

    mode_frame = Frame(mode_canvas) #Create the frame which will hold the widgets
    mode_frame.config(background="#4a5254")

    mode_canvas.pack(side="left", fill="both", expand=True)

    #Updated the window creation
    mode_canvas.create_window(0,0,window=mode_frame, anchor='nw')

    #Identify active mode
    current_mode = get_mode()

    Label(mode_frame,wraplength=350,text="This menu is used to manage commenting modes.",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=70,sticky=W)
    Label(mode_frame,wraplength=450,text="Hashtag mode:\n Comment on posts that contain a "+
    "specific hashtag. \nThe bot will automatically and\n"+
    " continuously find new posts after commenting",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=1,column=0,padx=65,pady=15,sticky=W)
    Label(mode_frame,wraplength=350,text="Account mode:\n Comment on posts that have been posted by "+
    "specific accounts. These accounts can be modified in the 'targets' menu.",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=2,column=0,padx=30,sticky=W)
    Label(mode_frame,wraplength=350,text="Feed mode:\n Comment on posts in your active account\'s feed. This mode"+
    " will automatically refresh your feed and comment on new posts as they appear. If you want the bot to"+
    " rapidly refresh your feed and find new posts as fast as possible, turn on rapid refresh."
    " If rapid refresh is off, the bot will pretend to be human between refreshes.",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=4,column=0,padx=25,sticky=W)

    Label(mode_frame,wraplength=350,text="Hashtag Mode",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=5,column=0,padx=10,sticky=W)
    Button(mode_frame, text="Set", command=lambda: set_mode('hashtag')).grid(row=5,column=0,padx=100,pady=10,sticky=W)

    Label(mode_frame,wraplength=400,text="Account Mode",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=6,column=0,padx=10,sticky=W)
    Button(mode_frame, text="Set", command=lambda: set_mode('account')).grid(row=6,column=0,padx=100,pady=10,sticky=W)

    Label(mode_frame,wraplength=400,text="Feed Mode",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=8,column=0,padx=10,sticky=W)
    Button(mode_frame, text="Set", command=lambda: set_mode('feed')).grid(row=8,column=0,padx=100,pady=10,sticky=W)

    #Display the currently active mode
    active_mode_label = Label(mode_frame,wraplength=350,text=f"*Active mode: {current_mode}",fg="#F23636",anchor=NW,background="#4a5254")
    active_mode_label.grid(row=9,column=0,padx=10,sticky=W)

    top.update()
    mode_canvas.config(scrollregion=mode_canvas.bbox("all"))


def view_commented_list():
    '''Open a new window to view commented list'''
    top = Toplevel()
    top.title('Comment List')
    top.resizable(False, False)
    top.configure(bg="#4a5254")

    #Setup icon
    top.iconbitmap('icon.ico')

    vscrollbar = Scrollbar(top)

    commented_canvas = Canvas(top,width=400,height=300,background="#4a5254",yscrollcommand=vscrollbar.set)

    vscrollbar.config(command=commented_canvas.yview)
    vscrollbar.pack(side=RIGHT, fill=Y)

    commented_frame = Frame(commented_canvas) #Create the frame which will hold the widgets
    commented_frame.config(background="#4a5254")

    commented_canvas.pack(side="left", fill="both", expand=True)

    #Updated the window creation
    commented_canvas.create_window(0,0,window=commented_frame, anchor='nw')

    Label(commented_frame,wraplength=350,text="This menu is used to view the links to all posts that "+
    "have been commented on. Links can be removed.",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=10,sticky=W)

    #Display all hashtags
    counter = 1
    with open('commented_posts.txt', 'r') as f:
        lines = f.readlines()

        for count, line in enumerate(lines):
            label = Label(commented_frame,wraplength=400,text=f"{count+1}.  {line}",fg="#e8e8e8",anchor=NW,background="#4a5254")
            label.grid(row=counter,column=0,padx=10,sticky=W)
            Button(commented_frame, text="Remove", command=lambda line=line: remove_file_item(line,'commented', commented_frame, commented_canvas, top)).grid(row=counter,column=0,padx=340,sticky=W)
            counter += 1

    #Allow for clearing of the file
    Label(commented_frame,wraplength=350,fg="#e8e8e8",text="Clear commented posts (cannot be undone): ",anchor=NW,background="#4a5254").grid(row=counter,column=0,padx=10,sticky=W)
    Button(commented_frame, text="Clear", command=lambda: clear_file('commented_posts')).grid(row=counter,column=0,padx=260,pady=10,sticky=W)

    top.update()
    commented_canvas.config(scrollregion=commented_canvas.bbox("all"))


def view_hashtags():
    '''Open a new window to view commented list'''
    top = Toplevel()
    top.title('Hashtag List')
    top.resizable(False, False)
    top.configure(bg="#4a5254")

    #Setup icon
    top.iconbitmap('icon.ico')

    vscrollbar = Scrollbar(top)

    hashtag_canvas = Canvas(top,width=400,height=300,background="#4a5254",yscrollcommand=vscrollbar.set)

    vscrollbar.config(command=hashtag_canvas.yview)
    vscrollbar.pack(side=RIGHT, fill=Y)

    hashtag_frame = Frame(hashtag_canvas) #Create the frame which will hold the widgets
    hashtag_frame.config(background="#4a5254")

    hashtag_canvas.pack(side="left", fill="both", expand=True)

    #Updated the window creation
    hashtag_canvas.create_window(0,0,window=hashtag_frame, anchor='nw')

    Label(hashtag_frame,wraplength=350,text="This menu is used to view a list of hashtags. Used in conjunction"+
    "with the 'hashtag' comment mode.",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=10,sticky=W)

    #Display all hashtags
    counter = 1
    with open('hashtags.txt', 'r') as f:
        lines = f.readlines()

        for count, line in enumerate(lines):
            label = Label(hashtag_frame,wraplength=400,text=f"{count+1}.  {line}",fg="#e8e8e8",anchor=NW,background="#4a5254")
            label.grid(row=counter,column=0,padx=10,sticky=W)
            Button(hashtag_frame, text="Remove", command=lambda line=line: remove_file_item(line,'hashtag', hashtag_frame, hashtag_canvas, top)).grid(row=counter,column=0,padx=340,sticky=W)

            counter += 1

    #Allow for clearing of the file
    Label(hashtag_frame,wraplength=350,fg="#e8e8e8",text="Clear hashtags (cannot be undone): ",anchor=NW,background="#4a5254").grid(row=counter,column=0,padx=10,sticky=W)
    Button(hashtag_frame, text="Clear", command=lambda: clear_file('hashtags')).grid(row=counter,column=0,padx=220,pady=10,sticky=W)

    top.update()
    hashtag_canvas.config(scrollregion=hashtag_canvas.bbox("all"))


def manage_targets():
    '''Open a new window to manage a list of target accounts'''
    top = Toplevel()
    top.title('Target Manager')
    top.resizable(False, False)
    top.configure(bg="#4a5254")

    #Setup icon
    top.iconbitmap('icon.ico')

    vscrollbar = Scrollbar(top)

    target_canvas = Canvas(top,width=400,height=300,background="#4a5254",yscrollcommand=vscrollbar.set)

    vscrollbar.config(command=target_canvas.yview)
    vscrollbar.pack(side=RIGHT, fill=Y)

    target_frame = Frame(target_canvas) #Create the frame which will hold the widgets
    target_frame.config(background="#4a5254")

    target_canvas.pack(side="left", fill="both", expand=True)

    #Updated the window creation
    target_canvas.create_window(0,0,window=target_frame, anchor='nw')

    Label(target_frame,wraplength=350,text="This menu is used to view a list of target accounts. These "+
    "accounts are used in conjunction with the 'account' comment mode. The bot will comment "+
    "on posts made by accounts with usernames in this target list.",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=10,sticky=W)

    #Display all targets
    counter = 1
    with open('target_accounts.txt', 'r') as f:
        lines = f.readlines()

        for count, line in enumerate(lines):
            label = Label(target_frame,wraplength=400,text=f"{count+1}.  {line}",fg="#e8e8e8",anchor=NW,background="#4a5254")
            label.grid(row=counter,column=0,padx=10,sticky=W)
            Button(target_frame, text="Remove", command=lambda line=line: remove_file_item(line,'target', target_frame, target_canvas, top)).grid(row=counter,column=0,padx=340,sticky=W)
            counter += 1

    #Allow for clearing of the file
    Label(target_frame,wraplength=350,fg="#e8e8e8",text="Clear targets (cannot be undone): ",anchor=NW,background="#4a5254").grid(row=counter,column=0,padx=10,sticky=W)
    Button(target_frame, text="Clear", command=lambda: clear_file('target_accounts')).grid(row=counter,column=0,padx=220,pady=10,sticky=W)

    top.update()
    target_canvas.config(scrollregion=target_canvas.bbox("all"))


def update_data(data, ticket):
    '''Update list files with new comment
        ARGS:
            data:string: data to update list with
            ticket:string: data identifier to determine action taken
    '''
    if(data != ''): #Make sure empty data is not added

        if(ticket == 'comment'):
            if(data == ''):
                return
            else:
                with open("comments.txt", "a+", encoding='utf-8') as f: #Open to append the new comment
                    f.seek(0) #set the offset to file start
                    line = f.readline()

                    if (line == ''): #Check for empty file
                        f.write(f'{data}\n')
                    else:
                        f.write(f'{data}\n')

        elif(ticket == 'hashtag'):
            if(data == ''):
                return
            else:
                with open("hashtags.txt", "a+") as f: #Open to append the new comment
                    f.seek(0) #set the offset to file start
                    line = f.readline()

                    if (line == ''): #Check for empty file
                        f.write(f'{data}\n')
                    else:
                        f.write(f'{data}\n')

        elif(ticket == 'add_target'):
            if(data == ''):
                return
            else:
                with open("target_accounts.txt", "a+") as f: #Open to append the new comment
                    f.seek(0) #set the offset to file start
                    line = f.readline()

                    if (line == ''): #Check for empty file
                        f.write(f'{data}\n')
                    else:
                        f.write(f'{data}\n')


def remove_file_item(text, ticket, frame, canvas, root):
    '''Remove data from a file'''

    if ticket == 'hashtag':

        #Grab the lines, then write all but the target text
        with open('hashtags.txt', 'r') as f:
            lines = f.readlines()

        with open('hashtags.txt', 'w') as f:
            for line in lines:
                if(line != text):
                    f.write(line)

        frame.destroy()
        frame = Frame(canvas) #Create the frame which will hold the widgets
        frame.config(background="#4a5254")

        #Updated the window creation
        canvas.create_window(0,0,window=frame, anchor='nw')

        Label(frame,wraplength=350,text="This menu is used to view a list of hashtags. Used in conjunction"+
        "with the 'hashtag' comment mode.",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=10,sticky=W)

        #Display all hashtags
        counter = 1
        with open('hashtags.txt', 'r') as f:
            lines = f.readlines()

            for count, line in enumerate(lines):
                label = Label(frame,wraplength=400,text=f"{count+1}.  {line}",fg="#e8e8e8",anchor=NW,background="#4a5254")
                label.grid(row=counter,column=0,padx=10,sticky=W)
                Button(frame, text="Remove", command=lambda line=line: remove_file_item(line,'hashtag', frame, canvas, root)).grid(row=counter,column=0,padx=340,sticky=W)

                counter += 1

        #Allow for clearing of the file
        Label(frame,wraplength=350,fg="#e8e8e8",text="Clear hashtags (cannot be undone): ",anchor=NW,background="#4a5254").grid(row=counter,column=0,padx=10,sticky=W)
        Button(frame, text="Clear", command=lambda: clear_file('hashtags')).grid(row=counter,column=0,padx=220,pady=10,sticky=W)

        canvas.config(scrollregion=canvas.bbox("all"))

    elif ticket == 'comment':

        #Grab the lines, then write all but the target text
        with open('comments.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open('comments.txt', 'w', encoding='utf-8') as f:
            for line in lines:
                if(line != text):
                    f.write(line)

        frame.destroy()

        frame = Frame(canvas) #Create the frame which will hold the widgets
        frame.config(background="#4a5254")

        #Updated the window creation
        canvas.create_window(0,0,window=frame, anchor='nw')

        Label(frame,wraplength=350,fg="#e8e8e8",text="You can view your comment list in this menu. Each comment "+
        "displayed can be used to comment on a post. Comments are selected randomly for each post.",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=10,sticky=W)

        #Display all comments
        counter = 1
        with open('comments.txt', 'r') as f:
            lines = f.readlines()

            for count, line in enumerate(lines):
                label = Label(frame,wraplength=400,text=f"{count+1}.  {line}",fg="#e8e8e8",anchor=NW,background="#4a5254")
                label.grid(row=counter,column=0,padx=10,sticky=W)
                Button(frame, text="Remove", command=lambda line=line: remove_file_item(line,'comment', frame, canvas, root)).grid(row=counter,column=0,padx=340,sticky=W)
                counter += 1

        #Allow for clearing of the file
        Label(frame,wraplength=350,fg="#e8e8e8",text="Clear comments (cannot be undone): ",anchor=NW,background="#4a5254").grid(row=counter,column=0,padx=10,sticky=W)
        Button(frame, text="Clear", command=lambda: clear_file('comments')).grid(row=counter,column=0,padx=230,pady=10,sticky=W)

    elif ticket == 'commented':

        #Grab the lines, then write all but the target text
        with open('commented_posts.txt', 'r') as f:
            lines = f.readlines()

        with open('commented_posts.txt', 'w') as f:
            for line in lines:
                if(line != text):
                    f.write(line)


        frame.destroy()

        frame = Frame(canvas) #Create the frame which will hold the widgets
        frame.config(background="#4a5254")

        #Updated the window creation
        canvas.create_window(0,0,window=frame, anchor='nw')

        Label(frame,wraplength=350,text="This menu is used to view the links to all posts that "+
        "have been commented on. Links can be removed.",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=10,sticky=W)

        #Display all hashtags
        counter = 1
        with open('commented_posts.txt', 'r') as f:
            lines = f.readlines()

            for count, line in enumerate(lines):
                label = Label(frame,wraplength=400,text=f"{count+1}.  {line}",fg="#e8e8e8",anchor=NW,background="#4a5254")
                label.grid(row=counter,column=0,padx=10,sticky=W)
                Button(frame, text="Remove", command=lambda line=line: remove_file_item(line,'commented', frame, canvas, root)).grid(row=counter,column=0,padx=340,sticky=W)
                counter += 1

        #Allow for clearing of the file
        Label(frame,wraplength=350,fg="#e8e8e8",text="Clear commented posts (cannot be undone): ",anchor=NW,background="#4a5254").grid(row=counter,column=0,padx=10,sticky=W)
        Button(frame, text="Clear", command=lambda: clear_file('commented_posts')).grid(row=counter,column=0,padx=260,pady=10,sticky=W)

    elif ticket == 'target':

        #Grab the lines, then write all but the target text
        with open('target_accounts.txt', 'r') as f:
            lines = f.readlines()

        with open('target_Accounts.txt', 'w') as f:
            for line in lines:
                if(line != text):
                    f.write(line)

        frame.destroy()

        frame = Frame(canvas) #Create the frame which will hold the widgets
        frame.config(background="#4a5254")

        #Updated the window creation
        canvas.create_window(0,0,window=frame, anchor='nw')

        Label(frame,wraplength=350,text="This menu is used to view a list of target accounts. These "+
        "accounts are used in conjunction with the 'account' comment mode. The bot will comment "+
        "on posts made by accounts with usernames in this target list.",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=10,sticky=W)

        #Display all targets
        counter = 1
        with open('target_accounts.txt', 'r') as f:
            lines = f.readlines()

            for count, line in enumerate(lines):
                label = Label(frame,wraplength=400,text=f"{count+1}.  {line}",fg="#e8e8e8",anchor=NW,background="#4a5254")
                label.grid(row=counter,column=0,padx=10,sticky=W)
                Button(frame, text="Remove", command=lambda line=line: remove_file_item(line,'target', frame, canvas, root)).grid(row=counter,column=0,padx=340,sticky=W)
                counter += 1

        #Allow for clearing of the file
        Label(frame,wraplength=350,fg="#e8e8e8",text="Clear targets (cannot be undone): ",anchor=NW,background="#4a5254").grid(row=counter,column=0,padx=10,sticky=W)
        Button(frame, text="Clear", command=lambda: clear_file('target_accounts')).grid(row=counter,column=0,padx=220,pady=10,sticky=W)


    elif ticket == 'account':

        #Grab the lines, then write all but the target text
        with open('accounts.txt', 'r') as f:
            lines = f.readlines()

        with open('accounts.txt', 'w') as f:
            for line in lines:
                if(line != text):
                    f.write(line)

        frame.destroy()

        frame = Frame(canvas) #Create the frame which will hold the widgets
        frame.config(background="#4a5254")
        canvas.create_window(0,0, window=frame, anchor = 'nw')

        #Add account
        Label(frame,wraplength=350,text="Add account:",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=10,sticky=W)
        Label(frame,wraplength=350,text="Username:",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=1,column=0,padx=10,sticky=W)
        username = Entry(frame, width = 30, bg = 'white')
        username.grid(row=1,column=0,padx=100,rowspan=1,sticky=W)

        Label(frame,wraplength=350,text="Password:",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=2,column=0,padx=10,sticky=W)
        password = Entry(frame, width = 30, bg = 'white')
        password.grid(row=2,column=0,padx=100,rowspan=1,sticky=W)
        Button(frame, text="Add", command=lambda: add_account(username.get(),password.get(), frame, canvas, root)).grid(row=2,column=0,padx=300,sticky=W)

        #Display accounts
        counter = 3
        with open('accounts.txt', 'r') as f:
            lines = f.readlines()

            for count, line in enumerate(lines):
                #Split up password and username data
                user, pword = line[:line.find(':')], line[line.find(':')+1:]
                u_label = Label(frame,wraplength=400,text=f"{count+1}.  Username: {user}",fg="#e8e8e8",anchor=NW,background="#4a5254")
                u_label.grid(row=counter,column=0,padx=10,sticky=W)
                counter += 1
                p_label = Label(frame,wraplength=400,text=f"     Password: {pword}",fg="#e8e8e8",anchor=NW,background="#4a5254")
                p_label.grid(row=counter,column=0,padx=10,sticky=W)

                Button(frame,text="Remove",command=lambda line=line: remove_file_item(line,'account', frame, canvas, root)).grid(row=counter,column=0,padx=340,sticky=W)

                counter += 1

        Label(frame,wraplength=350,text="Clear accounts (Cannot be undone):",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=counter,column=0,padx=10,pady=10,sticky=W)
        Button(frame, text="Clear", command=lambda: clear_file('accounts')).grid(row=counter,column=0,padx=230,pady=10,sticky=W)


def clear_file(file):
    '''Reset a file (make blank)
        ARGS:
            file:str: filename (without extension) to clear
    '''
    with open(file+'.txt', 'w') as f:
        pass


def add_account(user, password, account_frame, account_canvas, top):
    '''Add an account to the account list. 'accounts' file is formatted like so:
        usernamehere:userpasswordhere
        ARGS:
            user:str: account username
            pass:str: account password
    '''
    if(user == '' or password == ''): #Invalid data handling
        pass
    else:
        #Add data to accounts file
        with open("accounts.txt", "a+") as f:
            f.seek(0) #Move to file start
            line = f.readline()

            if (line == ''):
                f.write(f'{user}:{password}\n')
            else:
                f.write(f'{user}:{password}\n')

    account_frame.destroy()

    account_frame = Frame(account_canvas) #Create the frame which will hold the widgets
    account_frame.config(background="#4a5254")
    account_canvas.create_window(0,0, window=account_frame, anchor = 'nw')

    #Add account
    Label(account_frame,wraplength=350,text="Add account:",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=10,sticky=W)
    Label(account_frame,wraplength=350,text="Username:",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=1,column=0,padx=10,sticky=W)
    username = Entry(account_frame, width = 30, bg = 'white')
    username.grid(row=1,column=0,padx=100,rowspan=1,sticky=W)

    Label(account_frame,wraplength=350,text="Password:",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=2,column=0,padx=10,sticky=W)
    password = Entry(account_frame, width = 30, bg = 'white')
    password.grid(row=2,column=0,padx=100,rowspan=1,sticky=W)
    Button(account_frame, text="Add", command=lambda: add_account(username.get(),password.get(), account_frame, account_canvas, top)).grid(row=2,column=0,padx=300,sticky=W)

    #Display accounts
    counter = 3
    with open('accounts.txt', 'r') as f:
        lines = f.readlines()

        for count, line in enumerate(lines):
            #Split up password and username data
            user, pword = line[:line.find(':')], line[line.find(':')+1:]
            u_label = Label(account_frame,wraplength=400,text=f"{count+1}.  Username: {user}",fg="#e8e8e8",anchor=NW,background="#4a5254")
            u_label.grid(row=counter,column=0,padx=10,sticky=W)
            counter += 1
            p_label = Label(account_frame,wraplength=400,text=f"     Password: {pword}",fg="#e8e8e8",anchor=NW,background="#4a5254")
            p_label.grid(row=counter,column=0,padx=10,sticky=W)

            Button(account_frame,text="Remove",command=lambda line=line: remove_file_item(line,'account', account_frame, account_canvas, top)).grid(row=counter,column=0,padx=340,sticky=W)

            counter += 1

    Label(account_frame,wraplength=350,text="Clear accounts (Cannot be undone):",fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=counter,column=0,padx=10,pady=10,sticky=W)
    Button(account_frame, text="Clear", command=lambda: clear_file('accounts')).grid(row=counter,column=0,padx=230,pady=10,sticky=W)


def toggle_refresh_mode():
    '''set the programs refresh mode (used with feed mode)'''
    with open('config.txt', 'r') as f: #Clear file
        lines = f.readlines()
        for line in lines:
            if 'emulation_flag' in line:
                key = line[15:]
                key = key.strip('\n')

    with open('config.txt', 'w') as f: #Rewrite file w/ new refresh mode

        for line in lines:
            if('emulation_flag' in line):
                if key == 'True':
                    i = line.find('=')
                    flag = 'False'
                    line = line[:i+1] + flag + '\n' #Reconstruct the mode line
                    f.write(line)
                else:
                    i = line.find('=')
                    flag = 'True'
                    line = line[:i+1] + flag + '\n' #Reconstruct the mode line
                    f.write(line)
            else:
                f.write(line)

    #Update label
    if flag == 'True':
        display_flag = 'on'
    else:
        display_flag = 'off'
    refresh_mode_label.configure(text=f"*Rapid Refresh: {display_flag}")


def set_mode(mode):
    '''Set the programs commenting mode
        ARGS:
            mode:str: target mode to set'''

    with open('config.txt', 'r') as f: #Clear file
        lines = f.readlines()

    with open('config.txt', 'w') as f: #Rewrite file w/ new mode

        for line in lines:
            if 'mode' in line:
                i = line.find('=')
                line = line[:i+1] + mode + '\n' #Reconstruct the mode line
                f.write(line)
            else:
                f.write(line)

    #Update label
    active_mode_label.configure(text=f"*Active mode: {mode}")


def set_refresh_timer(time):
    '''Set the current refresh timer
        ARGS:
            time:str: desired refresh rate time value'''

    with open('config.txt', 'r') as f:
        lines = f.readlines()

    with open('config.txt', 'w') as f:

        for line in lines:
            if 'refresh_timer' in line:

                try: #Ensure we have valid input
                    time = float(time)
                    if time >= 0:
                        line = 'refresh_timer='+str(time)+'\n'
                        f.write(line)

                    else:#If negative, set to 0
                        line = 'refresh_timer=0\n'
                        f.write(line)
                        time = 0

                except ValueError:
                    line = 'refresh_timer=0\n'
                    f.write(line)
                    time = 0

            else:
                f.write(line)

    refresh_timer.configure(text=f"*Current refresh rate: {time}")


def set_account_swap_timer(value):
    '''Set the timer for accoutn swaps in feed mode.
        ARGS:
            value:str: new timer value (seconds)
    '''
    #Get config lines
    with open('config.txt', 'r') as f:
        lines = f.readlines()

    with open('config.txt', 'w') as f:
        for line in lines:
            if 'account_swap_timer' in line:
                line = f'account_swap_timer={value}\n'
                f.write(line)
            else:
                f.write(line)

    acc_swap_label.configure(text=f"*Current swap timer: {value}")


def set_feed_behavior(mode):
    '''Set the behavior
        ARGS:
            mode:str: behavior type for feed mode'''

    #Open file and replace mode
    with open('config.txt', 'r') as f:
        lines = f.readlines()

    with open('config.txt', 'w') as f:
        for line in lines:

            if 'feed_behavior' in line:
                line = 'feed_behavior='+mode+'\n'
                f.write(line)
            else:
                f.write(line)

    behavior_label.configure(text=f"*Current feed behavior: {mode}")


def set_age_limiter(limit):
    '''Set the max-post age limit when commenting in feed mode
        ARGS:
            limit:str: users desired max age limit'''

    with open('config.txt', 'r') as f:
        lines = f.readlines()

    with open('config.txt', 'w') as f:
        for line in lines:

            if 'post_age_limit' in line:
                try:
                    limit = int(limit)
                    if limit >= 3540: #max post age limit is 5 mins (300 secs)
                        limit = 3540
                    elif limit <= 0:
                        limit = 1 #must at-least be a second old

                    line = 'post_age_limit='+str(limit)+'\n'
                    f.write(line)

                except ValueError:
                    line = 'post_age_limit=1\n'
                    f.write(line)
                    limit = 1

            else:
                f.write(line)

    current_age_label.configure(text=f"*Current post age-limit: {limit}")


def get_account_swap_timer():
    '''return the account timer as an int'''

    #Get config lines
    with open('config.txt', 'r') as f:
        lines = f.readlines()

    for line in lines:
        if 'account_swap_timer' in line:
            value = line[19:].strip('\n')
            break

    return int(value) #Cast the value


def get_age_limiter():
    '''return the current age limit value'''

    with open('config.txt', 'r') as f:
        lines = f.readlines()

        for line in lines:
            if 'post_age_limit' in line:
                limit = line[15:]
                break
    return limit


def get_feed_behavior():
    '''return the current feed behavior'''

    with open('config.txt', 'r') as f:
        lines = f.readlines()

        for line in lines:
            if 'feed_behavior' in line:
                behav = line[14:]
                behav = behav.strip('\n')
                break
    return behav


def get_refresh_timer():
    '''return the current refresh timer value'''

    with open('config.txt', 'r') as f:
        lines = f.readlines()

        for line in lines:
            if 'refresh_timer' in line:
                time = line[14:]
                break
    return time

def get_mode():
    '''Return the currently active mode'''

    with open('config.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if('mode' in line):
                current_mode = line[5:].strip('\n')

    return current_mode


def get_refresh_mode():
    '''Return the currently active refresh mode'''
    with open('config.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if('emulation_flag' in line):
                current_mode = line[15:].strip('\n')

    return current_mode


def create_bot_thread(threads):
    '''Create a new thread to run a bot.
        ARGS:
            threads:list: list of all threads
    '''
    #Create the thread and append it
    new_thread = threading.Thread(target=begin_commenting)
    threads.append(new_thread)
    new_thread.start()


def begin_commenting():
    '''Initialize a bot, and begin commenting. Commenting mode determines behavior'''

    #Get active mode
    with open('config.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'mode' in line:
                mode = line[5:]

    mode = mode.strip('\n')

    add_console_message(f'Commenting intialized with mode [{mode}]') #Update console

    if(mode == 'account'):
        #Select an account
        with open('accounts.txt', 'r') as f:
            lines = f.readlines()
            account = random.choice(lines)

        user, pword = account[:account.find(':')].strip('\n'), account[account.find(':')+1:].strip('\n')

        add_console_message(f'New bot initialized with credentials [{user}], [{pword}]') #Update console

        bot = CommentBot(user, pword, mode)

    elif(mode == 'hashtag'):
        #Select an account
        with open('accounts.txt', 'r') as f:
            lines = f.readlines()
            account = random.choice(lines)

        user, pword = account[:account.find(':')].strip('\n'), account[account.find(':')+1:].strip('\n')

        add_console_message(f'New bot initialized with credentials [{user}], [{pword}]') #Update console

        bot = CommentBot(user, pword, mode)

    elif(mode == 'feed'):
        #Select an account
        with open('accounts.txt', 'r') as f:
            lines = f.readlines()
            account = random.choice(lines)

        user, pword = account[:account.find(':')].strip('\n'), account[account.find(':')+1:].strip('\n')

        add_console_message(f'New bot initialized with credentials [{user}], [{pword}]') #Update console

        bot = CommentBot(user, pword, mode)


def add_console_message(new_data):
    '''Update the console with data'''

    shared.console_msgs = shared.console_msgs+"\n"+new_data #Update msgs & console

    if(shared.console_open == True):
        try:
            console_text.configure(text=f"{shared.console_msgs}")
        except Exception:
            pass


def invalid_interface():
    '''Notify user program has not been installed'''
    #Setup up new 'root' window
    root = Tk()
    root.title('Installation Invalid')
    root.resizable(False, False)
    root.configure(bg="#4a5254")

    #Setup icon
    root.iconbitmap('icon.ico')

    msg = '''This installation of the software is invalid. Either the bot is not being
             run on the machine it was originally installed on, or the copy is invalid.
             If the copy is invalid, consider purchasing the comment bot.
          '''

    Label(root,wraplength=500,text=msg,fg="#e8e8e8",anchor=NW,background="#4a5254").grid(row=0,column=0,padx=10,sticky=W)

    mainloop()


def GetUUID():
    '''
    Obtain the (windows) machine's unique uuid. This is
    done by executing a command in the cmd prompt.
    '''
    cmd = 'wmic csproduct get uuid'
    uuid = str(popen(cmd))
    #uuid = str(subprocess.check_output(cmd))
    pos1 = uuid.find("\\n")+2
    uuid = uuid[pos1:-15]
    return uuid


def popen(cmd: str) -> str:
    """
    For pyinstaller -w.
    To be honest, I copied this function & this one only from stackoverflow
    (thanks TheCloclTwister). This function is needed to call a subprocess
    without opening the cmd window, and it will return the result of the cmd.
    """
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(cmd,startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return process.stdout.read()


if __name__ == "__main__":
    #Grab machine uuid & search db for uuid existence.
    machine_id = GetUUID()
    signature = None

    database = mysql.connector.connect(host="redacted",
                                       user="redacted",
                                       passwd="redacted",
                                       database="redacted")
    data_cursor = database.cursor()

    query = "SELECT signature FROM client WHERE signature = %s"
    data_cursor.execute(query, (machine_id, ))

    for entry in data_cursor:
        signature = entry[0]

    data_cursor.close()
    database.close()

    #If signature exists in database, launch interface.
    if signature == machine_id:
        main()
    else:
        invalid_interface()
