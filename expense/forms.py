from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['tittle', 'amount', 'category', 'date']
        widgets = {
            'tittle': forms.TextInput(attrs={'placeholder': 'Expense Title'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Amount'}),
            'date': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
        }

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select Category"
