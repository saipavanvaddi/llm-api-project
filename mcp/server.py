from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Manakarto")


@mcp.tool()
def get_order_status(order_id: int) -> str:
    """Get the current status of a food delivery order."""

    orders = {
        101: "Preparing",
        102: "Ready for pickup",
        103: "Out for delivery",
        104: "Delivered",
    }

    status = orders.get(order_id)

    if status is None:
        return f"Order {order_id} was not found."

    return f"Order {order_id} is {status}."


if __name__ == "__main__":
    mcp.run()
