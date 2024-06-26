from uuid import UUID
from flask import jsonify
from datetime import datetime
from http import HTTPStatus as responseStatus

from . import api
from app import db
from app.models import User
from app.utils.api_utils import error_message
from app.utils.decorators import api_login_required


@api.route("/admin/<user_id>", methods=["PUT"])
@api_login_required
def update_to_admin(user_id):
    """
    Update a user to admin.
    Args:
    user_id: The user ID.
    Returns:
    A JSON object containing successful message, the user Id and an http status code.
    """
    try:
        user = User.query.get(UUID(user_id))

        if user is None:
            return error_message("User not found", responseStatus.NOT_FOUND)

        user.is_admin = True
        user.updated_at = datetime.now()

        db.session.commit()

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "User updated to admin successfully",
                    "user_id": user.id,
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        db.session.rollback()
        print(e)
        return error_message(
            "Internal server error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/admin/<user_id>/cancel-admin", methods=["PUT"])
@api_login_required
def cancel_admin(user_id):
    """
    Cancel a user's admin role to normal user.
    Args:
    user_id: The user ID.
    Returns:
    A JSON object containing successful message, the user id and an http status code.
    """

    try:
        user = User.query.get(UUID(user_id))

        if user is None:
            return error_message("User not found", responseStatus.NOT_FOUND)

        user.is_admin = False
        user.updated_at = datetime.now()

        db.session.commit()

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "User admin role cancelled successfully",
                    "user_id": user.id,
                }
            ),
            responseStatus.OK,
        )
    except Exception as e:
        db.session.rollback()
        print(e)
        return error_message(
            "Internal server error", responseStatus.INTERNAL_SERVER_ERROR
        )
