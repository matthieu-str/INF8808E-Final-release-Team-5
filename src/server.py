'''
Contains the server to run our application.
'''

from flask_failsafe import failsafe
from app import app


@failsafe
def create_app():
    '''
        Gets the underlying Flask server from the Dash app.

        Returns:
            The server to be run
    '''

    return app.server


if __name__ == "__main__":
    create_app().run(port="8060", debug=True)
