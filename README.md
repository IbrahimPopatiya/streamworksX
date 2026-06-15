# 🎬 StreamWorksX

StreamWorksX is a **multi-media processing platform** built with FastAPI. It provides APIs for video/audio downloading and processing, OCR text extraction from images, and persistent storage of media metadata in PostgreSQL.

## ✨ Features

- 📥 Download YouTube videos and playlists
- 🎵 Extract audio from videos/playlists
- 🖼️ OCR text extraction from images (pytesseract)
- 🎞️ Video/audio processing pipelines (FFmpeg, moviepy, pydub)
- 🗄️ Persistent metadata storage with PostgreSQL + SQLAlchemy

## 🛠️ Tech Stack

- **Framework:** FastAPI, Uvicorn
- **Media processing:** FFmpeg, moviepy, ffmpeg-python, pydub, imageio
- **OCR:** pytesseract, Pillow
- **YouTube:** pytube / pytubefix
- **Database:** PostgreSQL, SQLAlchemy, psycopg2
- **Config:** python-dotenv

## ⚙️ Setup

### Prerequisites

- Python 3.10+
- [FFmpeg](https://ffmpeg.org/download.html) installed and available on your `PATH`
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and available on your `PATH`
- PostgreSQL database

### Installation

```bash
git clone https://github.com/IbrahimPopatiya/streamworksX.git
cd streamworksX

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
```

## ▶️ Running the App

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

## 📁 Project Structure

```
.
├── main.py          # FastAPI app & routes
├── crud.py          # Media processing / OCR / download logic
├── database.py      # Database connection setup
├── models.py        # SQLAlchemy models
├── schemas.py        # Pydantic schemas
├── create_table.py  # DB table creation script
├── data/            # Uploaded/downloaded media (ignored)
├── audio/           # Extracted audio (ignored)
└── videos/          # Downloaded videos (ignored)
```

## 📄 License

This project is provided as-is for educational and personal use.
