import uuid
from sqlalchemy.dialects.postgresql import UUID

from app import db


class CommentNotification(db.Model):
    __tablename__ = "CommentNotification"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("User.id"))
    comment_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Comment.id"))
    unread_comment_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Comment.id"))

    # relationship

    def __init__(self, comment_notification_dist, *args, **kwargs):
        self.created_at = comment_notification_dist.get("created_at")

    def __repr__(self):
        return f"<{self.id} - {self.is_read}>"