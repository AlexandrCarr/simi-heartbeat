from flask import Flask, request, jsonify
import datetime
import pandas as pd
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get Sheet ID from environment variable
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

if not SHEET_ID:
    logger.error("GOOGLE_SHEET_ID environment variable not set!")
    SHEET_ID = "PLACEHOLDER_SHEET_ID"

CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

app = Flask(__name__)


@app.route("/")
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Simi Heartbeat",
        "endpoints": {
            "/daily": "Get daily message with ?part=morning|afternoon|evening"
        }
    })


@app.route("/daily")
def daily():
    """
    Fetch personalized message for specific time of day.
    Query params:
        - part: morning, afternoon, or evening (default: morning)
    """
    try:
        logger.info(f"Fetching data from Google Sheet: {SHEET_ID}")

        # Read CSV from Google Sheets (no caching, fresh read every time)
        df = pd.read_csv(CSV_URL)

        # Clean column names (remove extra spaces)
        df.columns = df.columns.str.strip()

        # Convert to strings for comparison
        df["date"] = df["date"].astype(str).str.strip()
        df["part"] = df["part"].astype(str).str.strip()
        df["message"] = df["message"].astype(str).str.strip()

        # Get current date and requested part
        today = datetime.date.today().isoformat()
        part = request.args.get("part", "morning").strip().lower()

        logger.info(f"Looking for message: date={today}, part={part}")

        # Find matching message
        msg_row = df[
            (df["date"] == today) &
            (df["part"].str.lower() == part)
        ]

        if not msg_row.empty:
            msg = msg_row["message"].values[0]
            logger.info(f"Found message: {msg[:50]}...")
        else:
            msg = f"💌 No {part} message today — but someone loves you anyway."
            logger.warning(f"No message found for {today}/{part}")

        return jsonify({"message": msg})

    except Exception as e:
        error_msg = f"Error fetching message: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return jsonify({
            "message": f"(Error fetching message 😅: {str(e)})"
        }), 500


@app.route("/test")
def test():
    """
    Test endpoint to see all available messages in the sheet
    """
    try:
        df = pd.read_csv(CSV_URL)
        df.columns = df.columns.str.strip()

        return jsonify({
            "sheet_id": SHEET_ID,
            "total_messages": len(df),
            "messages": df.to_dict('records')
        })
    except Exception as e:
        logger.error(f"Test endpoint error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
