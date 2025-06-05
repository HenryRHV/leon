# Simple agent implementation based on planning/execution pseudocode
from __future__ import annotations
import json
from typing import Any, Dict, List

class Planner:
    def create_plan(self, goal: str) -> List[Dict[str, Any]]:
        # For demo purposes simply create a single step that echoes the goal
        return [{"action": "echo", "args": goal, "requires_confirmation": False}]

class Memory:
    def __init__(self, path: str = "agent_memory.json"):
        self.path = path
        self.data: Dict[str, Any] = {}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def store_plan(self, plan: List[Dict[str, Any]]):
        self.data["plan"] = plan
        self._save()

    def store_step(self, step: Dict[str, Any], result: Any):
        steps = self.data.setdefault("steps", [])
        steps.append({"step": step, "result": result})
        self._save()

    def get(self, key: str) -> Any:
        return self.data.get(key)

class Executor:
    def execute(self, step: Dict[str, Any]) -> Any:
        action = step.get("action")
        if action == "echo":
            return step.get("args")
        raise NotImplementedError(f"Unknown action {action}")


def ask_user(result: Any) -> bool:
    reply = input(f"Step result: {result}. Continue? [y/N] ")
    return reply.strip().lower() in {"y", "yes"}


def run_agent(goal: str) -> Any:
    planner = Planner()
    executor = Executor()
    memory = Memory()

    plan = planner.create_plan(goal)
    memory.store_plan(plan)

    for step in plan:
        result = executor.execute(step)
        memory.store_step(step, result)

        if step.get("requires_confirmation"):
            if not ask_user(result):
                break

    memory.data["final_result"] = result
    memory._save()
    return memory.get("final_result")

if __name__ == "__main__":
    goal = input("Enter goal: ")
    output = run_agent(goal)
    print("Final output:", output)
