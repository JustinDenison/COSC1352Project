import RPi.GPIO as GPIO
import pygame
from tkinter import *
import json

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('PsycWard.mp3')
pygame.mixer.music.play(-1)

UP_PIN = 25
DOWN_PIN = 24
LEFT_PIN = 26
RIGHT_PIN = 23
INTERACT_PIN = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(INTERACT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def button_callback(channel):
    if channel == UP_PIN:
        g.process("go north")
    elif channel == DOWN_PIN:
        g.process("go south")
    elif channel == LEFT_PIN:
        g.process("go west")
    elif channel == RIGHT_PIN:
        g.process("go east")
    elif channel == INTERACT_PIN:
        g.process("interact")

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
        self.setup_GPIO()

    def setup_GPIO(self):
        GPIO.add_event_detect(UP_PIN, GPIO.RISING, callback=button_callback, bouncetime=200)
        GPIO.add_event_detect(DOWN_PIN, GPIO.RISING, callback=button_callback, bouncetime=200)
        GPIO.add_event_detect(LEFT_PIN, GPIO.RISING, callback=button_callback, bouncetime=200)
        GPIO.add_event_detect(RIGHT_PIN, GPIO.RISING, callback=button_callback, bouncetime=200)
        GPIO.add_event_detect(INTERACT_PIN, GPIO.RISING, callback=button_callback, bouncetime=200)

    # Method to create rooms in the game
    # Method to create rooms in the game
    def createRooms(self):
        with open('rooms.json') as f:
            data = json.load(f)

        rooms_data = data['rooms']

        rooms = {}
        for room_data in rooms_data:
            room = Room(room_data['name'], room_data['image'])
            room.exits = room_data.get('exits', {})
            room.items = room_data.get('items', {})
            room.grabbables = room_data.get('grabbables', [])

            # Check if there's a diary item, and if so, read its content from the file
            for item, desc in room.items.items():
                if item.startswith("diary"):
                    diary_number = item.split("diary")[1]
                    with open(f"diary{diary_number}.txt", "r") as f:
                        diary_content = f.read()
                    room.items[item] = diary_content.strip()  # Set the content of the diary

            rooms[room.name] = room

        # Link exits
        for room_data in rooms_data:
            room = rooms[room_data['name']]
            for exit_dir, exit_room_name in room_data.get('exits', {}).items():
                room.addExit(exit_dir, rooms[exit_room_name])

        # Set initial room
        Game.currentRoom = rooms['Room 1']
        Game.inventory = []

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
            possible_actions = "     Hints: \n	You can type: \n	-go direction \n	  -direction are: south, north, east, west \n	-look item \n	   -item = check 'you see' \n	-take grabbable \n	   -grabbable = see 'you can carry'"
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
WIDTH = 1600
HEIGHT = 1200

# Create the window
window = Tk()
window.title("Room Adventure")

# Create the GUI as a Tkinter canvas inside the window
g = Game(window)
# Play the game
g.play()

# Wait for the window to close
window.mainloop()
