from app import create_app
from app.models import init_db

app = create_app()
init_db() 

# DEBUG: print all routes
print("Registered routes:")
print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)

