from flask import Blueprint, jsonify, current_app, request, abort
from src.domain.date import DateModel
from werkzeug.exceptions import HTTPException
import json


# define the blueprint
blueprint_api = Blueprint(name="blueprint_api", import_name=__name__)

@blueprint_api.route('/<date>', methods=['GET'])
@blueprint_api.route('/')
def get_date_timestamp(date=''):
    date_input = DateModel(date)
    current_app.logger.info(f"[Route={request.url_rule} Param={date}")
    return jsonify(date_input.date_as_dict())


@blueprint_api.errorhandler(Exception)
def handle_exception(e):
    current_app.logger.info(f'Exception:{e}')
    return jsonify({'error': 'Invalid Date'})