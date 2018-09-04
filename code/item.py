import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import json


class Item(Resource):
    # 限制進來的arguments 必須有price 不得為空
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank")

    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {'item': item}, 200 if item is not None else 404
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"

        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}, "success": True}, 201
        return {"message": "Item not found", "success": False}, 404



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
