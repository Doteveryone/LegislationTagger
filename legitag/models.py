from datetime import datetime
from legitag import db
from flask.ext.security import UserMixin, RoleMixin, login_required


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    name = db.StringField(max_length=255)
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])


class Edit(db.EmbeddedDocument):
    user = db.ReferenceField(User, required=True)
    description = db.StringField(max_length=255)
    occured_at = db.DateTimeField(default=datetime.now, required=True)

class Tag(db.EmbeddedDocument):
    key = db.StringField(max_length=100, required=True)
    value = db.StringField(max_length=255, required=True)

class Legislation(db.Document):
    title = db.StringField(max_length=255, required=True)
    original_url = db.URLField(required=False, unique=True)
    html_url = db.URLField(required=False)
    pdf_url = db.URLField(required=False)
    created_at = db.DateTimeField(default=datetime.now, required=True)
    updated_at = db.DateTimeField(default=datetime.now, required=True)
    _tags = db.EmbeddedDocumentListField(Tag)
    _edits = db.EmbeddedDocumentListField(Edit)

    @property
    def tags(self):
        return self._tags

    @property
    def edits(self):
        return self._edits

    def save(self, user=None, description=None, *args, **kwargs):

        # todo:check if anything has changed?

        # add to history
        if user:
            user_db = User.objects.get(id=user.get_id())
            edit = Edit(user=user_db, description=description)
            self._edits.append(edit)

        # todo: save state against history

        self.updated_at = datetime.now

        super(Legislation, self).save(*args, **kwargs)

    def append_tag(self, new_tag):
        found = False
        for tag in self.tags:
            if tag.key == new_tag.key and tag.value == new_tag.value:
                found = True
        if not found:
            self._tags.append(new_tag)
