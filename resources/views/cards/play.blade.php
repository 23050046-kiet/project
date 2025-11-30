@extends('layouts.app')

@section('title','Học Cards')

@section('content')
<section class="card" style="min-height:60vh">
    <h2 style="margin-bottom:12px">Học Card</h2>
    @php($cards = $desks->map(function($d){
        return [
            'id' => $d->id,
            'name' => $d->name_en,
            'img' => $d->image_path ? asset('storage/'.$d->image_path) : null,
        ];
    }))

    <div id="card-app" data-cards='@json($cards)' data-completed='@json($completedIds)' data-due='@json($dueIds)'></div>

    <style>
        .flip-wrap{perspective:1000px;max-width:520px;margin:24px auto}
        .flip-card{position:relative;width:100%;height:320px;transform-style:preserve-3d;transition:transform .6s}
        .flip-card.flipped{transform:rotateY(180deg)}
        .flip-face{position:absolute;inset:0;border:1px solid var(--border);border-radius:12px;background:#0b1220;padding:16px;display:flex;align-items:center;justify-content:center;backface-visibility:hidden}
        .flip-face.back{transform:rotateY(180deg)}
        .flip-face img{max-width:100%;max-height:100%;object-fit:contain;border-radius:10px}
        .controls{display:flex;gap:8px;justify-content:center;margin-top:16px}
        .counter{margin-top:8px;text-align:center;color:var(--muted)}
        .nav-nums{display:flex;gap:8px;justify-content:center;margin-top:16px}
        .nav-nums .num{width:36px;height:36px;display:flex;align-items:center;justify-content:center;border:1px solid var(--border);border-radius:8px;background:#0b1220;color:var(--text);cursor:pointer}
        .nav-nums .num.active{background:var(--primary);border-color:var(--primary)}
        .nav-nums .num.disabled{opacity:.5;cursor:not-allowed}
        .nav-nums .num.due{box-shadow:0 0 0 0 rgba(234,179,8,.8); border-color:#eab308; background:#3f3a1f}
        @keyframes pulseDue{0%{box-shadow:0 0 0 0 rgba(234,179,8,.7)}70%{box-shadow:0 0 0 10px rgba(234,179,8,0)}100%{box-shadow:0 0 0 0 rgba(234,179,8,0)}}
        .nav-nums .num.due{animation:pulseDue 2s infinite}
    </style>

    <div class="flip-wrap">
        <div class="flip-card" id="flip-card">
            <div class="flip-face front" id="front">
                <div class="muted">Bấm để lật xem nghĩa</div>
            </div>
            <div class="flip-face back" id="back">
                <div class="muted">…</div>
            </div>
        </div>
        <div class="nav-nums" id="nav-nums"></div>
        <div class="controls">
            <button class="btn" id="prev">⟵ Trước</button>
            <button class="btn btn-primary" id="flip">Lật</button>
            <button class="btn" id="next">Sau ⟶</button>
        </div>
        <div class="counter" id="counter">0 / 0</div>
    </div>

    <script>
    (function(){
        var root = document.getElementById('card-app');
        var data = [];
        var completed = [];
        try{ data = JSON.parse(root.getAttribute('data-cards')) || []; }catch(e){}
        try{ completed = JSON.parse(root.getAttribute('data-completed')) || []; }catch(e){}
        var completedSet = new Set(completed);
        var due = [];
        try{ due = JSON.parse(root.getAttribute('data-due')) || []; }catch(e){}
        var dueSet = new Set(due);
        var i = 0;
        var flipEl = document.getElementById('flip-card');
        var frontEl = document.getElementById('front');
        var backEl = document.getElementById('back');
        var counterEl = document.getElementById('counter');
        var navNumsEl = document.getElementById('nav-nums');
        var prevBtn = document.getElementById('prev');
        var nextBtn = document.getElementById('next');
        var flipBtn = document.getElementById('flip');
        var hasFlippedCurrent = false;

        function computeAllowedIndex(){
            var allowed = 0;
            for (var k=0;k<data.length;k++){
                var id = data[k].id;
                if (completedSet.has(id)) allowed = k+1; else break;
            }
            return allowed; // user may access indices <= allowed
        }

        function renderNav(){
            navNumsEl.innerHTML = '';
            var allowed = computeAllowedIndex();
            for (var idx=0; idx<data.length; idx++){
                var btn = document.createElement('button');
                var isDue = data[idx] && dueSet.has(data[idx].id);
                btn.className = 'num'+(idx===i ? ' active' : '')+ (idx>allowed ? ' disabled' : '') + (isDue ? ' due' : '');
                btn.textContent = (idx+1);
                (function(n){
                    btn.addEventListener('click', function(){
                        if (n>allowed) return; // blocked
                        setIndex(n);
                    });
                })(idx);
                navNumsEl.appendChild(btn);
            }
        }

        function render(){
            if(!data.length){
                frontEl.innerHTML = '<div class="muted">Chưa có card nào</div>';
                backEl.innerHTML = '<div class="muted">Thêm card trong Admin</div>';
                counterEl.textContent = '0 / 0';
                return;
            }
            var item = data[i];
            frontEl.innerHTML = item.img ? ('<img src="'+item.img+'" alt="'+(item.name||'')+'">') : '<div class="muted">(Không có hình)</div>';
            backEl.innerHTML = '<h2 style="margin:0;font-size:28px">'+(item.name||'')+'</h2>';
            counterEl.textContent = (i+1)+' / '+data.length;
            renderNav();
        }

        function setIndex(n){
            if(!data.length) return;
            i = (n<0) ? data.length-1 : (n>=data.length ? 0 : n);
            flipEl.classList.remove('flipped');
            hasFlippedCurrent = false;
            render();
        }

        function markCompleted(){
            var item = data[i];
            if (!item) return;
            // Gửi cập nhật nếu là lần đầu hoàn thành hoặc thẻ đang đến hạn ôn
            var needUpdate = !completedSet.has(item.id) || dueSet.has(item.id);
            if (!needUpdate) return;
            // send progress
            fetch('{{ route('cards.complete') }}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': '{{ csrf_token() }}'
                },
                body: JSON.stringify({ desk_id: item.id })
            }).then(function(){
                completedSet.add(item.id);
                // Vừa ôn xong thẻ đến hạn: bỏ highlight ngay cho UI đồng bộ
                if (dueSet.has(item.id)) { dueSet.delete(item.id); }
                renderNav();
            }).catch(function(){});
        }

        flipEl.addEventListener('click', function(){
            flipEl.classList.toggle('flipped');
            hasFlippedCurrent = flipEl.classList.contains('flipped');
            if (hasFlippedCurrent) markCompleted();
        });
        flipBtn.addEventListener('click', function(){
            flipEl.classList.toggle('flipped');
            hasFlippedCurrent = flipEl.classList.contains('flipped');
            if (hasFlippedCurrent) markCompleted();
        });
        prevBtn.addEventListener('click', function(){ setIndex(i-1); });
        nextBtn.addEventListener('click', function(){
            var allowed = computeAllowedIndex();
            if (i>=allowed){
                // require flip before moving forward
                // small toast
                var t = document.createElement('div');
                t.style = 'position:fixed;top:16px;right:16px;z-index:1000;background:#7f1d1d;color:#fecaca;border:1px solid #991b1b;border-radius:10px;padding:12px 14px;box-shadow:0 10px 25px rgba(0,0,0,.35);transition:opacity .3s ease, transform .3s ease;opacity:1;';
                t.textContent = 'Hãy lật thẻ trước khi sang thẻ tiếp theo';
                document.body.appendChild(t);
                setTimeout(function(){ t.style.opacity='0'; t.style.transform='translateY(-8px)'; }, 1800);
                setTimeout(function(){ if(t && t.parentNode){ t.parentNode.removeChild(t); } }, 2200);
                return;
            }
            setIndex(i+1);
        });

        render();
    })();
    </script>
</section>
@endsection
