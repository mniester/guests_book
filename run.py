from app import app

#the app does not work without import below - I don't know why

from app.routes import index



if __name__ == '__main__':
    app.run(debug = True)

