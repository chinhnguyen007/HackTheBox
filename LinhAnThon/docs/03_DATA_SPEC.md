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
| `background_asset_url` | string | **Có (MF)** | **Khoá logic** trỏ tới bộ nền của khu vực. Đọc §2.1.1 trước khi dùng | HTTPS tuyệt đối, đuôi `.bundle`, `basename` phải bằng `"bg_" + area_id` đã bỏ tiền tố `area_`. **Cấm** nhúng ảnh thô vào APK engine |
| `ambience_address` | string \| null | Không ★ *(đề nghị bổ sung schema)* | Khoá Addressables của bundle tiếng nền khu vực | `^remote_ambience_[a-z0-9_]+$` hoặc `null`. §2.1.2 |
| `hotspots` | array\<Hotspot\> | **Có** | Toàn bộ vùng chạm của màn hình | **Không được rỗng** — khu vực không có hotspot là ngõ cụt |
| `puzzles` | array\<Puzzle\> | **Có** | Các câu đố thuộc khu vực | Được phép rỗng `[]` |
| `jumpscares` | array\<Jumpscare\> | **Có** | Các cú doạ thuộc khu vực | Được phép rỗng `[]` |

`[[ Bốn khu vực có câu đố; area_gian_tho có hai (puz_tuan_tu_le_cung và puz_ba_hoi_chin_tieng). ]]`

### 2.1.1. `background_asset_url` là KHOÁ LOGIC, không phải địa chỉ mạng

`background_asset_url` là **khoá bắt buộc của Master Form** — cấm đổi tên, cấm bỏ. Nhưng giá trị của nó là một URL **phẳng**, không có nền tảng và không có phiên bản catalog:

```
"background_asset_url": "https://cdn.linhanthon.game/assets/bg_gian_tho.bundle"
```

trong khi quy ước đường dẫn CDN thật (`docs/05` §5.2) là:

```
https://cdn.linhanthon.game/assets/{android|ios}/{catalog_version}/...
```

Hai thứ đó không khớp nhau. **Luật hoà giải, áp cho cả engine lẫn validator:**

> **Engine KHÔNG BAO GIỜ gọi HTTP bằng chuỗi này.** Engine lấy `basename` không đuôi làm **Addressables key**, rồi để `Addressables.ResourceManager.InternalIdTransformFunc` ghép `{platform}` và `{catalog_version}` lúc chạy (`docs/05` §5.2.1).

| Bước | Ví dụ |
|---|---|
| Giá trị trong dữ liệu | `"https://cdn.linhanthon.game/assets/bg_gian_tho.bundle"` |
| Khoá Addressables engine rút ra | `bg_gian_tho` |
| Đường dẫn thật lúc chạy | `https://cdn.linhanthon.game/assets/android/2026.09.15.1/remote_area_gian_tho_assets_<hash>.bundle` |

| Validator kiểm gì | Mức |
|---|---|
| Chuỗi khớp `^https://.+/bg_[a-z0-9_]+\.bundle$` | **[LỖI]** |
| `basename` bằng đúng `"bg_" + area_id[len("area_"):]` — vd `area_gian_tho` ⇒ `bg_gian_tho` | **[LỖI]** |
| Validator **không** gọi mạng, **không** kiểm URL với tới được | — |

**Vì sao luật này quan trọng hơn vẻ ngoài của nó:** cơ chế quay lui ở `docs/05` §6.4 hoạt động bằng cách trỏ `addressables_catalog_url` về thư mục phiên bản trước. Nếu engine dùng chuỗi URL phẳng làm địa chỉ thật thì catalog lùi về bản cũ **mà ảnh nền vẫn là ảnh mới** — quay lui gãy im lặng, và không ai phát hiện cho tới khi người chơi báo lỗi hiển thị.

`[[ Cùng luật này áp cho seasonal_events[].override_bg (muc 4.5) va item_catalog[].icon_asset (muc 3.4): moi chuoi ".bundle" / ".png" trong du lieu deu la khoa logic. Mot cau: du lieu noi DIEU GI, catalog noi O DAU. ]]`

### 2.1.2. `ambience_address` — đề nghị bổ sung schema

**Trạng thái:** trường này **chưa có** trong `schema/level.schema.json`. Mục này là **đề nghị bổ sung**, không phải mô tả hiện trạng. Cho tới khi schema được cập nhật, `additionalProperties: false` sẽ từ chối nó — nên **phải sửa schema trước, dữ liệu sau**.

| Mục | Nội dung |
|---|---|
| **Kiểu** | `string \| null` |
| **Bắt buộc** | Không ★ — thiếu thì validator phát **[CẢNH BÁO]** và engine phải suy ra tên bằng quy ước chuỗi `"remote_ambience_" + area_id` |
| **Ý nghĩa** | Khoá Addressables của bundle chứa tiếng nền, độc thoại nội tâm và vox của **đúng khu vực này**. Bundle ấy được **tải trọn về cache rồi phát Streaming từ đĩa** — xem `docs/05` §1.6.6 |
| **Ràng buộc** | Khớp `^remote_ambience_[a-z0-9_]+$`. Nếu khác `null` thì phần sau tiền tố **phải bằng** `area_id`. Giá trị `null` nghĩa là *khu vực này cố ý không có tiếng nền*, khác hẳn với việc **không khai báo trường** (= quên) |
| **Ví dụ** | `"ambience_address": "remote_ambience_gian_tho"` |

**Vì sao cần một trường thay vì để engine tự ghép chuỗi:** ghép chuỗi trong mã là một phụ thuộc ẩn. Đổi tên nhóm Addressables một lần là toàn bộ tiếng nền im lặng, mà không cổng CI nào bắt được — vì không có trường nào để đối chiếu. Có trường thì validator kiểm được, và `docs/05` §8.2 có một dòng checklist kiểm được.

`[[ Tieng nen hong thi im lang bo qua (docs/05 muc 7.3 quy tac 1) — no la noi dung TUY CHON. Chinh vi the loi thieu no khong bao gio tu lo ra luc chay; phai bat bang validator. ]]`

## 2.2. Kiểu `Bounds` — hình chữ nhật vùng chạm

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `x` | integer | **Có** | Mép trái, pixel thiết kế | `0 ≤ x ≤ 1919` |
| `y` | integer | **Có** | Mép **trên** (y tăng xuống dưới) | `0 ≤ y ≤ 1079` |
| `width` | integer | **Có** | Chiều rộng | `> 0`, và `x + width ≤ 1920` |
| `height` | integer | **Có** | Chiều cao | `> 0`, và `y + height ≤ 1080` |

**Năm mức kiểm tra hình học:**

| # | Điều kiện | Mức | Lý do |
|---|---|---|---|
| G1 | `width ≤ 0` hoặc `height ≤ 0` | **[LỖI]** | Vùng chạm suy biến, người chơi không bao giờ bấm trúng |
| G2 | `x + width > 1920` hoặc `y + height > 1080` | **[LỖI]** | Tràn ra ngoài khung thiết kế; trên máy tỉ lệ khác sẽ bị cắt mất |
| G3 | `width < 88` hoặc `height < 88` | **[LỖI]** | Sàn chạm tuyệt đối của `01_KICH_BAN_CHAPTER_01.md` §6: **88 × 88 px @1920, không ngoại lệ**. *(Trước đây mức này là [CẢNH BÁO]; nâng lên [LỖI] vì không dữ liệu nào của Chương 1 vi phạm — nhỏ nhất hiện là 120 × 120 — nên không có gì để phá.)* |
| G4 | `88 ≤ min(width, height) < 120` **và KHÔNG** khai `visual_bounds` | **[CẢNH BÁO]** | Hai khả năng, cả hai đều phải sửa: hoặc quên **nới** vùng chạm cho đồ vật nhỏ, hoặc đã nới nhưng quên **khai** `visual_bounds`. Xem §2.3.4 |
| G5 | `88 ≤ min(width, height) < 120` **và CÓ** khai `visual_bounds` | **Chấp nhận** | Khai `visual_bounds` là cách nói với trình kiểm *"nhỏ ở đây là có chủ đích, không phải bỏ sót"* (nguyên văn mô tả trong `schema/level.schema.json`). **Nhưng sàn thiết kế vẫn là 120 × 120** — đừng dùng ngoại lệ này trừ khi bất khả kháng |

**Sàn thiết kế của vùng chạm là 120 × 120, không phải 88 × 88.** 88 là ngưỡng *"bấm được"*; 120 là ngưỡng *"bấm trúng ngay lần đầu, một tay, trên máy 5 inch, trong bóng tối"* — đúng tư thế chơi mà game này nhắm tới. Toàn bộ dữ liệu Chương 1 hiện đạt sàn 120: nhỏ nhất là `hs_dui_mo` với `120 × 120`. Giữ nguyên trạng đó.

> **`bounds` là VÙNG CHẠM, không phải vùng vẽ.** Đây là phân biệt quan trọng nhất của mục §2. `bounds` nói *"chạm vào đây thì có chuyện xảy ra"*; **`visual_bounds`** (§2.3.4) nói *"pixel của đồ vật nằm ở đây"*. Với đồ vật nhỏ — gáo dừa, gương bát quái, dùi mõ — hai hình chữ nhật đó **cố ý khác nhau**, và `bounds` **luôn** là hình lớn hơn.

> **Vì sao gốc toạ độ ở góc trên-trái mà Unity thì không?** Unity dùng gốc dưới-trái. Tổ engine chịu trách nhiệm lật trục **một lần duy nhất** ở lớp nạp dữ liệu: `unity_y = 1080 - (y + height)`. Tổ thiết kế **luôn** làm việc theo hệ trên-trái vì mọi phần mềm dựng bố cục (Figma, Photoshop, Krita) đều dùng hệ này. Đừng lật trục trong file dữ liệu.

## 2.3. Kiểu `Hotspot`

### 2.3.1. Bảng trường

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `id` | string | **Có** | Mã vùng chạm | `^hs_[a-z0-9_]+$`, **duy nhất toàn chương** |
| `bounds` | Bounds | **Có (MF)** | **Vùng chạm** — vị trí và kích thước của vùng người chơi bấm được | §2.2. **Không được chồng lấn** `bounds` của hotspot khác trong cùng khu vực |
| `visual_bounds` | Bounds \| null | Không ★ | **Vùng vẽ thật** của sprite bên trong `bounds` | Phải **nằm trọn** trong `bounds`. Bắt buộc khai khi sprite nhỏ hơn `bounds`. §2.3.4 |
| `action_type` | enum | **Có** | Việc xảy ra khi bấm | `ZOOM_PUZZLE` \| `COLLECT_ITEM` \| `EXAMINE` \| `USE_ITEM` \| `CHANGE_AREA` \| `DIALOGUE` |
| `target_puzzle_id` | string \| null | **Có ¹** | Câu đố sẽ mở | `^puz_...$`. Phải tồn tại **trong chính file này** |
| `target_area_id` | string | **Có ¹** | Khu vực sẽ đi tới | `^area_...$`. Phải có trong manifest. **Chỉ** `CHANGE_AREA` được mang trường này |
| `item_id` | string | **Có ¹** | Vật phẩm được trao (`COLLECT_ITEM`) hoặc được đặt vào (`USE_ITEM`) | `^item_...$`. Phải có trong `item_catalog` |
| `required_item` | string \| null | **Có ¹** | Vật phẩm phải có sẵn trong túi đồ | `^item_...$` hoặc `null`. Phải có trong `item_catalog` |
| `text_key` | string | **Có ¹** | Khoá localization của lời kể | `^txt_[a-z0-9_]+$`. **Cấm** nhúng chuỗi tiếng Việt vào file dữ liệu |
| `grants_flag` | string \| null | Không ★ | Cờ tiến trình bật lên sau khi hotspot chạy xong | `^flag_[a-z0-9_]+$`. Xem §5.3 — thiếu trường này thì validator phải suy luận |
| `required_flags` | array\<string\> | Không | Các cờ phải bật trước thì hotspot mới hoạt động | Mặc định `[]`. Mọi cờ phải có nguồn cấp. §2.7 |
| `fallback_text_key` | string \| null | Không ★ | Lời kể hiện ra khi hotspot **bị chặn** — thiếu vật phẩm hoặc thiếu cờ | `^txt_[a-z0-9_]+$` hoặc `null`. Khác `text_key`. §2.7 |
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

### 2.3.4. Vùng chạm mở rộng — `bounds` so với `visual_bounds`

`01_KICH_BAN_CHAPTER_01.md` §6 đặt một cơ chế **bắt buộc**: *"Kích thước chạm tối thiểu 88 × 88 px @1920 cho mọi hotspot, không ngoại lệ. Sprite nhỏ hơn thì dùng **vùng chạm mở rộng**."* Cơ chế ấy có thật trong kịch bản — `hs_guong_bat_quai` có sprite thật **96 × 96** nằm trong vùng chạm **130 × 130**, `hs_gao_dua` có sprite **86 × 62** trong vùng chạm **130 × 120** — nhưng **hợp đồng dữ liệu không có trường nào để khai nó**. Kết quả: thông tin ấy chỉ sống trong văn xuôi của `docs/01`, không cổng CI nào kiểm được, và tổ đồ hoạ không có gì để đối chiếu.

**`visual_bounds` là trường khai cơ chế đó.**

#### 2.3.4.1. Đặc tả trường

| Mục | Nội dung |
|---|---|
| **Kiểu** | `Bounds` (§2.2) hoặc `null` |
| **Bắt buộc** | Không ★. **Bắt buộc trên thực tế** khi sprite nhỏ hơn `bounds` theo bất kỳ chiều nào quá **24 px** — xem §2.3.4.3 |
| **Ý nghĩa** | Hình chữ nhật **pixel thật của đồ vật** trên lớp nền `_l1_mid`. `bounds` là nơi ngón tay chạm; `visual_bounds` là nơi mắt nhìn |
| **Ràng buộc** | `visual_bounds` phải **nằm trọn** trong `bounds`: `vb.x ≥ b.x` **và** `vb.y ≥ b.y` **và** `vb.x + vb.width ≤ b.x + b.width` **và** `vb.y + vb.height ≤ b.y + b.height`. Cho phép trùng khít bốn cạnh |
| **Không ràng buộc** | `visual_bounds` **không** bị luật chồng lấn B5 — hai đồ vật vẽ gần nhau là chuyện bình thường, miễn hai **vùng chạm** không giao nhau |
| **Mặc định** | Không khai ⇒ engine coi `visual_bounds = bounds` |

#### 2.3.4.2. Ví dụ — lấy nguyên văn từ `data/areas/`

```json
{
  "id": "hs_dui_mo",
  "bounds":        { "x": 555, "y": 780, "width": 120, "height": 120 },
  "visual_bounds": { "x": 560, "y": 780, "width": 110, "height": 120 },
  "action_type": "COLLECT_ITEM",
  "item_id": "item_dui_mo",
  "required_item": null,
  "one_shot": true
}
```

Đọc là: dùi mõ được vẽ rộng **110 px**, nhưng vùng chạm nới ra **120 px** và lệch sang trái 5 px để đạt sàn 120 × 120 của G5. Người chơi bấm hụt 5 px về bên trái vẫn nhặt được dùi.

```json
{
  "id": "hs_chieu_coi_trai_san",
  "bounds":        { "x": 730, "y": 901, "width": 440, "height": 120 },
  "visual_bounds": { "x": 730, "y": 910, "width": 440, "height":  88 },
  "action_type": "EXAMINE"
}
```

Đọc là: chiếu cói chỉ cao **88 px** (dải `y ∈ [910, 998]`), nhưng vùng chạm cao **120 px** (`y ∈ [901, 1021]`) — nới đều 9 px lên trên và 23 px xuống dưới.

#### 2.3.4.3. Validator kiểm gì

| # | Kiểm | Mức |
|---|---|---|
| V1 | `visual_bounds` thoả G1 và G2 của §2.2 (không suy biến, không tràn khung 1920×1080) | **[LỖI]** |
| V2 | `visual_bounds` **nằm trọn** trong `bounds` theo bốn bất đẳng thức ở §2.3.4.1 | **[LỖI]** |
| V3 | Có `visual_bounds` mà `bounds` nhỏ hơn 120 × 120 (mức G5) | **[LỖI]** |
| V4 | `visual_bounds` **lớn hơn hoặc bằng** `bounds` cả bốn cạnh (tức khai mà không mở rộng gì) | **[CẢNH BÁO]** — bỏ trường đi cho gọn |
| V5 | `bounds` lớn hơn `visual_bounds` quá **24 px** ở bất kỳ chiều nào mà **không** khai `visual_bounds` | **Không kiểm được từ dữ liệu.** Đây là lý do V6 tồn tại |
| V6 | `bounds` nhỏ hơn 120 × 120 (mức G4) **và** không có `visual_bounds` | **[CẢNH BÁO]** — hoặc đồ vật thật sự nhỏ (cần mở rộng và khai `visual_bounds`), hoặc đang thiếu khai báo |
| V7 | Với hotspot `COLLECT_ITEM` / `USE_ITEM` có `visual_bounds`: tâm `visual_bounds` phải nằm trong `bounds` | **[LỖI]** — nếu không thì hiệu ứng nhặt vật bay ra ngoài vùng chạm |

**Luật chồng lấn B5 (§5.2) vẫn chỉ áp cho `bounds`, không áp cho `visual_bounds`.** Nới vùng chạm ra mà đụng vùng chạm hàng xóm là **[LỖI]** — đó chính là điều kiện giữ cho việc mở rộng không biến thành việc ăn cắp vùng chạm của đồ vật bên cạnh. Ba cặp nguy hiểm nhất, đã ghi trong `02_PROMPT_DO_HOA.md` §6.5: `hs_binh_phong` ↔ `hs_o_lom_binh_phong`, `hs_mo_ca` ↔ `hs_dui_mo`, `hs_hinh_nhan` ↔ `hs_chieu_coi_trai_san`.

#### 2.3.4.4. Checklist đồ hoạ kiểm gì — và luật hoà giải với ràng buộc "sai số ≤ 24px"

`02_PROMPT_DO_HOA.md` §6.5 có một dòng: *"Mỗi đồ vật tương tác được nằm **đúng vùng bounds** của hotspot tương ứng, sai số ≤ 24px."*

**Dòng đó mâu thuẫn trực tiếp với cơ chế vùng chạm mở rộng** — `hs_guong_bat_quai` có sprite 96 × 96 trong `bounds` 130 × 130, tức lệch **34 px**, vượt dung sai 24 px, dù nó **đúng** theo thiết kế. Nếu QA đồ hoạ soát theo dòng đó, họ sẽ báo lỗi cho những hotspot làm đúng nhất.

> **LUẬT HOÀ GIẢI (bắt buộc, thay cho cách đọc cũ):** dung sai **≤ 24 px** áp cho cặp **`visual_bounds` ↔ pixel vẽ thật**, **không** áp cho cặp `bounds` ↔ pixel vẽ thật. Quan hệ giữa `bounds` và `visual_bounds` không phải là dung sai — nó là **chủ ý thiết kế**, và ràng buộc duy nhất của nó là "nằm trọn bên trong" (V2).

Bảng soát cho tổ đồ hoạ, thay cho một dòng cũ:

| # | Kiểm trên file PSD/PNG lớp `_l1_mid` | Dung sai | Hỏng thì sao |
|---|---|---|---|
| A1 | Bounding box **alpha khác 0** của đồ vật khớp `visual_bounds` | **≤ 24 px** mỗi cạnh | Đồ vật vẽ lệch khỏi chỗ dữ liệu nói nó đứng |
| A2 | Toàn bộ pixel của đồ vật nằm **trong** `bounds` | **0 px** — không được tràn | Người chơi thấy một phần đồ vật mà bấm vào không ăn |
| A3 | Với hotspot **không** khai `visual_bounds`: bounding box alpha khớp `bounds` | **≤ 24 px** | Hoặc thiếu khai `visual_bounds`, hoặc vẽ sai chỗ |
| A4 | Khoảng trống giữa `visual_bounds` và mép `bounds` **không** chứa pixel của đồ vật **khác** | **0 px** | Hai đồ vật dính nhau, người chơi bấm nhầm |
| A5 | Hotspot hiện sau khi giải câu đố (`hs_bai_vi_khuyet_danh`, `hs_dai_vai_dieu`, `hs_ao_cuoi_giay`) nằm ở **lớp bật/tắt riêng**, không nung vào nền | — | Người chơi thấy vật trước khi được phép nhặt |
| A6 | Không đồ vật quan trọng nào nằm trong dải `y < 80` (notch) hoặc `y > 1000` (thanh túi đồ) — kiểm trên **`visual_bounds`**, vì `bounds` được phép thò xuống dưới 1000 khi nới | — | Bị notch hoặc thanh túi đồ che |

`[[ Muc A6 la vi du ro nhat cua vi sao phai tach hai truong: hs_chieu_coi_trai_san co bounds cham toi y = 1021, tuc tho vao dai thanh tui do, nhung visual_bounds dung o y = 998. Do la HOP LE — vung cham duoc phep nam duoi tay nguoi choi, mien la PIXEL cua do vat thi khong. ]]`

## 2.4. Kiểu `Puzzle`

### 2.4.1. Bảng trường

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Ràng buộc |
|---|---|---|---|---|
| `id` | string | **Có** | Mã câu đố | `^puz_[a-z0-9_]+$`, duy nhất toàn chương |
| `type` | enum | **Có** | Thể loại cơ chế | `ROTATION_LOCK` \| `SEQUENCE_ORDER` \| `SLIDING_TILE` \| `ITEM_COMBINE` \| `PATTERN_TRACE` \| `AUDIO_MATCH` |
| `solution` | array\<integer\> | **Có** | Lời giải đúng | Không rỗng, ≤ 16 phần tử. Ngữ nghĩa theo `type` — §2.4.3 |
| `reward_item_id` | string \| null | **Có** | Vật phẩm trao khi giải đúng | `^item_...$` hoặc `null`. Phải có trong `item_catalog` |
| `wrong_action_jumpscare` | string \| null | **Có** | Cú doạ bắn khi giải sai | `^scare_...$` hoặc `null`. Phải tồn tại **trong chính file này** |
| `required_items` | array\<string\> | Không ★ | Vật phẩm **công cụ** phải có thì mới nhập được lời giải. **Không** bị tiêu thụ | Mặc định `[]`. Mọi phần tử phải có trong `item_catalog`. §2.7.5, §5.4 |
| `grants_flag` | string \| null | Không | Cờ **PHỤ** bật khi giải đúng — **ngoài** cờ chính tắc | Cờ chính tắc `flag_<id>_solved` **luôn** bật, có khai hay không. §2.7.6 |
| `ten_vi`, `ghi_chu_vi` | string | Không | Nhãn và ghi chú nội bộ | `ten_vi` ≤ 120 ký tự, `ghi_chu_vi` ≤ 500 |

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
| `delay_sec` | number | **Có ¹** với `ON_TIMER`, Không ★ với trigger khác | Độ trễ từ lúc điều kiện kích hoạt được thoả tới lúc cú doạ thật sự bắn | `0 ≤ v ≤ 600`. Thiếu trên `ON_TIMER` → **[LỖI]**. §2.7 |
| `trigger_item_id` | string | **Có ¹** với `ON_COLLECT_ITEM`, Không với `ON_WRONG_ITEM_USE` | Vật phẩm gắn với cú doạ | `^item_...$`, phải có trong `item_catalog`. **Cấm** với mọi `trigger_type` khác. §2.7 |
| `audio_asset` | string | **Có (MF)** | File âm thanh | `<tên>.ogg` / `.mp3` / `.wav`. Chương 1 dùng **`.ogg`**; đó là **tên asset nguồn**, thiết lập import quyết định định dạng lúc chạy (`sfx_scare_*` bắt buộc import thành **ADPCM**) — xem `docs/05` **§3.3**, không phải §4.3 |
| `sprite_animation` | string | **Có** | Hoạt ảnh sprite | `^anim_[a-z0-9_]+$` |
| `screen_flash` | boolean | **Có** | Có loé trắng màn hình không | `true` / `false`. **Phải khai báo tường minh** |
| `cooldown_sec` | number | Không ★ | Thời gian nghỉ tối thiểu trước khi bắn lại | `0 ≤ v ≤ 3600`. Quy ước chương: **90**. §2.7 |
| `cooldown_exempt` | boolean | Không | Khai báo **có chủ đích** rằng cú doạ này không có `cooldown_sec` | Mặc định `false`. Đặt `true` thì trình kiểm thôi nhắc — và **bắt buộc** kèm `ghi_chu_vi` nêu căn cứ miễn trừ. §2.7 |
| `ten_vi`, `ghi_chu_vi` | string | Không | Nhãn và ghi chú sản xuất | `ten_vi` ≤ 120 ký tự, `ghi_chu_vi` ≤ 500. Không hiển thị trong game. **Bắt buộc** khi cú doạ được miễn trừ một quy ước (vd bỏ `cooldown_sec`) — ghi rõ miễn trừ theo điều nào |

### 2.5.2. Ma trận bắt buộc theo `trigger_type`

| `trigger_type` | Bắt buộc có | Cấm có | `delay_sec` nghĩa là gì | Bắn khi |
|---|---|---|---|---|
| `ON_PUZZLE_FAIL_COUNT` | `max_fails` | `trigger_item_id` | Hợp lệ nhưng **không dùng ở Chương 1** — thời điểm bắn đã do lần giải sai thứ `max_fails` quyết định, thêm độ trễ chỉ làm mờ quan hệ nhân quả người chơi cần thấy | Giải sai đủ `max_fails` lần liên tiếp |
| `ON_ENTER_AREA` | — | `max_fails`, `trigger_item_id` | Số giây **sau khi fade-in xong** | Lần đầu bước vào khu vực |
| `ON_COLLECT_ITEM` | **`trigger_item_id`** | `max_fails` | Số giây **sau khi vật phẩm vào túi đồ** | Nhặt đúng vật phẩm `trigger_item_id` |
| `ON_TIMER` | **`delay_sec`** | `max_fails`, `trigger_item_id` | Số giây **đứng yên** trong khu vực | Hết thời gian đứng yên |
| `ON_WRONG_ITEM_USE` | — | `max_fails` | Số giây **sau khi thao tác sai kết thúc** | Dùng sai vật phẩm lên hotspot (lọc theo `trigger_item_id` nếu có) |

> **Hai sửa đổi so với bản trước, cả hai để khớp `schema/level.schema.json` và dữ liệu thật:**
>
> 1. **`delay_sec` không còn bị cấm trên `ON_ENTER_AREA` và `ON_COLLECT_ITEM`.** Ràng buộc cũ mâu thuẫn với ý đồ đạo diễn: `scare_hinh_nhan_chan_loi` (`ON_ENTER_AREA`) cần `delay_sec: 0.9` để bắn **sau** khi fade-in xong; `scare_di_anh_quay_mat` (`ON_COLLECT_ITEM`) cần `delay_sec: 0.25` để bắn **sau** khi dùi rời khỏi mõ. Độ trễ là công cụ dựng nhịp, không phải thứ riêng của `ON_TIMER`.
> 2. **`trigger_item_id` là BẮT BUỘC với `ON_COLLECT_ITEM`**, không phải "lọc nếu có". Không có nó thì cú doạ bắn khi nhặt **bất kỳ** vật phẩm nào trong khu vực — không một cú doạ nào của Chương 1 muốn thế, và không ai kiểm thử lại được một khiếu nại về nó.

**Kiểm tra chéo bổ sung:** nếu một câu đố trỏ `wrong_action_jumpscare` tới cú doạ X, mà X có `trigger_type` **không phải** `ON_PUZZLE_FAIL_COUNT` hoặc `ON_WRONG_ITEM_USE`, validator phát **[CẢNH BÁO]** — cú doạ đó sẽ không bao giờ bắn vì giải sai, tham chiếu là vô nghĩa.

## 2.6. Ví dụ đầy đủ — `data/areas/area_gian_tho.json` (trích)

Trích này lấy **nguyên văn giá trị từ dữ liệu thật**, và cố ý trưng ra cả chín trường logic mở rộng của §2.7.

```json
{
  "chapter_id": "chapter_01",
  "area_id": "area_gian_tho",
  "background_asset_url": "https://cdn.linhanthon.game/assets/bg_gian_tho.bundle",
  "ambience_address": "remote_ambience_gian_tho",
  "hotspots": [
    {
      "id": "hs_ban_tho_ho",
      "bounds": { "x": 640, "y": 300, "width": 660, "height": 420 },
      "action_type": "ZOOM_PUZZLE",
      "target_puzzle_id": "puz_tuan_tu_le_cung"
    },
    {
      "id": "hs_dui_mo",
      "bounds":        { "x": 555, "y": 780, "width": 120, "height": 120 },
      "visual_bounds": { "x": 560, "y": 780, "width": 110, "height": 120 },
      "action_type": "COLLECT_ITEM",
      "item_id": "item_dui_mo",
      "required_item": null,
      "one_shot": true
    },
    {
      "id": "hs_khe_mong_cua_gac",
      "bounds":        { "x": 430, "y": 115, "width": 150, "height": 120 },
      "visual_bounds": { "x": 430, "y": 120, "width": 150, "height": 110 },
      "action_type": "USE_ITEM",
      "required_item": "item_bai_vi_khuyet_danh",
      "item_id": "item_bai_vi_khuyet_danh",
      "grants_flag": "flag_then_gac_da_tra",
      "fallback_text_key": "txt_thieu_do_khe_mong_cua_gac",
      "one_shot": true
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
      "target_area_id": "area_bep_gieng",
      "required_flags": ["flag_puz_tuan_tu_le_cung_solved"],
      "fallback_text_key": "txt_khoa_cua_hau_xuong_bep"
    }
  ],
  "puzzles": [
    {
      "id": "puz_tuan_tu_le_cung",
      "type": "SEQUENCE_ORDER",
      "solution": [3, 6, 4, 1, 5, 2],
      "reward_item_id": "item_bai_vi_khuyet_danh",
      "wrong_action_jumpscare": "scare_khoi_tu_hinh_nguoi",
      "required_items": [],
      "grants_flag": "flag_puz_tuan_tu_le_cung_solved"
    },
    {
      "id": "puz_ba_hoi_chin_tieng",
      "type": "AUDIO_MATCH",
      "solution": [3, 3, 5, 3, 7, 3],
      "reward_item_id": "item_dai_vai_dieu",
      "wrong_action_jumpscare": "scare_khoi_tu_hinh_nguoi",
      "required_items": ["item_dui_mo"],
      "grants_flag": "flag_puz_ba_hoi_chin_tieng_solved"
    }
  ],
  "jumpscares": [
    {
      "id": "scare_khoi_tu_hinh_nguoi",
      "trigger_type": "ON_PUZZLE_FAIL_COUNT",
      "max_fails": 3,
      "cooldown_sec": 90,
      "audio_asset": "sfx_scare_khoi_tu.ogg",
      "sprite_animation": "anim_khoi_tu_dang_nguoi",
      "screen_flash": false
    },
    {
      "id": "scare_di_anh_quay_mat",
      "trigger_type": "ON_COLLECT_ITEM",
      "trigger_item_id": "item_dui_mo",
      "delay_sec": 0.25,
      "cooldown_sec": 90,
      "audio_asset": "sfx_scare_chan_nhang_boc.ogg",
      "sprite_animation": "anim_di_anh_dong_loat_quay",
      "screen_flash": false,
      "ghi_chu_vi": "S3 - impulse. Ban 250 ms sau khi dui roi khoi mo (nhat item_dui_mo). Mot lan duy nhat moi chuong."
    }
  ]
}
```

**Đọc trích này theo bảy điểm:**

| Dòng | Vì sao nó ở đó |
|---|---|
| `"ambience_address"` | Nếu thiếu, engine phải ghép chuỗi `"remote_ambience_" + area_id` trong mã — một phụ thuộc ẩn không cổng CI nào bắt được (§2.1.2) |
| `hs_dui_mo`: `bounds` 120×120 nhưng `visual_bounds` 110×120 | Dùi mõ vẽ rộng 110 px; vùng chạm nới sang trái 5 px để đạt sàn thiết kế 120. Đây là **vùng chạm mở rộng** (§2.3.4) |
| `hs_khe_mong_cua_gac`: `bounds` cao 120, `visual_bounds` cao 110 | Cùng cơ chế, nới đều 5 px lên trên và 5 px xuống dưới |
| `"grants_flag": "flag_then_gac_da_tra"` | Nguồn cấp **tường minh** cho cờ mở `area_gac_xep`. Không có nó là **[LỖI]** — trình kiểm không suy luận theo tên nữa (§5.3) |
| `"fallback_text_key"` trên hai hotspot bị chặn | Người chơi bấm mà chưa đủ điều kiện thì **được nghe một câu**, thay vì thấy không có gì xảy ra (§2.7.4) |
| `"required_items": ["item_dui_mo"]` | Mã hoá "phải cầm dùi mới gõ được mõ". Không có nó, `item_dui_mo` bị báo vật phẩm chết và phép chứng minh khả giải mất tính chặt (§5.4) |
| `"trigger_item_id"` + `"delay_sec"` trên `scare_di_anh_quay_mat` | `trigger_item_id` **bắt buộc** với `ON_COLLECT_ITEM`; `delay_sec: 0.25` đặt cú doạ **sau** khoảnh khắc dùi rời khỏi mõ, đúng nhịp đạo diễn (§2.7.7, §2.7.8) |

`[[ Luu y ve puz_tuan_tu_le_cung: "required_items": [] la mang RONG co chu dich — cau do nay khong can cong cu nao. Khac han voi viec khong khai truong. Con "grants_flag" o day khai lai dung co chinh tac flag_puz_tuan_tu_le_cung_solved: hop le, va co ich, vi no bien mot luat ngam thanh mot dong du lieu doc duoc. ]]`

## 2.7. Đặc tả đầy đủ các trường logic mở rộng

Chín trường dưới đây được thêm vào dữ liệu **song song** với việc tài liệu này được viết. Tám trong chín đã có trong `schema/level.schema.json` và đã có mặt trong `data/areas/*.json`; chỉ `ambience_address` (§2.1.2) là **đề nghị bổ sung**. Mục này là đặc tả đầy đủ của chúng — mỗi trường: **kiểu · bắt buộc khi nào · ý nghĩa · ràng buộc · ví dụ**.

| # | Trường | Kiểu | Trạng thái schema | Không có nó thì mất gì |
|---|---|---|---|---|
| 1 | `hotspots[].visual_bounds` | `Bounds \| null` | **Có** | Cơ chế vùng chạm mở rộng không khai báo được, QA đồ hoạ không có gì để soát |
| 2 | `hotspots[].grants_flag` | `string \| null` | **Có** | Cờ tiến trình không có nguồn cấp ⇒ chứng minh khả giải sụp |
| 3 | `hotspots[].required_flags` | `array<string>` | **Có** | Hotspot hiện ra trước khi được phép ⇒ vỡ thứ tự kịch bản |
| 4 | `hotspots[].fallback_text_key` | `string \| null` | **Có** | Người chơi bị chặn mà không được giải thích |
| 5 | `puzzles[].required_items` | `array<string>` | **Có** | Vật phẩm công cụ bị báo "chết", chứng minh khả giải mất chặt |
| 6 | `puzzles[].grants_flag` | `string \| null` | **Có** | Không đặt được tên cờ khác ngoài cờ chính tắc |
| 7 | `jumpscares[].trigger_item_id` | `string` | **Có** | Cú doạ bắn khi nhặt bất kỳ vật phẩm nào |
| 8 | `jumpscares[].delay_sec` | `number` | **Có** | Thời điểm bắn không xác định, mỗi máy một kiểu |
| 9 | `jumpscares[].cooldown_sec` (+ `cooldown_exempt`) | `number` / `boolean` | **Có** | Doạ liên tục, người chơi kỳ lại và cú doạ mất hết hiệu lực |
| — | `areas[].ambience_address` | `string \| null` | **CHƯA CÓ — đề nghị** | Tên bundle tiếng nền là phụ thuộc ẩn trong mã, không cổng CI nào bắt được |

---

### 2.7.1. `hotspots[].visual_bounds`

| Mục | Nội dung |
|---|---|
| **Kiểu** | `Bounds` (§2.2) hoặc `null` |
| **Bắt buộc khi nào** | Không bắt buộc về cú pháp. **Bắt buộc trên thực tế** khi vùng vẽ của sprite nhỏ hơn `bounds` quá 24 px ở bất kỳ chiều nào, và khi `min(bounds.width, bounds.height) < 120` |
| **Ý nghĩa** | Vùng **vẽ thật** của sprite. `bounds` = nơi ngón tay chạm; `visual_bounds` = nơi mắt nhìn |
| **Ràng buộc** | Nằm **trọn** trong `bounds` (bốn bất đẳng thức, §2.3.4.1). Không chịu luật chồng lấn B5. Không khai ⇒ engine coi bằng `bounds` |
| **Ví dụ** | Xem §2.3.4.2 — `hs_dui_mo` và `hs_chieu_coi_trai_san` |

Đặc tả đầy đủ, cùng phần validator và checklist đồ hoạ, nằm ở **§2.3.4**.

---

### 2.7.2. `hotspots[].grants_flag`

| Mục | Nội dung |
|---|---|
| **Kiểu** | `string` khớp `^flag_[a-z0-9_]+$` (6 – 64 ký tự), hoặc `null` |
| **Bắt buộc khi nào** | Cú pháp: không. **Logic: bắt buộc** nếu cờ ấy được bất kỳ `required_flags` hay `unlock_condition.required_flags` nào tham chiếu. Một cờ được tham chiếu mà **không** hotspot/puzzle nào khai `grants_flag` cho nó là **[LỖI]** — trình kiểm **không còn suy luận theo tên** (§5.3) |
| **Ý nghĩa** | Cờ tiến trình bật lên **sau khi hotspot chạy xong thành công**. Đây là **nguồn cấp tường minh duy nhất** cho một cờ do hotspot sinh ra |
| **Ràng buộc** | Một cờ nên có **đúng một** nguồn cấp. `null` nghĩa là *"hotspot này cố ý không cấp cờ nào"*, khác với việc không khai trường. Với `USE_ITEM`, `grants_flag` là một trong ba hiệu ứng hợp lệ (cùng `item_id` và `target_puzzle_id`) — phải có ít nhất một |
| **Ví dụ** | `{"id": "hs_o_lom_binh_phong", "action_type": "USE_ITEM", "required_item": "item_ban_rap_chu_the", "grants_flag": "flag_binh_phong_da_tra"}` |

**Bốn hotspot `USE_ITEM` của Chương 1 và cờ chúng cấp** — bảng đầy đủ ở §5.3.

---

### 2.7.3. `hotspots[].required_flags`

| Mục | Nội dung |
|---|---|
| **Kiểu** | `array<string>`, mỗi phần tử khớp `^flag_[a-z0-9_]+$`, **không trùng nhau** |
| **Bắt buộc khi nào** | Không. Mặc định `[]` |
| **Ý nghĩa** | Các cờ phải bật **đủ cả** (phép **AND**, không phải OR) thì hotspot mới hoạt động. Mảng rỗng = không điều kiện |
| **Ràng buộc** | Mỗi cờ phải có ít nhất một nguồn cấp tường minh trong chương (B9, §5.3). Hotspot có `required_flags` khác rỗng **nên** có `fallback_text_key` — thiếu là **[CẢNH BÁO]** |
| **Ví dụ** | `{"id": "hs_cau_thang_gac", "action_type": "CHANGE_AREA", "target_area_id": "area_gac_xep", "required_flags": ["flag_then_gac_da_tra"], "fallback_text_key": "txt_khoa_cau_thang_gac"}` |

**Phân biệt `required_flags` với `unlock_condition.required_flags`:** cái thứ nhất khoá **một hotspot** trong một khu vực; cái thứ hai khoá **cả một khu vực** ở tầng manifest. Cửa `CHANGE_AREA` thường cần cả hai, và hai chỗ ấy phải khai cùng một cờ — lệch nhau thì người chơi bấm được cửa nhưng bị chặn ở màn kế, hoặc ngược lại.

---

### 2.7.4. `hotspots[].fallback_text_key`

| Mục | Nội dung |
|---|---|
| **Kiểu** | `string` khớp `^txt_[a-z0-9_]+$` (5 – 96 ký tự), hoặc `null` |
| **Bắt buộc khi nào** | Không ★ — **rất khuyến nghị**. Hotspot có `required_item` khác `null` **hoặc** `required_flags` khác rỗng mà thiếu trường này ⇒ **[CẢNH BÁO]** |
| **Ý nghĩa** | Lời kể hiện ra khi người chơi bấm trúng hotspot **mà chưa đủ điều kiện**. Khác hẳn `text_key`: `text_key` là lời kể khi **thành công**, `fallback_text_key` là lời kể khi **bị chặn** |
| **Ràng buộc** | Phải có trong file localization. **Cấm** nhúng chuỗi tiếng Việt vào file dữ liệu. Nội dung phải nói *vì sao chưa được* theo giọng nhân vật, **không** nói *phải làm gì* — đó là việc của hệ gợi ý (`docs/04` §2) |
| **Ví dụ** | `{"id": "hs_khe_mong_cua_gac", "action_type": "USE_ITEM", "required_item": "item_bai_vi_khuyet_danh", "fallback_text_key": "txt_thieu_do_khe_mong_cua_gac"}` |

`[[ Day la truong chong "bam vao khong co gi xay ra" — trang thai te nhat cua mot game point-and-click. Nguoi choi bam, khong co phan hoi, ho ket luan hotspot hong va bo qua no vinh vien. Mot cau "Khe mong nay can mot cai gi vua khit — khong phai tay khong" giu ho lai. ]]`

---

### 2.7.5. `puzzles[].required_items`

| Mục | Nội dung |
|---|---|
| **Kiểu** | `array<string>`, mỗi phần tử khớp `^item_[a-z0-9_]+$`, **không trùng nhau** |
| **Bắt buộc khi nào** | Không ★ — **rất khuyến nghị**. Mặc định `[]` |
| **Ý nghĩa** | Các vật phẩm **công cụ** phải có sẵn trong túi đồ thì mới **nhập được lời giải**. Chúng **không bị tiêu thụ** |
| **Ràng buộc** | Mọi `item_id` phải có trong `item_catalog`. Thiếu trường ⇒ validator coi câu đố là giải được ngay khi vào khu vực, và mọi vật phẩm công cụ bị báo **[CẢNH BÁO]** vật phẩm chết (B7, §5.4) |
| **Ví dụ** | `{"id": "puz_ba_hoi_chin_tieng", "type": "AUDIO_MATCH", "solution": [3,3,5,3,7,3], "required_items": ["item_dui_mo"]}` |

> **`required_items` KHÔNG BAO GIỜ đổi `solution`.** Nó là điều kiện *mở bàn phím nhập*, không phải một phần của lời giải. Sáu mảng `solution` ở §2.4.3 là bất biến; thêm hay bớt `required_items` không được đụng tới một phần tử nào của chúng.

**Ba dòng bắt buộc của Chương 1** (khớp §5.4):

| Câu đố | `required_items` |
|---|---|
| `puz_rap_chu_the_menh` | `["item_giay_ban_va_than"]` |
| `puz_ba_hoi_chin_tieng` | `["item_dui_mo"]` |
| `puz_thap_lai_den_dau` | `["item_den_dau", "item_dai_vai_dieu", "item_chai_dau_hoa"]` |

---

### 2.7.6. `puzzles[].grants_flag`

| Mục | Nội dung |
|---|---|
| **Kiểu** | `string` khớp `^flag_[a-z0-9_]+$`, hoặc `null` |
| **Bắt buộc khi nào** | Không |
| **Ý nghĩa** | Cờ tiến trình **PHỤ**, bật khi giải đúng — **ngoài** cờ chính tắc |
| **Ràng buộc** | **Quy ước chính tắc là luật cố định, không phải mặc định của trường này:** giải xong câu đố `X` **luôn** bật cờ `flag_<X>_solved`, dù có khai `grants_flag` hay không. Engine và trình kiểm cùng hiện thực luật đó. Dùng `grants_flag` khi muốn **thêm** một tên cờ khác |
| **Ví dụ** | `{"id": "puz_tuan_tu_le_cung", "grants_flag": "flag_puz_tuan_tu_le_cung_solved"}` — khai lại đúng cờ chính tắc, hợp lệ và **có ích**: nó biến một luật ngầm thành một dòng dữ liệu đọc được |

`[[ Khac biet tinh te voi hotspots[].grants_flag: hotspot KHONG co co chinh tac. Neu mot hotspot khong khai grants_flag thi no khong bat co nao het. Cau do thi luon bat flag_<id>_solved. Dung nham hai luat nay. ]]`

---

### 2.7.7. `jumpscares[].trigger_item_id`

| Mục | Nội dung |
|---|---|
| **Kiểu** | `string` khớp `^item_[a-z0-9_]+$` |
| **Bắt buộc khi nào** | **BẮT BUỘC** với `trigger_type = ON_COLLECT_ITEM`. **Tuỳ chọn** với `ON_WRONG_ITEM_USE`. **CẤM** với `ON_PUZZLE_FAIL_COUNT`, `ON_ENTER_AREA`, `ON_TIMER` |
| **Ý nghĩa** | Vật phẩm gắn với cú doạ: với `ON_COLLECT_ITEM` là vật phẩm vừa nhặt; với `ON_WRONG_ITEM_USE` là vật phẩm bị dùng sai chỗ |
| **Ràng buộc** | Phải có trong `item_catalog`. Với `ON_COLLECT_ITEM`, vật phẩm ấy còn phải **nhặt được qua một hotspot `COLLECT_ITEM`** — nếu nó chỉ là `reward_item_id` của một câu đố thì cú doạ không bao giờ bắn ra được ⇒ cú doạ chết ⇒ **[LỖI]** |
| **Ví dụ** | `{"id": "scare_di_anh_quay_mat", "trigger_type": "ON_COLLECT_ITEM", "trigger_item_id": "item_dui_mo", "delay_sec": 0.25, "cooldown_sec": 90}` |

---

### 2.7.8. `jumpscares[].delay_sec`

| Mục | Nội dung |
|---|---|
| **Kiểu** | `number`, `0 ≤ v ≤ 600` |
| **Bắt buộc khi nào** | **BẮT BUỘC** với `ON_TIMER` — thiếu là **[LỖI]**: thời điểm bắn không xác định, mỗi máy bắn một kiểu, không ai kiểm thử lại được một khiếu nại. **Không ★** với mọi `trigger_type` khác |
| **Ý nghĩa** | Số giây từ lúc **điều kiện kích hoạt được thoả** tới lúc cú doạ **thật sự bắn**. Mốc "điều kiện được thoả" khác nhau theo `trigger_type` — xem cột thứ tư của bảng §2.5.2 |
| **Ràng buộc** | Với `ON_TIMER`, `delay_sec = 0` hợp lệ về kiểu nhưng bị **[CẢNH BÁO]**: bắn ngay khi vừa vào khu vực thì `ON_ENTER_AREA` mới đúng tên. Giá trị dưới 0,15 s trên trigger dạng xung (`ON_COLLECT_ITEM`, `ON_WRONG_ITEM_USE`) khiến người chơi không nối được nhân với quả — nên giữ trong dải **0,2 – 0,5 s** |
| **Ví dụ** | `{"id": "scare_hinh_nhan_chan_loi", "trigger_type": "ON_ENTER_AREA", "delay_sec": 0.9}` — bắn 900 ms **sau khi fade-in xong**, không phải 900 ms sau khi bắt đầu chuyển cảnh |

---

### 2.7.9. `jumpscares[].cooldown_sec` và `cooldown_exempt`

| Mục | `cooldown_sec` |
|---|---|
| **Kiểu** | `number`, `0 ≤ v ≤ 3600` |
| **Bắt buộc khi nào** | Không ★. Thiếu trên cú doạ **có thể bắn nhiều lần** (`ON_ENTER_AREA`, `ON_TIMER`, `ON_PUZZLE_FAIL_COUNT`) ⇒ **[CẢNH BÁO]** |
| **Ý nghĩa** | Thời gian nghỉ tối thiểu trước khi cú doạ này được bắn lại |
| **Ràng buộc** | Quy ước Chương 1: **90 giây**, khớp `ad_cooldown_after_scare_sec` của LiveOps và cửa sổ cấm quảng cáo `WITHIN_90S_AFTER_ANY_JUMPSCARE` (§4.6). Hai con số ấy **phải bằng nhau** — lệch thì hoặc quảng cáo lọt vào ngay sau một cú doạ, hoặc chặn quảng cáo lâu hơn cần thiết |
| **Ví dụ** | `{"id": "scare_bong_trong_chum", "trigger_type": "ON_PUZZLE_FAIL_COUNT", "max_fails": 3, "cooldown_sec": 90}` |

| Mục | `cooldown_exempt` |
|---|---|
| **Kiểu** | `boolean`, mặc định `false` |
| **Bắt buộc khi nào** | Không. Đặt `true` **chỉ khi** cú doạ cố ý không có `cooldown_sec` |
| **Ý nghĩa** | Khai báo bằng **dữ liệu** rằng việc thiếu `cooldown_sec` là có chủ đích, để trình kiểm thôi cảnh báo |
| **Ràng buộc** | Chỉ dùng cho cú doạ **nhẹ** (dread / ambience) được `04_horror.md` §2.7.2 miễn trừ luật nghỉ 90 giây: không transient, không `screen_flash`, không punch camera, không haptic ở mốc 0 ms. **Bắt buộc đi kèm `ghi_chu_vi`** nêu rõ căn cứ miễn trừ |
| **Ví dụ** | `scare_ao_cuoi_quay_dau` — cú đóng chương: `"trigger_type": "ON_TIMER", "delay_sec": 0.4, "screen_flash": false, "cooldown_exempt": true, "ghi_chu_vi": "S8 - dread scare, CO Y khong khai cooldown_sec: mien tru luat 90 s theo 04_horror.md muc 2.8.2..."` |

> **Vì sao miễn trừ phải là một trường chứ không phải một dòng ghi chú:** `ghi_chu_vi` là văn xuôi, trình kiểm không đọc được. Một cú doạ thiếu `cooldown_sec` mà chỉ có ghi chú sẽ hoặc bị cảnh báo mãi mãi (rồi người ta học cách bỏ qua cảnh báo), hoặc phải tắt luật kiểm (rồi mọi cú doạ khác cũng mất luật). Một trường boolean giải quyết cả hai: ý đồ thành dữ liệu, cảnh báo thành chính xác.

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
| `icon_asset` | string | **Có** | Biểu tượng trong túi đồ | `<tên>.png` — **khoá logic** như `background_asset_url` (§2.1.1). Cả 10 icon gói vào **một** atlas 1024×1024, nằm trong nhóm Addressables `remote_item_icons`, xem `docs/05` §2.1 và §3.1 |
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

JSON Schema chỉ nhìn được **một file tại một thời điểm**. Các nhóm ràng buộc dưới đây bắt buộc phải do `tools/validate_level.py` cưỡng chế.

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
| B9 | Mọi cờ trong `required_flags` **và** `unlock_condition.required_flags` đều có nguồn cấp **tường minh hoặc chính tắc** (§5.3) | **[LỖI]** | 7a |
| B10 | 16 bất biến LiveOps trong `validation.invariants` | **[LỖI]** | 11 |
| B11 | `visual_bounds` nằm **trọn** trong `bounds` của cùng hotspot (bốn bất đẳng thức, §2.3.4.1) | **[LỖI]** | 5 |
| B12 | `basename` của `background_asset_url` bằng đúng `"bg_" + area_id` đã bỏ tiền tố `area_` (§2.1.1) | **[LỖI]** | 7b |
| B13 | `ambience_address` khác `null` thì phần sau tiền tố phải bằng `area_id` (§2.1.2) | **[LỖI]** | 7b |
| B14 | Hotspot có `required_item ≠ null` hoặc `required_flags ≠ []` mà thiếu `fallback_text_key` (§2.7.4) | **[CẢNH BÁO]** | 7a |
| B15 | Cú doạ bắn được nhiều lần mà thiếu `cooldown_sec` và không có `cooldown_exempt: true` (§2.7.9) | **[CẢNH BÁO]** | 7b |

> **B5 và B11 là hai luật khác nhau, đừng gộp.** B5 cấm **`bounds` chồng `bounds`** — hai vùng chạm giao nhau thì người chơi bấm một chỗ ra hai kết quả. B11 chỉ kiểm **`visual_bounds` bên trong `bounds` của chính nó**. `visual_bounds` của hai hotspot khác nhau **được phép** gần nhau, thậm chí sát nhau — đồ vật vẽ cạnh đồ vật là chuyện thường; chỉ vùng chạm mới không được giẫm lên nhau.

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
| 2. **Quy ước chính tắc** | Tên cờ khớp mẫu `flag_<puzzle_id>_solved` và câu đố đó có thật. Đây là **luật cố định** của engine, không phải phỏng đoán (§2.7.6) | Chấp nhận, không cảnh báo |
| — | Không thoả mức 1 lẫn mức 2 | **[LỖI]** |

> **Mức 3 "suy luận theo từ khoá tên" đã bị BỎ.** Bản trước cho phép validator đối chiếu từ khoá giữa tên cờ và `id` các hotspot `USE_ITEM` trong khu vực nguồn, rồi gán tạm kèm cảnh báo. Ba lý do bỏ:
>
> 1. **Nó gãy lặng lẽ.** Đổi tên một hotspot là logic mở khoá đứt, mà cổng CI vẫn xanh vì suy luận tìm ra một ứng viên khác.
> 2. **Nó không còn cần thiết.** Cả bốn hotspot `USE_ITEM` của Chương 1 nay đã khai `grants_flag` tường minh — không cờ nào còn phải đoán.
> 3. **`schema/level.schema.json` đã chốt như vậy** trong mô tả của `hotspots[].grants_flag`: *"Trình kiểm KHÔNG suy luận nguồn cấp từ tên nữa"*. Tài liệu và schema phải nói cùng một câu.
>
> Hệ quả: một cờ được `required_flags` hay `unlock_condition.required_flags` tham chiếu mà không nơi nào khai `grants_flag` cho nó, và cũng không khớp mẫu chính tắc, là **[LỖI]** — mô phỏng khả giải ở giai đoạn 10 sẽ không bao giờ bật được cờ đó.

> **Khuyến nghị dứt khoát:** khai `grants_flag` tường minh trên **cả bốn** hotspot `USE_ITEM` của Chương 1, không chừa cái nào:
>
> | Hotspot | Khu vực | `grants_flag` | Vai trò |
> |---|---|---|---|
> | `hs_o_lom_binh_phong` | `area_hien_nha` | `flag_binh_phong_da_tra` | Mở đường sang `area_gian_tho` |
> | `hs_khe_mong_cua_gac` | `area_gian_tho` | `flag_then_gac_da_tra` | Mở đường lên `area_gac_xep` |
> | `hs_gieng_khoi` | `area_bep_gieng` | `flag_gieng_da_soi` | Soi sáng để lộ thông tin |
> | `hs_hinh_nhan` | `area_gac_xep` | `flag_chapter_01_hoan_thanh` | Đóng chương |
>
> Suy luận theo tên (mức 3) là chỗ dựa tạm; đổi tên hotspot một lần là logic mở khoá gãy mà không ai biết.

## 5.4. B7 — vì sao vật phẩm công cụ hay bị báo "chết"

Validator coi một vật phẩm là **được dùng tới** khi nó xuất hiện ở ít nhất một trong ba chỗ **máy đọc được**:

1. `hotspots[].required_item`
2. `puzzles[].required_items`
3. `unlock_condition.required_items`

Trường `dung_de` trong `item_catalog` là văn xuôi cho người đọc, **không** tính. Vì vậy **năm** vật phẩm công cụ — `item_giay_ban_va_than`, `item_dui_mo`, `item_den_dau`, `item_dai_vai_dieu`, `item_chai_dau_hoa` — sẽ bị báo **[CẢNH BÁO]** cho tới khi công dụng của chúng được mã hoá thành `required_items` trên đúng câu đố:

| Vật phẩm | Thuộc `required_items` của |
|---|---|
| `item_giay_ban_va_than` | `puz_rap_chu_the_menh` |
| `item_dui_mo` | `puz_ba_hoi_chin_tieng` |
| `item_den_dau`, `item_dai_vai_dieu`, `item_chai_dau_hoa` | `puz_thap_lai_den_dau` |

Khai báo đủ ba dòng của bảng trên (phủ cả năm vật phẩm) đem lại hai thứ cùng lúc: cảnh báo vật phẩm chết biến mất, **và** phép chứng minh khả giải ở giai đoạn 10 trở nên chặt thật sự — vì lúc đó nó mới kiểm được rằng người chơi đã cầm dùi mõ *trước khi* đứng trước cái mõ.

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
