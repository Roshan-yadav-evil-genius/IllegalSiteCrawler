from playwright.async_api import async_playwright
from customFunctions import handle_request
import asyncio
import json


async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Enable request interception
        await page.route("**/*", handle_request)

        # URL of the page to scrape
        url = "https://www.skokka.in"
        await page.goto(url, wait_until="load")

        # Get the page content (optional, if you want to do something with the content)
        page_content = await page.content()

        with open("page_content.html", "w", encoding="utf-8") as file:
            file.write(page_content)

        state = await context.storage_state()
        with open("state.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(state))

        await browser.close()

# Run the main function
asyncio.run(main())