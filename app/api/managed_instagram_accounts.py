from flask import jsonify, request

from app.exceptions import ValidationError
from . import api
from .. import db
from ..models import ManagedInstagramAccount, ManagedInstagramAccountSchema

managed_instagram_account_schema = ManagedInstagramAccountSchema(session=db.session)


@api.route('/managed_instagram_accounts/')
def get_managed_instagram_accounts():
    managed_instagram_accounts = ManagedInstagramAccount.query.all()
    return jsonify({
        'managed_instagram_accounts': [managed_instagram_account_schema.dump(a) for a in managed_instagram_accounts],
    })


@api.route('/managed_instagram_accounts/<int:id>')
def get_managed_instagram_account(id):
    managed_instagram_account = ManagedInstagramAccount.query.get_or_404(id)
    return jsonify(managed_instagram_account_schema.dump(managed_instagram_account))


@api.route('/managed_instagram_accounts/', methods=['POST'])
def new_managed_instagram_account():
    try:
        managed_instagram_account = managed_instagram_account_schema.load(request.json)
    except Exception as err:
        raise ValidationError(str(err))

    if ManagedInstagramAccount.query.filter_by(handle=managed_instagram_account.handle).first():
        raise ValidationError('handle already registered.')
    db.session.add(managed_instagram_account)
    db.session.commit()
    return jsonify(managed_instagram_account_schema.dump(managed_instagram_account)), 201


@api.route('/managed_instagram_accounts/<int:id>', methods=['PATCH'])
def edit_managed_instagram_account(id):
    managed_instagram_account = ManagedInstagramAccount.query.get_or_404(id)
    try:
        for key, value in request.json.items():
            setattr(managed_instagram_account, key, value)
    except Exception as err:
        raise ValidationError(str(err))
    db.session.add(managed_instagram_account)
    db.session.commit()
    return jsonify(managed_instagram_account_schema.dump(managed_instagram_account))
