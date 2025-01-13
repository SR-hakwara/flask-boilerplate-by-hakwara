from app import create_app
from dotenv import load_dotenv
from config import get_config

load_dotenv()
config = get_config()
app = create_app(config)

if __name__ == "__main__":
    app.run()
