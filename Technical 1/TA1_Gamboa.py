"""
CS0065 - Intelligent Systems
Technical Assessment 1: Random Walk Simulation using AgentPy
File: TA1_Gamboa.py
"""

import agentpy as ap
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import Counter


# ================= 1. Agent Definition =================
class SmartWalker(ap.Agent):
    def setup(self):
        self.position = (0, 0)
        self.path = []  # Task 1: Track movement trajectory

    def step(self):
        # Record current position before stepping
        self.path.append(self.position)

        # 4 possible directions (Von Neumann neighborhood)
        possible_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(possible_directions)

        # Task 2: Preferred movement rule (avoid occupied cells)
        occupied_positions = {other.position for other in self.model.agents if other != self}

        chosen_pos = None
        for dx, dy in possible_directions:
            candidate_x = max(0, min(self.model.p.grid_size[0] - 1, self.position[0] + dx))
            candidate_y = max(0, min(self.model.p.grid_size[1] - 1, self.position[1] + dy))
            candidate = (candidate_x, candidate_y)

            if candidate not in occupied_positions:
                chosen_pos = candidate
                break

        # Fallback to bounded step if surrounded
        if chosen_pos is None:
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            chosen_pos = (
                max(0, min(self.model.p.grid_size[0] - 1, self.position[0] + dx)),
                max(0, min(self.model.p.grid_size[1] - 1, self.position[1] + dy))
            )

        self.position = chosen_pos


# ================= 2. Model Definition =================
class RandomWalkModel(ap.Model):
    def setup(self):
        self.agents = ap.AgentList(self, self.p.agents, SmartWalker)
        total_cells = self.p.grid_size[0] * self.p.grid_size[1]
        all_coords = [(x, y) for x in range(self.p.grid_size[0]) for y in range(self.p.grid_size[1])]

        if self.p.agents <= total_cells:
            starting_coords = random.sample(all_coords, self.p.agents)
        else:
            starting_coords = [random.choice(all_coords) for _ in range(self.p.agents)]

        for agent, coord in zip(self.agents, starting_coords):
            agent.position = coord
            agent.path.append(coord)

    def step(self):
        self.agents.step()

    def end(self):
        # Task 3: Analyze and output final coordinates
        print("\n" + "=" * 50)
        print("SIMULATION COMPLETED: FINAL POSITION ANALYSIS")
        print("=" * 50)
        final_positions = [agent.position for agent in self.agents]
        coord_counts = Counter(final_positions)

        for idx, agent in enumerate(self.agents):
            print(f"Agent {idx + 1:02d} -> Final Position: {agent.position} | Total Moves: {len(agent.path) - 1}")

        unique_tiles = len(coord_counts)
        total_tiles = self.p.grid_size[0] * self.p.grid_size[1]
        print("-" * 50)
        print(f"Total Agents: {self.p.agents}")
        print(f"Grid Space: {self.p.grid_size[0]}x{self.p.grid_size[1]} ({total_tiles} cells)")
        print(f"Occupied Unique Cells: {unique_tiles}/{total_tiles} ({unique_tiles / total_tiles * 100:.1f}%)")
        print(f"Overlapped / Clustered Cells: {sum(1 for v in coord_counts.values() if v > 1)}")
        print("=" * 50 + "\n")


# ================= 3. Simulation & Animation =================
def run_simulation():
    print("--- RANDOM WALK SIMULATION PARAMETERS ---")
    num_agents = int(input("Enter number of agents: "))
    grid_size = int(input("Enter grid size (e.g., 10 for 10x10): "))
    num_steps = int(input("Enter number of steps: "))

    parameters = {
        'agents': num_agents,
        'grid_size': (grid_size, grid_size),
        'steps': num_steps
    }

    model = RandomWalkModel(parameters)
    model.setup()

    fig, ax = plt.subplots(figsize=(6, 6))
    colors = plt.cm.tab20.colors

    path_lines = [
        ax.plot([], [], color=colors[i % len(colors)], linestyle='-', linewidth=1.2, alpha=0.5)[0]
        for i in range(parameters['agents'])
    ]
    scat = ax.scatter([], [], s=130, edgecolors='black', zorder=3)

    def init():
        ax.set_xlim(-0.5, model.p.grid_size[0] - 0.5)
        ax.set_ylim(-0.5, model.p.grid_size[1] - 0.5)
        ax.set_xticks(range(model.p.grid_size[0]))
        ax.set_yticks(range(model.p.grid_size[1]))
        ax.grid(True, linestyle=":", alpha=0.6)
        return path_lines + [scat]

    def update(frame):
        model.step()
        for i, agent in enumerate(model.agents):
            xs = [pos[0] for pos in agent.path]
            ys = [pos[1] for pos in agent.path]
            path_lines[i].set_data(xs, ys)

        current_x = [agent.position[0] for agent in model.agents]
        current_y = [agent.position[1] for agent in model.agents]
        scat.set_offsets(list(zip(current_x, current_y)))
        scat.set_color([colors[i % len(colors)] for i in range(model.p.agents)])
        ax.set_title(f"Step {frame + 1}/{model.p.steps} | Random Walk Simulation")

        if frame == model.p.steps - 1:
            model.end()

        return path_lines + [scat]

    # Storing animation in anim so it is retained during execution
    anim = animation.FuncAnimation(
        fig,
        update,
        frames=model.p.steps,
        init_func=init,
        blit=False,
        repeat=False
    )
    plt.show()


if __name__ == "__main__":
    run_simulation()