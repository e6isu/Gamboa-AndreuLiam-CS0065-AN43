"""
CS0065 - Intelligent Systems
Technical Assessment 2: Rule-Based Agent (Vacuum Cleaner)
File: TA2_Gamboa.py
"""


# ================= Task 1: Environment Setup =================
class Environment:
    def __init__(self, rooms=None):
        # Default initialization for rooms (Task 1 & Bonus Task)
        if rooms is None:
            self.rooms = {"A": "Dirty", "B": "Dirty"}
        else:
            self.rooms = rooms

    def is_dirty(self, room):
        """Check if the given room is dirty."""
        return self.rooms.get(room, "").lower() == "dirty"

    def clean_room(self, room):
        """Clean the specified room."""
        if room in self.rooms:
            self.rooms[room] = "Clean"

    def display_grid(self, agent_location):
        """Bonus Task: Text-based grid visualization."""
        room_visuals = []
        for room in sorted(self.rooms.keys()):
            status = self.rooms[room]
            marker = "[*AGENT*]" if room == agent_location else "[       ]"
            room_visuals.append(f"Room {room}: {status:<5} {marker}")
        return " | ".join(room_visuals)


# ================= Task 2: Rule-Based Agent =================
class RuleBasedVacuumAgent:
    def __init__(self, starting_room="A"):
        self.location = starting_room

    def perceive_and_act(self, env):
        """
        Rule 1: If the current room is dirty, clean it.
        Rule 2: If the current room is clean, move to another room.
        """
        if env.is_dirty(self.location):
            # Rule 1
            env.clean_room(self.location)
            return f"CLEANED Room {self.location}"
        else:
            # Rule 2
            old_location = self.location
            self.move(env)
            return f"MOVED from Room {old_location} to Room {self.location}"

    def move(self, env):
        """Switch rooms in cyclic order (supports 2 or more rooms)."""
        available_rooms = sorted(list(env.rooms.keys()))
        current_index = available_rooms.index(self.location)
        next_index = (current_index + 1) % len(available_rooms)
        self.location = available_rooms[next_index]


# ================= Task 3: Simulation Loop =================
def run_simulation():
    print("=" * 60)
    print("      CS0065 - RULE-BASED VACUUM AGENT SIMULATION")
    print("=" * 60)

    # Task 1: Allow user to set initial environment state
    print("\n--- Set Initial Room States ---")
    state_a = input("Enter state for Room A (Clean/Dirty) [Default: Dirty]: ").strip().capitalize()
    if state_a not in ["Clean", "Dirty"]:
        state_a = "Dirty"

    state_b = input("Enter state for Room B (Clean/Dirty) [Default: Dirty]: ").strip().capitalize()
    if state_b not in ["Clean", "Dirty"]:
        state_b = "Dirty"

    # Optional Bonus Room C prompt
    include_c = input("Include Room C for Bonus Task? (y/n) [Default: n]: ").strip().lower()
    initial_rooms = {"A": state_a, "B": state_b}

    if include_c == 'y':
        state_c = input("Enter state for Room C (Clean/Dirty) [Default: Dirty]: ").strip().capitalize()
        if state_c not in ["Clean", "Dirty"]:
            state_c = "Dirty"
        initial_rooms["C"] = state_c

    start_loc = input(f"Choose starting room ({'/'.join(sorted(initial_rooms.keys()))}) [Default: A]: ").strip().upper()
    if start_loc not in initial_rooms:
        start_loc = "A"

    steps = int(input("Enter number of simulation steps: "))

    # Initialize environment and agent
    env = Environment(initial_rooms)
    agent = RuleBasedVacuumAgent(starting_room=start_loc)

    print("\n" + "=" * 60)
    print("SIMULATION INITIAL STATE:")
    print(f"Agent Location: Room {agent.location}")
    print(f"Environment: {env.rooms}")
    print(f"Grid: {env.display_grid(agent.location)}")
    print("=" * 60 + "\n")

    # Step loop
    for step in range(1, steps + 1):
        print(f"--- STEP {step}/{steps} ---")
        current_loc = agent.location
        action = agent.perceive_and_act(env)

        print(f"Agent Current Location : Room {current_loc}")
        print(f"Action Taken           : {action}")
        print(f"Current Environment    : {env.rooms}")
        print(f"Visualization          : {env.display_grid(agent.location)}")
        print("-" * 60)

    print("\n================ FINAL SIMULATION RESULT ================")
    print(f"Final Room States : {env.rooms}")
    print(f"Final Agent Pos   : Room {agent.location}")
    print("=========================================================\n")


if __name__ == "__main__":
    run_simulation()