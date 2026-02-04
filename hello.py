import random

---------- State ----------

trust = 5          # 0–10

hunger = 7         # 0–10 (higher = hungrier)

energy = 6         # 0–10

emotion = "neutral"

emotion_timer = 0

is_sleeping = False

rule=False

point=False

recognized = False

---------- Health ----------

is_sick = False

sick_timer = 0

---------- Food Preferences ----------

favorite_foods = ["fish", "meat", "milk","biscuits","biriyani"]

disliked_foods = ["vegetable","durian","lemon","oranges"]

forbidden_foods = ["chocolate","candi","expired milk","expired meat","rotten fish","cake"]

picky_chance = 0.35   # 35% chance to refuse even liked food

---------- Helpers ----------

def set_emotion(e, t=3):

global emotion, emotion_timer

emotion = e

emotion_timer = t

def decay_emotion():

global emotion, emotion_timer

if emotion_timer > 0:

    emotion_timer -= 1

else:

    emotion = "neutral"

def has(words, text):

return any(w in text for w in words)

def blink():

print(random.choice(["*slow blink*","looks at you"," wagging her tail","meow"]))

def laser():

global point, energy, is_sleeping, trust

point = True

while point==True:

    energy=energy-0.5

    lay=input(">")

    if energy <= 2:

        print("*poppu feels tired so he sleeps slowly*")

        is_sleeping = True

        energy = 6

        point = False

        

    elif has(["stops", "stopes pointing the laser"], lay):

        print("poppu jumps  to catch the laser but misses and looks confused")

        point=False

    elif has(["upp", "points up", "point upp"], lay):

        print("poppu jumps up to catch the red dot")

    elif has(["down", "points down"], lay):

        print("poppu jumps  to catch the red dot")

    elif has(["left", "points left"], lay):

        print("poppu jumps  to the left side diraction to catch the red dot")

    elif has(["right", "points right"], lay):

        print("poppu jumps to the right side to catch the laser")

    elif has(["hit", "fat", "stupid", "dum"], lay):

        trust = max(0, trust - 2)

        set_emotion("angry", 5)

        print(random.choice(["hits your face","bites you","*ears flatten and tail lashes violently*"]))

        point= False

    else:

        print("*tries to tuch the red dot")

def play():

global energy

global is_sleeping, trust

w = True

while w:

    energy -= 1

    pp = input("> ").lower().strip()



    if energy <= 2:

        print("*sleeps slowly*")

        is_sleeping = True

        energy = 6

        w = False

    elif emotion == "sad":

        print("*looks at you, not feeling playful*")

        w=False



    elif pp == "sit":

        print("*sitting*")

    elif has(["play with laser", "laser"], pp):

        laser()

        

    elif has(["gives it a ball", "play ball", "get the ball", "ball"], pp):

        for i in range(0,7):

            print(random.choice(["poppu is chasing the ball","meow","poppu tries to grab it but it rolls away","poppu jumps at the ball the ball rolls away","poppu tries to grab it","rolls away"]))

        print("poppu looks tired")

        energy=2



    elif pp == "roll over":

        print("*rolling over*")



    elif pp == "jump":

        print("*jumping*")

        

    elif has(["i love you", "good poppu", "cute", "good cat"], pp):

        print("licks you")



    elif pp in ["stop", "stop playing", "no more playing"]:

        print("*stops playing*")

        w = False



    elif has(["hit", "fat", "stupid", "dum"], pp):

        trust = max(0, trust - 2)

        set_emotion("angry", 5)

        print(random.choice(["hits your face","bites you","*ears flatten and tail lashes violently*"]))

        w = False



    else:

        print("*looks at you in confusion*")

def make_sick(t=4):

global is_sick, sick_timer

is_sick = True

sick_timer = t

set_emotion("sad", t)

def decay_sickness():

global is_sick, sick_timer

if sick_timer > 0:

    sick_timer -= 1

    if sick_timer==1:

        print("poppu a feels better now")

else:

    is_sick = False

print("🐾 Companion is here. Type 'bye' to rest.")

---------- Main Loop ----------

while True:

user = input("> ").lower().strip()



decay_emotion()

decay_sickness()

hunger = min(10, hunger + 0.2)

---------- name of cat ----------

if  has(["poppu"], user):

    print("meow")

#-------------Exit------------

if user in ["bye", "exit", "good night"]:

    print("*curls up and sleeps*")

    break



# ---------- Sleeping ----------

if is_sleeping:

    if has(["wake"], user):

        is_sleeping = False

        print("*opens one eye slowly*")

    else:

        print("*sleeps quietly*")

    continue

# ---------- Sick ----------

if is_sick==True:

    if has(["pet", "hug", "cuddle","are you okay"], user):

        print("*leans weakly into you and purrs softly*")

        trust = min(10, trust + 0.3)

    elif has(["food", "feed","gives it"], user):

        print("*sniffs the food but turns away*")

    else:

        print(random.choice(["*lies down quietly, not feeling well*","*lets out a small, weak meow*","*breathes slowly, eyes half closed*"]))

    continue



# ---------- Name ----------

if "i am" in user:

    print("*looks at you calmly*")

    trust = min(10, trust + 0.5)

    if not recognized and user in ["i am amritha", "i am amritha p"]:

        recognized = True

        print("poppu smells you and rembers you from it's past ")

        print("poppu feels happy to see you again")

        set_emotion("happy", 4)

        trust = min(10, trust + 1)

        print("*poppu looks at you for a hug*")

    continue



# ---------- Sadness ----------

if has(["sad", "lonely", "cry"], user):

    set_emotion("sad", 4)

    print("*rests head gently*")

    continue



# ---------- Hunger  ----------

if has(["hungry", "hunger"], user):

    if hunger >= 7:

        print("*meows softly and looks at you for food*")

    elif hunger >= 4:

        print("*looks at you expectantly*")

    else:

        blink()

    continue



# ---------- Food ----------

if has(["food", "feed", "eat", "eating", "milk", "fish", "meat", "biriyani", "gives it", "give you", "give milk", "give food"], user):



    # detect food given

    given_food = None

    for f in favorite_foods + disliked_foods + forbidden_foods:

        if f in user:

            given_food = f

            break



    if hunger <= 2:

        print("*sniffs the food and walks away*")

        continue



    # disliked food

    if given_food in disliked_foods:

        set_emotion("angry", 2)

        if  given_food=="durian":

            print("smells it and feel disgusted")

            trust = max(0, trust - 0.5)

        elif given_food=="lemon":

            print("licks it and makes a disgusted face")

            trust = max(0, trust - 0.4)

        else:

            print("*sniffs it, gags slightly, and walks away*")

            trust = max(0, trust - 0.3)

        continue

    #-----bad food----

    if given_food in forbidden_foods:

        print(random.choice(["*sniffs it… eats a little… then looks unwell*","*eats a little... and starts to vomit*"]))

        make_sick(5)

        hunger = max(0, hunger - 1)

        trust = max(0, trust - 1)

        continue



    # favorite or neutral food

    if given_food in favorite_foods:

        if random.random() < picky_chance and trust < 7:

            print("*sniffs carefully… then ignores it*")

            set_emotion("neutral", 2)

            continue

        else:

            hunger = max(0, hunger - 5)

            trust = min(10, trust + 1)

            set_emotion("happy", 4)

            print(random.choice(["*eats slowly… then purrs*","*devours it happily*","*meows approvingly while eating*"]))

            continue



    # unknown food

    else:

        print("*sniffs cautiously… unsure about this food*")

        continue

#------stay away---

if has(["go away", "stay away", "get lost", "i will not talk to you","shoo"], user):

     set_emotion("sad", 2)

     print("*moves away from you looking sad*")

     continue

    



# ---------- Come Here ----------

if has(["come here", "come closer", "sit next", "sit with"], user):

    if emotion == "angry":

        print("*refuses and stays away*")

    else:

        print("comes closer")

        trust = min(10, trust + 0.2)

    continue



# ---------- Hug ----------

if has(["hug", "hugg", "cuddle"], user):

    if emotion == "angry":

        print("*steps back, not in the mood*")

    else:

        print("presses head into your chest")

        set_emotion("happy", 3)

    continue



# ---------- Pet ----------

if has(["pet", "scratch", "scritch"], user):

    if emotion == "angry":

        print("*moves away from your hand*")

    else:

        print("*purrs softly*")

        trust = min(10, trust + 0.3)

    continue



# ---------- Belly ----------

if has(["belly", "stomach"], user):

    set_emotion("angry", 3)

    print("*ears flatten in warning*")

    continue



# ---------- Insults / Hit ----------

if has(["hit", "fat", "stupid","dum"], user):

    if rule==True:

        trust = max(0, trust - 2)

        set_emotion("angry", 5)

        print("*hisses at you and jumps away ...* ")

        rule=False

        continue

    elif rule==False:

        trust = max(0, trust - 2)

        set_emotion("angry", 5)

        print(random.choice(["hits your face","bites you","*ears flatten and tail lashes violently*"]))

        continue



# ---------- Sleep ----------

if has(["sleep", "rest"], user):

    is_sleeping = True

    rule=True

    energy=6

    if emotion=="angry":

        print("*curls up and falls asleep away from you*")

        continue

    else:

        print("*curls up and falls asleep beside you*")

        continue

#-------play------

if has(["play"], user):

    if emotion == "happy":

        print("*meow*")

        play()

        continue



    if emotion == "angry":

        print("*keeps distance, not in the mood to play*")

        continue



# ---------- Default ----------

if emotion == "happy":

    v=random.randint(1,2)

    if v == 1:

        print("*slow blinks affectionately*")

    if v == 2:

        print("*licks you*")

elif emotion == "sad":

    print("*stays close, quiet*")

elif emotion == "angry":

    print("*keeps distance, ears low*")

else:

    blink()