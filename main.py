from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from supabase import create_client
import os
# app/main.py
from fastapi import FastAPI
from app.db.engine import create_db_and_tables
from app.routers import option as ussd_option
from app.routers import form as ussd_form
from app.routers import ussd_app
from app.routers import field as ussd_field
from app.routers import api_action as ussd_api_action
from app.routers import state as ussd_state
# from app.routers import session
import uvicorn
from pyngrok import ngrok  # Import Pyngrok
from fastapi.middleware.cors import CORSMiddleware

# Specify the path to the templates directory
templates = Jinja2Templates(directory="app/templates")
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ussd_option.router, prefix="/ussd", tags=["ussd_option"])
app.include_router(ussd_form.router, prefix="/ussd", tags=["ussd_form"])
app.include_router(ussd_app.router, prefix="/ussd", tags=["ussd_app"])
app.include_router(ussd_field.router, prefix="/ussd", tags=["ussd_field"])
app.include_router(ussd_api_action.router, prefix="/ussd", tags=["ussd_api_action"])
app.include_router(ussd_state.router, prefix="/ussd", tags=["ussd_state"])
# app.include_router(session.router, prefix="/session", tags=["ussd_session"])


# CORS middleware to allow all origins during development

# Load environment variables from .env
load_dotenv()

# Retrieve Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Start ngrok when the app is run
def start_ngrok():
    public_url = ngrok.connect(8000)
    print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}/\"".format(public_url, 8000))

# Start ngrok when the app is run
if 'NGROK_ENV' in os.environ:
    print(" * Running on public address")
    print(" * Public URL: {}".format(os.environ['NGROK_PUBLIC_URL']))
else:
    print(" * Running on localhost")
    start_ngrok()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)