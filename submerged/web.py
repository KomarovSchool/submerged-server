from fastapi import FastAPI, UploadFile, File, HTTPException

from submerged.gpt import logger, generate_description_with_gpt
from submerged.telegram import post_to_telegram

app = FastAPI(title="Underwater Vision AI Server")


@app.post("/analyze_image/")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    """
    API endpoint to receive an image, analyze it using GPT, and post to Telegram.

    Accepts a POST request with a single file upload (`file`).
    """
    logger.info(f"Received image upload: {file.filename} (type: {file.content_type})")

    # Read image content
    try:
        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Received empty file.")
        logger.info(f"Successfully read {len(image_bytes)} bytes from uploaded file.")
    except Exception as e:
        logger.error(f"Error reading uploaded file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to read image file: {e}")
    finally:
        await file.close()  # Ensure the file is closed

    description = await generate_description_with_gpt(image_bytes)

    if not description:
        raise HTTPException(
            status_code=500, detail="Failed to generate description using AI model."
        )

    success = await post_to_telegram(image_bytes, description)

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Generated description but failed to post to Telegram.",
        )

    logger.info("Analysis and posting completed successfully.")
    return {"status": "success", "message": "Image analyzed and posted to Telegram."}
