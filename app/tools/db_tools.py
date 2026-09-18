from app.db.database import get_connection


def get_order_status_from_db(order_id: int):

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id, status
                FROM orders
                WHERE id = %s
                """,
                (order_id,),
            )

            order = cursor.fetchone()

    if order is None:
        return {
            "order_id": order_id,
            "status": "Order not found",
        }

    return {
        "order_id": order[0],
        "status": order[1],
    }