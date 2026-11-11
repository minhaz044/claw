from langchain_core.tools import tool

from src.claw.services.mouse_controller_service import MouseControllerService

mouse = MouseControllerService()


@tool
def mouse_move_and_click(positions: list[dict]) -> str:
    """
    Move the mouse to multiple screen coordinates and left-click each position.

    Args:
        positions: List of coordinates, e.g.
                   [{"x": 100, "y": 200}, {"x": 300, "y": 400}]
    """
    mouse.move_and_click(positions)
    return f"Successfully clicked {len(positions)} positions."


@tool
def mouse_double_click(x: int, y: int) -> str:
    """Double-click at the specified screen coordinates."""
    mouse.double_click(x, y)
    return f"Double-clicked at ({x}, {y})."


@tool
def mouse_right_click(x: int, y: int) -> str:
    """Right-click at the specified screen coordinates."""
    mouse.right_click(x, y)
    return f"Right-clicked at ({x}, {y})."


@tool
def mouse_down(x: int, y: int) -> str:
    """
    Press and hold the left mouse button at the specified coordinates.
    Use mouse_up to release it.
    """
    mouse.mouse_down(x, y)
    return f"Mouse button pressed at ({x}, {y})."


@tool
def mouse_up(x: int, y: int) -> str:
    """Release the left mouse button at the specified coordinates."""
    mouse.mouse_up(x, y)
    return f"Mouse button released at ({x}, {y})."


@tool
def mouse_drag(positions: list[dict]) -> str:
    """
    Drag the mouse through a sequence of coordinates.

    The first position is the starting point.
    The last position is the ending point.
    """
    if len(positions) < 2:
        return "Drag requires at least two positions."

    mouse.drag(positions)
    return f"Successfully dragged through {len(positions)} positions."


@tool
def mouse_scroll(direction: str, amount: int = 1) -> str:
    """
    Scroll the mouse wheel.

    Args:
        direction: 'up' or 'down'.
        amount: Number of scroll units.
    """
    mouse.scroll(direction, amount)
    return f"Scrolled {direction} by {amount} units."


@tool
def mouse_get_position() -> dict:
    """Get the current mouse cursor coordinates."""
    return mouse.get_position()


# Register all mouse tools
mouse_tools = [
    mouse_move_and_click,
    mouse_double_click,
    mouse_right_click,
    mouse_down,
    mouse_up,
    mouse_drag,
    mouse_scroll,
    mouse_get_position
]
