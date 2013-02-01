#!flask/bin/python
import urllib
import urllib2
import sys
from BeautifulSoup import BeautifulSoup
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models, hooks

urldata = 'http://map.crossfit.com/js/cfaffmapdata.js'
request_object = urllib2.Request(urldata)
response = urllib2.urlopen(request_object)
html_string = response.read()

count = 0
for value in ((html_string.split("[")[1]).split("]")[0]).split(",") :
        if (count % 3) == 0:
            aff_id = value
            print aff_id
            url = "http://map.crossfit.com/affinfo.php"
            post_data_dictionary = {'a':"%s" % aff_id, "t":"0"}
            post_data_encoded = urllib.urlencode(post_data_dictionary)
            request_object = urllib2.Request(url, post_data_encoded)
            response = urllib2.urlopen(request_object)
            html_string = response.read()
            soup = BeautifulSoup(html_string)

            try:
                website = soup.find('a').get('href')
                affiliate = soup.find('a').getText()
            except:
                website = ""
                affiliate = ""

            text = soup.findAll('br')

            if not affiliate:
                affiliate = text[0].previousSibling.getText()   
            address1 = text[0].nextSibling
            address2 = text[1].nextSibling
            full_address = "%s %s" % (address1,address2)
            full_address = full_address.encode('ascii', 'ignore')
            phone = text[2].nextSibling

            print "Affiliate: %s" % affiliate
            print "Website: %s" % website
            print "Address: %s %s" % (address1,address2)
            print "Phone: %s" % phone

        if (count % 3) == 1:
            cordx = value
            print "CordX: %s" % cordx

        if (count % 3) == 2:
            cordy = value
            print "CordY: %s" % (cordy)
            u = models.Affiliate(id=aff_id, name=affiliate, website=website, phone=phone, address=full_address, latitude=cordx, longitude=cordy)
            db.session.add(u)
            db.session.commit()

        count += 1
