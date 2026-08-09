import base64
import binascii
from io import BytesIO

from PIL import Image, UnidentifiedImageError

from backend.domains.scenario.schemas.multimodal import (
    ScenarioImageMetadata,
    ScenarioImagePayload,
)


MAX_SCENARIO_IMAGE_BYTES = 4 * 1024 * 1024
ALLOWED_SCENARIO_IMAGE_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
}


class ScenarioImageValidationError(ValueError):
    pass


def decode_scenario_image(payload: ScenarioImagePayload | dict) -> tuple[bytes, ScenarioImageMetadata]:
    image_payload = ScenarioImagePayload.model_validate(payload)
    if image_payload.mime_type not in ALLOWED_SCENARIO_IMAGE_MIME_TYPES:
        raise ScenarioImageValidationError(
            "Unsupported image format. Allowed formats are PNG, JPG, JPEG and WEBP."
        )
    if image_payload.size_bytes > MAX_SCENARIO_IMAGE_BYTES:
        raise ScenarioImageValidationError(
            f"Image is too large. Maximum size is {MAX_SCENARIO_IMAGE_BYTES} bytes."
        )

    try:
        image_bytes = base64.b64decode(image_payload.data_base64, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ScenarioImageValidationError("Image data is not valid base64.") from exc

    if not image_bytes:
        raise ScenarioImageValidationError("Image file is empty.")
    if len(image_bytes) != image_payload.size_bytes:
        raise ScenarioImageValidationError("Image size metadata does not match payload.")

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image.verify()
        with Image.open(BytesIO(image_bytes)) as image:
            width, height = image.size
    except (UnidentifiedImageError, OSError) as exc:
        raise ScenarioImageValidationError("Image file is damaged or unreadable.") from exc

    return image_bytes, ScenarioImageMetadata(
        filename=image_payload.filename,
        mime_type=image_payload.mime_type,
        size_bytes=image_payload.size_bytes,
        width=width,
        height=height,
    )
