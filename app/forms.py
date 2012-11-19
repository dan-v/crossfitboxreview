from flask.ext.wtf import Form, TextField, RecaptchaField
from flask.ext.wtf import Required

class ReviewForm(Form):
    rating = TextField('rating', validators = [Required()])
    rating_equipment = TextField('rating_equipment', validators = [Required()])
    rating_instructor = TextField('rating_instructor', validators = [Required()])
    comment = TextField('comment', validators = [Required()])
    #recaptcha = RecaptchaField()
