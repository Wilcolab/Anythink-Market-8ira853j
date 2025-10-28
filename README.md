# Image Filter App

A modern web application that allows you to upload images and apply various filters to them, all without saving anything to disk.

## Features

- Easy image upload with drag-and-drop support
- 12 different image filters including:
  - Grayscale
  - Blur
  - Emboss
  - Sharpen
  - Sepia tone
  - And more!
- Real-time side-by-side preview of filtered images
- Download functionality for processed images
- Modern responsive UI
- Zero disk storage (all operations happen in memory)

## Key Technical Aspects

- **Memory-Only Operation**: No images are saved to disk at any point
- **Real-Time Filtering**: All filters are applied instantly with side-by-side preview
- **Base64 Encoding**: Images are stored and transferred as base64-encoded strings
- **Optimized Image Processing**: Large images are automatically resized for better performance

## Requirements

- Python 3.7 or higher

## Installation

1. Clone the repository:

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:

```bash
python main.py
```

2. Open your web browser and go to: http://localhost:31337
3. Upload an image by clicking the "Select Image" button or by dragging and dropping
4. Click on any filter to instantly see the result
5. Download the filtered image if desired

## Architecture

- **Frontend**: Modern HTML/CSS/JS with responsive design
- **Backend**: FastAPI with Jinja2 templating
- **Image Processing**: PIL/Pillow library for applying filters
- **Data Flow**:
  1. Images are uploaded and stored in memory (never on disk)
  2. Filters are applied to in-memory images
  3. Filtered images are sent to the browser as base64-encoded data
  4. Downloads are generated on-demand directly from memory


## Technologies Used

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Image Processing**: Pillow (PIL)
- **Templating**: Jinja2

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
