from typing import Dict

from app.models import Post, PostStatus, User


def get_user_agg_interaction(user: User) -> Dict[str, int]:
    """
    Get user aggregated interaction data, including the number of the created posts, liked posts, commented posts and reply to comment, as well as bookmarked posts.
    Args:
        user (User): The user who is currently logged in.
    Returns:
        Dict[str, int]: A dictionary of user aggregated interaction data.
    """

    if not user:
        return {}

    created_posts = Post.query.filter(
        Post.user_id == user.id,
        Post.status.in_([PostStatus.APPROVED, PostStatus.UNREAD_APPROVED]),
        Post.is_delete == False,
    ).count()

    liked_posts = 0

    for post in user.liked_posts:
        if (
            post.status in [PostStatus.APPROVED, PostStatus.UNREAD_APPROVED]
            and not post.is_delete
        ):
            liked_posts += 1

    all_commented_posts = set()

    for comment in user.comments:
        if (
            comment.commented_post.status
            in [PostStatus.APPROVED, PostStatus.UNREAD_APPROVED]
            and not comment.commented_post.is_delete
        ):
            all_commented_posts.add(comment.commented_post)

    bookmarked_posts = 0
    for post in user.bookmarked_posts:
        if (
            post.status in [PostStatus.APPROVED, PostStatus.UNREAD_APPROVED]
            and not post.is_delete
        ):
            bookmarked_posts += 1

    rejected_posts = Post.query.filter(
        Post.user_id == user.id,
        Post.status.in_([PostStatus.REJECTED, PostStatus.UNREAD_REJECTED]),
        Post.is_delete == False,
    ).count()

    return {
        "createdPosts": created_posts,
        "likedPosts": liked_posts,
        "commentsAndReplies": len(all_commented_posts),
        "bookmarkedPosts": bookmarked_posts,
        "rejectedPosts": rejected_posts,
    }
