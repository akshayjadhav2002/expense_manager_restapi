from .controllers import controller_bp

def register_routes(app):
    app.register_blueprint(controller_bp)
