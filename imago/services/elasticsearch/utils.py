def build_media_url(db: str, media_id: str) -> str:
    """Function to construct media url for photo access.

    db: database name
    media_id: media id
    """
    return f"https://www.imago-images.de/bild/{db}/{media_id.zfill(10)}/s.jpg"
