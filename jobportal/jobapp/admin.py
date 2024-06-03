from django.contrib import admin

# Register your models here.
from .models import SignUp,AboutCompany,PostJobs,ApplyJobs
# Register your models here.
admin.site.register(SignUp)
admin.site.register(AboutCompany)
admin.site.register(PostJobs)
admin.site.register(ApplyJobs)