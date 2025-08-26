import keyboard
from pynput.keyboard import Controller, Key
import time
import random

# Initialize the keyboard controller
keyboard_controller = Controller()

q = ['Dog','Donkey','Leopard','Polar bear','Rabbit','Pigeon','Dolphin','Eagle','Goat','Eel','Beagle','Beaver','Badger','Hamster','Hawk','Jaguar','Lizard','Llama','Rhinoceros','Wombat','Sheep','Sloth','Racoon','Lynx','Lemur','Blue whale','Cow','Tiger','Cheetah','Turtle','Porcupine','Albatross','Frog','Flying squirrel','Jackal','Goose','Gorilla','Orangutan','Giraffe','Cobra','Deer','Chihuahua','Koala','Chinchillas','Hedgehog','Bison','Meerkat','Owl','Mole','Monitor lizard','Mule','Rat','Cat','Lion','Bear','Tortoise','Hare','Crow','Whale','Ostrich','Emu','Arctic fox','Chimpanzee','Antelope','Hermit Crab','Hammerhead shark','Chameleon','King Cobra','Kangaroo','Dodo','Zebra','Bull','Mouse','Vulture','Duck','Elk','Baboon','Snake','Horse','Panther','Elephant','Crocodile','Hen','Fish','Alligator','Fox','Armadillo','Wolf','Monkey','Bat','Giant Panda','Camel','Hippopotamus','Ibex','Iguana','Jellyfish','Possum','Buffalo','Otter','Flamingo','Swan','Boar','Mammoth','Peacock']

# Wait for the initial Enter key press to start the loop
print("Press Enter to start...")
keyboard.wait('enter')  # This will start the loop when Enter is pressed once

# Now, the program will run the loop 500 times automatically
for _ in range(500):
   
    n = str(random.choice(q))
    print(n)
    keyboard_controller.type(n)     # Writes "I love you"
    keyboard_controller.press(Key.enter)       # Presses the Enter key
    keyboard_controller.release(Key.enter)     # Releases the Enter key
    time.sleep(2)                            # Adds a short delay between iterations

# print("Finished writing 'I love you' 500 times.")
