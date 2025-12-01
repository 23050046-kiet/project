@extends('layouts.app')

@section('title','Đăng ký')

@section('content')
<section class="card narrow">
    <h2>✍️ Đăng ký tài khoản mới</h2>
    <p class="muted" style="margin-top:-10px; margin-bottom:16px;">Điền thông tin của bạn vào form bên dưới.</p>
    @if($errors->any())
        <div class="alert error">{{ $errors->first() }}</div>
    @endif
    <form method="POST" action="{{ route('register.post') }}" class="form-grid">
        @csrf
        <label>Họ tên
            <input type="text" name="name" value="{{ old('name') }}" required **autocomplete="name"**>
        </label>
        <label>Email
            <input type="email" name="email" value="{{ old('email') }}" required **autocomplete="email"**>
        </label>
        <label>Mật khẩu
            <input type="password" name="password" required **autocomplete="new-password"**>
        </label>
        <label>Nhập lại mật khẩu
            <input type="password" name="password_confirmation" required>
        </label>
        <button type="submit" class="btn btn-primary">Đăng ký</button>
    </form>
    <p class="muted">Đã có tài khoản? <a href="{{ route('login') }}">Đăng nhập</a></p>
</section>
@endsection
