__author__ = "miller.tim"
__date__ = "$Mar 27, 2017 7:24:42 PM$"

#Custom Modules
from seeclickfix import postSCFix, getLocation, updateSCFix
from classes import Cleanup, User, getBase, getEngine

#Requires Flask, SQLAlchemy, json, and geopy
from flask import Flask, render_template, request, flash
from flask import session, redirect, url_for
from flask_login import LoginManager, login_user, login_required
from flask_login import logout_user, current_user
from sqlalchemy.orm import sessionmaker
import json
import geopy

CITY = "Oakland, Ca" #Oakland hard coded as city used later in geopy

#Pull SQL functions from 'classes' module
Base = getBase()
Engine = getEngine()

#Create SQL Session
Base.metadata.bind = Engine
DBSession = sessionmaker(bind = Engine)
DBSession.bind=Engine
session = DBSession()

#Create Flask App
app = Flask(__name__)
app.secret_key = ''

#Manage Login Feature
login_manager=LoginManager()
login_manager.init_app(app)

#Home Page
#'Section' is the name of the page in the tab
@app.route('/')
def welcome():
    return render_template("home_page.html", 
            section = 'Home')

#Error Page
#HTML was never fully built
@app.route('/error')
def error():    
    return render_template('error_display.html',
            section = "Error")

#Function automaticially triggered when user tries to
#access controlled page, without loggin in.
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template("unauthorized.html")   
            
#Module mandated by Flask to look up user
@login_manager.user_loader
def user_loader(username):
    user = session.query(User).filter(User.username==username).first()
    return user

#Log users into webpage
@app.route('/login', methods=['GET','POST'])
def login():
    #pull from html form
    username = request.form['username']
    #Check Username exists
    if session.query(User).filter(User.username == username).count():
        #Get user account
        user = session.query(User).filter(User.username == username).first()
        #Check password against database
        if user.check_password(request.form['password']):
            user.authenticated=True
            session.add(user) #Reflect user authorization in SQL
            session.commit()
            login_user(user, remember=True) #Reflect user authorization in Flask
            return redirect(url_for('profile', username=username))        
        else:
            #Next step: require user feedback password or username incorrect
            return redirect(url_for("welcome"))
    else:
        #Next Step: require user feedback password or username incorrect            
        return redirect(url_for("welcome"))
    
#Logout of webpage
@app.route('/logout', methods=["GET"])
@login_required
def logout():
    #Danger of keeping users logged in that don't logout properly
    user = current_user
    user.authenticated=False #SQL update
    session.add(user)
    session.commit()
    logout_user() #Flask Update
    
    #Next Step: May be better to return to homepage
    return render_template("logout.html", 
            section="Log out")

#New Users input profile information
@app.route('/signup')
def signup():      
    return render_template("enter_user_data.html", 
            section="Sign up")  
            
#Profile page for a user
#Next Step: build in protection from other users
#Next Step: Create ability to show notifications
@app.route('/profile/<username>')
@login_required
def profile(username):
    return render_template("user_profile.html", 
            username=username,
            section="Profile")
            
#Cleanups Hosted by a user            
@app.route('/hosted_cleanups')
@login_required
def view_hosted_cleanups():
    return render_template("hosted_cleanups.html", 
                            section="Hosted Cleanups")
                            
#Cleanups a user is participating in                            
@app.route('/participated_cleanups')
@login_required
def view_participated_cleanups():
    return render_template("participated_cleanups.html", 
                            section="Participated Cleanups")                            
            
#Take new user profile input and place it in SQL
##Next step: fields for optional inputs: i.e email and volunteer hours
@app.route('/create_account', methods=['POST'])
def create_account():
    #Pull data from html form
    new_name = request.form["username"]
    new_password = request.form["password"]
    new_confirm_password = request.form["confirm_password"]
    #Users can not use unavailable usernames
    if not session.query(User).filter(User.username == new_name).count():
        #Check unencrypted passwords match
        if new_password==new_confirm_password:
            #Create account and log in user
            new_user = User(username = new_name, password = new_password)
            new_user.hash_password() #Encrypt password
            new_user.authenticated=True #Login user to SQL
            session.add(new_user)
            session.commit()
            login_user(new_user, remember=True) #Login user to Flask
            return redirect(url_for('profile', username=new_name)) #Send to profile page
        else:
            #Next Step: feedback that passwords do not match
            return(redirect(url_for("signup")))    
    else:
        #Next Step: user feedback that username unavailble
        return(redirect(url_for("signup")))

##Page for each cleanup
#Gets cleanup id number from html link 
@app.route('/cleanup/<id>')
def cleanup(id):
    clean = session.query(Cleanup).filter(Cleanup.id == id).first()
    return render_template("cleanup.html", 
            section = "Cleanup", 
            clean = clean)
            
##Display all of the current Clean-ups
@app.route('/active_clean_ups')
def viewall_cleanup():
#    if session.query(Cleanup).count(): #commented out if/then is meant for when there are no cleanups
    cleans = session.query(Cleanup).all() #Look at all of the cleanups
    return render_template('viewall_cleanup.html', 
            section="Active Clean ups",
            cleans = cleans)
#    else:
#        #Replace with actual html 
#        return ("No Active Cleanups")


#Remove cleanup from the sql dataset
#Next Step: Notify participants that cleanup was canceled
@app.route('/delete_cleanup', methods=["POST"])
@login_required
def delete_cleanup():
    cleanup_id = request.form['delete_cleanup_id'] #HTML would only send variables through form. 
    cleanup = session.query(Cleanup).filter(Cleanup.id==cleanup_id).first() #Object needed to be pulled from SQL, based on variable
    #Users and cleanups are closley linked by host and participant foreign keys
    #First delete the cleanup from the user's hosting roster
    current_user.cleanups_hosted.remove(cleanup)
    #Then, remove all participants from cleanup
    cleanup.participants = []
    #Finally remove the cleanup from SQL
    session.delete(cleanup)
    session.commit()
    return redirect(url_for('viewall_cleanup'))

#The logged in user adds him/herself to a selected cleanup
@app.route('/join_cleanup', methods = ["POST"])
@login_required
def join_cleanup():
    cleanup_id = request.form['join_cleanup_id'] #HTML would only send variable
    cleanup = session.query(Cleanup).filter(Cleanup.id==cleanup_id).first() #From variable, find object from SQL
    cleanup.participants.append(current_user) #User is added via Many-to-Many SQL relationship
    session.add(cleanup)
    session.commit()
    return redirect(url_for('cleanup', id=cleanup.id))

##User inputs new Cleanup information
@app.route('/enter_cleanup_data')
@login_required
def enter_cleanup():
    return render_template('enter_cleanup_data.html', 
            section='Create Cleanup')

##Add Clean up
##Display the new clean-up data
@app.route('/create_cleanup', methods = ["POST"])
@login_required
def create_cleanup():
    #Pull from html form
    new_date = request.form["event_date"]
    new_time = request.form['event_time'] #Total hours found through arithmatic
    new_end_time = request.form['end_time']
    new_street_number=request.form['street_number'] #Next Step: Cross street based location
    new_street_name=request.form['street_name']
    new_image=request.form['event_image']
    location = getLocation(new_street_number, new_street_name, CITY) #Function lives in 'SeeClickFix' module. 
                                                                      #Uses geopy to find location
                                                                      #City is set at top of page
    #This point once held code to advertise on SeeClickFix immediately after creation
    #The code has since been move to a later stage in the process. However, remnants of the advertisements remain 
    new_cleanup = Cleanup(date=new_date,
                            start_time = new_time,
                            end_time = new_end_time,
                            street_number = new_street_number,
                            street_name = new_street_name,
                            image=new_image, 
                            host= current_user, 
                            lat = location.latitude,
                            lng = location.longitude,
                            address=location.address#,
                            #html_url = issue_url # SeeClick Fix Remnant 
                            )
    session.add(new_cleanup)
    session.commit()
    return render_template('create_cleanup.html', 
            section = "Confirm Cleanup",
            cleanup=new_cleanup,
            url = "https://test.seeclickfix.com/issues/1317339" #SeeClickFix Remnant
            )
            
#Post Clean-up to SeeClickFix.com            
@app.route('/advertise/<id>') #ID is from html href/link
@login_required
def advertise_cleanup(id):
    cleanup = session.query(Cleanup).filter(Cleanup.id==id).first()
    print("Lat: %f, Address: %s" % (cleanup.lat, cleanup.address)) #Sanity Check
    api_request = postSCFix(cleanup) #Function in SeeClickFix Module,interacts with SeeClickFix API
    response = api_request.json() #Contains Response from SeeClickFix
    issue_url = response['html_url'] #Important to distinguish site from api urls
    cleanup.html_url=issue_url #Add to SQL database
    session.add(cleanup)
    session.commit()
    return redirect(url_for('cleanup', id=id))
    
if __name__ == "__main__":
app.run()
