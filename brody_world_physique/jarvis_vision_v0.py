"""Brody Image I1: bounded adapter to the EXISTING Jarvis local Qwen-VL service.

Uses the same OpenAI-compatible endpoint and payload as Jarvis'
LocalVisionCognition; does not import Jarvis or start/download any model.

Output is a descriptive CANDIDATE only: no F16 RealImageObservation claim,
no segmentation mask, no Brody API injection, no Binder invocation, no memory
write, no action/decision authority.
"""
from __future__ import annotations

import argparse
import base64
from dataclasses import asdict, dataclass
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import (
    HTTPRedirectHandler, ProxyHandler, Request, build_opener,
)

from PIL import Image, ImageOps, UnidentifiedImageError

DEFAULT_ENDPOINT = "http://127.0.0.1:8081/v1/chat/completions"
DEFAULT_MODEL = "Qwen2.5-VL-3B-Instruct"
MAX_INPUT_BYTES = 25 * 1024 * 1024
MAX_PIXELS = 20_000_000
MAX_RESPONSE_BYTES = 1024 * 1024
SOURCE_KINDS = ("USER_IMAGE_FILE", "GENERATED_ARTIFACT")


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _local_endpoint(endpoint: str) -> str:
    """No external IP/domain and no unencrypted LAN exposure, even on redirect."""
    parts = urlsplit(endpoint)
    if (
        parts.scheme != "http"
        or parts.hostname not in ("localhost", "127.0.0.1", "::1")
        or parts.username is not None
        or parts.password is not None
        or parts.path != "/v1/chat/completions"
        or parts.query
        or parts.fragment
    ):
        raise ValueError(
            "vision endpoint must be loopback http://127.0.0.1:PORT/v1/chat/completions; "
            "use a local SSH tunnel when calling from the portable"
        )
    try:
        port = parts.port
    except ValueError as exc:
        raise ValueError("invalid vision endpoint port") from exc
    if port is None or not 1 <= port <= 65535:
        raise ValueError("vision endpoint requires an explicit TCP port")
    return endpoint


def _jpeg_for_local_model(image_path: Path, max_dimension: int) -> tuple[str, str, list[int]]:
    if not 64 <= max_dimension <= 4096:
        raise ValueError("max_dimension must be 64..4096")
    size = image_path.stat().st_size
    if not 0 < size <= MAX_INPUT_BYTES:
        raise ValueError("input image must be nonempty and <= 25 MiB")
    with Image.open(image_path) as raw:
        if raw.width * raw.height > MAX_PIXELS:
            raise ValueError("input image exceeds 20 million pixels")
        if raw.format not in ("PNG", "JPEG", "WEBP"):
            raise ValueError("supported images: PNG, JPEG or WEBP")
        image = ImageOps.exif_transpose(raw)
        image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
        # Model input is an encoded RGB JPEG; not source-identical.
        if image.mode == "RGBA" or "transparency" in image.info:
            rgb = Image.new("RGB", image.size, "white")
            rgba = image.convert("RGBA")
            rgb.paste(rgba, mask=rgba.getchannel("A"))
            image = rgb
        else:
            image = image.convert("RGB")
        dimensions = list(image.size)
        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=85)
    sent = buffer.getvalue()
    return base64.b64encode(sent).decode("ascii"), hashlib.sha256(sent).hexdigest(), dimensions


@dataclass(frozen=True)
class VisionDescriptionCandidateV0:
    schema_version: str
    observation_status: str
    source_kind: str
    source_sha256: str
    model_input_sha256: str
    model_input_size: tuple[int, int]
    provider: str
    provider_model: str
    provider_endpoint: str
    prompt: str
    candidate_text: str
    semantics_verified: bool = False
    real_image_observation: bool = False
    memory_write_allowed: bool = False
    auto_promotion_allowed: bool = False
    readonly: bool = True
    decision_authority: str = "KX108_ONLY"
    allowed_to_act: bool = False
    kernel_mutation: bool = False


def describe_image(
    image_path: str | Path,
    *,
    endpoint: str = DEFAULT_ENDPOINT,
    model: str = DEFAULT_MODEL,
    prompt: str = (
        "Décris les éléments visibles, leur position relative, les limites et "
        "les incertitudes. Ne suppose ni matière, ni profondeur, ni identité "
        "ni causalité non vérifiées."
    ),
    source_kind: str = "USER_IMAGE_FILE",
    timeout: float = 120,
    max_dimension: int = 1280,
    max_tokens: int = 256,
) -> VisionDescriptionCandidateV0:
    """Send exactly ONE explicitly chosen image to a loopback Qwen-VL service."""
    endpoint = _local_endpoint(endpoint)
    if source_kind not in SOURCE_KINDS:
        raise ValueError("source_kind must distinguish user file from generated artifact")
    if not model.strip() or not prompt.strip() or not 0 < timeout <= 300:
        raise ValueError("model, prompt and positive timeout <=300 are required")
    if not 16 <= max_tokens <= 1024:
        raise ValueError("max_tokens must be 16..1024")
    selected_path = Path(image_path)
    if selected_path.is_symlink():
        raise ValueError("image must not be a symlink")
    image_path = selected_path.resolve(strict=True)
    if not image_path.is_file():
        raise ValueError("image must be a regular file")
    if not 0 < image_path.stat().st_size <= MAX_INPUT_BYTES:
        raise ValueError("input image must be nonempty and <= 25 MiB")
    original_sha256 = hashlib.sha256(image_path.read_bytes()).hexdigest()
    encoded, sent_sha256, dimensions = _jpeg_for_local_model(image_path, max_dimension)
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es un fournisseur visuel descriptif sans pouvoir d'action. "
                    "Décris seulement ce qui est visible. Signale les incertitudes. "
                    "Une image générée n'est jamais une observation physique."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": "data:image/jpeg;base64," + encoded},
                    },
                ],
            },
        ],
        "temperature": 0.1,
        "max_tokens": max_tokens,
        "stream": False,
    }
    request = Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    # No HTTP proxy / no redirect; neither the image nor prompt can leak to
    # a remote host via a redirected URL.
    opener = build_opener(ProxyHandler({}), _NoRedirect())
    try:
        with opener.open(request, timeout=timeout) as reply:
            raw = reply.read(MAX_RESPONSE_BYTES + 1)
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise RuntimeError("Jarvis/Qwen-VL local endpoint unavailable or rejected request") from exc
    if len(raw) > MAX_RESPONSE_BYTES:
        raise RuntimeError("vision response too large")
    try:
        response = json.loads(raw.decode("utf-8"))
        answer = response["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("invalid local vision response envelope") from exc
    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("empty or non-textual vision response")

    return VisionDescriptionCandidateV0(
        schema_version="BRODY_VISION_DESCRIPTION_CANDIDATE_V0",
        observation_status="MODEL_DESCRIPTION_UNVERIFIED",
        source_kind=source_kind,
        source_sha256=original_sha256,
        model_input_sha256=sent_sha256,
        model_input_size=tuple(dimensions),
        provider="JARVIS_LOCAL_QWEN_VL",
        provider_model=model,
        provider_endpoint=endpoint,
        prompt=prompt,
        candidate_text=answer.strip(),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Brody Image I1: existing Jarvis Qwen-VL vision provider (local only)"
    )
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True, help="JSON candidate receipt output")
    parser.add_argument("--endpoint", default=os.getenv("JARJAR_VISION_URL", DEFAULT_ENDPOINT))
    parser.add_argument("--model", default=os.getenv("JARJAR_VISION_MODEL", DEFAULT_MODEL))
    parser.add_argument("--prompt", default=(
        "Décris les objets visibles, leur position et les incertitudes. "
        "Ne fabrique pas de contexte extérieur à la photo."
    ))
    parser.add_argument("--source-kind", choices=SOURCE_KINDS, default="USER_IMAGE_FILE")
    parser.add_argument("--max-dimension", type=int, default=1280)
    args = parser.parse_args(argv)
    if args.out.resolve() == args.image.resolve():
        parser.error("--out must not overwrite --image")
    candidate = describe_image(
        args.image, endpoint=args.endpoint, model=args.model,
        prompt=args.prompt, source_kind=args.source_kind,
        max_dimension=args.max_dimension,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(asdict(candidate), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(candidate.candidate_text)
    print("candidate_receipt=" + str(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
