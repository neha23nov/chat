from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .routes import message_generator

from .database import database
from .models import ChatBox
from .routes import user, broadcast, contacts, auth, woocommerce, integration, wallet, analytics
from .services import dramatiq_router
from .import oauth2
from .routes.message_generator import router as message_router
from .routes import message_generator




# -----------------------------
# Initialize app and scheduler
# -----------------------------
app = FastAPI()
scheduler = AsyncIOScheduler()
scheduler_started = False

# -----------------------------
# CORS Configuration
# -----------------------------
origins = [
    "http://localhost:8080",  # Vue frontend
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Change to ["*"] for testing only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Database Initialization
# -----------------------------
async def create_db_and_tables():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)

# -----------------------------
# Startup Event
# -----------------------------
@app.on_event("startup")
async def startup_event():
    # Create DB tables
    await create_db_and_tables()
    
    # Start scheduler
    global scheduler_started
    if not scheduler_started:
        scheduler.add_job(close_expired_chats, 'interval', minutes=1)
        scheduler.start()
        scheduler_started = True
        print("Scheduler started.")

# -----------------------------
# Shutdown Event
# -----------------------------
@app.on_event("shutdown")
async def shutdown_event():
    global scheduler_started
    if scheduler_started:
        scheduler.shutdown(wait=False)
        scheduler_started = False
        print("Scheduler shut down.")



# -----------------------------
# Include Routers
# -----------------------------
app.include_router(auth.router)        # ✅ /auth prefix
app.include_router(user.router)
app.include_router(broadcast.router)
app.include_router(contacts.router)
app.include_router(wallet.router)
app.include_router(oauth2.router)
app.include_router(dramatiq_router.router)
app.include_router(woocommerce.router)
app.include_router(integration.router)
app.include_router(analytics.router)

app.include_router(message_generator.router, prefix="/message")


# -----------------------------
# Scheduler Job Function
# -----------------------------
async def close_expired_chats() -> None:
    """Close chats that have been inactive for more than 24 hours."""
    try:
        async for session in database.get_db():  # async generator
            now = datetime.now()
            result = await session.execute(
                select(ChatBox.Last_Conversation).where(
                    ChatBox.Last_Conversation.active == True,
                    now - ChatBox.Last_Conversation.last_chat_time > timedelta(minutes=1440)
                )
            )
            expired_conversations = result.scalars().all()

            for conversation in expired_conversations:
                conversation.active = False

            await session.commit()
            print(f"Successfully closed {len(expired_conversations)} expired chats.")
            break  # only need first session
    except Exception as e:
        print(f"Error in close_expired_chats: {e}")
