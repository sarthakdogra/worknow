from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.worker import Worker
from models.user import User
from schemas.worker import WorkerCreate, WorkerUpdate


class WorkerService:

    @staticmethod
    def create_worker_profile(
        db: Session,
        current_user: User,
        worker_data: WorkerCreate,
    ):

        existing_profile = (
            db.query(Worker)
            .filter(Worker.user_id == current_user.id)
            .first()
        )

        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Worker profile already exists."
            )

        worker = Worker(
            user_id=current_user.id,
            bio=worker_data.bio,
            experience_summary=worker_data.experience_summary,
            location_city=worker_data.location_city,
            location_state=worker_data.location_state,
        )

        db.add(worker)
        db.commit()
        db.refresh(worker)

        return worker

    @staticmethod
    def get_worker_profile(
        db: Session,
        current_user: User,
    ):

        worker = (
            db.query(Worker)
            .filter(Worker.user_id == current_user.id)
            .first()
        )

        if not worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker profile not found."
            )

        return worker

    @staticmethod
    def update_worker_profile(
        db: Session,
        current_user: User,
        worker_data: WorkerUpdate,
    ):

        worker = (
            db.query(Worker)
            .filter(Worker.user_id == current_user.id)
            .first()
        )

        if not worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker profile not found."
            )

        update_data = worker_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(worker, key, value)

        db.commit()
        db.refresh(worker)

        return worker

    @staticmethod
    def delete_worker_profile(
        db: Session,
        current_user: User,
    ):

        worker = (
            db.query(Worker)
            .filter(Worker.user_id == current_user.id)
            .first()
        )

        if not worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker profile not found."
            )

        db.delete(worker)
        db.commit()

        return {
            "message": "Worker profile deleted successfully."
        }