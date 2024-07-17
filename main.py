from app import create_app, db
from app.models import User, Message
import os

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000), host='0.0.0.0')
