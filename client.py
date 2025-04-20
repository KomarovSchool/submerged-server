import httpx

async def send_image():
    url = "http://localhost:8123/analyze_image/"
    image_path = "data/image.jpeg"

    try:
        with open(image_path, "rb") as f:
            files = {"file": ("image.jpeg", f, "image/jpeg")}
            async with httpx.AsyncClient() as client:
                response = await client.post(url, files=files)

        print("Status code:", response.status_code)
        print("Response:", response.json())

    except Exception as e:
        print("Error sending image:", e)

# Run the function using asyncio
if __name__ == "__main__":
    import asyncio
    asyncio.run(send_image())
