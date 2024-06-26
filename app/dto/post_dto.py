from typing import List, Dict, Union
from app.utils.helper import getTimeAgo
from app.models import Post, User, Comment, CommentStatus
from .comment_dto import CommentDTO

# isPreview
# a post with maximum 3 comments, and each comment with maximum 3 replies
# maximum comment level is 2


class PostDTO:
    def __init__(
        self, post: Post, postCreator: User, user: User, isPreview: bool = False
    ):
        if not any([post, postCreator, user]):
            raise ValueError("post, postCreator and user are required")

        self.id = post.id if post else None
        self.title = post.title if post else None
        self.content = post.content if post else None
        self.image_url = post.image_url if post else None
        self.tags = [(tag.name, tag.color) for tag in post.tags] or []
        self.postStatus = post.status.value if post else None
        self.timeAgo = getTimeAgo(post.updated_at) if post else None
        self.postCreator = PostDTO._get_user(postCreator)
        self.isCreator = True if postCreator.id == user.id else False
        self.userInteraction = self._get_user_on_post_interaction(post, user)
        self.isPreview = isPreview
        self.comments = self._get_comments(
            post.comments, isPreview=isPreview, user=user
        )

    @staticmethod
    def _get_user(user: User) -> Dict[str, Union[int, str, bool]]:
        return {
            "id": user.id,
            "username": user.username,
            "anon_no": user.anon_no,
            "avatar_url": user.avatar_url,
            "campus": user.campus.value,
            "is_admin": user.is_admin,
        }

    @staticmethod
    def _get_user_on_post_interaction(
        post: Post, user: User
    ) -> Dict[str, Union[int, bool]]:
        return {
            "likes": len(post.liked_by),
            "comments": len(post.comments),
            "isLikedByUser": user in post.liked_by,
            "isBookmarkedByUser": user in post.bookmarked_by,
            "isCommentedByUser": any(
                [
                    comment
                    for comment in post.comments
                    if comment.commentCreator == user
                    and comment.status != CommentStatus.REPORTED
                ]
            ),
        }

    @staticmethod
    def _get_comments(
        comments: List[Comment], isPreview: bool, user: User
    ) -> List[Dict[str, Union[int, str, bool, List]]]:

        newComments = []

        sortedComments = sorted(
            comments, key=lambda comment: comment.created_at, reverse=False
        )

        for comment in sortedComments:

            # stop the loop if the post is a preview and the number of comments is 3
            if isPreview and len(newComments) >= 3:
                break

            elif comment:
                # if the comment is a reply on the first comment level, skip it
                if comment.replied_comment:
                    continue

            commentDTO = CommentDTO(comment=comment, user=user, commentLevel=1)

            commentDTO.get_replies(maxCommentLevel=10000, isPreview=isPreview)

            newComments.append(commentDTO.to_dict())

        return newComments

    @staticmethod
    def _get_user_on_comment_interaction(comment: Comment) -> Dict[str, int]:
        return {"likes": len(comment.liked_by), "replies": len(comment.replies)}

    def to_dict(self) -> Dict[str, Union[int, str, bool, List]]:
        data = {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "image_url": self.image_url,
            "tags": self.tags,
            "postStatus": self.postStatus,
            "timeAgo": self.timeAgo,
            "postCreator": self.postCreator,
            "isCreator": self.isCreator,
            "userInteraction": self.userInteraction,
            "isPreview": self.isPreview,
            "comments": self.comments,
        }

        return data
