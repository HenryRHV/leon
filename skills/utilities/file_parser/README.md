# File Parser Skill

This skill extracts basic information from a variety of common file types. It works entirely offline once the required Python packages are installed.

## Supported Formats

- `.xmind`
- `.pdf`
- `.docx`
- `.txt`
- `.xlsx`
- `.eml`
- `.mp4`
- `.png`, `.jpg`

## Dependencies

Install the following packages inside your Python environment:

```sh
pip install PyPDF2 python-docx openpyxl xmindparser Pillow
```

`ffprobe` from FFmpeg is also required for MP4 metadata extraction.

## Usage

Invoke the `analyze` action with the path to a file. Leon will respond with a short summary or metadata extracted from the file.
