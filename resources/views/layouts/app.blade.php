<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>@yield('title', 'VibeCode')</title>
    @php($ver = file_exists(public_path('css/app.css')) ? filemtime(public_path('css/app.css')) : time())
    <link rel="stylesheet" href="{{ asset('css/app.css') }}?v={{ $ver }}">
</head>
<body>
    <header class="site-header">
        <div class="container flex between center">
            <a class="brand" href="{{ url('/') }}">VibeCode</a>
            <nav class="nav">
                @auth
                    <a href="{{ route('dashboard') }}">Dashboard</a>
                    @if(auth()->user()->is_admin)
                        <a href="{{ route('admin.dashboard') }}">Admin</a>
                    @endif
                    <form method="POST" action="{{ route('logout') }}" class="inline">
                        @csrf
                        <button type="submit" class="btn btn-outline">Đăng xuất</button>
                    </form>
                @else
                    <a href="{{ route('login') }}">Đăng nhập</a>
                    <a href="{{ route('register') }}" class="btn btn-primary">Đăng ký</a>
                @endauth
            </nav>
        </div>
    </header>
    <main class="container">
        @yield('content')
    </main>
    
</body>
</html>
