from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..import schema, models, utils, oauth

router = APIRouter(
    tags=['authentication']
)


@router.post('/login', response_model=schema.Token)
def login(user_creditional: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_creditional.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_NOT_FOUND, detail=f'Invaild Credentials')

    if not utils.verify(user_creditional.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_NOT_FOUND, detail=f'Invaild Credentials')

    access_token = oauth.create_access_token(data={"user_id": f"{user.id}"})

    return {'access_token': access_token, 'type': 'bearer'}
