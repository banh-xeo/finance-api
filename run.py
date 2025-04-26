from finance import create_app
from loguru import logger
import sys

# Initialize logger level
logger.remove()
logger.add(
    sink=sys.stdout,
    level="DEBUG",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=8000)