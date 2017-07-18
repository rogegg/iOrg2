from django import forms
from datareader.models import Question

class AnswerForm(forms.Form):
    choices = (('V', 'Verdadero',), ('F', 'Falso',))

    options = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'iorg-input'}),
                                choices=choices, initial='V', label='')


    def create_form(q):
        option_list = q.get_option_list()
        new_list = []
        i = 0
        for option in option_list:
            new_list.append((i,option))
            i=i+1
        print(new_list)
        choices = tuple(new_list)
        options = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'iorg-input'}),
                                    choices=choices, initial='0', label='')

