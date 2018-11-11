from flask import Flask, render_template, redirect
# import mongo lib
import pymongo
from scrape import scrape_data

# Flask Setup
app = Flask(__name__)

#mongodb setup
conn = 'mongodb://localhost:27017'
# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)
db = client.mars_scrape_db
db.latest.drop()
#scrape()
@app.route("/")
def index():
	try:
		latest_data = db.latest.find_one()
	except Exception as e:
		print(e)

	return render_template('index.html', mars_data=latest_data)

@app.route('/scrape')
def scrape():
	try:
		mdata = db.latest
		data = scrape_data()
		mdata.delete_many({"planet":"mars"})
		mdata.insert_one(data)
	except Exception as e:
		print(e)

	return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)