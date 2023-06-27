from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):

    @staticmethod
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('user most have email')
        if not username:
            raise ValueError('user must have unique username')

        user = self.model(email=self.normalize_email(email),
                          username=username)
        user.Password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, password, username)
        user.is_admin = True
        user.save(using=self._db)
        return user
