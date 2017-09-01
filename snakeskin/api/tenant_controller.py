from flask import current_app as app
from flask import Blueprint, jsonify

from snakeskin.api.errors import ResourceNotFoundError
from snakeskin.models.tenant import Tenant


tenant = Blueprint('tenant', __name__, url_prefix='/api/tenant')

@tenant.route('/')
def show_tenants():
    tenants = Tenant.query.all()
    return jsonify([t.short_profile() for t in tenants])

@tenant.route('/<tenant_id>')
def show_tenant_profile(tenant_id):
    tenant = Tenant.query.filter_by(id=tenant_id).first()
    if tenant is None:
        app.logger.error('The requested tenant {} could not be found.'.format(tenant_id))
        raise ResourceNotFoundError('The requested tenant could not be found.')

    return jsonify(tenant.full_profile())
