"""Brody Image: first falsifiable slice of the user's reciprocal visual method.

Source: docs/23 and docs/24 (FSO original). This module implements a LOSSLESS
raster analysis<->synthesis experiment, and *proposed* candidate-retention
gates. It does not implement semantic painters' layers, object segmentation,
learned physics, parametric training, canonical memory, or Obsidia authority.

The master is always the source; image descriptions are candidates only.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path

from PIL import Image, UnidentifiedImageError

MAX_PIXELS = 20_000_000
MAX_LAYERS = 4096


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _pixel_digest(image: Image.Image) -> str:
    image = image.convert("RGBA")
    h = hashlib.sha256()
    h.update(f"RGBA:{image.width}x{image.height}:".encode("ascii"))
    h.update(image.tobytes())
    return h.hexdigest()


def _rgba(path: Path) -> Image.Image:
    with Image.open(path) as image:
        if image.width * image.height > MAX_PIXELS:
            raise ValueError("image too large for bounded pixel experiment")
        if image.format not in ("JPEG", "PNG", "WEBP"):
            raise ValueError("supported sources: PNG, JPEG, WEBP")
        return image.convert("RGBA")


def _outdir(source: Path, destination: Path) -> None:
    if destination == source or source in destination.parents:
        # This does NOT prevent output under source's parent: source is a file.
        raise ValueError("cannot use source image as an output directory")


def decompose_reverso(
    source: str | Path, output_dir: str | Path, *, tile_size: int = 128,
    intent: str = "Reproduce original visible pixel values exactly.",
) -> dict:
    """Image -> independent lossless spatial tiles -> replayed RGBA image.

    Tiles are not objects, semantic painter layers, or any physics model.
    Pixel equality refers to decoded RGBA values (not identical JPEG bytes).
    """
    if not 16 <= tile_size <= 1024:
        raise ValueError("tile_size must be between 16 and 1024")
    if not intent.strip():
        raise ValueError("user intent must be preserved")
    src_path = Path(source).resolve(strict=True)
    out = Path(output_dir).resolve()
    _outdir(src_path, out)
    image = _rgba(src_path)
    nx = (image.width + tile_size - 1) // tile_size
    ny = (image.height + tile_size - 1) // tile_size
    if nx * ny > MAX_LAYERS:
        raise ValueError("too many layers; increase tile_size")
    if out == src_path.parent:
        raise ValueError("output directory must not be source directory")

    layers_dir = out / "lossless_layers"
    if layers_dir.exists() and any(layers_dir.iterdir()):
        raise ValueError("output lossless_layers already contains files; use fresh directory")
    if any((out / name).exists() for name in ("manifest.json", "reconstructed.png")):
        raise ValueError("output already contains a prior manifest or reconstruction")
    layers_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for row in range(ny):
        for col in range(nx):
            x, y = col * tile_size, row * tile_size
            tile = image.crop((x, y, min(x + tile_size, image.width), min(y + tile_size, image.height)))
            name = f"tile-{row:03d}-{col:03d}.png"
            asset = layers_dir / name
            tile.save(asset, format="PNG")
            records.append({
                "asset": f"lossless_layers/{name}",
                "x": x, "y": y, "width": tile.width, "height": tile.height,
                "sha256": _sha256(asset),
            })
    manifest = {
        "schema_version": "BRODY_REVERSO_PIXEL_LAYERS_V0",
        "route": "LOSSLESS_SPATIAL_TILES_NOT_SEMANTIC_SEGMENTATION",
        "source_ref": str(src_path),
        "source_sha256": _sha256(src_path),
        "reference_rgba_pixel_digest": _pixel_digest(image),
        "width": image.width, "height": image.height,
        "intent": intent,
        "layers": records,
        "claims": {
            "world_physics_understood": False,
            "semantic_decomposition": False,
            "pixel_round_trip_only": True,
            "learned_model_updated": False,
        },
        "memory_write_allowed": False,
        "auto_promotion_allowed": False,
        "decision_authority": "KX108_ONLY",
        "allowed_to_act": False,
        "kernel_mutation": False,
    }
    manifest_file = out / "manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    verification = replay_reverso(manifest_file, output=out / "reconstructed.png")
    return {
        "manifest": str(manifest_file),
        "reconstructed": str(out / "reconstructed.png"),
        "reference_rgba_pixel_digest": manifest["reference_rgba_pixel_digest"],
        "reconstructed_rgba_pixel_digest": verification["reconstructed_rgba_pixel_digest"],
        "pixel_equivalence": verification["pixel_equivalence"],
        "layer_count": len(records),
        "source_sha256": manifest["source_sha256"],
        "memory_write_allowed": False,
    }


def replay_reverso(manifest_path: str | Path, *, output: str | Path | None = None) -> dict:
    """Replay from saved layers, verify every blob hash and complete coverage."""
    manifest_path = Path(manifest_path).resolve(strict=True)
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "BRODY_REVERSO_PIXEL_LAYERS_V0":
        raise ValueError("wrong reverso manifest version")
    w, h = data["width"], data["height"]
    if not 0 < w * h <= MAX_PIXELS:
        raise ValueError("invalid canvas dimensions")
    records = data.get("layers")
    if not isinstance(records, list) or not 1 <= len(records) <= MAX_LAYERS:
        raise ValueError("invalid layer manifest")
    result = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    coverage = bytearray(w * h)
    root = manifest_path.parent
    for item in records:
        asset_name = item["asset"]
        asset_relative = Path(asset_name)
        if asset_relative.is_absolute() or ".." in asset_relative.parts or len(asset_relative.parts) != 2 or asset_relative.parts[0] != "lossless_layers":
            raise ValueError("unsafe layer path")
        asset = (root / asset_relative).resolve(strict=True)
        if root not in asset.parents:
            raise ValueError("layer path escapes manifest root")
        if _sha256(asset) != item["sha256"]:
            raise ValueError("layer hash mismatch: replay must fail closed")
        tile = _rgba(asset)
        x, y, tw, th = (item[k] for k in ("x", "y", "width", "height"))
        if min(x, y) < 0 or x + tw > w or y + th > h or tile.size != (tw, th):
            raise ValueError("invalid tile geometry")
        for yy in range(y, y + th):
            for xx in range(x, x + tw):
                offset = yy * w + xx
                if coverage[offset]:
                    raise ValueError("overlapping spatial layers")
                coverage[offset] = 1
        result.paste(tile, (x, y))
    if 0 in coverage:
        raise ValueError("reconstruction is missing source pixels")
    digest = _pixel_digest(result)
    if digest != data["reference_rgba_pixel_digest"]:
        raise ValueError("reconstructed pixels do not match source reference")
    if output is not None:
        out = Path(output).resolve()
        if out == manifest_path or any(out == (root / rec["asset"]).resolve() for rec in records):
            raise ValueError("output cannot overwrite manifest or layer")
        out.parent.mkdir(parents=True, exist_ok=True)
        result.save(out, format="PNG")
    return {
        "pixel_equivalence": "PASS_EXACT_DECODED_RGBA",
        "reconstructed_rgba_pixel_digest": digest,
        "pixel_count": w * h,
        "layer_count": len(records),
        "world_model_validation": "NOT_RUN",
        "semantic_validation": "NOT_RUN",
        "memory_write_allowed": False,
    }


@dataclass(frozen=True)
class WorldRelationCandidateV0:
    """A relationship supplied by an observer/model, NOT a proven physical law."""
    subject_ref: str
    relation: str
    object_ref: str
    source_ref: str
    evidence_status: str = "MODEL_CANDIDATE"
    world_law_proven: bool = False
    readonly: bool = True
    decision_authority: str = "KX108_ONLY"

    def __post_init__(self):
        if any(not isinstance(s, str) or not s.strip() for s in
               (self.subject_ref, self.relation, self.object_ref, self.source_ref)):
            raise ValueError("relation needs source and both object references")
        if self.evidence_status not in ("MODEL_CANDIDATE", "OBSERVATION_CANDIDATE", "REVIEWED"):
            raise ValueError("invalid evidence status")
        if self.world_law_proven:
            raise ValueError("a relation candidate cannot prove a world law")


@dataclass(frozen=True)
class LearningEpisodeSignalV0:
    """Summary of an attempted skill/invariant/error, NOT native memory."""
    kind: str
    route_ref: str
    source_ref: str
    outcome: str
    independent_evidence_refs: tuple[str, ...] = ()
    replay_confirmed: bool = False
    relevant_to_intent: bool = True

    def __post_init__(self):
        if self.kind not in ("SOURCE_ANCHOR", "INVARIANT", "SKILL", "FAILURE_PATTERN",
                             "HYPOTHESIS", "MODEL_DESCRIPTION", "RAW_PIXEL_DUMP"):
            raise ValueError("unknown learning signal kind")
        if self.outcome not in ("PASS", "FAIL", "UNKNOWN", "INCONCLUSIVE"):
            raise ValueError("unknown outcome")
        if not self.route_ref.strip() or not self.source_ref.strip():
            raise ValueError("learning signals need source and route")
        object.__setattr__(self, "independent_evidence_refs",
                           tuple(self.independent_evidence_refs))


def triage_learning(signal: LearningEpisodeSignalV0, *, previous_failed_routes: tuple[str, ...] = ()) -> dict:
    """Proposed bounded policy: what to refer to, test, or omit.

    This is NOT an empirically established human memory algorithm. Outputs
    are advice/candidates; no native-memory writes or model-weight changes.
    """
    verified = bool(signal.independent_evidence_refs) and signal.replay_confirmed
    if signal.kind == "SOURCE_ANCHOR":
        action, why = "KEEP_SOURCE_REFERENCE", "Maintain source provenance; do not duplicate all pixels in semantic memory"
    elif not signal.relevant_to_intent:
        action, why = "OMIT_FROM_LEARNING_CANDIDATE", "Not relevant to the current user intent"
    elif signal.kind in ("RAW_PIXEL_DUMP", "MODEL_DESCRIPTION"):
        action, why = "REFERENCE_ONLY", "Raw pixels and unverified VLM prose are not a validated skill or physical fact"
    elif signal.kind == "HYPOTHESIS" or signal.outcome in ("UNKNOWN", "INCONCLUSIVE"):
        action, why = "REVIEW_HYPOTHESIS", "Insufficient evidence: request replay or independent observation"
    elif verified and signal.kind in ("INVARIANT", "SKILL", "FAILURE_PATTERN"):
        action, why = "REVIEW_VALIDATED_PATTERN", "Independent evidence and replay: candidate for governed review only"
    else:
        action, why = "REVIEW_EXPERIENCE", "An outcome alone is not a general reusable fact"
    avoid_route = (
        signal.route_ref in previous_failed_routes
        and signal.kind == "FAILURE_PATTERN"
        and signal.outcome == "FAIL"
    )
    return {
        "schema_version": "BRODY_LEARNING_TRIAGE_CANDIDATE_V0",
        "kind": signal.kind,
        "source_ref": signal.source_ref,
        "route_ref": signal.route_ref,
        "proposed_action": action,
        "rationale": why,
        "known_failed_route_repetition": avoid_route,
        "should_propose_alternate_route": avoid_route,
        "world_fact_claim": False,
        "human_memory_mechanism_proven": False,
        "canonical_memory": False,
        "memory_write_allowed": False,
        "auto_promotion_allowed": False,
        "decision_authority": "KX108_ONLY",
        "allowed_to_act": False,
        "kernel_mutation": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Brody Reverso: lossless raster analysis -> layers -> reconstruction")
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--tile-size", type=int, default=128)
    parser.add_argument("--intent", default="Rebuild exact original pixels while keeping the source as anchor.")
    args = parser.parse_args(argv)
    answer = decompose_reverso(args.image, args.out, tile_size=args.tile_size, intent=args.intent)
    print(json.dumps(answer, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
