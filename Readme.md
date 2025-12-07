# YouTube to Blog Converter

A desktop application that fetches YouTube video transcripts and converts them into structured blog posts using AI.

## Features

- **Transcript Fetching:** Automatically retrieves transcripts from YouTube videos.
- **AI Generation:** Converts raw transcripts into Professional, Casual, Educational, or Story-mode blog posts.
- **History & Management:** Tracks generated files with a built-in history viewer.
- **Markdown Support:** Renders output in rich HTML/Markdown.

## Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/LonelyGuy-SE1/Link2Blog.git
    cd Link2Blog
    ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    _(Note: Ensure `wxPython` is installed for your system)_

3.  **Environment Variables:**
    Create a `.env` file in the root directory:
    ```
    GRADIENT_API_KEY=your_api_key_here
    ```
    (You can modify `ai.py` to use other AI providers too!)

## Usage

1.  Run the application:
    ```bash
    python main.py
    ```
2.  Paste a YouTube URL and click **Fetch Transcript**.
3.  Select a style and click **Generate**.
4.  Copy / Save the blog post locally.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
