import fastapi
from api.task.routes import router as task_router
from adapters import MinIOClient
from starlette import status


router = fastapi.APIRouter(prefix='/api')

router.include_router(task_router)


@router.get('/greetings')
def get_greetings():
    return {'text': 'Greetings!'}


@router.post('/upload')
async def upload_file(file: fastapi.UploadFile = fastapi.File(...)):
    client = MinIOClient()
    await client.upload_from_bytes(file)

    return fastapi.Response(status_code=status.HTTP_204_NO_CONTENT)



