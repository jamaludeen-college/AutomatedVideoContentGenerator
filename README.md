# 🎬 AI Video Generator (Text-to-Video)

**Turn simple text topics into engaging short videos instantly!** 🚀

This project is a fully automated pipeline that generates YouTube Shorts/Reels style videos from a simple text prompt. It handles everything: Scriptwriting, Audio generation, Stock footage searching, Subtitling, and Video Editing.

---

## 🔥 Features (Idhu enna pannum?)

* 🧠 **Smart Scripting:** Uses **OpenAI GPT-4o** or **Groq (Llama-3)** to write engaging scripts.
* 🗣️ **Realistic Voiceover:** Generates high-quality AI voices using **Edge TTS** (with automatic fallback to Google TTS).
* 🎥 **Dynamic Visuals:** Automatically searches and downloads relevant HD stock footage from **Pexels API**.
* 📝 **Auto-Captions:** Generates word-level timed subtitles using **OpenAI Whisper**.
* 🎬 **Auto-Editing:** Stitches video, audio, and text together using **MoviePy**.
* 🖥️ **Dual Interface:** Run it via **Command Line (CLI)** or a beautiful **Streamlit Web UI**.

---

## 🛠️ Tech Stack (Tools & Weapons)

* **Language:** Python 3.10+
* **AI Models:** OpenAI GPT-4o, Groq Llama-3, Whisper
* **Media Processing:** MoviePy, ImageMagick, Pydub, FFMPEG
* **APIs:** Pexels (Video), OpenAI/Groq (Text)
* **Interface:** Streamlit

---

## ⚙️ Prerequisites (Mudhalla idhu venum)

Before running the project, make sure you have:

1.  **Python 3.8+** installed.
2.  **ImageMagick** installed (Crucial for text rendering on Windows).
    * [Download Here](https://imagemagick.org/script/download.php#windows)
    * *Note:* During installation, check the box **"Install legacy utilities (e.g. convert)"**.
3.  **API Keys:**
    * [OpenAI API Key](https://platform.openai.com/)
    * [Pexels API Key](https://www.pexels.com/api/)
    * [Groq API Key](https://console.groq.com/) (Optional, for faster/cheaper scripts)

---

## 🚀 Installation (Epdi Install panradhu?)

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Text-To-Video-AI.git](https://github.com/YOUR_USERNAME/Text-To-Video-AI.git)
    cd Text-To-Video-AI
    ```

2.  **Create a Virtual Environment (Recommended)**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables**
    Create a file named `.env` in the root directory and add your keys:
    ```env
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
    GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
    PEXELS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

---

## 🏃‍♂️ Usage (Epdi Run panradhu?)

You have two ways to run this project:

### Option 1: The "Showroom" Mode (Web UI) 🖥️
Best for easy usage and visualization.

```bash
streamlit run streamlit_app.py

Mode (CLI):
python app.py "Why is the ocean salty?"

📂 Project Structure

📦 Text-To-Video-AI/
├── app.py                   # CLI Entry Point
├── streamlit_app.py         # Web UI Entry Point
├── .env                     # API Keys (Don't share this!)
├── rendered_video.mp4       # Final Output
├── utility/
│   ├── script/              # Script generation logic
│   ├── audio/               # TTS logic (EdgeTTS + Fallback)
│   ├── captions/            # Whisper timestamp logic
│   ├── video/               # Pexels search & keyword extraction
│   └── render/              # MoviePy editing engine
└── requirements.txt         # Python dependencies
