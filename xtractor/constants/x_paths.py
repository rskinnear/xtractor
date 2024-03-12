# XPATH used to locate any post or element within the main feed
POST_XPATH = '//div[@data-testid]//article[@data-testid="tweet"]'

# XPATH used to locate the number of views on a post
VIEWS_XPATH = './/div[@class="css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0"]'

# XPATH used to identify specific metric/impression elements by injecting the metric type into the placeholder {metric}
METRICS_XPATH = '//div[@data-testid="{metric}"]'

# XPATH used to locate the main feed, usually the column where the tweets or posts are displayed
FEED_XPATH = '//div[@data-testid="primaryColumn"]'

# XPATH used to locate the link to the followers list for a specific user, {username} placeholder to be replaced dynamically
FOLLOWERS_XPATH = '//a[@href="/{username}/verified_followers"]'

# XPATH used to locate the link to the profiles a specific user is following
FOLLOWING_XPATH = '//a[@href="/{username}/following"]'

# XPATH used to locate the link to the user's subscribers
SUBSCRIPTIONS_XPATH = '//a[@href="/{username}/creator-subscriptions/subscriptions"]'

# XPATH used to extract the user's bio/description from their profile
BIO_XPATH = './/div[@data-testid="UserDescription"]'

# XPATH used to extract the user's display name
NAME_XPATH = './/div[@data-testid="UserName"]'

# XPATH used to extract the date when the user joined the platform
JOIN_DATE_XPATH = './/span[@data-testid="UserJoinDate"]'

# XPATH used to extract the user's listed profession or category, if available
PROFESSION_XPATH = './/span[@data-testid="UserProfessionalCategory"]'

# XPATH used to extract the user's listed location
LOCATION_XPATH = './/span[@data-testid="UserLocation"]'

# XPATH used to extract the user's website URL, if they've added one to their profile
URL_XPATH = './/span[@data-testid="UserUrl"]'
