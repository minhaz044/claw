from playwright.async_api import async_playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


class BrowserManagerService:
    def __init__(self):
        self._playwright = None
        self._browser = None
        self._page = None

    async def _get_page(self):
        if (
                self._browser is not None
                and self._browser.is_connected()
                and self._page is not None
                and not self._page.is_closed()
        ):
            return self._page

        await self.close()

        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.firefox.launch(
            headless=False
        )
        self._page = await self._browser.new_page()

        self._page.set_default_timeout(15000)
        self._page.set_default_navigation_timeout(30000)

        return self._page

    async def _close(self):
        if self._browser is not None:
            try:
                await self._browser.close()
            except Exception:
                pass

        self._browser = None
        self._page = None

        if self._playwright is not None:
            try:
                await self._playwright.stop()
            except Exception:
                pass

        self._playwright = None

    async def open_web_url(self, url: str) -> str:
        """Navigate to a URL and report the actual result."""

        try:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            page = await self._get_page()

            response = await page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000,
            )

            return (
                f"Navigation completed.\n"
                f"URL: {page.url}\n"
                f"Title: {await page.title()}\n"
                f"HTTP status: {response.status if response else 'Unknown'}"
            )

        except Exception as e:
            return f"Navigation failed: {type(e).__name__}: {e}"

    async def inspect_web_page(self) -> str:
        """Inspect the current page and return visible text and interactive elements."""

        try:
            page = await self._get_page()

            await page.locator("body").wait_for(
                state="attached",
                timeout=15000,
            )

            # Wait for a common interactive element, if one appears.
            try:
                await page.locator(
                    "input, button, a[href], [role='button'], video, audio"
                ).first.wait_for(
                    state="visible",
                    timeout=10000,
                )
            except PlaywrightTimeoutError:
                pass

            elements = await page.locator("""
                button, a[href], input, textarea, select,
                video, audio, summary, [role],
                [tabindex]:not([tabindex="-1"]),
                [contenteditable="true"], [onclick]
            """).evaluate_all(
                """
                elements => elements
                    .filter(el => {
                        const r = el.getBoundingClientRect();
                        const s = getComputedStyle(el);
                        return r.width > 0 && r.height > 0 &&
                            s.display !== "none" &&
                            s.visibility !== "hidden";
                    })
                    .slice(0, 100)
                    .map((el, index) => ({
                        index,
                        tag: el.tagName.toLowerCase(),
                        role: el.getAttribute("role") || "",
                        text: (
                            el.innerText ||
                            el.getAttribute("aria-label") ||
                            el.getAttribute("placeholder") ||
                            el.getAttribute("title") || ""
                        ).trim().slice(0, 120),
                        id: el.id || "",
                        name: el.getAttribute("name") || "",
                        type: el.getAttribute("type") || "",
                        href: el.getAttribute("href") || ""
                    }))
                """)

            text = await page.locator("body").inner_text(timeout=10000)

            return (
                f"URL: {page.url}\n"
                f"Title: {await page.title()}\n\n"
                f"Page text:\n{text[:4000]}\n\n"
                f"Interactive elements:\n{elements}"
            )[:12000]

        except Exception as e:
            return f"Inspection failed: {type(e).__name__}: {e}"

    async def click_an_element(self, selector: str) -> str:
        """Click an element on the current page."""
        try:
            page = await self._get_page()
            await page.locator(selector).first.click(timeout=10000)
            return f"Clicked element: {selector}"
        except Exception as e:
            return f"Click failed: {type(e).__name__}: {e}"

    async def type_into_input_field(self, selector: str, text: str) -> str:
        """Enter text into an input or editable element."""
        try:
            page = await self._get_page()
            await page.locator(selector).first.fill(text, timeout=10000)
            return f"Entered text into: {selector}"
        except Exception as e:
            return f"Typing failed: {type(e).__name__}: {e}"

    async def press__btn(self, selector: str, key: str) -> str:
        """Press a key on an element."""
        try:
            page = await self._get_page()
            await page.locator(selector).first.press(key, timeout=10000)
            return f"Pressed {key} on {selector}"
        except Exception as e:
            return f"Key press failed: {type(e).__name__}: {e}"
