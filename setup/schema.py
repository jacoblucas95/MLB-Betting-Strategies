import sqlite3

connection = sqlite3.connect('setup/twitter.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE users(
    user_id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE, 
    password VARCHAR
    );''')

cursor.execute('''CREATE TABLE tweets(
    tweet_id INTEGER PRIMARY KEY,
    username VARCHAR,
    tweet VARCHAR,
    time VARCHAR,
    likes INTEGER DEFAULT '0',
    retweets INTEGER DEFAULT '0',
    FOREIGN KEY (username) REFERENCES users(username)
    FOREIGN KEY (retweeted_from) REFERENCES users(username)
    );''')

connection.commit()
cursor.close()