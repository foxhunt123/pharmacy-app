from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.pickers import MDDatePicker

import json
import os
from datetime import datetime

# 🔥 СКЕНЕР
from scanner import scan_barcode

# 🔥 БАЗА (можеш да я разширяваш)
MED_DB = {
    "3800123456789": {"name": "Парацетамол", "qty": "1 кутия"},
    "3800999999999": {"name": "Спазмалгон", "qty": "20 таблетки"}
}


class MainUI(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.data_file = "data.json"
        self.data = []
        self.selected_date = ""

        root = MDBoxLayout(orientation="vertical")

        root.add_widget(MDTopAppBar(title="Моята аптечка"))

        # TABS
        tabs = MDBoxLayout(size_hint_y=None, height=60, padding=10, spacing=10)

        self.btn_home = MDRaisedButton(text="Моята аптечка")
        self.btn_exp = MDRaisedButton(text="Изтичащи")

        self.btn_home.bind(on_release=self.show_home)
        self.btn_exp.bind(on_release=self.show_expiring)

        tabs.add_widget(self.btn_home)
        tabs.add_widget(self.btn_exp)

        root.add_widget(tabs)

        # INPUT
        left = MDBoxLayout(orientation="vertical", size_hint_x=0.4, padding=15, spacing=10)

        self.name_field = MDTextField(hint_text="Име на лекарство")
        self.qty_field = MDTextField(hint_text="Количество")

        self.date_btn = MDRaisedButton(text="📅 Избери дата")
        self.date_btn.bind(on_release=self.open_calendar)

        self.date_label = MDLabel(text="Няма дата", halign="center")

        self.add_btn = MDRaisedButton(text="Добави")
        self.add_btn.bind(on_release=self.add_item)

        # 🔥 СКЕНЕР БУТОН
        self.scan_btn = MDRaisedButton(text="📷 Сканирай")
        self.scan_btn.bind(on_release=self.scan_item)

        left.add_widget(self.name_field)
        left.add_widget(self.qty_field)
        left.add_widget(self.scan_btn)
        left.add_widget(self.date_btn)
        left.add_widget(self.date_label)
        left.add_widget(self.add_btn)

        # LIST
        scroll = MDScrollView()

        self.list_layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=14,
            padding=12
        )
        self.list_layout.bind(minimum_height=self.list_layout.setter("height"))

        scroll.add_widget(self.list_layout)

        main = MDBoxLayout()
        main.add_widget(left)
        main.add_widget(scroll)

        root.add_widget(main)
        self.add_widget(root)

        self.load_data()

    # 🔥 СКАНИРАНЕ
    def scan_item(self, obj):
        code = scan_barcode()

        if not code:
            return

        if code in MED_DB:
            self.name_field.text = MED_DB[code]["name"]
            self.qty_field.text = MED_DB[code]["qty"]
        else:
            self.name_field.text = f"Непознат продукт ({code})"

    # DATE
    def open_calendar(self, obj):
        picker = MDDatePicker()
        picker.bind(on_save=self.set_date)
        picker.open()

    def set_date(self, instance, date, date_range):
        self.selected_date = str(date)
        self.date_label.text = self.selected_date

    # DAYS LEFT
    def get_days_left(self, date_str):
        try:
            exp = datetime.strptime(date_str, "%Y-%m-%d").date()
            today = datetime.today().date()
            return (exp - today).days
        except:
            return 0

    # ADD
    def add_item(self, obj):
        if not self.name_field.text or not self.selected_date:
            return

        self.data.append({
            "name": self.name_field.text,
            "qty": self.qty_field.text,
            "date": self.selected_date
        })

        self.save_data()
        self.refresh()

        self.name_field.text = ""
        self.qty_field.text = ""
        self.selected_date = ""
        self.date_label.text = "Няма дата"

    def create_card(self, item):
        days = self.get_days_left(item.get("date", ""))

        if days <= 0:
            accent = (1, 0.3, 0.3, 1)
            status = "Изтекло"
            subtitle = "Трябва да се изхвърли"
        elif days <= 7:
            accent = (1, 0.75, 0.2, 1)
            status = f"Изтича след {days} дни"
            subtitle = "Внимание"
        else:
            accent = (0.2, 0.8, 0.4, 1)
            status = "В срок"
            subtitle = "ОК"

        card = MDCard(
            size_hint_y=None,
            height=120,
            radius=[18],
            elevation=6,
            md_bg_color=(1, 1, 1, 1),
            padding=0
        )

        row = MDBoxLayout()

        left_bar = MDBoxLayout(size_hint_x=None, width=6, md_bg_color=accent)

        content = MDBoxLayout(orientation="vertical", padding=12, spacing=2)

        title = MDLabel(
            text=item.get("name"),
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=28
        )

        qty = MDLabel(text=f"Наличност: {item.get('qty')}", theme_text_color="Secondary")
        date = MDLabel(text=f"Срок: {item.get('date')}", theme_text_color="Secondary")

        status_label = MDLabel(
            text=status,
            theme_text_color="Custom",
            text_color=accent
        )

        subtitle_label = MDLabel(
            text=subtitle,
            theme_text_color="Hint"
        )

        delete_btn = MDIconButton(icon="delete")
        delete_btn.bind(on_release=lambda x: self.delete_item(item))

        content.add_widget(title)
        content.add_widget(qty)
        content.add_widget(date)
        content.add_widget(status_label)
        content.add_widget(subtitle_label)

        row.add_widget(left_bar)
        row.add_widget(content)
        row.add_widget(delete_btn)

        card.add_widget(row)

        return card

    def refresh(self, mode=None):
        self.list_layout.clear_widgets()

        for item in self.data:
            days = self.get_days_left(item.get("date", ""))

            if mode == "expired":
                if days <= 7:
                    self.list_layout.add_widget(self.create_card(item))
            else:
                self.list_layout.add_widget(self.create_card(item))

    def show_home(self, obj):
        self.refresh()

    def show_expiring(self, obj):
        self.refresh("expired")

    def delete_item(self, item):
        if item in self.data:
            self.data.remove(item)
        self.save_data()
        self.refresh()

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except:
                self.data = []
        else:
            self.data = []

        self.refresh()


class MyApp(MDApp):
    def build(self):
        return MainUI()


MyApp().run()