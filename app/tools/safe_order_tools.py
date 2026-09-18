import logging

from app.db.database import get_connection

logger = logging.getLogger(__name__)


def get_order_status_safe(order_id: int):

    try:

        if order_id <= 0:
            return {
                "success": False,
                "error": "Order ID must be greater than 0",
            }

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
                "success": False,
                "error": f"Order {order_id} was not found",
            }

        return {
            "success": True,
            "order_id": order[0],
            "status": order[1],
        }

    except Exception:

        logger.exception("Failed to retrieve order status")

        return {
            "success": False,
            "error": "Unable to retrieve order status",
        }
