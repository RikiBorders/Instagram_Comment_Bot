import mysql.connector
import os
import subprocess
from tkinter import *


def GetUUID():
    '''
    Obtain the (windows) machine's unique uuid. This is
    done by executing a command in the cmd prompt.
    '''
    cmd = 'wmic csproduct get uuid'
    uuid = str(subprocess.check_output(cmd))
    pos1 = uuid.find("\\n")+2
    uuid = uuid[pos1:-15]
    return uuid


def verify_license_key(key):
    '''
    Check if the inputted license key is enabled.
    If the key is enabled, then we will disable it, and
    return true. NOTE: Disabled = false (0), and
    enabled = true (1).
    '''
    license = None
    client_signature = None
    database = mysql.connector.connect(host="redacted",
                                       user="redacted",
                                       passwd="redacted",
                                       database="redacted")
    data_cursor = database.cursor()

    #Get & extract the target license key
    query = "SELECT license_key FROM license WHERE license_key = %s"
    data_cursor.execute(query, (key, ))

    for entry in data_cursor: #Obtain license column
        license = entry[0]

    #If the license doesnt exist, close database and return
    if license == None:
        data_cursor.close()
        database.close()
        return

    #Get and extract uuid incase of reinstallation.
    data_cursor.execute("SELECT bound_id FROM license WHERE license_key = %s", (key,))
    for entry in data_cursor:
        client_id = entry[0]

    data_cursor.execute("SELECT signature FROM client WHERE client_id = %s", (client_id,))
    for entry in data_cursor:
        client_signature = entry[0]

    #Check key status. If enabled, disabled and return true
    query = "SELECT license_status FROM license WHERE license_key = %s"
    data_cursor.execute(query, (key, ))

    for entry in data_cursor: #Obtain status column
        status = entry[0]

    if status or GetUUID() == client_signature: #Disable key, close database, setup files
        query = "UPDATE license SET license_status = 0 WHERE license_key = %s"
        data_cursor.execute(query, (key,))

        database.commit()
        data_cursor.close()
        database.close()
        setup_files(key)

    else: #Close database.
        data_cursor.close()
        database.close()
        show_installation_failed()


def setup_files(key):
    '''
    Retrieve pc UUID, and send it to the database and save as the client's
    signature.
    '''
    #Set client UUID
    UUID = GetUUID()

    #Open database and select key's associated client
    database = mysql.connector.connect(host="redacted",
                                       user="redacted",
                                       passwd="redacted",
                                       database="redacted")
    data_cursor = database.cursor()

    data_cursor.execute("SELECT bound_id FROM license WHERE license_key = %s", (key,))
    for entry in data_cursor:
        client_id = entry[0]

    #Set the client's signature as their uuid
    query = "UPDATE client SET signature = %s WHERE client_id = %s"
    data_cursor.execute(query, (UUID, client_id,))

    #Close database & commit
    database.commit()
    data_cursor.close()
    database.close()

    #Write standard text files
    with open('accounts.txt', 'w+') as f:
        pass
    with open('commented_posts.txt', 'w+') as f:
        pass
    with open('comments.txt', 'w+') as f:
        pass
    with open('hashtags.txt', 'w+') as f:
        pass
    with open('sources.txt', 'w+') as f:
        pass
    with open('target_accounts.txt', 'w+') as f:
        pass
    #setup config file
    with open('config.txt', 'w+') as f:
        f.write('mode=feed\n')
        f.write('emulation_flag=True\n')
        f.write('refresh_timer=12.0\n')
        f.write('feed_behavior=top\n')
        f.write('post_age_limit=60\n')
        f.write('account_swap_timer=1800\n')
        f.write('fullscreen=True\n')

    #Indicate to user that installation was a success
    show_installation_complete()


def show_installation_complete():
    '''
    Show user window indicating that installation completed successfully.
    '''
    root = Tk()
    root.title('Installation Complete!')
    root.resizable(False, False)
    root.configure(bg="#464646")
    main_canvas = Canvas(root,width=450,height=100,background="#4a5254")
    main_frame = Frame(main_canvas) #Create the frame which will hold the widgets
    main_frame.config(background="#4a5254")

    main_canvas.pack(side="left", fill="both", expand=True)
    main_canvas.create_window(0,0,window=main_frame, anchor='nw')

    #Setup icon
    root.iconbitmap('icon.ico')

    success_message = """                Installation has been completed successfully!
                      To run the bot, close this window and run comment_bot.exe.
                      The bot can only be installed on one machine at a time. If you
                      Have any questions, contact RKAB support.
                      Be sure to subscribe on youtube: redacted"""

    Label(main_frame,wraplength=500,text=success_message,fg="#e8e8e8",anchor=W,background="#4a5254").grid(row=0,column=0,sticky=W)

    mainloop()


def show_installation_failed():
    '''
    Show user window indicating that installation failed.
    '''
    root = Tk()
    root.title('Installation Failed.')
    root.resizable(False, False)
    root.configure(bg="#464646")
    main_canvas = Canvas(root,width=500,height=100,background="#4a5254")
    main_frame = Frame(main_canvas) #Create the frame which will hold the widgets
    main_frame.config(background="#4a5254")

    main_canvas.pack(side="left", fill="both", expand=True)
    main_canvas.create_window(0,0,window=main_frame, anchor='nw')

    #Setup icon
    root.iconbitmap('icon.ico')

    fail_message = """            Installation could not be complete. This can be the result
                         of various things. Remember that the bot can only be installed on
                         one computer. If you need to install the bot on a new computer,
                         contact RKAB support. Be sure to check out redacted on instagram,
                         and subscribe on youtube: redacted"""

    Label(main_frame,wraplength=500,text=fail_message,fg="#e8e8e8",anchor=W,background="#4a5254").grid(row=0,column=0,sticky=W)

    mainloop()


def installation_interface():
    '''
    Preliminary screen for bot installation. Ask the user for their
    license key, then verify with database.
    '''
    root = Tk()
    root.title('RKAB Comment Bot Installer')
    root.resizable(False, False)
    root.configure(bg="#464646")
    main_canvas = Canvas(root,width=500,height=100,background="#4a5254")
    main_frame = Frame(main_canvas) #Create the frame which will hold the widgets
    main_frame.config(background="#4a5254")

    main_canvas.pack(side="left", fill="both", expand=True)
    main_canvas.create_window(0,0,window=main_frame, anchor='nw')

    #Setup icon
    root.iconbitmap('icon.ico')

    Label(main_frame,wraplength=500,text='Enter your license key below',fg="#e8e8e8",anchor=W,background="#4a5254").grid(row=0,column=0,sticky=W)
    key = Entry(main_frame, width = 30, bg = 'white')
    key.grid(row=1,column=0,sticky=W)
    Button(main_frame, text="Submit", command=lambda: verify_license_key(key.get())).grid(row=1,column=1,padx=10,sticky=W)

    mainloop()


if __name__ == "__main__":
    installation_interface()
