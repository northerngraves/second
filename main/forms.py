from django import forms
import re

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Введите ваш номер'}))
    code = forms.CharField(required=False, max_length=6, widget=forms.TextInput(attrs={'placeholder': 'Введите код'}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # Удаляем все, кроме цифр
        phone_number = re.sub(r'\D', '', phone_number)

        # Проверяем, что осталось ровно 10 цифр
        if len(phone_number) != 10:
            raise forms.ValidationError("Please enter a valid phone number with exactly 10 digits.")
        
        return phone_number


class CheckoutForm(forms.Form):

    CHOICES_DELIVERY = [
        ('delivery', 'Доставка'),
        ('shop', 'Самовывоз'),
    ]

    CHOICES_PAYMENT = [
        ('delivery', 'Доставка'),
        ('shop', 'Самовывоз'),
    ]

    address = forms.CharField(
        label="Введите адрес",
        widget=forms.Textarea(attrs={
            'placeholder':'Адрес доставки', 
            'class':'w-full rounded-lg overflow-hidden px-4 py-2'
        })
    )
    orderType = forms.ChoiceField(
        choices=CHOICES_DELIVERY,
        label="Выберите способ получения заказа",
        widget=forms.RadioSelect(attrs={
            'name':'delivery',
            'class':'flex h-5 w-5'
        })
    )
    paymentType = forms.ChoiceField(
        choices=CHOICES_PAYMENT,
        label="Выберите способ оплаты",
        widget=forms.RadioSelect(attrs={
            'name':'delivery',
            'class':'flex h-5 w-5'
        })
    )