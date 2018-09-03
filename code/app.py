from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required


from security import authenticate, identity
from user import UserRegister



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

items = []

class Item(Resource):
    # 限制進來的arguments 必須有price 不得為空
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank")
    
    # @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()
        item = {
            'name': data['name'],
            'price': data['price']
        }
        items.append(item)
        return json.dumps(items), 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        print(items)
        return {'message': 'item deleted'}

    def put(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        data = Item.parser.parse_args()
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
            return items
        else:
            item.update(data)
            return items


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')



app.run(port=5000, debug=True)



