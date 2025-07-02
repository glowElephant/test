# Character Customization Prototype

This repository contains a minimal prototype for a character customization service.
The `app.py` server exposes simple endpoints for listing packages, purchasing
items with points, and uploading images. Uploaded images are saved in two
directories:

* `web_images/` – optimized WebP images used for the UI
* `pod_images/` – high‑resolution originals for POD printing

The database schema is defined in `schema.sql` and implemented via SQLAlchemy in
`app.py`.

## Quick Start

```bash
pip install flask sqlalchemy pillow
python app.py
```

The server starts on `http://localhost:5000`.
