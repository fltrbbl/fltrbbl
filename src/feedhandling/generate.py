from .fetch import Feed




def generate_feed_atom(feed: Feed):
    for entry in feed.items():
        feed.add_item(entry)
    return feed.to_string()
