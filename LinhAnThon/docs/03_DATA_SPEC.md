# LINH AN THÔN — CHƯƠNG 1
## ĐẶC TẢ TRƯỜNG DỮ LIỆU (DATA SPEC)

| Trường | Giá trị |
|---|---|
| Dự án | **Linh An Thôn — Chapter 1** |
| Tài liệu | `docs/03_DATA_SPEC.md` — hợp đồng kỹ thuật giữa tổ thiết kế và tổ engine |
| Phạm vi | `data/chapter_01.json` · `data/areas/<area_id>.json` · `data/liveops_chapter_01.json` |
| Schema kiểm tra | `schema/level.schema.json` · `schema/liveops.schema.json` (JSON Schema draft 2020-12) |
| Công cụ kiểm tra | `tools/validate_level.py` — Python 3, **chỉ thư viện chuẩn** |
| Độ phân giải thiết kế | **1920 × 1080**, gốc toạ độ **(0,0) ở góc trên-bên trái**, x sang phải, y xuống dưới |
| Nguồn sự thật | SPINE đã chốt — không đổi bất kỳ `area_id` / `item_id` / `puzzle_id` / `scare_id` nào |
| Ngôn ngữ | Tài liệu: tiếng Việt có dấu. Mọi `id` và khoá JSON: **snake_case không dấu** |
| Ngày cập nhật | 2026-09-15 |

> **Tài liệu này là hợp đồng, không phải gợi ý.** Mỗi dòng trong các bảng dưới đây đều được cưỡng chế bằng một trong hai lớp: **JSON Schema** (cấu trúc, kiểu, enum, ràng buộc có điều kiện trong phạm vi một file) hoặc **`tools/validate_level.py`** (mọi ràng buộc liên file: tham chiếu chéo, id duy nhất toàn chương, chồng lấn hotspot, chu trình phụ thuộc vật phẩm, chứng minh khả giải). Trường nào không có ở đây thì không được xuất hiện trong file dữ liệu — cả hai schema đều đặt `additionalProperties: false` ở các khối cốt lõi.

---

# 0. CÁCH ĐỌC CÁC BẢNG

| Ký hiệu cột "Bắt buộc" | Nghĩa |
|---|---|
| **Có** | Thiếu trường này là **[LỖI]**. Build bị chặn. |
| **Có ¹** | Bắt buộc *có điều kiện* — chỉ khi `action_type` / `trigger_type` / `type` tương ứng. Xem ma trận ở §2.3.2, §2.4.2, §2.5.2. |
| Không | Tuỳ chọn. Bỏ trống thì engine dùng giá trị mặc định ghi trong cột "Ràng buộc". |
| Không ★ | Tuỳ chọn nhưng **rất khuyến nghị**. Thiếu thì validator vẫn chạy được nhưng phải *suy luận*, và sẽ phát **[CẢNH BÁO]**. Xem §5.3. |

| Ký hiệu khác | Nghĩa |
|---|---|
| `null` | Giá trị JSON null — **khác hẳn** với việc không khai báo trường. Khi bảng ghi "null hoặc ...", trường đó vẫn **phải có mặt**. |
| **MF** | Khoá bắt buộc theo Master Form. Cấm đổi tên, cấm đổi vị trí. |
| `[[ ... ]]` | Ghi chú sản xuất, không thuộc hợp đồng. |

---

# 1. KIẾN TRÚC BA TẦNG CỦA DỮ LIỆU

```
data/chapter_01.json ............... MANIFEST CHƯƠNG (tầng 1)
   │                                 Ai tồn tại, theo thứ tự nào, mở khoá bằng gì.
   │                                 Sổ đăng ký DUY NHẤT của vật phẩm (item_catalog).
   │
   ├── areas/area_san_gach.json .... KHU VỰC (tầng 2)
   ├── areas/area_hien_nha.json      Nội dung chơi được: hotspot, câu đố, cú doạ.
   ├── areas/area_gian_tho.json      Mỗi file là một màn hình, độc lập, tải riêng.
   ├── areas/area_bep_gieng.json
   └── areas/area_gac_xep.json
                                     
data/liveops_chapter_01.json ...... CẤU HÌNH VẬN HÀNH (tầng 3)
                                     Gợi ý, IAP, sự kiện mùa, gem, quảng cáo.
                                     Đẩy qua remote config, KHÔNG build lại app.
```

**Ba quy tắc phân tầng, không được vi phạm:**

1. **Tầng 2 không bao giờ khai báo vật phẩm mới.** File khu vực chỉ *tham chiếu* `item_id`; nơi khai báo duy nhất là `item_catalog` ở tầng 1. Validator bắt lỗi mọi `item_id` lạ.
2. **Tầng 2 không biết gì về nhau.** `target_puzzle_id` và `wrong_action_jumpscare` **bắt buộc** trỏ vào chính file đó. Cầu nối duy nhất giữa hai khu vực là `CHANGE_AREA` + `unlock_condition` ở tầng 1.
3. **Tầng 3 không được sửa tầng 2.** LiveOps chỉ thay lớp trang trí. `hotspot_bounds`, `puzzle_solution`, `jumpscare_trigger_type`, `max_fails` nằm trong danh sách `does_not_change` — bất biến 10, xem §4.5.

---

# 2. ĐẶC TẢ `data/areas/<area_id>.json` — FILE KHU VỰC

## 2.1. Cấp gốc

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `chapter_id` | string | **Có** | Chương chứa khu vực này | `^chapter_[0-9]{2}$`. Phải khớp `chapter_id` của manifest |
| `area_id` | string | **Có** | Mã khu vực | `^area_[a-z0-9_]+$`. Phải khớp **tên file** và phải có trong `area_order` của manifest |
| `background_asset_url` | string | **Có** | URL Addressables bundle chứa ảnh nền | HTTPS tuyệt đối, đuôi `.bundle`. **Cấm** nhúng ảnh thô vào APK engine |
| `hotspots` | array\<Hotspot\> | **Có** | Toàn bộ vùng chạm của màn hình | **Không được rỗng** — khu vực không có hotspot là ngõ cụt |
| `puzzles` | array\<Puzzle\> | **Có** | Các câu đố thuộc khu vực | Được phép rỗng `[]` |
| `jumpscares` | array\<Jumpscare\> | **Có** | Các cú doạ thuộc khu vực | Được phép rỗng `[]` |

`[[ Bốn khu vực có câu đố; area_gian_tho có hai (puz_tuan_tu_le_cung và puz_ba_hoi_chin_tieng). ]]`

## 2.2. Kiểu `Bounds` — hình chữ nhật vùng chạm

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `x` | integer | **Có** | Mép trái, pixel thiết kế | `0 ≤ x ≤ 1919` |
| `y` | integer | **Có** | Mép **trên** (y tăng xuống dưới) | `0 ≤ y ≤ 1079` |
| `width` | integer | **Có** | Chiều rộng | `> 0`, và `x + width ≤ 1920` |
| `height` | integer | **Có** | Chiều cao | `> 0`, và `y + height ≤ 1080` |

**Ba mức kiểm tra hình học:**

| Điều kiện | Mức | Lý do |
|---|---|---|
| `width ≤ 0` hoặc `height ≤ 0` | **[LỖI]** | Vùng chạm suy biến, người chơi không bao giờ bấm trúng |
| `x + width > 1920` hoặc `y + height > 1080` | **[LỖI]** | Tràn ra ngoài khung thiết kế; trên máy tỉ lệ khác sẽ bị cắt mất |
| `width < 88` hoặc `height < 88` | **[CẢNH BÁO]** | Dưới ngưỡng chạm ngón tay. Vẫn build được, nhưng QA phải thử tay thật trên máy 5 inch |

> **Vì sao gốc toạ độ ở góc trên-trái mà Unity thì không?** Unity dùng gốc dưới-trái. Tổ engine chịu trách nhiệm lật trục **một lần duy nhất** ở lớp nạp dữ liệu: `unity_y = 1080 - (y + height)`. Tổ thiết kế **luôn** làm việc theo hệ trên-trái vì mọi phần mềm dựng bố cục (Figma, Photoshop, Krita) đều dùng hệ này. Đừng lật trục trong file dữ liệu.

## 2.3. Kiểu `Hotspot`

### 2.3.1. Bảng trường

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `id` | string | **Có** | Mã vùng chạm | `^hs_[a-z0-9_]+$`, **duy nhất toàn chương** |
| `bounds` | Bounds | **Có** | Vị trí và kích thước | §2.2. **Không được chồng lấn** hotspot khác trong cùng khu vực |
| `action_type` | enum | **Có** | Việc xảy ra khi bấm | `ZOOM_PUZZLE` \| `COLLECT_ITEM` \| `EXAMINE` \| `USE_ITEM` \| `CHANGE_AREA` \| `DIALOGUE` |
| `target_puzzle_id` | string \| null | **Có ¹** | Câu đố sẽ mở | `^puz_...$`. Phải tồn tại **trong chính file này** |
| `target_area_id` | string | **Có ¹** | Khu vực sẽ đi tới | `^area_...$`. Phải có trong manifest. **Chỉ** `CHANGE_AREA` được mang trường này |
| `item_id` | string | **Có ¹** | Vật phẩm được trao (`COLLECT_ITEM`) hoặc được đặt vào (`USE_ITEM`) | `^item_...$`. Phải có trong `item_catalog` |
| `required_item` | string \| null | **Có ¹** | Vật phẩm phải có sẵn trong túi đồ | `^item_...$` hoặc `null`. Phải có trong `item_catalog` |
| `text_key` | string | **Có ¹** | Khoá localization của lời kể | `^txt_[a-z0-9_]+$`. **Cấm** nhúng chuỗi tiếng Việt vào file dữ liệu |
| `grants_flag` | string \| null | Không ★ | Cờ tiến trình bật lên sau khi hotspot chạy xong | `^flag_[a-z0-9_]+$`. Xem §5.3 — thiếu trường này thì validator phải suy luận |
| `required_flags` | array\<string\> | Không | Các cờ phải bật trước thì hotspot mới hoạt động | Mặc định `[]`. Mọi cờ phải có nguồn cấp |
| `one_shot` | boolean | Không | Hotspot biến mất sau lần kích hoạt đầu | Mặc định `false` |
| `enabled` | boolean | Không | Tắt hotspot mà không xoá dữ liệu | Mặc định `true`. Dùng cho kill-switch LiveOps |
| `ten_vi` | string | Không | Tên tiếng Việt cho công cụ nội bộ | ≤ 120 ký tự. Không hiển thị trong game |
| `ghi_chu_vi` | string | Không | Ghi chú sản xuất | ≤ 500 ký tự |

### 2.3.2. Ma trận bắt buộc theo `action_type`

Đây là phần được mã hoá thành các khối `if/then` trong `schema/level.schema.json`.

| `action_type` | Bắt buộc có | Bắt buộc **không** có | Ngữ nghĩa |
|---|---|---|---|
| `ZOOM_PUZZLE` | `target_puzzle_id` | `target_area_id` | Phóng to vào một câu đố trong cùng khu vực |
| `COLLECT_ITEM` | `item_id`, **và trường** `required_item` (giá trị được phép là `null`) | `target_area_id` | Nhặt vật phẩm vào túi đồ |
| `USE_ITEM` | `required_item` **khác null**, **và** ít nhất một trong `item_id` / `target_puzzle_id` | `target_area_id` | Dùng vật phẩm lên một điểm trong cảnh |
| `CHANGE_AREA` | `target_area_id` | — | Chuyển sang khu vực khác |
| `EXAMINE` | `text_key` | `item_id`, `required_item`, `target_puzzle_id`, `target_area_id` | Quan sát, hiện một đoạn mô tả |
| `DIALOGUE` | `text_key` | `item_id`, `required_item`, `target_puzzle_id`, `target_area_id` | Độc thoại nội tâm hoặc lời thoại |

**Phân biệt hai lỗi hay gặp nhất:**

- `COLLECT_ITEM` với `"required_item": null` → nhặt được ngay. **Xoá hẳn** trường `required_item` → **[LỖI]**, vì không phân biệt được "không cần điều kiện" với "quên khai báo điều kiện".
- `USE_ITEM` với `"required_item": null` → **[LỖI]**. Dùng vật phẩm thì bắt buộc phải nói rõ *vật phẩm nào*.

### 2.3.3. Bốn dạng `USE_ITEM` trong Chương 1

| Dạng | `required_item` | `item_id` | `target_puzzle_id` | `grants_flag` | Ví dụ trong chương |
|---|---|---|---|---|---|
| Đặt vào để mở đường | có | = `required_item` | — | **nên có** | `hs_o_lom_binh_phong` — tra bản rập vào ô lõm |
| Dùng làm then cửa | có | = `required_item` | — | **nên có** | `hs_khe_mong_cua_gac` — tra bài vị vào khe mộng |
| Soi sáng để lộ thông tin | có | = `required_item` | — | tuỳ | `hs_gieng_khoi` — soi đèn xuống lòng giếng |
| Dùng để mở câu đố | có | — | có | — | (dự phòng, chưa dùng ở Chương 1) |

`[[ Khi item_id trùng required_item nghĩa là vật phẩm KHÔNG bị tiêu thụ, chỉ được đặt vào chỗ. Engine giữ nguyên nó trong túi đồ. ]]`

## 2.4. Kiểu `Puzzle`

### 2.4.1. Bảng trường

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `id` | string | **Có** | Mã câu đố | `^puz_[a-z0-9_]+$`, duy nhất toàn chương |
| `type` | enum | **Có** | Thể loại cơ chế | `ROTATION_LOCK` \| `SEQUENCE_ORDER` \| `SLIDING_TILE` \| `ITEM_COMBINE` \| `PATTERN_TRACE` \| `AUDIO_MATCH` |
| `solution` | array\<integer\> | **Có** | Lời giải đúng | Không rỗng, ≤ 16 phần tử. Ngữ nghĩa theo `type` — §2.4.3 |
| `reward_item_id` | string \| null | **Có** | Vật phẩm trao khi giải đúng | `^item_...$` hoặc `null`. Phải có trong `item_catalog` |
| `wrong_action_jumpscare` | string \| null | **Có** | Cú doạ bắn khi giải sai | `^scare_...$` hoặc `null`. Phải tồn tại **trong chính file này** |
| `required_items` | array\<string\> | Không ★ | Vật phẩm **công cụ** phải có thì mới nhập được lời giải | Mặc định `[]`. Xem cảnh báo ở §5.4 |
| `grants_flag` | string \| null | Không | Cờ bật khi giải đúng | Mặc định dùng quy ước `flag_<id>_solved` |
| `ten_vi`, `ghi_chu_vi` | string | Không | Nhãn và ghi chú nội bộ | — |

### 2.4.2. Ràng buộc `solution` theo `type`

| `type` | Số phần tử | Cho phép lặp | Kiểm tra thêm |
|---|---|---|---|
| `ROTATION_LOCK` | 2 – 8 | **Có** (hai vòng có thể cùng vị trí) | Mỗi phần tử `0 ≤ v ≤ 11` |
| `SEQUENCE_ORDER` | ≥ 2 | Không | Phải là hoán vị các bước phân biệt, `v ≥ 1` |
| `PATTERN_TRACE` | ≥ 2 | Không | Mỗi nét chỉ đi một lần, `v ≥ 1` |
| `ITEM_COMBINE` | ≥ 2 | Không | Mỗi bước ghép chỉ làm một lần, `v ≥ 1` |
| `SLIDING_TILE` | **đúng 9 hoặc 16** | Không | Phải có **đúng một** số `0` = ô trống |
| `AUDIO_MATCH` | ≥ 2 | **Có** | Số tiếng gõ mỗi hồi, `1 ≤ v ≤ 32` |

### 2.4.3. Ngữ nghĩa `solution` của sáu câu đố Chương 1

| `puzzle_id` | `type` | `solution` | Đọc là |
|---|---|---|---|
| `puz_khoa_bat_quai` | `ROTATION_LOCK` | `[6, 3, 8]` | Ba vòng đồng tâm, đánh số tám quẻ Bát quái theo chiều kim đồng hồ từ chính Bắc. Vòng ngoài → quẻ **Khảm** (nước, toạ Bắc), vòng giữa → quẻ **Ly** (lửa, hướng Nam), vòng trong → quẻ **Khôn** (đất, phận nữ — Bà Cô) |
| `puz_rap_chu_the_menh` | `PATTERN_TRACE` | `[2,1,4,3,7,5,8,6]` | Thứ tự tám nét theo bút thuận Hán-Nôm: ngang trước sổ sau, trái trước phải sau, trên trước dưới sau, phẩy mác sau cùng |
| `puz_tuan_tu_le_cung` | `SEQUENCE_ORDER` | `[3,6,4,1,5,2]` | Vị trí hiện tại của sáu lễ vật trên bàn thờ, xếp theo đúng thứ tự tuần lễ cúng: lau bài vị → thắp đèn → thắp nhang → rót rượu → đọc văn khấn → hoá vàng |
| `puz_ba_hoi_chin_tieng` | `AUDIO_MATCH` | `[3,3,5,3,7,3]` | Ba cặp (số tiếng dồn, số tiếng chốt) của ba hồi mõ: hồi một 3+3, hồi hai 5+3, hồi ba 7+3 |
| `puz_thap_lai_den_dau` | `ITEM_COMBINE` | `[2,5,1,3,4]` | Thứ tự năm thao tác thắp đèn: xé vải điều se tim (2) → luồn tim qua cổ đèn (5) → chắt dầu vào bầu (1) → vặn tim vừa đủ (3) → mồi lửa bằng que đóm (4) |
| `puz_xep_anh_gia_pha` | `SLIDING_TILE` | `[2,5,7,4,8,3,6,1,0]` | Khung 3×3 đọc theo hàng. Số là mã mảnh ván, `0` là ô trống — **đúng chỗ khuôn mặt bị khoét** |

> **Quy tắc bất di bất dịch:** `solution` là dữ liệu, không phải bí mật. Nó nằm trong bundle mà máy người chơi tải về, nên **không** được dùng để chống gian lận. Mọi phần thưởng có giá trị thật (gem, mở khoá IAP) đều xác thực phía máy chủ — xem §4.3.

## 2.5. Kiểu `Jumpscare`

### 2.5.1. Bảng trường

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `id` | string | **Có** | Mã cú doạ | `^scare_[a-z0-9_]+$`, duy nhất toàn chương |
| `trigger_type` | enum | **Có** | Điều kiện bắn | `ON_PUZZLE_FAIL_COUNT` \| `ON_ENTER_AREA` \| `ON_COLLECT_ITEM` \| `ON_TIMER` \| `ON_WRONG_ITEM_USE` |
| `max_fails` | integer | **Có ¹** | Số lần giải sai liên tiếp trước khi bắn | `≥ 1`. **Chỉ** `ON_PUZZLE_FAIL_COUNT`; trigger khác mang trường này là **[LỖI]** |
| `delay_sec` | number | Không ★ | Số giây đứng yên trong khu vực trước khi bắn | `> 0`. **Chỉ** `ON_TIMER`. Thiếu → **[CẢNH BÁO]**, mỗi máy sẽ bắn một kiểu |
| `trigger_item_id` | string | Không | Vật phẩm gắn với cú doạ | **Chỉ** `ON_COLLECT_ITEM` / `ON_WRONG_ITEM_USE` |
| `audio_asset` | string | **Có** | File âm thanh | `<tên>.ogg` / `.mp3` / `.wav`. Chương 1 dùng **`.ogg`** — xem `docs/05` §4.3 |
| `sprite_animation` | string | **Có** | Hoạt ảnh sprite | `^anim_[a-z0-9_]+$` |
| `screen_flash` | boolean | **Có** | Có loé trắng màn hình không | `true` / `false`. **Phải khai báo tường minh** |
| `cooldown_sec` | number | Không | Thời gian nghỉ tối thiểu trước khi bắn lại | `≥ 0` |

### 2.5.2. Ma trận bắt buộc theo `trigger_type`

| `trigger_type` | Bắt buộc có | Cấm có | Bắn khi |
|---|---|---|---|
| `ON_PUZZLE_FAIL_COUNT` | `max_fails` | `delay_sec`, `trigger_item_id` | Giải sai đủ `max_fails` lần liên tiếp |
| `ON_ENTER_AREA` | — | `max_fails`, `delay_sec`, `trigger_item_id` | Lần đầu bước vào khu vực |
| `ON_COLLECT_ITEM` | — | `max_fails`, `delay_sec` | Nhặt vật phẩm (lọc theo `trigger_item_id` nếu có) |
| `ON_TIMER` | — (nhưng **nên** có `delay_sec`) | `max_fails`, `trigger_item_id` | Hết thời gian đứng yên |
| `ON_WRONG_ITEM_USE` | — | `max_fails`, `delay_sec` | Dùng sai vật phẩm lên hotspot |

**Kiểm tra chéo bổ sung:** nếu một câu đố trỏ `wrong_action_jumpscare` tới cú doạ X, mà X có `trigger_type` **không phải** `ON_PUZZLE_FAIL_COUNT` hoặc `ON_WRONG_ITEM_USE`, validator phát **[CẢNH BÁO]** — cú doạ đó sẽ không bao giờ bắn vì giải sai, tham chiếu là vô nghĩa.

## 2.6. Ví dụ đầy đủ — `data/areas/area_gian_tho.json` (trích)

```json
{
  "chapter_id": "chapter_01",
  "area_id": "area_gian_tho",
  "background_asset_url": "https://cdn.linhanthon.game/assets/bg_gian_tho.bundle",
  "hotspots": [
    {
      "id": "hs_ban_tho_ho",
      "bounds": { "x": 640, "y": 300, "width": 660, "height": 420 },
      "action_type": "ZOOM_PUZZLE",
      "target_puzzle_id": "puz_tuan_tu_le_cung"
    },
    {
      "id": "hs_dui_mo",
      "bounds": { "x": 560, "y": 780, "width": 110, "height": 120 },
      "action_type": "COLLECT_ITEM",
      "item_id": "item_dui_mo",
      "required_item": null
    },
    {
      "id": "hs_khe_mong_cua_gac",
      "bounds": { "x": 430, "y": 120, "width": 150, "height": 110 },
      "action_type": "USE_ITEM",
      "required_item": "item_bai_vi_khuyet_danh",
      "item_id": "item_bai_vi_khuyet_danh",
      "grants_flag": "flag_then_gac_da_tra"
    },
    {
      "id": "hs_van_khan",
      "bounds": { "x": 1330, "y": 740, "width": 230, "height": 140 },
      "action_type": "EXAMINE",
      "text_key": "txt_examine_van_khan"
    },
    {
      "id": "hs_cua_hau_xuong_bep",
      "bounds": { "x": 60, "y": 790, "width": 200, "height": 200 },
      "action_type": "CHANGE_AREA",
      "target_area_id": "area_bep_gieng"
    }
  ],
  "puzzles": [
    {
      "id": "puz_tuan_tu_le_cung",
      "type": "SEQUENCE_ORDER",
      "solution": [3, 6, 4, 1, 5, 2],
      "reward_item_id": "item_bai_vi_khuyet_danh",
      "wrong_action_jumpscare": "scare_khoi_tu_hinh_nguoi"
    },
    {
      "id": "puz_ba_hoi_chin_tieng",
      "type": "AUDIO_MATCH",
      "solution": [3, 3, 5, 3, 7, 3],
      "reward_item_id": "item_dai_vai_dieu",
      "wrong_action_jumpscare": "scare_khoi_tu_hinh_nguoi",
      "required_items": ["item_dui_mo"]
    }
  ],
  "jumpscares": [
    {
      "id": "scare_khoi_tu_hinh_nguoi",
      "trigger_type": "ON_PUZZLE_FAIL_COUNT",
      "max_fails": 3,
      "audio_asset": "sfx_scare_khoi_tu.ogg",
      "sprite_animation": "anim_khoi_tu_dang_nguoi",
      "screen_flash": false
    }
  ]
}
```

`[[ Hai trường in đậm về mặt giá trị thực tiễn: "grants_flag" trên hs_khe_mong_cua_gac và "required_items" trên puz_ba_hoi_chin_tieng. Không có chúng, file vẫn hợp lệ nhưng validator phải đoán, và item_dui_mo sẽ bị báo là vật phẩm chết. ]]`

---

# 3. ĐẶC TẢ `data/chapter_01.json` — MANIFEST CHƯƠNG

## 3.1. Cấp gốc

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `schema_version` | integer | **Có** | Phiên bản hợp đồng dữ liệu | `≥ 1`. Tăng khi đổi cấu trúc **không tương thích ngược** |
| `version` | string | **Có** | Phiên bản nội dung chương | SemVer `x.y.z` |
| `chapter_id` | string | **Có** | Mã chương | `^chapter_[0-9]{2}$` |
| `chapter_name` | string | Không | Tên hiển thị nội bộ | — |
| `language` | string | Không | Ngôn ngữ gốc | `vi-VN` |
| `design_resolution` | object | **Có** | Khung thiết kế | `{width: 1920, height: 1080, origin: "TOP_LEFT"}` — cố định |
| `cdn_base_url` | string | **Có** | Gốc CDN của mọi bundle | HTTPS. Có thể ghi đè bằng remote config lúc chạy |
| `start_area_id` | string | **Có** | Khu vực mở màn | Phải có trong `area_order`, và `unlock_condition.type` phải là `NONE` |
| `area_order` | array\<string\> | **Có** | Thứ tự tuyến tính các khu vực | Không rỗng. **Phần tử cuối = khu vực kết chương**, validator bắt buộc chứng minh tới được |
| `areas` | array\<AreaEntry\> | **Có** | Bảng đăng ký khu vực | Mọi `area_id` trong `area_order` phải có mục tương ứng |
| `item_catalog` | array\<ItemEntry\> | **Có** | **Sổ đăng ký vật phẩm duy nhất** của chương | Mọi `item_id` được tham chiếu ở bất kỳ đâu đều phải có ở đây |
| `puzzle_index`, `jumpscare_index` | array | Không | Bảng tra cứu phẳng cho công cụ nội bộ | Phải nhất quán với file khu vực |

## 3.2. Kiểu `AreaEntry`

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `area_id` | string | **Có** | Mã khu vực | Phải có trong `area_order` |
| `ten_vi` | string | Không | Tên tiếng Việt | Dùng cho công cụ nội bộ và log |
| `order` | integer | Không | Số thứ tự | Phải khớp vị trí trong `area_order` |
| `file` | string | **Có** | Đường dẫn tương đối tới file khu vực | Tính từ thư mục `data/` |
| `background_asset_url` | string | Không | Nhân bản từ file khu vực để tải trước | Nếu có thì phải khớp |
| `unlock_condition` | UnlockCondition | **Có** | Điều kiện mở khu vực | §3.3 |

## 3.3. Kiểu `UnlockCondition` — trái tim của logic tiến trình

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `type` | enum | **Có** | Phép hợp điều kiện | `NONE` (mở sẵn) \| `ALL_OF` (cần đủ) \| `ANY_OF` (cần một) |
| `required_items` | array\<string\> | **Có** | Vật phẩm phải có trong túi | Mọi phần tử phải có trong `item_catalog` |
| `required_flags` | array\<string\> | **Có** | Cờ tiến trình phải bật | Mọi cờ **phải có nguồn cấp** — xem §5.3 |
| `entry_hotspot_id` | string \| null | **Có** | Cửa vào (hotspot `CHANGE_AREA` dẫn tới đây) | Phải tồn tại. `null` với khu vực mở màn |
| `from_area_id` | string \| null | **Có** | Khu vực đứng trước | Phải tồn tại. Cũng là **phạm vi tìm kiếm** khi validator suy luận nguồn cấp cờ |
| `locked_text_key` | string \| null | **Có** | Lời nhắc khi cửa còn khoá | `^txt_...$` hoặc `null` |
| `mo_ta_vi` | string | Không | Mô tả điều kiện cho người đọc | Không dùng để cưỡng chế logic |

**Bảng mở khoá thực tế của Chương 1:**

| Thứ tự | `area_id` | `type` | Cần vật phẩm | Cần cờ |
|---|---|---|---|---|
| 1 | `area_san_gach` | `NONE` | — | — |
| 2 | `area_hien_nha` | `ALL_OF` | `item_chia_khoa_dong` | — |
| 3 | `area_gian_tho` | `ALL_OF` | — | `flag_binh_phong_da_tra` |
| 4 | `area_bep_gieng` | `ALL_OF` | — | `flag_puz_tuan_tu_le_cung_solved` |
| 5 | `area_gac_xep` | `ALL_OF` | `item_den_dau_sang` | `flag_then_gac_da_tra` |

## 3.4. Kiểu `ItemEntry`

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `item_id` | string | **Có** | Mã vật phẩm | `^item_[a-z0-9_]+$`, duy nhất toàn chương |
| `ten_vi` | string | **Có** | Tên hiển thị (qua localization) | — |
| `icon_asset` | string | **Có** | Biểu tượng trong túi đồ | `<tên>.png` — nằm trong nhóm `inv_icons`, xem `docs/05` §3.2 |
| `mo_ta_vi` | string | Không | Lời mô tả khi xem trong túi đồ | — |
| `nhat_o_area` | string | **Có** | Khu vực nhặt được | Phải tồn tại |
| `nguon` | string | **Có** | `hs_...` hoặc `puz_...` sinh ra vật phẩm | **Phải trỏ tới hotspot hoặc puzzle có thật** |
| `dung_de` | string | Không | Công dụng, viết cho người đọc | Không cưỡng chế logic — công dụng **máy đọc được** nằm ở `required_item` / `required_items` |

---

# 4. ĐẶC TẢ `data/liveops_chapter_01.json` — CẤU HÌNH VẬN HÀNH

Tài liệu chủ quản là `docs/04_LIVEOPS_MONETIZATION.md`; mục này chỉ đặc tả **hình dạng dữ liệu**.

## 4.1. Cấp gốc

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `schema_version` | integer | **Có** | Phiên bản hợp đồng | `≥ 1` |
| `config_id` | string | **Có** | Mã cấu hình | `^liveops_chapter_[0-9]{2}$` |
| `config_version` | string | **Có** | Phiên bản cấu hình | SemVer. **Tăng mỗi lần đẩy remote config** |
| `chapter_id` | string | **Có** | Chương áp dụng | Phải khớp manifest màn chơi |
| `last_updated_utc` | string | Không | Dấu thời gian | `YYYY-MM-DDThh:mm:ssZ` |
| `server_time_source` | enum | Không | Nguồn giờ chuẩn | `NTP_UTC` \| `SERVER_HEADER` \| `DEVICE_LOCAL` |
| `rollout` | object | **Có** | Trạng thái phát hành + kill-switch | §4.2 |
| `hint_system` | object | **Có** | Hệ gợi ý ba tier | §4.3 |
| `iap` | object | **Có** | Sản phẩm, khôi phục, paywall | §4.4 |
| `seasonal_events` | array | **Có** | Sự kiện theo mùa | §4.5 |
| `gem_economy` | object | **Có** | Nguồn, bồn chứa, cân bằng gem | §4.6 |
| `ad_placements` | array | **Có** | Vị trí quảng cáo | §4.6 |
| `telemetry` | object | **Có** | Sự kiện đo đạc | Tên sự kiện snake_case, ≤ 40 ký tự, ≤ 25 tham số |
| `remote_config_keys` | array | **Có** | Bảng đăng ký khoá remote config | `key` duy nhất, `type` ∈ {string,int,float,bool,json} |
| `ab_tests` | object | **Có** | Khe thử nghiệm A/B | Tổng `allocation_pct` mỗi khe = 100 |
| `player_safety_compliance` | object | **Có** | Ràng buộc an toàn và pháp lý | §4.7 |
| `validation` | object | **Có** | Danh sách bất biến, đọc được cho người | Mỗi dòng ứng với một hàm kiểm trong validator |

## 4.2. `rollout`

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `state` | enum | **Có** | Giai đoạn phát hành | `DRAFT` \| `STAGING` \| `CANARY` \| `LIVE` \| `PAUSED` \| `ROLLED_BACK` |
| `percent` | integer | **Có** | Tỉ lệ người chơi nhận cấu hình | `0 – 100` |
| `min_app_version` | string | **Có** | Bản app tối thiểu | SemVer. Máy cũ hơn bỏ qua cấu hình này |
| `min_addressables_catalog_version` | string | Không | Catalog tối thiểu | `YYYY.MM.DD.N` |
| `kill_switches` | object\<boolean\> | **Có** | Công tắc khẩn cấp | Bắt buộc đủ 5 khoá `kill_switch_*` |

## 4.3. `hint_system` (rút gọn — chi tiết ở `docs/04` §2)

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `hint_cost_gems` | integer | **Có (MF)** | Đơn giá cơ sở một đơn vị gợi ý | `≥ 0`. Giá trị chốt: `5` |
| `ads_reward_hints` | integer | **Có (MF)** | Số đơn vị gợi ý đổi được từ một lượt quảng cáo | `≥ 0`. Giá trị chốt: `1` |
| `free_path_guaranteed` | boolean | **Có** | Bảo đảm luôn có đường miễn phí | **Bắt buộc `true`** — nguyên tắc N1 |
| `max_wait_sec_to_full_solution` | integer | **Có** | Trần thời gian chờ để mở đáp án miễn phí | `≤ 900`. Giá trị chốt: `300` |
| `tiers` | array | **Có** | Đúng 3 tier | `gem_cost` và `unlock_free_after_sec` **phải tăng dần theo tier** |
| `unlock_sources` | array | **Có** | Các đường mở gợi ý | Phải có ≥ 1 nguồn với `gem_cost = 0` **và** `ads_required = 0` |
| `per_puzzle_overrides` | array | Không | Ghi đè theo từng câu đố | `puzzle_id` / `area_id` phải tồn tại trong `data/areas/` |
| `constraints` | object\<boolean\> | **Có** | 5 ràng buộc đạo đức | **Mọi giá trị phải `true`** |

## 4.4. `iap.products[]`

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `iap_product_id` | string | **Có (MF)** | Mã sản phẩm trên store | `^com\.game\.` — **duy nhất** trong mảng |
| `product_type` | enum | **Có** | Loại sản phẩm | `NON_CONSUMABLE` \| `CONSUMABLE`. **Chương 1 cấm `SUBSCRIPTION`** |
| `price_usd` | number | **Có (MF)** | Giá neo USD | `> 0`. Giá hiển thị thật **luôn** lấy từ store |
| `unlock` | object | Không | Nội dung được mở | `{chapter_id, grants_flags[], grants_gems}` |
| `regional_pricing` | array | **Có** | Bảng giá theo vùng | `region_code` duy nhất, **bắt buộc đủ `VN`, `US`, `SEA_DEFAULT`** |

## 4.5. `seasonal_events[]`

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `event_id` | string | **Có** | Mã sự kiện | `^evt_[a-z0-9_]+$` |
| `enabled` | boolean | **Có** | Bật/tắt | — |
| `event_start` | string | **Có (MF)** | Ngày mở | `YYYY-MM-DD`, **phải < `event_end`** |
| `event_end` | string | **Có** | Ngày đóng | `YYYY-MM-DD` |
| `override_bg` | string | **Có (MF)** | Bundle ảnh nền thay thế | `<tên>.bundle`, **phải nằm trong `addressables.bundles`** |
| `applies_to_areas` | array | **Có** | Khu vực áp dụng | Mọi `area_id` phải tồn tại. **Hai sự kiện đang bật không được chồng cửa sổ thời gian trên cùng một khu vực** |
| `theme_override.does_not_change` | array | **Có** | Danh sách bất khả xâm phạm | **Bắt buộc chứa** `hotspot_bounds`, `puzzle_solution`, `jumpscare_trigger_type`, `max_fails` |
| `addressables` | object | **Có** | Bundle và chính sách tải | `download_policy` ∈ `ON_EVENT_ENTER` \| `PREFETCH_ON_WIFI` \| `ON_DEMAND` |
| `fallback` | object | **Có** | Đường lui khi tải hỏng | `never_block_gameplay` **bắt buộc `true`** |

## 4.6. `gem_economy` và `ad_placements`

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `gem_economy.sources[]` | array | **Có** | Nguồn kiếm gem | `source_id` `^src_` duy nhất; `type` ∈ `FREE` \| `AD` \| `IAP` |
| `gem_economy.sinks[]` | array | **Có** | Nơi tiêu gem | `sink_id` `^snk_` duy nhất; `category` ∈ `CONVENIENCE` \| `COSMETIC` \| `BONUS_CONTENT` |
| `gem_economy.balance_targets` | object | **Có** | Mục tiêu cân bằng | **`expected_free_earn_chapter_01` ≥ `expected_spend_p90_player`** |
| `ad_placements[].ad_format` | enum | **Có** | Định dạng quảng cáo | **Chỉ** `REWARDED_VIDEO` \| `REWARDED_INTERSTITIAL`. Cấm banner và interstitial ép xem |
| `ad_placements[].opt_in_only` | boolean | **Có** | Chỉ xem khi tự bấm | **Bắt buộc `true`** |
| `ad_placements[].blocked_windows` | array | **Có** | Cửa sổ cấm quảng cáo | **Bắt buộc chứa** `DURING_JUMPSCARE_ENVELOPE` và `WITHIN_90S_AFTER_ANY_JUMPSCARE` |

## 4.7. `player_safety_compliance`

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `no_loot_box.randomized_paid_rewards` | boolean | **Có** | Có hộp quà ngẫu nhiên không | **Bắt buộc `false`** |
| `price_transparency.two_step_confirm` | boolean | **Có** | Xác nhận hai bước | **Bắt buộc `true`** |
| `accessibility_never_monetized` | object\<boolean\> | **Có** | Tuỳ chọn an toàn/trợ năng | **Mọi giá trị phải `true`** — nguyên tắc N4 |

## 4.8. Ví dụ tối thiểu — sáu khoá Master Form

```json
{
  "schema_version": 1,
  "config_id": "liveops_chapter_01",
  "config_version": "1.0.0",
  "chapter_id": "chapter_01",
  "hint_system": {
    "hint_cost_gems": 5,
    "ads_reward_hints": 1,
    "free_path_guaranteed": true,
    "max_wait_sec_to_full_solution": 300
  },
  "iap": {
    "products": [
      {
        "iap_product_id": "com.game.chapter02",
        "product_type": "NON_CONSUMABLE",
        "price_usd": 1.99,
        "regional_pricing": [
          { "region_code": "VN",          "currency": "VND", "price_local": 49000 },
          { "region_code": "US",          "currency": "USD", "price_local": 1.99  },
          { "region_code": "SEA_DEFAULT", "currency": "USD", "price_local": 1.79  }
        ]
      }
    ]
  },
  "seasonal_events": [
    {
      "event_id": "evt_halloween_2026",
      "enabled": true,
      "event_start": "2026-10-25",
      "event_end": "2026-11-03",
      "override_bg": "bg_halloween.bundle",
      "applies_to_areas": ["area_san_gach", "area_hien_nha"],
      "addressables": {
        "bundles": ["bg_halloween.bundle"],
        "download_policy": "ON_EVENT_ENTER"
      },
      "fallback": {
        "on_download_fail": "USE_BASE_BACKGROUND",
        "never_block_gameplay": true
      }
    }
  ]
}
```

---

# 5. BẤT BIẾN LIÊN FILE — PHẦN JSON SCHEMA KHÔNG LÀM ĐƯỢC

JSON Schema chỉ nhìn được **một file tại một thời điểm**. Bảy nhóm ràng buộc dưới đây bắt buộc phải do `tools/validate_level.py` cưỡng chế.

## 5.1. Bảng tổng hợp

| # | Bất biến | Mức | Giai đoạn trong validator |
|---|---|---|---|
| B1 | Mọi `id` (`area_` / `item_` / `hs_` / `puz_` / `scare_`) **duy nhất toàn chương** | **[LỖI]** | 6 |
| B2 | `target_puzzle_id` và `wrong_action_jumpscare` trỏ vào đối tượng **trong cùng file khu vực** | **[LỖI]** | 7b |
| B3 | `target_area_id` trỏ tới khu vực có trong manifest | **[LỖI]** | 7b |
| B4 | `item_id` / `required_item` / `reward_item_id` đều có trong `item_catalog` | **[LỖI]** | 7b |
| B5 | Không hotspot nào chồng lấn hotspot khác **trong cùng khu vực** | **[LỖI]** | 5 |
| B6 | Đồ thị phụ thuộc vật phẩm **không có chu trình** | **[LỖI]** | 8 |
| B7 | Vật phẩm nhặt được mà **không nơi nào dùng tới** | **[CẢNH BÁO]** | 9 |
| B8 | **Khả giải**: tới được mọi khu vực, giải được mọi câu đố, cầm được mọi vật phẩm, tới được khu vực kết chương | **[LỖI]** | 10 |
| B9 | Mọi cờ trong `required_flags` đều có nguồn cấp | **[LỖI]** | 7a |
| B10 | 16 bất biến LiveOps trong `validation.invariants` | **[LỖI]** | 11 |

## 5.2. B5 — định nghĩa chồng lấn

Hai hình chữ nhật A và B chồng lấn khi **và chỉ khi** cả bốn bất đẳng thức sau đều đúng:

```
A.x < B.x + B.width      B.x < A.x + A.width
A.y < B.y + B.height     B.y < A.y + A.height
```

Chạm **mép** không tính là chồng lấn: hotspot kết thúc ở `x = 640` và hotspot bắt đầu ở `x = 640` là hợp lệ. Đây là lý do `hs_khe_mong_cua_gac` (y: 120…230) đặt ngay trên `hs_cau_thang_gac` (y: 250…580) mà vẫn qua được kiểm tra.

## 5.3. B9 — ba mức xác định nguồn cấp cờ tiến trình

`unlock_condition.required_flags` là cách manifest diễn đạt "cửa này mở khi việc kia đã làm xong". Nhưng **hợp đồng khu vực không có trường nào nói cờ được bật ở đâu** — nên validator phải truy nguồn theo ba mức ưu tiên:

| Mức | Cách xác định | Kết quả |
|---|---|---|
| 1. **Tường minh** | Một hotspot hoặc puzzle khai báo `"grants_flag": "<cờ>"` | Chấp nhận, không cảnh báo |
| 2. **Quy ước** | Tên cờ khớp mẫu `flag_<puzzle_id>_solved` và câu đố đó có thật | Chấp nhận, không cảnh báo |
| 3. **Suy luận** | Đối chiếu từ khoá giữa tên cờ và `id` các hotspot `USE_ITEM` trong khu vực nguồn (`from_area_id`). Chỉ nhận khi **duy nhất một** ứng viên thắng | Chấp nhận **kèm [CẢNH BÁO]** |
| — | Không ứng viên nào, hoặc nhiều ứng viên ngang điểm | **[LỖI]** |

**Ví dụ mức 3 trong Chương 1:** cờ `flag_binh_phong_da_tra` không có nguồn tường minh. Khu vực nguồn là `area_hien_nha`; hotspot `USE_ITEM` duy nhất ở đó là `hs_o_lom_binh_phong`, chia sẻ hai từ khoá `binh` và `phong`. Validator gán tạm và phát cảnh báo.

> **Khuyến nghị dứt khoát:** thêm `grants_flag` vào cả ba hotspot `USE_ITEM` mở đường (`hs_o_lom_binh_phong` → `flag_binh_phong_da_tra`, `hs_khe_mong_cua_gac` → `flag_then_gac_da_tra`). Suy luận theo tên là chỗ dựa tạm; đổi tên hotspot một lần là logic mở khoá gãy mà không ai biết.

## 5.4. B7 — vì sao vật phẩm công cụ hay bị báo "chết"

Validator coi một vật phẩm là **được dùng tới** khi nó xuất hiện ở ít nhất một trong ba chỗ **máy đọc được**:

1. `hotspots[].required_item`
2. `puzzles[].required_items`
3. `unlock_condition.required_items`

Trường `dung_de` trong `item_catalog` là văn xuôi cho người đọc, **không** tính. Vì vậy bốn vật phẩm công cụ — `item_giay_ban_va_than`, `item_dui_mo`, `item_den_dau`, `item_dai_vai_dieu`, `item_chai_dau_hoa` — sẽ bị báo **[CẢNH BÁO]** cho tới khi công dụng của chúng được mã hoá thành `required_items` trên đúng câu đố:

| Vật phẩm | Thuộc `required_items` của |
|---|---|
| `item_giay_ban_va_than` | `puz_rap_chu_the_menh` |
| `item_dui_mo` | `puz_ba_hoi_chin_tieng` |
| `item_den_dau`, `item_dai_vai_dieu`, `item_chai_dau_hoa` | `puz_thap_lai_den_dau` |

Khai báo đủ ba dòng này đem lại hai thứ cùng lúc: cảnh báo vật phẩm chết biến mất, **và** phép chứng minh khả giải ở giai đoạn 10 trở nên chặt thật sự — vì lúc đó nó mới kiểm được rằng người chơi đã cầm dùi mõ *trước khi* đứng trước cái mõ.

## 5.5. B8 — thuật toán chứng minh khả giải

Validator không đi theo kịch bản viết sẵn. Nó mô phỏng người chơi bằng **thuật toán điểm bất động** (least fixed point):

```
Trạng thái = (khu vực đã tới, túi đồ, câu đố đã giải, cờ đã bật)
Khởi tạo   = ({start_area_id}, ∅, ∅, ∅)

Lặp:
    Với mỗi khu vực ĐÃ tới:
        Với mỗi hotspot trong đó:
            COLLECT_ITEM  → nếu required_item là null hoặc đã có  ⇒ nhặt item_id
            USE_ITEM      → nếu required_item đã có               ⇒ bật grants_flag, trao item_id
            ZOOM_PUZZLE   → nếu đủ required_items                 ⇒ giải, bật cờ, nhận thưởng
            CHANGE_AREA   → nếu unlock_condition thoả             ⇒ tới khu vực đó
    Cho tới khi một vòng KHÔNG làm trạng thái thay đổi nữa.
```

Điểm dừng chính là **mọi thứ người chơi có thể với tới**. Sau đó validator đối chiếu với mục tiêu và báo **[LỖI]** kèm chẩn đoán cụ thể (*thiếu vật phẩm nào*, *thiếu cờ nào*) cho từng mục không đạt. Chạy với `--trace` sẽ in ra nhật ký mô phỏng — đúng thứ tự game mở ra cho người chơi, dùng được luôn làm kịch bản QA.

---

# 6. QUY ƯỚC ĐỊNH DANH

## 6.1. Tiền tố bắt buộc

| Tiền tố | Loại | Nơi khai báo **duy nhất** | Ví dụ |
|---|---|---|---|
| `area_` | Khu vực | `chapter_01.json` → `areas[]` | `area_gian_tho` |
| `item_` | Vật phẩm | `chapter_01.json` → `item_catalog[]` | `item_bai_vi_khuyet_danh` |
| `hs_` | Hotspot | `areas/<area>.json` → `hotspots[]` | `hs_khe_mong_cua_gac` |
| `puz_` | Câu đố | `areas/<area>.json` → `puzzles[]` | `puz_ba_hoi_chin_tieng` |
| `scare_` | Cú doạ | `areas/<area>.json` → `jumpscares[]` | `scare_khoi_tu_hinh_nguoi` |
| `flag_` | Cờ tiến trình | `grants_flag` (nên khai báo tường minh) | `flag_then_gac_da_tra` |
| `txt_` | Khoá localization | File localization | `txt_examine_van_khan` |
| `anim_` | Hoạt ảnh | Addressables | `anim_khoi_tu_dang_nguoi` |

Mọi `id` chỉ dùng `[a-z0-9_]`: **không dấu tiếng Việt, không chữ hoa, không gạch ngang, không khoảng trắng**. Dấu tiếng Việt chỉ xuất hiện trong `ten_vi`, `mo_ta_vi`, `ghi_chu_vi` và trong file localization.

## 6.2. Quy ước `text_key`

| Mẫu | Dùng cho | Ví dụ |
|---|---|---|
| `txt_examine_<đối tượng>` | Hotspot `EXAMINE` | `txt_examine_bat_huong` |
| `txt_thoai_<đối tượng>` | Hotspot `DIALOGUE` | `txt_thoai_vach_buong` |
| `txt_khoa_<cửa>` | `locked_text_key` | `txt_khoa_cau_thang_gac` |
| `txt_hint_<puzzle_id>_t<n>` | Gợi ý tier n | `txt_hint_puz_khoa_bat_quai_t2` |
| `txt_liveops_<tình huống>` | Thông báo vận hành | `txt_liveops_het_luot_xem_ads` |

---

# 7. CHẠY TRÌNH KIỂM CHỨNG

```bash
# Kiểm toàn bộ (mặc định thư mục data)
python3 tools/validate_level.py

# Chỉ định thư mục data khác
python3 tools/validate_level.py /home/user/HackTheBox/LinhAnThon/data

# Chỉ kiểm cấu hình LiveOps
python3 tools/validate_level.py --liveops data/liveops_chapter_01.json

# Cổng CI trước khi khoá bản: cảnh báo cũng tính là lỗi
python3 tools/validate_level.py --strict

# In nhật ký mô phỏng người chơi (dùng làm kịch bản QA)
python3 tools/validate_level.py --trace
```

| Tham số | Ý nghĩa |
|---|---|
| `data_dir` (vị trí) | Thư mục dữ liệu. Mặc định `/home/user/HackTheBox/LinhAnThon/data` |
| `-m`, `--manifest` | Đường dẫn manifest khác mặc định |
| `--liveops` | Đường dẫn file cấu hình LiveOps |
| `--skip-liveops` | Bỏ qua giai đoạn 11 |
| `--strict` | Coi `[CẢNH BÁO]` là lỗi |
| `--trace` | In nhật ký mô phỏng người chơi |
| `--no-color` | Tắt màu ANSI (tự tắt khi không xuất ra terminal) |
| `--quiet` | Chỉ in các mục có `[LỖI]` hoặc `[CẢNH BÁO]` |

**Mã thoát:** `0` = sạch (có thể còn cảnh báo) · `1` = có ít nhất một `[LỖI]`, hoặc có cảnh báo khi chạy `--strict`.

| Nhãn | Nghĩa | Hệ quả |
|---|---|---|
| `[LỖI]` | Vi phạm hợp đồng. Dữ liệu **sẽ** làm hỏng game | Chặn build, mã thoát 1 |
| `[CẢNH BÁO]` | Hợp lệ nhưng đáng ngờ, hoặc validator phải suy luận | Không chặn build, trừ khi `--strict` |
| `[OK]` | Một lớp kiểm tra đã qua sạch | — |
| `[i]` | Thông tin ngữ cảnh | — |

> **Cổng CI đề xuất:** chạy `--strict` trên nhánh `main`, chạy thường trên nhánh tính năng. Nhờ vậy tổ thiết kế thử nghiệm thoải mái, nhưng không bản nào được khoá khi còn một cờ tiến trình phải đoán hay một vật phẩm chết.
