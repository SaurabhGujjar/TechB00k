from .models import Profile

def data(request):
    try:
        c = Profile.objects.get(user__username=request.user)
        p = c.pro_pic
        return { 'data' : p }
    except:
        print('No user logged in')
        e = ''
        return { 'data' : e }
