
from elevenlabs.client import ElevenLabs
from elevenlabs import stream, Voice, VoiceSettings
from load_dotenv import load_dotenv
import os
import time

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVEN_API_KEY")
)


voice = Voice(voice_id=os.getenv("ELEVEN_LABS_VOICE_ID"),    settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True))




from ChainManager import ChainManager




def start():
    load_dotenv()
    chain_manager = ChainManager()
    previous_3 = []
    while True:
        plan = chain_manager.generate_execution_plan(previous_3)
        print(plan)
        expected_keys = ['m1', 'm2', 'm3']
        expected_nested_keys = ['plan', 'questions']
        if list(plan.keys()) != expected_keys:
            break
        for key in expected_keys:
            minute = plan[key]
            if list(minute.keys()) != expected_nested_keys:
                break
            plan_for_minute = minute["plan"]
            if plan_for_minute == "silence":
                time.sleep(60)
                continue
            questions_for_minute = minute["questions"][:1]
            execution = chain_manager.execute_plan(plan_for_minute, questions_for_minute)
            print(f"\n\n\{execution}\n\n")
            audio_stream = client.generate(
                text=execution,
                stream=True,
                voice=voice
                )
            stream(audio_stream)
            previous_3.append(plan_for_minute)

if __name__ == "__main__":
    start()
