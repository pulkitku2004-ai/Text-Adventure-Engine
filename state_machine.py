class InvalidTransition (Exception):
    pass


class StateMachine:
    #we store properties that every instance of class needs to have
    #self is a box that travels with the object forever
    #self is a bag that init fills it once, every other methods reaches into it w/o refilling it, travels with the object for its entire lifetime
    def __init__(self, transitions, state, guards=None):
        self.transitions = transitions
        self.guards = guards
        self.state = state


    #legal events available
    #from Hall can go only South to Study, from Study can go North for Hall and East for Vault, no other
    #cant go anywhere from Vault, it is the goal
    #if key in inventory, then path open to Vault from Study, else Blocked
    def available_events(self, state):
        return self.state[state]["exits"]
        
    
    #transition is pure state in, state out function
    #context it receives is player state
    def transition (self, state, event, context):

        if event not in self.available_events(state):
            raise InvalidTransition
        
        #use is not instead of != and use and instead of &
        if self.guards is not None and (state, event) in self.guards:
            result =  self.guards[(state, event)](context) # self.guards[(state, event)] retrieves the has_key function from the dict.
            #adding context calls the function with context with argument

            if result == False:
                raise InvalidTransition
        
        return self.transitions[(state, event)]
    

"""machine = StateMachine(transitions, guards)

print(machine.available_events("Vault"))
print(machine.transition("Study", "North", "ok"))
"""