from django import forms

class PortfolioForm(forms.Form):
    portfolio_file = forms.FileField(label='Upload your portfolio Excel file')
