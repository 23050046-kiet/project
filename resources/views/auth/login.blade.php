@extends('layouts.app')

@section('title','Đăng nhập')

@section('content')
<section class="card narrow">
    <h2>Đăng nhập</h2>
    @if($errors->any())
        <div class="alert error">{{ $errors->first() }}</div>
    @endif
    <form method="POST" action="{{ route('login.post') }}" class="form-grid">
        @csrf
        <label>Email
            <input type="email" name="email" value="{{ old('email') }}" required>
        </label>
        <label>Mật khẩu
            <input type="password" name="password" required>
        </label>
        <label class="checkbox">
            <input type="checkbox" name="remember"> Ghi nhớ
        </label>
        <button type="submit" class="btn btn-primary">Đăng nhập</button>
    </form>
    <p class="muted">Chưa có tài khoản? <a href="{{ route('register') }}">Đăng ký</a></p>
</section>
@endsection
