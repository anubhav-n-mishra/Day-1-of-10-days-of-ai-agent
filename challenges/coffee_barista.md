# Coffee Barista - Day 2 Implementation

This branch implements the Day 2 primary objective: turn the starter agent into a friendly coffee shop barista that takes voice orders and saves them.

Summary of features added on the `coffee_barista` branch:

- Barista persona and instructions in `backend/src/agent.py` to maintain a structured order state.
- The assistant will output a single-line marker when the order is complete: `ORDER_COMPLETE_JSON: { ... }`.
- A helper script `backend/save_order.py` which accepts a JSON object (via CLI arg or stdin) and appends it to `backend/orders.json`.
- A README update documenting how to run and test the feature locally on Windows.

How it works (quick):

1. Start the backend (use the venv python):

```powershell
cd backend
.\.venv\Scripts\python.exe src/agent.py dev
```

2. Start the frontend:

```powershell
cd frontend
pnpm dev
```

3. Open `http://localhost:3001` and talk to the barista. The agent will ask clarifying questions to fill the order state.

4. When the order is complete, the agent prints a single-line marker:

```
ORDER_COMPLETE_JSON: {"drinkType":"latte","size":"medium","milk":"oat","extras":["vanilla"],"name":"Alex"}
```

5. Save the order by passing the JSON to the save helper:

```powershell
python ..\backend\save_order.py '{"drinkType":"latte","size":"medium","milk":"oat","extras":["vanilla"],"name":"Alex"}'
```

Notes:
- The `coffee_barista` branch contains the Day 2 changes. `master` has been reverted to remove these changes so you can keep `master` clean.
- If you want automatic saving when the agent emits the `ORDER_COMPLETE_JSON` marker, I can add a small handler server-side to call `save_order.append_order` directly.
