from flask import Flask, render_template, request, redirect, escape, abort,url_for,session
from  methods import *
import hashlib

app = Flask(__name__)
#FOR SESSIONS
app.secret_key = 'MyVerySecretKey'

#TEMPLATE ROUTES
#LOGIN PAGE
@app.route('/')
@app.route('/login', methods = ['POST','GET'])
def log():
    count = len(get_post())
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        response = log_in(username, password)
        print('This is the response: ', response)
        session['username'] = username
        print('Session ni ya uyu mguys' , session['username'])
        if response == 'Wrong password':
            return  render_template('login.html',response = response)
        elif response == 'Username not found':
            return render_template('login.html', response= response)
        else:
            recent = response
            #print('response[0]:',recent)
            return render_template('home.html', username = username, recent= recent, count = count)
        

#ADMIN PAGE
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')   
    else:
        fname  = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        code = hashlib.sha256(f'{str(password)}'.encode()).hexdigest()
        sign_up(fname,lname,email,username,code)
        return redirect(url_for('blog'))
#VIEW BLOG
@app.route('/blog')
def blog():
    post = get_post()
    count = len(post)
    return render_template('blog.html', post = post, count= count)
#CREATE NEW POST
@app.route('/blog/create',methods= ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('newposts.html')
    else:
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        create_post(author,title,content)
        return redirect(url_for('blog'))


@app.route('/clear',methods = ['GET'])
def clear():
    return render_template('update.html')
@app.route('/play')
def play():
    return render_template('play.html')
#ACTIONS
#SEARCH APP
@app.route('/search/<keyword>', methods=['POST'])
def search(keyword):
    keyword = request.form['keyword']
    print(keyword)
    result = db_search(keyword)
    authors = result[0]
    posts = result[1]
    return render_template('result.html' ,authors = authors, posts = posts, keyword= keyword)

#GET POST
@app.route('/blog/<int:id>')
def post(id):
    count= len(get_post())
    with DbManager(**DBCONGIF) as cursor:
        SQL = '''SELECT * FROM post WHERE post_id = %s'''
        cursor.execute(SQL,(id,))
        post = cursor.fetchall()
        content = []
        for i in post:
            content.append(i)
    return render_template('post.html' ,content= content, count=count)
    #EDIT POST
@app.route('/blog/edit/<int:id>', methods  = ['GET', 'POST'])
def edit(id):
    count = len(get_post())
    with DbManager(**DBCONGIF) as cursor:
        if request.method == 'POST':       
            author = request.form['author']
            title = request.form['title']
            content = request.form['content']
            SQL = '''UPDATE  post SET author = %s, title = %s, content = %s where post_id = %s'''
            cursor.execute(SQL,(author,title,content,id,)) 
            SQL_2 = '''SELECT * FROM post WHERE post_id = %s '''
            cursor.execute(SQL_2,(id,))
            result = cursor.fetchall()       
            return render_template('post.html', content= result , count=count)
        else:
            SQL = '''SELECT * FROM post WHERE post_id = %s'''
            cursor.execute(SQL,(id,))
            post = cursor.fetchall()
            content = []
            for i in post:
                content.append(i)
            return render_template('editpost.html', post = content)
#DELETE POST
@app.route('/blog/delete/<int:id>')
def delete(id):
        return delete_post(id)

@app.route('/view-data', methods=['POST'])
def view_data():
    username = request.form['username']
    password = request.form['password']
    log_data = view_log(username,password)
    return render_template('admin.html', log_data = log_data) 

@app.route('/play/search', methods=['POST'])
def search_letter():
    letter = request.form['letter']
    phrase  = request.form['phrase']
    result = str(search4letters(letter, phrase))
    return render_template('play.html', result = result)

@app.route('/play/lucky_no', methods=['POST','GET'])
def lucky():
    guess = int(request.form.get('guess',False)) 
    response = lucky_number(guess)
    return render_template('play.html',response = response)

@app.route('/play/keygen')
def keygen():
    key = password_gen()
    return render_template('play.html', key = key)
    
@app.route('/play/bmi', methods=['POST'] )
def bmi():
    name = request.form['name']
    weight = int(request.form['weight'])
    height = float(request.form['height'])   
    bmi = bmi_calc(name,weight,height)
    return render_template('play.html', bmi = bmi)

if __name__ == '__main__':
    app.run(port = 3000,debug=True)
