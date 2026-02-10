import gradio as gr
import os
from pathlib import Path
import soundfile as sf
import numpy as np
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

# Create voices directory if it doesn't exist
VOICES_DIR = Path("voices")
VOICES_DIR.mkdir(exist_ok=True)

# Global variable to store the saved voice path
saved_voice_path = None


def save_voice(audio_tuple):
    """
    Save the recorded audio to the voices directory.
    
    Args:
        audio_tuple: Tuple of (sample_rate, audio_data) from Gradio microphone
    
    Returns:
        str: Status message
    """
    global saved_voice_path
    
    if audio_tuple is None:
        return "❌ No audio recorded. Please record your voice first."
    
    try:
        sample_rate, audio_data = audio_tuple
        
        # Generate filename
        voice_filename = VOICES_DIR / "my_voice.wav"
        
        # Save audio file
        sf.write(str(voice_filename), audio_data, sample_rate)
        saved_voice_path = str(voice_filename)
        
        return f"✅ Voice saved successfully to {voice_filename}!"
    
    except Exception as e:
        return f"❌ Error saving voice: {str(e)}"


def clone_and_speak(text, api_key):
    """
    Clone the saved voice and generate speech from text using ElevenLabs API.
    
    Args:
        text: The text to convert to speech
        api_key: ElevenLabs API key
    
    Returns:
        tuple: (audio_path, status_message)
    """
    global saved_voice_path
    
    # Validation
    if not text or text.strip() == "":
        return None, "❌ Please enter some text to generate speech."
    
    if not api_key or api_key.strip() == "":
        return None, "❌ Please enter your ElevenLabs API key."
    
    if saved_voice_path is None or not os.path.exists(saved_voice_path):
        return None, "❌ No voice saved. Please record and save your voice first."
    
    try:
        # Initialize ElevenLabs client
        client = ElevenLabs(api_key=api_key.strip())
        
        # Step 1: Create a temporary voice clone from the recording
        # This requires the "Starter" plan or higher on ElevenLabs for API usage
        with open(saved_voice_path, 'rb') as f:
            voice = client.voices.add(
                name="TempClonedVoice",
                description="Temporary voice created from Gradio recording",
                files=[f]
            )
        
        voice_id = voice.voice_id
        
        # Step 2: Generate speech using the newly created voice
        audio_generator = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.75,
                style=0.0,
                use_speaker_boost=True
            )
        )
        
        # Save generated audio
        output_path = "generated_speech.mp3"
        with open(output_path, 'wb') as f:
            for chunk in audio_generator:
                if chunk:
                    f.write(chunk)
        
        # Step 3: Cleanup - delete the temporary voice to keep account clean
        try:
            client.voices.delete(voice_id)
        except Exception:
            pass
        
        return output_path, "✅ Speech generated using YOUR voice! Listen below."
    
    except Exception as e:
        error_msg = str(e)
        if "invalid_api_key" in error_msg.lower() or "unauthorized" in error_msg.lower() or "401" in error_msg:
            return None, "❌ Invalid API key. Please check your ElevenLabs API key."
        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
            return None, "❌ API quota exceeded. Please check your ElevenLabs account."
        elif "subscription" in error_msg.lower() or "plan" in error_msg.lower() or "403" in error_msg:
            return None, "❌ Instant Voice Cloning via API requires a 'Starter' plan or higher. Free users can only use character-based voices in the Dashboard."
        else:
            return None, f"❌ Error generating speech: {error_msg}"


def clone_with_voice_design(text, api_key):
    """
    Alternative method: Uses ElevenLabs Voice Design API for better cloning.
    This creates a custom voice from the sample.
    
    Args:
        text: The text to convert to speech
        api_key: ElevenLabs API key
    
    Returns:
        tuple: (audio_path, status_message)
    """
    global saved_voice_path
    
    # Validation
    if not text or text.strip() == "":
        return None, "❌ Please enter some text to generate speech."
    
    if not api_key or api_key.strip() == "":
        return None, "❌ Please enter your ElevenLabs API key."
    
    if saved_voice_path is None or not os.path.exists(saved_voice_path):
        return None, "❌ No voice saved. Please record and save your voice first."
    
    try:
        # Initialize ElevenLabs client
        client = ElevenLabs(api_key=api_key.strip())
        
        # Add voice from file (Professional Voice Cloning)
        # Note: This requires a paid plan on ElevenLabs
        voice = client.voices.add(
            name="MyClonedVoice",
            files=[saved_voice_path]
        )
        
        # Generate speech with the cloned voice
        audio_bytes = client.text_to_speech.convert(
            voice_id=voice.voice_id,
            text=text,
            model_id="eleven_multilingual_v2"
        )
        
        # Save generated audio
        output_path = "generated_speech.mp3"
        with open(output_path, 'wb') as f:
            for chunk in audio_bytes:
                if chunk:
                    f.write(chunk)
        
        # Clean up: delete the created voice
        try:
            client.voices.delete(voice.voice_id)
        except:
            pass  # Ignore cleanup errors
        
        return output_path, "✅ Speech generated with voice cloning! Listen below."
    
    except Exception as e:
        error_msg = str(e)
        if "invalid_api_key" in error_msg.lower() or "unauthorized" in error_msg.lower() or "401" in error_msg:
            return None, "❌ Invalid API key. Please check your ElevenLabs API key."
        elif "quota" in error_msg.lower() or "subscription" in error_msg.lower() or "plan" in error_msg.lower():
            return None, "❌ Voice cloning requires a paid ElevenLabs plan. Try the basic method instead."
        else:
            return None, f"❌ Error with voice cloning: {error_msg}"


# Create Gradio Interface
with gr.Blocks(title="Voice Cloning App", theme=gr.themes.Soft()) as app:
    gr.Markdown(
        """
        # 🎙️ Voice Cloning Application
        
        **Step 1:** Record your voice (speak for at least 10-15 seconds for best results)  
        **Step 2:** Save your voice recording  
        **Step 3:** Enter your ElevenLabs API key ([Get one here](https://elevenlabs.io/))  
        **Step 4:** Type what you want to say and generate!
        """
    )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📝 Step 1 & 2: Record and Save Voice")
            audio_input = gr.Audio(
                sources=["microphone"],
                type="numpy",
                label="Record Your Voice"
            )
            save_btn = gr.Button("💾 Save Voice", variant="primary")
            save_status = gr.Textbox(label="Status", interactive=False)
        
        with gr.Column():
            gr.Markdown("### 🔑 Step 3: API Configuration")
            api_key_input = gr.Textbox(
                label="ElevenLabs API Key",
                type="password",
                placeholder="Enter your API key here..."
            )
            gr.Markdown(
                """
                > **Note:** Get your free API key at [elevenlabs.io](https://elevenlabs.io/)  
                > Free tier includes 10,000 characters/month
                """
            )
    
    gr.Markdown("### 🎯 Step 4: Generate Speech")
    
    with gr.Row():
        text_input = gr.Textbox(
            label="Text to Speak",
            placeholder="Type what you want your cloned voice to say...",
            lines=3
        )
    
    with gr.Row():
        generate_btn = gr.Button("🎵 Generate Speech (Basic)", variant="primary", scale=2)
        generate_pro_btn = gr.Button("✨ Generate with Voice Clone (Pro)", variant="secondary", scale=2)
    
    with gr.Row():
        audio_output = gr.Audio(label="Generated Speech", type="filepath")
        generation_status = gr.Textbox(label="Generation Status", interactive=False)
    
    # Event handlers
    save_btn.click(
        fn=save_voice,
        inputs=[audio_input],
        outputs=[save_status]
    )
    
    generate_btn.click(
        fn=clone_and_speak,
        inputs=[text_input, api_key_input],
        outputs=[audio_output, generation_status]
    )
    
    generate_pro_btn.click(
        fn=clone_with_voice_design,
        inputs=[text_input, api_key_input],
        outputs=[audio_output, generation_status]
    )

if __name__ == "__main__":
    print("🚀 Starting Voice Cloning Application...")
    print("📂 Voice files will be saved to:", VOICES_DIR.absolute())
    app.launch(share=False, server_name="127.0.0.1", server_port=7860)
