from django.urls import reverse
from ninja import ModelSchema
from pydantic import field_validator

from website.users.models import User


class UpdateUserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["username", "name"]
        fields_optional = "__all__"

    # ModelSchema adds these fields after Pydantic creates the base schema.
    @field_validator("username", "name", check_fields=False)
    @classmethod
    def reject_null(cls, value: str | None) -> str:
        if value is None:
            msg = "This field cannot be null."
            raise ValueError(msg)
        return value


class UserSchema(ModelSchema):
    url: str

    class Meta:
        model = User
        fields = ["username", "email", "name"]

    @staticmethod
    def resolve_url(obj: User):
        return reverse("api:retrieve_user", kwargs={"username": obj.username})
