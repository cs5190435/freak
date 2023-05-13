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
    PRIMARY KEY (tweet_id)
);

DROP TABLE IF EXISTS Hashtags;
CREATE TABLE Hashtags (
    tweet_id varchar(50) NOT NULL,
    hashtag varchar(100) NOT NULL 
);


-- Table Links -- 
DROP TABLE IF EXISTS Links; 
CREATE TABLE Links (
    tweet_id varchar(50) NOT NULL,
    retweet_count int DEFAULT NULL,
    tweet_url varchar(10000) DEFAULT NULL, 
    url_expanded_url varchar(10000) DEFAULT NULL, 
    media_url varchar(10000) DEFAULT NULL, 
    likes_count int DEFAULT NULL,
    reports_count int DEFAULT NULL
);



-- Edges Table --
DROP TABLE IF EXISTS Edges;
CREATE TABLE Edges (
    user1 varchar(25) NOT NULL,
    user2 varchar(25) DEFAULT NULL,
    type varchar(10) NOT NULL,
    tweet_id varchar(50) NOT NULL, 
    width int DEFAULT NULL
);

-- Following Table (user1 follows user2) --
DROP TABLE IF EXISTS Following;
CREATE TABLE Following (
    user1 varchar(25) NOT NULL, 
    user2 varchar(25) NOT NULL
);

--Liked Table--
DROP TABLE IF EXISTS Liked;
CREATE TABLE Liked (
    username varchar(25) NOT NULL,
    tweet_id varchar(50) NOT NULL
);

--Reported Table --
DROP TABLE IF EXISTS Reported;
CREATE TABLE Reported (
    username varchar(25) NOT NULL,
    tweet_id varchar(50) NOT NULL
);

--max id--
DROP TABLE IF EXISTS maxid;
CREATE TABLE maxid (
    max integer
);

END TRANSACTION;
INSERT INTO maxid (max) VALUES (0);
