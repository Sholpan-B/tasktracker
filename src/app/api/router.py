from fastapi import APIRouter


router = APIRouter(prefix='/api')
task_router = APIRouter(prefix='/task')
router.include_router(task_router)


@router.get('/greetings')
def get_greetings():
    return {'text': 'Greetings!'}
