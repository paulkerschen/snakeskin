from flask import current_app as app
from flask import Blueprint, g, jsonify

from snakeskin.api.errors import ResourceNotFoundError
from snakeskin.models.user import User


user = Blueprint('user', __name__, url_prefix='/api/tenant/<tenant_id>/user/<external_id>')


@user.url_value_preprocessor
def fetch_user(endpoint, values):
    user = User.query.filter_by(tenant_id=values['tenant_id'], external_id=values['external_id']).first()
    if user is None:
        app.logger.error('The requested user {} could not be found.'.format(values['external_id']))
        raise ResourceNotFoundError('The requested user could not be found.')
    else:
        g.user = user

@user.route('/')
def show_user_profile(tenant_id, external_id):
    return jsonify({
        'tenant': g.user.tenant.short_profile(),
        'user': g.user.full_profile()
    })

@user.route('/data_sources')
def show_user_data_sources(tenant_id, external_id):
    result = g.user.get_data_sources()
    return jsonify(result)

@user.route('/recent_activities')
def show_user_recent_activities(tenant_id, external_id):
    result = g.user.get_recent_activities()
    return jsonify(result)

@user.route('/top_activities')
def show_user_top_activities(tenant_id, external_id):
    result = g.user.get_top_activities()
    return jsonify(result)

@user.route('/total_activities')
def show_user_total_activities(tenant_id, external_id):
    result = g.user.get_total_activities()
    return jsonify(result)
