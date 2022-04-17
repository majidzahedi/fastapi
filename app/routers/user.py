from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema
from ..database import get_db
from ..utils import hash

router = APIRouter(
    prefix='/user',
    tags=['users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    user.password = hash(user.password)
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as error:
        return {'error': error}

    return new_user


@router.get('/{id}', response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            detail=f'user with {id} not found', status_code=status.HTTP_404_NOT_FOUND)

    return user
