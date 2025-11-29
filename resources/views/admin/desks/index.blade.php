@extends('layouts.app')

@section('title','Danh sách Cards')

@section('content')
<section class="card">
    <h2>Danh sách Card</h2>
    @if(session('success'))
        <div id="toast-success" style="position:fixed;top:16px;right:16px;z-index:1000;background:#064e3b;color:#d1fae5;border:1px solid #065f46;border-radius:10px;padding:12px 14px;box-shadow:0 10px 25px rgba(0,0,0,.35);transition:opacity .3s ease, transform .3s ease;opacity:1;">
            {{ session('success') }}
        </div>
        <script>
            (function(){
                var el = document.getElementById('toast-success');
                if(!el) return;
                setTimeout(function(){ el.style.opacity = '0'; el.style.transform = 'translateY(-8px)'; }, 2500);
                setTimeout(function(){ if(el && el.parentNode){ el.parentNode.removeChild(el); } }, 3000);
            })();
        </script>
    @endif

    <div class="card" style="overflow-x:auto">
        <table style="width:100%;border-collapse:collapse">
            <thead>
                <tr style="text-align:left">
                    <th style="padding:8px;border-bottom:1px solid var(--border)">Tên (EN)</th>
                    <th style="padding:8px;border-bottom:1px solid var(--border)">Hình</th>
                    <th style="padding:8px;border-bottom:1px solid var(--border)">Tạo lúc</th>
                    <th style="padding:8px;border-bottom:1px solid var(--border)">Thao tác</th>
                </tr>
            </thead>
            <tbody>
            @forelse($desks as $desk)
                <tr>
                    <td style="padding:8px;border-bottom:1px solid var(--border)">{{ $desk->name_en }}</td>
                    <td style="padding:8px;border-bottom:1px solid var(--border)">
                        @if($desk->image_path)
                            <img src="{{ asset('storage/'.$desk->image_path) }}" alt="{{ $desk->name_en }}" style="width:80px;height:60px;object-fit:cover;border-radius:6px;border:1px solid var(--border)">
                        @else
                            <span class="muted">(Không có hình)</span>
                        @endif
                    </td>
                    <td style="padding:8px;border-bottom:1px solid var(--border)">{{ $desk->created_at->format('d/m/Y H:i') }}</td>
                    <td style="padding:8px;border-bottom:1px solid var(--border)">
                        <form method="POST" action="{{ route('admin.desks.destroy', $desk) }}" onsubmit="return confirm('Xóa card này?');" class="inline">
                            @csrf
                            @method('DELETE')
                            <button type="submit" class="btn btn-outline">Xóa</button>
                        </form>
                    </td>
                </tr>
            @empty
                <tr><td colspan="4" class="muted" style="padding:12px">Chưa có card nào.</td></tr>
            @endforelse
            </tbody>
        </table>
    </div>

    <div style="margin-top:12px">
        {{ $desks->links() }}
    </div>

    <div style="margin-top:16px">
        <a href="{{ route('admin.desks.create') }}" class="btn btn-primary">Tạo Card mới</a>
        <a href="{{ route('admin.dashboard') }}" class="btn btn-outline">Quay lại Admin</a>
    </div>
</section>
@endsection
