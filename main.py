from flask import Flask, render_template, url_for, request, redirect,make_response, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
import os
import hashlib
import random
import uuid
#from flask_uploads 
#from models import User, db #susitvarkyti


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_base.db'
app.config['UPLOAD_DOCS'] = "static/doc/"
app.config['UPLOAD_Images'] = "static/galerija/"
app.config['UPLOAD_BACKGROUND'] = "static/img/"
DEFAULT_IMG = "cropped-1920.jpg"
db = SQLAlchemy(app)

#============================ Lentutes ============================
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	name = db.Column(db.String(200), nullable=False)
	surname = db.Column(db.String(200), nullable=False)
	phone = db.Column(db.String(200), default="")
	email = db.Column(db.String(200), nullable=False)
	lvl = db.Column(db.Integer, default=0)
	password = db.Column(db.String(200), nullable=False)
	image = db.Column(db.String(300), default="")
	info = db.Column(db.String(1000), default="")
	info_en = db.Column(db.String(1000), default="")
	show = db.Column(db.String(10), default="False")
	confirmed = db.Column(db.String(10), default="False")
	session_token = db.Column(db.String, default="")
	lang = db.Column(db.String, default="LT")
	
	
	
class Contact_text(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	info = db.Column(db.String(4000), default="")
	info_en = db.Column(db.String(4000), default="")

	
class Messages(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False)
	sms = db.Column(db.String(4000), default="")
	

class Document(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	name = db.Column(db.String(4000), default="")
	
class MyImage(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	name = db.Column(db.String(4000), default="")
	
	
class News(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	title = db.Column(db.String(4000), default="")
	title_en = db.Column(db.String(4000), default="")
	date = db.Column(db.String(4000), default="")
	location = db.Column(db.String(4000), default="")
	
	
class News_in_LT(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	title = db.Column(db.String(4000), default="")
	title_en = db.Column(db.String(4000), default="")
	date = db.Column(db.String(4000), default="")
	location = db.Column(db.String(4000), default="")
	

class News_in_World(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	title = db.Column(db.String(4000), default="")
	title_en = db.Column(db.String(4000), default="")
	date = db.Column(db.String(4000), default="")
	location = db.Column(db.String(4000), default="")

class History(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	text = db.Column(db.String(400000), default="")
	text_en = db.Column(db.String(400000), default="")
	
class Officer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	text = db.Column(db.String(400000), default="")
	text_en = db.Column(db.String(400000), default="")

class Comision(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	text = db.Column(db.String(400000), default="")
	text_en = db.Column(db.String(400000), default="")
	
class Recruit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	text = db.Column(db.String(400000), default="")
	text_en = db.Column(db.String(400000), default="")
	
class Purpose(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	text = db.Column(db.String(400000), default="")
	text_en = db.Column(db.String(400000), default="")
	
class About(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	text = db.Column(db.String(400000), default="")
	text_en = db.Column(db.String(400000), default="")

class Document_EPS(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	name_lt = db.Column(db.String(4000), default="")	
	name = db.Column(db.String(4000), default="")	
	name_en = db.Column(db.String(4000), default="")	
	URL = db.Column(db.String(4000), default="")	
	link_name = db.Column(db.String(4000), default="")	
	link_name_en = db.Column(db.String(4000), default="")	

class Topimg(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	name = db.Column(db.String(100), default="")
	
	
#============================ Duomenu Baze ============================	
	
	
if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
	#print(app.config['SQLALCHEMY_DATABASE_URI'])
	db.create_all()
	users_ = list(User.query.all())
	if len(users_)== 0:
		#Admin
		super_admin = User()
		super_admin.name = "SuperAdmin"
		super_admin.surname = "SuperAdmin"
		super_admin.phone = 88888888
		super_admin.email = "admin@demo.lt"
		super_admin.lvl = 2
		password = "demo"
		super_admin.password = hashlib.sha256(password.encode()).hexdigest()
		super_admin.info = "Pradinis administratorius"
		super_admin.show = "False"
		super_admin.confirmed = "True"
		super_admin.lang = "LT"
		db.session.add(super_admin)
		db.session.commit()

		
		
#============================ Base ============================
def get_bg_img():
	try:
		data = Topimg.query.get_or_404(1)
		img = data.name
	except:
		img = "../" + app.config['UPLOAD_BACKGROUND'] + DEFAULT_IMG
	return img
	
def guest_user():
	current_user = User()
	current_user.name=""
	current_user.surname="Svecias"
	current_user.email="gg@gg.gg"
	current_user.lvl=0
	current_user.id=-1
	current_user.lang = "LT"
	return current_user
	
def current_user():
	email = request.cookies.get("current-user-email")
	current_user = User.query.filter_by(email=email).first()
	if current_user == None:
		current_user = guest_user()
	current_user.lang = request.cookies.get("current-user-lang")
	#print(current_user.lang)
	return current_user


		
@app.route("/prisijungti/",  methods=["POST","GET"])
def login():
	message = ""
	email=""
	fokus ='autofocus=""'
	if request.method == 'POST':
		email = request.form.get("login")
		password = request.form.get("password")
		hashed_password = hashlib.sha256(password.encode()).hexdigest()
		user = User.query.filter_by(email=email).first()		
		if not user:
			user = guest_user()
			user.password = hashed_password

		if hashed_password != user.password:
			message =  "WRONG PASSWORD! / Klaidingas Slaptažodis"
			return render_template("login.html", email = email, message = message,fokus="", current_user=current_user(),bg_img=get_bg_img())
			
		elif hashed_password == user.password:
			user.session_token = str(uuid.uuid4())
			response = make_response(redirect(url_for('index')))
			response.set_cookie("session-token", user.session_token)  #  consider adding httponly=True on production
			response.set_cookie("current-user-name", user.name) 
			response.set_cookie("current-user-lvl", str(user.lvl)) 
			response.set_cookie("current-user-id", str(user.id)) 
			response.set_cookie("current-user-email", str(user.email)) 
			response.set_cookie("current-user-lang", str(user.lang)) 
			return response
	else:
		return render_template("login.html", email = email, message = message,fokus=fokus, current_user=current_user(), bg_img=get_bg_img())
		
		
@app.route("/logout/")
def logout():
	response = make_response(redirect(url_for('index')))
	response.set_cookie('session-token', '', expires=0)
	response.set_cookie('current-user-name', '', expires=0)
	response.set_cookie('current-user-lvl', '', expires=0)
	response.set_cookie('current-user-id', '', expires=0)
	response.set_cookie('current-user-email', '', expires=0)
	#response.set_cookie('current-user-lang', '', expires=0)
	return response
	
@app.route("/change_lang/")
def change_lang():
	response = make_response(redirect(url_for('index')))
	lang = request.cookies.get("current-user-lang")
	if lang == "EN":
		response.set_cookie("current-user-lang","LT") 
	else:
		response.set_cookie("current-user-lang","EN") 	
	return response

	

	
@app.route("/")
def index():
	try:
		data = About.query.get_or_404(1)
	except:
		data = About()
		data.text = "Teksto nėra adminas turi pridėti"
		data.text_en = "Admin have to add text"
		db.session.add(data)
		db.session.commit()
	news_ = list(reversed(News.query.order_by(News.date_created).all()))
	return render_template("index.html", data=data,news=news_,bg_img=get_bg_img(), current_user=current_user())
	
	
	
@app.route("/edit_about/<int:id>", methods=["GET", "POST"])
def edit_about(id):
	data = About.query.get_or_404(id)
	if request.method == "POST":
		data.text = request.form['text']
		data.text_en = request.form['text_en']
		try:
			db.session.commit()
			return redirect('/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("APIE_create.html",data=data, current_user=current_user(), bg_img=get_bg_img())
	
	
	
@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html',current_user=current_user(),bg_img=get_bg_img()), 404
	
	
	
#============================ Registracija ============================

@app.route("/registracija/", methods=["POST","GET"])
def registration():
	if request.method == 'POST':
		user = User()
		user.name = request.form.get('user_name')
		user.surname = request.form['surname']
		user.phone = request.form['phone']
		user.email = request.form['email']
		user.lvl = 0
		password = request.form['password']
		user.password = hashlib.sha256(password.encode()).hexdigest()
		#passwordr = request.form['passwordr']
		#user.image = format(request.form['image'])
		#user.info = request.form['info']
		user.info = ""
		user.info_en = ""
		user.show = "False"
		user.confirmed = "False"
		try:
			db.session.add(user)
			db.session.commit()
			return render_template("registration_sucess.html", current_user=current_user(), bg_img=get_bg_img())
			
		except:
			
			return 'buvo problema dedant i db'
	else:
		return render_template("registration.html", current_user=current_user(), bg_img=get_bg_img())
		

	
#============================ Zinutes ============================
	
@app.route("/sms/")
def messages_users():
	messages_ = list(reversed(Messages.query.order_by(Messages.date_created).all()))
	return render_template("sms.html", messages=messages_, current_user=current_user(), bg_img=get_bg_img())
	
#============================ Vartotojai ============================

@app.route("/vartotojai/", methods=["POST","GET"])
def control_users():
	users = reversed(User.query.order_by(User.date_created).all())
	return render_template("vartotojai.html", users=users, current_user=current_user(), bg_img=get_bg_img())
	


@app.route('/confirm_user/<int:id>')
def confirm_user(id):
	user = User.query.get_or_404(id)
	user.confirmed = "True"
	user.lvl = 1
	try:
		db.session.commit()
		return redirect('/vartotojai/')
	except:
		return 'problema patvirtinant vartotoja'
	

@app.route('/show_user/<int:id>')
def show_user(id):
	user = User.query.get_or_404(id)
	if user.show == "False":
		user.show = "True"
	else:
		user.show = "False"
	try:
		db.session.commit()
		return redirect('/vartotojai/')
	except:
		return 'problema suteikiant vartotojuj rodymo statusa'
	
	
@app.route('/delete_user/<int:id>')
def delete_user(id):
	user = User.query.get_or_404(id)
	try:
		db.session.delete(user)
		db.session.commit()
		return redirect('/vartotojai/')
	except:
		return 'problema trinant vartotoja'

		
@app.route("/edit_user/<int:id>", methods=["GET", "POST"])
def edit_user(id):
	user = User.query.get_or_404(id)
	if request.method == "POST":
		user.name = request.form.get('user_name')
		user.surname = request.form['surname']
		user.phone = request.form['phone']
		user.email = request.form['email']
		#user.lvl = 0
		password = request.form['password']
		user.password = hashlib.sha256(password.encode()).hexdigest()
		#passwordr = request.form['passwordr']
		#user.image = format(request.form['image'])
		user.info = request.form['info']
		user.info_en = request.form['info_en']
		#user.show = "False"
		try:
			db.session.commit()
			return redirect('/vartotojai/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("profilis.html",user=user, current_user=current_user(), bg_img=get_bg_img())

	
	
	
	
@app.route('/down_user/<int:id>')
def down_user(id):
	user = User.query.get_or_404(id)
	user.lvl -= 1
	try:
		db.session.commit()
		return redirect('/vartotojai/')
	except:
		return 'problema mazinant vartotojo lvl'
	
	
	
@app.route('/up_user/<int:id>')
def up_user(id):
	user = User.query.get_or_404(id)
	user.lvl += 1
	try:
		db.session.commit()
		return redirect('/vartotojai/')
	except:
		return 'problema didinant vartotojo lvl'
	
	
	
	
@app.route('/remove_message/<int:id>')
def remove_message(id):
	message = Messages.query.get_or_404(id)
	try:
		db.session.delete(message)
		db.session.commit()
		return redirect('/sms/')
	except:
		return 'problema trinant zinute'

	
#============================ kontaktai ============================
	
@app.route("/kontaktai/", methods=["POST","GET"])
def contacts_of_users():
	if request.method == 'POST':
		message = Messages()
		message.name = request.form['name']
		message.email = request.form['email']
		message.sms = request.form['message']
		db.session.add(message)
		db.session.commit()
		return render_template("zinute_priimta.html", current_user=current_user(), bg_img=get_bg_img())
	else:
		users_ = reversed(User.query.order_by(User.date_created).all())
		users = []
		
		try:
			contact_main = Contact_text.query.get_or_404(1)
		except:
			contact_main = Contact_text()
			contact_main.info = "Bendroji kontaktinė informacija neužpildyta"
			contact_main.info_en = "General contact information is blank"
			db.session.add(contact_main)
			db.session.commit()
		
		
		for user in users_:
			if user.show == "True":
				users.append(user)
		return render_template("kontaktai.html", users=users, contact_main=contact_main, current_user=current_user(), bg_img=get_bg_img())
	
	
	
	
@app.route("/edit_contact_info/<int:id>", methods=["GET", "POST"])
def edit_contact_info(id):
	main_info = Contact_text.query.get_or_404(id)
	if request.method == "POST":
		main_info.info = request.form['info']
		main_info.info_en = request.form['info_en']
		try:
			db.session.commit()
			return redirect('/kontaktai/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("redaguoti_kontaktus.html",contact_main=main_info, current_user=current_user(), bg_img=get_bg_img())
	
	

	
#============================ naujienos ============================
	
@app.route("/Naujienos/", methods=["GET", "POST"])
def news():
	news_ = list(reversed(News.query.order_by(News.date_created).all()))
	return render_template("Naujienos.html",news = news_ , current_user=current_user(), bg_img=get_bg_img())
	

@app.route("/create_news/", methods=["GET", "POST"])	
def create_news():
	new_ = News()
	new_.title = ""
	new_.title_en =""
	new_.date =""
	new_.location =""
	if request.method == "POST":
		new_.title = request.form['title']
		new_.title_en = request.form['title_en']
		new_.date = request.form['date']
		new_.location = request.form['location']
		try:
			db.session.add(new_)
			db.session.commit()
			return redirect('/Naujienos/')
		except:
			return "nepavyko prideti naujienos i db"
	else:
		return render_template("Naujienos_create.html",new = new_, current_user=current_user(), bg_img=get_bg_img())
	
	
	
@app.route("/edit_new/<int:id>", methods=["GET", "POST"])
def edit_new(id):
	new_ = News.query.get_or_404(id)
	if request.method == "POST":
		new_.title = request.form['title']
		new_.title_en = request.form['title_en']
		new_.date = request.form['date']
		new_.location = request.form['location']
		try:
			db.session.commit()
			return redirect('/Naujienos/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("Naujienos_create.html",new = new_, current_user=current_user(), bg_img=get_bg_img())
	
	
@app.route("/delete_new/<int:id>", methods=["GET", "POST"])
def delete_new(id):
	new_ = News.query.get_or_404(id)
	try:
		db.session.delete(new_)
		db.session.commit()
		return redirect('/Naujienos/')
	except:
		return 'problema trinant naujiena'
	
	
# ================== events #=====================


	
@app.route("/Renginiai_lietuvoje/", methods=["GET", "POST"])
def events():
	events = list(reversed(News_in_LT.query.order_by(News_in_LT.date_created).all()))
	return render_template("Renginiai_lietuvoje.html",events = events , current_user=current_user(), bg_img=get_bg_img())
	

@app.route("/create_event/", methods=["GET", "POST"])	
def create_event():
	event = News_in_LT()
	event.title = ""
	event.title_en =""
	event.date =""
	event.location =""
	if request.method == "POST":
		event.title = request.form['title']
		event.title_en = request.form['title_en']
		event.date = request.form['date']
		event.location = request.form['location']
		try:
			db.session.add(event)
			db.session.commit()
			return redirect('/Renginiai_lietuvoje/')
		except:
			return "nepavyko prideti naujienos i db"
	else:
		return render_template("Renginiai_lietuvoje_create.html",event = event, current_user=current_user(), bg_img=get_bg_img())
	
	
	
@app.route("/edit_event/<int:id>", methods=["GET", "POST"])
def edit_event(id):
	event = News_in_LT.query.get_or_404(id)
	if request.method == "POST":
		event.title = request.form['title']
		event.title_en = request.form['title_en']
		event.date = request.form['date']
		event.location = request.form['location']
		try:
			db.session.commit()
			return redirect('/Renginiai_lietuvoje/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("Renginiai_lietuvoje_create.html",event = event, current_user=current_user(), bg_img=get_bg_img())
	
	
@app.route("/delete_event/<int:id>", methods=["GET", "POST"])
def delete_event(id):
	event = News_in_LT.query.get_or_404(id)
	try:
		db.session.delete(event)
		db.session.commit()
		return redirect('/Renginiai_lietuvoje/')
	except:
		return 'problema trinant naujiena'
	
	
	
	
# ================== tarptautiniai events #=====================


	
@app.route("/Tarptautiniai_renginiai/", methods=["GET", "POST"])
def tevents():
	events = list(reversed(News_in_World.query.order_by(News_in_World.date_created).all()))
	return render_template("Tartautiniai_renginiai.html",events = events , current_user=current_user(), bg_img=get_bg_img())
	

@app.route("/create_tevent/", methods=["GET", "POST"])	
def tcreate_event():
	event = News_in_World()
	event.title = ""
	event.title_en =""
	event.date =""
	event.location =""
	if request.method == "POST":
		event.title = request.form['title']
		event.title_en = request.form['title_en']
		event.date = request.form['date']
		event.location = request.form['location']
		try:
			db.session.add(event)
			db.session.commit()
			return redirect('/Tarptautiniai_renginiai/')
		except:
			return "nepavyko prideti naujienos i db"
	else:
		return render_template("Tartautiniai_renginiai_create.html",event = event, current_user=current_user(), bg_img=get_bg_img())
	
	
	
@app.route("/edit_tevent/<int:id>", methods=["GET", "POST"])
def tedit_event(id):
	event = News_in_World.query.get_or_404(id)
	if request.method == "POST":
		event.title = request.form['title']
		event.title_en = request.form['title_en']
		event.date = request.form['date']
		event.location = request.form['location']
		try:
			db.session.commit()
			return redirect('/Tarptautiniai_renginiai/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("Tartautiniai_renginiai_create.html",event = event, current_user=current_user(), bg_img=get_bg_img())
	
	
@app.route("/delete_tevent/<int:id>", methods=["GET", "POST"])
def tdelete_event(id):
	event = News_in_World.query.get_or_404(id)
	try:
		db.session.delete(event)
		db.session.commit()
		return redirect('/Tarptautiniai_renginiai/')
	except:
		return 'problema trinant naujiena'
	
	
	
#============================ History ============================
	
	
	
@app.route("/history/")
def history():
	try:
		data = History.query.get_or_404(1)
	except:
		data = History()
		data.text = "Teksto nėra adminas turi pridėti"
		data.text_en = "Admin have to add text"
		db.session.add(data)
		db.session.commit()
	#data.text = data.text.replace(" ","&nbsp")
	#data.text_en = data.text_en.replace(" ","&nbsp")
	return render_template("History.html", data=data, current_user=current_user(), bg_img=get_bg_img())
	

@app.route("/edit_history/<int:id>", methods=["GET", "POST"])
def edit_history(id):
	data = History.query.get_or_404(id)
	if request.method == "POST":
		data.text = request.form['text']
		data.text_en = request.form['text_en']
		try:
			db.session.commit()
			return redirect('/history/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("APIE_create.html",data=data, current_user=current_user(), bg_img=get_bg_img())
	
	
	
#============================ Officer ============================	
	
	
@app.route("/officer/")
def officer():
	try:
		data = Officer.query.get_or_404(1)
	except:
		data = Officer()
		data.text = "Teksto nėra adminas turi pridėti"
		data.text_en = "Admin have to add text"
		db.session.add(data)
		db.session.commit()
	#data.text = data.text.replace(" ","&nbsp")
	#data.text_en = data.text_en.replace(" ","&nbsp")
	return render_template("Officer.html", data=data, current_user=current_user(), bg_img=get_bg_img())
	

@app.route("/edit_officer/<int:id>", methods=["GET", "POST"])
def edit_officer(id):
	data = Officer.query.get_or_404(id)
	if request.method == "POST":
		data.text = request.form['text']
		data.text_en = request.form['text_en']
		try:
			db.session.commit()
			return redirect('/officer/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("APIE_create.html",data=data, current_user=current_user(), bg_img=get_bg_img())
	
	

	
#============================ Comision ============================	
	
	
@app.route("/comision/")
def comision():
	try:
		data = Comision.query.get_or_404(1)
	except:
		data = Comision()
		data.text = "Teksto nėra adminas turi pridėti"
		data.text_en = "Admin have to add text"
		db.session.add(data)
		db.session.commit()
	#data.text = data.text.replace(" ","&nbsp")
	#data.text_en = data.text_en.replace(" ","&nbsp")
	return render_template("Comision.html", data=data, current_user=current_user(), bg_img=get_bg_img())
	

@app.route("/edit_comision/<int:id>", methods=["GET", "POST"])
def edit_comision(id):
	data = Comision.query.get_or_404(id)
	if request.method == "POST":
		data.text = request.form['text']
		data.text_en = request.form['text_en']
		try:
			db.session.commit()
			return redirect('/comision/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("APIE_create.html",data=data, current_user=current_user(), bg_img=get_bg_img())
	
	
	
	

	
#============================ Recruit ============================	
	
	
@app.route("/recruit/")
def recruit():
	try:
		data = Recruit.query.get_or_404(1)
	except:
		data = Recruit()
		data.text = "Teksto nėra adminas turi pridėti"
		data.text_en = "Admin have to add text"
		db.session.add(data)
		db.session.commit()
	#data.text = data.text.replace(" ","&nbsp")
	#data.text_en = data.text_en.replace(" ","&nbsp")
	return render_template("Recruit.html", data=data, current_user=current_user(), bg_img=get_bg_img())
	

@app.route("/edit_recruit/<int:id>", methods=["GET", "POST"])
def edit_recruit(id):
	data = Recruit.query.get_or_404(id)
	if request.method == "POST":
		data.text = request.form['text']
		data.text_en = request.form['text_en']
		try:
			db.session.commit()
			return redirect('/recruit/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("APIE_create.html",data=data, current_user=current_user(), bg_img=get_bg_img())
	
	
	
	
#============================ Purpose ============================	
	
	
@app.route("/purpose/")
def purpose():
	try:
		data = Purpose.query.get_or_404(1)
	except:
		data = Purpose()
		data.text = "Teksto nėra adminas turi pridėti"
		data.text_en = "Admin have to add text"
		db.session.add(data)
		db.session.commit()
	#data.text = data.text.replace(" ","&nbsp")
	#data.text_en = data.text_en.replace(" ","&nbsp")
	return render_template("Purpose.html", data=data, current_user=current_user(), bg_img=get_bg_img())
	

@app.route("/edit_purpose/<int:id>", methods=["GET", "POST"])
def edit_purpose(id):
	data = Purpose.query.get_or_404(id)
	if request.method == "POST":
		data.text = request.form['text']
		data.text_en = request.form['text_en']
		try:
			db.session.commit()
			return redirect('/purpose/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("APIE_create.html",data=data, current_user=current_user(), bg_img=get_bg_img())
	
	
	
	
#============================ dokumentai ============================	
def is_name_in_docs(name,docs):
	for doc in docs:
		if doc.name == name:
			return True
	return False

@app.route("/dokumentai/", methods=["GET", "POST"])
def documents():
	if request.method == "POST":
		docs = list(reversed(Document.query.order_by(Document.date_created).all()))
		file = request.files['file']
		if not is_name_in_docs(file.filename, docs):
			path = app.config['UPLOAD_DOCS'] + file.filename
			try:
				file.save(path)
			except:
				return "nepavyko issaugoti failo i vieta"
			try:
				documen = Document()
				documen.name = file.filename
				db.session.add(documen)
				db.session.commit()
			except:
				return "nepavyko issaugoti vardo i duomenu baze"
	docs = list(reversed(Document.query.order_by(Document.date_created).all()))
	return render_template("dokumentai.html",docs = docs, current_user=current_user(), bg_img=get_bg_img())	
	

@app.route('/download_document/<int:id>', methods=['GET', 'POST'])
def download_document(id):
	doc = Document.query.get_or_404(id)
	if len(doc.name)> 0:
		path =  app.config['UPLOAD_DOCS'] + doc.name
		return send_file(path, as_attachment=True)
	return redirect('/dokumentai/')
	
	

@app.route('/delete_document/<int:id>', methods=['GET', 'POST'])
def delete_document(id):
	doc = Document.query.get_or_404(id)
	try:
		try:
			path =  app.config['UPLOAD_DOCS'] + doc.name
			print(path)
			os.remove(path)
		except:pass
		db.session.delete(doc)
		db.session.commit()
		return redirect('/dokumentai/')
	except:
		return 'problema trinant dokumenta'
	
	
	
#============================ Galerija ============================	
	

	
@app.route('/galerija/', methods=['GET', 'POST'])
def galerija():
	if request.method == "POST":
		images = list(reversed(MyImage.query.order_by(MyImage.date_created).all()))
		file = request.files['file']
		if not is_name_in_docs(file.filename, images):
			path = app.config['UPLOAD_Images'] + file.filename
			try:
				file.save(path)
			except:
				return "nepavyko issaugoti failo i vieta"
			try:
				my_image = MyImage()
				my_image.name = "../" + app.config['UPLOAD_Images'] + file.filename
				db.session.add(my_image)
				db.session.commit()
			except:
				return "nepavyko issaugoti vardo i duomenu baze"
	images = list(reversed(MyImage.query.order_by(MyImage.date_created).all()))	
	return render_template("galerija.html",images = images, current_user=current_user(), bg_img=get_bg_img())	
	
	
	
@app.route('/delete_image/<int:id>', methods=['GET', 'POST'])
def delete_image(id):
	doc = MyImage.query.get_or_404(id)
	path =  doc.name[3:]
	try:
		try:
			os.remove(path)
		except:pass
		db.session.delete(doc)
		db.session.commit()
		return redirect('/galerija/')
	except:
		return 'problema trinant paveiksliuka'	
	

#============================ EPS ============================	
	
@app.route("/EPS/", methods=["GET", "POST"])
def documents_eps():
	docs = list(reversed(Document_EPS.query.order_by(Document_EPS.date_created).all()))
	return render_template("EPS.html",docs = docs, current_user=current_user(),bg_img=get_bg_img())	

@app.route("/create_EPS/", methods=["GET", "POST"])
def create_documents_eps():
	if request.method == "POST":
		docs = list(reversed(Document_EPS.query.order_by(Document_EPS.date_created).all()))
		file = request.files['file']
		name_lt = request.form['name_lt']
		name_en = request.form['name_en']
		link = request.form['link']
		if not is_name_in_docs(file.filename, docs):
			path = app.config['UPLOAD_DOCS'] + file.filename
			try:
				file.save(path)
			except:
				return "nepavyko issaugoti failo i vieta"
			try:
				documen = Document_EPS()
				documen.name = file.filename
				documen.name_en = name_en
				documen.name_lt = name_lt
				documen.URL = link
				db.session.add(documen)
				db.session.commit()
				return redirect('/EPS/')
			except:
				return "nepavyko issaugoti vardo i duomenu baze"
	return render_template("EPS_create.html", current_user=current_user(), bg_img=get_bg_img())


@app.route('/download_document_EPS/<int:id>', methods=['GET', 'POST'])
def download_document_eps(id):
	doc = Document_EPS.query.get_or_404(id)
	if len(doc.name)> 0:
		path =  app.config['UPLOAD_DOCS'] + doc.name
		return send_file(path, as_attachment=True)
	return redirect('/EPS/')
	
	

@app.route('/delete_document_EPS/<int:id>', methods=['GET', 'POST'])
def delete_document_eps(id):
	doc = Document_EPS.query.get_or_404(id)
	try:
		try:
			path =  app.config['UPLOAD_DOCS'] + doc.name
			print(path)
			os.remove(path)
		except:pass
		db.session.delete(doc)
		db.session.commit()
		return redirect('/EPS/')
	except:
		return 'problema trinant dokumenta'
	
#====================== TOP paveiksliukas ==============================

def delete_Topimg():
	doc = Topimg.query.get_or_404(1)
	try:
		os.remove(doc.name[3:])
	except:pass
	db.session.delete(doc)
	db.session.commit()
		
@app.route("/top_image/", methods=["GET", "POST"])
def top_image():
	if request.method == "POST":
		file = request.files['file']
		path = app.config['UPLOAD_BACKGROUND'] + file.filename
		try:
			file.save(path)
			imgs = list(reversed(Topimg.query.order_by(Topimg.date_created).all()))
			if len(imgs)>0:
				delete_Topimg()
		except:
			return "nepavyko issaugoti failo i vieta"
		try:
			img = Topimg()
			img.name = "../" + app.config['UPLOAD_BACKGROUND'] + file.filename
			db.session.add(img)
			db.session.commit()
			return redirect('/')
		except:
			return "nepavyko issaugoti vardo i duomenu baze"
	
	return render_template("topimg.html", current_user=current_user(), bg_img=get_bg_img())
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

	
if __name__=="__main__":
	app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
