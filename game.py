import random
import curses
import unit
import math
import area
import item
import brain
import gameCalc
import time

units = []
areas = []
items = []
msg_credits = 3
hour = 0

def defineUnits(num):
    for i in range(num):
        work = random.randint(5,20)
        search = random.randint(5,20)
        ind = random.randint(1,20)
        guy = unit.unit(i+1,0,work,search,ind)
        units.append(guy)
    for i in range(num):
        for j in range(num):
            score = 50
            if i == j:
                score = 50
            units[i].opinions.append(brain.opinion(i + 1,score))

def getBadGuys(num):
    numOfGuys = math.ceil(num/5)
    for i in range(numOfGuys):
        x = random.randint(0, num - 1)
        bad = units[x]
        if bad.role == 0:
            bad.role = 1
        else:
            i = i - 1

def defineArea(tasks):
    h = math.floor(tasks / 6)
    m = math.floor(tasks / 3)
    e = tasks - h - m
    #monitor Room
    MR = area.area("Monitor room")
    MR.easy_tasks = 0
    MR.med_tasks = 0
    MR.hard_tasks = 0
    #kitchen
    K = area.area("Kitchen")
    K.easy_tasks = 0
    K.med_tasks = 0
    K.hard_tasks = 0
    #server room
    S = area.area("Server room")
    S.easy_tasks = 0
    S.med_tasks = 0
    S.hard_tasks = 0
    #storage room
    sto = area.area("Storage")
    sto.easy_tasks = 0
    sto.med_tasks = 0
    sto.hard_tasks = 0
    #power room
    p = area.area("Power room")
    p.easy_tasks = 0
    p.med_tasks = 0
    p.hard_tasks = 0
    #rand
    for i in range(h):
        x = random.randint(1,5)
        match x:
            case 1:
                MR.hard_tasks += 1
            case 2:
                K.hard_tasks += 1
            case 3:
                S.hard_tasks += 1
            case 4:
                sto.hard_tasks += 1
            case 5:
                p.hard_tasks += 1
    for i in range(m):
        x = random.randint(1,5)
        match x:
            case 1:
                MR.med_tasks += 1
            case 2:
                K.med_tasks += 1
            case 3:
                S.med_tasks += 1
            case 4:
                sto.med_tasks += 1
            case 5:
                p.med_tasks += 1
    for i in range(e):
        x = random.randint(1,5)
        match x:
            case 1:
                MR.easy_tasks += 1
            case 2:
                K.easy_tasks += 1
            case 3:
                S.easy_tasks += 1
            case 4:
                sto.easy_tasks += 1
            case 5:
                p.easy_tasks += 1
    #add
    MR.camera = True
    MR.sensor = True
    areas.append(MR)
    areas.append(S)
    areas.append(p)
    areas.append(K)
    areas.append(sto)
    for i in range(len(areas)):
        areas[i].needed = 20 * areas[i].easy_tasks + 40 * areas[i].med_tasks + 60 * areas[i].hard_tasks
        areas[i].easy_limit = 20 * areas[i].easy_tasks

def addItems():
    for k in range(len(areas)):
        for i in range(areas[k].hard_tasks):
            if areas[k].id == "Monitor room":
                items.append(item.item("Ethernet cord", 0, "Monitor room", 2))
                items.append(item.item("Computer", 0, "Monitor room", 2))
            if areas[k].id == "Kitchen":
                items.append(item.item("Knife", 2, "Kitchen", 2))
                items.append(item.item("Bag of rice", 0, "Kitchen", 2))
            if areas[k].id == "Server room":
                items.append(item.item("Screw Driver", 1, "Server room", 2))
                items.append(item.item("Server", 0, "Server room", 2))
            if areas[k].id == "Power room":
                items.append(item.item("Power cell", 0, "Power room", 2))
                items.append(item.item("Large piston", 0, "Power room", 2))
            if areas[k].id == "Storage":
                items.append(item.item("Cleaning Spray", 0, "Storage", 2))
                items.append(item.item("Broom", 0, "Storage", 2))
    for k in range(len(areas)):
        for i in range(areas[k].med_tasks):
            if areas[k].id == "Monitor room":
                items.append(item.item("Monitor", 0, "Monitor room", 1))
            if areas[k].id == "Kitchen":
                items.append(item.item("Meat", 0, "Kitchen", 1))
            if areas[k].id == "Server room":
                items.append(item.item("Rails", 0, "Server room", 1))
            if areas[k].id == "Power room":
                items.append(item.item("Small piston", 0, "Power room", 1))
            if areas[k].id == "Storage":
                items.append(item.item("Bucket", 1, "Storage", 1))
    for i in range(7):
        x = random.randint(1, 7)
        match x:
            case 1:
                items.append(item.item("Camera", 0, "Monitor room", 0))
            case 2:
                items.append(item.item("Sensor", 0, "Monitor room", 0))
            case 3:
                items.append(item.item("Gun", 3, "None", 0))
            case 4:
                items.append(item.item("Shorty", 4, "None", 0))
            case 5:
                items.append(item.item("Glass shard", 1, "None", 0))
            case 6:
                items.append(item.item("Pizza", 0, "Monitor room", 0))
            case 7:
                items.append(item.item("Work Gloves", 0, "Monitor room", 0))
    items.append(item.item("Gun", 3, "None", 0))
    #all items in - need to distribute
    for i in range(len(items)):
        x = random.randint(0,4)
        areas[x].items.append(items[i])



def homeScreen(stdscr):
    # Clear screen
    stdscr.clear()
    
    # Define dimensions
    menu_width = 30
    height, width = stdscr.getmaxyx()  # Get screen dimensions
    
    buttons = ["MANAGE", "TASKS", "LOG", "EXECUTE"]

    selected = 0
    camera_area = 0

    while True:
        stdscr.clear()

        # Display menu on the left side
        for idx, button in enumerate(buttons):
            if idx == selected:
                stdscr.addstr(idx, 0, button, curses.A_REVERSE)
            else:
                stdscr.addstr(idx, 0, button)
        
        # Display content on the right side
        content_start_x = menu_width + 1
        stdscr.addstr(0, content_start_x, "C A M E R A - 0 "+ str(camera_area + 1) +" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        for i in range(30):
            if i % 2 == 0:
                stdscr.addstr(1 + i, content_start_x, "|")
            else:
                stdscr.addstr(1 + i, content_start_x, " ")
        camera(stdscr, areas[camera_area])
        # Get user input
        key = stdscr.getch()

        # Navigate buttons
        if key == ord('w') and selected > 0:
            selected -= 1
        elif key == ord('s') and selected < len(buttons) - 1:
            selected += 1
        elif key == ord('d') and camera_area < len(areas) - 1:
            camera_area += 1
        elif key == ord('a') and camera_area > 0:
            camera_area -= 1
        elif key == ord('q'):
            break
        elif key == ord(' '):  # Enter key
            stdscr.clear()
            match selected:
                #Player Command
                case 0:
                    #launch management menu
                    management_screen(stdscr)
                #Task List
                case 1:
                    task_screen(stdscr)
                #LOG List
                case 2:
                    None
                #Execute
                case 3:
                    None
            stdscr.addstr(0, content_start_x, f"Selected: {buttons[selected]}")
            stdscr.refresh()
            stdscr.getch()  # Wait for another key press to exit
            break
        curses.doupdate()
        stdscr.refresh()
def display_monitor(stdscr, num):
    content_start_x = 30 + 1
    stdscr.addstr(0, content_start_x, "M O N I T O R - 0 "+ str(num) +" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    for i in range(30):
        if i % 2 == 0:
            stdscr.addstr(1 + i, content_start_x, "|")
        else:
            stdscr.addstr(1 + i, content_start_x, " ")
def task_screen(stdscr):
    stdscr.clear()
    buttons = ["START WORK", "BACK"]
    selected = 0
    while True:
        display_monitor(stdscr, 2)
        space = 0
        stdscr.addstr(1, 55, "Task Terminal")
        for i in range(len(areas)):
            total = areas[i].needed
            if total <= 0:
                areas[i].needed = 1
                areas[i].progress = 1
            progress = math.floor(20 * (areas[i].progress / total))
            stdscr.addstr(2 + i + space, 32, "+------------------------------------------------------------------+")
            stdscr.addstr(3 + i+ space, 33, areas[i].id)
            stdscr.addstr(3 + i+ space, 50, "[" + str("=" * progress) + ">")
            stdscr.addstr(3 + i+ space, 72, "] " + str(math.ceil(100 * areas[i].progress / areas[i].needed))+"%")
            stdscr.addstr(3 + i+ space, 80, "Items Needed: " + str(areas[i].med_tasks + (2 * areas[i].hard_tasks)))
            space += 2
        for i in range(len(buttons)):
            if i == selected:
                stdscr.addstr(i, 0, buttons[i], curses.A_REVERSE)
            else:
                stdscr.addstr(i, 0, buttons[i])
        
        key = stdscr.getch()
        if key == ord('w') and selected > 0:
            selected -= 1
        elif key == ord('s') and selected < len(buttons) - 1:
            selected += 1
        elif key == ord(" "):
            if selected == 0:
                #RUN THE HOUR
                #hour += 1
                gameCalc.runTheHour(units, areas)

            else:
                homeScreen(stdscr)




def management_screen(stdscr):
    stdscr.clear()
    buttons = ["DIRECT", "MESSAGE", "BACK"]
    selected = 0
    selected_unit = 0
    selected_loc = 0
    selected_units = []
    while True:
        stdscr.clear()
        # Display menu on the left side
        for idx, button in enumerate(buttons):
            if idx == selected:
                stdscr.addstr(idx, 0, button, curses.A_REVERSE)
            else:
                stdscr.addstr(idx, 0, button)
        
        # Display content on the right side
        content_start_x = 30 + 1
        stdscr.addstr(0, content_start_x, "M O N I T O R - 0 1 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        for i in range(30):
            if i % 2 == 0:
                stdscr.addstr(1 + i, content_start_x, "|")
            else:
                stdscr.addstr(1 + i, content_start_x, " ")
        # Get user input
        stdscr.addstr(2, 32, "+------------------+-------------------------+---------------------+")
        stdscr.addstr(3, 32, "|  ENGINEERING ID  |                         |        STATUS       |")
        stdscr.addstr(4, 32, "+------------------+-------------------------+---------------------+")
        space = 0
        for i in range(len(units)):
            stdscr.addstr(5 + i + space, 32, "Name: Unit #" + str(units[i].id))
            space += 1
        space = 0
        for i in range(len(units)):
            status = "DEAD"
            if not units[i].knownDead:
                status = "ALIVE"
            stdscr.addstr(5 + i + space, 86, status, curses.A_STANDOUT)
            space += 1
        key = stdscr.getch()

        # Navigate buttons
        if key == ord('w') and selected > 0:
            selected -= 1
        elif key == ord('s') and selected < len(buttons) - 1:
            selected += 1
        elif key == ord('q'):
            break
        elif key == ord(' '):  # Enter key
            stdscr.clear()
            match selected:
                case 1:
                    if msg_credits > 0:
                        #allow to send
                        while True:
                            stdscr.clear()
                            # Display menu on the left side
                            
                            # Display content on the right side
                            content_start_x = 30 + 1
                            stdscr.addstr(0, 0, "Choose who to message")
                            stdscr.addstr(0, content_start_x, "M O N I T O R - 0 1 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
                            for i in range(30):
                                if i % 2 == 0:
                                    stdscr.addstr(1 + i, content_start_x, "|")
                                else:
                                    stdscr.addstr(1 + i, content_start_x, " ")
                            # Get user input
                            stdscr.addstr(2, 32, "+------------------+-------------------------+---------------------+")
                            stdscr.addstr(3, 32, "|  ENGINEERING ID  |                         |        STATUS       |")
                            stdscr.addstr(4, 32, "+------------------+-------------------------+---------------------+")
                            space = 0
                            for i in range(len(units)):
                                if i == selected_unit:
                                    stdscr.addstr(5 + i + space, 32, "Name: Unit #" + str(units[i].id), curses.A_REVERSE)
                                    space += 1
                                else:
                                    stdscr.addstr(5 + i + space, 32, "Name: Unit #" + str(units[i].id))
                                    space += 1
                            if len(units) == selected_unit:
                                stdscr.addstr(5 + len(units) + space, 32, "BACK", curses.A_REVERSE)
                                space += 1
                            else:
                                stdscr.addstr(5 + len(units) + space, 32, "BACK")
                                space += 1
                                
                            space = 0
                            for i in range(len(units)):
                                status = "DEAD"
                                if not units[i].knownDead:
                                    status = "ALIVE"
                                stdscr.addstr(5 + i + space, 86, status, curses.A_STANDOUT)
                                space += 1
                            key = stdscr.getch()

                            # Navigate buttons
                            if key == ord('w') and selected_unit > 0:
                                selected_unit -= 1
                            elif key == ord('s') and selected_unit < len(units):
                                selected_unit += 1
                            elif key == ord('q'):
                                break
                            elif key == ord(' '):  # Enter key
                                stdscr.clear()
                                if selected_unit == len(units):
                                    management_screen(stdscr)
                                else:
                                    message_unit(stdscr, selected_unit)
                    else:
                        stdscr.clear()
                        stdscr.addstr(1, 0, "Message Limit Reached! Gain more next turn.")
                        stdscr.getch()
                                
                case 0:
                    #DIRECT
                    while True:
                        stdscr.addstr(0, 0, "Select units to guide")
                        stdscr.addstr(0, content_start_x, "M O N I T O R - 0 1 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
                        for i in range(30):
                            if i % 2 == 0:
                                stdscr.addstr(1 + i, content_start_x, "|")
                            else:
                                stdscr.addstr(1 + i, content_start_x, " ")
                        # Get user input
                        stdscr.addstr(2, 32, "+------------------+")
                        stdscr.addstr(3, 32, "|  ENGINEERING ID  |")
                        stdscr.addstr(4, 32, "+------------------+")
                        space = 0
                        
                        for i in range(len(units)):
                            if i == selected_unit or (units[i].id -1) in selected_units:
                                stdscr.addstr(5 + i + space, 32, "Name: Unit #" + str(units[i].id), curses.A_REVERSE)
                                space += 1
                            else:
                                stdscr.addstr(5 + i + space, 32, "Name: Unit #" + str(units[i].id))
                                space += 1
                        if len(units) == selected_unit:
                            stdscr.addstr(5 + len(units) + space, 32, "CONFIRM", curses.A_REVERSE)
                            space += 1
                        else:
                            stdscr.addstr(5 + len(units) + space, 32, "CONFIRM")
                            space += 1
                        if len(units) + 1 == selected_unit:
                            stdscr.addstr(6 + len(units) + space, 32, "BACK", curses.A_REVERSE)
                            space += 1
                        else:
                            stdscr.addstr(6 + len(units) + space, 32, "BACK")
                            space += 1
                        key = stdscr.getch()
                        # Navigate buttons
                        if key == ord('w') and selected_unit > 0:
                            selected_unit -= 1
                        elif key == ord('s') and selected_unit < len(units) + 1:
                            selected_unit += 1
                        elif key == ord('q'):
                            break
                        elif key == ord(' ') or key == ('e'):  # Enter key
                            if key == ('e'):
                                selected_unit = len(units) + 1
                            if selected_unit == len(units) + 1:
                                management_screen(stdscr)
                            if selected_unit == len(units): #location
                                while True:
                                    stdscr.clear()
                                    stdscr.addstr(0, 0, "Select units to guide")
                                    stdscr.addstr(0, content_start_x, "M O N I T O R - 0 1 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
                                    for i in range(30):
                                        if i % 2 == 0:
                                            stdscr.addstr(1 + i, content_start_x, "|")
                                        else:
                                            stdscr.addstr(1 + i, content_start_x, " ")
                                    space = 0
                                    for i in range(len(areas)):
                                        if i == selected_loc:
                                            stdscr.addstr(3 + i + space, 32, str(areas[i].id), curses.A_REVERSE)
                                            space += 1
                                        else:
                                            stdscr.addstr(3 + i + space, 32, str(areas[i].id))
                                            space += 1
                                    if len(areas) == selected_loc:
                                        stdscr.addstr(5 + len(areas) + space, 32, "BACK", curses.A_REVERSE)
                                        space += 1
                                    else:
                                        stdscr.addstr(5 + len(areas) + space, 32, "BACK")
                                        space += 1
                                    key = stdscr.getch()
                                    # Navigate buttons
                                    if key == ord('w') and selected_loc > 0:
                                        selected_loc -= 1
                                    elif key == ord('s') and selected_loc < len(units):
                                        selected_loc += 1
                                    elif key == ord('q'):
                                        break
                                    elif key == ord(' '):  # Enter key
                                    # Get user input
                                        if selected_loc == len(areas):
                                            management_screen(stdscr)
                                        else:
                                            for kl in range(len(selected_units)):
                                                if units[selected_units[kl]].alive:
                                                    units[selected_units[kl]].lastArea = units[selected_units[kl]].location
                                                
                                                    units[selected_units[kl]].location.units.remove(units[selected_units[kl]])
                                                    units[selected_units[kl]].location = areas[selected_loc]
                                                    areas[selected_loc].units.append(units[selected_units[kl]])

                                            stdscr.clear()
                                            break
                                break
                            else:
                                if selected_unit in selected_units:
                                    selected_units.remove(selected_unit)
                                else:
                                    selected_units.append(selected_unit)

                case 2:
                    homeScreen(stdscr)
        curses.doupdate()
        stdscr.refresh()
def message_unit(stdscr, given_unit):
    selected_unit = given_unit
    messages = ["Ask for their status", "Ask for their opinions"]
    selected_msg = 0
    #message the unit
    #allow to send
    while True: 
        stdscr.clear()
        # Display menu on the left side
        
        # Display content on the right side
        content_start_x = 30 + 1
        stdscr.addstr(0, 0, "Choose who to message")
        stdscr.addstr(0, content_start_x, "M O N I T O R - 0 1 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        for i in range(30):
            if i % 2 == 0:
                stdscr.addstr(1 + i, content_start_x, "|")
            else:
                stdscr.addstr(1 + i, content_start_x, " ")
        # Get user input
        stdscr.addstr(3, content_start_x + 1, "Messaging Unit #" + str(selected_unit + 1))
        space = 0
        for i in range(len(messages)):
            if i == selected_msg:
                stdscr.addstr(5 + i + space, 32,  str(messages[i]), curses.A_REVERSE)
                space += 1
            else:
                stdscr.addstr(5 + i + space, 32, str(messages[i]))
                space += 1
        if len(messages) == selected_msg:
            stdscr.addstr(5 + len(messages) + space, 32, "BACK", curses.A_REVERSE)
            space += 1
        else:
            stdscr.addstr(5 + len(messages) + space, 32, "BACK")
            space += 1
        key = stdscr.getch()
        # Navigate buttons
        if key == ord('w') and selected_msg > 0:
            selected_msg -= 1
        elif key == ord('s') and selected_msg < len(messages):
            selected_msg += 1
        elif key == ord('q'):
            break
        elif key == ord(' '):  # Enter key
            stdscr.clear()
            if selected_msg == len(messages):
                management_screen(stdscr)
            #show message the unit
            stdscr.clear()
            # Display menu on the left side
            
            # Display content on the right side
            #msg_credits -= 1
            content_start_x = 30 + 1
            stdscr.addstr(0, content_start_x, "M O N I T O R - 0 1 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
            for i in range(30):
                if i % 2 == 0:
                    stdscr.addstr(1 + i, content_start_x, "|")
                else:
                    stdscr.addstr(1 + i, content_start_x, " ")
            if selected_msg == 0:
                if not units[selected_unit].alive:
                    stdscr.addstr(2, 33, "Theres no response...")
                    units[selected_unit].knownDead = True
                    stdscr.getch()
                    break
                #display status
                stdscr.addstr(2, 32, "+------------------+-----------------------------------------------+----------------+")
                stdscr.addstr(3, 32, "|  ENGINEERING ID  |                    ITEMS                      |    Location    |")
                stdscr.addstr(4, 32, "+------------------+-----------------------------------------------+----------------+")
                stdscr.addstr(6, 36, "Unit #" + str(units[selected_unit].id))
                item1 = "None"
                item2 = "None"
                for i in range(len(units[selected_unit].items)):        #get items
                
                    if len(units[selected_unit].items) >= 1:
                        item1 = str(units[selected_unit].items[0].id)
                    if len(units[selected_unit].items) > 1:
                        item2 = str(units[selected_unit].items[1].id)
                stdscr.addstr(6, 56, item1)
                stdscr.addstr(6, 80, item2)
                stdscr.addstr(6, 101, str(units[selected_unit].location.id))
                key = stdscr.getch()
                break

            elif selected_msg == 1:
                if not units[selected_unit].alive:
                    stdscr.addstr(2, 33, "Theres no response...")
                    stdscr.getch()
                    break
                #display opinions
                #get opinions
                highest = 0
                lowest = 0
                think = units[selected_unit].opinions
                for i in range(len(think)):
                    if think[i].op > think[highest].op:
                        highest = i
                    if think[i].op < think[lowest].op:
                        lowest = i

                #display status
                stdscr.addstr(2, 33, "Unit #" + str(units[selected_unit].id) + " Thinks Unit #" + str(highest + 1)+ " is trustworthy")
                stdscr.addstr(3, 33, "Unit #" + str(units[selected_unit].id) + " Thinks Unit #" + str(lowest + 1) + " is suspicious")
                stdscr.getch()
                break
                
def camera(stdscr, area):
    if area.camera == True:
        stdscr.addstr(1, 32, "Area: " + area.id)
        spacing = 7
        stdscr.addstr(3, 32, "Units Present")
        stdscr.addstr(4, 32, "+------------------+-------------------------+---------------------+")
        stdscr.addstr(5, 32, "|  ENGINEERING ID  |                         |        Items        |")
        stdscr.addstr(6, 32, "+------------------+-------------------------+---------------------+")
        stdscr.addstr(3, 130, "Visible Bodies")
        stdscr.addstr(4, 130, "+------------------+")
        stdscr.addstr(5, 130, "|   RECOVERED ID   |")
        stdscr.addstr(6, 130, "+------------------+")
        stdscr.addstr(3, 180, "Visible Items")
        stdscr.addstr(4, 180, "+---------------+")
        stdscr.addstr(5, 180, "|   ITEM NAME   |")
        stdscr.addstr(6, 180, "+---------------+")

        
        for i in range(len(area.units)):        #get items
            item1 = "None"
            item2 = "None"
            if len(area.units[i].items) >= 1:
                item1 = str(area.units[i].items[0].id)
            if len(area.units[i].items) > 1:
                item2 = str(area.units[i].items[1].id)
            lines = ["+------------------+","|  ENGINEERING ID  |","+------------------+","| Name: Unit #" + str(area.units[i].id),"|                                               ","| Items: "+ item1 +"     " + item2,"+-----------------------------------------------+"," "]
            lines_quest = ["+-----------------------------------------------+","|                ENGINEERING ID                 |","|-----------------------------------------------+","| Name: Unit #" + str(area.units[i].id),"|                                               ","| Items: "+ item1 +"     " + item2,"+-----------------------------------------------+"," "]

            #return in questioning
            stdscr.addstr(spacing + i, 32, lines[3])
            stdscr.addstr(spacing + i, 77, lines[5])
            spacing += 1
            #needs to add the shit
        space = 7
        for i in range(len(area.items)):
            stdscr.addstr(space + i, 180, area.items[i].id)
            space += 1
        space = 7
        for i in range(len(area.bodies)):
            stdscr.addstr(space + i, 130, "Name: Unit #" + area.bodies[i].id)
            space += 1
    else:
        stdscr.addstr(1, 32, "Area: " + area.id)
        stdscr.addstr(2, 32, "ERROR! CAMERA FEED NOT FOUND")




def printAll():
    for i in range(len(units)):
        a = units[i]
        print(a.id, a.role, a.work, a.search, a.independence, a.trust, a.location.id)
    print()
    for i in range(len(areas)):
        a = areas[i]
        print(a.id, a.easy_tasks, a.med_tasks, a.hard_tasks)
        print("Items --------")
        for j in range(len(a.items)):
            print(a.items[j].id, end = " ")
        print()
    print()

def start():
    defineUnits(10)
    getBadGuys(10)
    defineArea(20)
    addItems()
    #MR STORAGE POWER KITCHEN STORAGE
    #place all units in Monitor room
    for i in range(len(units)):
        units[i].location = areas[0]
        areas[0].units.append(units[i])
    #Set to home screen
    curses.wrapper(homeScreen)

start()
printAll()