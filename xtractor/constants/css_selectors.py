# Locate the link to view analytics for a post/tweet
VIEWS_CSS_SELECTOR = 'a[href$="/analytics"]'

# Locate a specific metric element in post/tweet metrics
METRICS_CSS_SELECTOR = 'div[data-testid="{metric}"]' 

# Locate the text content of a post/tweet
TEXT_CSS_SELECTOR = 'div[data-testid="tweetText"]'

# Locate links to tweets by a specific user
HREF_CSS_SELECTOR = 'a[href^="/{username}/status/"]'

# Locate the timestamp of a post/tweet
DATE_CSS_SELECTOR = "time"

# Locate the username of a post/tweet author
USERNAME_CSS_SELECTOR = 'div[data-testid="User-Name"]'

# Locate the repost context of a post/tweet (e.g., "retweeted by")
REPOST_CSS_SELECTOR = 'span[data-testid="socialContext"]'

# Locate images attached to a post/tweet
MEDIA_CSS_SELECTOR = 'img[alt="Image"]' 

# Locate videos attached to a post/tweet
VIDEO_CSS_SELECTOR = 'div[data-testid="videoComponent"]'

# Locate the "Show more" link in expanded post/tweet text
SHOW_MORE_CSS_SELECTOR = 'span[data-testid="tweet-text-show-more-link"]' 
