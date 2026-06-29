from app import create_app
import os
os.makedirs("app/instance", exist_ok=True)
app = create_app()

if __name__ == "__main__":

    app.run(
        debug=True
    )
    
