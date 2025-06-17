from langgraph.graph import StateGraph, END
from typing import Dict, Any
from models.calendar_event_model import CalendarEventModel
from agents.calendar_agent import CalendarAgent

State = Dict[str, Any]

def create_calendar_graph():
    parser = CalendarEventModel()
    calendar = CalendarAgent()

    g = StateGraph(State)

    # Directly wrap function (no StructuredTool)
    def parse_input_fn(state: Dict[str, Any]) -> Dict[str, Any]:
        return {"parsed": parser.parse(state["text"])}

    def calendar_flow_fn(state: Dict[str, Any]) -> Dict[str, Any]:
        return calendar.process_calendar_flow(state["parsed"])

    g.add_node("parse_input", parse_input_fn)
    g.add_node("calendar_flow", calendar_flow_fn)

    g.set_entry_point("parse_input")
    g.add_edge("parse_input", "calendar_flow")
    g.add_edge("calendar_flow", END)

    return g.compile()

if __name__ == "__main__":
    graph = create_calendar_graph()
    user_input = {"text": "Schedule a 30-minute Zoom meeting with alice and bob tomorrow afternoon"}
    result = graph.invoke(user_input)
    print(result)
