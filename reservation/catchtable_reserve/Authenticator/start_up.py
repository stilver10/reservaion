from playwright.async_api import async_playwright

async def setting():
    p = await async_playwright().start()
    print("Launching browser...")
    browser = await p.chromium.launch(headless=False, timeout=5000)
    context = await browser.new_context()
    await context.tracing.start(screenshots=True, snapshots=True, sources=True)
    print("Browser launched.")
    return context