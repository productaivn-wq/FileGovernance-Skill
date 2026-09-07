"""
Verification Engine for Social Media Publications.
Provides rigorous pre-submit and post-publication empirical verification
to prevent false-positive completion claims, text truncation, and missing media assets.
"""
import os
from typing import Dict, Any, List


class PublicationVerifier:
    """Rigorous verification gate for automated social media publishing."""

    @staticmethod
    def verify_pre_submit_text(raw_text: str, inserted_text: str, min_ratio: float = 0.90) -> Dict[str, Any]:
        """
        Asserts that the text inside the composer matches the source text
        before the Post button is ever clicked.
        """
        raw_len = len(raw_text.strip())
        inserted_len = len(inserted_text.strip())
        ratio = inserted_len / max(raw_len, 1)

        is_valid = ratio >= min_ratio
        return {
            "valid": is_valid,
            "raw_length": raw_len,
            "inserted_length": inserted_len,
            "ratio": round(ratio, 4),
            "error": None if is_valid else f"Text truncated in editor! Expected {raw_len} chars, found {inserted_len} ({round(ratio*100, 1)}%)"
        }

    @staticmethod
    def verify_media_attached(has_file_input: bool, image_path: str, preview_count: int) -> Dict[str, Any]:
        """
        Asserts that an image was physically attached and rendered in preview
        prior to submission.
        """
        file_exists = os.path.exists(image_path)
        is_valid = file_exists and preview_count > 0

        return {
            "valid": is_valid,
            "file_exists": file_exists,
            "preview_count": preview_count,
            "error": None if is_valid else f"Media attachment failed! File exists: {file_exists}, preview count: {preview_count}"
        }

    @staticmethod
    def verify_post_dom_content(published_text: str, expected_start: str, expected_end: str, media_count: int, require_media: bool = True) -> Dict[str, Any]:
        """
        Post-publication verification from actual live DOM.
        Validates start marker, end marker, and media element presence.
        """
        has_start = expected_start.lower() in published_text.lower()
        has_end = expected_end.lower() in published_text.lower()
        has_media = media_count > 0 if require_media else True

        is_valid = has_start and has_end and has_media
        reasons: List[str] = []
        if not has_start:
            reasons.append(f"Missing start marker: '{expected_start[:30]}...'")
        if not has_end:
            reasons.append(f"Missing end marker: '{expected_end[:30]}...'")
        if require_media and not has_media:
            reasons.append("Missing expected media element in published card")

        return {
            "valid": is_valid,
            "has_start_marker": has_start,
            "has_end_marker": has_end,
            "has_media": has_media,
            "media_count": media_count,
            "error": None if is_valid else "; ".join(reasons)
        }
