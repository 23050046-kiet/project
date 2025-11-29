<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Auth;
use App\Models\User;
use Illuminate\Http\Request;

class AdminController extends Controller
{
    public function dashboard()
    {
        $users = User::query()->orderBy('id','asc')->paginate(10);
        return view('admin.dashboard', compact('users'));
    }

    public function destroyUser(User $user, Request $request)
    {
        if ($user->id === Auth::id()) {
            return back()->with('error', 'Không thể xóa tài khoản của chính bạn.');
        }
        $user->delete();
        return back()->with('success', 'Xóa user thành công!');
    }
}
