"""
Cannot be run on Python 3.13+
Detect document language using Apache Tika for text extraction
and fastText pre-trained language identification model.
"""

# pip install tika requests
# pip install fasttext-wheel   (often best on Windows)
# pip install langcodes

from __future__ import annotations

import langcodes
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

import requests
from tika import parser

MODEL_URL_FTZ = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz"

def language_name(code: str) -> str:
    try:
        return langcodes.Language.get(code).display_name()
    except Exception:
        return code


def ensure_fasttext_installed():
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


def extract_text_with_tika(file_path: Path) -> Tuple[str, Dict[str, Any]]:
    parsed = parser.from_file(str(file_path))
    text = (parsed.get("content") or "").strip()
    metadata = parsed.get("metadata") or {}
    return text, metadata


def normalize_text_for_lid(text: str, max_chars: int = 50_000) -> str:
    """
    Fast language ID works best on a moderate sample of clean text.
    - collapse whitespace
    - trim to max_chars to keep it fast/robust
    """
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_chars:
        text = text[:max_chars]
    return text


def detect_language_fasttext(
    text: str,
    model_path: Path,
    top_k: int = 3,
) -> List[Tuple[str, float]]:
    import fasttext

    model = fasttext.load_model(str(model_path))
    labels, probs = model.predict(text, k=top_k)

    # labels look like "__label__en"
    results = [(lbl.replace("__label__", ""), float(p)) for lbl, p in zip(labels, probs)]
    return results


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

    text, metadata = extract_text_with_tika(file_path)

    if not text:
        return {
            "file": str(file_path),
            "tika_metadata_language": metadata.get("language"),
            "fasttext_predictions": [],
            "note": "No extractable text found by Tika (empty content).",
        }

    text_norm = normalize_text_for_lid(text, max_chars=max_chars)
    preds = detect_language_fasttext(text_norm, model_path=model_path, top_k=top_k)

    return {
        "file": str(file_path),
        "tika_metadata_language": metadata.get("language"),
        "fasttext_predictions": [
            {
                "lang": lang,
                "lang_name": language_name(lang),
                "prob": prob,
            }
            for lang, prob in preds
        ],
        "chars_used": len(text_norm),
    }


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        return 2

    for fp in argv[1:]:
        try:
            result = detect_file_language(fp)
            print(f"\nFile: {result['file']}")
            print(f"Tika metadata language: {result['tika_metadata_language']}")
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
    folder = "test_files"
    file_path = "test_files\\sample test.pdf" # Change to your test file path
    result = detect_file_language(file_path)
    if result["fasttext_predictions"]:
        top = result["fasttext_predictions"][0]
        print("The language detected is:", top["lang_name"], f"({top['lang']})")
    else:
        print("No language detected (no extractable text) for", file_path)
    raise SystemExit(main(sys.argv))
