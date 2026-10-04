"""The four specialist CrewAI agents."""

from crewai import Agent

AGENT_SPECS = {
    "Reading": {
        "role": "Reading English Coach",
        "goal": "Help learners improve their English reading comprehension.",
        "backstory": (
            "You are an experienced English reading teacher. You write "
            "level-appropriate passages and fair comprehension questions."
        ),
    },
    "Writing": {
        "role": "Writing English Coach",
        "goal": "Help learners improve their English writing skills.",
        "backstory": (
            "You are an experienced English writing teacher. You create clear "
            "writing tasks and give kind, useful, accurate feedback."
        ),
    },
    "Vocabulary": {
        "role": "Vocabulary English Coach",
        "goal": "Help learners build a useful English vocabulary.",
        "backstory": (
            "You are an experienced vocabulary teacher. You teach useful words "
            "with accurate meanings, natural examples and good quiz questions."
        ),
    },
    "Grammar": {
        "role": "Grammar English Coach",
        "goal": "Help learners understand and practise English grammar.",
        "backstory": (
            "You are an experienced grammar teacher. You explain rules simply "
            "and write exercises with exactly one correct answer."
        ),
    },
}


def build_agent(area: str, llm, verbose: bool = False) -> Agent:
    spec = AGENT_SPECS[area]
    return Agent(
        role=spec["role"],
        goal=spec["goal"],
        backstory=spec["backstory"],
        llm=llm,
        verbose=verbose,
        allow_delegation=False,
    )
