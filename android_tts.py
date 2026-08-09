# -*- coding: utf-8 -*-
"""
این ماژول از موتور تبدیل متن به گفتار (TTS) خودِ اندروید استفاده می‌کند.
نکته مهم: خواندن صحیح فارسی به این بستگی دارد که گوشی کاربر بسته زبان
فارسی برای TTS (مثلاً Google Text-to-Speech) را نصب داشته باشد.
اگر زبان فارسی روی گوشی موجود نباشد، اندروید معمولاً با نزدیک‌ترین صدا
(یا انگلیسی) متن را می‌خواند.
"""

from kivy.utils import platform

_tts_engine = None


def _get_engine():
    global _tts_engine
    if _tts_engine is not None:
        return _tts_engine

    from jnius import autoclass, PythonJavaClass, java_method

    TextToSpeech = autoclass("android.speech.tts.TextToSpeech")
    Locale = autoclass("java.util.Locale")
    PythonActivity = autoclass("org.kivy.android.PythonActivity")

    class OnInitListener(PythonJavaClass):
        __javainterfaces__ = ["android/speech/tts/TextToSpeech$OnInitListener"]
        __javacontext__ = "app"

        def __init__(self, callback):
            super().__init__()
            self.callback = callback

        @java_method("(I)V")
        def onInit(self, status):
            self.callback(status)

    result = {"engine": None}

    def on_init(status):
        engine = result["engine"]
        if engine is not None:
            try:
                fa_locale = Locale("fa", "IR")
                engine.setLanguage(fa_locale)
            except Exception:
                pass

    listener = OnInitListener(on_init)
    engine = TextToSpeech(PythonActivity.mActivity, listener)
    result["engine"] = engine
    _tts_engine = engine
    return _tts_engine


def speak_persian(text: str):
    """متن فارسی داده‌شده را با بلندگوی گوشی می‌خواند."""
    if platform != "android":
        # روی کامپیوتر (برای تست) فقط در کنسول چاپ می‌شود
        print(f"[TTS TEST MODE] متن خوانده می‌شود: {text}")
        return

    from jnius import autoclass

    TextToSpeech = autoclass("android.speech.tts.TextToSpeech")
    engine = _get_engine()
    engine.speak(text, TextToSpeech.QUEUE_FLUSH, None, "utt1")
