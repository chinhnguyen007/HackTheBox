# Linh Ẩn Thôn — Chapter 1

Bộ tài liệu thiết kế và dữ liệu màn chơi cho một game **2D point-and-click kinh dị dân gian Việt Nam**.

Bối cảnh: ngôi nhà cổ làng quê Bắc Bộ thập niên 1990. Chủ đề: hủ tục **cúng thế mạng**.
Phong cách: "Áo Cưới Giấy", vẽ tay, u tối. Nền tảng: Android & iOS, APK engine ≤ 30 MB, asset tải qua Unity Addressables.

Toàn bộ nội dung trong thư mục này được sinh theo **Master Form** 4 module: kịch bản → prompt đồ họa → JSON màn chơi → cấu hình LiveOps.

---

## Chương 1 có gì

Mọi con số dưới đây được **đếm trực tiếp từ dữ liệu**, không chép từ tài liệu:

| Đại lượng | Giá trị |
|---|---|
| Khu vực | 5 |
| Hotspot | 67 — `EXAMINE` 38 · `COLLECT_ITEM` 8 · `CHANGE_AREA` 8 · `ZOOM_PUZZLE` 6 · `USE_ITEM` 4 · `DIALOGUE` 3 |
| Câu đố | 6 — đủ 6 loại: `ROTATION_LOCK` `SEQUENCE_ORDER` `SLIDING_TILE` `ITEM_COMBINE` `PATTERN_TRACE` `AUDIO_MATCH` |
| Jump-scare | 8 |
| Vật phẩm | 10 |
| Khóa localization | 57 |
| Bất biến LiveOps | 17 |

Thứ tự chơi: `area_san_gach` → `area_hien_nha` → `area_gian_tho` → `area_bep_gieng` → `area_gac_xep`.

---

## Cấu trúc

```
docs/
  01_KICH_BAN_CHAPTER_01.md        Bước 1 — kịch bản, lore, vị trí vật phẩm, logic câu đố
  02_PROMPT_DO_HOA.md              Bước 2 — 3 bộ prompt Midjourney/SD + khóa nhất quán phong cách
  03_DATA_SPEC.md                  Đặc tả trường dữ liệu (hợp đồng giữa CMS và engine)
  04_LIVEOPS_MONETIZATION.md       Bước 4 — hint, IAP, sự kiện theo mùa, telemetry
  05_TICH_HOP_UNITY_ADDRESSABLES.md  Ngân sách dung lượng, nhóm bundle, chiến lược tải
  06_AN_TOAN_NGUOI_CHOI.md         Nhạy sáng ≤3 Hz, chế độ nhẹ nhàng, haptic
data/
  chapter_01.json                  Manifest chương: thứ tự khu vực, cổng mở khóa, item catalog
  areas/<area_id>.json             Bước 3 — 1 file/khu vực, đúng schema Master Form
  liveops_chapter_01.json          Cấu hình LiveOps
schema/
  level.schema.json                JSON Schema cho file khu vực
  liveops.schema.json              JSON Schema cho LiveOps
tools/
  validate_level.py                Trình kiểm chứng (chỉ dùng thư viện chuẩn Python 3)
```

---

## Kiểm chứng dữ liệu

```bash
python3 tools/validate_level.py            # kiểm thường
python3 tools/validate_level.py --strict   # nâng cảnh báo thành lỗi — dùng cho cổng CI
python3 tools/validate_level.py --self-test  # tự kiểm đột biến (xem bên dưới)
python3 tools/validate_level.py /duong/dan/khac/data   # trỏ vào thư mục data khác
```

Không cần cài gì thêm — chỉ thư viện chuẩn Python 3.

Trình kiểm tra soát tham chiếu chéo, ID trùng, hotspot chồng lấn, biên 1920×1080, ngưỡng vùng chạm,
chu trình trong đồ thị phụ thuộc vật phẩm, vật phẩm chết, cú dọa không thể bắn ra, và **tính khả giải**
của cả chương bằng mô phỏng điểm bất động.

### `--self-test` dùng để làm gì

Một trình kiểm tra có thể báo "dữ liệu sạch" mà thực ra **không hề đọc** trường nó tuyên bố đang kiểm.
Dự án này đã dính đúng lỗi đó: ở các bản đầu, validator tự suy ra cờ tiến trình từ *tên định danh* câu đố
rồi nạp chính cái đoán đó vào kết luận "khả giải" — nên nó báo `[OK] KHẢ GIẢI 5/5 khu vực` trên một
chương thực ra chết cứng ở khu vực thứ hai.

`--self-test` tồn tại để bắt chính kiểu lỗi đó. Nó lần lượt **làm hỏng từng điểm dữ liệu** (đổi giá trị và
xóa hẳn khóa), chạy lại toàn bộ phép kiểm, và đòi trình kiểm phải báo lỗi ở mọi điểm. Thoát 0 chỉ khi
phát hiện 100%.

> Nếu bạn sửa `validate_level.py`, hãy chạy `--self-test` trước khi tin bất kỳ kết quả `[OK]` nào.
> Một phép kiểm không tự chứng minh được nó đọc dữ liệu thật thì không đáng tin.

---

## Quy ước dữ liệu

- **Hệ tọa độ**: 1920×1080, gốc trên-trái, `x` sang phải, `y` xuống dưới.
- **`bounds` là vùng chạm**, cạnh tối thiểu 120 px @1920. Khi sprite vẽ nhỏ hơn vùng chạm, kích thước vẽ
  thật nằm ở `visual_bounds` (phải nằm trọn trong `bounds`).
- **Cờ tiến trình chỉ đến từ `grants_flag` ghi thẳng trong JSON.** Không có suy diễn theo tên — nếu một cờ
  được tham chiếu mà không ai cấp phát, đó là lỗi.
- **`background_asset_url` là khóa logic**, không phải URL tải thẳng; engine phân giải qua Addressables.
  Xem `docs/05` mục 5.2.
- ID dùng snake_case không dấu với tiền tố `area_` `hs_` `puz_` `scare_` `item_`. Chuỗi hiển thị tiếng Việt
  có dấu.

---

## Sửa nội dung mà không build lại app

Dữ liệu màn chơi và cấu hình LiveOps đều là JSON đẩy qua CMS → CDN, không nhúng trong APK.
Đổi vị trí hotspot, lời giải câu đố, giá hint hay theme sự kiện đều không cần bản build mới.

Quy trình an toàn: sửa JSON → chạy `--strict` và `--self-test` → cả hai thoát 0 → mới đẩy lên CMS.
