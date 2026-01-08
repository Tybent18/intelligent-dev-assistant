# Lab inventory and usage data
labs = {
    "LabA": {"ink_used": 12, "current_stock": 20},
    "LabB": {"ink_used": 7, "current_stock": 10},
    "LabC": {"ink_used": 15, "current_stock": 18},
}

# Global reorder threshold
REORDER_THRESHOLD = 10

def get_reorder_recommendations():
    recommendations = {}
    for lab, info in labs.items():
        if info["current_stock"] - info["ink_used"] < REORDER_THRESHOLD:
            # Recommend enough to reach threshold + safety buffer
            recommendations[lab] = (REORDER_THRESHOLD + info["ink_used"] + 5) - info["current_stock"]
    return recommendations