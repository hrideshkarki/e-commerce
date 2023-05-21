from . import api
from ..models import Product
from ..apiauthhelper import token_auth
from flask import request

@api.get('/cart')
@token_auth.login_required
def getCartAPI():
    cart = token_auth.current_user().products

    return {
        'status':'ok',
        'results':len(cart),
        'products_in_cart': [prod.to_dict() for prod in cart]
    }

@api.post('/add-to-cart/<int:product_id>')
@token_auth.login_required 
def addToCartAPI(product_id):
    product = Product.query.get(product_id)
    if product: 
        if product in token_auth.current_user().products: 
            return {
                'status':'not ok',
                'message':'This product is already in your cart.'
            }
        else: 
            token_auth.current_user().add_to_cart(product)
            return {
                'status': 'ok',
                'message': 'Successfully added the item to your cart.',
                'product': product.to_dict(),
                'products_in_cart':[prod.to_dict() for prod in token_auth.current_user().products]
            }

    else: 
        return {
            'status':'not ok',
            'message':'This product does not exist'
        }

@api.delete('/remove-from-cart/<int:product_id>')
@token_auth.login_required
def removeFromCartAPI(product_id):
    product = Product.query.get(product_id)
    if product:
        if product in token_auth.current_user().products:
            token_auth.current_user().remove_from_cart(product)
            return {
                'status':'ok',
                'message':'Sucessfully removed item from cart.',
                'product_removed': product.to_dict(),
                'products_in_cart':[prod.to_dict() for prod in token_auth.current_user().products]
            }
        else:
           return {
                'status':'not ok',
                'message':'This product is not in your cart.'
            } 
    else:
        return {
            'status':'not ok',
            'message':'This product does not exist.'
        }
    
@api.delete('/empty-cart')
@token_auth.login_required
def emptyCartAPI():
    if token_auth.current_user().products:
        token_auth.current_user().empty_cart()
        return {
                'status':'ok',
                'message':'Your cart is empty now'
            }
    else:
        return {
            'status':'not ok',
            'message':'Cart already empty'
        }

@api.get('/item-in-cart/<int:product_id>')
@token_auth.login_required
def isItemInCartAPI(product_id):
    if token_auth.current_user().products:
        product = Product.query.get(product_id)
        if product:
            if product in token_auth.current_user().products:
                return {
                    'status':'ok', 
                    'in_cart':'true',
                    'message':'The item is in the cart.'
                    }
            else:
                return {
                    'status':'ok', 
                    'in_cart':'false',
                    'message':'The item is not in the cart.'
                    }
        else:
            return {
            'status':'not ok',
            'message':'This product is out of stock'
        }
    else:
        return {
            'status':'ok', 
            'in_cart':'false',
            'message':'Your cart looks empty.'
        }