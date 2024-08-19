from django import forms

class KanaKanjiForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 6,               
            }
        ),
        label="「仮名漢字」に変換できます。",
        max_length=280
    )

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        return text
