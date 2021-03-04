from flask import Flask, request, redirect, render_template
import scrape_mars
import pymongo


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db
collection = db.items

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'

#scrape_data = {}


@app.route('/')
def index():
    if  collection.count() == 0 or  collection.find() == []:
        return render_template('index.html')

    scrape_data = collection.find().sort("_id",-1).limit(1)[0]
    featured_image_url = scrape_data['featured_img']
    news_title = scrape_data['title']
    news_p = scrape_data['paragraph']
    table_headers = enumerate(scrape_data['table_headers'])
    table_content = scrape_data['table_content']
    hemisphere_image_urls = scrape_data['hemisphere_image_urls']

    return render_template('index.html', hemisphere_image_urls = hemisphere_image_urls,  featured_image_url = featured_image_url, news_p=news_p, news_title=news_title, table_content= table_content, table_headers = table_headers)

@app.route('/scrape', methods = ['GET'])
def scrape():
    collection.insert_one(scrape_mars.scrape())
    return redirect('/')

"""

@app.route('/hello/<user>')
def hello_name(user):
   return render_template('hello.html', name = user)

@app.route('/hello/<int:score>')
def hello_name(score):
   return render_template('hello.html', marks = score)


@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)

"""

if __name__ == '__main__':
    app.run(debug=True)
