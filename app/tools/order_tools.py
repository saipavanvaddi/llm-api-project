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