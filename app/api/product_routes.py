from . import api
from ..models import Product
from ..apiauthhelper import token_auth
from flask import request


@api.get('/products')
def getProductsAPI(): 
    products = Product.query.all()
    return {
        'status':'ok',
        'results': len(products),
        'products': [p.to_dict() for p in products]
    }

@api.get('/products/<int:product_id>')
def getProductAPI( product_id):
    product = Product.query.get(product_id)
    if product:
        return {
            'status':'ok',
            'results': 1,
            'product': product.to_dict()
        }
    else:
        return {
            'status': 'not ok',
            'message': 'The product you are looking for does not exist'
        }, 404

# @api.product('/products/create')
# @token_auth.login_required
# def createProductAPI():
#     data = request.json
    
#     title = data['title']
#     img_url = data['img_url']
#     caption = data['caption'] 
#     #  i think this should be description

#     product = Product(title, img_url, caption, token_auth.current_user().id)

#     product.saveToDB()

            
#     return {
#         'status': 'ok',
#         'message': 'Succesfully found a product.',
#         'product': product.to_dict()
#     }, 201


@api.get('/productsq=<string:search_name>')
@api.get('/productsq=')
def getSearchedProductsAPI(search_name=''):
    if search_name.strip():
        products = Product.query.filter(Product.title.ilike("%" + search_name + "%")).all()
    else:
        products = Product.query.all()
    return {
        'status':'ok',
        'results':len(products),
        'products': [prod.to_dict() for prod in products]
    }

