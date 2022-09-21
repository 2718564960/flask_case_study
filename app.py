from flask import Flask
import config
from exts import db,mail
from blueprints import user_bp, qa_bp
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run()
