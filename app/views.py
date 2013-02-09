from flask import render_template, flash, redirect, request
from flask.helpers import url_for
from app import app, db, models
from forms import ReviewForm
import datetime
from sqlalchemy import *
from flask_oauth import OAuth

FACEBOOK_APP_ID = '556465061044186'
FACEBOOK_APP_SECRET = 'c63a760215c2722f6abd3936c1f53d7d'
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/review/<affiliate_id>', methods = ['GET', 'POST'])
def review(affiliate_id=None):
    form = ReviewForm()
    a = models.Affiliate.query.get(affiliate_id)

    if form.validate_on_submit():
        try: 
            r = models.Review(affiliate_id=a.id, ipaddress=request.remote_addr, rating_overall=form.rating.data, rating_equipment=form.rating_equipment.data, rating_instructor=form.rating_instructor.data, comment=form.comment.data, review_date=datetime.datetime.utcnow())
            db.session.add(r)
            db.session.commit()
            flash("Review for %s has been posted!" % a.name, 'success')
            return redirect('/')
        except:
            db.session.rollback()
            flash('You only can post one review!', 'error')
    else: 
        if request.method == "POST":
            flash('Please make sure all fields are filled out correctly.', 'error')

    return render_template('review.html', 
        affiliate_info = a,
        form = form)

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

@app.route('/affiliate_details/<affiliate_id>', methods = ['GET'])
def affiliate_details(affiliate_id=None):
    affiliate_rating = 0
    final_rating = 0
    affiliate_reviews = (models.Review.query.filter_by(affiliate_id=affiliate_id)).order_by(models.Review.review_date.desc())
    if affiliate_reviews.count() > 0:
        for review in affiliate_reviews:
            affiliate_rating += review.rating_overall
        final_rating = (affiliate_rating / affiliate_reviews.count()) * 1.00

    else:
        final_rating = None
    affiliate_info = models.Affiliate.query.get(affiliate_id)

    return render_template('affiliate_details.html', affiliate_info=affiliate_info, affiliate_rating=final_rating, latest_review=affiliate_reviews.first(), total_reviews=affiliate_reviews.count())

@app.route('/gym/<affiliate_id>', methods = ['GET'])
@app.route('/gym/<affiliate_id>/<int:page>', methods = ['GET', 'POST'])
def gym(affiliate_id=None, page = 1):
    affiliate_rating = 0
    final_rating = 0
    affiliate_reviews = (models.Review.query.filter_by(affiliate_id=affiliate_id)).order_by(models.Review.review_date.desc())
    displayed_reviews = (models.Review.query.filter_by(affiliate_id=affiliate_id)).order_by(models.Review.review_date.desc()).paginate(page, 5, False)
    if affiliate_reviews.count() > 0:
        for review in affiliate_reviews:
            affiliate_rating += review.rating_overall
        final_rating = affiliate_rating / affiliate_reviews.count()

    else:
        final_rating = None
    affiliate_info = models.Affiliate.query.get(affiliate_id)

    return render_template('gym.html', affiliate_info=affiliate_info, affiliate_rating=final_rating, latest_review=affiliate_reviews.first(), total_reviews=affiliate_reviews.count(), reviews=displayed_reviews)
