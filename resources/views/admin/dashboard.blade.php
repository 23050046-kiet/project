@extends('layouts.app')

@section('title','Admin')

@section('content')
<section class="card">
    <h2>Khu vực quản trị</h2>
    @if(session('success'))
        <div id="toast-success" style="position:fixed;top:16px;right:16px;z-index:1000;background:#064e3b;color:#d1fae5;border:1px solid #065f46;border-radius:10px;padding:12px 14px;box-shadow:0 10px 25px rgba(0,0,0,.35);transition:opacity .3s ease, transform .3s ease;opacity:1;">
            {{ session('success') }}
        </div>
        <script>
            (function(){
                var el = document.getElementById('toast-success');
                if(!el) return; setTimeout(function(){ el.style.opacity='0'; el.style.transform='translateY(-8px)'; }, 2500);
                setTimeout(function(){ if(el&&el.parentNode){ el.parentNode.removeChild(el);} }, 3000);
            })();
        </script>
    @endif
    @if(session('error'))
        <div id="toast-error" style="position:fixed;top:16px;right:16px;z-index:1000;background:#7f1d1d;color:#fecaca;border:1px solid #991b1b;border-radius:10px;padding:12px 14px;box-shadow:0 10px 25px rgba(0,0,0,.35);transition:opacity .3s ease, transform .3s ease;opacity:1;">
            {{ session('error') }}
        </div>
        <script>
            (function(){
                var el = document.getElementById('toast-error');
                if(!el) return; setTimeout(function(){ el.style.opacity='0'; el.style.transform='translateY(-8px)'; }, 2500);
                setTimeout(function(){ if(el&&el.parentNode){ el.parentNode.removeChild(el);} }, 3000);
            })();
        </script>
    @endif
    <p>Xin chào, <strong>{{ auth()->user()->name }}</strong> (Admin)</p>
    <div class="grid two">
        <div class="card">
            <h3>Hành động</h3>
            <a href="{{ route('admin.desks.create') }}" class="btn btn-primary">Tạo Card mới</a>
            <a href="{{ route('admin.desks.index') }}" class="btn btn-primary" style="margin-left:8px">Danh sách Cards</a>
        </div>
    </div>
    <div class="card" style="margin-top:16px;overflow-x:auto">
        <h3>Danh sách Users</h3>
        <table style="width:100%;border-collapse:collapse;margin-top:8px">
            <thead>
                <tr style="text-align:left">
                    <th style="padding:8px;border-bottom:1px solid var(--border)">ID</th>
                    <th style="padding:8px;border-bottom:1px solid var(--border)">Tên</th>
                    <th style="padding:8px;border-bottom:1px solid var(--border)">Email</th>
                    <th style="padding:8px;border-bottom:1px solid var(--border)">Vai trò</th>
                    <th style="padding:8px;border-bottom:1px solid var(--border)">Thao tác</th>
                </tr>
            </thead>
            <tbody>
                @forelse($users as $u)
                <tr>
                    <td style="padding:8px;border-bottom:1px solid var(--border)">{{ $u->id }}</td>
                    <td style="padding:8px;border-bottom:1px solid var(--border)">{{ $u->name }}</td>
                    <td style="padding:8px;border-bottom:1px solid var(--border)">{{ $u->email }}</td>
                    <td style="padding:8px;border-bottom:1px solid var(--border)">
                         @if($u->is_admin)
                            <strong style="color:var(--primary); font-weight:700;">Admin</strong>
                        @else
                            User
                        @endif
                    </td>
                    <td style="padding:8px;border-bottom:1px solid var(--border)">
                        <form method="POST" action="{{ route('admin.users.destroy', $u) }}" class="inline" onsubmit="return confirm('Xóa user này?');">
                            @csrf
                            @method('DELETE')
                            <button type="submit" class="btn btn-outline" {{ $u->id === auth()->id() ? 'disabled' : '' }}>Xóa</button>
                        </form>
                    </td>
                </tr>
                @empty
                <tr><td colspan="5" class="muted" style="padding:12px">Chưa có user nào.</td></tr>
                @endforelse
            </tbody>
        </table>
        <div style="margin-top:8px">{{ $users->links() }}</div>
    </div>
    <p class="muted">Quay lại <a href="{{ route('dashboard') }}">Dashboard người dùng</a>.</p>
</section>
@endsection
