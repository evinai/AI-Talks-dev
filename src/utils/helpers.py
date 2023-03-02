from typing import Any, Dict, Optional
from gtts import gTTS, lang
from io import BytesIO

import streamlit as st
import openai

DEFAULT_SPEECH_LANG = "Russian"


def get_dict_key(dictionary: Dict, value: Any) -> Optional[Any]:
    for key, val in dictionary.items():
        if val == value:
            return key


def lang_selector() -> str:
    languages = lang.tts_langs()
    lang_options = list(lang.tts_langs().values())
    default_index = lang_options.index(DEFAULT_SPEECH_LANG)
    lang_name = st.selectbox(
        label="Select speech language",
        options=lang_options,
        index=default_index
    )
    return get_dict_key(languages, lang_name)


def speech_speed_radio() -> bool:
    speed_options = {
        "Normal": False,
        "Slow": True
    }
    speed_speech = st.radio(
        label="Select speech speed",
        options=speed_options.keys(),
    )
    return speed_options.get(speed_speech)


def show_player(ai_content: str, lang_code: str, is_speech_slow: bool) -> None:
    sound_file = BytesIO()
    tts = gTTS(text=ai_content, lang=lang_code, slow=is_speech_slow)
    tts.write_to_fp(sound_file)
    st.write("Push play to hear sound of AI:")
    st.audio(sound_file)


def send_ai_request(api_key: str, user_text: str, ) -> str:
    openai.api_key = api_key
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": user_text
            }
        ]
    )
    if st.checkbox(label="Show Full API Response", value=False):
        st.json(completion)

    return completion.get("choices")[0].get("message").get("content")


def api_key_checker(api_key: str) -> str:
    if api_key == "ZVER":
        return st.secrets.api_credentials.api_key
    return api_key