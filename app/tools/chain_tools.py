def get_my_latest_order(user_id: int):

    orders = {
        10: {
            "order_id": 101,
            "restaurant": "Sai Biryani",
        },
        20: {
            "order_id": 102,
            "restaurant": "Andhra Spice",
        },
    }

    order = orders.get(user_id)

    if order is None:
        return {
            "success": False,
            "error": "No order found",
        }

    return {
        "success": True,
        "order_id": order["order_id"],
        "restaurant": order["restaurant"],
    }


def get_order_items(order_id: int):

    orders = {
        101: [
            {
                "name": "Chicken Biryani",
                "quantity": 2,
            },
            {
                "name": "Coke",
                "quantity": 1,
            },
        ],
        102: [
            {
                "name": "Veg Biryani",
                "quantity": 1,
            }
        ],
    }

    items = orders.get(order_id)

    if items is None:
        return {
            "success": False,
            "error": "Order not found",
        }

    return {
        "success": True,
        "order_id": order_id,
        "items": items,
    }
