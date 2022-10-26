#from src import data
from src import app
from config_priv import FLASK_PORT_NUMBER

if __name__ == "__main__":
    app.flask_app.run(host="localhost", port=FLASK_PORT_NUMBER, debug=False)