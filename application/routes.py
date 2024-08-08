from flask import Flask, render_template, request, flash, url_for, redirect, session
from main import app
from datetime import date, datetime 
from application.model import *

@app.route('/')
def index():
    return render_template('home_page.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Please enter the Username and Password')
            return redirect(url_for('login'))
        
        if len(password) < 8:
            flash('Password must be longer than 8 characters')
            return redirect(url_for('login'))
        # chars = ['!','@','*','1','2','3','4','5','6','7','8','9','0'] Work on logic
        # if chars not in password: #
        #     flash('Password must contain at least one special character and number')
        #     return redirect(url_for('login'))

        user = User.query.filter_by(username = username).first()

        if not user:   
            flash('User not found, please create an account')
            return redirect(url_for('login'))
        #print(password,user.password, password == user.password)
        if password != user.password:
            flash('Password is incorrect, please check')
            return redirect(url_for('login'))
        campaign = Campaign.query.all()
        #print(campaign)
        
        session['username'] = user.username
        session['Role'] = user.role[0].name

        #Displaying campaign for sponsor
        if session['Role'] == 'Sponsor':
            user = session['username']
            get_user = User.query.filter_by(username = user).first()
            userid = get_user.id
            getspons = Sponsor.query.filter_by(user_id = userid).first()
            spons_id = getspons.id
            camps = Campaign.query.filter_by(sponsor_id = userid).first()
            #posts = Campaign.query.filter_by(sponsor_id = camps).all()
        else:
            pass





        #if session['username'] == 'admin' and session['Role'] == 'admin' and :

        flash('Login Successful!')
        if session['Role'] == 'Influencer':
             return render_template('inf_home.html', campaign = campaign) #Campaign = camp
        if session['Role'] == 'Sponsor':
            return render_template('spo_home.html', campaign = campaign, spons_id = spons_id)
        else:
            return render_template('admin_home.html')
@app.route('/home_page')
def home_page():
    return render_template('home.html')   

@app.route('/inf_home')
def inf_home():
    return render_template('inf_home.html')

@app.route('/spo_home')
def spo_home():
    return render_template('spo_home.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('Role', None)
    flash('You have been successfully logged out!')
    return redirect(url_for('home_page'))

@app.route('/register', methods= ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        filled_username = request.form['username']
        filled_password = request.form['password']
        confirm_password = request.form['confirm_password']
        filled_email = request.form['email']
        filled_dob = request.form['dob']
        filled_address = request.form['address']
        filled_city = request.form['city']
        filled_state = request.form['state']
        filled_country = request.form['country']
        filled_role = request.form['role']

        if not filled_username or not filled_password or not filled_email or not filled_role:
            flash('Please enter username, password, email and role')
            return redirect(url_for('register'))

        if len(filled_password) < 8:
            flash('Password must be at least 8 characters')
            return redirect(url_for('register'))
        
        if filled_password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        if filled_role not in ['admin', 'Influencer', 'Sponsor']:
            flash('Invalid role')
            return redirect(url_for('register'))
        
        user = User.query.filter_by(username=filled_username).first()
        if user:
            flash('User already exists')
            return redirect(url_for('register'))
        
        user = User.query.filter_by(email=filled_email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('register'))

        filled_dob = datetime.strptime(filled_dob, '%Y-%m-%d')


        #role ask if necessary if doing the registration pages individually

        filled_role = Role.query.filter_by(name=filled_role).first()
        new_user = User(username = filled_username, password=filled_password, email=filled_email, dob = filled_dob, address = filled_address, city = filled_city, state = filled_state, country = filled_country, role = [filled_role])
        db.session.add(new_user)
        db.session.commit()
        get_user = User.query.filter_by(username = filled_username).first()
        
        if filled_role.name == 'Influencer':
            return render_template('register_inf.html', data_name = get_user.username, data_id = get_user.id, data_email = get_user.email)
        if filled_role.name == 'Sponsor':
            return render_template('register_spo.html', data_name = get_user.username, data_id = get_user.id, data_email = get_user.email)
    
# @app.route('/register/<int:id>',methods= ['GET','POST'])
# def choose(id):
#     if request.method == 'GET':
#         return render_template('choose.html',id = id)
#     #if request.method == 'POST':


@app.route('/register_inf', methods= ['GET','POST']) #continue to query user_id from previous step
def register_inf():
    if request.method == 'GET':
        return render_template('register_inf.html')
    if request.method == 'POST':
        industry = request.form['industry']
        niche = request.form['niche']
        platform_preference = request.form['platform_preference']
        reach = request.form['reach']
        following = request.form['following']
        username = request.form['username']
        id = request.form['id']
        email_id = request.form['email_id']
        
        
        new_inf =Influencer(industry = industry, niche = niche, platform_preference = platform_preference, reach = reach, following = following,name = username, user_id = id, email_id = email_id)
        db.session.add(new_inf)
        db.session.commit()
        flash('Influencer Profile created successfully, please continue to login')
        return redirect(url_for('home_page'))
            #role ask if necessary if doing the registration pages individually


@app.route('/register_spo', methods= ['GET','POST'])
def register_spo():
    if request.method == 'GET':
        return render_template('register_spo.html')
    if request.method == 'POST':
        industry = request.form['industry']
        budget = request.form['budget']
        industry_description = request.form['industry_description']
        username = request.form['username']
        id = request.form['id']
        email_id = request.form['email_id'] 
        
        new_spo = Sponsor(industry = industry, budget = budget, industry_description = industry_description, name = username, user_id = id, email_id = email_id)
        db.session.add(new_spo)
        db.session.commit()
        flash('Sponsor Profile created successfully, please continue to login')
        return redirect(url_for('home_page'))
        #role ask if necessary if doing the registration pages individually

@app.route('/add_campaign', methods=['GET', 'POST'])
def add_campaign():
    if request.method == 'GET':
        user = session['username']
        get_user = User.query.filter_by(username=user).first()
        userid=get_user.id
        get_spons=Sponsor.query.filter_by(user_id=userid).first()
        sponsid = get_spons.id
        spons_name = get_spons.name
        return render_template('add_campaign.html', spons_name = spons_name)
    if request.method == 'POST':
        name_of_campaign = request.form['name_of_campaign']
        description = request.form['description']
        budget = request.form['budget']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        niche = request.form['niche']
        visibility = request.form['visibility']
        #sponsor_id = request.form['sponsor_id']

        # need to add verification of data and role.
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        if not name_of_campaign or not description or not budget or not start_date or not end_date or not niche or not visibility:
            flash('Please enter all details')
            return redirect(url_for('add_campaign'))
        if session['Role']=='Sponsor':
            user = session['username']
            get_user = User.query.filter_by(username=user).first()
            userid=get_user.id
            get_spons=Sponsor.query.filter_by(user_id=userid).first()
            sponsid = get_spons.id
            spons_name = get_spons.name
            
        

        campaign = Campaign(name_of_campaign = name_of_campaign, description = description, Budget = budget, start_date = start_date, end_date = end_date, niche = niche, visibility = visibility, sponsor_id = sponsid )
        db.session.add(campaign)
        db.session.commit()
        flash('Campaign has been created.')
        return render_template('spo_home.html')
    # if visibility == 'Public':
    #     return render_template('spo_home.html', spons_name = spons_name)
    # if visibility == 'Private':
    #     return render_template('spo_home.html', data_name = get_spons.name)

@app.route('/ad_request', methods = ['GET', 'POST'])
def ad_request():
    if request.method == 'GET':
        #Sponsor ID
        user = session['username']
        get_user = User.query.filter_by(username = user).first()
        userid = get_user.id
        getspons_id = Sponsor.query.filter_by(user_id = userid).first()
        spons_id = getspons_id
        
        #Influencer ID
        # user = session['username']
        # get_user = User.query.filter_by(username = user).first()
        # userid = get_user.id
        # getinf_id = Influencer.query.filter_by(user_id = userid).first()
        # inf_id = getinf_id

        # #Campaign ID
        # user = session['username']
        # get_user = User.query.filter_by(username = user).first()
        # userid = get_user.id
        # getcamp_id = Campaign.query.filter_by(id = userid).first()
        # camp_id = getcamp_id.id

        return render_template('ad_request.html', spons_id = spons_id)
    if request.method == 'POST':
        message= request.form['message']
        deliverables = request.form['deliverables']
        payment = request.form['payment']
        status = request.form['status']

        #Sponsor ID
        user = session['username']
        get_user = User.query.filter_by(username = user).first()
        userid = get_user.id
        getspons_id = Sponsor.query.filter_by(user_id = userid).first()
        spons_id = getspons_id.id
        
        #Influencer ID




        if not message or not deliverables or not payment or not status:
            return redirect(url_for('ad_request'))
        new_ad_request = AdRequest(message = message, deliverables = deliverables, payment = payment, status = status)
        db.session.add(new_ad_request)
        db.session.commit()
        return render_template('home.html')
    
@app.route('/edit_campaign/<int:spons_id>', methods = ['GET', 'POST'])
def edit_campaign(spons_id):#change this to spons_id similar to login
    
    if session['Role'] == Influencer:
        flash('You are not authorised to edit this Campaign')
        return redirect(url_for('index')) #check home_page
    if request.method == 'GET':
        camp = Campaign.query.get(spons_id) # select with respect to sponsor id
        camp_id = Campaign.query.filter_by()
        if not camp: 
            flash('Campaign not found')
            return redirect(url_for('spo_home'))
        return render_template('edit_campaign.html',camp = camp)
    
    if request.method == 'POST':
        campaign =Campaign.query.get(id)
        name_of_campaign = request.form['name_of_campaign']
        description = request.form['description']
        budget = request.form['budget']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        niche = request.form['niche']
        visibility = request.form['visibility']
        #sponsor_id = request.form['sponsor_id']
        print(campaign)
        # need to add verification of data and role.
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        if not name_of_campaign or not description or not budget or not start_date or not end_date or not niche or not visibility:
            flash('Please enter all details')
            return redirect(url_for('add_campaign'))
        if name_of_campaign:
            campaign.name_of_cammpaign = name_of_campaign
        if description:
            campaign.description = description
        if budget:
            campaign.budget = budget
        if start_date:
            campaign.start_date = start_date
        if end_date:
            campaign.end_date = end_date
        if niche:
            campaign.niche = niche
        if visibility:
            campaign.visibility = visibility
        
        db.session.commit()
        flash('Campaign updated succesfully')
        return redirect(url_for(spo_home))
    
    
@app.route('/delete_campaign/<int:id>')
def delete_product(id):
    if session['Role'] =='Influencer':
        flash('You are not authorized to delete product')
        return redirect(url_for('index'))
    
    campaign = Campaign.query.get(id)
    if not campaign:
        flash('Campaign not found')
        return redirect(url_for('index'))
    
    db.session.delete(campaign)  
    db.session.commit()
    flash('Campaign deleted successfully')
    return redirect(url_for('index'))

@app.route('/view_requests', methods=['GET', 'POST'])
def viewrequests():
    if request.method == 'GET':
        if 'Role' in session and session['Role'] != 'Influencer':
            requests = AdRequest.query.filter_by(status='pending').all()
            return render_template('requests.html',requests = requests) # check landing page
       
        if 'Role' in session and session['role'] == 'store_manager':
            requests = AdRequest.query.filter_by(requester=session['user']).all()
            return render_template('requests.html',requests = requests) #check landing page
        
@app.route('/approve_request/<int:id>')
def approve_request(id):
    request = AdRequest.query.get(id)

    request = AdRequest.query.filter_by(name=request.id).first()
    if request:
        request.status = 'rejected'
        db.session.commit()
        return redirect(url_for('viewRequests'))
    request = AdRequest(name=request.id, description=request.message)
    try:
        db.session.add(request)
        request.status = 'approved'
        db.session.commit()
        flash('Ad Request Successfull')
        return redirect(url_for('viewRequests')) #check landing page
    except:
        flash('Error approving request')
        return redirect(url_for('viewRequests'))  # check landing page