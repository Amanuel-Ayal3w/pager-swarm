"""Compile the incident graph."""

from langgraph.graph import END, START, StateGraph

from pager.graph.nodes import (
    after_approval,
    after_plan,
    after_triage,
    after_verify,
    approve,
    diagnose,
    execute,
    investigate,
    plan,
    triage,
    verify,
)
from pager.graph.state import IncidentState


def build_graph(checkpointer):
    graph = StateGraph(IncidentState)
    graph.add_node("triage", triage)
    graph.add_node("investigate", investigate)
    graph.add_node("diagnose", diagnose)
    graph.add_node("plan", plan)
    graph.add_node("approve", approve)
    graph.add_node("execute", execute)
    graph.add_node("verify", verify)
    graph.add_edge(START, "triage")
    graph.add_conditional_edges("triage", after_triage, ["investigate", END])
    graph.add_edge("investigate", "diagnose")
    graph.add_edge("diagnose", "plan")
    graph.add_conditional_edges("plan", after_plan, {"approve": "approve", "end": END})
    graph.add_conditional_edges("approve", after_approval, {"execute": "execute", "investigate": "triage", "end": END})
    graph.add_edge("execute", "verify")
    graph.add_conditional_edges("verify", after_verify, {"approve": "approve", "end": END})
    return graph.compile(checkpointer=checkpointer)
