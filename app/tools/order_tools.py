def get_order_status(order_id: int):

    orders = {
        101: "Preparing",
        102: "Ready for pickup",
        103: "Out for delivery",
        104: "Delivered",
    }

    status = orders.get(order_id)

    if status is None:
        return {
            "order_id": order_id,
            "status": "Order not found",
        }

    return {
        "order_id": order_id,
        "status": status,
    }


def get_order_items(order_id: int):
    orders = {
        101: [
            {"name": "Chicken Biryani", "quantity": 2},
            {"name": "Coke", "quantity": 1},
        ],
        102: [
            {"name": "Veg Biryani", "quantity": 1},
            {"name": "Water", "quantity": 2},
        ],
    }

    items = orders.get(order_id)

    if items is None:
        return {
            "order_id": order_id,
            "items": [],
            "message": "Order not found",
        }

    return {
        "order_id": order_id,
        "items": items,
    }