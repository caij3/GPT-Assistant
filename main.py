import threading
from webserver import run_flask  # Adjust according to your actual file name
from bot import run_bot  # Adjust according to your actual file name

if __name__ == "__main__":
    # Start the Flask web server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Run the Discord bot in the main thread
    run_bot()
