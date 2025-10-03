from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..database import database
from ..models import User  # SQLAlchemy User model
from ..Schemas import user as user_schema
from ..hashing import Hash
from .. import JWTtoken

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# ✅ Register new user
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: user_schema.register_user, db: AsyncSession = Depends(database.get_db)):
    # Check if user already exists
    result = await db.execute(
        select(User.User).filter(User.User.email == request.email)
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password correctly
    password_hash = Hash.bcrypt(request.password)

    # Create new user object
    new_user = User.User(
        username=request.username,
        email=request.email,
        password_hash=password_hash,  # store hashed password
        WABAID=request.WABAID,
        PAccessToken=request.PAccessToken,
        Phone_id=request.Phone_id,
        api_key=request.cf_token
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "User registered successfully", "email": new_user.email}

# ✅ Login user
@router.post("/login")
async def login(request: user_schema.LoginUser, db: AsyncSession = Depends(database.get_db)):
    # Find user by username
    result = await db.execute(select(User.User).filter(User.User.username == request.username))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid username")

    # Verify hashed password
    if not Hash.verify(request.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid password")

    # Generate JWT token
    access_token = JWTtoken.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
