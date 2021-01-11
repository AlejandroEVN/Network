from django import forms

# Form for new post
class PostForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control mb-4"

    content = forms.CharField (
        required=True,
        max_length=240,
        label="Content",
        widget=forms.Textarea (
            attrs= {
                "rows": 5,
                "placeholder": "Max 240 characters"
            })
    )
    