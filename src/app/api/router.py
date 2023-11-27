from fastapi import APIRouter
from api.task.routes import router as task_router

router = APIRouter(prefix='/api')

router.include_router(task_router)


@router.get('/greetings')
def get_greetings():
    return {'text': 'Greetings!'}
