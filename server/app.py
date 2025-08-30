from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET/POST/PATCH/DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "id": bakery.id,
            "name": bakery.name,
        }
        bakeries.append(bakery_dict)

    response = make_response(
        jsonify(bakeries),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    
    if bakery:
        bakery_dict = {
            "id": bakery.id,
            "name": bakery.name,
        }
        response = make_response(
            jsonify(bakery_dict),
            200
        )
    else:
        response = make_response(
            jsonify({"error": "Bakery not found"}),
            404
        )
    
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    
    if not bakery:
        response = make_response(
            jsonify({"error": "Bakery not found"}),
            404
        )
        response.headers["Content-Type"] = "application/json"
        return response
    
    # Update bakery name from form data
    if 'name' in request.form:
        bakery.name = request.form['name']
    
    db.session.commit()
    
    bakery_dict = {
        "id": bakery.id,
        "name": bakery.name,
    }
    
    response = make_response(
        jsonify(bakery_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/baked_goods')
def baked_goods():
    baked_goods = []
    for baked_good in BakedGood.query.all():
        baked_good_dict = {
            "id": baked_good.id,
            "name": baked_good.name,
            "price": baked_good.price,
            "bakery_id": baked_good.bakery_id,
        }
        baked_goods.append(baked_good_dict)

    response = make_response(
        jsonify(baked_goods),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    # Create new baked good from form data
    new_baked_good = BakedGood(
        name=request.form.get('name'),
        price=request.form.get('price'),
        bakery_id=request.form.get('bakery_id')
    )
    
    db.session.add(new_baked_good)
    db.session.commit()
    
    baked_good_dict = {
        "id": new_baked_good.id,
        "name": new_baked_good.name,
        "price": new_baked_good.price,
        "bakery_id": new_baked_good.bakery_id,
    }
    
    response = make_response(
        jsonify(baked_good_dict),
        201
    )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/baked_goods/<int:id>')
def baked_good_by_id(id):
    baked_good = BakedGood.query.filter(BakedGood.id == id).first()
    
    if baked_good:
        baked_good_dict = {
            "id": baked_good.id,
            "name": baked_good.name,
            "price": baked_good.price,
            "bakery_id": baked_good.bakery_id,
        }
        response = make_response(
            jsonify(baked_good_dict),
            200
        )
    else:
        response = make_response(
            jsonify({"error": "Baked good not found"}),
            404
        )
    
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.filter(BakedGood.id == id).first()
    
    if not baked_good:
        response = make_response(
            jsonify({"error": "Baked good not found"}),
            404
        )
        response.headers["Content-Type"] = "application/json"
        return response
    
    db.session.delete(baked_good)
    db.session.commit()
    
    response = make_response(
        jsonify({"message": "Baked good deleted successfully"}),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)