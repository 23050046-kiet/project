<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class UserCardProgress extends Model
{
    use HasFactory;

    protected $table = 'user_card_progress';

    protected $fillable = [
        'user_id',
        'desk_id',
        'completed_at',
    ];

    protected function casts(): array
    {
        return [
            'completed_at' => 'datetime',
            'next_review_at' => 'datetime',
            'review_stage' => 'integer',
        ];
    }
}
