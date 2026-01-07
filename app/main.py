from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db, engine
from app import models, schemas
from app.github_client import fetch_repo_details

from sqlalchemy.exc import SQLAlchemyError
import httpx
from app.exceptions import (
    sqlalchemy_exception_handler,
    httpx_exception_handler,
    generic_exception_handler,
)

app = FastAPI(title="GitHub Repository Tracker API")
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(httpx.RequestError, httpx_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Create tables
models.Base.metadata.create_all(bind=engine)
@app.get("/health")
def health_check():
    return {"status": "ok"}


# POST: Create repository (GitHub API call)
@app.post(
    "/repositories",
    response_model=schemas.RepositoryResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_repository(
    repo: schemas.RepositoryCreate,
    db: Session = Depends(get_db)
):
    github_data = await fetch_repo_details(repo.owner, repo.repo_name)

    if not github_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found on GitHub"
        )

    db_repo = models.Repository(
        owner=repo.owner,
        repo_name=repo.repo_name,
        stars=github_data["stars"],
        language=github_data["language"],
        description=github_data["description"],
    )

    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)

    return db_repo


# GET: Fetch repository by ID
@app.get(
    "/repositories/{repo_id}",
    response_model=schemas.RepositoryResponse
)
def get_repository(repo_id: int, db: Session = Depends(get_db)):
    repo = db.query(models.Repository).filter(models.Repository.id == repo_id).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    return repo


# PUT: Update repository
@app.put(
    "/repositories/{repo_id}",
    response_model=schemas.RepositoryResponse
)
def update_repository(
    repo_id: int,
    repo_update: schemas.RepositoryUpdate,
    db: Session = Depends(get_db)
):
    repo = db.query(models.Repository).filter(models.Repository.id == repo_id).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    for field, value in repo_update.dict(exclude_unset=True).items():
        setattr(repo, field, value)

    db.commit()
    db.refresh(repo)

    return repo


# DELETE: Delete repository
@app.delete(
    "/repositories/{repo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_repository(repo_id: int, db: Session = Depends(get_db)):
    repo = db.query(models.Repository).filter(models.Repository.id == repo_id).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    db.delete(repo)
    db.commit()

    return None
