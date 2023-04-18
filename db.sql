BEGIN TRANSACTION;

DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    username varchar(25) NOT NULL,
    password varchar(40) NOT NULL,
    fullname varchar(50) DEFAULT NULL, 
    PRIMARY KEY (username)
);


-- Table Tweets --
DROP TABLE IF EXISTS Tweets;
CREATE TABLE Tweets (
    tweet_id varchar(50) NOT NULL,
    created_at TIMESTAMP NOT NULL, 
    language varchar(5) NOT NULL, 
    username varchar(25) NOT NULL, 
    type varchar(10) NOT NULL, 
    no_of_likes int DEFAULT NULL,
    no_of_retweets int DEFAULT NULL,
    no_of_reports int DEFAULT NULL,
    PRIMARY KEY (tweet_id),
    FOREIGN KEY (username) REFERENCES Users(username)
);

DROP TABLE IF EXISTS Hashtags;
CREATE TABLE Hashtags (
    tweet_id varchar(50) NOT NULL,
    hashtag varchar(100) NOT NULL, 
    FOREIGN KEY(tweet_id) REFERENCES Tweets(tweet_id)
);


-- Table Links -- 
DROP TABLE IF EXISTS Links; 
CREATE TABLE Links (
    tweet_id varchar(50) NOT NULL,
    tweet_url varchar(10000) DEFAULT NULL, 
    url_expanded_url varchar(10000) DEFAULT NULL, 
    media_url varchar(10000) DEFAULT NULL 
);



-- Edges Table --
DROP TABLE IF EXISTS Edges;
CREATE TABLE Edges (
    user1 varchar(25) NOT NULL,
    user2 varchar(25) DEFAULT NULL,
    type varchar(10) NOT NULL,
    tweet_id varchar(50) NOT NULL, 
    width int DEFAULT NULL,
    FOREIGN KEY(tweet_id) REFERENCES Tweets(tweet_id),
    FOREIGN KEY (user1) REFERENCES Users(username),
    FOREIGN KEY (user2) REFERENCES Users(username)
);

-- Following Table --
DROP TABLE IF EXISTS Following;
CREATE TABLE Following (
    user1 varchar(25) NOT NULL, 
    user2 varchar(25) NOT NULL,
    FOREIGN KEY (user1) REFERENCES Users(username),
    FOREIGN KEY (user2) REFERENCES Users(username)
);

END TRANSACTION;
