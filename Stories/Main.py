import random

person = input("hero's name\n")

personSType = ["cat", "rat", "bike", "car", "doctor", "children"]
xpersonSType = random.randrange(0, len(personSType), 1)

personSColor = ["red", "blue", "white", "green"]
xpersonSColor = random.randrange(0, len(personSColor), 1)

personSFriend = ["GrandMa", "Elf", "Alien", "car"]
xpersonSFriend = random.randrange(0, len(personSColor), 1)

personSFriendName = input("name of friend\n")

personSJob = ["students", "dentists", "artists", "animators"]
xpersonSJob = random.randrange(0, len(personSJob), 1)

action = ["run", "walk", "stand", "watch TV"]
xaction = random.randrange(0, len(action), 1)

location = ["home", "mountain", "office"]
xlocation = random.randrange(0, len(location), 1)


print(person +" is "  + personSColor[xpersonSColor] + " " + personSType[xpersonSType] + ".\n")
print("Friend of " + person + " is " + personSFriendName + ". " + personSFriendName + " is " + personSFriend[xpersonSFriend] + ". \n")
print("They are " + personSJob[xpersonSJob] + ". " + "They " + action[xaction] + " " + location[xlocation])

