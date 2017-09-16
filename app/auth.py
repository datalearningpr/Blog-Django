from app.models import User  
   
class MyCustomBackend:  
  
    def authenticate(self, username=None, password=None):  
        try:  
            user = User.objects.get(username=username)  
        except User.DoesNotExist:  
            pass  
        else:  
            if user.password == password:  
                return user  
        return None  
   
    def get_user(self, username):  
        try:  
            return User.objects.get(pk=username)  
        except User.DoesNotExist:  
            return None  