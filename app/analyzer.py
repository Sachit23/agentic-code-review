from app.llm import analyze_code
import traceback


def run_analysis(diff):
    try:
        return analyze_code(diff)
    except Exception as e:
        tb = traceback.format_exc()
        return f"Analysis failed with exception: {e}\n\nTraceback:\n{tb}"

