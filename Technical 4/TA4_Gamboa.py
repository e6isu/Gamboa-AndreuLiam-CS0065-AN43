"""TA4: Weather advice using KR, RBR and CBR.
Andreu Liam C. Gamboa | AN43 | November 2, 2026
Run: python TA4_Gamboa.py
Run with manual revision: python TA4_Gamboa.py --interactive
"""
from copy import deepcopy
import sys


# PART 1: Six facts organized into three explicit categories.
def make_facts(temp, humidity, rain, wind, outdoors, daytime):
    return {
        "environment": {"temperature": temp, "humidity": humidity},
        "weather": {"is_raining": rain, "strong_wind": wind},
        "activity": {"outdoors": outdoors, "daytime": daytime},
    }


facts = make_facts(32, 85, True, False, True, True)


# PART 2A: Each function implements an IF-THEN rule.
def rule_hot(f):
    if f["environment"]["temperature"] > 30:
        return "Choose a cooler place for the activity."


def rule_rain(f):
    if f["weather"]["is_raining"] and f["activity"]["outdoors"]:
        return "Bring an umbrella."


def rule_humid(f):
    if f["environment"]["humidity"] > 80:
        return "Choose a well-ventilated place."


def rule_wind(f):
    if f["weather"]["strong_wind"] and f["activity"]["outdoors"]:
        return "Move the activity indoors."


# PART 2B: Evaluate every rule against a working-memory copy.
def infer(knowledge):
    working_memory = deepcopy(knowledge)
    rules = [rule_hot, rule_rain, rule_humid, rule_wind]
    actions = []
    for rule in rules:
        action = rule(working_memory)
        print(f"  {rule.__name__}: {'MATCH' if action else 'no match'}")
        if action and action not in actions:
            actions.append(action)
    return actions


# PART 3A: Three illustrative past cases with the same six features.
def build_case_base():
    return [
        {"problem": make_facts(32, 85, True, False, True, False),
         "solution": "Bring an umbrella; choose a cool, ventilated place."},
        {"problem": make_facts(24, 60, False, False, True, True),
         "solution": "Continue the planned outdoor activity."},
        {"problem": make_facts(27, 70, True, True, True, True),
         "solution": "Move the activity indoors until the wind eases."},
    ]


# PART 3B: Similarity = equal feature values / total query features.
# All six features have equal weight; numeric values match exactly.
def similarity(query, past):
    matches = 0
    total = 0
    for category, features in query.items():
        for key, value in features.items():
            total += 1
            if past.get(category, {}).get(key) == value:
                matches += 1
    return matches / total if total else 0.0


def retrieve(query, cases):
    if not cases:
        raise ValueError("The case base must contain at least one case.")
    scores = [similarity(query, case["problem"]) for case in cases]
    for index, score in enumerate(scores, 1):
        print(f"  Case {index}: {score:.2%} similarity")
    # The earliest case wins when scores tie.
    best = max(range(len(cases)), key=lambda i: scores[i])
    print(f"  Retrieved case: {best + 1}")
    return cases[best]


# PART 3C: Reuse the selected solution.
def reuse(case):
    return case["solution"]


# PART 3D: Accept a manual revision, or keep the original solution.
def revise(solution, interactive=False):
    if interactive:
        replacement = input("New solution (Enter keeps original): ").strip()
        if replacement:
            return replacement
    return solution


# PART 3E: Copy the new problem so later edits cannot alter this case.
def retain(query, solution, cases):
    cases.append({"problem": deepcopy(query), "solution": solution})


def show_input(query):
    print("INPUT (temperature in C; humidity in %):")
    for category, features in query.items():
        values = ", ".join(f"{key}={value}" for key, value in features.items())
        print(f"  {category}: {values}")


def main():
    print("RBR - Weather Activity Advice")
    show_input(facts)
    print("PROCESS - Check all four rules:")
    actions = infer(facts)
    print("OUTPUT - Rule-Based Reasoning Actions:")
    for action in actions:
        print(f"- {action}")
    if not actions:
        print("- No rule matched; no action inferred.")

    print("\nCBR - Weather Activity Advice")
    show_input(facts)
    cases = build_case_base()
    print(f"Case base before retention: {len(cases)} cases")
    print("PROCESS - Retrieve:")
    selected = retrieve(facts, cases)
    solution = reuse(selected)
    print(f"Reuse: {solution}")
    final = revise(solution, "--interactive" in sys.argv)
    state = "unchanged" if final == solution else "manually adjusted"
    print(f"Revise: {state}")
    retain(facts, final, cases)
    print(f"Retain: case base now contains {len(cases)} cases")
    print("OUTPUT - Case-Based Reasoning Solution:")
    print(f"- {final}")
    print(f"New case self-similarity: {similarity(facts, cases[-1]['problem']):.2%}")


if __name__ == "__main__":
    main()
