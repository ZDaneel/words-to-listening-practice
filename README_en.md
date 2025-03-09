# words-to-listening-practice
[![GitHub license](https://img.shields.io/github/license/ZDaneel/words-to-listening-practice)](https://github.com/ZDaneel/words-to-listening-practice/blob/main/LICENSE)

[简体中文](./README.md) · **English**

Many people may be like me, having much better reading skills than listening skills. This is mainly due to a lack of vocabulary in listening. The usual approach is to write it down, look up the meaning, and try to memorize it, but just because I can understand and memorize it doesn't mean I can comprehend it when I hear it. In the next listening practice, I may still be unable to react quickly. This requires practice in a new context, but in the past, it was usually difficult to achieve such practice.

So, is it possible to generate practice articles based on given vocabulary and be able to listen to them sentence by sentence?

## Final effect

![image-20250103194812282](https://cdn.jsdelivr.net/gh/ZDaneel/cloudimg@main/img/202501031948106.png)

## Prerequisites

- OpenAI-API: [Pricing Catalog](https://openai.com/api/pricing/)
	- GPT-4o mini: Article generation. Does not require a very good model for generating articles.

	- TTS: Text to speech. Expensive, but currently the best effect on the market.

	- Whisper: Speech to subtitle, relatively expensive.

- [Language Reactor](https://www.languagereactor.com): Browser plugin that supports sentence-by-sentence listening.

## Functions

This script supports the following tasks:

1. **words_to_speech**: Converts multiple input words into audio files.

2. **speech_to_srt**: Transcribes audio files into SRT subtitle files.

3. **words_to_speech_and_srt**: Converts input words into audio files and generates corresponding SRT subtitle files.

4. **text_to_speech_and_srt**: Directly converts input text into speech and generates SRT files.

## Install

1. **Clone Repository:**

```bash
git clone https://github.com/ZDaneel/words-to-listening-practice.git
cd words-to-listening-practice
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Configuration**

-   Copy the `.env.example` file and rename it to `.env`.
- Edit the `.env` file to fill in the OpenAI API key and other configuration information:

```
OPENAI_API_KEY=OpenAI API key # Required
OUTPUT_DIR=Output file save directory # Required
VOICE=shimmer # TTS voice, optional values see below
MODEL_CHAT=gpt-4o-mini # GPT model for text generation
MODEL_TTS=tts-1 # TTS model for text-to-speech
TTS_LANGUAGE=de # Target language code (e.g., de, en, fr, es, zh)
TRANSCRIBE_PROMPT="Transcribe in a complete sentence. Start and end with a period." # Transcription prompt
SPEED=1.0 # Speech playback speed (1.0 is normal speed)
TIME_ADJUST_MS=10 # Subtitle timestamp adjustment (milliseconds)
SYSTEM_PROMPT0="......" # System prompt for generating listening articles (customizable as needed)
```

**Optional `VOICE` values:**

-   `alloy`
-   `echo`
-   `fable`
-   `onyx`
-   `nova`
-   `shimmer`

## Usage

Run the following command in the command line:

```bash
python main.py --task <task> [options]
```

**Usage example:**

1. **Convert multiple words to speech and generate SRT:**

```
python main.py --task words_to_speech_and_srt --input-text "Nachhaltigkeit,Umweltbewusstsein,Energiewende" --speed 1.5
```

2. **Convert a piece of text to speech**

```
python main.py --task text_to_speech --input-text "This is the text to be converted to speech."
```

3. **Transcribe existing audio files to SRT:**

```
python main.py --task speech_to_srt --audio-file my_audio.mp3
```

4. **Directly convert a segment of text to speech and SRT.**

```
python main.py --task text_to_speech_and_srt --input-text "This is the text to be converted into speech and subtitles."
```
