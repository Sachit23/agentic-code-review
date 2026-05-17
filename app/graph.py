from typing import TypedDict
from app.llm import analyze_code
from langgraph.graph import StateGraph

class PRState(TypedDict):
    diff: str
    security: str
    tests: str
    refactor: str
    
def security_agent(state: PRState):
    prompt = f"""You are a security expert reviewing a code diff.
    Identify any potential security issues in the following diff:
    
    {state['diff']}
    """
    
    result = analyze_code(prompt)
    return {"security": result}

def test_agent(state: PRState):
    prompt = f"""You are a testing expert reviewing a code diff.
    Generate any missing test cases or improvements to existing tests for the following diff:
    
    {state['diff']}
    """
    
    result = analyze_code(prompt)
    return {"tests": result}

def refactor_agent(state: PRState):
    prompt = f"""You are a code quality expert reviewing a code diff.
    Suggest any refactorings or improvements to code quality for the following diff:
    
    {state['diff']}
    """
    
    result = analyze_code(prompt)
    return {"refactor": result}

def build_graph():
    builder = StateGraph(PRState)
    
    builder.add_node("security", security_agent)
    builder.add_node("tests", test_agent)
    builder.add_node("refactor", refactor_agent)
    
    # Sequential for now (Phase 3 = parallel)
    builder.set_entry_point("security")
    builder.add_edge("security", "tests")
    builder.add_edge("tests", "refactor")
    
    return builder.compile()