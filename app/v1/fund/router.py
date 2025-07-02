from exceptions import FundNotFoundException
from fastapi import APIRouter, Depends
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from v1.dependencies.auth_dep import get_current_user
from v1.dependencies.dao_dep import get_session_with_commit
from v1.fund.schemas import FundDetailAPISchema
from v1.users.dao import FundDAO

v1_funds_router = APIRouter()


@v1_funds_router.get("/detail/{fund_id}", response_model=FundDetailAPISchema)
async def get_fund_detail_by_id(
    fund_id: int,
    user_data: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit),
) -> FundDetailAPISchema:
    fund = await FundDAO(session=session).find_one_or_none_by_id(data_id=fund_id)

    if fund is not None:
        return FundDetailAPISchema.model_validate(fund)

    else:
        raise FundNotFoundException
