from finance import create_app
from loguru import logger

# Initialize logger level
logger.remove()
logger.add(
    sink="logs/finance.log",
    mode="w",
    level="DEBUG",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=8000)
