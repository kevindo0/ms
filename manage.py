from apps.utils import logger
from apps.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
