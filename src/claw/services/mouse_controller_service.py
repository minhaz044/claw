import pyautogui


class MouseControllerService:

    def move_and_click(self, positions: list[dict]):
        """Move to each position and perform a left click."""
        for position in positions:
            pyautogui.click(
                x=position["x"],
                y=position["y"]
            )

    def double_click(self, x: int, y: int):
        """Double-click at the specified position."""
        pyautogui.doubleClick(x=x, y=y)

    def right_click(self, x: int, y: int):
        """Right-click at the specified position."""
        pyautogui.rightClick(x=x, y=y)

    def mouse_down(self, x: int, y: int):
        """Press and hold the left mouse button."""
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()

    def mouse_up(self, x: int, y: int):
        """Release the left mouse button."""
        pyautogui.moveTo(x, y)
        pyautogui.mouseUp()

    def drag(self, positions: list[dict]):
        """Drag the mouse through multiple positions."""
        if not positions:
            return

        start = positions[0]

        pyautogui.moveTo(start["x"], start["y"])
        pyautogui.mouseDown()

        try:
            for position in positions[1:]:
                pyautogui.moveTo(
                    position["x"],
                    position["y"],
                    duration=0.1
                )
        finally:
            pyautogui.mouseUp()

    def scroll(self, direction: str, amount: int = 1):
        """Scroll up or down."""
        if direction.lower() == "up":
            pyautogui.scroll(amount)
        elif direction.lower() == "down":
            pyautogui.scroll(-amount)
        else:
            raise ValueError("Direction must be 'up' or 'down'")

    def get_position(self):
        """Return the current mouse position."""
        position = pyautogui.position()

        return {
            "x": position.x,
            "y": position.y
        }
