from state_machine import StateMachine, InvalidTransition
import json

file_path = "world.json"
with open(file_path, "r", encoding="utf-8") as json_file:
    # Load the JSON content back into a Python dictionary
    state = json.load(json_file)

def has_key(context):
    if "key" in context:
        return True
    else:
        return False

guards = {
    ("Study", "East"):has_key
}

transitions = {
    ("Hall", "South"): "Study",
    ("Study", "North"): "Hall",
    ("Study", "East"): "Vault"
}


"""
state = {
    "Hall": {},
    "Study": {},
    "Vault": {}
}
state["Hall"] = {
    "desc": "It is the first room, where we spawn.",
    "list": ["key"],
    "exits": {"South": "Study"}
}        
state["Study"] = {
    "desc": "This is where the guard exists if we move towards East, It checks if key is in inventory.",
    "list": [],
    "exits": {"North": "Hall", 
              "East": "Vault"}
}
state["Vault"] = {
    "desc": "The Goal, the function here rests.",
    "list": [],
    "exits": {"Final": "State"}
}

file_path = "world.json"

with open(file_path, "w", encoding="utf-8") as json_file:
    # indent=4 makes the file human-readable and pretty-printed
    # ensure_ascii=False keeps special characters intact
    json.dump(state, json_file, indent=4, ensure_ascii=False)
print(f"Data successfully saved to {file_path}")
"""
current_room = "Hall"

player_move = StateMachine(transitions, state, guards)
print("Put the move in this pattern: 'go <Direction>'")
print("Choose what you want: 'Go', 'take', 'check'")

inventory = []
while True:

    room_info = player_move.state[current_room]
    print()
    print (room_info)

    user_input = input("Enter your move here: ")

    if user_input.startswith('go '):
        user_input = user_input.split()[1].capitalize()
        try:
            move_result = player_move.transition(current_room, user_input, inventory)
        
        except InvalidTransition:  
            print("\nInvalidTransaction, no exit exists in state.")
        else:
            current_room = move_result
            print(f"Current Room: {current_room}")
    
    elif user_input == "check":
        print(inventory)
        print(current_room)

    elif user_input == "take key":
        wanted_item = user_input.split()[1]
        if wanted_item in player_move.state[current_room]["list"]:
            inventory.append(wanted_item)
            player_move.state[current_room]["list"].remove(wanted_item)
        print(f"Updated inventory: {inventory}")

    if current_room == "Vault":
        print("Goal Achieved")
        break
