import argparse
import logging
from tts_module import TextToSpeech

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Text-to-Speech and Speech-to-SRT CLI")

    parser.add_argument(
        "--task",
        type=str,
        required=True,
        choices=[
            "words_to_speech",
            "speech_to_srt",
            "words_to_speech_and_srt",
            "text_to_speech_and_srt",
        ],
        help="Choose the task to perform: words_to_speech | speech_to_srt | words_to_speech_and_srt | text_to_speech_and_srt",
    )

    parser.add_argument(
        "--speed",
        type=float,
        default=None,
        help="Playback speed multiplier (0.25-4.0). Defaults to the environment variable or 1.0",
    )

    parser.add_argument("--input-text", type=str, help="Text for converting to speech")

    parser.add_argument(
        "--audio-file",
        type=str,
        help="Path to the audio file for transcription (output SRT)",
    )

    args = parser.parse_args()

    tts = TextToSpeech()

    if args.task == "words_to_speech":
        if not args.input_text:
            logger.error("The 'words_to_speech' task requires --input-text")
            return

        audio_file_path = tts.process_words_to_speech(
            user_input=args.input_text, speed=args.speed
        )
        if audio_file_path:
            print(f"[DONE] Speech generation completed. File saved: {audio_file_path}")

    elif args.task == "speech_to_srt":
        if not args.audio_file:
            logger.error("The 'speech_to_srt' task requires --audio-file")
            return

        srt_file_path = tts.process_speech_to_srt(audio_file_path=args.audio_file)
        if srt_file_path:
            print(f"[DONE] Transcription completed. SRT file saved: {srt_file_path}")

    elif args.task == "words_to_speech_and_srt":
        if not args.input_text:
            logger.error("The 'words_to_speech_and_srt' task requires --input-text")
            return

        audio_file_path = tts.process_words_to_speech(
            user_input=args.input_text, speed=args.speed
        )
        if audio_file_path:
            srt_file_path = tts.process_speech_to_srt(
                audio_file_path=str(audio_file_path)
            )
            if srt_file_path:
                print("[DONE] Words to speech and srt completed:")
                print(f"       Audio file: {audio_file_path}")
                print(f"       SRT file: {srt_file_path}")

    elif args.task == "text_to_speech_and_srt":
        if not args.input_text:
            logger.error("The 'text_to_speech_and_srt' task requires --input-text")
            return

        audio_file_path, srt_file_path = tts.direct_text_to_speech_and_srt(
            text=args.input_text, speed=args.speed
        )

        if audio_file_path and srt_file_path:
            print("[DONE] Text to speech and srt")
            print(f"       Audio file: {audio_file_path}")
            print(f"       SRT file: {srt_file_path}")
    else:
        logger.error("Audio generation failed; cannot proceed with transcription.")


if __name__ == "__main__":
    main()
