"""Minimal Afirme automation entrypoint."""

from __future__ import annotations

from ..simple_agent import DEFAULT_MAX_STEPS, DEFAULT_MODEL, create_agent, run_agent

DEFAULT_TASK = "Search Afirme's official site for the current auto insurance quote workflow and list the key steps."


def build_agent(task: str = DEFAULT_TASK, *, model: str = DEFAULT_MODEL):
    """Return a preconfigured agent for Afirme tasks."""

    return create_agent(task, model=model)


async def run(
    task: str = DEFAULT_TASK,
    *,
    max_steps: int = DEFAULT_MAX_STEPS,
    model: str = DEFAULT_MODEL,
):
    """Execute the minimal Afirme flow and return the agent history."""

    return await run_agent(task, model=model, max_steps=max_steps)


__all__ = ["DEFAULT_TASK", "build_agent", "run"]
