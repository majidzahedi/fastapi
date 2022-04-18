from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from .. import schema, database, models, oauth

router = APIRouter(
    prefix='/vote',
    tags=['vote']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='post not founded!')

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail='already voted!')

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'done!'}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='not voted yet!')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'done!'}
