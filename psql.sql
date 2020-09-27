DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS comments;

CREATE TABLE accounts(
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    UNIQUE(user_name)
);

CREATE TABLE posts(
    post_id SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    post_title VARCHAR(255) NOT NULL,
    post_text VARCHAR(255) NOT NULL,
    post_created DATE NOT NULL DEFAULT CURRENT_DATE,
    UNIQUE(post_title),
    CONSTRAINT fk_accounts
    FOREIGN KEY(user_name)
    REFERENCES accounts(user_name)
);

CREATE TABLE comments(
    comment_id SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    post_title VARCHAR(255) NOT NULL,
    comment_text VARCHAR(255),
    comment_created DATE NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT fk_posts
    FOREIGN KEY(post_title)
    REFERENCES posts(post_title)
)