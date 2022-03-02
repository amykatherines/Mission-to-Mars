# use Flask to render a template, redirecting to another url, and creating a URL.
from flask import Flask, render_template, redirect, url_for
# use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo
# to use the scraping code, convert from Jupyter notebook to Python.
import scraping


# Setup flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# tells Python that the app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# This URI is saying that the app can reach Mongo through our 
# localhost server, using port 27017, using a database named "mars_app"
mongo = PyMongo(app)

# tells Flask what to display when we're looking at the home page, index.html 
# (index.html is the default HTML file that we'll use to display the content we've scraped)
@app.route("/")

# This function is what links our visual representation of our work, our web app, to the code that powers it.
def index():
   # uses PyMongo to find the "mars" collection in our database, assign the path "mars" to a variable
   mars = mongo.db.mars.find_one()

   # "return render_template("index.html" tells Flask to return an HTML template using an index.html file
   # ", mars=mars"  tells Python to use the "mars" collection in MongoDB.
   return render_template("index.html", mars=mars)

# will set up our scraping route. This route will be the "button" of the web application, the one that 
# will scrape updated data when we tell it to from the homepage of our web app. 
# It'll be tied to a button that will run the code when it's clicked.
@app.route("/scrape")

def scrape():

   # assign a new variable that points to our Mongo database
   mars = mongo.db.mars

   # create a new variable to hold the newly scraped data
   # In this line, we're referencing the scrape_all function in the 
   # scraping.py file exported from Jupyter Notebook.
   mars_data = scraping.scrape_all()

   # Now that we've gathered new data, we need to update the database using .update_one()
   # Here, we're inserting data, but not if an identical record already exists. In the query_parameter, we can specify a field 
   # (e.g. {"news_title": "Mars Landing Successful"}), in which case MongoDB 
   # will update a document with a matching news_title. 
   # Or it can be left empty ({}) to update the first matching document in the collection
   # we'll use the data we have stored in mars_data. The syntax used here is {"$set": data}. 
   # This means that the document will be modified ("$set") with the data in question.
   # the option we'll include is upsert=True. This indicates to Mongo to 
   # create a new document if one doesn't already exist, 
   # and new data will always be saved (even if we haven't already created a document for it)
   mars.update_one({}, {"$set":mars_data}, upsert=True)

   # add a redirect after successfully scraping the data: return redirect('/', code=302). 
   # This will navigate our page back to / where we can see the updated content.
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()