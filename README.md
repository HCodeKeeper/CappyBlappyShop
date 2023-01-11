# CappyBlappyShop

## .env file structure:
```
SERVER_PORT = 
DOMAIN= 
STRIPE_API_SECRET_KEY=
DB_USER=
DB_PASSWORD=
DJANGO_SECRET_KEY=

EMAIL_HOST = 
EMAIL_PORT = 
EMAIL_HOST_USER = 
EMAIL_HOST_PASSWORD = 
```
## Running the project
run redis server
```
redis-server
```
run stripe listener
```
stripe listen --events checkout.session.completed --forward-to localhost:<your_port; default: 8000>/event/checkout_succeeded
```
run django server
