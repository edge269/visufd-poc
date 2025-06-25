import sys
from pathlib import Path

# Add project root and src folder to PYTHONPATH for imports
root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / 'src'))
