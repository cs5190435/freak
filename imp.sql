BEGIN TRANSACTION;

COPY Users FROM '/Users/chaitanyakadali/freak/ref/Users.csv' WITH CSV HEADER DELIMITER AS ',';
COPY Tweets FROM '/Users/chaitanyakadali/freak/ref/Tweets.csv' WITH CSV HEADER DELIMITER AS ',';
COPY Links FROM '/Users/chaitanyakadali/freak/ref/output.csv' WITH CSV HEADER DELIMITER AS ',';
COPY Hashtags FROM '/Users/chaitanyakadali/freak/ref/Hashtags.csv' WITH CSV HEADER DELIMITER AS ',';
COPY Edges FROM '/Users/chaitanyakadali/freak/ref/Final_Edges.csv' WITH CSV HEADER DELIMITER AS ',';
COPY Following FROM '/Users/chaitanyakadali/freak/ref/Following.csv' WITH CSV HEADER DELIMITER AS ',';

END TRANSACTION;

CREATE INDEX tweetid ON Tweets (tweet_id);
