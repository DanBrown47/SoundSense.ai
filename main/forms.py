from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
    
    def clean_file_field(self):
        print("Passed form")
        uploaded_file = self.cleaned_data['file']
        filename = uploaded_file.name
        print("HEHE", filename)
        self.cleaned_data['original_filename'] = str(filename)  # Save filename into another field
        return uploaded_file


class SongForm(forms.Form):
    file = MultipleFileField()

    