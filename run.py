from app import create_app
from models import db, User, Desk, UserCardProgress
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Register models in shell context"""
    return {
        'db': db,
        'User': User,
        'Desk': Desk,
        'UserCardProgress': UserCardProgress
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
