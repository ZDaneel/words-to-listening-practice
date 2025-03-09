# words-to-listening-practice
[![GitHub license](https://img.shields.io/github/license/ZDaneel/words-to-listening-practice)](https://github.com/ZDaneel/words-to-listening-practice/blob/main/LICENSE)

 **简体中文** · [English](./README_en.md)

很多人可能和我一样，阅读能力比听力好很多。主要是因为听力词汇匮乏，通常的做法是记录下来、查询意思并试图记忆，但是看懂了会背了不代表能听懂，在下次听力练习中仍然可能无法快速反应过来。就需要在新的语境下练习，但是在过去通常很难实现这样的练习。

那么，能否通过给定的词汇，生成练习的文章，并且能够逐句精听呢？

## 最终效果

![image-20250103194812282](https://cdn.jsdelivr.net/gh/ZDaneel/cloudimg@main/img/202501031948106.png)

## 前置要求

- OpenAI-API: [价格目录](https://openai.com/api/pricing/)
	- GPT-4o mini：文章生成。便宜，生成文章不需要太好的模型
	- TTS：文字转语音。贵，但目前的效果市面上几乎最好
	- Whisper：语音转字幕，价格偏贵
- [Language Reactor](https://www.languagereactor.com): 浏览器插件，能够支持逐句精听

## 功能

该脚本支持以下任务：

1.  **words\_to\_speech**: 将输入的多个单词转换为语音文件。
2.  **speech\_to\_srt**: 将音频文件转录为 SRT 字幕文件。
3.  **words\_to\_speech\_and\_srt**: 将输入的单词转换为语音文件，并生成相应的 SRT 字幕文件。
4.  **text\_to\_speech\_and\_srt**: 将输入的文本直接转换为语音并生成 SRT 文件。

## 安装

1. **克隆仓库:**

```bash
git clone https://github.com/ZDaneel/words-to-listening-practice.git
cd words-to-listening-practice
```

2. **安装依赖:**

```bash
pip install -r requirements.txt
```

3. **配置**

-   复制 `.env.example` 文件并重命名为 `.env`。
-   编辑 `.env` 文件，填入OpenAI API 密钥和其他配置信息：

```
OPENAI_API_KEY=OpenAI API密钥  # 必填
OUTPUT_DIR=输出文件保存目录      # 必填，例如：output
VOICE=shimmer                  # TTS 语音，可选值见下文
MODEL_CHAT=gpt-4o-mini            # 用于生成文本的 GPT 模型
MODEL_TTS=tts-1                 # 用于文本转语音的 TTS 模型
TTS_LANGUAGE=de                 # 目标语言代码 (例如：de, en, fr, es, zh)
TRANSCRIBE_PROMPT="Transcribe in a complete sentence. Start and end with a period."  # 转录提示语
SPEED=1.0                       # 语音播放速度 (1.0 为正常速度)
TIME_ADJUST_MS=10               # 字幕时间戳调整 (毫秒)
SYSTEM_PROMPT0="......"     # 用于生成听力文章的系统提示 (根据需要定制)
```

**可选的 `VOICE` 值:**

-   `alloy`
-   `echo`
-   `fable`
-   `onyx`
-   `nova`
-   `shimmer`

## 使用方法

在命令行中运行以下命令： 

```bash
python main.py --task <任务> [选项]
```

**使用示例:**

1. **将多个单词转换为语音并生成 SRT:**

```
python main.py --task words_to_speech_and_srt --input-text "Nachhaltigkeit,Umweltbewusstsein,Energiewende" --speed 1.5
```

2. **将一段文本转为语音**

```
python main.py --task text_to_speech --input-text "这是希望转为语音的文本"
```

3. **将已有的音频文件转录为 SRT:**

```
python main.py --task speech_to_srt --audio-file my_audio.mp3
```

4. **直接将一段文本转为语音和srt**

```
python main.py --task text_to_speech_and_srt --input-text "这是希望转为语音和字幕的文本"
```

