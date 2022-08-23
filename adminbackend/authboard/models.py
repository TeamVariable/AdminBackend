from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from typing import List, Any

# Create your models here.
class UserManage(BaseUserManager):
    def create_user(self, email: str, name: str, password: str = None) -> None:
        if not email:
            raise ValueError("User must have an email address")
        
        user = self.model(
            email = self.normalize_email(email),
            name = name
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email: str, name: str, password: str = None) -> None:
        user = self.create_user(
            email=email,
            name=name,
            password=password
        )
        user.is_admin = True
        user.is_suepruser = True
        user.save(using=self._db)
        
        return user


class TimeStepField(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    
    class Meta:
        abstract = True 


class User(AbstractBaseUser, PermissionsMixin, TimeStepField):
    email = models.EmailField(
        verbose_name='이메일', max_length=50, unique=True,
        blank=False, null=False,
    )
    name = models.CharField(
        max_length=5, verbose_name='이름' 
        ,blank=False, null=False,
    )
    password = models.CharField(max_length=30, verbose_name='비밀번호', blank=True, null=False)
    birth_day = models.DateTimeField(null=False, blank=True)
    
    # 어드민 필드 설정
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    # 필드 변경 및 적용 
    objects: UserManage[Any] = UserManage()
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: List[str] = ["password"]
    
    def __str__(self) -> str:
        return f"{self.email}"
    
    def has_perm(self, perm, obj=None) -> bool:
        return True
    
    def has_module_perm(self, app_label) -> bool:
        return True
    
    @property
    def is_staff(self):
        return self.is_admin