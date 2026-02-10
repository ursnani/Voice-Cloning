# 🎙️ Voice Cloning Application

A Python-based voice cloning application that allows you to record your voice and generate speech in your cloned voice using AI.

## Features

- 🎤 **Voice Recording**: Record your voice directly through the web interface
- 💾 **Voice Storage**: Save your voice samples locally
- 🤖 **AI Voice Cloning**: Clone your voice using ElevenLabs API
- 🎵 **Text-to-Speech**: Generate speech from text in your cloned voice
- 🌐 **Web Interface**: Easy-to-use Gradio-based UI

## Requirements

- Python 3.8 or higher
- ElevenLabs API key ([Get one here](https://elevenlabs.io/))
  - Free tier includes 10,000 characters/month

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. **Start the application**:
```bash
python app.py
```

2. **Open your browser** and navigate to:
```
http://127.0.0.1:7860
```

3. **Record your voice**:
   - Click on the microphone button
   - Speak for at least 10-15 seconds for best results
   - Click "Save Voice" to store your recording

4. **Enter your API key**:
   - Paste your ElevenLabs API key in the designated field
   - Get your free API key at [elevenlabs.io](https://elevenlabs.io/)

5. **Generate speech**:
   - Type the text you want to convert to speech
   - Click "Generate Speech (Basic)" for standard text-to-speech
   - Or click "Generate with Voice Clone (Pro)" for advanced voice cloning (requires paid plan)

## How It Works

### Basic Method
Uses ElevenLabs' standard text-to-speech with voice settings optimized for similarity to your recording.

### Professional Method
Creates a custom voice clone from your sample using ElevenLabs' Voice Design API (requires paid subscription).

## File Structure

```
Voice Cloning/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── voices/            # Directory for saved voice recordings
└── generated_speech.mp3  # Output file for generated speech
```

## API Key Setup

1. Go to [ElevenLabs](https://elevenlabs.io/)
2. Sign up for a free account
3. Navigate to your profile settings
4. Copy your API key
5. Paste it in the application interface

## Troubleshooting

### "Invalid API key" error
- Verify your API key is correct
- Check that you have an active ElevenLabs account

### "API quota exceeded" error
- You've reached your monthly character limit
- Upgrade your plan or wait for the next billing cycle

### "Voice cloning requires a paid plan" error
- The Professional Voice Clone feature requires a paid ElevenLabs subscription
- Use the Basic method instead, which works with the free tier

## Tips for Best Results

- **Recording Quality**: Speak clearly in a quiet environment
- **Recording Length**: Record at least 10-15 seconds of speech
- **Varied Speech**: Include different tones and emotions in your recording
- **Text Input**: Start with shorter sentences to test the quality

## License

This project is for educational and personal use.

## Credits

- Built with [Gradio](https://gradio.app/)
- Powered by [ElevenLabs](https://elevenlabs.io/) API
