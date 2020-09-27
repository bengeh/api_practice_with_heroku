# git clone then do pip install -r requirements.txt to download all required dependencies
# run direnv allow to set DATABASE_URL for envrc

# start postgres server first
# pg_ctl -D /usr/local/var/postgres start

# activate the sql script to create table into local postgres
# \i {PATH_TO}/api_practice_with_heroku/psql.sql

# Once table is created, 
# http://127.0.0.1:5000/register?username=hi&password=lmao to register an account
# http://127.0.0.1:5000/create_post?post_title=hello test&post_text=this is the post description&post_created_by=hi to create a post
# http://127.0.0.1:5000/get_post?post_name=hello test to get a post 


# heroku pg:push postgres DATABASE_URL --app personal-diary-circles <- push local db into heroku
# heroku pg:reset DATABASE_URL --app personal-diary-circles <- resets heroku db
 