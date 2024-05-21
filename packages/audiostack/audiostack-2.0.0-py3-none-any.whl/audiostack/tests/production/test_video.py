import os

import audiostack

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants = {}  # type: dict


def test_video() -> None:
    script = audiostack.Content.Script.create(scriptText="hello sam")

    speech = audiostack.Speech.TTS.create(scriptItem=script, voice="sara")

    mix = audiostack.Production.Mix.create(speechItem=speech)
    print(mix)

    video = audiostack.Delivery.Video.create(
        productionItem=mix,
        public=True,
    )
    print(video)
