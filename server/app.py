from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    messages=Message.query.order_by(Message.created_at.desc()).all()
    return jsonify([m.to_dict() for m in messages])
@app.route('/messages',methods=['POST'])
def post_messages():
    data=request.get_json()
    body=data.get('body')
    username=data.get('username')
    new_message=Message(body=body,username=username)
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict())

@app.route('/messages/<int:id>',methods=['PATCH'])
def update_by_id(id):
    data=request.get_json()
    body=data.get("body")
    message=Message.query.filter(Message.id==id).first()
    message.body=body
    db.session.commit()
    return jsonify(message.to_dict())


@app.route('/messages/<int:id>',methods=['DELETE'])
def delete_by_id(id):
    message=Message.query.filter(Message.id==id).first()
    db.session.delete(message)
    db.session.commit()
    return ''

if __name__ == '__main__':
    app.run(port=5555)
