###############################################
# Name: Justin Denison
# Date: 3/30/24 (final)
# A game with many rooms and a puzzle
# Instructions:
#   1. take key and go to room 4 to interact with chest
#   2. go to room 3 to interact with statue
#   3. go to room 2 to inteact with fireplace
#################################################


from tkinter import *


# Class representing a room in the game
class Room(object):
    def __init__(self, name, image):
        # Initialize room attributes
        self._name = name
        self._image = image
        self._exits = {}
        self._items = {}
        self._grabbables = []

    # Getter and setter methods for room attributes
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def exits(self):
        return self._exits

    @exits.setter
    def exits(self, value):
        self._exits = value

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    @property
    def grabbables(self):
        return self._grabbables

    @grabbables.setter
    def grabbables(self, value):
        self._grabbables = value

    # Method to add an exit to the room
    def addExit(self, exit, room):
        self._exits[exit] = room

    # Method to add an item to the room
    def addItem(self, item, desc):
        self._items[item] = desc

    # Method to add a grabbable item to the room
    def addGrabbable(self, item):
        self._grabbables.append(item)

    # Method to remove a grabbable item from the room
    def delGrabbable(self, item):
        self._grabbables.remove(item)

    # Method to return a string description of the room
    def __str__(self):
        s = "You are in {}.\n".format(self.name)
        s += "You see: "
        for item in self.items.keys():
            s += item + " "
        s += "\n"
        s += "You can carry: "
        for grab in self.grabbables:
            s += grab + " "
        s += "\n"
        s += "Exits: "
        for exit in self.exits.keys():
            s += exit + " "
        return s


# Class representing the game
class Game(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

    # Method to create rooms in the game
    def createRooms(self):
        r1 = Room("Room 1", "room1.png")
        r2 = Room("Room 2", "room2.png")
        r3 = Room("Room 3", "room3.png")
        r4 = Room("Room 4", "room4.png")
        r5 = Room("Room 5", "room5.png")
        r6 = Room("Room 6", "room6.png")
        r7 = Room("Room 7", "room7.png")
        r8 = Room("Room 8", "room8.png")
        r9 = Room("Room 9", "room9.png")
        r10 = Room("Room 10", "room10.png")
        r11 = Room("Room 11", "room11.png")
        r12 = Room("Room 12", "room12.png")
        r13 = Room("Room 13", "room13.png")
        r14 = Room("Room 14", "room14.png")
        r15 = Room("Room 15", "room15.png")
        r16 = Room("Room 16", "room16.png")
        r17 = Room("Room 17", "room17.png")
        r18 = Room("Room 18", "room18.png")
        r19 = Room("Room 19", "room19.png")
        r20 = Room("Room 20", "room20.png")
        r21 = Room("Room 21", "room21.png")
        r22 = Room("Room 22", "room22.png")
        r23 = Room("Room 23", "room23.png")
        r24 = Room("Room 24", "room24.png")
        r1.addExit("north", r2)
        r2.addExit("north", r3)
        r3.addExit("north", r4)
        r3.addExit("east", r17)
        r4.addExit("north", r5)
        r5.addExit("north", r6)
        r6.addExit("east", r7)
        r7.addExit("east", r8)
        r8.addExit("east", r9)
        r9.addExit("east", r10)
        r10.addExit("east", r11)
        r11.addExit("south", r12)
        r12.addExit("south", r13)
        r13.addExit("south", r14)
        r14.addExit("south", r15)
        r14.addExit("west", r24)
        r15.addExit("south", r16)
        r16.addExit("north", r15)
        r17.addExit("east", r20)
        r17.addExit("west", r3)
        r18.addExit("south", r20)
        r18.addExit("east", r19)
        r19.addExit("south", r21)
        r19.addExit("west", r18)
        r24.addExit("west", r21)
        r24.addExit("east", r14)
        r21.addExit("north", r19)
        r21.addExit("south", r23)
        r21.addExit("west", r20)
        r21.addExit("east", r24)
        r20.addExit("north", r18)
        r20.addExit("south", r22)
        r20.addExit("west", r17)
        r20.addExit("east", r21)
        r22.addExit("north", r20)
        r22.addExit("east", r23)
        r23.addExit("north", r21)
        r23.addExit("west", r22)



        r1.addItem("chair", "it looks uncomfortable")
        r1.addItem("table", "it looks very sturdy")
        r2.addItem("rug", "it looks very old and recently moved")
        r2.addItem("fireplace", "it provides a nice warm atmosphere")
        r3.addItem("bookshelf", "it has many random books on it and some big ones that stand out")
        r3.addItem("statue", "it is small and seems to be hollow?")
        r3.addItem("desk", "it has a drawer that needs to be unlocked")
        r4.addItem("brewrig", "it is here for some reason, I guess")
        r4.addItem("chest", "it seems to be a locked chest")
        r1.addItem("diary1",
                   "4/2/22\n\nI had an idea. After my late brother's passing from the 'mystery disease' deathicitis I knew I had to find a solution. The only problem was a lack of patients to test my solution on and experiment with. I have so far been able to capture a few. They usually fight but its nothing I cant handle.\n\nDr. Zonderstrom")
        r1.addItem("diary2",
                   "4/30/22\n\nI cannot believe I did not think of this sooner! I have made a lot of progress in finding a cure. I must admit at first the screams got to me a little bit but it is all in the name of Science! I am thinking of ramping up testing to speed up time to find a cure.\n\nDr. Zonderstrom")
        r1.addItem("diary3",
                   "5/13/22\n\nI have hit a bit of a wall. I saw massive progress at first but in my latest test (No. 67) it seems the cure stops the disease temporarily but doesnt totally cure it. The only way onward is to further test. Its all in the name of my brother. I hate to admit it but I am not even bothered by the testing process anymore. Desensitization is an interesting phenomenon.\n\nDr. Zonderstrom")
        r1.addItem("diary4",
                   "6/3/22\n\nI had to ramp up work a lot but I was able to crack the problem! In trial No. 115 I tried applying the solution all at once and not over a gradual time period and it led to a complete cure of the disease! The only downside to this is that it causes severe memory loss and immenent death hours after waking up. I am currently working to solve this.\n\nDr. Zonderstrom")
        r1.addItem("diary5",
                   "6/21/24\n\nStill no cure. I have begun to get headaches from the work load. I do not know if it is some form of karma for my actions. Many people have died in my experiments so far (No. 143 currently), however it is all for the greater good. If only people would understand thsi is the only way to further push science! We cannot be weak willed and allow ourselves to be bested!\n\nDr. Zonderstrom")
        r1.addItem("diary6",
                   "7/3/24\n\nI have realized that I am unfortunatleuy ailed by the same illness that took my brother and that I dedicated myself to solving. All before perfecting the cure. This will most likley be my last entry due to death after I risk the medicine on my own body. It is my only hope to survive. If you are reading these then I am probably one of the numerous bodies surrounding the labs. I wouldve like to have been remembered, but I do not think the world would take kindly to my experiments. I will leave my medical ID here as proof of my work and testament to my life. It might help you to identify me.\n\nDr. Zonderstrom\n\n\n-------------------------------\n-                             -\n- medical identification card -\n-                             -\n- name: Dr Jack Zonderstrom   -\n-                             -\n- director of pathology       -\n-                             -\n-------------------------------")

        r1.addGrabbable("key")
        r3.addGrabbable("book")
        r4.addGrabbable("beverage")

        Game.currentRoom = r1
        Game.inventory = []

    # Method to set up the graphical user interface
    def setupGUI(self):
        self.pack(fill=BOTH, expand=1)
        Game.player_input = Entry(self, bg="white")
        Game.player_input.bind("<Return>", self.process)
        Game.player_input.pack(side=BOTTOM, fill=X)
        Game.player_input.focus()

        img = None
        Game.image = Label(self, width=int(WIDTH / 2), image=img)
        Game.image.image = img
        Game.image.pack(side=LEFT, fill=Y)
        Game.image.pack_propagate(False)

        text_frame = Frame(self, width=WIDTH / 2)

        Game.text = Text(text_frame, bg="lightgrey", state=DISABLED)
        Game.text.pack(fill=Y, expand=1)
        text_frame.pack(side=RIGHT, fill=Y)
        text_frame.pack_propagate(False)

    # Method to set the current room image
    def setRoomImage(self):
        if (Game.currentRoom == None):
            Game.img = PhotoImage(file="skull.gif")
        else:
            Game.img = PhotoImage(file=Game.currentRoom.image)

        Game.image.config(image=Game.img)
        Game.image.image = Game.img

    # Method to set the status displayed on the right of the GUI
    def setStatus(self, status):
        Game.text.config(state=NORMAL)
        Game.text.delete("1.0", END)
        if (Game.currentRoom == None):
            Game.text.insert(END, "You are dead")
        else:
            possible_actions = "Hints: \nYou can type: \ngo direction \ndirection = south, north, east, west \nlook item \nitem = check 'you see' \ntake grabbable \ngrabbable = see 'you can carry'"
            Game.text.insert(END, str(Game.currentRoom) + "\nYou are carrying: " + str(
                Game.inventory) + "\n\n" + status + "\n\n\n" + possible_actions)
            Game.text.config(state=DISABLED)

    # Method to start playing the game
    def play(self):
        self.createRooms()
        self.setupGUI()
        self.setRoomImage()
        self.setStatus("")

    # Method to process the player's input
    def process(self, event):
        action = Game.player_input.get()
        action = action.lower()
        response = "I don't understand. Try verb noun. Valid verbs are go, look, take."
        if (action == "quit" or action == "exit" or action == "bye" or action == "sionara"):
            exit(0)
        if (Game.currentRoom == None):
            Game.player_input.delete(0, END)
            return
        words = action.split()
        if (len(words) == 2):
            verb = words[0]
            noun = words[1]

        done = False

        if (verb == "go"):
            response = "Invalid exit."

            if (noun in Game.currentRoom.exits):
                Game.currentRoom = Game.currentRoom.exits[noun]
                response = "Room changed."
        elif (verb == "look"):
            response = "I don't see that item"
            if (noun in Game.currentRoom.items):
                response = Game.currentRoom.items[noun]
        elif verb == "interact":
            # Check if the noun is interactable
            if noun in ["chair", "table", "rug", "brewrig"]:
                response = Game.currentRoom.items[noun]
            # Handle specific interactions based on items and inventory
            elif noun == "chest":
                if "key" in Game.inventory and "hammer" not in Game.inventory:
                    response = "Interesting! The key unlocked the chest and in it you found a hammer!"
                    Game.inventory.append("hammer")
                else:
                    response = "The chest is locked."
            elif noun == "statue":
                if "hammer" in Game.inventory and "fire extinguisher" not in Game.inventory:
                    response = "Interesting! The hammer smashed the statue and you found a fire extinguisher in it!"
                    Game.inventory.append("fire extinguisher")
                else:
                    response = "The statue seems sturdy."
            elif noun == "fireplace":
                if "fire extinguisher" in Game.inventory:
                    response = "You have extinguished the fireplace and escaped through a hidden door!"
                    exit(0)
                else:
                    response = "The fireplace crackles warmly."
        elif (verb == "take"):
            response = "I don't see that item"
            for grabbable in Game.currentRoom.grabbables:
                if (noun == grabbable):
                    Game.inventory.append(grabbable)
                    Game.currentRoom.delGrabbable(grabbable)
                    response = "Item grabbed"
                    break
        self.setStatus(response)
        self.setRoomImage()
        Game.player_input.delete(0, END)


######################MAIN#########################

# Default size of the GUI
WIDTH = 800
HEIGHT = 600

# Create the window
window = Tk()
window.title("Room Adventure")

# Create the GUI as a Tkinter canvas inside the window
g = Game(window)
# Play the game
g.play()

# Wait for the window to close
window.mainloop()
