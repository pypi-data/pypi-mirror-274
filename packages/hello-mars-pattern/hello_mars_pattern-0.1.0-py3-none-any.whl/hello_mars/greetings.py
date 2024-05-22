def hello_from_mercury(day_or_night):
    if day_or_night == "day":
        return "Hello from Mercury during the day!"
    else:
        return "Hello from Mercury! Next planet is Venus."

def hello_from_venus(day_or_night):
    if day_or_night == "day":
        return "Hello from Venus during the day!"
    else:
        return "Hello from Venus! Next planet is Earth."

def hello_from_earth(day_or_night):
    if day_or_night == "day":
        return "Hello from Earth during the day!"
    else:
        return "Hello from Earth! Next planet is Mars."

def hello_from_jupiter(day_or_night):
    if day_or_night == "day":
        return "Hello from Jupiter during the day!"
    else:
        return "Hello from Jupiter! Next planet is Saturn."

def hello_from_saturn(day_or_night):
    if day_or_night == "day":
        return "Hello from Saturn during the day!"
    else:
        return "Hello from Saturn! Next planet is Uranus."

def hello_from_uranus(day_or_night):
    if day_or_night == "day":
        return "Hello from Uranus during the day!"
    else:
        return "Hello from Uranus! No more planets."

def greet_user():
    planet = input("Which planet are you asking from (Mercury, Venus, Earth, Jupiter, Saturn, Uranus)? ").strip().lower()
    day_or_night = input("Is it day or night? ").strip().lower()
    
    greetings = {
        "mercury": hello_from_mercury,
        "venus": hello_from_venus,
        "earth": hello_from_earth,
        "jupiter": hello_from_jupiter,
        "saturn": hello_from_saturn,
        "uranus": hello_from_uranus,
    }
    
    if planet in greetings:
        print(greetings[planet](day_or_night))
    else:
        print("Invalid planet name.")
