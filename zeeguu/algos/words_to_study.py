from zeeguu.model import Bookmark, BookmarkPriorityARTS


def bookmarks_to_study(user, desired_bookmarks_count=-1):
    bookmarks = Bookmark.query. \
        filter_by(user_id=user.id). \
        join(BookmarkPriorityARTS). \
        filter(BookmarkPriorityARTS.bookmark_id == Bookmark.id). \
        order_by(BookmarkPriorityARTS.priority.desc()). \
        limit(desired_bookmarks_count)\
        .all()

    # TODO: Filter by Bookmark.already_seen_today()
    return bookmarks
