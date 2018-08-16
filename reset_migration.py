from flaskblog.app import db
from flaskblog.models import *

if __name__=='__main__':
    db.drop_all()
    db.create_all()