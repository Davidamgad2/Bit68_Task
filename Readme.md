Thank you so much for this opportuinty!

I use python 3.10.6. Please note that the venv was ignored.

If you want to run it via cmd, you will need to install the file requirements.txt via pip install -r requirements.

Then python manage.py runserver

urls:
    register/: will be when you navigate to localhost:8000 you can register via email, name and password

    login/: is responsiple to give you token by entering your email and the password that you have registered earlier


    product/: will give you a list of product ordered by price

    product/search/: will give you results with the thing you search for. Please note that you will need send 'search' as key in parameters section while using the postman 


    cart/: will return to you the items that you have in cart
    
    cart/add/: will add the quantity and the item to the cart. Please note that you have two options you can send 'quantity' in the body with the 'id' of the product for example for the jason {"id":1,"quantity":2}. If you don't wish to send quantity it will by default add one. It will return a response with message done!


    place_order/: will take the current cart and add it to your orders and then remove the CART.

    myorders/: will get you all of your orders.


Please note that you can use login to get token and use it for authorization, or you can use email.

I added the secret key to .env and install decouple

Finally Thank you again for your time and your efforts! 