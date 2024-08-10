from application.database import db
from datetime import date
class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    dob = db.Column(db.DATE, nullable = True)
    address = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    country = db.Column(db.String(80))

    role = db.relationship('Role', secondary = 'user_role' )


    def __repr__(self):
        return f'<User {self.username}'


class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(80), nullable = False, unique = True)
    description = db.Column(db.String(225), nullable = False)


    def __repr__(self):
        return f'<Role {self.name}'


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(80), db.ForeignKey(User.username))# does it have quotes?
    role = db.Column(db.Integer, db.ForeignKey(Role.id))#ask rohit if its role.id or role.name


    def __repr__(self):
        return f'<UserRole {self.id}'

class Niche(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    #niche = db.relationship('Campaign', backref='Niche', lazy=True)

    def __repr__(self):
        return f'<Niche {self.name}>' 


class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(225), db.ForeignKey(User.username))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    industry = db.Column(db.String(80), nullable = False)
    niche = db.Column(db.String(80), nullable = False)
    #niche_name = db.Column(db.String(80), db.ForeignKey(Niche.name)) #ask if niche name or id is better!!!!!
    platform_preference = db.Column(db.String(80), nullable = False)
    reach = db.Column(db.Integer, nullable = False)
    following = db.Column(db.Integer, nullable = False)
    email_id = db.Column(db.String(225), db.ForeignKey(User.email))

    
    def __repr__(self):
        return f'<Influencer {self.name}>'
    


class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(225), db.ForeignKey(User.username))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    industry = db.Column(db.String(80), nullable = False)
    email_id = db.Column(db.String(225), db.ForeignKey(User.email))
    budget = db.Column(db.Integer,nullable = False)
    industry_description = db.Column(db.String(200))
    
    
    category = db.relationship('Campaign', backref='sponsor', lazy=True)


    def __repr__(self):
         return f'<Sponsor {self.name}>'
    def __repr__(self):
        return f'{self.user_id}'
    def __repr__(self):
        return f'{self.id}'



class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey(Sponsor.id))
    name_of_campaign = db.Column(db.String(225), nullable = False)
    description = db.Column(db.String(330), nullable = False)
    Budget = db.Column(db.Integer, nullable = False)
    start_date = db.Column(db.Date, nullable = False, default = date.today())
    end_date = db.Column(db.Date, nullable = False )#continue the date command here
    niche = db.Column(db.String(225), nullable = False)
    visibility = db.Column(db.String(40),nullable = False)#Public or Private

    
    
    def __repr__(self):
        return f'<Campaign {self.name_of_campaign}>'
    def __repr__(self):
        return f'{self.sponsor_id}'

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    campaign_id = db.Column(db.Integer, db.ForeignKey(Campaign.id))
    sponsor_id = db.Column(db.Integer, db.ForeignKey(Sponsor.id))
    Influencer_id = db.Column(db.Integer, db.ForeignKey(Influencer.id)) #Change I to i
    message = db.Column(db.String(225), nullable = False)
    deliverables = db.Column(db.String(225), nullable = False)
    payment = db.Column(db.Integer, nullable = False)
    status = db.Column(db.String(80),nullable = False)#Pending or Accepted or Rejectet

    campaign = db.relationship('Campaign', backref='AdRequest', lazy=True) #Changing bacref from influencer to sponsor

    def __repr__(self):
        return f'<AdRequest: {self.request_type} _id_ {self.id}>'





