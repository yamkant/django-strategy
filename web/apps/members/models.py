from core.models import BaseModel
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

class MemberManager(BaseUserManager):
    def createMember(self, phone, password):
        member = self.model(phone=phone)
        member.set_password(password)
        member.save()
        return member

#TODO: AbstractUser 동작원리 찾아보기
class Member(BaseModel, AbstractUser):
    username = None
    phone = models.CharField(
        unique=True,
        max_length=11,
        validators=[
            RegexValidator(
                r"^01[016789][0-9]{7,8}$",
                message="This phone number format is invalid.",
            )
        ]
    )
    # add method on this Member model.
    objects = MemberManager()

    USERNAME_FIELD = "phone"

    class Meta:
        managed = True
        db_table = 'members'