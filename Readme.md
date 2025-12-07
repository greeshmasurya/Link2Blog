# YouTube Video to Blog Converter

A desktop application that fetches YouTube video transcripts and converts them into structured blog posts using AI.

## Features

- **Transcript Fetching:** Automatically retrieves transcripts from YouTube videos.
- **AI Generation:** Converts raw transcripts into Professional, Casual, Educational, or Story-mode blog posts.
- **History & Management:** Tracks generated files with a built-in history viewer.
- **Markdown Support:** Renders output in rich HTML/Markdown.

## PROBLEM STATEMENT
Manually converting YouTube video transcripts into well-structured blog posts demands considerable
time and effort. It involves organizing raw transcripts, formatting them cleanly, and adapting the tone or
writing style. For creators, educators, and bloggers, an automated tool that fetches transcripts and
transforms them into polished blog posts can significantly improve workflow efficiency.

## APPROACH / METHODOLOGY

### Architecture
- **GUI Framework:** wxPython for the desktop interface  
- **API Integration:** Gradient AI API (This can be changed to any other popular providers too; the format is OpenAI-compatible.)  
- **Modular Design:** Individual modules for transcript handling, AI processing, storage, and UI  

### Data Structures Used
- **Lists** → storing generation history  
- **Dictionaries / JSON** → API requests, responses, config files  
- **Strings** → formatting and processing transcript text  

### Workflow
1. User enters a YouTube video URL  
2. Transcript retrieved via `youtube-transcript-api`  
3. Transcript processed and sent to AI with selected writing style  
4. AI returns a structured blog post (title, sections, insights, conclusion)  
5. Output displayed in HTML/Markdown format  
6. User can save with custom filename and folder location  

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


### SAMPLE/DEMO Snapshots.

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

## CHALLENGES FACED
1. Formatting raw data received from the AI  
2. Designing a minimal yet easy-to-understand/use GUI  

## SCOPE FOR IMPROVEMENT
1. Add multilingual transcript support  
2. Enable batch processing for multiple URLs  
3. Support additional AI model providers directly  
4. Allow exporting to PDF, DOCX, and HTML  
5. Add custom user-defined templates  
6. Build analytics dashboard for history and insights  
7. Introduce cloud sync for storing generated blogs  

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
