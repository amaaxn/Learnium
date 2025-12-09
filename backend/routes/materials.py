from flask import Blueprint

materials_bp = Blueprint("materials", __name__)

@materials_bp.route("", methods=["GET"])
def list_materials():
    return {"message": "not implemented yet"}