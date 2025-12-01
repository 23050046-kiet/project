@extends('layouts.app')

@section('title','Dashboard')

@section('content')
<section class="card">
    <h2>🏠 Dashboard người dùng</h2>
    <p>Xin chào, <strong>{{ auth()->user()->name }}</strong></p>
    <p>
        <a href="{{ route('cards.play') }}" class="btn btn-primary">ẤN VÀ BẮT ĐẦU HỌC NÀO</a>
        
    </p>
    <hr style="border-color:var(--border);margin:16px 0">
    <h3>Tiến độ học</h3>
    @php($t = isset($total) ? (int)$total : 0)
    @php($c = isset($completed) ? (int)$completed : 0)
    @if($t === 0)
        <p class="muted">Chưa có card nào để thống kê.</p>
    @else
    <div id="progress" data-total="{{ $t }}" data-completed="{{ $c }}" style="display:flex;gap:16px;align-items:center;">
        <svg width="140" height="140" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="54" stroke="var(--border)" stroke-width="12" fill="none"></circle>
            <circle id="progress-ring" cx="60" cy="60" r="54" stroke="var(--primary)" stroke-width="12" fill="none" stroke-linecap="round" transform="rotate(-90 60 60)" style="stroke-dasharray:0 0;stroke-dashoffset:0"></circle>
            <text id="progress-text" x="60" y="64" text-anchor="middle" fill="var(--text)" font-size="18" font-weight="600">0%</text>
        </svg>
        <div>
            <div><strong>{{ $c }}</strong> / {{ $t }} cards đã hoàn thành</div>
            <div class="muted">Lật thẻ để đánh dấu hoàn thành</div>
        </div>
    </div>
    <script>
    (function(){
        var el = document.getElementById('progress');
        if(!el) return;
        var total = parseInt(el.getAttribute('data-total')||'0',10);
        var completed = parseInt(el.getAttribute('data-completed')||'0',10);
        var pct = total>0 ? Math.round((completed/total)*100) : 0;
        var ring = document.getElementById('progress-ring');
        var txt = document.getElementById('progress-text');
        var r = 54; var C = 2*Math.PI*r;
        ring.style.strokeDasharray = C + ' ' + C;
        ring.style.strokeDashoffset = C * (1 - pct/100);
        txt.textContent = pct + '%';
    })();
    </script>
    @endif
</section>
<section class="card" style="margin-top:16px">
    <h3>Bảng xếp hạng</h3>
    @php($leaders = isset($leaderboard) ? $leaderboard : collect())
    @if($leaders->isEmpty())
        <p class="muted">Chưa có dữ liệu xếp hạng.</p>
    @else
    <div style="overflow-x:auto;margin-top:8px">
        <table style="width:100%;border-collapse:collapse">
            <thead>
                <tr style="text-align:left">
                    <th style="padding:8px;border-bottom:1px solid var(--border)">#TOP</th>
                    <th style="padding:8px;border-bottom:1px solid var(--border)">Tên</th>
                    <th style="padding:8px;border-bottom:1px solid var(--border)">Email</th>
                    <th style="padding:8px;border-bottom:1px solid var(--border)">Số Card Hoàn thành</th>
                </tr>
            </thead>
            <tbody>
                @foreach($leaders as $idx => $row)
                <tr>
                    <td style="padding:8px;border-bottom:1px solid var(--border)">{{ $idx+1 }}</td>
                    <td style="padding:8px;border-bottom:1px solid var(--border)">{{ $row['name'] }}</td>
                    <td style="padding:8px;border-bottom:1px solid var(--border)">{{ $row['email'] }}</td>
                    <td style="padding:8px;border-bottom:1px solid var(--border)"><strong>{{ $row['count'] }}</strong></td>
                </tr>
                @endforeach
            </tbody>
        </table>
    </div>
    @endif
</section>
@endsection
