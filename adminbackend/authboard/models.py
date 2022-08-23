from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from argon2 import PasswordHasher
from typing import List, Union

# Create your models here.
class UserManage(BaseUserManager):
    use_in_migrations: bool = True
    
    def _create_user(self, email: str, name: str, birth_day: str, password: Union[str, bytes], **extra_fields) -> None:
        if not email:
            raise ValueError("User must have an email address")
        
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            password = PasswordHasher().hash(password),
            birth_day = birth_day,  
            **extra_fields      
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_user(self, email: str, name: str, birth_day: str, password: Union[str, bytes], **extra_fields) -> None:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_supuseruser", False)
        
        return self._create_user(email, name, birth_day, password, **extra_fields)    
    
    def create_superuser(self, email: str, name: str, birth_day: str, password: Union[str, bytes], **extra_fields) -> None:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("관리자 권한이 필요합니다")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("슈퍼유저 권한이 필요합니다")
        
        return self._create_user(email, name, birth_day, password, **extra_fields)
        

class TimeStepField(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="가입날짜")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정날짜")   
    
    class Meta:
        abstract: bool = True 


class User(AbstractBaseUser, PermissionsMixin, TimeStepField):
    email = models.EmailField(
        verbose_name='이메일', max_length=50, 
        unique=True, blank=False, null=False,
    )
    name = models.CharField(
        max_length=5, verbose_name='이름',
        blank=False, null=False
    )
    password = models.CharField(
        max_length=100, verbose_name='패스워드',
        blank=False, null=False
    )
    birth_day = models.DateField(null=False, blank=False, help_text="ex)1995-08-01", verbose_name="생년월일")
    
    # 어드민 필드 설정
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    # 필드 변경 및 적용 
    objects = UserManage()
    USERNAME_FIELD: str = "email"
    EMAIL_FIELD: str = "email"
    REQUIRED_FIELDS: List[str] = ["name", "password", "birth_day"]
    
    def __str__(self) -> str:
        return f"{self.email}"
    
    def has_perm(self, perm, obj=None) -> bool:
        return True
    
    def has_module_perm(self, app_label) -> bool:
        return True
    
    class Meta:
        db_table: str = "admin_auth"