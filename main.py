# -*- coding: utf-8 -*-
"""
اپلیکیشن ساده: نمایش دوربین + خواندن متن فارسی با صدای بلند (TTS)
ساخته‌شده با Kivy برای اندروید
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp

# رنگ پس‌زمینه ساده و روشن
Window.clearcolor = (0.96, 0.97, 0.99, 1)


class RoundedButton(Button):
    """دکمه با گوشه‌های گرد و استایل ساده"""
    def __init__(self, bg_color=(0.25, 0.5, 0.95, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.font_size = dp(18)
        self.bold = True
        self._bg_color = bg_color
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(16), spacing=dp(14), **kwargs)

        self.camera_widget = None
        self.camera_active = False

        # عنوان
        title = Label(
            text="[b]دوربین و خواندن متن[/b]",
            markup=True,
            font_size=dp(22),
            color=(0.15, 0.15, 0.2, 1),
            size_hint_y=None,
            height=dp(50),
        )
        self.add_widget(title)

        # جای نمایش دوربین
        self.camera_box = BoxLayout(size_hint_y=0.5)
        self.add_widget(self.camera_box)

        # دکمه روشن/خاموش کردن دوربین
        self.camera_btn = RoundedButton(
            text="نمایش دوربین",
            size_hint_y=None,
            height=dp(50),
            bg_color=(0.25, 0.5, 0.95, 1),
        )
        self.camera_btn.bind(on_release=self.toggle_camera)
        self.add_widget(self.camera_btn)

        # باکس متن فارسی
        self.text_input = TextInput(
            hint_text="یک کلمه یا جمله فارسی بنویسید...",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(60),
            multiline=False,
            padding=[dp(12), dp(15)],
            base_direction="rtl",
        )
        self.add_widget(self.text_input)

        # دکمه خواندن متن
        self.speak_btn = RoundedButton(
            text="خواندن با صدای بلند",
            size_hint_y=None,
            height=dp(50),
            bg_color=(0.2, 0.75, 0.45, 1),
        )
        self.speak_btn.bind(on_release=self.speak_text)
        self.add_widget(self.speak_btn)

        # پیام وضعیت
        self.status_label = Label(
            text="",
            font_size=dp(14),
            color=(0.4, 0.4, 0.4, 1),
            size_hint_y=None,
            height=dp(30),
        )
        self.add_widget(self.status_label)

    # ---------- دوربین ----------
    def toggle_camera(self, instance):
        if not self.camera_active:
            try:
                self.camera_widget = Camera(play=True, resolution=(640, 480))
                self.camera_box.clear_widgets()
                self.camera_box.add_widget(self.camera_widget)
                self.camera_active = True
                self.camera_btn.text = "بستن دوربین"
                self.status_label.text = ""
            except Exception as e:
                self.status_label.text = f"خطا در باز کردن دوربین: {e}"
        else:
            self.camera_box.clear_widgets()
            self.camera_widget = None
            self.camera_active = False
            self.camera_btn.text = "نمایش دوربین"

    # ---------- خواندن متن (TTS) ----------
    def speak_text(self, instance):
        text = self.text_input.text.strip()
        if not text:
            self.status_label.text = "لطفاً ابتدا متنی وارد کنید."
            return

        try:
            from android_tts import speak_persian  # ماژول کمکی پایین همین پوشه
            speak_persian(text)
            self.status_label.text = "در حال خواندن..."
        except Exception as e:
            self.status_label.text = f"قابلیت صدا در دسترس نیست: {e}"


class PersianTTSApp(App):
    def build(self):
        self.title = "دوربین و خواندن متن فارسی"
        return MainLayout()


if __name__ == "__main__":
    PersianTTSApp().run()
