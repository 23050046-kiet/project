<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\AdminController;
use App\Http\Controllers\CardController;

Route::get('/', function () {
    return view('welcome');
});

// Auth routes
Route::middleware('guest')->group(function () {
    Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
    Route::post('/login', [AuthController::class, 'login'])->name('login.post');
    Route::get('/register', [AuthController::class, 'showRegister'])->name('register');
    Route::post('/register', [AuthController::class, 'register'])->name('register.post');
});

Route::post('/logout', [AuthController::class, 'logout'])->name('logout')->middleware('auth');

// User dashboard with progress data
Route::get('/dashboard', function () {
    $user = auth()->user();
    $total = \App\Models\Desk::count();
    $completed = 0;
    if ($user) {
        $completed = \App\Models\UserCardProgress::where('user_id', $user->id)
            ->whereNotNull('completed_at')
            ->count();
    }
    // Leaderboard: top users by completed cards
    $leaderRows = \App\Models\UserCardProgress::selectRaw('user_id, COUNT(*) as cnt')
        ->whereNotNull('completed_at')
        ->groupBy('user_id')
        ->orderByDesc('cnt')
        ->limit(10)
        ->get();
    $usersMap = \App\Models\User::whereIn('id', $leaderRows->pluck('user_id'))
        ->get(['id','name','email'])
        ->keyBy('id');
    $leaderboard = $leaderRows->map(function ($row) use ($usersMap) {
        $u = $usersMap->get($row->user_id);
        return [
            'id' => $row->user_id,
            'name' => $u?->name ?? 'Unknown',
            'email' => $u?->email ?? '',
            'count' => (int) $row->cnt,
        ];
    });
    return view('dashboard', compact('total', 'completed', 'leaderboard'));
})->name('dashboard')->middleware('auth');

// User card play page
Route::get('/cards', [CardController::class, 'play'])->name('cards.play')->middleware('auth');
Route::post('/cards/complete', [CardController::class, 'complete'])->name('cards.complete')->middleware('auth');

// Admin routes
Route::middleware(['auth','admin'])->group(function () {
    Route::get('/admin', [AdminController::class, 'dashboard'])->name('admin.dashboard');
    Route::get('/admin/desks', [\App\Http\Controllers\DeskController::class, 'index'])->name('admin.desks.index');
    Route::get('/admin/desks/create', [\App\Http\Controllers\DeskController::class, 'create'])->name('admin.desks.create');
    Route::post('/admin/desks', [\App\Http\Controllers\DeskController::class, 'store'])->name('admin.desks.store');
    Route::delete('/admin/desks/{desk}', [\App\Http\Controllers\DeskController::class, 'destroy'])->name('admin.desks.destroy');

    // Manage users inline on dashboard
    Route::delete('/admin/users/{user}', [AdminController::class, 'destroyUser'])->name('admin.users.destroy');
});
