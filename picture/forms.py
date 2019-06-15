from django.forms import ModelForm

from .models import Reply
from SharePic.middleware import get_request_user_id


class AddReplyInfoFrom(ModelForm):
    
    def save(self, commit=True):
        user_id = get_request_user_id()
        self.instance.creater_id = user_id
        return super(AddReplyInfoFrom, self).save()
    
    class Meta:
        model = Reply
        fields = ["parent_reply", "album_id", "content"]
