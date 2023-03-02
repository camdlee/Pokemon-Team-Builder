
# ----- Imports ------
import os

#------ Config -----
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REGISTERED_USERS = {
        'dylank@thieves.com': {
            'name': 'Dylan',
            'password': 'ilovemydog'
            },
        'christian@thieves.com': {
            'name': 'Christian',
            'password': 'test123'
        },
        'devin@thieves.com': {
            'name': 'Devin',
            'password': 'Password'
        },
        'cameron@thieves.com': {
            'name': 'Cameron',
            'password': 'Thieves-110'
        }
    }