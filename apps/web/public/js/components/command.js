// Expenso Quick Command Parser Component
const Command = (() => {
  const catKeywords = {
    "Food": ["food", "dinner", "lunch", "breakfast", "burger", "pizza", "coffee", "chai", "snack", "zomato", "swiggy", "restaurant"],
    "Transport": ["transport", "uber", "ola", "auto", "metro", "bus", "fuel", "petrol", "diesel", "cab", "train"],
    "Shopping": ["shopping", "amazon", "flipkart", "clothes", "shoes", "grocery", "mart"],
    "Bills": ["bill", "electricity", "water", "wifi", "internet", "recharge", "phone"],
    "Rent": ["rent", "flat", "pg"],
    "Entertainment": ["movie", "cinema", "game", "netflix", "party"],
    "Health": ["health", "medicine", "doctor", "pharmacy", "clinic"],
    "Salary": ["salary", "stipend"],
    "Freelancing": ["freelance", "client", "upwork", "fiverr"]
  };

  function parse(text) {
    const raw = text.trim();
    if (!raw) return null;

    const amtMatch = raw.match(/(?:₹|\$|€|£)?\s*(\d+(?:\.\d{1,2})?)/);
    if (!amtMatch) return null;
    const amount = parseFloat(amtMatch[1]);

    const isIncome = /salary|freelance|allowance|dividend|bonus|received|income/i.test(raw);
    const type = isIncome ? "income" : "expense";

    let desc = raw.replace(/(?:₹|\$|€|£)?\s*\d+(?:\.\d{1,2})?/, "")
      .replace(/^(add|spent|paid|record|for|on|at|got)\s+/gi, "").trim();
    if (!desc) desc = isIncome ? "Quick Income" : "Quick Expense";

    let matchedCatId = null;
    const lower = desc.toLowerCase();
    for (const [cName, kws] of Object.entries(catKeywords)) {
      if (kws.some(kw => lower.includes(kw))) {
        const found = State.state.categories.find(c => c.name.toLowerCase() === cName.toLowerCase());
        if (found) { matchedCatId = found.id; break; }
      }
    }
    return {
      amount,
      description: desc,
      type,
      category_id: matchedCatId,
      transaction_date: State.getTodayDateString()
    };
  }

  return { parse };
})();
