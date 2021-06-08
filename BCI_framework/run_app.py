import os
from library.bci_experiment import app

from flask_cors import CORS


if __name__ == '__main__':
    CORS(app)
    app.debug = True

    host = os.environ.get('IP', '0.0.0.0')
    
    # Only for debug
    # port = int(os.environ.get('PORT', 8081))
    port = int(os.environ.get('PORT', 8081))
    app.run(host=host, port=port)
