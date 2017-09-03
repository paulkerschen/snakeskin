from snakeskin.db import db
from snakeskin.models.base import Base
from snakeskin.proxies import canvas


"""
The `tenants` table tracks the top-level integrated environments which have data in the Learning Record Store.
A tenant incorporates a set of users, data sources, data consumers, and learning record statements.
Examples: "UC Berkeley", "Stanford", "UCB Test Data".

TODO This iniital sandbox-schema mixes the LRS Tenant model with a Canvas Data Source model. Instead, a given
Tenant might have multiple Canvas Data Sources, or have no designated Canvas Data Source at all. For example,
the "UC Berkeley QA" environment will contain only one User with an external ID of "211159", but LRS statements
referring to that QA-environment user may come from Beta, Test, or developer-specific Canvas instances, each
with its own unique LRS Credential.
"""
class Tenant(Base):
    __tablename__ = 'tenants'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    scheme = db.Column(db.String(255))
    domain = db.Column(db.String(255))
    token = db.Column(db.String(255))

    def __init__(self, name, scheme=None, domain=None, token=None):
        self.name = name
        self.scheme = scheme
        self.domain = domain
        self.token = token

    def __repr__(self):
        return '<Tenant %r>' % (self.name)

    def short_profile(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def full_profile(self):
        return {
            'id': self.id,
            'name': self.name,
            'users': [u.short_profile() for u in self.users]
        }

    def get_user_profile(self, user):
        response = canvas.get_user_for_sis_id(self, user.external_id)
        if response:
            return response.json()
        else:
            return None
