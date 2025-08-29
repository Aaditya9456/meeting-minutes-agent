from agents import function_tool
from typing import List, Dict, Any

@function_tool
def get_meeting_minutes(meeting_notes: str) -> str:
    print("Getting meeting minutes...")