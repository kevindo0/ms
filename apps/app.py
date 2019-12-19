from flask import Flask
from dynaconf import settings

print(dir(settings))

def _register_blueprint(app):
    from apps.ptest.views import test_bp
    
    app.register_blueprint(test_bp, url_prefix='/test')

def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config)

    # 模块注册
    _register_blueprint(app)

    # session
    app.permanent_session_lifetime = timedelta(seconds=config['session']['expire'])
    app.session_interface = RedisSessionInterface(redis=predis, prefix=config['session']['redis_prefix'])

    if config['debug']:
        @app.after_request
        def cors_headers(response):
            origin = request.headers.get('Origin')
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Max-Age"] = sys.maxsize
            response.headers[
                "Access-Control-Allow-Headers"] = "authorization,Access-Control-Allow-Origin,Content-Type,Cookie,Connection,Accept-Language,Accept-Encoding,Accept,User-Agent,Host,Accept-Charset"
            response.headers[
                "Access-Control-Allow-Methods"] = "GET,POST,PATCH,OPTIONS,DELETE,PUT"
            response.headers[
                "Access-Control-Allow-Origin"] = origin
            return response

    @app.errorhandler(HttpException)
    def http_exception(error):
        logger.exception(error)
        return jsonify({
            "code": error.code,
            "message": error.message
        })

    @app.errorhandler(Exception)
    def internel_error(error):
        logger.exception(error)
        return jsonify({
            "code": 500,
            "message": "Internal Error"
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "code": 400,
            "message": "BadRequest"
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "code": 404,
            "message": "NotFound"
        })

    @app.errorhandler(405)
    def method_not_support(error):
        return jsonify({
            "code": 405,
            "message": "MethodNotSupport"
        })

    return app