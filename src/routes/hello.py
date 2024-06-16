from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

hello_blueprint = Blueprint("hello", __name__)

@hello_blueprint.route("/hello", methods=["GET"])
@jwt_required()
def hello():
  identity = get_jwt_identity()
  print(identity)
  print(identity["role"])
  return { "hello": "hello world" }