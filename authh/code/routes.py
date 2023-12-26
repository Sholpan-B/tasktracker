import fastapi as fa
import schemas
from repo import UserRepo

router = fa.APIRouter(prefix='/api', tags=['user'])
repo = UserRepo


@router.get('/users')
async def get_users(params: schemas.UserAllOptionalSchema = fa.Depends()):
    return await repo.get_list(params.model_dump(exclude_none=True))


@router.get('/users/{id}')
async def get_user_by_id(id: int):
    return await repo.get(id=id)

