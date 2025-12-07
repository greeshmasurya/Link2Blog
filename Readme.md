# YouTube Video to Blog Converter

A desktop application that fetches YouTube video transcripts and converts them into structured blog posts using AI.

## Features

- **Transcript Fetching:** Automatically retrieves transcripts from YouTube videos.
- **AI Generation:** Converts raw transcripts into Professional, Casual, Educational, or Story-mode blog posts.
- **History & Management:** Tracks generated files with a built-in history viewer.
- **Markdown Support:** Renders output in rich HTML/Markdown.

## Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/greeshmasurya/Link2Blog.git
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
    <img width="1366" height="730" alt="image" src="https://github.com/user-attachments/assets/cce83be7-72eb-413b-87a2-ddab967ffed9" />

2.  Paste a YouTube URL and click **Fetch Transcript**.

    <img width="1366" height="730" alt="image" src="https://github.com/user-attachments/assets/11b79554-6cf4-475b-980b-f178edea6b27" />

3.  Select a style and click **Generate**.

    <img width="1366" height="732" alt="image" src="https://github.com/user-attachments/assets/eb759986-bd12-44cb-af80-d3731af9b4c2" />
     
4.  Copy / Save the blog post locally.

   <img width="1366" height="730" alt="image" src="https://github.com/user-attachments/assets/f3e7a832-e6b5-4548-a692-736af056e1ad" />

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
