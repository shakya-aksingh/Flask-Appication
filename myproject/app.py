from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required

from user import UserRegister
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'mysecretkey'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot to be left!")

    # Authentication for getting particular item from the items
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
        '''for item in items:
            if item['name'] == name:
                return item
        return {'message': 'Item not found'},404'''

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name {} already exists.".format(name)}, 40

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        # filter the given name from the items
        items = list(filter(lambda x: x['name'] != name, items))
        return {"message": "Item Deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True)
