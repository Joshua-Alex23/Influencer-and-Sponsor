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
             return redirect(url_for('inf_home')) #Campaign = camp
        if session['Role'] == 'Sponsor':
            return redirect(url_for('spo_home')) #spons_id = spons_id
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

@app.route('/admin_campaign')
def admin_campaign():

        campaign = Campaign.query.all()
        niche = [camp.niche for camp in campaign]
        #niche_len = [len(camp.niche for camp in campaign)]
        users = User.query.all()
        user_id = [user.id for user in users]
        inf = Influencer.query.count()
        print(inf)
        spo = Sponsor.query.count()
        return render_template('admin_campaign.html',campaign = campaign, user_id = user_id, niche = niche, inf = int(inf), spo = int(spo))

@app.route('/admin_users')
def admin_users():
    users = User.query.all()
    inf = Influencer.query.all()
    spo = Sponsor.query.all()
    return render_template('admin_users.html', users = users)

@app.route('/inf_home')
def inf_home():
    campaign = Campaign.query.all()
    return render_template('inf_home.html', campaign = campaign)


@app.route('/inf_update', methods=['GET', 'POST'])
def inf_update():
    if request.method == 'GET':
        name = session['username']
        user = User.query.filter_by(username=name).first()
        userid = user.id
        inf = Influencer.query.filter_by(user_id=userid).first()

        return render_template('inf_update.html',
                               user = user,
                               data_name=name,
                               user_id=user.id,
                               data_email=user.email,
                               niche=inf.niche,
                               industry=inf.industry,
                               platform=inf.platform_preference,
                               reach=inf.reach,
                               following=inf.following)

    if request.method == 'POST':
        name = session['username']
        user = User.query.filter_by(username=name).first()
        userid = user.id
        inf = Influencer.query.filter_by(user_id=userid).first()

        # Retrieve form data
        filled_username = request.form['username']
        filled_password = request.form['password']
        confirm_password = request.form['confirm_password']
        filled_email = request.form['email']
        filled_dob = request.form['dob']
        filled_address = request.form['address']
        filled_city = request.form['city']
        filled_state = request.form['state']
        filled_country = request.form['country']
        filled_niche = request.form['niche']
        filled_industry = request.form['industry']
        filled_platform = request.form['platform_preference']
        filled_reach = request.form['reach']
        filled_following = request.form['following']

        # Validate the form inputs
        if not filled_username or not filled_password or not filled_email:
            flash('Please enter username, password, and email')
            return redirect(url_for('inf_update'))

        if len(filled_password) < 8:
            flash('Password must be at least 8 characters')
            return redirect(url_for('inf_update'))

        if filled_password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('inf_update'))

        if User.query.filter(User.username == filled_username, User.id != userid).first():
            flash('Username already exists')
            return redirect(url_for('inf_update'))

        if User.query.filter(User.email == filled_email, User.id != userid).first():
            flash('Email already exists')
            return redirect(url_for('inf_update'))

        filled_dob = datetime.strptime(filled_dob, '%Y-%m-%d')

        # Update User details
        user.username = filled_username
        user.password = filled_password
        user.email = filled_email
        user.dob = filled_dob
        user.address = filled_address
        user.city = filled_city
        user.state = filled_state
        user.country = filled_country

        # Update Influencer details
        inf.niche = filled_niche
        inf.industry = filled_industry
        inf.platform_preference = filled_platform
        inf.reach = filled_reach
        inf.following = filled_following

        # Commit changes to the database
        db.session.commit()

        flash('Profile Updated Successfully!')
        return redirect(url_for('inf_home'))

@app.route('/spo_home')
def spo_home():
    username = session['username']
    user = User.query.filter_by(username = username).first()
    user_id = user.id

    sponsor = Sponsor.query.filter_by(user_id = user_id).first()
    # sponsors = Sponsor.query.all()
    spo_id = sponsor.id
    campaign = Campaign.query.filter_by(sponsor_id = spo_id).all()
    print(spo_id)
    return render_template('spo_home.html', campaign = campaign,spo_id = spo_id)

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
        
        newrequests = AdRequest_inf(campaign_id = campaign_id,
                                    sponsor_id = spo_id,
                                    influencer_id = inf_id,
                                    message = message,
                                    deliverables = deliverables,
                                    payment = payment,
                                    status = status)# sponsor_id =spo_id,
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
        newrequests = AdRequest_spo(campaign_id = camp.id,
                                sponsor_id =getspons,
                                message = message,
                                deliverables = deliverables,
                                payment = payment,
                                status = status) 
        db.session.add(newrequests)
        db.session.commit()
        flash('Request sent successfully!')
        return redirect(url_for('inf_home'))
    

@app.route('/edit_request/<int:id>/', methods = ['GET', 'POST'])
def edit_request(id):
    if session['Role'] == Influencer:
        flash('You are not authorised to edit this Campaign')
        return redirect(url_for('inf_home'))
    if request.method == 'GET':
        requests = AdRequest_inf.query.get(id)
        inf_id = requests.influencer_id
        inf = Influencer.query.get(inf_id)
        camp_id = requests.campaign_id
        camp = Campaign.query.get(camp_id)
        camp_name = camp.name_of_campaign

        return render_template('edit_request.html', requests = requests, inf_name = inf.name, camp_name = camp_name)
    if request.method == 'POST':
        requests = AdRequest_inf.query.get(id)
        campaign_id = requests.campaign_id
        message = request.form['message']
        deliverables = request.form['deliverables']
        payment = request.form['payment']
        status = request.form['status']

        if not message or not deliverables or not payment or not status:
            flash('Please enter all details')
            return redirect(url_for('view_request_spo'))
        
        if campaign_id:
            requests.campaign_id = campaign_id
        if message:
            requests.message = message
        if deliverables:
            requests.deliverables = deliverables
        if payment:
            requests.payment = payment
        if status:
            requests.status = status
        
        db.session.commit()
        return render_template('view_requests_spo.html')
    

@app.route('/delete_request/<int:id>')
def delete_request(id):

    requests = AdRequest_inf.query.get(id)
    if not requests:
        flash('Campaign not found')
        return redirect(url_for('view_requests_spo'))
    
    db.session.delete(requests)  
    db.session.commit()
    return redirect(url_for('view_requests_spo'))

        

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
def campaign_details(id):
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
        if session['Role'] == 'Sponsor':
            return redirect(url_for('spo_home'))
        elif session["Role"] == 'admin':
            return redirect(url_for('admin_campaign'))
    
    db.session.delete(campaign)  
    db.session.commit()
    flash('Campaign deleted successfully')
    if session['Role'] == 'Sponsor':
        return redirect(url_for('spo_home'))
    elif session["Role"] == 'admin':
        return redirect(url_for('admin_campaign'))





@app.route('/view_requests', methods=['GET', 'POST'])
def view_requests():
    # if request.method == 'GET':
    #     requests = AdRequest.query.filter_by(status='pending').all()
    #     return render_template('view_requests.html',requests = requests) # check landing page
    if request.method == 'GET':
        user = session['username']
        get_user = User.query.filter_by(username=user).first()
        userid=get_user.id
            
        
        if session["Role"] == 'Influencer':
            inf = Influencer.query.filter_by(user_id = userid).first()
            inf_id = inf.id
            print(inf_id)
            requests = AdRequest_inf.query.filter(AdRequest_inf.influencer_id == inf_id, AdRequest_inf.status == 'pending').all()
            # camp_id = AdRequest_inf.query.get(AdRequest_inf.campaign_id) Do if time permits!!
            # camp = Campaign.query.get(camp_id)
            accepted = AdRequest_inf.query.filter(AdRequest_inf.influencer_id == inf_id, AdRequest_inf.status == 'approved').all()
            return render_template('view_requests_inf.html', requests=requests, accepted = accepted)
        elif session["Role"] == 'Sponsor':
            spo = Sponsor.query.filter_by(user_id = userid).first()
            spo_id = spo.id
            requests = AdRequest_spo.query.filter(AdRequest_spo.sponsor_id == spo_id, AdRequest_spo.status == 'pending').all()
            accepted = AdRequest_spo.query.filter(AdRequest_spo.sponsor_id == spo_id, AdRequest_spo.status == 'approved').all()
            sent = AdRequest_inf.query.filter(AdRequest_inf.sponsor_id == spo_id, AdRequest_inf.status == 'pending').all()
            return render_template('view_requests_spo.html', requests = requests, accepted = accepted, sent = sent)
        # else:
        #     pass
        #     # requests = []  # Or handle other roles or no role appropriately

        
@app.route('/view_requests_inf')
def view_requests_inf():
    return render_template('view_requests_inf.html')  

@app.route('/view_requests_spo')
def view_requests_spo():
    return render_template('view_requests_spo.html')   
  
@app.route('/approve_request/<int:id>', methods = ['GET', 'POST'])
def approve_request(id):
    if session['Role'] == 'Influencer':
        adrequest = AdRequest_inf.query.get(id)

        if adrequest:
            adrequest.status = 'approved'  # Update status to approved
            db.session.commit()
            flash('Request approved successfully', 'success')
            return redirect(url_for('view_requests_inf'))
        
    elif session['Role'] == 'Sponsor':
        adrequest = AdRequest_spo.query.get(id)

        if adrequest:
            adrequest.status = 'approved'  # Update status to approved
            db.session.commit()
            flash('Request approved successfully', 'success')
            return redirect(url_for('view_requests_spo'))


@app.route('/reject_request/<int:id>', methods = ['GET', 'POST'])
def reject_request(id):
    if session['Role'] == 'Influencer':
        adrequest = AdRequest_inf.query.get(id)

        if adrequest:
            adrequest.status = 'rejected'  # Update status to approved
            db.session.commit()
            flash('Request rejected')
            return redirect(url_for('view_requests_inf'))
    elif session['Role'] == 'Sponsor':
        adrequest = AdRequest_spo.query.get(id)

        if adrequest:
            adrequest.status = 'rejected'  # Update status to approved
            db.session.commit()
            flash('Request rejected')
            return redirect(url_for('view_requests_spo'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search', None)

        if not search_query:
            flash('Please enter a search keyword')
            if session['Role'] == 'Influencer':
                return redirect(url_for('inf_home'))
            elif session['Role'] == 'Sponsor':
                return redirect(url_for('spo_home'))
            elif session['Role'] == 'admin':
                return redirect(url_for('admin_home'))

        role = session['Role']
        username = session['username']
        user = User.query.filter_by(username = username).first()

        campaigns = []
        influencers = []

        # Filter based on role
        if role == 'Influencer':
            # Influencers can search for public campaigns
            campaigns = Campaign.query.filter(
                Campaign.name_of_campaign.ilike(f'%{search_query}%'),
                Campaign.visibility == "Public"
            ).all()
        elif role == 'Sponsor':
            # Sponsors can search their own campaigns
            sponsor = Sponsor.query.filter_by(user_id=user.id).first()
            if sponsor:
                campaigns = Campaign.query.filter(
                    Campaign.name_of_campaign.ilike(f'%{search_query}%'),
                    Campaign.sponsor_id == sponsor.id
                ).all()
        
        # If the admin role is included, they can search for both
        elif role == 'admin':
            campaigns = Campaign.query.filter(
                Campaign.name_of_campaign.ilike(f'%{search_query}%')
            ).all()
            influencers = Influencer.query.filter(
                Influencer.name.ilike(f'%{search_query}%')
            ).all()

        if not campaigns and not influencers:
            flash('No results found')
            if role == 'Influencer':
                return redirect(url_for('inf_home'))
            elif role == 'Sponsor':
                return redirect(url_for('spo_home'))
            elif role == 'admin':
                return redirect(url_for('admin_home'))

        return render_template('search.html', campaigns=campaigns, influencers=influencers, role=role)

    if session['Role'] == 'Influencer':
        return redirect(url_for('inf_home'))
    elif session['Role'] == 'Sponsor':
        return redirect(url_for('spo_home'))
    elif session['Role'] == 'admin':
        return redirect(url_for('admin_home'))


# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         search_query = request.form.get('search', None)
#         if not search_query:
#             flash('Please enter a search keyword')
#             if session['Role'] == 'Influencer':
#                 return redirect(url_for('inf_home'))
#             elif session['Role'] == 'Sponsor':
#                 return redirect(url_for('spo_home'))
#             elif session['Role'] == 'admin':
#                 return redirect(url_for('admin_home'))
        
        
#         campaigns = Campaign.query.filter(Campaign.name_of_campaign.ilike(f'%{search_query}%')).all()

#         influencers = Influencer.query.filter(Influencer.name.ilike(f'%{search_query}%')).all()
        
#         if not campaigns and not influencers:
#             flash('No results found')
#             if session['Role'] == 'Influencer':
#                 return redirect(url_for('inf_home'))
#             elif session['Role'] == 'Sponsor':
#                 return redirect(url_for('spo_home'))
#             elif session['Role'] == 'admin':
#                 return redirect(url_for('admin_home'))

#         role = session['Role']
#         return render_template('search.html', campaigns=campaigns, influencers=influencers, role = role)
#     if session['Role'] == 'Influencer':
#         return redirect(url_for('inf_home'))
#     elif session['Role'] == 'Sponsor':
#         return redirect(url_for('spo_home'))
#     elif session['Role'] == 'admin':
#         return redirect(url_for('admin_home'))

@app.route('/flag_user/<int:user_id>', methods=['POST'])
def flag_user(user_id):
    user = User.query.get(user_id)
    user.is_flagged = True
    db.session.commit()
    flash('User has been flagged.')
    return redirect(url_for('admin_users'))

@app.route('/flag_campaign/<int:id>/', methods=['POST'])
def flag_campaign(id):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        campaign = Campaign.query.get(id)
        campaign.is_flagged = True
        db.session.commit()
        flash('Campaign has been flagged.')
        return redirect(url_for('admin_campaign'))

@app.route('/unflag_campaign/<int:id>/', methods=['POST'])
def unflag_campaign(id):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        campaign = Campaign.query.get(id)
        campaign.is_flagged = False
        db.session.commit()
        flash('Campaign has been unflagged.')
        return redirect(url_for('admin_campaign'))

@app.route('/flag_users/<int:id>/', methods=['POST'])
def flag_users(id):
    if request.method == 'POST':
        user = User.query.get(id)
        user.is_flagged = True
        db.session.commit()
        flash('User has been flagged.')
        return redirect(url_for('admin_users'))
    
@app.route('/unflag_users/<int:id>/', methods=['POST'])
def unflag_users(id):
    if request.method == 'POST':
        user = User.query.get(id)
        user.is_flagged = False
        db.session.commit()
        flash('User has been unflagged.')
        return redirect(url_for('admin_users'))
    
@app.route('/delete_users/<int:id>/')
def delete_users(id):
    user = User.query.get(id)
    inf = Influencer.query.filter_by(user_id = id).first()
    spo = Sponsor.query.filter_by(user_id = id).first()
    if inf or spo:  # Check if either an influencer or sponsor exists
        if inf:
            db.session.delete(inf)
        if spo:
            db.session.delete(spo)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted')
    return redirect(url_for('admin_users'))
