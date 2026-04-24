from  fastapi import APIRouter, HTTPException,Depends,status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import UserProfile,RefreshToken
from db.schema import RegisterSchema,LoginSchema
from passlib.context import CryptContext
from datetime import timezone,timedelta,datetime
from config import ACCESS_EXPIRE_TOKEN,REFRESH_EXPIRE_TOKEN,SECRET_KEY,ALGORITHM
from jose import jwt


auth_router = APIRouter(prefix="/auth",tags=["authorization"])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

hash_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password):
    return hash_context.hash(password)

def verify_password(password,hash_password):
    return hash_context.verify(password,hash_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=(ACCESS_EXPIRE_TOKEN))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    return create_access_token(data=data,expires_delta=timedelta(days=REFRESH_EXPIRE_TOKEN))

@auth_router.post("/register",response_model=dict)
async def register(register_data:RegisterSchema ,db:Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == register_data.username).first()
    if user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exists")
    hashed_password = hash_password(register_data.password)
    register_db = UserProfile(
        first_name = register_data.first_name,
        last_name = register_data.last_name,
        username = register_data.username,
        age = register_data.age,
        profile_image = register_data.profile_image,
        password = hashed_password
    )
    db.add(register_db)
    db.commit()
    db.refresh(register_db)
    return {'status':'Успешно прошла регистрация'}

@auth_router.post("/login",response_model=dict)
async def login(login_data:LoginSchema ,db:Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == login_data.username).first()
    if not user_db or not verify_password(login_data.password, user_db.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Username or password is incorrect")
    access_token = create_access_token(data=({'sub': user_db.username}))
    refresh_token = create_access_token(data=({'sub': user_db.username}))
    refresh_db = RefreshToken(user_id=user_db.id, token=refresh_token)
    db.add(refresh_db)
    db.commit()
    db.refresh(refresh_db)

    return {
        'user':user_db.username,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'type': 'Bearer'
    }

@auth_router.post('/generate_refresh_token', response_model = dict)
async def generate_token(refreshToken:str, db: Session = Depends(get_db)):
    refresh_db = db.query(RefreshToken).filter(RefreshToken.token == refreshToken).first()
    if not refresh_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Token not found")
    access_token = create_access_token({'sub': refresh_db.user_id})
    return {
        'access_token': access_token,
        'type': 'Bearer'
    }

@auth_router.post('/logout',response_model=dict)
async def logout(refresh_token:str, db: Session = Depends(get_db)):
    refresh_db = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not refresh_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Token not found")
    db.delete(refresh_db)
    db.commit()
    return {'status': 'Success logout'}
