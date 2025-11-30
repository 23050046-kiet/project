<?php

namespace App\Http\Controllers;

use App\Models\Desk;
use App\Models\UserCardProgress;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class CardController extends Controller
{
    public function play()
    {
        // Use ascending order so newly added cards appear at the end
        $desks = Desk::query()->orderBy('id','asc')->get(['id','name_en','image_path','created_at']);
        $completedIds = [];
        $dueIds = [];
        if (Auth::check()) {
            $completedIds = UserCardProgress::where('user_id', Auth::id())
                ->whereNotNull('completed_at')
                ->pluck('desk_id')
                ->all();
            $dueIds = UserCardProgress::where('user_id', Auth::id())
                ->whereNotNull('next_review_at')
                ->where('next_review_at', '<=', now())
                ->pluck('desk_id')
                ->all();
        }
        return view('cards.play', [
            'desks' => $desks,
            'completedIds' => $completedIds,
            'dueIds' => $dueIds,
        ]);
    }

    public function complete(Request $request)
    {
        $request->validate([
            'desk_id' => ['required','integer','exists:desks,id'],
        ]);
        $userId = Auth::id();
        $deskId = (int) $request->input('desk_id');

        $progress = UserCardProgress::firstOrCreate([
            'user_id' => $userId,
            'desk_id' => $deskId,
        ]);
        if (is_null($progress->completed_at)) {
            // First time flip: mark completed and schedule first review (5m)
            $progress->completed_at = now();
            $progress->review_stage = 1;
            $progress->next_review_at = now()->addSeconds(10);
        } else {
            // Advance schedule: 5m -> 10m -> 1d -> stop
            $stage = (int)($progress->review_stage ?? 0);
            if ($stage < 1) { $stage = 1; }
            if ($stage === 1) {
                $progress->review_stage = 2;
                $progress->next_review_at = now()->addMinutes(10);
            } elseif ($stage === 2) {
                $progress->review_stage = 3;
                $progress->next_review_at = now()->addDay();
            } else {
                // Stage >=3: stop scheduling further reviews
                $progress->review_stage = 4;
                $progress->next_review_at = null;
            }
        }
        $progress->save();
        return response()->json(['ok' => true]);
    }
}
