import RPi.GPIO as GPIO
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
        self._grabbables = {}

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

    def setRoomImage(self):
        if (Game.currentRoom == None):
            Game.img = PhotoImage(file="skull.gif")
        else:
            Game.img = PhotoImage(file=Game.currentRoom.image)

        Game.image.config(image=Game.img)
        Game.image.image = Game.img

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

    def play(self):
        self.createRooms()
        self.setupGUI()
        self.setRoomImage()
        self.setStatus("")


def handle_button(channel):
    action = ""
    if channel == 25:
        action = "go north"
    elif channel == 24:
        action = "go east"
    elif channel == 23:
        action = "go south"
    elif channel == 26:
        action = "go west"

    g.process(action)


WIDTH = 1600
HEIGHT = 1200

window = Tk()
window.title("Room Adventure")

g = Game(window)
g.play()

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(25, GPIO.RISING, callback=lambda _: handle_button(25), bouncetime=300)
GPIO.add_event_detect(24, GPIO.RISING, callback=lambda _: handle_button(24), bouncetime=300)
GPIO.add_event_detect(23, GPIO.RISING, callback=lambda _: handle_button(23), bouncetime=300)
GPIO.add_event_detect(26, GPIO.RISING, callback=lambda _: handle_button(26), bouncetime=300)

window.mainloop()
