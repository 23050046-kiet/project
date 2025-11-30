<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::table('user_card_progress', function (Blueprint $table) {
            $table->unsignedTinyInteger('review_stage')->default(0)->after('next_review_at');
        });
    }

    public function down(): void
    {
        Schema::table('user_card_progress', function (Blueprint $table) {
            $table->dropColumn('review_stage');
        });
    }
};
