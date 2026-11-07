from playwright.async_api import async_playwright


class BrowserManager:
    def __init__(self):
        self._playwright = None
        self._browser = None
        self._page = None

    async def get_page(self):
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

    async def close(self):
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
