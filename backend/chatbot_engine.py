import sys
from pathlib import Path

# Add parent directory to path so we can import chatbot.py
sys.path.append(str(Path(__file__).parent.parent))

from chatbot import build_response, get_metric, calculate_growth