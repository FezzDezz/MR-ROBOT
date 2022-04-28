# -*- coding: utf-8 -*-
from dataclasses import dataclass
from keyboa import Keyboa, Button


@dataclass
class InlineMarkupClass:
    EMTPY_FIELD = '1'
    btn_return = Button(button_data={'« Назад': '/start'}).button

    @staticmethod
    def MainMenu():
        # Buttons
        btn_edit_template = Button(button_data={'Шаблон': 'template'}, front_marker='/').button
        btn_add_treasure = Button(button_data={'Добавити скарб': 'treasure'}, front_marker='/new_').button
        # Markup
        menu = [
            btn_edit_template,
            btn_add_treasure
        ]
        # Keyboard
        keyboard = Keyboa(items=menu, items_in_row=1, copy_text_to_callback=False).keyboard
        return keyboard

    @staticmethod
    def NewTreasureMenu():
        # Buttons
        btn_return = Button(button_data={'« Назад': '/start'}).button
        btn_save_treasure = Button(button_data={'Зберегти скарб': 'treasure'}, front_marker='new_', back_marker='_save').button
        btn_delete_treasure = Button(button_data={'Видалити скарб': 'treasure'}, front_marker='new_', back_marker='_delete').button
        # Markup
        menu = [
            btn_save_treasure,
            btn_delete_treasure,
            btn_return
        ]
        # Keyboard
        keyboard = Keyboa(items=menu, items_in_row=1, copy_text_to_callback=False).keyboard
        return keyboard

    @staticmethod
    def TemplateMenu():
        # Buttons
        btn_return = Button(button_data={'В« РќР°Р·Р°Рґ': '/start'}).button
        # btn_return = Button(button_data={'В« РќР°Р·Р°Рґ': 'return to'}, back_marker=' main menu').button
        btn_save_template = Button(button_data={'Р—Р±РµСЂРµРіС‚Рё': 'template'}, front_marker='/save_').button
        btn_clear_template = Button(button_data={'Р’РёРґР°Р»РёС‚Рё': 'template'}, front_marker='/clear_').button
        # Markup
        menu = [
            btn_save_template,
            btn_clear_template,
            btn_return
        ]
        # Keyboard
        keyboard = Keyboa(items=menu, items_in_row=2, copy_text_to_callback=False).keyboard
        return keyboard

    @property
    def TestMenu(self):
        # Buttons
        btn_empty_field = Button(button_data={'РџСѓСЃС‚РёР№ callback': self.EMTPY_FIELD}).button
        # Markup
        menu = [
            btn_empty_field
        ]
        # Keyboard
        keyboard = Keyboa(items=menu, items_in_row=1, copy_text_to_callback=False).keyboard
        return keyboard
    pass
