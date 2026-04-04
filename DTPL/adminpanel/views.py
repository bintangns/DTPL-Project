from django.shortcuts import render, redirect


def admin_login(request):
    if request.session.get('is_admin_logged_in'):
        return redirect('dashboard:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # dummy login sementara
        if username == 'admin' and password == 'admin123':
            request.session['is_admin_logged_in'] = True
            return redirect('dashboard:home')

        return render(request, 'adminpanel/login.html', {
            'error': 'Username atau password salah.'
        })

    return render(request, 'adminpanel/login.html')


def admin_logout(request):
    request.session.flush()
    return redirect('adminpanel:login')