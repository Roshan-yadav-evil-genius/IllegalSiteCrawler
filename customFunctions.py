from playwright.async_api import Route,Request

async def handle_request(route: Route, request: Request):
    # Abort the request if it is for an image
    if request.resource_type == "image":
        await route.abort()
    else:
        await route.continue_()