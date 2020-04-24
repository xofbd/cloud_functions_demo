import json
import os

import sqlalchemy


def get_weather_data(city):
    password = os.environ.get('PW')
    ip_address = '35.230.110.188'
    port = '5432'
    uri = 'postgresql://postgres:{}@{}:{}/postgres'

    engine = sqlalchemy.create_engine(uri.format(password, ip_address, port))

    columns = ['temp', 'dew_temp', 'pressure', 'wind_speed']
    query = "SELECT AVG({}), AVG({}), AVG({}), AVG({}) FROM tempdata WHERE city=%s".format(
        *columns)

    with engine.connect() as conn:
        results = conn.execute(query, city).fetchall()

    return json.dumps(dict(zip(columns, [float(result) for result in results[0]])))


def main(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()

    if request.args and 'city' in request.args:  # POST request
        return get_weather_data(request.args.get('city'))
    elif request_json and 'city' in request_json:  # GET request
        return get_weather_data(request_json['city'])
    else:
        return 'City not found or request was bad.'


if __name__ == '__main__':
    print(get_weather_data('bos'))
