# Lab inventory and usage data
labs = {
    "LabA": {"ink_used": [3, 4, 5], "current_stock": 20},
    "LabB": {"ink_used": [2, 3, 2], "current_stock": 10},
    "LabC": {"ink_used": [5, 6, 4], "current_stock": 18},
}

REORDER_THRESHOLD = 10

def get_total_usage(lab):
    return sum(labs[lab]["ink_used"])

def get_reorder_recommendations():
    recommendations = {}
    for lab, info in labs.items():
        projected_stock = info["current_stock"] - get_total_usage(lab)
        if projected_stock < REORDER_THRESHOLD:
            recommendations[lab] = (REORDER_THRESHOLD + get_total_usage(lab) + 5) - info["current_stock"]
    return recommendations

# Simple chatbot logic
def chatbot_response(message):
    message = message.lower()
    if "which labs need ink" in message:
        recs = get_reorder_recommendations()
        if not recs:
            return "All labs have enough ink."
        else:
            return "Labs needing ink: " + ", ".join(f"{lab} ({amt} units)" for lab, amt in recs.items())
    elif "stock of" in message:
        for lab in labs:
            if lab.lower() in message:
                return f"{lab} current stock: {labs[lab]['current_stock']}, total usage: {get_total_usage(lab)}"
        return "Lab not found."
    else:
        return "I can tell you lab stock and which labs need ink."