print('this is working')

# THIS WILL GO IN ROUTES.PY
import requests as r
from flask import jsonify
# Not sure if we need these:
import os
PRODUCT_API_KEY  = os.environ.get('PRODUCT_API_KEY ')

# @app.route('/products')
# def products_page():
#     # note at end of this we add the pageSize=20
#     #url = f'https://newsapi.org/v2/everything?q=tesla&from=2023-03-18&sortBy=publishedAt&apiKey={NEWS_API_KEY}&pageSize=20'
    
#     response = r.get(url)
#     data = response.json()
#     articles = []
#     # in the JSON it says that status should be 'ok', written in the JSON file
#     if data['status'] == 'ok':
#         articles = data['articles']
#     return render_template('products.html', articles=articles)

# in the API blueprint
@app.route('/api/<string:product_name>')
def get_product_info(product_name):
    # Your code to retrieve product info from the Genius API goes here
    response = r.get('https://api.genius.com/search', headers={'Authorization': 'Bearer PRODUCT_API_KEY'}, params={'q': product_name})
    product_info = response.json()
    
    # instead of data = response.json()
    return jsonify(product_info)