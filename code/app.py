from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList



import json

app = Flask(__name__)
app.secret_key = 'mao'
api = Api(app)

jwt_config = {
    'JWT_AUTH_URL_RULE': '/login'
    # 'JWT_EXPIRATION_DELTA': timedelta(days=1)
}

app.config.update(jwt_config)

jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')



app.run(port=5000, debug=True)



