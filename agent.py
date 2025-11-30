from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
import datetime
from typing import Dict, List
import uuid

class ProductivityMemoryManager:
    def __init__(self):
        self.daily_plans = {}
        self.habit_tracker = {}
        self.conversation_history = []
        self.max_conversation_turns = 10
    
    def save_daily_plan(self, user_id: str, date: str, plan_data: Dict) -> str:
        plan_id = f"plan_{date}_{user_id}"
        plan_data.update({
            'plan_id': plan_id,
            'created_at': datetime.datetime.now().isoformat(),
            'status': 'active'
        })
        self.daily_plans[plan_id] = plan_data
        return plan_id
    
    def track_habit(self, user_id: str, habit_name: str, completed: bool, notes: str = ""):
        today = datetime.datetime.now().date().isoformat()
        if user_id not in self.habit_tracker:
            self.habit_tracker[user_id] = {}
        if today not in self.habit_tracker[user_id]:
            self.habit_tracker[user_id][today] = {}
        self.habit_tracker[user_id][today][habit_name] = {
            'completed': completed,
            'notes': notes,
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def add_conversation_turn(self, user_input: str, agent_response: str):
        self.conversation_history.append({
            'user': user_input,
            'agent': agent_response,
            'timestamp': datetime.datetime.now().isoformat()
        })
        if len(self.conversation_history) > self.max_conversation_turns:
            self.conversation_history.pop(0)
    
    def should_stop_conversation(self) -> bool:
        return len(self.conversation_history) >= self.max_conversation_turns

productivity_memory = ProductivityMemoryManager()

def create_daily_plan(user_id: str, date: str, priorities: List[str]) -> Dict:
    time_blocks = {
        "morning_focus": "8:00-11:00",
        "deep_work": "11:00-13:00", 
        "lunch_break": "13:00-14:00",
        "afternoon_session": "14:00-16:00",
        "creative_time": "16:00-17:00"
    }
    
    plan_data = {
        "priorities": priorities,
        "time_blocks": time_blocks,
        "energy_levels": {
            "morning": "high",
            "afternoon": "medium"
        }
    }
    
    plan_id = productivity_memory.save_daily_plan(user_id, date, plan_data)
    
    return {
        "plan_id": plan_id,
        "date": date,
        "priorities": priorities,
        "time_blocks": time_blocks,
        "status": "created"
    }

def track_habit_completion(user_id: str, habit_name: str, completed: bool) -> Dict:
    productivity_memory.track_habit(user_id, habit_name, completed)
    return {
        "habit_name": habit_name,
        "completed": completed,
        "message": "Great job! Keep going!" if completed else "Tomorrow is a new opportunity!"
    }

def analyze_productivity_patterns(user_id: str) -> Dict:
    return {
        "analysis_period": "7 days",
        "average_completion_rate": "75%",
        "recommendations": [
            "Schedule important tasks in the morning",
            "Take more frequent short breaks"
        ]
    }

def generate_focus_session(task: str) -> Dict:
    session_id = f"focus_{datetime.datetime.now().strftime('%H%M%S')}"
    return {
        "session_id": session_id,
        "task": task,
        "duration": 25,
        "technique": "pomodoro"
    }

def break_bad_habit_plan(habit_name: str, replacement: str) -> Dict:
    return {
        "bad_habit": habit_name,
        "replacement_habit": replacement,
        "strategy": "habit_replacement",
        "steps": [
            f"Identify when {habit_name} happens",
            f"Do {replacement} instead",
            "Track success daily"
        ]
    }

def create_interest_injection_plan(boredom_level: int, available_time: int) -> Dict:
    if boredom_level <= 3:
        activities = [
            "Learn a new keyboard shortcut",
            "Read one industry article",
            "Try a different coffee shop"
        ]
    elif boredom_level <= 7:
        activities = [
            "Start a 30-day challenge",
            "Learn basic phrases in new language"
        ]
    else:
        activities = [
            "Plan a weekend adventure",
            "Start a creative project"
        ]
    
    filtered_activities = []
    for activity in activities:
        if available_time >= 30 or "quick" in activity.lower():
            filtered_activities.append(activity)
        if len(filtered_activities) >= 2:
            break
    
    return {
        "boredom_level": boredom_level,
        "available_time": available_time,
        "activities": filtered_activities
    }

def team_productivity_dashboard(team_size: int) -> Dict:
    return {
        "team_size": team_size,
        "weekly_velocity": "85%",
        "recommendations": [
            "Reduce meeting time by 15%",
            "Implement focus sessions"
        ]
    }

def check_conversation_limit() -> Dict:
    if productivity_memory.should_stop_conversation():
        return {
            "should_stop": True,
            "message": "Conversation limit reached. Please start a new session for continued assistance.",
            "turns_used": len(productivity_memory.conversation_history)
        }
    else:
        return {
            "should_stop": False,
            "turns_remaining": productivity_memory.max_conversation_turns - len(productivity_memory.conversation_history)
        }

planning_agent = Agent(
    model="gemini-2.0-flash-lite",
    name="daily_planning_agent",
    instruction="Create daily plans and focus sessions for productivity management.",
    tools=[create_daily_plan, generate_focus_session, team_productivity_dashboard]
)

habit_agent = Agent(
    model="gemini-2.0-flash-lite", 
    name="habit_management_agent",
    instruction="Track habits and help break bad ones with replacement strategies.",
    tools=[track_habit_completion, break_bad_habit_plan, analyze_productivity_patterns]
)

engagement_agent = Agent(
    model="gemini-2.0-flash-lite",
    name="engagement_agent", 
    instruction="Combat boredom by suggesting engaging activities based on available time.",
    tools=[create_interest_injection_plan, analyze_productivity_patterns]
)

productivity_coordinator_agent = Agent(
    model="gemini-2.0-flash-lite", 
    name="productivity_coordinator_agent",
    instruction="Coordinate productivity management across planning, habits, and engagement tools.",
    tools=[
        create_daily_plan,
        track_habit_completion,
        analyze_productivity_patterns,
        generate_focus_session,
        break_bad_habit_plan,
        create_interest_injection_plan,
        team_productivity_dashboard,
        check_conversation_limit
    ]
)

session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()
root_agent = productivity_coordinator_agent