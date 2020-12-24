from app_module import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from xkcdpass import xkcd_password as xp

#TODO: secure
SALT = 'alwaysbeliveingold'

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    def is_anonymous(self):
        if self.username is None:
            return True
        return False

    def get_id(self):
        return self.username

    @property
    def password_hash(self):
        return db.users.find_one({'username':self.username})['password_hash']

    @property
    def name(self):
        return db.users.find_one({'username':self.username})['name']
    @property
    def message(self):
        return db.users.find_one({'username':self.username})['message']
    @property
    def signature(self):
        try:
            return db.users.find_one({'username':self.username})['signature']
        except:
            return 'From Simon'

    def set_password(self, password):
        password_hash = generate_password_hash(SALT+password)
        db.users.update({'username':self.username}, {'$set': {'password_hash': password_hash}})
    
    @staticmethod
    def generate_password(numwords=3):
        wordlist = xp.generate_wordlist(min_length=4, max_length=8)
        passlist = xp.first_upper_case(xp.generate_xkcdpassword(wordlist,numwords=numwords, delimiter=" ").split(" "))
        return ''.join(passlist)
            
    def check_password(self, password):
        return check_password_hash(self.password_hash, SALT+password)

    def __repr(self):
        return f'<User {self.username}>'

@login.user_loader
def load_user(username):
    u = db.users.find_one({"username": username})
    if not u:
        return None
    return User(username=u['username'])
