/**
 * TAI XIU GRAND MASTER - SERVER BOT 24/7
 * Hướng dẫn chạy:
 * 1. Cài đặt Node.js
 * 2. Chạy lệnh: npm init -y
 * 3. Chạy lệnh: node server.js
 */

const fs = require('fs');

// Cấu hình Game
const CONFIG = {
    SAVE_FILE: './database.json',
    TICK_RATE: 15000, // Mỗi phiên cách nhau 15 giây
    INITIAL_BALANCE: 10000000,
    CHIP_SAMPLES: [100000, 500000, 1000000, 5000000]
};

// Khởi tạo dữ liệu
let data = {
    balance: CONFIG.INITIAL_BALANCE,
    history: [],
    sessionId: 1000
};

// Đọc dữ liệu cũ nếu có
if (fs.existsSync(CONFIG.SAVE_FILE)) {
    data = JSON.parse(fs.readFileSync(CONFIG.SAVE_FILE));
}

function save() {
    fs.writeFileSync(CONFIG.SAVE_FILE, JSON.stringify(data, null, 2));
}

function log(msg) {
    const now = new Date().toLocaleTimeString('vi-VN');
    console.log(`[${now}] ${msg}`);
}

function runSession() {
    data.sessionId++;
    log(`--- PHIÊN MỚI: #GM-${data.sessionId} ---`);

    // 1. Giả lập đặt cược tự động
    const side = Math.random() > 0.5 ? 'TAI' : 'XIU';
    const betAmt = CONFIG.CHIP_SAMPLES[Math.floor(Math.random() * CONFIG.CHIP_SAMPLES.length)];
    
    if (data.balance < betAmt) {
        log("CẢNH BÁO: Số dư không đủ để đặt cược tiếp!");
    } else {
        data.balance -= betAmt;
        log(`Bot đặt cược: ${side} - Số tiền: ${betAmt.toLocaleString()} VND`);
    }

    // 2. Lắc xúc xắc
    const d1 = Math.floor(Math.random() * 6) + 1;
    const d2 = Math.floor(Math.random() * 6) + 1;
    const d3 = Math.floor(Math.random() * 6) + 1;
    const total = d1 + d2 + d3;
    const result = total >= 11 ? 'TAI' : 'XIU';

    log(`Kết quả: ${d1}-${d2}-${d3} => ${total} (${result})`);

    // 3. Tính toán thắng thua
    if (side === result) {
        const winAmt = Math.floor(betAmt * 1.98);
        data.balance += winAmt;
        log(`CHÚC MỪNG: Thắng +${winAmt.toLocaleString()} VND`);
    } else {
        log(`CHIA BUỒN: Thua -${betAmt.toLocaleString()} VND`);
    }

    // 4. Cập nhật lịch sử
    data.history.push(result);
    if (data.history.length > 50) data.history.shift();
    
    log(`Số dư hiện tại: ${data.balance.toLocaleString()} VND`);
    log(`Lịch sử gần đây: ${data.history.join(' | ')}`);
    
    save();
    log(`Chờ phiên tiếp theo trong ${CONFIG.TICK_RATE/1000}s...\n`);
}

// Chạy vòng lặp 24/7
log("HỆ THỐNG TÀI XỈU BOT 24/7 ĐANG KHỞI CHẠY...");
setInterval(runSession, CONFIG.TICK_RATE);
runSession(); // Chạy ngay lập tức phiên đầu tiên
