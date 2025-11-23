import json
import sys
from pathlib import Path

ORDERS_FILE = Path(__file__).resolve().parent / "orders.json"


def append_order(order_obj: dict):
    orders = []
    if ORDERS_FILE.exists():
        try:
            with ORDERS_FILE.open("r", encoding="utf-8") as f:
                orders = json.load(f)
        except Exception:
            orders = []

    orders.append(order_obj)
    with ORDERS_FILE.open("w", encoding="utf-8") as f:
        json.dump(orders, f, indent=2)


def main():
    # Read JSON from stdin or first CLI arg
    raw = None
    if len(sys.argv) > 1:
        raw = sys.argv[1]
    else:
        raw = sys.stdin.read().strip()

    if not raw:
        print("No JSON provided. Usage: python save_order.py '{\"drinkType\":...}' or pipe JSON into stdin.")
        sys.exit(1)

    try:
        order = json.loads(raw)
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        sys.exit(2)

    append_order(order)
    print(f"Saved order to {ORDERS_FILE}")


if __name__ == "__main__":
    main()
