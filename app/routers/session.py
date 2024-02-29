from pathlib import Path as OSPath
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from app.db.engine import get_db
from app.db.models.option import USSDOption
from app.db.models.state import USSDState
from app.routers.state import get_state
from app.routers.option import get_option
from app.routers.ussd_app import get_app_by_public_id
from app.schemas.session import USSDSession, USSDSessionInput
from app.db.models.ussd_app import USSDApp

from datetime import datetime, timedelta
import uuid

# Assuming templates directory is in the parent directory of main.py
templates = Jinja2Templates(directory=str(OSPath(__file__).parent.parent / "templates"))




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
async def initialize_session(
    public_id: str,
    input: USSDSessionInput
):
    """
    Initialize a USSD session.
    """
    # Validate that the user has access to the specified USSD app
    # user_has_access = await check_user_access_to_app(fusionauth_user.sub, app_id)
    # if not user_has_access:
    #     raise HTTPException(status_code=403, detail="User does not have access to this app")

    # Calculate session expiration time (adjust based on your requirements)
    
    input.app_id = public_id
    expiration_time = datetime.utcnow() + timedelta(minutes=30)
    # session = await get_session_from_memory(input, public_id, USSDSession(**input.model_dump(), expiration = expiration_time))
    session = session_memory.get(input.id)
    if session is not None:
        # save_session(session)
        return session
    session = USSDSession(**input.model_dump(), expiration = expiration_time)
    
    
    # Save the session to the session memory
    save_session(session)
    return session
async def get_session_from_memory(input: USSDSessionInput, public_id: str, session: USSDSession) -> Optional[USSDSession]:
    """
    Retrieve the session from the session memory.
    """
    # print(user_id, public_id, session, resume_old_session)
    # print(input.app_id, public_id)
    
    # print(input.app_id)
    # raise HTTPException(status_code=404, detail=f"{input.app_id}, {public_id}")
    # if session is None:
        # Check if there is a session_id associated with the user_id for the specific app_id
    # app_session_mapping = user_app_session_mapping.get(input.user_id, {})
    # session_id = app_session_mapping.get(public_id)
    # print(session_memory)
    # if session_id:
    #     # print(session_id)
    #     removed_session = session_memory.pop(session_id, None)
    #     if removed_session:
    #         # print(removed_session)
    #         if input.resume_old_session:
    #             session = removed_session
    #             print(input.resume_old_session)
        # print("No removed")
    # print(session, "\n_________________\n")
    # print(session_memory)
    if session.id not in session_memory:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.expiration is not None and session.expiration < datetime.utcnow():
        session_memory.pop(session.id)
        raise HTTPException(status_code=404, detail="Session expired")
    # print("HOOO")
    # raise HTTPException(status_code=404, detail=f"{session.app_id}, {public_id}")
    return session_memory.get(session.id)


# ... (OAuth2 and dependencies remain the same)

# Dependency to initialize or retrieve a session
def initialize_or_get_session(
    input: USSDSessionInput,
    session: Optional[USSDSession] = Depends(get_session_from_memory),
    
) -> USSDSession:
    return session
# @router.post("/init-session/{app_id}", response_model=USSDSession)


async def get_ussd_app_and_session(
    input: USSDSessionInput,
    public_id: str = Path(..., title="The USSD code or identifier for the app."),
    ussd_app: USSDApp = Depends(get_app_by_public_id),
    session: USSDSession = Depends(initialize_session),
):
    return ussd_app, session
@router.post("/ussd-entry/{public_id}")
async def ussd_entry_point(
    input: USSDSessionInput,
    public_id: str = Path(..., title="The USSD code or identifier for the app."),
    secret: Optional[str] = None,
    app_and_session: tuple[USSDApp, USSDSession] = Depends(get_ussd_app_and_session),
    db: Session = Depends(get_db)
):
    ussd_app, session = app_and_session
    # Ensure the session belongs to the specified USSD app
    
    if session.app_id != public_id:
        raise HTTPException(status_code=403, detail=f"Session {session.app_id} does not belong to this app")
    
    # Ensure the app has a initial_state defined
    if ussd_app.initial_state_id is None:
        raise HTTPException(status_code=400, detail="The app does not have a version ready for production.")

    # If the session's current_state is None, set it to the initial_state of the USSDApp
    # if session.current_state is None and input.resume_old_session == False:
    print(input.user_input)
    if session.current_state is None or input.user_input=='start':
        session.current_state = get_state(ussd_app.initial_state_id, db)
        save_session(session)
        options = session.current_state.options
        template_data = {"message": session.current_state.message, "options": options}
        response_template = session.current_state.response_template or "default_response_template.txt"

        # try:
        # print(response_template)
        response_html = templates.TemplateResponse(response_template, {"request": None, "data": template_data})
        # print(response_html)
        session.output = response_html.body
        return session

    # Retrieve the current state based on the session's current_state
    current_state: USSDState = session.current_state

    # Retrieve the main menu options
    # main_menu_options = get_state(ussd_app.initial_state_id).options
    options = current_state.options
    # If it is the initial state, display the message and options using a Jinja template
    # Done
    # if current_state.id == ussd_app.initial_state_id:
        
        # raise HTTPException(status_code=400, detail="Invalid input")
        # Retrieve the main menu options
        # main_menu_options = get_state(ussd_app.initial_state).options
        # save_session(session)

        # # Implement logic based on the next state, options, etc.
        # response_message = generate_response_message(next_state, ussd_app)
        # Use the response template if available, otherwise use a default template
        # template_data = {"message": current_state.message, "options": options}
        # response_template = current_state.response_template or "default_response_template.txt"

        # # try:
        # # print(response_template)
        # response_html = templates.TemplateResponse(response_template, {"request": None, "data": template_data})
        # # print(response_html)
        # session.output = response_html.body
        # return session
        
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=f"Error rendering template: {str(e)}")
    # Determine the next state based on user input or the default next state
    # Commence a partir d'ici. La fonction get_next_state est déjà définie mais pas terminée
    next_state = get_next_state(input.user_input, current_state, options, db)

    # Update the session's current_state
    session.current_state = next_state
    print(session.current_state)
    
    options = session.current_state.options
    # # Implement logic based on the next state, options, etc.
    # response_message = generate_response_message(next_state, ussd_app)
    # Use the response template if available, otherwise use a default template
    template_data = {"message": session.current_state.message, "options": options}
    response_template = session.current_state.response_template or "default_response_template.txt"

    # try:
    print(response_template)
    response_html = templates.TemplateResponse(response_template, {"request": None, "data": template_data})
    print(response_html.body)
    session.output = response_html.body
    save_session(session)
    return session
    # return {"message": response_message}

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
def get_next_state(user_input: str, current_state: USSDState, main_menu_options: List[USSDOption], db: Session) -> USSDState:
    # Utilisez filter pour trouver l'option correspondante
    matching_options: List[USSDOption] = list(filter(lambda option: option.option_value == user_input, current_state.options))
    # raise Exception(status_code=514, detail="Not implemented")
    if matching_options:
        # Récupérez l'id de la première option correspondante
        matched_option = matching_options[0]
        matched_option_id = matched_option.id

        # Récupérez l'option correspondante à partir de la base de données (ou autre source)
        
        print(matched_option)
        # Mise à jour du state actuel
        current_state = get_state(matched_option.next_state_id, db)
        print(current_state)
    else:
        # Logique à traiter lorsque user_input ne correspond à aucune option
        # Soulevez une exception HTTP
        raise HTTPException(status_code=400, detail="Invalid input")
    
    return current_state