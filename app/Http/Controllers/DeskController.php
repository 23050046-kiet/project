<?php

namespace App\Http\Controllers;

use App\Models\Desk;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class DeskController extends Controller
{
    public function index()
    {
        $desks = Desk::query()->latest()->paginate(10);
        return view('admin.desks.index', compact('desks'));
    }

    public function create()
    {
        return view('admin.desks.create');
    }

    public function store(Request $request)
    {
        $data = $request->validate([
            'name_en' => ['required','string','max:255'],
            'image' => ['required','image','max:2048'],
        ]);

        $imagePath = $request->file('image')->store('desks', 'public');

        Desk::create([
            'name_en' => $data['name_en'],
            'image_path' => $imagePath,
        ]);

        return redirect()->back()->with('success', 'Tạo card thành công!');
    }

    public function destroy(Desk $desk)
    {
        if ($desk->image_path) {
            Storage::disk('public')->delete($desk->image_path);
        }
        $desk->delete();
        return redirect()->route('admin.desks.index')->with('success', 'Xóa card thành công!');
    }
}
