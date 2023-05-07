from app import app
import os

if __name__ =="__main__":
    app.run(host="127.0.0.1", debug=True, port=os.getenv("PORT", default=5000))
