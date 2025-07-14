import json, os
import psycopg2
import logging
from dotenv import load_dotenv

# Set up and configure logging
log_dir = os.path.join("..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "loader.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
)


def load_telegram_messages():
    logging.info("Loading environment variables...")

    load_dotenv(os.path.join(os.path.abspath(os.path.join("..")), ".env"))

    try:
        conn = psycopg2.connect(
            dbname=os.getenv("PG_DB"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
        )
        cursor = conn.cursor()
        logging.info("Connected to PostgreSQL database.")
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        return

    try:
        logging.info("Ensuring raw schema and telegram_messages table exist...")
        cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        cursor.execute("DROP TABLE IF EXISTS raw.telegram_messages;")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS raw.telegram_messages (
                channel_title TEXT,
                channel_username TEXT,
                id BIGINT,
                text TEXT,
                date TIMESTAMP,
                views INTEGER,
                media_type TEXT
            );
        """
        )
        logging.info("Schema and table setup completed.")
    except Exception as e:
        logging.error(f"Error during schema/table creation: {e}")
        return

    data_paths = [
        "../data/raw/telegram_messages/2025-07-11/CheMed123.json",
        "../data/raw/telegram_messages/2025-07-11/lobelia4cosmetics.json",
        "../data/raw/telegram_messages/2025-07-11/newoptics.json",
        "../data/raw/telegram_messages/2025-07-11/thiopianfoodanddrugauthority.json",
        "../data/raw/telegram_messages/2025-07-11/tikvahpharma.json",
        "../data/raw/telegram_messages/2025-07-11/yetenaweg.json",
    ]

    total_inserted = 0
    for path in data_paths:
        if not os.path.exists(path):
            logging.warning(f"File not found: {path}")
            continue

        logging.info(f"Loading messages from {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                messages = json.load(f)
                for msg in messages:
                    cursor.execute(
                        """
                        INSERT INTO raw.telegram_messages (
                            channel_title, channel_username, id, text, date, views, media_type
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            msg["channel_title"],
                            msg["channel_username"],
                            msg["id"],
                            msg["text"],
                            msg["date"],
                            msg["views"],
                            msg["media_type"],
                        ),
                    )
                    total_inserted += 1
        except Exception as e:
            logging.error(f"Failed to process {path}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    logging.info(f"Load complete: {total_inserted} messages inserted.")
