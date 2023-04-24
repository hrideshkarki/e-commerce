# print('this is working')

# # THIS WILL GO IN ROUTES.PY
# import requests as r
# from flask import jsonify
# # Not sure if we need these:
# import os
# PRODUCT_API_KEY  = os.environ.get('PRODUCT_API_KEY ')

# # @app.route('/products')
# # def products_page():
# #     # note at end of this we add the pageSize=20
# #     #url = f'https://newsapi.org/v2/everything?q=tesla&from=2023-03-18&sortBy=publishedAt&apiKey={NEWS_API_KEY}&pageSize=20'
    
# #     response = r.get(url)
# #     data = response.json()
# #     articles = []
# #     # in the JSON it says that status should be 'ok', written in the JSON file
# #     if data['status'] == 'ok':
# #         articles = data['articles']
# #     return render_template('products.html', articles=articles)

# # in the API blueprint
# @app.route('/api/<string:product_name>')
# def get_product_info(product_name):
#     # Your code to retrieve product info from the Genius API goes here
#     response = r.get('https://api.genius.com/search', headers={'Authorization': 'Bearer PRODUCT_API_KEY'}, params={'q': product_name})
#     product_info = response.json()
    
#     # instead of data = response.json()
#     return jsonify(product_info)

# #this is the API

# import requests
# import json

# # set up the request parameters
# params = {
#   'api_key': 'C8FA965A8F6D4DDCB9FAC8BC1A5A2B52',
#   'type': 'bestsellers',
#   'url': 'https://www.amazon.com/s/zgbs/pc/516866'
# }

# # make the http GET request to Rainforest API
# api_result = requests.get('https://api.rainforestapi.com/request', params)

# # print the JSON response from Rainforest API
# print(json.dumps(api_result.json()))



# {% extends 'base.html' %}

# {% block content %}
# <div class="container mt-5">
#   <h1>Products Page</h1>
#   <div class="dropdown">
#     <a class="btn btn-secondary dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-bs-toggle="dropdown" aria-expanded="false">
#       View By Department
#     </a>
#     <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink">
#       <li><a class="dropdown-item" href="/products">All Departments</a></li>
#       {% for dept in departments_list%}
#       <li><a class="dropdown-item" href="/products/{{dept}}">{{dept}}</a></li>
#       {% endfor %}
#     </ul>
#   </div>
#   <div class="row justify-content-center">
#     {% for p in products %}
#     <div class="col-md-4 mb-3">
#       <div class="card border-0" style="border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
#         <a href="/product/{{p.id}}"> 
#           <img src="{{p.image}}" class="card-img-top" alt="...">
#         </a>
#         <div class="card-body">
#           <h5 class="card-title" style="height: 40px; overflow: hidden;">{{p.title}}</h5>
#           <p class="card-text">${{p.price}}</p>
#           <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#productModal{{p.id}}">
#             Read more
#           </button>
#         </div>
#       </div>
#     </div>
#     <!-- Product Modal -->
#     <div class="modal fade" id="productModal{{p.id}}" tabindex="-1" aria-labelledby="productModalLabel{{p.id}}" aria-hidden="true">
#       <div class="modal-dialog">
#         <div class="modal-content">
#           <div class="modal-header">
#             <h5 class="modal-title" id="productModalLabel{{p.id}}">{{p.title}}</h5>
#             <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
#           </div>
#           <div class="modal-body">
#             <img src="{{p.image}}" class="img-fluid mb-3" alt="{{p.title}}">
#             <p>{{p.description}}</p>
#             <p class="text-muted"><small>SKU: {{p.sku}}</small></p>
#             <p><b>Price: ${{p.price}}</b></p>
#           </div>
#         </div>
#       </div>
#     </div>
#     {% endfor %}
#   </div>
# </div>
# {% endblock %}
