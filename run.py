from app import create_app

app = create_app()

# DEBUG: print all routes
print("Registered routes:")
print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)

