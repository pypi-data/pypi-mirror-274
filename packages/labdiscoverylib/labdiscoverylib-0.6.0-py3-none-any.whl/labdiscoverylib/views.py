# Copyright 2023 onwards LabsLand Experimentia S.L.U.
# This software is licensed under the GNU AGPL v3:
# GNU Affero General Public License version 3 (see the file LICENSE)
# Read in the documentation about the license

import json
import time
import datetime
import traceback

from flask import Blueprint, Response, current_app, jsonify, request, url_for

from labdiscoverylib.exc import NotFoundError
from labdiscoverylib.config import ConfigurationKeys
from labdiscoverylib.utils import create_token, _to_timestamp, _current_backend, _current_weblab
from labdiscoverylib.users import CurrentUser, _set_weblab_user_cache
from labdiscoverylib.ops import status_time, update_weblab_user_data, dispose_user

weblab_blueprint = Blueprint("weblab", __name__) # pylint: disable=invalid-name

@weblab_blueprint.before_request
def _require_http_credentials():
    """
    All methods coming from WebLab-Deusto must be authenticated (except for /api). Here, it is used the
    WEBLAB_USERNAME and WEBLAB_PASSWORD configuration variables, which are used by WebLab-Deusto.
    Take into account that this username and password authenticate the WebLab-Deusto system, not the user.
    For example, a WebLab-Deusto in institution A might have 'institutionA' as WEBLAB_USERNAME and some
    randomly generated password as WEBLAB_PASSWORD.
    """
    # Don't require credentials in /api
    if request.url.endswith('/api'):
        return None

    auth = request.authorization
    if auth:
        provided_username = auth.username
        provided_password = auth.password
    else:
        provided_username = provided_password = None

    expected_username = current_app.config[ConfigurationKeys.WEBLAB_USERNAME]
    expected_password = current_app.config[ConfigurationKeys.WEBLAB_PASSWORD]
    if provided_username != expected_username or provided_password != expected_password:
        if request.url.endswith('/test'):
            error_message = "Invalid credentials: no username provided"
            if provided_username:
                error_message = "Invalid credentials: wrong username provided. Check the lab logs for further information."
            return Response(json.dumps(dict(valid=False, error_messages=[error_message])), status=401, headers={'WWW-Authenticate':'Basic realm="Login Required"', 'Content-Type': 'application/json'})

        if expected_username:
            current_app.logger.warning("Invalid credentials provided to access {}. Username provided: {!r} (expected: {!r})".format(request.url, provided_username, expected_username))

        return Response(response=("You don't seem to be a WebLab-Instance"), status=401, headers={'WWW-Authenticate':'Basic realm="Login Required"'})

    return None



@weblab_blueprint.route("/sessions/api")
def _api_version():
    """
    Just return the api version as defined. If in the future we support new features, they will fall under new API versions. If the report version is 1, it will only consume whatever was provided in version 1.
    """
    return jsonify(api_version="1")



@weblab_blueprint.route("/sessions/test")
def _test():
    """
    Just return that the settings are right. For example, if the password was incorrect, then something else will fail
    """
    return jsonify(valid=True)



@weblab_blueprint.route("/sessions/", methods=['POST'])
def _start_session():
    """
    Create a new session: WebLab-Deusto is telling us that a new user is coming. We register the user in the backend system.
    """
    request_data = request.get_json(force=True)
    return jsonify(**_process_start_request(request_data))

def _process_start_request(request_data):
    """ 
    Auxiliar method, called also from the Flask CLI to fake_user.

    The expected request_data looks like this:

    {
        'request': {
            'locale': 'en',
            'ldeReservationId': 'Zyv24cnaOqWXnZVO2v3hdQdrIxBC66BM9VM1EUFCBqM',
            'user': {
                # User data
            },
            'server': {
                # Server data
            },
            'backUrl': "http://...", # wherever we have to redirect the user after
        },
        'laboratory': {
            'name': "My lab",
            'category': "My category", # Optional
        },
        'user': {
            'username': "john", # Not guaranteed to be unique
            'unique': "john@labsland",
            'fullName': "John Smith", # Optional
        },
        'schedule': {
            'start': "2023-12-06T23:13:58.076302+00:00",
            'length': 298, # seconds left after that start
        }
    }

    """
    client_initial_data = request_data['request'].get('user')
    server_initial_data = request_data['request'].get('server')

    # Parse the initial date + assigned time to know the maximum time
    start_date = datetime.datetime.fromisoformat(request_data['schedule']['start'])
    slot_length = float(request_data['schedule']['length'])
    max_date = start_date + datetime.timedelta(seconds=slot_length)
    locale = request_data['request'].get('locale', 'en')
    full_name = request_data['user'].get('fullName')
    username = request_data['user']['username']
    username_unique = request_data['user']['unique']

    experiment_name = request_data['laboratory']['name']
    category_name = request_data['laboratory'].get('category')
    if category_name:
        experiment_id = '{}@{}'.format(experiment_name, category_name)
    else:
        experiment_id = experiment_name

    back_url = request_data['request']['backUrl']

    # Create a global session
    session_id = create_token()


    # Prepare adding this to backend
    user = CurrentUser(session_id=session_id, back=back_url,
                       last_poll=datetime.datetime.now(datetime.timezone.utc),
                       max_date=max_date,
                       username=username,
                       username_unique=username_unique,
                       exited=False, data={}, locale=locale,
                       full_name=full_name, experiment_name=experiment_name,
                       experiment_id=experiment_id, category_name=category_name,
                       request_client_data=client_initial_data,
                       request_server_data=server_initial_data,
                       start_date=start_date)

    backend = _current_backend()

    backend.add_user(session_id, user, expiration=30 + int(float(slot_length)))


    kwargs = {}
    scheme = current_app.config.get(ConfigurationKeys.WEBLAB_SCHEME)
    if scheme:
        kwargs['_scheme'] = scheme

    weblab = _current_weblab()
    if weblab._on_start:
        _set_weblab_user_cache(user)
        weblab._set_session_id(session_id)
        try:
            data = weblab._on_start(client_initial_data, server_initial_data)
        except Exception as error:
            traceback.print_exc()
            current_app.logger.warning("Error calling _on_start: {}".format(error), exc_info=True)
            try:
                dispose_user(session_id, waiting=True)
            except Exception as nested_error:
                traceback.print_exc()
                current_app.logger.warning("Error calling _on_dispose after _on_start failed: {}".format(nested_error), exc_info=True)

            return dict(error=True, message="Error initializing laboratory")
        else:
            if data:
                user.data = data
            user.data.store_if_modified()
            update_weblab_user_data(response=None)

    link = url_for('weblab_callback_url', session_id=session_id, _external=True, **kwargs)
    return dict(url=link, session_id=session_id)



@weblab_blueprint.route('/sessions/<session_id>/status')
def _status(session_id):
    """
    This method provides the current status of a particular
    user.
    """
    return jsonify(should_finish=status_time(session_id))

@weblab_blueprint.route('/sessions/status/multiple', methods=['POST'])
def _multiple_status():
    """
    This method provides the current status of a bulk of
    users.
    """
    t0 = time.time()

    request_data = request.get_json(silent=True, force=True)
    if request_data is None or request_data.get('session_ids') is None:
        return jsonify(success=False, error_code='missing-parameters', error_human="session_ids expected in POST JSON")

    # If the user passes a 'timeout' which is a float, calculate the
    # future timeout, which is the moment when this method should stop
    # processing requests.
    try:
        timeout = float(request_data.get('timeout'))
        future_timeout = t0 + timeout
        if future_timeout <= t0:
            future_timeout = None
    except:
        future_timeout = None

    status = {
        # session_id: status
    }

    for session_id in request_data['session_ids']:
        status[session_id] = status_time(session_id)

        if future_timeout is not None and time.time() > future_timeout:
            # Do not process more requests, timeout happened
            break

    return jsonify(status=status)


@weblab_blueprint.route('/sessions/<session_id>', methods=['POST', 'DELETE'])
def _dispose_experiment(session_id):
    """
    This method is called to kick one user out. This may happen
    when an administrator defines so, or when the assigned time
    is over.
    """
    if request.method == 'POST':
        request_data = request.get_json(force=True)
        if 'action' not in request_data:
            return jsonify(message="Unknown op")

        if request_data['action'] != 'delete':
            return jsonify(message="Unknown op")

    try:
        dispose_user(session_id, waiting=True)
    except NotFoundError:
        return jsonify(message="Not found")

    return jsonify(message="Deleted")
