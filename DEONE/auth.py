import hmac, sha, base64
from datetime import datetime
import logging

TIMEFORMAT = "%a, %d %b %Y %H:%M:%S +0000"
SECRETKEY = 'deone_appspot'

def generate_auth(app3_user, app3_timestamp):
    """
    The timestamp format should be as specified in RFC 2822 and in UTC:
        "%a, %d %b %Y %H:%M:%S +0000"
        
    - See http://www.faqs.org/rfcs/rfc2822.html
    """
    message = "%s\n%s" % (app3_user, app3_timestamp)
    
    auth = hmac.new(
        key = SECRETKEY,
        msg = message,
        digestmod = sha,
    ).digest()
    
    return base64.encodestring(auth).strip()

def generate_timestamp():
    """
    Generates a timestamp in the standard format.
    """
    return datetime.utcnow().strftime(TIMEFORMAT)

def is_within_n_minutes(sent_time, n=15):
    """
    Check whether one of our timestamps is within n minutes of
    now. (All times are in UTC)
    """
    sent_time = datetime.strptime(sent_time, TIMEFORMAT)
    
    return not (datetime.utcnow() - sent_time).seconds >= n * 60
    
def is_authorized(request):
    #return True
    if ('App3-Timestamp' not in request.headers) or ('App3-Auth' not in request.headers) or ('App3-User' not in request.headers) or ('App3-Pass' not in request.headers):
        logging.info("Need all of the headers to have been passed for authentication.")
        return False
    app3_timestamp = request.headers['App3-Timestamp']
    app3_auth = request.headers['App3-Auth']
    app3_user = request.headers['App3-User']
    app3_pass = request.headers['App3-Pass']

    """
    Returns whether a user is authorized based on the request.
    """
    user = User.authenticate(app3_user, app3_pass)
    if user and not user.suspended:
        logging.info("authenticated user.")
    else:
        return False

    # Time skew... Could be replay attack?
    if not is_within_n_minutes(app3_timestamp, 15): 
        return False
    
    # Check whether we generate the same auth header as they did
    return app3_auth == generate_auth(app3_user, app3_timestamp)