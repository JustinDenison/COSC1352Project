import pygame
from tkinter import *
import json

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('PsycWard.mp3')
pygame.mixer.music.play(-1)

class Room(object):
    def __init__(self, name, image):
        self._name = name
        self._image = image
        self._exits = {}
        self._items = {}
        self._grabbables = []

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

    def addExit(self, exit, room):
        self._exits[exit] = room

    def addItem(self, item, desc):
        self._items[item] = desc

    def addGrabbable(self, item):
        self._grabbables.append(item)

    def delGrabbable(self, item):
        self._grabbables.remove(item)

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


class Game(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.image_label = None

    def createRooms(self):
        with open('rooms.json') as f:
            data = json.load(f)

        rooms_data = data['rooms']

        rooms = {}
        for room_data in rooms_data:
            room = Room(room_data['name'], room_data['image'])
            room.exits = room_data.get('exits', {})
            room.items = room_data.get('items', {})
            room.grabbables = room_data.get('grabbables', {})

            for item, desc in room.items.items():
                if item.startswith("diary"):
                    diary_number = item.split("diary")[1]
                    with open(f"diary{diary_number}.txt", "r") as f:
                        diary_content = f.read()
                    room.items[item] = diary_content.strip()

            rooms[room.name] = room

        for room_data in rooms_data:
            room = rooms[room_data['name']]
            for exit_dir, exit_room_name in room_data.get('exits', {}).items():
                room.addExit(exit_dir, rooms[exit_room_name])

        Game.currentRoom = rooms['Room 1']
        Game.inventory = []

    def setupGUI(self):
        self.pack(fill=BOTH, expand=1)

        # Create a frame for the control buttons and mini-map
        control_frame = Frame(self)
        control_frame.pack(side=LEFT, fill=Y)

        # Create a frame for the control buttons
        button_frame = Frame(control_frame)
        button_frame.pack(side=TOP, fill=Y, padx=10)

        # Load button images
        wimg = PhotoImage(file="up.png")
        aimg = PhotoImage(file="left.png")
        simg = PhotoImage(file="down.png")
        dimg = PhotoImage(file="right.png")

        # WASD control buttons using grid manager
        button_w = Button(button_frame, text="W", command=lambda: self.move("north"), image=wimg, width=50, height=50)
        button_w.image = wimg  # Keep a reference to the image
        button_w.grid(row=0, column=1)

        button_a = Button(button_frame, text="A", command=lambda: self.move("west"), image=aimg, width=50, height=50)
        button_a.image = aimg  # Keep a reference to the image
        button_a.grid(row=1, column=0)

        button_s = Button(button_frame, text="S", command=lambda: self.move("south"), image=simg, width=50, height=50)
        button_s.image = simg  # Keep a reference to the image
        button_s.grid(row=1, column=1)

        button_d = Button(button_frame, text="D", command=lambda: self.move("east"), image=dimg, width=50, height=50)
        button_d.image = dimg  # Keep a reference to the image
        button_d.grid(row=1, column=2)

        # Create a label for the mini-map
        mini_map_frame = Frame(control_frame)
        mini_map_frame.pack(side=TOP, fill=Y, padx=5)

        self.mini_map_label = Label(mini_map_frame)
        self.mini_map_label.pack(side=TOP, fill=BOTH, expand=1)

        # Create a frame for the text display area
        text_frame = Frame(control_frame)
        text_frame.pack(side=TOP, fill=BOTH, expand=1)

        # Text widget for displaying game status
        Game.text = Text(text_frame, bg="lightgrey", state=DISABLED, wrap=NONE, width=50)
        Game.text.pack(fill=BOTH, expand=1)

        # Create a frame for the room image
        image_frame = Frame(self)
        image_frame.pack(side=LEFT, fill=BOTH, expand=1)

        # Create a label for displaying the room image
        self.image_label = Label(image_frame)
        self.image_label.pack(side=TOP, fill=BOTH, expand=1)

    def move(self, direction):
        if Game.currentRoom and direction in Game.currentRoom.exits:
            Game.currentRoom = Game.currentRoom.exits[direction]
            self.setStatus("Moved " + direction + ".")
            self.setRoomImage()
        else:
            self.setStatus("Cannot move " + direction + ".")

    def setRoomImage(self):
        if Game.currentRoom is None:
            img = PhotoImage(file="skull.gif")
        else:
            img = PhotoImage(file=Game.currentRoom.image)

        self.image_label.config(image=img)
        self.image_label.image = img

        mini_map_image = None
        if Game.currentRoom:
            mini_map_filename = "map{}.png".format(Game.currentRoom.name.split()[-1])
            try:
                mini_map_image = PhotoImage(file=mini_map_filename)
            except:
                pass

        if mini_map_image is None:
            mini_map_image = PhotoImage(file="placeholder_map.png")

        self.mini_map_label.config(image=mini_map_image)
        self.mini_map_label.image = mini_map_image

    def setStatus(self, status):
        Game.text.config(state=NORMAL)
        Game.text.delete("1.0", END)
        if Game.currentRoom is None:
            Game.text.insert(END, "You are dead")
        else:
            possible_actions = "Hints: \nYou can type: \ngo direction \ndirection = south, north, east, west \nlook item \nitem = check 'you see' \ntake grabbable \ngrabbable = see 'you can carry'"
            Game.text.insert(END, str(Game.currentRoom) + "\nYou are carrying: " + str(
                Game.inventory) + "\n\n" + status + "\n\n\n" + possible_actions)
            Game.text.config(state=DISABLED)

    def play(self):
        self.createRooms()
        self.setupGUI()
        self.setRoomImage()
        self.setStatus("")

    def process(self, event):
        action = Game.player_input.get()
        action = action.lower()
        response = "I don't understand. Try verb noun. Valid verbs are go, look, take."
        if action in ["quit", "exit", "bye", "sionara"]:
            exit(0)
        if Game.currentRoom is None:
            Game.player_input.delete(0, END)
            return
        words = action.split()
        if len(words) >= 2:
            verb = words[0]
            noun = words[1]

        done = False

        if verb == "go":
            response = "Invalid exit."
            if noun in Game.currentRoom.exits:
                Game.currentRoom = Game.currentRoom.exits[noun]
                response = "Room changed."
        elif verb == "look":
            response = "I don't see that item"
            if noun in Game.currentRoom.items:
                response = Game.currentRoom.items[noun]
        elif verb == "interact":
            if noun == "safe":
                if len(words) == 3 and words[2] == "040222":
                    response = "You opened the safe and found a diary!"
                    if "diary3" not in Game.currentRoom.items:
                        with open("diary3.txt", "r") as f:
                            diary_content = f.read()
                        Game.currentRoom.addItem("diary3", diary_content.strip())
                        Game.inventory.append("key3")
                else:
                    response = "The safe requires a password."
            elif noun == "bookshelf":
                if "diary4" not in Game.currentRoom.items:
                    with open("diary4.txt", "r") as f:
                        diary_content = f.read()
                    response = Game.currentRoom.items[noun]
                    Game.inventory.append("key4")
                else:
                    response = Game.currentRoom.items[noun]
            elif noun == "diary1":
                if "diary1" not in Game.inventory:
                    response = Game.currentRoom.items[noun]
                    Game.inventory.append("key1")
                else:
                    response = Game.currentRoom.items[noun]
            elif noun == "diary2":
                if "diary2" not in Game.inventory:
                    response = Game.currentRoom.items[noun]
                    Game.inventory.append("key2")
                else:
                    response = Game.currentRoom.items[noun]
            elif noun == "poster" and "key5" not in Game.inventory:
                response = "You found a hidden compartment behind the poster and discovered a key!"
                Game.inventory.append("key5")
                Game.currentRoom.addItem("diary5", "An old diary lies on the ground.")
            elif noun == "mirror" and "hammer" in Game.inventory:
                response = "You have broken the window with the hammer out of anger! Behind it you find a hidden door with 5 locks on it! This is on a wall that is supposed to not have anything behind it. It must be a secret room!"
                Game.currentRoom.addItem("door", "the door has 5 locks on it")
            elif noun == "door" and "door" in Game.currentRoom.items and "key1" in Game.inventory and "key2" in Game.inventory and "key3" in Game.inventory and "key4" in Game.inventory and "key5" in Game.inventory:
                response = "You unlock the hidden door and enter the secret room!"
                Game.currentRoom = Game.currentRoom.exits["Hidden"]

        elif verb == "take":
            response = "I don't see that item"
            for grabbable in Game.currentRoom.grabbables:
                if noun == grabbable:
                    Game.inventory.append(grabbable)
                    Game.currentRoom.delGrabbable(grabbable)
                    response = "Item grabbed"
                    break
        self.setStatus(response)
        self.setRoomImage()
        Game.player_input.delete(0, END)


WIDTH = 1600
HEIGHT = 600

window = Tk()
window.title("Room Adventure")

g = Game(window)
g.play()

window.mainloop()
