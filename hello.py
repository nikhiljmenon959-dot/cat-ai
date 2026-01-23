import random

# ---------- State ----------
trust = 5          # 0–10
hunger = 7         # 0–10 (higher = hungrier)
energy = 6         # 0–10
emotion = "neutral"
emotion_timer = 0
is_sleeping = False
rule=False
# ---------- Helpers ----------
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
    print("*slow blink*")

def play():
    w=True
    while w :
        pp= input("> ").lower().strip()
        if pp in ["sit"]:
            print("*sitting*")
        elif pp in ["roll over"]:
            print("*rolling over*")
        elif pp in ["jump"]:
            print("*jumping*")
        elif pp in ["stop","stop playing","no more playing"]:
            print("stop playing*")
            w=False
        elif has(["hit", "fat", "stupid","dum"], user):
            trust = max(0, trust - 2)
            set_emotion("angry", 5)
            print(random.choice(["hits your face","bites you","*ears flatten and tail lashes violently*"]))
        else:
            print("*looks at you in confusion*")

print("🐾 Companion is here. Type 'bye' to rest.")

# ---------- Main Loop ----------
while True:
    user = input("> ").lower().strip()

    decay_emotion()
    hunger = min(10, hunger + 0.2)

    # ---------- Exit ----------
    if  has(["poppu"], user):
        print("meow")

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

    # ---------- Name ----------
    if "i am" in user:
        print("*looks at you calmly*")
        trust = min(10, trust + 0.5)
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
    if has(["food", "feed", "eat", "eating", "milk","fish", "meat","biriyani", "gives it", "give you","give milk", "give food"], user):
        if hunger <= 2:
            print("*sniffs the food and ignores it*")
        else:
            hunger = max(0, hunger - 5)
            trust = min(10, trust + 1)
            set_emotion("happy", 4)
            print(random.choice(["*eats happily and purrs*","*devours the food eagerly*","*meows happily while eating*"]))
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
        set_emotion("angry", 4)
        print("*ears flatten in warning*")
        continue

    # ---------- Insults / Hit ----------
    if has(["hit", "fat", "stupid"], user):
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
            print(random.choice(["*slow blinks affectionately*","*kisses you*","*meow*"])
        if v == 2:
            print("*licks you*")
    elif emotion == "sad":
        print("*stays close, quiet*")
    elif emotion == "angry":
        print("*keeps distance, ears low*")
    else:
        blink()
