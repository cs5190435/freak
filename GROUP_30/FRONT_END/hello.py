from flask import Flask, render_template, request, url_for, flash, redirect
import psycopg2
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


def postgres_connection():
    con = psycopg2.connect(database="group_30", user="group_30", password="H1G9ZpQR3ats7t", host="10.17.51.34", port="5432")
    print("Database opened successfully")
    return con

'''@app.route('/<int:cid>')
def post(cid):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute("select * from country where country_id = %s",(cid,))
    post = cur.fetchone()
    con.close()
    if post is None:
        abort(404)
    return render_template('post.html', post = post)'''

@app.route('/')
def index():
    return render_template('index.html')
    
    
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        if not username:
            flash('Username is required!')
        elif not fullname:
            flash('Name is required!')
        elif not password:
            flash('Password is required!')
        else:
            con = postgres_connection()
            cur = con.cursor()
            cur.execute('select * from Users where username = %s',(username,))
            check = cur.fetchone()
            if check is None:
                cur.execute('insert into Users values (%s, %s, %s)',(username, password, fullname))
                con.commit()
                cur.execute('select * from Users where username = %s',(username,))
                post = cur.fetchone()
                cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type, tweets.username from links, (select Tweets.tweet_id, Tweets.created_at, Tweets.language, Tweets.type, Tweets.username from Tweets, (select user2 from Following where user1 = %s) as foo where Tweets.username = foo.user2) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(username,))
                twts = cur.fetchall()
                con.close()
                flash('account created successfully')
                return render_template('user.html',post=post,twts=twts)
            else:
                flash('user name already exists! please use a different user name')
    return render_template('create.html')


@app.route('/createone', methods=('GET', 'POST'))
def createone():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        else:
            con = postgres_connection()
            cur = con.cursor()
            cur.execute('select * from Users where username = %s',(username,))
            post = cur.fetchone()
            if post is None:
                flash('Invalid Login!')
            elif username != str(post[0]) or password != str(post[1]):
                print(str(username) + " " + str(password) + " : " + str(post[0]) + " " + str(post[1])) 
                flash('Invalid Login! Please try again')
            else:
                cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type, tweets.username from links, (select Tweets.tweet_id, Tweets.created_at, Tweets.language, Tweets.type, Tweets.username from Tweets, (select user2 from Following where user1 = %s) as foo where Tweets.username = foo.user2) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(username,))
                twts = cur.fetchall()
                con.close()
                return render_template('user.html',post=post,twts=twts)
    return render_template('createone.html')


@app.route('/user <string:username>-<string:fullname>')
def user(username, fullname):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('select * from Users where username = %s',(username,))
    post = cur.fetchone()
    cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type, tweets.username from links, (select Tweets.tweet_id, Tweets.created_at, Tweets.language, Tweets.type, Tweets.username from Tweets, (select user2 from Following where user1 = %s) as foo where Tweets.username = foo.user2) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(username,))
    twts = cur.fetchall()
    con.close()
    return render_template('user.html', post=post, twts=twts)


@app.route('/following <string:username>-<string:password>-<string:fullname>', methods=('GET', 'POST'))
def following(username,password,fullname):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('select Users.username, Users.fullname from Following, Users where Following.user1 = %s and Following.user2 = Users.username limit 10', (username,))
    posts = cur.fetchall()
    con.close()
    return render_template('following.html', posts=posts, username = username, fullname = fullname, password=password)


@app.route('/followingtwo <string:username>-<string:password>-<string:fullname>', methods=('GET', 'POST'))
def followingtwo(username,password,fullname):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('select Users.username, Users.fullname from Following, Users where Following.user2 = %s and Users.username = Following.user1 limit 10', (username,))
    posts = cur.fetchall()
    con.close()
    return render_template('followingtwo.html', posts=posts, username = username, fullname=fullname,password=password)


@app.route('/search <username>-<password>-<fullname>', methods=('GET','POST'))
def search(username, password, fullname):
    if request.method == 'POST':
        searchuser = request.form['searchname']
        con = postgres_connection()
        cur = con.cursor()
        cur.execute('select * from Users where position(%s in username) != 0 and username != %s', (searchuser,username))
        posts = cur.fetchall()
        #return render_template('index.html')
        return render_template('searchpage.html',username=username,password=password,fullname=fullname,posts=posts)
    return render_template('search.html',post=[username,password,fullname])

@app.route('/searchtwo <username>-<password>-<fullname>', methods=('GET','POST'))
def searchtwo(username, password, fullname):
    if request.method == 'POST':
        searchhash = request.form['searchname']
        con = postgres_connection()
        cur = con.cursor()
        cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, Tweets.created_at, Tweets.language, Tweets.type, Tweets.username from Hashtags,links,Tweets where links.tweet_id=Hashtags.tweet_id and Tweets.tweet_id=Hashtags.tweet_id and Hashtags.hashtag=%s order by created_at desc', (searchhash,))
        twts = cur.fetchall()
        #return render_template('index.html')
        return render_template('searchpagetwo.html', post=[username,password,fullname],twts=twts,searchhash=searchhash)
    return render_template('searchtwo.html',post=[username,password,fullname])


@app.route('/profile <username>-<password>-<fullname>')
def profile(username, password, fullname):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type from links, (select tweet_id, created_at, language, type from Tweets where username = %s) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(username,))
    twts = cur.fetchall()
    return render_template('profile.html',post=[username,fullname,password],twts=twts)


@app.route('/deleteacc <username>')
def deleteacc(username):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('delete from Hashtags where tweet_id in (select tweet_id from Tweets where username = %s)',(username,))
    con.commit()
    cur.execute('delete from Users where username = %s',(username,))
    con.commit()
    con.close()
    flash('account deleted successfully','information')
    return render_template ('index.html')


@app.route('/updateacc <username>-<fullname>',methods=('GET','POST'))
def updateacc(username,fullname):
    if request.method == 'POST':
        newusername = request.form['username']
        newfullname = request.form['fullname']
        newpassword = request.form['password']
        con = postgres_connection()
        cur = con.cursor()
        cur.execute('select * from Users where username = %s',(newusername,))
        check = cur.fetchone()
        if check is None or (newusername == username):
            cur.execute('update Users set username = %s, fullname = %s, password = %s where username = %s',(newusername,newfullname,newpassword,username))
            con.commit()
            cur.execute('select * from Users where username = %s',(newusername,))
            post = cur.fetchone()
            cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type from links, (select tweet_id, created_at, language, type from Tweets where username = %s) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(newusername,))
            twts = cur.fetchall()
            con.close()
            #print(str(post[0]) + "::" + str(post[2]))
            flash('account is updated')
            return render_template('profile.html',post=[post[0],post[2],post[1]],twts=twts)
        else:
            flash('user name you have given is already used by some other person! please use a different user name')
    return render_template('updateacc.html')


@app.route('/otheruser <username>-<password>-<fullname>-<otherusername>')
def otheruser(username, password, fullname, otherusername):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type from links, (select tweet_id, created_at, language, type from Tweets where username = %s) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(otherusername,))
    twts = cur.fetchall()
    con.close()
    return render_template('otheruser.html',username=username,password=password,fullname=fullname,otherusername=otherusername,twts=twts)


@app.route('/startfollow <username>-<password>-<fullname>-<otherusername>')
def startfollow(username, password, fullname, otherusername):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('select * from Following where user2 = %s and user1 = %s',(otherusername,username))
    post = cur.fetchone()
    if post is None:
        cur.execute('insert into Following values (%s,%s)',(otherusername,username))
        con.commit()
        cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type from links, (select tweet_id, created_at, language, type from Tweets where username = %s) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(otherusername,))
        twts = cur.fetchall()
        con.close()
        flash('Now you are following the user')
        return render_template('otheruser.html',username=username,password=password,fullname=fullname,otherusername=otherusername,twts=twts)
    else:
        cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type from links, (select tweet_id, created_at, language, type from Tweets where username = %s) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(otherusername,))
        twts = cur.fetchall()
        con.close()
        flash('You are already following the user')
        return render_template('otheruser.html',username=username,password=password,fullname=fullname,otherusername=otherusername,twts=twts)


@app.route('/newtweet <username>-<fullname>-<password>',methods=('GET','POST'))
def newtweet(username, fullname, password):
    if request.method == 'POST':
        newusername = username
        newtype = '1. Tw'
        newlang = request.form['lang']
        newtweet_url = request.form['tweet_url']
        newurls_expanded_url = newtweet_url
        newmedia_expaned_url =request.form['media_url']
        hashtags = request.form['hashtags']	    
        con = postgres_connection()
        cur = con.cursor()
        cur.execute('select now()::timestamptz(0)')
        newcreated_at = cur.fetchone()[0]
        cur.execute('select max from maxid')
        tweet = cur.fetchone()
        tweetid = tweet[0]
        cur.execute('update maxid set max = max + 1')
        con.commit()
        cur.execute('insert into Tweets values (%s, %s, %s, %s, %s)',(('x'+str(tweetid)), newcreated_at, newlang, newusername, newtype))
        con.commit()
        cur.execute('insert into links values (%s, 0, %s, %s, %s, 0, 0)',(('x'+str(tweetid)), newtweet_url, newurls_expanded_url, newmedia_expaned_url))
        con.commit()
        arr = hashtags.split('#')
        if hashtags != "":
            for hashtag in arr:
                cur.execute('insert into Hashtags values (%s, %s)',(('x'+str(tweetid)), hashtag))
                con.commit()
        cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type from links, (select tweet_id, created_at, language, type from Tweets where username = %s) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(newusername,))
        twts = cur.fetchall()
        con.close()
        return render_template('profile.html',post=[username,fullname,password],twts=twts)
    return render_template('newtweet.html',username=username,fullname=fullname,password=password)
    
    
@app.route('/reply <tweetid>-<username>-<password>-<fullname>-<secondusername>', methods=('GET','POST'))
def reply(tweetid, username, password, fullname, secondusername):
    if request.method == 'POST':
        newusername = username
        newtype = '4. Re'
        newlang = request.form['lang']
        newtweet_url = request.form['tweet_url']
        #newtweet_url = '1'
        newurls_expanded_url = newtweet_url
        #newurls_expanded_url = request.form['url_expanded_url']
        newmedia_expaned_url =request.form['media_url']	        
        #newmedia_expaned_url ='1'       
        con = postgres_connection()
        cur = con.cursor()
        cur.execute('select now()::timestamptz(0)')
        newcreated_at = cur.fetchone()[0]
        cur.execute('select max from maxid')
        newtweet = cur.fetchone()
        newtweetid = newtweet[0]
        cur.execute('update maxid set max = max + 1')
        con.commit()
        cur.execute('insert into Tweets values (%s, %s, %s, %s, %s)',(('x'+str(newtweetid)), newcreated_at, newlang, newusername, newtype))
        con.commit()
        cur.execute('insert into links values (%s, 0, %s, %s, %s, 0, 0)',(('x'+str(newtweetid)), newtweet_url, newurls_expanded_url, newmedia_expaned_url))
        con.commit()
        cur.execute('insert into edges values (%s, %s, %s, %s, 1)',(username, secondusername, newtype, ('x'+str(newtweetid))))
        con.commit()
        cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type, tweets.username from links, (select Tweets.tweet_id, Tweets.created_at, Tweets.language, Tweets.type, Tweets.username from Tweets, (select user2 from Following where user1 = %s) as foo where Tweets.username = foo.user2) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(newusername,))
        twts = cur.fetchall()
        con.close()
        return render_template('user.html', post=[username, password, fullname], twts=twts)
    return render_template('reply.html',post=[username, password, fullname])
    
    
@app.route('/retweet <tweetid>-<username>-<password>-<fullname>-<secondusername>')
def retweet(tweetid, username, password, fullname, secondusername):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('select now()::timestamptz(0)')
    newcreated_at = cur.fetchone()[0]
    cur.execute('select language, created_at from Tweets where tweet_id = %s',(tweetid,))
    p = cur.fetchone()
    cur.execute('select tweet_url, url_expanded_url, media_url from links where tweet_id = %s',(tweetid,))
    q = cur.fetchone()
    cur.execute('select max from maxid')
    newtweet = cur.fetchone()
    newtweetid = newtweet[0]
    cur.execute('update maxid set max = max + 1')
    con.commit()
    cur.execute('update links set retweet_count = (retweet_count + 1) where tweet_id = %s',(tweetid,))
    con.commit()	
    #cur.execute('insert into Tweets values (%s, %s, %s, %s, %s)',(('x'+str(newtweetid)), username, '3. RT', newcreated_at, p[0]))
    cur.execute('insert into Tweets values (%s, %s, %s, %s, %s, 0, 0)',(('x'+str(newtweetid)), newcreated_at, username, '3. RT', p[0]))
    con.commit()
    cur.execute('insert into links values (%s,0,%s,%s,%s,0,0)',(('x'+str(newtweetid)), q[0], q[1], q[2]))
    con.commit()
    cur.execute('insert into edges values (%s, %s, %s, %s, 1)',(username, secondusername, '3. RT', ('x'+str(newtweetid))))
    con.commit()
    cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type, tweets.username from links, (select Tweets.tweet_id, Tweets.created_at, Tweets.language, Tweets.type, Tweets.username from Tweets, (select user2 from Following where user1 = %s) as foo where Tweets.username = foo.user2) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(username,))
    twts = cur.fetchall()
    con.close()
    return render_template('user.html',post=[username,password,fullname],twts=twts)
    

@app.route('/stopfollow <username>-<password>-<fullname>-<otherusername>')
def stopfollow(username, password, fullname, otherusername):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('select * from Following where user2 = %s and user1 = %s',(otherusername,username))
    post = cur.fetchone()
    if post is not None:
        cur.execute('delete from Following where user2 = %s and user1 = %s',(otherusername,username))
        con.commit()
        cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type from links, (select tweet_id, created_at, language, type from Tweets where username = %s) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(otherusername,))
        twts = cur.fetchall()
        con.close()
        flash('Now you are not following the user')
        return render_template('otheruser.html',username=username,password=password,fullname=fullname,otherusername=otherusername,twts=twts)
    else:
        cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type from links, (select tweet_id, created_at, language, type from Tweets where username = %s) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(otherusername,))
        twts = cur.fetchall()
        con.close()
        flash('You don\'t follow the user already')
        return render_template('otheruser.html',username=username,password=password,fullname=fullname,otherusername=otherusername,twts=twts)


@app.route('/liked <tweetid>-<username>-<password>-<fullname>')
def liked(tweetid, username, password, fullname):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('select * from liked where username = %s and tweet_id = %s',(username,tweetid))
    post = cur.fetchone()
    if post is None:
        cur.execute('update links set likes_count = (likes_count + 1) where tweet_id = %s',(tweetid,))
        con.commit()
        cur.execute('insert into liked values (%s, %s)',(username,tweetid))
        con.commit()
    cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type, tweets.username from links, (select Tweets.tweet_id, Tweets.created_at, Tweets.language, Tweets.type, Tweets.username from Tweets, (select user2 from Following where user1 = %s) as foo where Tweets.username = foo.user2) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc ',(username,))
    twts = cur.fetchall()
    con.close()
    return render_template('user.html',post=[username, password, fullname],twts=twts)


@app.route('/likedother <tweetid>-<username>-<password>-<fullname>-<otherusername>')
def likedother(tweetid, username, password, fullname, otherusername):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('select * from liked where username = %s and tweet_id = %s',(username,tweetid))
    post = cur.fetchone()
    if post is None:
        cur.execute('update links set likes_count = (likes_count + 1) where tweet_id = %s',(tweetid,))
        con.commit()
        cur.execute('insert into liked values (%s, %s)',(username,tweetid))
        con.commit()
    cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type from links, (select tweet_id, created_at, language, type from Tweets where username = %s) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(otherusername,))
    twts = cur.fetchall()
    con.close()
    return render_template('otheruser.html',username=username, password=password, fullname=fullname,otherusername=otherusername,twts=twts)


@app.route('/reported <tweetid>-<username>-<password>-<fullname>')
def reported(tweetid, username, password, fullname):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('select * from reported where username = %s and tweet_id = %s',(username,tweetid))
    post = cur.fetchone()
    if post is None:
        cur.execute('update links set reports_count = (reports_count + 1) where tweet_id = %s',(tweetid,))
        con.commit()
        cur.execute('insert into reported values (%s, %s)',(username,tweetid))
        con.commit()
    cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type, tweets.username from links, (select Tweets.tweet_id, Tweets.created_at, Tweets.language, Tweets.type, Tweets.username from Tweets, (select user2 from Following where user1 = %s) as foo where Tweets.username = foo.user2) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(username,))
    twts = cur.fetchall()
    con.close()
    return render_template('user.html',post=[username, password, fullname],twts=twts)

@app.route('/reportedother <tweetid>-<username>-<password>-<fullname>-<otherusername>')
def reportedother(tweetid, username, password, fullname, otherusername):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('update links set reports_count = (reports_count + 1) where tweet_id = %s and not exists (select * from reported where username = %s and tweet_id = %s)',(tweetid,username,tweetid))
    con.commit()
    cur.execute('insert into reported values (%s, %s)',(username,tweetid))
    con.commit()
    cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type from links, (select tweet_id, created_at, language, type from Tweets where username = %s) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(otherusername,))
    twts = cur.fetchall()
    con.close()
    return render_template('otheruser.html',username=username, password=password, fullname=fullname,otherusername=otherusername,twts=twts)


@app.route('/deletetwt <tweetid>-<username>-<fullname>-<password>')
def deletetwt(tweetid, username, fullname, password):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute("delete from hashtags where tweet_id = %s", (tweetid,))
    con.commit()	
    cur.execute('delete from Tweets where tweet_id = %s',(tweetid,))
    con.commit()
    cur.execute('select links.tweet_id, links.retweet_count, links.likes_count, links.reports_count, links.tweet_url, tweets.created_at, tweets.language, tweets.type from links, (select tweet_id, created_at, language, type from Tweets where username = %s) as tweets where tweets.tweet_id = links.tweet_id order by tweets.created_at desc',(username,))
    twts = cur.fetchall()
    con.close()
    return render_template('profile.html',post=[username,fullname,password],twts=twts)
    
    
@app.route('/trend <username>-<password>-<fullname>')
def trend(username, password, fullname):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('select * from trendingthree')
    posts = cur.fetchall()
    con.close()
    return render_template('trend.html', posts=posts,username=username,password=password,fullname=fullname)
    
 
@app.route('/show <tweetid>')
def show(tweetid):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('select hashtag from Hashtags where tweet_id = %s',(tweetid,))
    posts = cur.fetchall()
    return render_template('show.html',posts=posts)
    
    
@app.route('/recommend <username>-<password>-<fullname>')
def recommend(username, password, fullname):
    con = postgres_connection()
    cur = con.cursor()
    cur.execute('WITH RECURSIVE recommend (f1,f2) AS (select user2 as f1, user1 as f2,1 as dist from Following where user1= %s UNION select user2,f2,dist+1 from Following ,recommend where user1=recommend.f1 and recommend.f2!= user2 and (dist=1 or dist=2) and user2 not in (select user2 from Following where user1 =%s)) select distinct f1 as recommend  from recommend where f1!=f2 and dist!=1 order by recommend', (username, username))
    posts = cur.fetchall()
    con.close()
    return render_template('recommend.html', posts=posts,username=username,password=password,fullname=fullname)
    
if __name__ == '__main__':
    app.run(host="localhost", port=5039, debug=True)


