from claw.services.browser_manager_service import BrowserManagerService
from langchain.tools import tool

_browser_manager = BrowserManagerService()


@tool
async def browser_open_url(url: str):
    """
    Open a URL in the browser and return the actual navigation result.
    Navigates to the specified URL using the browser manager
    and reports the result of the navigation.

    Args:
        url (str): The fully qualified URL to open (e.g., "https://example.com").

    Returns (str): The actual result returned by the browser manager,
      including navigation status or page information.
    """
    return await _browser_manager.open_web_url(url)


@tool
async def browser_inspect_page():
    """
    Inspect the currently open web page.

    Returns visible page text and available interactive elements,
    such as buttons, links, and input fields.

    Returns:
        str: Page content and interactive element details.
    """
    return await _browser_manager.inspect_web_page()


@tool
async def browser_click_element(selector: str):
    """
    Click an element on the currently open web page.

    Args:
        selector (str): CSS/HTML selector or supported element identifier.

    Returns:
        str: Result of the click operation.
    """
    return await _browser_manager.click_an_element(selector)


@tool
async def browser_type_into_element(selector: str, text: str):
    """
    Type text into an input or editable element.

    Args:
        selector (str): Selector identifying the target element.
        text (str): Text to enter into the element.

    Returns:
        str: Result of the typing operation.
    """
    return await _browser_manager.type_into_input_field(selector, text)


@tool
async def browser_press_btn(selector: str, key: str):
    """
    Press a keyboard key on an element on the current web page.

    Args:
        selector (str): Selector identifying the web page element.
        key (str): Key to press (e.g., Button, link,Enter, Tab, Escape).

    Returns:
        str: Result of the key press operation on the web page.
    """
    return await _browser_manager.press__btn(selector, key)

@tool
async def browser_open_url_in_new_tab(url: str = None):
    """
    Open a URL in a new browser tab.

    Creates a new tab in the existing browser context, keeping all
    previously opened tabs and their login sessions, cookies, and
    browser storage intact.

    Args:
        url (str, optional): The URL to open in the new tab.
            Supports URLs with or without http:// or https://.
            If omitted, a blank new tab will be created.

    Returns:
        str: Result of the new tab creation, including the URL
            and page title, or an error message if creation fails.
    """
    return await _browser_manager.new_tab(url)