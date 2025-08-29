from agents import Agent
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, List
import os
import asyncio
from agents import Runner

# Load environment variables
load_dotenv()

class ActionItem(BaseModel):
    task: str
    owner: Optional[str] = None
    due: Optional[str] = None

class MeetingMinutes(BaseModel):
    summary: str
    decisions: List[str]
    action_items: List[ActionItem]

async def  generate_meeting_minutes(transcript: str) -> dict:
    """
    Generate meeting minutes from transcript using OpenAI Agent SDK
    
    Args:
        transcript (str): The meeting transcript text
        
    Returns:
        dict: Meeting minutes with summary, decisions, and action items
    """
    try:
        # Check if OpenAI API key is available
        if "OPENAI_API_KEY" not in os.environ:
            raise ValueError("OPENAI_API_KEY environment variable not found")
        
        agent = Agent(
            name="MeetingMinutesAgent",
            instructions="""
You are a Meeting Minutes Agent. 
Your job is to take transcripts of meetings and produce:

1. A summary of the discussion
2. Key decisions made
3. Action items with owners and due dates (if mentioned)

Please analyze the transcript and provide a structured response.
""",
            output_type=MeetingMinutes
        )
        
        # Process the transcript
        result = await Runner.run(agent, transcript)    
        output = result.final_output
        print(output)
        # Convert to dictionary format for API response
        return {
            "summary": output.summary,
            "decisions": output.decisions,
            "action_items": [
                {
                    "task": item.task,
                    "owner": item.owner,
                    "due": item.due
                }
                for item in output.action_items
            ]
        }
        
    except Exception as e:
        print(f"Error generating meeting minutes: {str(e)}")
        return {
            "summary": "Error generating meeting minutes",
            "decisions": [],
            "action_items": [],
            "error": str(e)
        }

if __name__ == "__main__":
    sample_transcript = """
    Meeting started at 10:00 AM.
    John discussed the new project timeline.
    Sarah mentioned budget concerns.
    Decision: Project will start next week.
    Action: John to prepare project plan by Friday.
    Action: Sarah to review budget by Monday.
    Meeting ended at 11:00 AM.
    """

    async def main():
        result = await generate_meeting_minutes(sample_transcript)
        print("Meeting Minutes:")
        print(f"Summary: {result['summary']}")
        print(f"Decisions: {result['decisions']}")
        print(f"Action Items: {result['action_items']}")

    asyncio.run(main())
    
