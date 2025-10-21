from dotenv import load_dotenv
load_dotenv()   # 👈 Load environment FIRST
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import router as app_router

app = FastAPI(title="Admin APIs with Supabase")

# ✅ Enable CORS (important for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production: use your real frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include all your route modules
app.include_router(router = app_router)

# ✅ Root test endpoint
@app.get("/")
def root():
    return {"message": "FastAPI + Supabase backend running with CORS enabled!"}
