import random
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

# ---------- Constants ----------
FAVORITE_FOODS = ["fish", "meat", "milk", "biscuits", "biriyani"]
DISLIKED_FOODS = ["vegetable", "durian", "lemon", "oranges"]
FORBIDDEN_FOODS = ["chocolate", "candi", "expired milk", "expired meat", "rotten fish", "cake"]
PICKY_CHANCE = 0.35

# Medicine types
MEDICINES = ["antibiotic", "pain relief", "fever medicine", "stomach medicine"]

# ---------- Cat State ----------
@dataclass
class CatState:
    trust: float = 5.0
    hunger: float = 6.0
    energy: float = 10.0
    closeness: int = 3
    emotion: str = "neutral"
    emotion_timer: int = 0
    is_sleeping: bool = False
    is_sick: bool = False
    sick_timer: int = 0
    is_very_sick: bool = False
    very_sick_timer: int = 0
    health: float = 10.0  # New health stat (0-10)
    recognized: bool = False
    zoomies_active: bool = False

cat = CatState()

# ---------- Utility Functions ----------
def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(max_val, value))

def has_keywords(keywords: List[str], text: str) -> bool:
    """Check if any keyword is in the text."""
    return any(keyword in text for keyword in keywords)

def random_choice_print(messages: List[str]) -> None:
    """Print a random message from a list."""
    print(random.choice(messages))

def get_current_hour() -> int:
    """Get the current hour (0-23)."""
    return datetime.now().hour

def check_3am_zoomies() -> bool:
    """Check if it's 3 AM and trigger random zoomies."""
    hour = get_current_hour()
    
    # Between 2 AM and 4 AM, there's a chance of zoomies
    if 2 <= hour <= 4:
        # 30% chance of zoomies during these hours
        if random.random() < 0.3 and not cat.zoomies_active:
            cat.zoomies_active = True
            cat.energy = 10  # Full energy for zoomies!
            return True
    return False

def trigger_zoomies() -> None:
    """Handle the 3 AM zoomies outburst."""
    print("\n" + "="*50)
    print("🌙 *SUDDENLY AT 3 AM* 🌙")
    print("="*50)
    
    zoomies_messages = [
        "*ZOOOOOM* poppu races across the room at full speed!",
        "*crashes into furniture* MEOW MEOW MEOW!!!",
        "*runs up and down repeatedly* poppu is going CRAZY!",
        "*jumps on everything* THE ZOOMIES HAVE TAKEN OVER!",
        "*slides across the floor* poppu can't be stopped!",
        "*parkour off the walls* MAXIMUM CHAOS MODE!",
        "*knocks something over* CRASH! poppu doesn't even care!",
        "*eyes are HUGE and wild* poppu stares at nothing... then BOLTS!"
    ]
    
    print("\n⚡ THE ZOOMIES HAVE BEGUN! ⚡\n")
    
    # Multiple random outbursts
    num_outbursts = random.randint(5, 8)
    for i in range(num_outbursts):
        random_choice_print(zoomies_messages)
        if i < num_outbursts - 1:
            input("*press enter to witness more chaos*\n")
    
    print("\n*poppu suddenly stops... looks around innocently...*")
    print("*yawns and acts like nothing happened*\n")
    
    # After zoomies, cat is tired
    cat.energy = 3
    cat.hunger = min(10, cat.hunger + 2)  # All that running made them hungry
    cat.zoomies_active = False
    
    print("poppu looks slightly tired now")
    print("="*50 + "\n")

def check_critical_condition_sickness() -> None:
    """Check if hunger or energy is 0 and trigger very sick with a chance."""
    if cat.is_very_sick:  # Already very sick
        return
    
    trigger_chance = 0
    reason = ""
    
    # Check hunger
    if cat.hunger >= 10:
        trigger_chance = 0.6  # 60% chance when starving
        reason = "starvation"
    
    # Check energy
    if cat.energy <= 0:
        if trigger_chance > 0:
            trigger_chance = 0.8  # 80% if both hunger and exhaustion
            reason = "starvation and exhaustion"
        else:
            trigger_chance = 0.5  # 50% chance when exhausted
            reason = "exhaustion"
    
    # Trigger sickness if conditions met
    if trigger_chance > 0 and random.random() < trigger_chance:
        print(f"\n⚠️  Poppu has become very sick from {reason}!")
        make_very_sick()

def make_very_sick() -> None:
    """Trigger very serious sickness that requires medicine."""
    cat.is_very_sick = True
    cat.very_sick_timer = 15  # Has 15 turns to get medicine
    cat.health = 6.0
    set_emotion("sad", 10)
    
    print("\n" + "!"*50)
    print("⚠️  CRITICAL: POPPU IS VERY SICK! ⚠️")
    print("!"*50)
    random_choice_print([
        "*poppu is breathing heavily and looks very weak*",
        "*poppu is shaking and won't eat*",
        "*poppu's eyes are half-closed and barely moving*",
        "*poppu is making pained meowing sounds*"
    ])
    print("\n💊 Poppu needs MEDICINE urgently!")
    print("Available medicines: antibiotic, pain relief, fever medicine, stomach medicine")
    print(f"⏰ Time remaining: {cat.very_sick_timer} turns")
    print(f"❤️  Health: {cat.health}/10")
    print("!"*50 + "\n")

def decay_very_sick() -> bool:
    """Decay very sick timer and health. Returns True if cat passed out."""
    if not cat.is_very_sick:
        return False
    
    cat.very_sick_timer -= 1
    cat.health -= 0.5  # Health decreases each turn
    
    # Show warnings
    if cat.very_sick_timer % 3 == 0:
        print(f"\n⚠️  WARNING: Poppu's health is {cat.health:.1f}/10")
        print(f"⏰ {cat.very_sick_timer} turns until critical condition!")
        random_choice_print([
            "*poppu whimpers weakly*",
            "*poppu's breathing is shallow*",
            "*poppu barely responds to touch*"
        ])
        print()
    
    # Check if passed out
    if cat.health <= 0 or cat.very_sick_timer <= 0:
        print("\n" + "💔"*25)
        print("CRITICAL CONDITION!")
        print("💔"*25)
        print("*poppu has passed out from the illness...*")
        print("*poppu needs immediate veterinary care*")
        print("\n🏥 GAME OVER - Poppu needs to go to the vet hospital 🏥\n")
        print("💔"*25 + "\n")
        return True
    
    return False

def give_medicine(medicine_type: str) -> bool:
    """Give medicine to the cat. Returns True if successful."""
    if not cat.is_very_sick:
        print("*poppu doesn't need medicine right now*")
        return False
    
    if medicine_type not in MEDICINES:
        print(f"That's not a valid medicine. Available: {', '.join(MEDICINES)}")
        return False
    
    # Random chance the medicine works
    success_chance = 0.7  # 70% chance it's the right medicine
    
    if random.random() < success_chance:
        print("\n" + "✨"*25)
        print("🎉 THE MEDICINE WORKED! 🎉")
        print("✨"*25)
        random_choice_print([
            f"*poppu slowly swallows the {medicine_type}*",
            f"*after taking the {medicine_type}, poppu's breathing steadies*",
            f"*the {medicine_type} starts to take effect*"
        ])
        print("\n*After a few moments...*")
        print("*poppu's eyes brighten a little*")
        print("*poppu tries to stand up, looking much better*")
        print("*weak meow* ...meow...")
        print("\n💚 Poppu is recovering! Health restored!")
        print("✨"*25 + "\n")
        
        # Restore health
        cat.is_very_sick = False
        cat.very_sick_timer = 0
        cat.health = 8.0
        cat.hunger = 5.0  # Reset hunger to safe level
        cat.energy = 5.0  # Reset energy to safe level
        cat.trust = min(10, cat.trust + 2)  # Trust increases for saving them
        set_emotion("happy", 5)
        
        return True
    else:
        print(f"\n*poppu takes the {medicine_type} but it doesn't seem to help much*")
        print("*maybe try a different medicine?*")
        cat.health = max(1, cat.health - 0.3)  # Small health penalty for wrong medicine
        cat.very_sick_timer -= 1
        print(f"❤️  Health: {cat.health:.1f}/10")
        print(f"⏰ Time remaining: {cat.very_sick_timer} turns\n")
        return False

# ---------- Cat Behavior Functions ----------
def set_emotion(emotion: str, timer: int = 3) -> None:
    """Set the cat's emotion with a timer."""
    cat.emotion = emotion
    cat.emotion_timer = timer

def decay_emotion() -> None:
    """Reduce emotion timer and reset to neutral when expired."""
    if cat.emotion_timer > 0:
        cat.emotion_timer -= 1
    else:
        if not cat.is_very_sick:  # Don't reset emotion if very sick
            cat.emotion = "neutral"

def decay_sickness() -> None:
    """Reduce sickness timer and clear sickness when expired."""
    if cat.sick_timer > 0:
        cat.sick_timer -= 1
        if cat.sick_timer == 1:
            print("poppu feels better now")
    else:
        cat.is_sick = False

def make_sick(timer: int = 4) -> None:
    """Make the cat sick."""
    cat.is_sick = True
    cat.sick_timer = timer
    set_emotion("sad", timer)

def blink() -> None:
    """Cat blinks or shows neutral behavior."""
    random_choice_print([
        "*slow blink*",
        "looks at you",
        " wagging her tail",
        "meow"
    ])

# ---------- Game Activities ----------
def play_with_laser() -> None:
    """Interactive laser pointer game."""
    while True:
        cat.energy -= 0.5
        
        if cat.energy <= 2:
            print("*poppu feels tired so he sleeps slowly*")
            cat.is_sleeping = True
            cat.energy = 6
            return
        
        action = input("> ").lower().strip()
        
        if has_keywords(["stop", "stope"], action):
            print("poppu jumps to catch the laser but misses and looks confused")
            return
        elif has_keywords(["up", "upp"], action):
            print("poppu jumps up to catch the red dot")
        elif has_keywords(["down"], action):
            print("poppu jumps to catch the red dot")
        elif has_keywords(["left"], action):
            print("poppu jumps to the left side direction to catch the red dot")
        elif has_keywords(["right"], action):
            print("poppu jumps to the right side to catch the laser")
        elif has_keywords(["hit", "fat", "stupid", "dum"], action):
            cat.trust = max(0, cat.trust - 2)
            set_emotion("angry", 5)
            random_choice_print([
                "hits your face",
                "bites you",
                "*ears flatten and tail lashes violently*"
            ])
            return
        else:
            print("*tries to touch the red dot*")

def play_with_ball() -> None:
    """Play ball with the cat."""
    messages = [
        "poppu is chasing the ball",
        "meow",
        "poppu tries to grab it but it rolls away",
        "poppu jumps at the ball, the ball rolls away",
        "poppu tries to grab it",
        "rolls away"
    ]
    for _ in range(7):
        random_choice_print(messages)
    print("poppu looks tired")
    cat.energy = 2

def play() -> None:
    """Main play function."""
    while True:
        cat.energy -= 1
        
        if cat.energy <= 2:
            print("*sleeps slowly*")
            cat.is_sleeping = True
            cat.energy = 6
            return
        
        if cat.emotion == "sad":
            print("*looks at you, not feeling playful*")
            return
        
        action = input("> ").lower().strip()
        
        if action == "sit":
            print("*sitting*")
        elif has_keywords(["laser"], action):
            play_with_laser()
        elif has_keywords(["ball"], action):
            play_with_ball()
        elif action == "roll over":
            print("*rolling over*")
        elif action == "jump":
            print("*jumping*")
        elif has_keywords(["i love you", "good poppu", "cute", "good cat"], action):
            print("licks you")
        elif has_keywords(["stop", "no more"], action):
            print("*stops playing*")
            return
        elif has_keywords(["hit", "fat", "stupid", "dum"], action):
            cat.trust = max(0, cat.trust - 2)
            set_emotion("angry", 5)
            random_choice_print([
                "hits your face",
                "bites you",
                "*ears flatten and tail lashes violently*"
            ])
            return
        else:
            print("*looks at you in confusion*")

# ---------- Interaction Handlers ----------
def handle_food(user_input: str) -> bool:
    """Handle food-related interactions. Returns True if handled."""
    if not has_keywords(["food", "feed", "eat", "eating", "milk", "fish", "meat", "biriyani", "give"], user_input):
        return False
    
    # Very sick cats won't eat
    if cat.is_very_sick:
        print("*poppu is too sick to eat... poppu needs medicine!*")
        return True
    
    # Check if cat is full
    if cat.hunger <= 2:
        print("*sniffs the food and walks away*")
        return True
    
    # Detect food type
    given_food = None
    for food in FAVORITE_FOODS + DISLIKED_FOODS + FORBIDDEN_FOODS:
        if food in user_input:
            given_food = food
            break
    
    # Handle disliked food
    if given_food in DISLIKED_FOODS:
        set_emotion("angry", 2)
        if given_food == "durian":
            print("smells it and feels disgusted")
            cat.trust = max(0, cat.trust - 0.5)
        elif given_food == "lemon":
            print("licks it and makes a disgusted face")
            cat.trust = max(0, cat.trust - 0.4)
        else:
            print("*sniffs it, gags slightly, and walks away*")
            cat.trust = max(0, cat.trust - 0.3)
        return True
    
    # Handle forbidden food - NOW CAN TRIGGER VERY SICK!
    if given_food in FORBIDDEN_FOODS:
        random_choice_print([
            "*sniffs it… eats a little… then looks unwell*",
            "*eats a little... and starts to vomit*"
        ])
        
        # First make normally sick
        make_sick(5)
        cat.hunger = max(0, cat.hunger - 1)
        cat.trust = max(0, cat.trust - 1)
        
        # 40% chance of escalating to very sick from bad food!
        if random.random() < 0.4:
            print("\n⚠️  The food was really bad! Poppu is getting worse!")
            make_very_sick()
        
        return True
    
    # Handle favorite food
    if given_food in FAVORITE_FOODS:
        if random.random() < PICKY_CHANCE and cat.trust < 7:
            print("*sniffs carefully… then ignores it*")
            set_emotion("neutral", 2)
        else:
            cat.hunger = max(0, cat.hunger - 5)
            cat.trust = min(10, cat.trust + 1)
            set_emotion("happy", 4)
            random_choice_print([
                "*eats slowly… then purrs*",
                "*devours it happily*",
                "*meows approvingly while eating*"
            ])
        return True
    
    # Unknown food
    print("*sniffs cautiously… unsure about this food*")
    return True

def handle_medicine(user_input: str) -> bool:
    """Handle giving medicine. Returns True if handled."""
    if not has_keywords(["medicine", "med", "antibiotic", "pain relief", "fever medicine", "stomach medicine", "give medicine"], user_input):
        return False
    
    # Extract medicine type
    medicine_type = None
    for med in MEDICINES:
        if med in user_input:
            medicine_type = med
            break
    
    if medicine_type:
        give_medicine(medicine_type)
    else:
        if cat.is_very_sick:
            print(f"Which medicine? Available: {', '.join(MEDICINES)}")
        else:
            print("*poppu doesn't need medicine right now*")
    
    return True

def handle_sleeping_state(user_input: str) -> bool:
    """Handle interactions when cat is sleeping. Returns True if still sleeping."""
    if not cat.is_sleeping:
        return False
    
    if has_keywords(["wake"], user_input):
        cat.is_sleeping = False
        print("*opens one eye slowly*")
        return False
    else:
        print("*sleeps quietly*")
        return True

def handle_sick_state(user_input: str) -> bool:
    """Handle interactions when cat is sick. Returns True if handled."""
    if not cat.is_sick:
        return False
    
    if has_keywords(["pet", "hug", "cuddle", "are you okay"], user_input):
        print("*leans weakly into you and purrs softly*")
        cat.trust = min(10, cat.trust + 0.3)
    elif has_keywords(["food", "feed", "give"], user_input):
        print("*sniffs the food but turns away*")
    else:
        random_choice_print([
            "*lies down quietly, not feeling well*",
            "*lets out a small, weak meow*",
            "*breathes slowly, eyes half closed*"
        ])
    return True

def handle_very_sick_state(user_input: str) -> bool:
    """Handle interactions when cat is very sick. Returns True if handled."""
    if not cat.is_very_sick:
        return False
    
    # Medicine handling is done separately
    if has_keywords(["medicine", "med"], user_input):
        return False  # Let handle_medicine deal with it
    
    if has_keywords(["pet", "hug", "cuddle", "are you okay", "status", "check"], user_input):
        print("*poppu weakly lifts head to look at you*")
        print(f"❤️  Health: {cat.health:.1f}/10")
        print(f"⏰ Time remaining: {cat.very_sick_timer} turns")
        print("💊 Poppu desperately needs medicine!")
        cat.trust = min(10, cat.trust + 0.2)
    else:
        random_choice_print([
            "*lies limply, breathing heavily*",
            "*makes a weak, pained meow*",
            "*trembles slightly, looking very unwell*",
            "*barely moves, eyes glazed over*"
        ])
    return True

def handle_default_response() -> None:
    """Handle default responses based on emotion."""
    if cat.emotion == "happy":
        random_choice_print(["*slow blinks affectionately*", "*licks you*"])
    elif cat.emotion == "sad":
        print("*stays close, quiet*")
    elif cat.emotion == "angry":
        cat.closeness = 3
        print("*keeps distance, ears low*")
    else:
        blink()

# ---------- Main Game Loop ----------
def main():
    """Main game loop."""
    current_time = datetime.now()
    print(f"🐾 Game started at: {current_time.strftime('%I:%M %p')}")
    print(f"⏰ Current hour: {current_time.hour}:00")
    print("🐾 Companion is here. Type 'bye' to rest.")
    print("⚠️  WARNING: Keep poppu fed and rested, or serious illness may occur!\n")
    
    # Counter for triggering random events
    interaction_count = 0
    
    while True:
        user_input = input("> ").lower().strip()
        
        # Update states
        decay_emotion()
        decay_sickness()
        cat.hunger = min(10, cat.hunger + 0.2)
        
        # Check for very sick progression
        if cat.is_very_sick:
            if decay_very_sick():
                break  # Game over - cat passed out
        
        # Check for critical conditions (hunger/energy at 0)
        if not cat.is_very_sick:
            check_critical_condition_sickness()
        
        # Check for 3 AM zoomies (only if not very sick)
        interaction_count += 1
        if not cat.is_very_sick and interaction_count % 3 == 0:
            if check_3am_zoomies():
                trigger_zoomies()
                continue
        
        # Warning messages for critical stats
        if cat.hunger >= 9 and not cat.is_very_sick:
            print("⚠️  Poppu is STARVING! Feed poppu immediately!")
        elif cat.hunger >= 8 and not cat.is_very_sick:
            print("⚠️  Poppu is very hungry and getting weak...")
        
        if cat.energy <= 1 and not cat.is_very_sick and not cat.is_sleeping:
            print("⚠️  Poppu is EXHAUSTED! Let poppu rest immediately!")
        elif cat.energy <= 2 and not cat.is_very_sick and not cat.is_sleeping:
            print("⚠️  Poppu is very tired...")
        
        # Cat responds to name
        if has_keywords(["poppu"], user_input):
            if not cat.is_very_sick:
                print("meow")
            else:
                print("*weak meow...*")
        
        # Exit condition
        if user_input in ["bye", "exit", "good night"]:
            print("*curls up and sleeps*")
            break
        
        # Handle special states first (priority order matters!)
        if handle_very_sick_state(user_input):
            continue
        
        # Medicine can be given in any state
        if handle_medicine(user_input):
            continue
        
        if handle_sleeping_state(user_input):
            continue
        if handle_sick_state(user_input):
            continue
        
        # Introduction
        if "i am" in user_input:
            print("*looks at you calmly*")
            cat.trust = min(10, cat.trust + 0.5)
            if not cat.recognized and user_input in ["i am amritha", "i am amritha p"]:
                cat.recognized = True
                print("poppu smells you and remembers you from its past")
                print("poppu feels happy to see you again")
                set_emotion("happy", 4)
                cat.trust = min(10, cat.trust + 1)
                print("*poppu looks at you for a hug*")
            continue
        
        # Emotions
        if has_keywords(["sad", "lonely", "cry"], user_input):
            set_emotion("sad", 4)
            print("*rests head gently*")
            continue
        
        # Hunger check
        if has_keywords(["hungry", "hunger"], user_input):
            if cat.hunger >= 7:
                print("*meows softly and looks at you for food*")
            elif cat.hunger >= 4:
                print("*looks at you expectantly*")
            else:
                blink()
            continue
        
        # Food interactions
        if handle_food(user_input):
            continue
        
        # Stay away
        if has_keywords(["go away", "stay away", "get lost", "shoo"], user_input):
            set_emotion("sad", 2)
            print("*moves away from you looking sad*")
            continue
        
        # Come here
        if has_keywords(["come here", "come closer", "sit next", "sit with"], user_input):
            if cat.emotion == "angry":
                cat.closeness = 3
                print("*refuses and stays away*")
            else:
                closeness_responses = {
                    3: ("comes closer", 2),
                    2: ("*comes more closer*", 1),
                    1: ("*sits on your lap*", 0),
                    0: (random.choice(["*looks at as if you are dumb*", "*checks if you are okay with its paw*"]), 0)
                }
                response, new_closeness = closeness_responses[cat.closeness]
                print(response)
                cat.closeness = new_closeness
                cat.trust = min(10, cat.trust + 0.2)
            continue
        
        # Hug
        if has_keywords(["hug", "hugg", "cuddle"], user_input):
            if cat.emotion == "angry":
                print("*steps back, not in the mood*")
            else:
                print("presses head into your chest")
                set_emotion("happy", 3)
            continue
        
        # Pet
        if has_keywords(["pet", "scratch", "scritch"], user_input):
            if cat.emotion == "angry":
                print("*moves away from your hand*")
            else:
                print("*purrs softly*")
                cat.trust = min(10, cat.trust + 0.3)
            continue
        
        # Belly
        if has_keywords(["belly", "stomach"], user_input):
            set_emotion("angry", 3)
            print("*ears flatten in warning*")
            continue
        
        # Insults
        if has_keywords(["hit", "fat", "stupid", "dum"], user_input):
            cat.trust = max(0, cat.trust - 2)
            set_emotion("angry", 5)
            cat.closeness = 3
            random_choice_print([
                "hits your face",
                "bites you",
                "*ears flatten and tail lashes violently*",
                "*hisses at you and jumps away...*"
            ])
            continue
        
        # Sleep
        if has_keywords(["sleep", "rest"], user_input):
            cat.is_sleeping = True
            cat.energy = 6
            if cat.emotion == "angry":
                cat.closeness = 3
                print("*curls up and falls asleep away from you*")
            else:
                print("*curls up and falls asleep beside you*")
            continue
        
        # Play
        if has_keywords(["play"], user_input):
            if cat.emotion == "happy":
                print("*meow*")
                play()
            elif cat.emotion == "angry":
                print("*keeps distance, not in the mood to play*")
                cat.closeness = 3
            continue
        
        # Manual zoomies trigger for testing
        if has_keywords(["zoomies", "crazy", "run around"], user_input):
            if not cat.is_very_sick:
                trigger_zoomies()
            else:
                print("*poppu is too sick for zoomies...*")
            continue
        
        # Default response
        handle_default_response()

if __name__ == "__main__":
    main()
