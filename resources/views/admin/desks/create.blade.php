@extends('layouts.app')

@section('title','Tạo Desk')

@section('content')
<section class="card narrow">
    @if(session('success'))
        <div id="toast-success" style="position:fixed;top:16px;right:16px;z-index:1000;background:#064e3b;color:#d1fae5;border:1px solid #065f46;border-radius:10px;padding:12px 14px;box-shadow:0 10px 25px rgba(0,0,0,.35);transition:opacity .3s ease, transform .3s ease;opacity:1;">
            {{ session('success') }}
        </div>
        <script>
            (function(){
                var el = document.getElementById('toast-success');
                if(!el) return;
                setTimeout(function(){
                    el.style.opacity = '0';
                    el.style.transform = 'translateY(-8px)';
                }, 2500);
                setTimeout(function(){
                    if(el && el.parentNode){ el.parentNode.removeChild(el); }
                }, 3000);
            })();
        </script>
    @endif
    <h2>Tạo Card mới</h2>
    @if($errors->any())
        <div class="alert error">{{ $errors->first() }}</div>
    @endif
    <form method="POST" action="{{ route('admin.desks.store') }}" enctype="multipart/form-data" class="form-grid">
        @csrf
        <label>Tên (English)
            <input type="text" name="name_en" value="{{ old('name_en') }}" required>
        </label>
        <label>Hình ảnh
            <input type="file" name="image" accept="image/*" required>
        </label>
        <button type="submit" class="btn btn-primary">Lưu</button>
        <a href="{{ route('admin.dashboard') }}" class="btn btn-outline">Hủy</a>
    </form>
</section>
@endsection
