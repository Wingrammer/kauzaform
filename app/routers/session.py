from pathlib import Path as OSPath
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from app.db.models.option import USSDOption
from app.db.models.state import USSDState
from app.routers.state import get_state
from app.routers.ussd_app import get_app_by_code
from app.schemas.session import USSDSession
from app.db.models.ussd_app import USSDApp

from datetime import datetime, timedelta
import uuid

# Assuming templates directory is in the parent directory of main.py
templates = Jinja2Templates(directory=str(OSPath(__file__).parent / "templates"))

def generate_session_id() -> str:
    """
    Generate a unique session ID using UUID.
    """
    return str(uuid.uuid4())


router = APIRouter()
# Session memory dictionary to store sessions
session_memory: Dict[str, USSDSession] = {}
# Maintain a separate dictionary to track user_id to session_id mapping for each app
user_app_session_mapping: Dict[str, Dict[int, str]] = {}

def save_session(session: USSDSession):
    """
    Save the session to the session memory.
    """
    session_memory[session.id] = session
    # Update user_id to session_id mapping for the specific app_id
    app_session_mapping = user_app_session_mapping.setdefault(session.user_id, {})
    app_session_mapping[session.app_id] = session.id

async def get_session_from_memory(user_id: str, ussd_app: USSDApp, session: Optional[USSDSession] = None, resume_old_session: bool = False) -> Optional[USSDSession]:
    """
    Retrieve the session from the session memory.
    """
    
    if session is None:
        # Check if there is a session_id associated with the user_id for the specific app_id
        app_session_mapping = user_app_session_mapping.get(user_id, {})
        session_id = app_session_mapping.get(ussd_app.id)
        if session_id:
            removed_session = session_memory.pop(session_id, None)
            if removed_session:
                if resume_old_session:
                    session = removed_session
                else:
                    session = await initialize_session(ussd_app)
    if session.id not in session_memory:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.expiration is not None and session.expiration < datetime.utcnow():
        session_memory.pop(session.id)
        raise HTTPException(status_code=404, detail="Session expired")
    
    return session_memory.get(session.id)


# ... (OAuth2 and dependencies remain the same)

# Dependency to initialize or retrieve a session
def initialize_or_get_session(
    user_id: str,
    ussd_app: USSDApp,
    session: Optional[USSDSession] = Depends(get_session_from_memory),
    resume_old_session: bool = False,
) -> USSDSession:
    return session
@router.post("/init-session/{app_id}", response_model=USSDSession)
async def initialize_session(
    user_id: str,
    ussd_app: USSDApp
):
    """
    Initialize a USSD session.
    """
    # Validate that the user has access to the specified USSD app
    # user_has_access = await check_user_access_to_app(fusionauth_user.sub, app_id)
    # if not user_has_access:
    #     raise HTTPException(status_code=403, detail="User does not have access to this app")

    # Calculate session expiration time (adjust based on your requirements)
    expiration_time = datetime.utcnow() + timedelta(minutes=ussd_app.session_expiry)

    # Create a new USSD session
    session_id = generate_session_id()  # Implement a function to generate unique session IDs
    session = USSDSession(
        session_id=session_id,
        app_id=ussd_app.id,
        user_id=user_id,
        expiration=expiration_time,
        current_state=None,  # Set to the initial state
        # Add other session-related fields as needed
    )
    
    # Save the session to the session memory
    save_session(session)

    return session

@router.post("/ussd-entry/{app_code}")
async def ussd_entry_point(
    user_id: str,
    user_input: str,
    app_code: str = Path(..., title="The USSD code or identifier for the app."),
    secret: Optional[str] = None,
    ussd_app: USSDApp = Depends(get_app_by_code),  # Using Dependency Injection
    session: USSDSession = Depends(initialize_or_get_session),
    resume_old_session: Optional[bool] = False,
):
    # Ensure the session belongs to the specified USSD app
    if session.app_id != ussd_app.id:
        raise HTTPException(status_code=403, detail="Session does not belong to this app")
    
    # Ensure the app has a initial_state defined
    if ussd_app.initial_state is None:
        raise HTTPException(status_code=400, detail="The app does not have a version ready for production.")

    # If the session's current_state is None, set it to the initial_state of the USSDApp
    if session.current_state is None or not resume_old_session:
        session.current_state = ussd_app.initial_state
        save_session(session)

    # Retrieve the current state based on the session's current_state
    current_state = get_state(session.current_state)

    # Retrieve the main menu options
    main_menu_options = get_state(ussd_app.initial_state).options
    
    # If it is the initial state, display the message and options using a Jinja template
    if current_state.id == ussd_app.initial_state:
        # Retrieve the main menu options
        main_menu_options = get_state(ussd_app.initial_state).options

        # Use the response template if available, otherwise use a default template
        template_data = {"message": current_state.message, "options": main_menu_options}
        # response_html = templates.TemplateResponse(current_state.response_template or "default_response_template.txt", {"request": None, "data": template_data})
        # return response_html
    # Determine the next state based on user input or the default next state
    next_state = get_next_state(user_input, current_state, main_menu_options)

    # Update the session's current_state
    session.current_state = next_state
    save_session(session)

    # Implement logic based on the next state, options, etc.
    response_message = generate_response_message(next_state, ussd_app)

    return {"message": response_message}

def generate_response_message(next_state, ussd_app):
    # Get the USSDState object for the next state
    next_state_obj = get_state(next_state)

    # Check if there is a response template defined
    if next_state_obj.response_template:
        # Render the response using the template
        rendered_response = templates.TemplateResponse(
            name=next_state_obj.response_template,
            context={"ussd_app": ussd_app, "next_state": next_state_obj},
            media_type="text/plain",
        ).body.decode("utf-8")

        return rendered_response
        # return ''

    # If no response template is defined, return a default message
    return f"Default message for state {next_state}"

# Determine the next state based on user input or the default next state
def get_next_state(user_input:str, current_state: USSDState, main_menu_options: List[USSDOption]):
    # Implement logic based on the current state, options, etc.

    # Check if user_input matches any of the options in the current state
    if user_input in [option.option_value for option in current_state.options]:
        # Logic to handle when user_input matches an option
        # ...
        pass
    else:
        # Logic to handle when user_input does not match any option
        # raise http error
        raise HTTPException(status_code=400, detail="Invalid input")
    
    return current_state