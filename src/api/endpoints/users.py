from fastapi import APIRouter, Depends, Response, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from typing import List, Union
from pymongo.database import Database
from db import get_db
from models.user import (
    BaseUserOut,
    UserOut,
    CreateUserIn,
    UserInDB,
    UpdateUserIn,
    UserMinimalMetadataOut,
    CheckFavoritePlant,
)
from core.security import (
    get_password_hash,
    get_current_active_user,
    get_current_active_superuser,
    get_current_user_if_exists,
)
from endpoints.helpers_tools.common_dependencies import QuerySearchPageParams
from endpoints.helpers_tools.user_dependencies import (
    validate_accept_terms_of_service,
    validate_username_and_email_not_in_db,
    validate_current_user_edit_itself,
    validate_match_passwords__new_user,
    get_existing_user,
    get_user_from_email_registration_token,
)
from models.exceptions import (
    ExceptionUserNotPrivilege,
    ExceptionUserNotAuthenticated,
    ExceptionUserNotFound,
    ExceptionUserNotAllowToEditThisUser,
    ExceptionUserNotAcceptTermsOfService,
    ExceptionUserOrEmailAlreadyExists,
    ExceptionPasswordNotMatch,
    DetailUserNotFound,
    ExceptionEmailVerificationTokenNotFound,
)
from endpoints.helpers_tools.email import setup_email_verification
from models.user_observations import ObservationPreviewBase
from models.user_questions import QuestionPreviewBase
from endpoints.helpers_tools.generic import format_obj_image_preview

router = APIRouter()


@router.get(
    "/",
    response_model=List[UserInDB],
    dependencies=[Depends(get_current_active_superuser)],
    summary="Get all users",
    description="Get all users. Only superusers can do this.",
    responses={
        401: {
            "description": ExceptionUserNotAuthenticated().detail,
            "model": ExceptionUserNotAuthenticated,
        },
        403: {
            "description": ExceptionUserNotPrivilege().detail,
            "model": ExceptionUserNotPrivilege,
        },
    },
)
async def read_users(
    db: Database = Depends(get_db),
    search_params: QuerySearchPageParams = Depends(QuerySearchPageParams),
) -> List[UserInDB]:
    return list(db.users.find({}).skip(search_params.skip).limit(search_params.limit))


@router.get(
    "/me",
    response_class=RedirectResponse,
    summary="Get current user",
    description="Redirect to user profile",
    responses={
        401: {
            "description": ExceptionUserNotAuthenticated().detail,
            "model": ExceptionUserNotAuthenticated,
        }
    },
)
async def read_current_user(
    current_user: BaseUserOut = Depends(get_current_active_user),
) -> RedirectResponse:
    return current_user.username


@router.get(
    "/{username}",
    response_model=UserOut,
    summary="User page",
    description="Get user basic data with list of observations and questions",
    responses={
        404: {
            "description": DetailUserNotFound().detail,
            "model": DetailUserNotFound,
        },
    },
)
async def read_user(
    requested_user: UserInDB = Depends(get_existing_user),
    current_user: UserMinimalMetadataOut = Depends(get_current_user_if_exists),
    db: Database = Depends(get_db),
) -> UserOut:
    """
    exclude email and phone if the requested user is not the current user.
    """
    # TODO: Refactor this in the future when needed

    # * set requested user object
    requested_user = UserOut(**requested_user.dict())

    # * get user observations (all of them)
    observations = list(
        db.observations.find(
            {"user_id": requested_user.user_id, "submitted": True, "deleted": False}
        ).sort("create_dt", -1)
    )
    observations = list(map(format_obj_image_preview, observations))
    requested_user.observations = [ObservationPreviewBase(**x) for x in observations]

    # * get user questions (all of them)
    questions = list(
        db.questions.find(
            {"user_id": requested_user.user_id, "submitted": True, "deleted": False}
        ).sort("create_dt", -1)
    )
    questions = list(map(format_obj_image_preview, questions))
    requested_user.questions = [QuestionPreviewBase(**x) for x in questions]

    # TODO: add list of detection user (not developed yet)

    if requested_user.username == current_user.username or current_user.is_superuser:
        # * When requested user is the current user or current user is a superuser
        return requested_user
    # * When requested user is not the current user or current user is not a superuser
    return requested_user.dict(exclude={"email", "phone"})


@router.put(
    "/{username}",
    status_code=204,
    summary="Update current user",
    description="Update current user with shown fields",
    dependencies=[Depends(validate_current_user_edit_itself)],
    responses={
        400: {
            "description": ExceptionUserNotAllowToEditThisUser().detail,
            "model": ExceptionUserNotAllowToEditThisUser,
        },
        401: {
            "description": ExceptionUserNotAuthenticated().detail,
            "model": ExceptionUserNotAuthenticated,
        },
        404: {
            "description": ExceptionUserNotFound().detail,
            "model": ExceptionUserNotFound,
        },
    },
)
async def update_user(
    username: str,
    user_in: UpdateUserIn,
    db: Database = Depends(get_db),
):
    db.users.update_one(
        {"username": username},
        {"$set": user_in.dict(exclude_none=True, exclude_unset=True)},
    )
    return Response(status_code=204)


@router.post(
    "/",
    status_code=201,
    dependencies=[
        Depends(validate_accept_terms_of_service),
        Depends(validate_username_and_email_not_in_db),
        Depends(validate_match_passwords__new_user),
    ],
    summary="Create new user",
    description="After registration, user must verify email",
    responses={
        400: {
            "description": "Input Validation",
            "model": Union[
                ExceptionUserNotAcceptTermsOfService,
                ExceptionUserOrEmailAlreadyExists,
                ExceptionPasswordNotMatch,
            ],
        },
    },
)
async def create_user(
    user_in: CreateUserIn,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Database = Depends(get_db),
):
    # * hash the password
    hash_password = get_password_hash(user_in.password.get_secret_value())

    # * setup userInDB with hash password
    userInDB = UserInDB(**user_in.dict(exclude={"password"}), password=hash_password)

    # * email verification
    background_tasks.add_task(
        setup_email_verification,
        userInDB.user_id,
        userInDB.email,
        request.base_url,
    )

    # * insert user
    db.users.insert_one(userInDB.dict())

    return Response(status_code=201)


@router.get(
    "/verify-email/{token}",
    status_code=204,
    summary="Verify email",
    description="Verify email with email verification token",
    responses={
        404: {
            "description": ExceptionEmailVerificationTokenNotFound().detail,
            "model": ExceptionEmailVerificationTokenNotFound,
        },
    },
)
async def verify_email(
    user_id: str = Depends(get_user_from_email_registration_token),
    db: Database = Depends(get_db),
):
    db.users.update_one(
        {"user_id": user_id},
        {"$set": {"email_verified": True, "is_active": True}},
    )
    return Response(status_code=204)


@router.get(
    "/me/favorite-plant/{science_name}",
    response_model=CheckFavoritePlant,
    summary="Check favorite plant",
    description="Check if current user the requested plant is in favorite list",
)
async def check_favorite_plant(
    science_name: str,
    current_user: UserInDB = Depends(get_current_active_user),
) -> CheckFavoritePlant:
    is_favorite = any(
        favorite_plant.science_name == science_name
        for favorite_plant in current_user.favorite_plants
    )
    return CheckFavoritePlant(is_favorite=is_favorite)
