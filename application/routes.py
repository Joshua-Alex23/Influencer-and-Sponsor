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
        niche = [camp.niche for camp in campaign]
        #niche_len = [len(camp.niche for camp in campaign)]
        users = User.query.all()
        user_id = [user.id for user in users]
        inf = Influencer.query.count()
        print(inf)
        spo = Sponsor.query.count()
        #print(campaign)
        
        session['username'] = user.username
        session['Role'] = user.role[0].name

        #Displaying campaign for sponsor
        # if session['Role'] == 'Sponsor':
        #     user = session['username']
        #     get_user = User.query.filter_by(username = user).first()
        #     userid = get_user.id
        #     getspons = Sponsor.query.filter_by(user_id = userid).first()
        #     spons_id = getspons.id
        #     camps = Campaign.query.filter_by(sponsor_id = userid).first()
        #     #posts = Campaign.query.filter_by(sponsor_id = camps).all()
        # else:
        #     pass


        


        #if session['username'] == 'admin' and session['Role'] == 'admin' and :

        flash('Login Successful!')
        if session['Role'] == 'Influencer':
             return render_template('inf_home.html', campaign = campaign) #Campaign = camp
        if session['Role'] == 'Sponsor':
            return render_template('spo_home.html', campaign = campaign) #spons_id = spons_id
        else:
            return redirect(url_for('admin_home'))
@app.route('/home_page')
def home_page():
    return render_template('home.html')   

@app.route('/admin_home')
def admin_home():

        campaign = Campaign.query.all()
        niche = [camp.niche for camp in campaign]
        #niche_len = [len(camp.niche for camp in campaign)]
        users = User.query.all()
        user_id = [user.id for user in users]
        inf = Influencer.query.count()
        print(inf)
        spo = Sponsor.query.count()
        return render_template('admin_home.html',campaign = campaign, user_id = user_id, niche = niche, inf = int(inf), spo = int(spo))

@app.route('/inf_home')
def inf_home():
    campaign = Campaign.query.all()
    return render_template('inf_home.html', campaign = campaign)

# @app.route('/inf_update', methods = ['GET', 'POST'])
# def inf_update(id):
#     if request.method == 'GET':
#         name = session['username']
#         user = User.query.filter_by(username = name).first()
#         userid = user.id
#         inf = Influencer.query.filter_by(user_id = id).first()
#         #user = User.query.get(id)
        

#         return render_template('inf_update.html',
#                                 data_name = name, 
#                                 user_id = user.id,
#                                 data_email = user.email,
#                                 niche = inf.niche, 
#                                 industry = inf.industry,
#                                 platform = inf.platform_preference,
#                                 reach = inf.reach,
#                                 following = inf.following)
#     if request.method == 'POST':
#         name = session['username']
#         user = User.query.filter_by(username = name).first()
#         userid = user.id
#         #need to add rest of the details from user column
#         filled_username = request.form['username']
#         filled_password = request.form['password']
#         confirm_password = request.form['confirm_password']
#         filled_email = request.form['email']
#         filled_dob = request.form['dob']
#         filled_address = request.form['address']
#         filled_city = request.form['city']
#         filled_state = request.form['state']
#         filled_country = request.form['country']

#         if not filled_username or not filled_password or not filled_email:
#             flash('Please enter username, password and email')
#             return redirect(url_for('inf_update'))

#         if len(filled_password) < 8:
#             flash('Password must be at least 8 characters')
#             return redirect(url_for('inf_update'))
        
#         if filled_password != confirm_password:
#             flash('Passwords do not match')
#             return redirect(url_for('inf_update'))
        
#         user = User.query.filter_by(username=filled_username).first()
#         if user:
#             flash('User already exists')
#             return redirect(url_for('inf_update'))
        
#         user = User.query.filter_by(email=filled_email).first()
#         if user:
#             flash('Email already exists')
#             return redirect(url_for('inf_update'))

#         filled_dob = datetime.strptime(filled_dob, '%Y-%m-%d')

#         if filled_username:
#             user.username = filled_username
#         if filled_password:
#             user.password = filled_password
#         if filled_email:
#             user.email = filled_email
#         if filled_dob:
#             user.dob = filled_dob
#         if filled_address:
#             user.address = filled_address
#         if filled_city:
#             user.city = filled_city
#         if filled_state:
#             user.state = filled_state
#         if filled_country:
#             user.country = filled_country

        


#         #role ask if necessary if doing the registration pages individually

#         update_user = User(username = filled_username, password=filled_password, email=filled_email, dob = filled_dob, address = filled_address, city = filled_city, state = filled_state, country = filled_country)
#         #db.session.update(update_user)
#         db.session.commit()
#         flash('Profile Updated Successfully!')
#         return redirect(url_for('inf_home'))

@app.route('/spo_home')
def spo_home():
    sponsors = Sponsor.query.all()
    campaign = Campaign.query.all()
    return render_template('spo_home.html',sponsors = sponsors, campaign = campaign)

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

        return redirect(url_for('spo_home')) #spons_id = sponsid

@app.route('/ad_request')  #View Influencers from Sponsor
def ad_request():
        #Sponsor ID
    user = session['username']
    get_user = User.query.filter_by(username = user).first()
    userid = get_user.id
    getspons_id = Sponsor.query.filter_by(user_id = userid).first()
    spons_id = getspons_id
    #get Influencer data
    inf = Influencer.query.all()

    return render_template('ad_request.html', influencer = inf)

@app.route('/send_request_inf/<int:id>/', methods=['GET', 'POST'])
def send_request_inf(id):
    if request.method == 'GET':
        inf = Influencer.query.get(id)
        inf_id = inf.id
        user = session['username']
        get_user = User.query.filter_by(username = user).first()
        userid = get_user.id
        spo = Sponsor.query.filter_by(user_id = userid).first()
        spo_id = spo.id
        camp = Campaign.query.filter_by(sponsor_id = spo_id).all()
        return render_template('send_request_inf.html', inf_id = inf_id,
                                                        inf_name = inf.name,
                                                        userid = userid, 
                                                        spo_id = spo_id,
                                                        campaigns = camp)
    if request.method == 'POST':
        campaign_id = request.form['campaign_id']
        message = request.form['message']
        deliverables = request.form['deliverables']
        payment = request.form['payment']
        status = request.form['status']
        inf = Influencer.query.get(id)
        inf_id = inf.id
        user = session['username']
        get_user = User.query.filter_by(username = user).first()
        userid = get_user.id
        spo = Sponsor.query.filter_by(user_id = userid).first()
        spo_id = spo.id

        if not message or not deliverables or not payment or not status:
            flash('Please enter all details')
            return redirect(url_for('send_request_inf'))
        
        newrequests = AdRequest(campaign_id = campaign_id,
                                sponsor_id =spo_id,
                                Influencer_id = inf_id,
                                message = message,
                                deliverables = deliverables,
                                payment = payment,
                                status = status)
        db.session.add(newrequests)
        db.session.commit()
        flash('Request sent successfully!')
        return redirect(url_for('spo_home'))



@app.route('/send_request/<int:id>/', methods=['GET', 'POST']) # Send Requests from Influencer to Sponsor
def send_request(id):
    if request.method == 'GET':
        if session['Role'] == 'Influencer':  #remove this
            camp = Campaign.query.get(id)
            getspons = camp.sponsor_id
            user = session['username']
            get_user = User.query.filter_by(username=user).first()
            userid=get_user.id
            inf = Influencer.query.filter_by(user_id = userid).first()
            inf_id = inf.id
            inf_name = inf.name
            spo = Sponsor.query.get(getspons)
            return render_template('send_request.html',
                                spo_name = spo.name,
                                spo_id = spo.id,  
                                camp_id = camp.id, 
                                campaign = camp.name_of_campaign, 
                                camp_desc = camp.description, 
                                camp_budget = camp.Budget, 
                                inf_id = inf_id, 
                                inf_name = inf_name)

    if request.method == 'POST':
        message = request.form['message']
        deliverables = request.form['deliverables']
        payment = request.form['payment']
        status = request.form['status']

        camp = Campaign.query.get(id)
        getspons = camp.sponsor_id
        user = session['username']
        get_user = User.query.filter_by(username=user).first()
        userid=get_user.id
        inf = Influencer.query.filter_by(user_id = userid).first()
        inf_id = inf.id
        inf_name = inf.name
        spo = Sponsor.query.get(getspons)
        
        if not message or not deliverables or not payment or not status:
            flash('Please enter all details')
            return redirect(url_for('send_request'))
        newrequests = AdRequest(campaign_id = camp.id,
                                sponsor_id =getspons,
                                Influencer_id = inf_id,
                                message = message,
                                deliverables = deliverables,
                                payment = payment,
                                status = status)
        db.session.add(newrequests)
        db.session.commit()
        flash('Request sent successfully!')
        return redirect(url_for('inf_home'))



@app.route('/edit_campaign/<int:id>/', methods = ['GET', 'POST'])
def edit_campaign(id):#change this to spons_id similar to login
    
    if session['Role'] == Influencer:
        flash('You are not authorised to edit this Campaign')
        return redirect(url_for('inf_home')) #check home_page
    if request.method == 'GET':
        campaign = Campaign.query.get(id)
        if not campaign: 
            flash('Campaign not found')
            return redirect(url_for('spo_home'))
        #print(camp)
        return render_template('edit_campaign.html',campaign = campaign)
    
    if request.method == 'POST':
        campaign = Campaign.query.get(id)
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
            return redirect(url_for('spo_home'))
        if name_of_campaign:
            campaign.name_of_cammpaign = name_of_campaign
        if description:
            campaign.description = description
        if budget:
            campaign.Budget = budget
        if start_date:
            campaign.start_date = start_date
        if end_date:
            campaign.end_date = end_date
        if niche:
            campaign.niche = niche
        if visibility:
            campaign.visibility = visibility
        
        db.session.commit()
        #print(id)
        flash('Campaign updated succesfully')
        return redirect(url_for('spo_home'))
    
@app.route('/campaign_details/<int:id>/', methods = ['GET'])
def campaign_details(id):#change this to spons_id similar to login
    if request.method == 'GET':
        campaign = Campaign.query.get(id)
        if not campaign: 
            flash('Campaign not found')
            return redirect(url_for('spo_home'))
        #print(camp)
        return render_template('campaign_details.html',campaign = campaign)


@app.route('/delete_campaign/<int:id>')
def delete_campaign(id):
    if session['Role'] =='Influencer':
        flash('You are not authorized to delete product')
        return redirect(url_for('spo_home'))
    
    campaign = Campaign.query.get(id)
    if not campaign:
        flash('Campaign not found')
        return redirect(url_for('spo_home'))
    
    db.session.delete(campaign)  
    db.session.commit()
    flash('Campaign deleted successfully')
    if session['Role'] == 'Sponsor':
        return redirect(url_for('spo_home'))
    if session["Role"] == 'admin':
        return redirect(url_for('admin_home'))





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