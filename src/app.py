"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Sports activities
    "Soccer": {
        "description": "Join the school soccer team for weekly matches and training.",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 22,
        "participants": []
    },
    "Swimming": {
        "description": "Group swimming lessons and recreational swims.",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": []
    },
    # Artistic activities
    "Painting Workshop": {
        "description": "Explore your creativity with paints and mixed media.",
        "schedule": "Sundays, 2:00 PM - 4:00 PM",
        "max_participants": 10,
        "participants": []
    },
    "Dance Class": {
        "description": "Express yourself through various dance styles.",
        "schedule": "Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 18,
        "participants": []
    },
    # Intellectual activities
    "Book Club": {
        "description": "Discuss and share thoughts on selected books.",
        "schedule": "Tuesdays, 6:00 PM - 7:00 PM",
        "max_participants": 12,
        "participants": []
    },
    "Math Olympiad Prep": {
        "description": "Prepare for math competitions with peers and mentors.",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    if email not in activity["participants"]:
        activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


# Unregister endpoint
@app.post("/activities/{activity_name}/unregister")
def unregister_for_activity(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    try:
        activity["participants"].remove(email)
    except ValueError:
        raise HTTPException(status_code=404, detail="Participant not found")
    return {"message": f"Removed {email} from {activity_name}"}
