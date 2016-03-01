# Andela21-project an **An online store** *web app*
This online application enables users sign up in order to create their own onlines stores, edit posts well as share links with potential customers.
Developed using flask *web-framework* in python language

 ## Main features
 1.Create an online store
 2.Share links to products in ones store
 3.Edit your store
 4.Provide user authentication and password recovery options


NOTE: To gain access a user needs to sign up.

Alternatively, you can easily get a local copy of this application on your workstation. This guide assumes that you have a working installation of Python 3.4 and pip in your workstation

######Clone this repository

-$ git clone https://github.com/margierain/Andela21-project.git

######Install project dependencies via pip. It's recommended that you do this in a virtualenv

-$ pip install -r requirements.txt

######Initialize your development database.

-$ python runs.py db init

###### To construct the database and migrate the database models.

-$python runs.py db migrate
-$ python runs.py db upgrade

######Run the server.

-$ python runs.py runserver  

## Configurations
 
Incase your deploying this online store application the following environments have to set-up.

JOKENIA_ADMIN - 
JOKENIA_MAIL_SENDER - this is the one how sends users who sign up emails
SECRET_KEY -  this key generates the tokens generate by the CSRF as well as the authentication send to users who sign up 
JOKENIA_PASSWORD- this is the password for the Admin

## How the app works
As a new user your required to sign up then check your email for an access token sent by our team to give you access to use the application.Just incase the token  expires, you have an option to resend yourself a token.   
Once your authenticated your gmail gravatar as well as your email address will appear in your user profile pages. A user has options to reset their password as well as email incase they need to.
The create store form gives your option to input the product you want sell, a short and long description of the product. Go ahead, input the price and the picture of the product to increase your advertising appeal.

### Improvements needed
1. To add a cart functionality, so that when a user selects products it can be saved to their shopping bucket *cart*
2.Add a payment option so that actual purchase of goods can happen
3.Send emails to interested customer on new products added to ones store
4.Analysis user preferences so that user have a customized experience
5.Placing orders for goods that a customer, would  want to purchase but has not seen it in any store.


### Conclusion 
This is a practice web application that enabled me to put my skills on the runways as a learning process.