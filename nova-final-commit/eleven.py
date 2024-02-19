import elevenlabs
import env
elevenlabs.set_api_key (env.Elevenlabs_api_key)
class nova:
    def __init__(self):
        self.voice = elevenlabs.Voice(
        voice_id = "ZQe5CZNOzWyzPSCn5a3c",
        settings = elevenlabs.VoiceSettings(
            stability = 0,
            similarity_boost = 0.75
            )
        )
        self.text = "Hi, I'm from the future!"

    def play(self):
            audio = elevenlabs.generate(
            text = self.text,
            voice = self.voice)
            print(self.text)
            elevenlabs.play(audio)

def nova_voice(TEXT):
    v1 = nova()
    v1.text = TEXT
    v1.play()
