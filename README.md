# Flash Card App

Ứng dụng web flash card đơn giản xây dựng bằng \`php\` và \`javascript\`, quản lý phụ thuộc bằng \`composer\` và \`npm\`. Ứng dụng hỗ trợ tạo, ôn tập, quản lý flash card với phiên ôn luyện theo lặp lại ngắt quãng.

## Công nghệ

- Backend: \`php\` (\`laravel\`)
- Frontend: \`javascript\`
- Trình quản lý gói: \`composer\`, \`npm\`

## Tính năng
- User / Admin - dang nhap , dang ki 
- Tạo, sửa, xoá flash card (import file ảnh)
- Phiên ôn tập với thuật toán lặp lại ngắt quãng đơn giản 10s 10phuts 1 ngay spaced repetition
- Theo dõi tiến độ và thống kê cơ bản, chart tien dộ, bảng xếp hạng(leaderboard)
- Giao diện responsive

## Cấu trúc dự án

- \`public/\`: web root
- \`app/\`, \`routes/\`, \`database/\`: mã nguồn \`laravel\`
- \`resources/\`: views, assets
- \`vendor/\`: phụ thuộc \`composer\`
- \`node_modules/\`: phụ thuộc \`npm\`

## Cài đặt \& Chạy (Windows)
0. Hỗ trợ : WAMPP hoac XAMPP
1. Mở \`VS Code\` hoặc \`PhpStorm\`, kéo dự án về máy.
2. Đổi tên \`.env.example\` thành \`.env\`.
3. Sửa cấu hình DB trong \`.env\`:
    - \`DB_CONNECTION=mysql\`
    - \`DB_HOST=127.0.0.1\`
    - \`DB_PORT=3306\`
    - \`DB_DATABASE=laravel\`
    - \`DB_USERNAME=root\`
    - \`DB_PASSWORD=\`
4. Cài phụ thuộc:
    - \`composer install\`
5. Tạo app key:
    - \`php artisan key:generate\`
6. Migration:
    - \`php artisan migrate\`
7. Seed dữ liệu:
    - \`php artisan db:seed\`
8. Liên kết storage:
    - \`php artisan storage:link\`
9. Truy cập:
    - Mở Chrome: \`http://localhost/vibecode/public/\`
    - Đăng nhập: \`admin@example.com\` /\`admin123\`

## Scripts

- \`npm install\`, \`npm run dev\`, \`npm run build\`

## Ghi chú phát triển

- Thiết kế mô hình \`Card\`, \`ReviewSession\`.
- Áp dụng MVC của \`laravel\`, mô-đun hoá \`javascript\`.
- Rà soát mã, sửa lỗi về routing, state management, build.

## Tài khoản quản trị (Admin)

- Email: \`admin@example.com\`
- Mật khẩu: \`admin123\`
- Trang quản trị: \`/admin\` (nếu có cấu hình)

## Triển khai

- \`composer install --no-dev\`
- \`php artisan migrate --force\`
- \`npm run build\`
- Tr trỏ web server tới \`public/\`
