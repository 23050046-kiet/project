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
        if (Auth::check()) {
            $completedIds = UserCardProgress::where('user_id', Auth::id())
                ->whereNotNull('completed_at')
                ->pluck('desk_id')
                ->all();
        }
        return view('cards.play', [
            'desks' => $desks,
            'completedIds' => $completedIds,
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
            $progress->completed_at = now();
            $progress->save();
        }
        return response()->json(['ok' => true]);
    }
}
