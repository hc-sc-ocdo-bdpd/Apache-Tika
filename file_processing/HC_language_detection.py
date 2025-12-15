"""
Detect document language using repo File extraction (no Apache Tika)
and fastText pre-trained language identification model.

- pip install requests
- pip install fasttext-wheel   (often best on Windows)
- pip install langcodes
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

import langcodes
import requests

from file_processing import File 

MODEL_URL_FTZ = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz"

# -----------------------------
# Human-readable language names
# -----------------------------
def language_name(code: str) -> str:
    try:
        return langcodes.Language.get(code).display_name()
    except Exception:
        return code


# -----------------------------
# fastText install + model download
# -----------------------------
def ensure_fasttext_installed() -> None:
    try:
        import fasttext  # noqa: F401
    except ImportError as e:
        raise ImportError(
            "fasttext is not installed.\n"
            "Try:\n"
            "  pip install fasttext-wheel   (often best on Windows)\n"
            "or:\n"
            "  pip install fasttext\n"
        ) from e


def download_model(model_path: Path, url: str = MODEL_URL_FTZ) -> None:
    model_path.parent.mkdir(parents=True, exist_ok=True)
    if model_path.exists():
        return

    print(f"Downloading fastText model to: {model_path}")
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(model_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)


# -----------------------------
# Text extraction via repo File
# -----------------------------
def extract_text_with_repo_file(file_path: Path) -> Tuple[str, Dict[str, Any]]:
    """
    Uses your repository's File class to extract metadata and text.
    Assumes text lives at file.metadata["text"].
    """
    f = File(str(file_path))

    # your example: file.metadata.get('text', 'No text extracted')
    text = (f.metadata.get("text") or "").strip()

    # Keep metadata for debugging / parity with previous interface
    # Add anything you want here
    metadata: Dict[str, Any] = dict(f.metadata) if isinstance(f.metadata, dict) else {}
    metadata.update(
        {
            "file_name": getattr(f, "file_name", None),
            "size": getattr(f, "size", None),
            "owner": getattr(f, "owner", None),
        }
    )

    return text, metadata


# -----------------------------
# Pre-processing for fastText
# -----------------------------
def normalize_text_for_lid(text: str, max_chars: int = 50_000) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars] if len(text) > max_chars else text


# -----------------------------
# fastText prediction (cached model)
# -----------------------------
_FASTTEXT_MODEL = None

def _get_fasttext_model(model_path: Path):
    global _FASTTEXT_MODEL
    import fasttext

    if _FASTTEXT_MODEL is None:
        _FASTTEXT_MODEL = fasttext.load_model(str(model_path))
    return _FASTTEXT_MODEL


def detect_language_fasttext(
    text: str,
    model_path: Path,
    top_k: int = 3,
) -> List[Tuple[str, float]]:
    model = _get_fasttext_model(model_path)
    labels, probs = model.predict(text, k=top_k)
    return [(lbl.replace("__label__", ""), float(p)) for lbl, p in zip(labels, probs)]


# -----------------------------
# Public function: detect language for a file
# -----------------------------
def detect_file_language(
    file_path: str | Path,
    model_path: str | Path = "models/lid.176.ftz",
    top_k: int = 3,
    max_chars: int = 50_000,
) -> Dict[str, Any]:
    ensure_fasttext_installed()

    file_path = Path(file_path)
    model_path = Path(model_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    download_model(model_path)

    text, metadata = extract_text_with_repo_file(file_path)

    if not text:
        return {
            "file": str(file_path),
            "repo_metadata": metadata,
            "fasttext_predictions": [],
            "note": "No extractable text found by repo File extractor (empty content).",
        }

    text_norm = normalize_text_for_lid(text, max_chars=max_chars)
    preds = detect_language_fasttext(text_norm, model_path=model_path, top_k=top_k)

    return {
        "file": str(file_path),
        "repo_metadata": metadata,
        "fasttext_predictions": [
            {"lang": lang, "lang_name": language_name(lang), "prob": prob}
            for lang, prob in preds
        ],
    }


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("Usage: python file_langdetect.py <file1> [file2 ...]")
        return 2

    for fp in argv[1:]:
        try:
            result = detect_file_language(fp)
            print(f"\nFile: {result['file']}")

            # Optional: show some repo metadata to confirm extraction path worked
            md = result.get("repo_metadata", {}) or {}
            print(f"File Name: {md.get('file_name')}")
            print(f"File Size: {md.get('size')} bytes")
            print(f"Owner: {md.get('owner')}")

            if result["fasttext_predictions"]:
                print("fastText predictions:")
                for p in result["fasttext_predictions"]:
                    print(f"  - {p['lang_name']} ({p['lang']}): {p['prob']:.4f}")
                print(f"Chars used: {result.get('chars_used')}")
            else:
                print(f"Note: {result.get('note')}")
        except Exception as e:
            print(f"\nFile: {fp}\nERROR: {e}")

    return 0


if __name__ == "__main__":
    file_path = r"test_files\sample test.pdf"  # change me
    result = detect_file_language(file_path)

    if result["fasttext_predictions"]:
        top = result["fasttext_predictions"][0]
        print("The language detected is:", top["lang_name"], f"({top['lang']})", "for", file_path)
    else:
        print("No language detected (no extractable text) for", file_path)

    raise SystemExit(main(sys.argv))