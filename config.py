import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess123456789'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'mysql://root:passwd@localhost/boxreview'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
RECAPTCHA_PUBLIC_KEY = '6LeXPNkSAAAAAAo-eZu24VHqR3oXKkazQjTFtY_c'
RECAPTCHA_PRIVATE_KEY = '6LeXPNkSAAAAAPXk1Q5wRagfFS-fzZaldoYi6GgE'