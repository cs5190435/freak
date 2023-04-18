BEGIN TRANSACTION;

COPY Users FROM '/Users/chaitanya/freak/ref/Users.csv' WITH CSV HEADER DELIMITER AS ',';
COPY Tweets FROM '/Users/chaitanya/freak/ref/Tweets.csv' WITH CSV HEADER DELIMITER AS ',';
COPY Links FROM '/Users/chaitanya/freak/ref/Links.csv' WITH CSV HEADER DELIMITER AS ',';
COPY Hashtags FROM '/Users/chaitanya/freak/ref/Hashtags.csv' WITH CSV HEADER DELIMITER AS ',';
COPY Edges FROM '/Users/chaitanya/freak/ref/Final_Edges.csv' WITH CSV HEADER DELIMITER AS ',';
COPY Following FROM '/Users/chaitanya/freak/ref/Following.csv' WITH CSV HEADER DELIMITER AS ',';

END TRANSACTION;
