from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

Window.clearcolor = (0.1, 0.15, 0.2, 1)


class LoanCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        title = Label(
            text='[b]محاسبه‌گر وام[/b]',
            markup=True,
            font_size='24sp',
            size_hint_y=None,
            height=60,
            color=(1, 1, 1, 1)
        )
        self.add_widget(title)

        self.add_widget(Label(text='مبلغ وام (تومان):', size_hint_y=None, height=35, color=(1, 1, 1, 1)))
        self.amount = TextInput(multiline=False, input_filter='float', size_hint_y=None, height=45, hint_text='مثال: 100000000')
        self.add_widget(self.amount)

        self.add_widget(Label(text='نرخ سود سالانه (%):', size_hint_y=None, height=35, color=(1, 1, 1, 1)))
        self.rate = TextInput(multiline=False, input_filter='float', size_hint_y=None, height=45, hint_text='مثال: 18')
        self.add_widget(self.rate)

        self.add_widget(Label(text='تعداد اقساط (ماه):', size_hint_y=None, height=35, color=(1, 1, 1, 1)))
        self.months = TextInput(multiline=False, input_filter='int', size_hint_y=None, height=45, hint_text='مثال: 60')
        self.add_widget(self.months)

        btn = Button(text='محاسبه', size_hint_y=None, height=55, background_color=(0.2, 0.6, 0.9, 1), font_size='18sp')
        btn.bind(on_press=self.calculate)
        self.add_widget(btn)

        self.result = Label(text='', markup=True, size_hint_y=None, height=220, color=(1, 1, 0.6, 1), font_size='16sp')
        self.add_widget(self.result)

    def calculate(self, instance):
        try:
            amount = float(self.amount.text or 0)
            rate = float(self.rate.text or 0)
            months = int(self.months.text or 1)

            if amount <= 0 or rate < 0 or months <= 0:
                self.result.text = '[color=ff6666]لطفاً مقادیر درست وارد کنید[/color]'
                return

            monthly_rate = rate / 100 / 12

            if monthly_rate == 0:
                installment = amount / months
            else:
                installment = amount * monthly_rate * (1 + monthly_rate) ** months / \
                              ((1 + monthly_rate) ** months - 1)

            total = installment * months
            interest = total - amount

            self.result.text = (
                f'[b]قسط ماهانه:[/b]\n'
                f'[color=66ff99]{installment:,.0f} تومان[/color]\n\n'
                f'[b]مبلغ کل بازپرداخت:[/b]\n'
                f'[color=66ff99]{total:,.0f} تومان[/color]\n\n'
                f'[b]سود کل:[/b]\n'
                f'[color=ff9999]{interest:,.0f} تومان[/color]'
            )
        except Exception as e:
            self.result.text = f'[color=ff6666]خطا: {e}[/color]'


class LoanApp(App):
    def build(self):
        self.title = 'محاسبه‌گر وام'
        return LoanCalculator()


if __name__ == '__main__':
    LoanApp().run()
