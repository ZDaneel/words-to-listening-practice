from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv
import logging
from typing import Optional
import time
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SrtTimeAdjuster:
    @staticmethod
    def parse_time(time_str: str) -> datetime:
        return datetime.strptime(time_str, "%H:%M:%S,%f")

    @staticmethod
    def format_time(dt: datetime) -> str:
        return dt.strftime("%H:%M:%S,%f")[:-3]

    def adjust_timestamp(self, time_str: str, adjust_ms: int) -> str:
        dt = self.parse_time(time_str)
        adjusted_dt = dt - timedelta(milliseconds=adjust_ms)
        return self.format_time(adjusted_dt)

    def process_srt(self, content: str, adjust_ms: int = 500) -> str:
        lines = content.strip().split("\n")
        processed_lines = []
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            if line.isdigit():
                processed_lines.append(line)
                i += 1

                if i < len(lines):
                    timestamp_line = lines[i]
                    if "-->" in timestamp_line:
                        start_time, end_time = timestamp_line.split(" --> ")
                        adjusted_start = self.adjust_timestamp(start_time, adjust_ms)
                        adjusted_end = self.adjust_timestamp(end_time, adjust_ms)
                        processed_lines.append(f"{adjusted_start} --> {adjusted_end}")
                    i += 1

                while i < len(lines) and lines[i].strip():
                    processed_lines.append(lines[i])
                    i += 1

                if i < len(lines):
                    processed_lines.append("")
            else:
                i += 1

        return "\n".join(processed_lines)


class TextToSpeech:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found, please check .env file")

        self.voice = os.getenv("VOICE", "nova")
        self.model_chat = os.getenv("MODEL_CHAT", "gpt-4o-mini")
        self.model_tts = os.getenv("MODEL_TTS", "tts-1")
        self.tts_language = os.getenv("TTS_LANGUAGE", "de")
        self.transcribe_prompt = os.getenv(
            "TRANSCRIBE_PROMPT",
            "Transcribe in a complete sentence. Start and end with a period.",
        )
        self.output_dir = os.getenv("OUTPUT_DIR", "output")
        self.speed = float(os.getenv("SPEED", "1.0"))
        self.system_prompt = os.getenv(
            "SYSTEM_PROMPT",
            "You are a German listening comprehension article generation assistant. Based on the German words or phrases provided by the user, separated by commas, generate a listening article at the C1-C2 level. Requirements: 1. Use natural spoken German, including appropriate colloquial expressions and conjunctions. 2. Include interjections, filler words, and other spoken features. 3. Simulate the language style of an academic lecture or report, with topics covering society, technology, the environment, education, etc. 4. All provided words or phrases must be integrated naturally. 5. Ensure the article has a clear theme and logical structure. 6. Can include speaker pauses, repetitions, or self-corrections as real speech characteristics. 7. Use complex sentence structures common in DSH exams, such as clauses, passive voice, and subjunctive mood.",
        )
        self.time_adjust_ms = int(os.getenv("TIME_ADJUST_MS", "300"))

        self.client = OpenAI()
        self.available_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        self.valid_extensions = {".mp3", ".wav", ".ogg"}
        self.min_speed = 0.25
        self.max_speed = 4.0

        self.srt_adjuster = SrtTimeAdjuster()

    def validate_text(self, text: str) -> bool:
        if not text or not text.strip():
            logger.error("Input text cannot be empty")
            return False
        return True

    def validate_voice(self, voice: str) -> bool:
        if voice.lower() not in self.available_voices:
            logger.error(
                f"Unsupported voice type. Available options: {', '.join(self.available_voices)}"
            )
            return False
        return True

    def validate_speed(self, speed: float) -> bool:
        if not self.min_speed <= speed <= self.max_speed:
            logger.error(f"Speed must be between {self.min_speed} and {self.max_speed}")
            return False
        return True

    def create_output_path(
        self, output_dir: str, filename: str, extension: str
    ) -> Path:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        if not extension.startswith("."):
            extension = f".{extension}"

        if extension not in self.valid_extensions:
            extension = ".mp3"

        return output_path / f"{filename}{extension}"

    def generate_text(
        self, user_input: str, model: Optional[str] = None
    ) -> Optional[str]:
        try:
            model = model or self.model_chat
            response = self.client.chat.completions.with_raw_response.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input},
                ],
                model=model,
            )
            completion = response.parse()
            generated_text = completion.choices[0].message.content

            logger.info("Text generation completed.")
            return generated_text

        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            return None

    def words_to_speech(
        self,
        text: str,
        voice: Optional[str] = None,
        output_dir: Optional[str] = None,
        filename: Optional[str] = None,
        extension: str = ".mp3",
        model: Optional[str] = None,
        speed: Optional[float] = None,
    ) -> Optional[Path]:

        try:
            voice = voice or self.voice
            output_dir = output_dir or self.output_dir
            model = model or self.model_tts
            speed = speed if speed is not None else self.speed

            if (
                not self.validate_text(text)
                or not self.validate_voice(voice)
                or not self.validate_speed(speed)
            ):
                return None

            if not filename:
                filename = text[:20].replace(" ", "_")

            output_path = self.create_output_path(output_dir, filename, extension)
            logger.info(f"Start generating speech... (speed: {speed}x)")

            response = self.client.audio.speech.create(
                model=model, voice=voice.lower(), input=text, speed=speed
            )

            response.stream_to_file(output_path)

            logger.info(f"Speech generation completed! File saved at: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error generating speech: {str(e)}")
            return None

    def validate_file(self, file_path: str) -> bool:
        path = Path(file_path)

        if not path.exists():
            logger.error(f"File does not exist: {file_path}")
            return False

        valid_extensions = {".mp3", ".wav", ".m4a", ".mp4"}
        if path.suffix.lower() not in valid_extensions:
            logger.error(
                f"Unsupported file format. Supported formats: {', '.join(valid_extensions)}"
            )
            return False

        return True

    def transcribe(self, file_path: str) -> Optional[Path]:
        try:
            if not self.validate_file(file_path):
                return None

            logger.info("Start transcribing audio...")

            with open(file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    language=self.tts_language,
                    prompt=self.transcribe_prompt,
                    response_format="srt",
                    file=audio_file,
                )

            adjusted_transcript = self.srt_adjuster.process_srt(
                transcript, self.time_adjust_ms
            )

            output_path = Path(file_path).with_suffix(".srt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(adjusted_transcript)

            logger.info(f"Transcription completed! Results saved to: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            return None

    def process_words_to_speech(
        self, user_input: str, speed: Optional[float] = None
    ) -> Optional[Path]:

        if not user_input:
            logger.error("Input text cannot be empty")
            return None

        generated_text = self.generate_text(user_input)
        if not generated_text:
            return None

        filename = user_input[:20].replace(" ", "_")
        audio_file_path = self.words_to_speech(
            text=generated_text, speed=speed, filename=filename
        )
        return audio_file_path

    def process_speech_to_srt(self, audio_file_path: str) -> Optional[Path]:
        if not audio_file_path:
            logger.error("Audio file path cannot be empty")
            return None

        srt_file_path = self.transcribe(audio_file_path)
        return srt_file_path

    def direct_text_to_speech_and_srt(
        self,
        text: str,
        voice: Optional[str] = None,
        output_dir: Optional[str] = None,
        filename: Optional[str] = None,
        extension: str = ".mp3",
        model: Optional[str] = None,
        speed: Optional[float] = None,
    ) -> tuple[Optional[Path], Optional[Path]]:
        try:
            audio_file_path = self.words_to_speech(
                text=text,
                voice=voice,
                output_dir=output_dir,
                filename=filename,
                extension=extension,
                model=model,
                speed=speed,
            )

            if not audio_file_path:
                logger.error("Failed to generate audio file")
                return None, None

            srt_file_path = self.transcribe(str(audio_file_path))

            if not srt_file_path:
                logger.error("Failed to generate SRT file")
                return audio_file_path, None

            return audio_file_path, srt_file_path

        except Exception as e:
            logger.error(f"Error in direct text to speech and srt conversion: {str(e)}")
            return None, None
