#!/usr/bin/env python

"""

   Script that goes through all the feeds that are
   available in the DB and retrieves the newest articles
   in order to populate the DB with them.

   The DB is populated by saving Article objects in the
   articles table.

   Before this script checking whether there were new items
   in a given feed was done while serving the request for
   items to read. That was too slow.

   To be called from a cron job.

"""

import zeeguu
from zeeguu.content_recommender.mixed_recommender import reading_preferences_hash, recompute_recommender_cache
from zeeguu.model import User, ArticlesCache

session = zeeguu.db.session


def hashes_of_existing_cached_preferences():
    """

        goes through the ArticleCache table and gets
        the distinct content_hashes

    :return:
    """
    query = session.query(ArticlesCache.content_hash.distinct())
    distinct_hashes = [each[0] for each in query.all()]
    return distinct_hashes


def clean_the_cache():
    ArticlesCache.query.delete()
    session.commit()


def recompute_for_users(existing_hashes):
    """

        recomputes only those caches that are already in the table
        and belong to a user.

        in theory, the recomputing should be doable independent of users
        in practice, the recompute_recommender_cache takes the user as input.
        for that function to become independent of the user we need to be
        able to recover the ids of the languages, topics, searchers, etc. from the
        content_hash
        to do this their ids would need to be comma separated

    :param existing_hashes:
    :return:
    """
    for user in User.query.all():
        try:
            reading_pref_hash = reading_preferences_hash(user)
            if reading_pref_hash in existing_hashes:
                ArticlesCache.query.filter_by(content_hash=reading_pref_hash).delete()
                recompute_recommender_cache(reading_pref_hash, session, user)
                print(f"Success for {user}")
        except Exception as e:
            print(f"Failed for user {user}")


existing_hashes = hashes_of_existing_cached_preferences()
clean_the_cache()
recompute_for_users(existing_hashes)
