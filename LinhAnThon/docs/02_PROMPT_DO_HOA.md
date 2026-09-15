# LINH AN THÔN — CHAPTER 1
## BỘ PROMPT ĐỒ HOẠ CHUẨN NGỮ CẢNH (MIDJOURNEY / STABLE DIFFUSION)

Tài liệu: `docs/02_PROMPT_DO_HOA.md` — **Deliverable BƯỚC 2 của Master Form**
Nguồn sự thật: **SPINE đã chốt** + `data/areas/*.json` (bounds hotspot, 8 `sprite_animation`) + `03_world.md` (bản phác bố cục dùng dựng ControlNet) + `02_puzzle.md` (khung zoom câu đố) + `01_narrative.md` (không khí, bảng màu, danh sách cấm) + **`docs/06_AN_TOAN_NGUOI_CHOI.md`** (mọi yêu cầu biến thể an toàn `_soft` / `_static`, trần độ sáng, bảng màu flash hợp lệ).

Độ phân giải thiết kế: **1920 x 1080**, gốc toạ độ **(0,0) ở góc TRÊN-BÊN TRÁI**.
Ngôn ngữ: phần giải thích bằng **tiếng Việt có dấu**; **prompt giữ nguyên tiếng Anh** để dán thẳng vào Midjourney / Stable Diffusion.

> **Tài liệu an toàn người chơi nay là deliverable:** `docs/06_AN_TOAN_NGUOI_CHOI.md`. Mọi chỗ trong tài liệu này trước đây trỏ vào file nháp `04_horror.md` cho phần an toàn / nhạy sáng / biến thể `_soft` `_static` đã được trỏ lại sang `docs/06`.

> **Nguyên tắc số 1 của tài liệu này:** không có "prompt template chung điền chỗ trống". Mỗi khu vực, mỗi câu đố, mỗi sprite có **một prompt riêng đã viết sẵn nội dung thật** — chuỗi `[TÊN KHU VỰC]` trong Master Form đã được thay bằng mô tả thật của chính khu vực đó, kèm chi tiết riêng khớp với bounds hotspot trong `03_world.md`.

---

## 0. CÁCH DÙNG TÀI LIỆU

| Mục | Nội dung | Số prompt |
|---|---|---|
| **§1** | Khoá nhất quán phong cách (bảng màu, chuỗi khoá, seed/sref) | — |
| **§2** | Quy ước đặt tên file xuất (khớp asset id trong JSON) | — |
| **§3 — MỤC A** | Prompt **bối cảnh 2D** — 1 prompt riêng cho từng area trong spine | **5** |
| **§4 — MỤC B** | Prompt **zoom cận cảnh giải đố** — 1 prompt riêng cho từng câu đố | **6** |
| **§5 — MỤC C** | Prompt **nhân vật & jump-scare sprite** — nền xám đặc `#808080` để tách nền | **13** |
| **§6** | Bảng tổng hợp tài sản + checklist QA trước khi đóng bundle | — |
| | **TỔNG** | **24 prompt** |

**Quy trình chuẩn cho hoạ sĩ / TA:**
1. Đọc §1, sinh **tấm neo phong cách** (`style_anchor_linhanthon_v1`) **trước tiên**. Chưa có tấm neo thì chưa được sinh bất cứ thứ gì khác.
2. Lấy URL tấm neo → dán vào chỗ `{STYLE_ANCHOR}` trong mọi dòng tham số Midjourney bên dưới.
3. Mỗi prompt gồm **4 khối copy nhanh**: `Prompt` → `Negative prompt` → `Midjourney (đuôi tham số)` → `Stable Diffusion (tham số)`.
4. Trong mọi khối Negative, chuỗi **`NEG-CORE,`** là chỗ **dán nguyên văn** khối negative gốc ở §1.3 (viết gọn để đỡ rườm rà tài liệu, khi dùng phải bung đủ).
5. Xuất file theo đúng §2. Sai tên file = Addressables không nạp được, không phải lỗi mỹ thuật mà là lỗi tích hợp.

---

## 1. KHOÁ NHẤT QUÁN PHONG CÁCH (STYLE CONSISTENCY LOCK)

### 1.1. Bảng màu chung toàn Chương 1 (master palette)

Toàn bộ 24 tài sản dùng **đúng 14 màu này**. Hoạ sĩ được pha trung gian, **không được thêm sắc độ lạ** (đặc biệt: không xanh lá tươi, không xanh dương bão hoà, không tím neon).

| # | Token | Hex | Tên tiếng Việt | Dùng ở đâu |
|---|---|---|---|---|
| 1 | `ink_black` | `#0E0F12` | Đen mực nhang | Bóng sâu nhất. **Không bao giờ dùng `#000000`** |
| 2 | `soot_grey` | `#1C2026` | Xám bồ hóng | Vách gỗ ám khói, trần bếp, xà nhà |
| 3 | `jack_wood` | `#2E2A24` | Nâu gỗ mít sẫm | Bình phong, mõ cá, hòm gỗ, cột hiên |
| 4 | `mud_brown` | `#4A4034` | Nâu bùn / đất nện | Nền bếp, sân sau, gạch vỡ |
| 5 | `moss_green` | `#55604A` | Xanh rêu mạch gạch | Sân gạch Bát Tràng, thành giếng, mép chum |
| 6 | `ash_grey` | `#7E8B93` | Xám tro chạng vạng | Bầu trời xa, khói, sương |
| 7 | `dusk_violet` | `#3A3F55` | Tím-xám giờ chạng vạng | Trời Area 1, fill lạnh toàn chương |
| 8 | `dieu_red` | `#8C3A2E` | Đỏ vải điều đã bạc | Vải điều bịt khám thờ Bà Cô, nẹp vải cũ đã bạc |
| 9 | `votive_red` | `#A63328` | Đỏ giấy hàng mã | Áo cưới giấy, vàng mã, giấy điều mới |
| 10 | `gilt_gold` | `#C9A227` | Sơn son thếp vàng tróc | Hoành phi, khám thờ, chữ đại tự |
| 11 | `lamp_warm` | `#FFD9A0` | Ánh đèn dầu Hoa Kỳ | **Key light duy nhất** của cả chương |
| 12 | `flash_bone` | `#FFF2DC` | Trắng ngà xung flash | Flash S1 / S2. **Bảng màu flash hợp lệ và trần alpha: `docs/06_AN_TOAN_NGUOI_CHOI.md` §2.4** |
| 13 | `ban_paper` | `#D9C9A3` | Giấy bản / giấy dó | Giấy rập, sổ, cáo phó, da hình nhân |
| 14 | `xo_white` | `#F2EDE3` | Trắng khăn xô | **Điểm trắng duy nhất** được phép trong khung hình |

**Luật dùng màu bắt buộc:**
- **Một nguồn sáng ấm duy nhất** (`lamp_warm` / than hồng) chọi với **fill lạnh** (`dusk_violet`). Không bao giờ có hai nguồn ấm cân bằng nhau trong một khung.
- **`xo_white` là tài nguyên hiếm**: mỗi khung hình chỉ được **một** mảng trắng thật. Ở Area 1 là mảnh khăn xô; ở Area 3 là bát cơm úp; ở Area 5 là khuôn mặt bị khoét.
- Độ bão hoà trung bình toàn khung **≤ 25%**. `votive_red` là ngoại lệ duy nhất được phép chói.
- **Không bao giờ vẽ mặt ma** (`01_narrative.md` Phụ lục B.1). Bóng ma luôn là **bóng, khói, giấy, hoặc mặt vẽ bằng than hai chấm một vạch**.

### 1.2. Chuỗi khoá phong cách `SL-CORE` — BẮT BUỘC xuất hiện trong MỌI prompt

Dán **nguyên văn** vào dòng `Style:` của cả 24 prompt. Không rút gọn, không đảo thứ tự, không dịch.

```plaintext
Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects
```

Lý do khoá cứng: mô hình khuếch tán trôi phong cách rất nhanh giữa các lần sinh cách nhau vài ngày. Chuỗi 50 từ này là **neo ngữ nghĩa**; `--sref` / LoRA là **neo thị giác**. Phải có **cả hai** mới giữ được 24 tài sản nhìn như cùng một hoạ sĩ vẽ.

### 1.3. Negative prompt gốc `NEG-CORE` — BẮT BUỘC cho mọi prompt

```plaintext
3D render, CGI, octane, unreal engine, photorealistic, photograph, anime, manga, chibi, cel shading, western cartoon, comic book, concept art sketch, HDR, bloom, lens flare, depth of field, bokeh, fisheye, wide angle distortion, vanishing point perspective, isometric, tilt-shift, text, letters, watermark, signature, logo, UI, HUD, frame, border, Chinese lantern festival, red Chinese new year decor, yin-yang clay roof tiles, interlocking tube-and-pan roof tiles, glazed green roof tiles, upturned flying eaves, Chinese temple roof, Japanese torii, kimono, samurai, Thai temple, Halloween pumpkin, crucifix, rosary, pentagram, ouija board, exorcism, western demon, horned devil, Annabelle doll, evil clown, Sadako, long-haired white ghost climbing out of a well, ghost face close-up, hollow black eye sockets, screaming mouth, sharp teeth, blood, gore, entrails, decomposed corpse, body horror, neon colors, oversaturated, pastel, cheerful, sunny daylight, clean, brand new, glossy, plastic, clutter, unreadable silhouette
```

Ba nhóm trong `NEG-CORE` và lý do:
- **Nhóm kỹ thuật** (3D, HDR, DOF, perspective): game là **Orthographic phẳng**, mọi hiệu ứng ống kính sẽ phá cảm giác mặt phẳng và làm hotspot lệch khỏi bounds.
- **Nhóm sai văn hoá** (Chinese new year, **yin-yang / tube-and-pan roof tiles**, torii, kimono, Thai temple, crucifix, pentagram): mô hình rất hay trượt từ "Asian folk horror" sang Trung/Nhật/Thái hoặc sang exorcism phương Tây. Đây là lỗi **chí mạng** với dự án này.
  > **Chỗ trượt âm thầm nhất là MÁI NHÀ.** Hễ nhắc "clay roof tiles" là mô hình vẽ **ngói âm dương** (ngói ống + ngói lòng máng úp ngửa xen kẽ) — đó là ngói Hoa / nhà miền núi phía Bắc, **không phải** nhà ba gian đồng bằng Bắc Bộ. Nhà ba gian Bắc Bộ lợp **ngói mũi hài** (ngói ta): viên dẹt, đầu bo tròn hình mũi hài, **xếp lớp chồng mép kiểu vảy cá**, mái thẳng dốc thoải, bờ nóc trơn, không đao cong. Mọi prompt có mái nhà **bắt buộc** ghi rõ `mui-hai` + `fish-scale courses`, và `yin-yang clay roof tiles` phải nằm trong negative.
- **Nhóm cliché bị cấm** (Sadako, ghost face, blood, gore): trích thẳng từ `01_narrative.md` Phụ lục B.1. Đặc biệt `long-haired white ghost climbing out of a well` **phải luôn có mặt** vì Area 4 có giếng khơi — mô hình sẽ tự động vẽ Sadako nếu không chặn.

### 1.4. Giao thức seed / `--sref` / LoRA để giữ đồng bộ

**Bước 0 — Tấm neo phong cách (làm một lần, trước tất cả).**

```plaintext
Style anchor plate for a Vietnamese folk-horror point-and-click game: the corner of a smoke-blackened wooden ancestral room, one lit kerosene hurricane lamp on a jackfruit-wood table, a faded red cloth strip, a sheet of do paper, damp mossy brick floor, empty of people.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: this plate exists only to define material and light language — wet brick, soot on wood, gold leaf flaking off lacquer, oil-lamp halo falling off within one arm length, paper fibre texture on every pale surface, cold violet fill #3A3F55 in every shadow, saturation under 25 percent, exactly one pure white accent.
Format: 1920x1080, 16:9, flat orthographic, centred, no characters, no text.
```

Chọn **1 tấm tốt nhất** → upscale → lưu `art/_anchor/style_anchor_linhanthon_v1.png` → lấy URL → đó là `{STYLE_ANCHOR}`.

**Midjourney:**

| Tham số | Giá trị chốt | Lý do |
|---|---|---|
| `--sref {STYLE_ANCHOR}` | URL tấm neo | Neo thị giác, quan trọng nhất |
| `--sw 140` | 140 (thang 0–1000, mặc định 100) | Đủ mạnh để bám phong cách, chưa đè mất nội dung riêng của từng area |
| `--style raw` | luôn luôn | Tắt lớp "làm đẹp" mặc định của MJ — tranh phải **bẩn**, không được bóng bẩy |
| `--seed` | xem bảng dưới | Cùng seed + cùng `--sref` = cùng "tay vẽ" |
| `--chaos 0` | luôn luôn | Cần lặp lại được, không cần đa dạng |
| `--v 6.1` | khoá phiên bản | **Không đổi version giữa chừng chương.** Đổi version = vẽ lại từ đầu |
| `--no` | rút gọn từ `NEG-CORE` | MJ chỉ nhận danh sách ngắn, xem từng prompt |

**Bảng seed chốt cho Chương 1** (đổi seed = mất đồng bộ, phải xin duyệt Art Lead):

| Nhóm tài sản | Seed | Ghi chú |
|---|---|---|
| Tấm neo phong cách | `179611` | Seed gốc toàn dự án |
| MỤC A — bối cảnh 5 area | `179611` + thứ tự area → `179612` … `179616` | Area 1 = 179612, Area 5 = 179616 |
| MỤC B — zoom 6 câu đố | `179621` … `179626` | Theo thứ tự P1…P6 |
| MỤC C — sprite jump-scare | `179631` … `179643` | Theo thứ tự C1…C13 |
| Biến thể `_soft` / `_static` | **dùng lại đúng seed của bản gốc** | Biến thể phải là **cùng một hình**, chỉ khác biên độ |

**Stable Diffusion:**

| Tham số | Giá trị chốt |
|---|---|
| Checkpoint | 1 model duy nhất cho cả chương (khuyến nghị SDXL base + refiner, hoặc 1 model illustration SDXL) — **khoá hash model, ghi vào `art/_anchor/README`** |
| LoRA | `linhanthon_style_v1` — huấn luyện trên **16–20 tấm** đã duyệt từ tấm neo + Area 1/Area 3, weight **0.75** cho bối cảnh, **0.65** cho sprite |
| Sampler | `DPM++ 2M Karras` |
| Steps | **34** (bối cảnh) / **28** (sprite) |
| CFG | **6.5** (bối cảnh) / **7.0** (sprite, cần bám mô tả chặt hơn) |
| Hires fix | Latent (nearest-exact), scale **1.5x**, denoise **0.38** |
| ControlNet | `lineart` weight **0.55** từ **bản phác bố cục ASCII trong `03_world.md`** đã dựng lại thành sketch — đây là cách giữ hotspot đúng bounds |
| Clip skip | 2 |

> **Vì sao phải dùng ControlNet cho MỤC A:** bounds hotspot trong `03_world.md` là **hợp đồng cứng** với tổ code. Nếu cái chum nước rơi lệch 200px so với `{x:330, y:730, width:300, height:260}` thì người chơi bấm vào khoảng không. ControlNet lineart từ bản phác là cách duy nhất ép mô hình đặt đồ vật đúng ô.

### 1.5. Danh sách CẤM tuyệt đối (kế thừa `01_narrative.md` Phụ lục B.1)

Áp cho **mọi** khâu mỹ thuật, kể cả ảnh nháp gửi nội bộ:

| Cấm | Thay bằng |
|---|---|
| Ma tóc dài trắng trèo lên từ giếng (Sadako) | Giếng chỉ trả về **một chiếc guốc trẻ con** và **một quầng sáng thứ hai** |
| Mặt ma cận cảnh, hốc mắt đen, miệng hét | **Bóng đen phẳng**, **khói tụ**, hoặc **mặt vẽ than hai chấm một vạch** trên giấy |
| Máu, nội tạng, xác phân huỷ | Giấy rách, mực nhoè, mốc, tro, nước giếng |
| Búp bê ma, hề ma, gương vỡ có tay thò ra | Hình nhân nan tre dán giấy bản |
| Thánh giá, ngũ giác, ouija, phù thuỷ | Bát quái, bài vị, khám thờ, mõ cá, vàng mã |
| Đèn lồng đỏ Trung Hoa, torii Nhật, kimono | Mành nứa, guốc mộc, khăn mỏ quạ, chõng tre, điếu bát |
| **Ngói âm dương** (ngói ống + lòng máng), mái đao cong vút, ngói men xanh | **Ngói mũi hài** (ngói ta) xếp lớp **kiểu vảy cá**, mái thẳng dốc thoải, bờ nóc trơn, rui mè ám bồ hóng |
| Câu đối **giấy điều đỏ** treo ở nhà đang có tang | Câu đối **khắc chìm vào vữa bằng chữ Hán**, dán đè một dải **giấy trắng để tang** (giấy bản `#D9C9A3`), giấy bong/rách nên vẫn đọc được chữ bên dưới |
| Màu neon, ánh sáng bão hoà, trời nắng | Chạng vạng, đèn dầu, than hồng, tối 70% khung ở Area 4 |

---

## 2. QUY ƯỚC ĐẶT TÊN FILE XUẤT (khớp asset id trong JSON)

### 2.1. Luật gốc

| Loại | Công thức tên | Ví dụ | Xuất hiện ở đâu trong JSON |
|---|---|---|---|
| **Bối cảnh** | `bg_` + `<area_id>` bỏ tiền tố `area_` | `area_gian_tho` → **`bg_gian_tho`** | `background_asset_url: ".../bg_gian_tho.bundle"` |
| **Zoom câu đố** | `zoom_` + `<puzzle_id>` **giữ nguyên** tiền tố `puz_` | `puz_khoa_bat_quai` → **`zoom_puz_khoa_bat_quai`** | `puzzles[].id` (engine ghép `zoom_` + id) |
| **Sprite jump-scare** | `spr_<ten_khong_dau>` — **dùng đúng tên đã chốt trong `data/areas/*.json`** (`jumpscares[].sprite_animation`); bảng đối chiếu đầy đủ 8 cú: `docs/06_AN_TOAN_NGUOI_CHOI.md` §4.4.1 | **`spr_hinh_nhan_the_mang`** | `jumpscares[].sprite_animation` = `anim_<ten>` trỏ tới sheet của sprite này |
| **Sheet animation** | `anim_<ten_khong_dau>` | **`anim_hinh_nhan_hien_gan`** | `jumpscares[].sprite_animation` (nguyên văn) |
| **Icon vật phẩm** | `icon_` + `<item_id>` **giữ nguyên** tiền tố `item_` | `item_ao_cuoi_giay` → **`icon_item_ao_cuoi_giay`** | `hotspots[].item_id` (engine ghép `icon_` + id) |

> **Không đặt dấu tiếng Việt, không viết hoa, không dấu cách, không gạch ngang.** Chỉ `a-z`, `0-9`, `_`. Đây là ràng buộc của Addressables key, không phải sở thích.

### 2.2. Hậu tố lớp và biến thể

| Hậu tố | Nghĩa | Bắt buộc cho |
|---|---|---|
| `_l0_back` | Lớp BACKGROUND (parallax 0.00) | Mọi bối cảnh |
| `_l1_mid` | Lớp MIDGROUND (chứa phần lớn hotspot) | Mọi bối cảnh |
| `_l2_fore` | Lớp FOREGROUND (parallax 0.03–0.06) | Mọi bối cảnh |
| `_l3_fx` | Lớp FX overlay (khói, bụi, vignette) | Mọi bối cảnh |
| `_flat` | Bản dẹt 1 lớp để duyệt nhanh / thumbnail | Mọi bối cảnh, **không đóng bundle** |
| `_plate` | Nền tĩnh của khung zoom câu đố | Mọi zoom |
| `_parts` | Atlas các phần tử người chơi thao tác được | Mọi zoom |
| `_soft` | Biến thể **giảm chuyển động** (`gentle_mode` / `reduce_motion`) — xem `docs/06_AN_TOAN_NGUOI_CHOI.md` §4.3 | 8 sprite jump-scare |
| `_static` | Biến thể **không animation** (`scare_intensity = 0`) — xem `docs/06_AN_TOAN_NGUOI_CHOI.md` §4.3 và §4.5 | 8 sprite jump-scare |
| `_f00` … `_f11` | Khung hình rời trước khi đóng sheet | Sprite có animation |

### 2.3. Ví dụ đầy đủ một bộ (Area 3 — gian thờ)

```plaintext
art/bg/bg_gian_tho_l0_back.png        4096 x 2304, PNG-24
art/bg/bg_gian_tho_l1_mid.png         4096 x 2304, PNG-32 (alpha)
art/bg/bg_gian_tho_l2_fore.png        4096 x 2304, PNG-32 (alpha)
art/bg/bg_gian_tho_l3_fx.png          4096 x 2304, PNG-32 (alpha)
art/bg/bg_gian_tho_flat.png           1920 x 1080, chỉ để duyệt
  -> Addressables bundle: bg_gian_tho.bundle
  -> JSON: "background_asset_url": "https://cdn.linhanthon.game/assets/bg_gian_tho.bundle"

art/zoom/zoom_puz_tuan_tu_le_cung_plate.png    1920 x 1080
art/zoom/zoom_puz_tuan_tu_le_cung_parts.png    2048 x 2048 atlas
  -> Addressables bundle: zoom_puz_tuan_tu_le_cung.bundle

art/spr/spr_chan_nhang_chay_f00.png ... _f07.png    1024 x 1024
art/spr/anim_di_anh_dong_loat_quay.png             2048 x 2048 sheet
art/spr/anim_di_anh_dong_loat_quay_soft.png
art/spr/anim_di_anh_dong_loat_quay_static.png
  -> Addressables bundle: scare_di_anh_quay_mat.bundle
  -> JSON: "sprite_animation": "anim_di_anh_dong_loat_quay"

art/icon/icon_item_dui_mo.png         320 x 320 -> đóng atlas 160 x 160 @1x
```

### 2.4. Ràng buộc kỹ thuật xuất file (APK ≤ 30MB, tất cả qua remote bundle)

- **Vẽ ở 4096 x 2304** (2x design res) → xuất **1920 x 1080** cho bản chuẩn và **1280 x 720** cho biến thể `_lo` dành máy yếu.
- Nén cuối: **ASTC 6x6** (iOS/Android hiện đại), fallback **ETC2 RGBA8** (Android cũ). Không đưa PNG thô vào bundle.
- Atlas sprite tối đa **2048 x 2048**, padding **4px**, **không** rotate.
- Alpha của sprite phải **sạch tuyệt đối** sau khi tách nền `#808080` — mép giấy/nan tre là chỗ dễ sót viền xám nhất, bắt buộc kiểm ở zoom 400%.
- Pivot sprite jump-scare: **bottom-center** cho vật đứng (`spr_hinh_nhan_the_mang`), **center** cho vật bay/quét (`spr_ban_tay_vang_ma`).
- Mọi PNG trung gian **không** commit vào repo game; chỉ commit bản đã nén + manifest.

---

# 3. MỤC A — PROMPT BỐI CẢNH (2D BACKGROUND)

**5 prompt riêng biệt, mỗi area một prompt.** Không có prompt chung. Chuỗi `[TÊN KHU VỰC]` của Master Form đã được thay bằng mô tả thật, và mỗi prompt được bổ sung **danh sách đồ vật bắt buộc phải nhìn thấy** — chính là các hotspot trong `03_world.md`, đặt đúng vùng màn hình tương ứng với bounds.

> **Luật chung của MỤC A:** không người, không bàn tay, không ma trong bản nền. Mọi thứ động đều là sprite rời (MỤC C). Ngoại lệ duy nhất: **hình nhân thế mạng ở Area 5** — nó là đồ vật có thật, đứng đó suốt chương, nên nằm trong lớp MIDGROUND của bản nền.

---

## A1 · `bg_san_gach` — `area_san_gach` "Sân gạch và ngõ vào"

*Chiều rằm tháng Bảy, 17h40, vừa tạnh mưa rào. Giờ chạng vạng — giờ người và bóng lẫn vào nhau. Đây là area hướng dẫn: người chơi học cơ chế hotspot, và nhặt manh mối đầu tiên về đám tang vừa xong.*

**Prompt**

```plaintext
2D hand-painted background plate for a point-and-click horror game — the moss-stained Bat Trang brick courtyard and bamboo-lane entrance of a three-bay Northern Vietnamese ancestral house, 17:40 on a rain-wet evening of the seventh lunar month, seen by a visitor standing at the closed gate.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: BACKGROUND LAYER — violet-grey dusk sky #3A3F55 after rain, flat black bamboo-hedge silhouette across the whole top, a concrete pole carrying a rusted commune loudspeaker at upper centre-left, the fish-scale mui-hai clay-tile roof of the three-bay house filling the right half, thin cooking smoke from a neighbour's kitchen. MIDGROUND LAYER — a closed double wooden gate in the left third between two brick pillars, each pillar carrying one half of a parallel couplet incised into the lime mortar in Han characters, the incision now pasted over with a strip of plain off-white do-paper mourning band #D9C9A3 because the house is in mourning, the band already lifting at one corner and torn along its length so the incised Han characters underneath stay fully readable, and a small carved Vietnamese note at the pillar base, a round wood-framed bat quai mirror hanging on the gate lintel above, a three-ring concentric wooden padlock carved with eight trigrams set between the gate leaves, on the right the house facade with closed buc ban wooden doors above three stone steps and a brass padlock dangling from the crossbar, a white mourning notice with rain-bled purple ink pasted on the veranda pillar, a washing line strung from the veranda pillar across to an areca palm. FOREGROUND LAYER — wet mossy brick paving with green-black joints, a Thong Nhat bicycle leaning on the left wall with a knotted cloth bag in its front basket, a large glazed stoneware rain jar at lower-left-of-centre brimming with black mirror-still water, a coconut ladle lying on the bricks one step away from the jar as if just dropped, a dented aluminium basin of votive ash mid-bottom with half-burnt joss paper still showing printed characters, a gap between two floor bricks at lower right with a folded yellowed note pushed deep inside. FX LAYER — backlit evening dust, a few mosquitoes, very light drizzle at ten percent opacity, cold blue vignette. Colour discipline: exactly ONE pure white note in the whole frame, the torn muslin mourning cloth #F2EDE3 hanging wet on the line; everything else stays grey, mud brown and moss green.
Format: 1920x1080, 16:9, flat orthographic front elevation, locked camera, horizon at 45 percent height, every interactive prop fully inside frame with an 80px safe margin top and bottom, at least 20px of empty breathing space between neighbouring props, readable silhouettes, no characters, no people, no hands, no ghosts, no text, delivered as four separate layers BACKGROUND / MIDGROUND / FOREGROUND / FX on transparent PNG.
```

**Negative prompt**

```plaintext
NEG-CORE, red paper couplet banners, bright red couplet strips on the gate pillars, freshly pasted red paper, yin-yang tube-and-pan roof tiles, upturned curved eaves, sunny sky, blue sky, green healthy lawn, flowers in bloom, festive red lanterns, new paint, tourist heritage site, Chinese courtyard, Japanese garden, stone lion statues, people, silhouette of a person standing in the yard, reflection of a figure in the water jar, car, motorbike, power lines crossing the sky, modern plastic furniture
```

Aspect ratio: **16:9 — 1920 x 1080**

**Midjourney (đuôi tham số)**

```plaintext
--ar 16:9 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179612 --chaos 0 --no people, person, figure, reflection of a person, sunny, blue sky, red lanterns, text, 3D render, photorealistic, Sadako, blood
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 34 | CFG 6.5 | Seed 179612 | Size 1024x576 -> Hires Latent 1.5x denoise 0.38 -> 1920x1080
ControlNet lineart weight 0.55, ảnh điều khiển = sketch dựng lại từ bản phác 03_world.md §1.1.1
LoRA linhanthon_style_v1 : 0.75 | Clip skip 2
```

**Chốt bố cục (bắt buộc khớp bounds `03_world.md` §1.1.2):**

| Đồ vật trong prompt | Hotspot | Vùng màn hình |
|---|---|---|
| Gương bát quái trên xà cổng | `hs_guong_bat_quai` | `{296,150,130,130}` — trên, trái |
| Loa phát thanh trên cột | `hs_loa_phat_thanh` | `{700,120,200,150}` — trên, giữa |
| Cột gạch trái / phải + câu đối khắc chìm, dán giấy trắng để tang | `hs_cau_doi_trai` / `hs_cau_doi_phai` | vùng chạm `{83,300,120,420}` / `{515,300,120,420}`; **nét vẽ** câu đối vẫn rộng 110 px — `visual_bounds` `{88,300,110,420}` / `{520,300,110,420}` |
| Ổ khoá gỗ ba vòng giữa hai cánh cổng | `hs_o_khoa_cong` | `{280,430,180,180}` |
| Cáo phó trên cột hiên | `hs_cao_pho` | `{1000,330,150,210}` |
| Bậc tam cấp + cửa bức bàn | `hs_cua_vao_hien` | `{1180,380,300,520}` |
| Dây phơi + khăn xô | `hs_day_phoi_khan_xo` | `{1540,230,340,150}` |
| Xe đạp + túi vải | `hs_xe_dap_tui_vai` | `{60,760,240,230}` |
| Chum nước mưa (góc Bắc) | `hs_chum_nuoc_mua` | `{330,730,300,260}` |
| Gáo dừa rơi trên gạch | `hs_gao_dua` | vùng chạm `{648,795,130,120}`; **nét vẽ** `{648,800,130,110}` |
| Chậu hoá vàng | `hs_dong_tro_hoa_vang` | `{820,820,280,170}` |
| Khe gạch chân tường | `hs_khe_gach_thu_tay` | `{1560,800,220,120}` |

> **Ghi chú tục tang — bắt buộc đọc trước khi sinh A1.** Nhà này **vừa có tang ba ngày** (cáo phó còn dán, khăn xô còn ướt trên dây phơi). Theo lệ Bắc Bộ, nhà có tang thì **phủ hoặc thay câu đối**: dải **giấy điều đỏ** phải được gỡ xuống hoặc dán đè bằng **giấy trắng** cho tới khi mãn tang. Vì vậy trong A1 câu đối **không phải giấy đỏ** — nó là **chữ Hán khắc chìm vào lớp vữa cột gạch**, bên trên dán một dải **giấy bản trắng ngà `#D9C9A3`** đang bong mép và rách dọc.
>
> **Ba ràng buộc không được vi phạm khi vẽ:**
> 1. **Nội dung câu đối giữ nguyên 100%** — nó là **clue C2 và C3 của `puz_khoa_bat_quai`** (vế trái *"Toạ Bắc — lưng dựa dòng nước"* → Khảm; vế phải *"Hướng Nam — mặt đón lửa trời"* → Ly). Che mất chữ = người chơi mất hai manh mối = câu đố không giải được. Giấy tang **phải** bong/rách đủ để đọc được nét khắc bên dưới.
> 2. **Chữ khắc là chữ Hán (chữ Nho), không phải chữ Nôm.** Dòng chú thích nhỏ khắc bằng mũi dao ở **chân cột** mới là **quốc ngữ** — hai thứ chữ khác nhau, khác vị trí, không được trộn.
> 3. **Giấy tang là `ban_paper #D9C9A3` (trắng ngà), KHÔNG phải `xo_white #F2EDE3`.** Suất trắng tinh duy nhất của khung hình A1 đã dành cho **mảnh khăn xô trên dây phơi** (§1.1). Vẽ giấy tang trắng tinh là phá luật "một điểm trắng duy nhất".

---

## A2 · `bg_hien_nha` — `area_hien_nha` "Hiên nhà và bức bình phong"

*18h10, trời sập hẳn. Area "ngưỡng": không gian hẹp lại, trần thấp xuống, camera đẩy gần hơn Area 1 khoảng 15%. Gió lùa dọc hiên làm mành nứa đập vào khung cửa theo nhịp không đều — đó là âm thanh nhận dạng của khu vực, và cũng là thứ sẽ dùng để doạ ở S2.*

**Prompt**

```plaintext
2D hand-painted background plate for a point-and-click horror game — the brick veranda and carved wooden screen at the threshold of a three-bay Northern Vietnamese ancestral house at 18:10, full night outside, the last cold blue of dusk washing in from the yard on the left and a thin warm seam of light leaking under the inner door on the right.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: BACKGROUND LAYER — dark three-bay timber wall, a small lacquered horizontal board so faded its characters are gone, a warm orange seam of light escaping under the closed inner door, ceiling pressed low so the frame feels vertically compressed. MIDGROUND LAYER — the hero object dead centre, a tall dark jackfruit-wood folding screen taller than a person, its surface polished black by decades of hands, carrying two Han characters worn almost flat so only a shallow groove remains, a rectangular recess exactly the depth of one sheet of do paper cut into the wooden frame at the screen's right edge, a soot-blackened American-style kerosene hurricane lamp hanging from a hook on the veranda post at far right with a dry empty fount, a closed ironwood buc ban door on the right. FOREGROUND LAYER — a smoke-stained split-bamboo blind hanging across the very top of the frame, slightly askew, its dust marks forming two clean square patches where something used to hang, a bamboo daybed on the left carrying a clay water pipe, a chewed dark quid of betel and a chipped cup, a rolled torn sedge mat with the corner of a blue-covered notebook poking out from under it, a low wooden stool on the left with a child's calligraphy practice book open on it, three stone steps at the extreme left edge going back down to the yard with slippery moss, a pair of wooden clogs set neatly on the brick floor with their toes pointing into the house and black charcoal crumbs on the soles, a small stack of thin do paper weighted by a sharpened charcoal stick at the foot of the screen. FX LAYER — thin drifting incense haze crossing horizontally, dust in the door seam light, the unlit lamp's halo painted as cold grey rather than warm.
Format: 1920x1080, 16:9, flat orthographic front elevation, locked camera, framing 15 percent tighter than the courtyard plate, low ceiling, every interactive prop fully inside frame with an 80px safe margin top and bottom, the three floor props along the bottom edge separated by at least 60px, no characters, no people, no hands, no ghosts, no text, delivered as four separate layers BACKGROUND / MIDGROUND / FOREGROUND / FX on transparent PNG.
```

**Negative prompt**

```plaintext
NEG-CORE, bright interior lighting, lamp already lit and glowing, Chinese folding screen with painted landscape, gold ornate carving, calligraphy clearly legible, Japanese shoji, tatami, people, hand reaching from behind the blind, ghost silhouette, crowded props, symmetrical composition
```

Aspect ratio: **16:9 — 1920 x 1080**

**Midjourney (đuôi tham số)**

```plaintext
--ar 16:9 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179613 --chaos 0 --no people, hand, ghost, lit lamp, bright light, shoji, tatami, ornate gold carving, text, 3D render, photorealistic
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 34 | CFG 6.5 | Seed 179613 | Size 1024x576 -> Hires Latent 1.5x denoise 0.38 -> 1920x1080
ControlNet lineart weight 0.55, ảnh điều khiển = sketch dựng lại từ bản phác 03_world.md §1.2.1
LoRA linhanthon_style_v1 : 0.75 | Clip skip 2
```

**Chốt bố cục (bắt buộc khớp bounds `03_world.md` §1.2.2):**

| Đồ vật trong prompt | Hotspot | Vùng màn hình |
|---|---|---|
| Mành nứa treo ngang mép trên | `hs_manh_nua` | `{360,96,1000,130}` |
| Đèn dầu Hoa Kỳ treo trên móc cột | `hs_den_dau_treo` | `{1500,180,160,250}` |
| Bức bình phong (hai chữ bị bào mờ) | `hs_binh_phong` | `{640,300,420,560}` |
| Ô lõm chữ nhật trên khung bình phong | `hs_o_lom_binh_phong` | `{1080,470,130,180}` — **cách bình phong đúng 20px, không được vẽ dính** |
| Cửa bức bàn | `hs_cua_buc_ban` | `{1420,470,280,450}` |
| Vở tập viết chữ Nho trên đôn | `hs_vo_tap_viet` | `{170,430,220,140}` |
| Bậc tam cấp mép trái | `hs_xuong_san_gach` | `{30,600,120,270}` |
| Chõng tre + điếu bát | `hs_chong_tre` | `{170,600,390,270}` |
| Sổ bìa xanh dưới manh chiếu | `hs_nhat_ky_duoi_chieu` | vùng chạm `{160,882,280,120}`; **nét vẽ** `{160,890,280,105}` |
| Đôi guốc mộc | `hs_guoc_moc` | vùng chạm `{640,882,240,120}`; **nét vẽ** `{640,890,240,105}` |
| Xấp giấy bản + thỏi than | `hs_giay_ban_va_than` | vùng chạm `{940,882,200,120}`; **nét vẽ** `{940,890,200,105}` |

---

## A3 · `bg_gian_tho` — `area_gian_tho` "Gian thờ giữa và bàn thờ họ"

*18h40. Trung tâm thông tin của chương, mật độ chữ cao nhất, và cũng là area đông hotspot nhất (17 cái). Cột trái là "trục Bà Cô" (khám thờ → bài vị → vải điều → **bộ pháp khí chuông-mõ trên đôn gỗ thấp**), cột phải là "trục tài liệu" (gia phả → văn khấn → vách buồng). Bàn thờ giữ trọn tâm màn hình.*

**Prompt**

```plaintext
2D hand-painted background plate for a point-and-click horror game — the central bay and clan ancestral altar of a three-bay Northern Vietnamese house at 18:40, high black timber ceiling, the room one stop darker than the veranda, lit only by a single guttering oil lamp on the left of the altar while its twin on the right sits dead with a full fount.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: BACKGROUND LAYER — soot-blackened timber walls, a long red-and-gold lacquered horizontal board across the upper centre with four large characters whose gold leaf has flaked away, a dark doorway to an inner chamber at the right edge, a hanging coil of incense burning on the crossbeam at upper right, its ash fallen into a spiral on the floor. MIDGROUND LAYER — the clan altar occupying the exact centre, left in the half-cleared mess of a funeral just ended: a lacquered fruit tray pushed off-axis, a plate of sticky rice, a spilled cup of rice wine, an upturned bowl of rice with a halved boiled egg and a pair of white funeral chopsticks standing upright in it, stacks of votive paper piled at its feet, a crazed-glaze ceramic incense bowl visibly rotated forty-five degrees out of line with the board above and its whole bundle of old joss sticks leaning with it; on the far left wall a small separate wooden shrine niche a hand lower than the altar, its door sealed with a strip of faded red cloth, no photograph, no name, no bowl of its own; beside it a steep seven-step worm-eaten wooden ladder climbing to a loft hatch with its fourth step half broken, and above the hatch a narrow rectangular mortise slot in the door frame exactly where a crossbar should be; on the right a tea cabinet with a cloth-bound family register lying open, one line in the grandchildren row scraped away until the paper tore. FOREGROUND LAYER — a sedge mat spread on the floor with a small worn kneeling hollow the size of a child, a jackfruit-wood fish-shaped temple block on a low stool at the left with its mallet lying beside it, a votive-burning basin, a low rear door in the far left corner wedged shut by a timber bar, a hand-copied prayer book with purple ink tilted at the altar's edge. FX LAYER — smoke from three joss sticks rising straight then bending sideways halfway up, dust suspended in the lamp beam, heaviest vignette of the chapter.
Format: 1920x1080, 16:9, flat orthographic front elevation, locked camera, altar centred, seventeen interactive props arranged in three readable columns left / centre / right with at least 20px empty space between neighbours, every prop fully inside frame with an 80px safe margin top and bottom, no characters, no people, no hands, no ghosts, no legible text, delivered as four separate layers BACKGROUND / MIDGROUND / FOREGROUND / FX on transparent PNG.
```

**Negative prompt**

```plaintext
NEG-CORE, Chinese temple interior, Buddha statue, golden Buddha, red Chinese couplets, incense sticks burning brightly, bright candles, tidy clean altar, symmetrical perfectly aligned incense bowl, people praying, monk, ghost figure at the altar, face in the portrait frames, readable Chinese calligraphy, warm cosy lighting
```

Aspect ratio: **16:9 — 1920 x 1080**

**Midjourney (đuôi tham số)**

```plaintext
--ar 16:9 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179614 --chaos 0 --no people, monk, Buddha statue, ghost, bright candles, tidy altar, Chinese temple, readable calligraphy, text, 3D render, photorealistic
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 34 | CFG 6.5 | Seed 179614 | Size 1024x576 -> Hires Latent 1.5x denoise 0.38 -> 1920x1080
ControlNet lineart weight 0.60 (area đông hotspot nhất, cần siết chặt hơn), ảnh điều khiển = sketch dựng lại từ bản phác 03_world.md §1.3.1
LoRA linhanthon_style_v1 : 0.75 | Clip skip 2
```

**Chốt bố cục (17 hotspot — `03_world.md` §1.3.2). Bốn chỗ dễ sai nhất:**

- **Bát hương phải lệch 45°** so với hoành phi (`hs_bat_huong` `{1330,520,150,150}`). Đây là điềm nặng nhất trong tín ngưỡng Bắc Bộ — hoạ sĩ vẽ thẳng hàng là **hỏng cả beat B05a**.
- **Khám thờ Bà Cô** (`hs_kham_tho_ba_co` `{110,240,290,240}`) phải **thấp hơn bát hương gia tiên một tấc** và **bịt kín bằng vải điều**, không ảnh, không tên, không bát hương riêng.
- **Khe mộng cửa gác** (vùng chạm `{430,115,150,120}`, **nét vẽ** `{430,120,150,110}`) là một **khe rỗng hình chữ nhật** ngay trên khuôn cửa gác — phải nhìn ra ngay là "thiếu một thanh then".
- Hai hotspot **chỉ hiện sau khi giải câu đố** (`hs_bai_vi_khuyet_danh` `{130,500,250,120}`, `hs_dai_vai_dieu` vùng chạm `{130,635,250,120}` / **nét vẽ** `{130,640,250,110}`) cần **vẽ riêng thành lớp bật/tắt**, không nung vào nền.

---

## A4 · `bg_bep_gieng` — `area_bep_gieng` "Bếp tro và giếng khơi sau nhà"

*19h05. **Area tối nhất chương**: 70% khung hình là đen tuyền trong 2–3 phút đầu, độ sáng nền 18% cho tới khi người chơi thắp được đèn. Cửa liếp tre chia đôi khung hình ở x ≈ 1170: trái là bếp (trong nhà), phải là sân sau (ngoài trời). Dải x 1150–1200 là **vùng trung tính không có hotspot** — người chơi đọc được ranh giới không gian chỉ bằng mắt.*

**Prompt**

```plaintext
2D hand-painted background plate for a point-and-click horror game — a Northern Vietnamese earth-floor ash kitchen and the brick draw-well in the back yard behind it at 19:05, the darkest scene of the chapter, a split-bamboo door panel cutting the frame vertically at fifty-eight percent width, the left half interior and almost pitch black, the right half open night air.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: BACKGROUND LAYER — left half, straw-and-mud plastered kitchen walls under a soot crust so thick it looks furred, low thatch roof; right half, night sky over the back yard, the black silhouette of an old bombax tree by the pond edge with bare branches reaching sideways and a row of joss-stick stubs planted at its foot, faint glimmer of pond water. MIDGROUND LAYER — a bamboo drying rack slung under the roof beams hung with a bundle of split kindling sticks, empty bottles and one old dismantled hurricane lamp, a cardboard-covered market notebook wedged between two rafters, a xoan-wood kitchen post bearing five knife notches cut at five different heights each with a year beside it, a plain wooden table pushed against the bamboo door panel with an old oil stain on its top, and on the right a brick draw-well with its rim at hip height and a mouth of solid black, a dented tin bucket hanging on a bamboo stake with a rope still visibly wet, and a line of knife-scratched characters on the inner face of the well rim almost filled with moss. FOREGROUND LAYER — a cast-iron three-legged trivet holding a lidded rice pot in the middle of the kitchen floor, a heap of husk-banked ash with live embers breathing red underneath, a glass bottle of kerosene stoppered with a twist of dried banana leaf standing against the post, on the left wall a soot patch at waist height with stick figures drawn by a child's fingertip, three large and one small crossed out, and next to it a few big lines written in charcoal in an adult hand, slippery mossy well kerb. FX LAYER — ambient brightness held at eighteen percent, embers pulsing red, mist rising off the well mouth, sparse fireflies in the back yard, a very faint cold blue sliver of light coming through the bamboo door panel.
Format: 1920x1080, 16:9, flat orthographic front elevation, locked camera, vertical split at fifty-eight percent width with a neutral empty strip fifty pixels wide on the boundary, seventy percent of the frame in darkness but every prop still silhouette-readable, every interactive prop fully inside frame with an 80px safe margin top and bottom, no characters, no people, no hands, no ghosts, nothing climbing out of the well, no text, delivered as four separate layers BACKGROUND / MIDGROUND / FOREGROUND / FX on transparent PNG.
```

**Negative prompt**

```plaintext
NEG-CORE, long-haired ghost climbing out of the well, pale hand on the well rim, face in the water, Sadako, Ringu, wet white dress, bright kitchen, modern gas stove, tiled floor, electric light bulb, cheerful farmhouse, full moon, starry sky, people, silhouette in the doorway
```

> **Cảnh báo riêng cho A4:** đây là prompt **dễ hỏng nhất cả bộ**. Mô hình nhìn thấy "giếng + đêm + horror" là tự động vẽ Sadako. Negative về giếng **không được rút gọn** ở bất kỳ lần sinh nào. Theo quyết định đã chốt của tổ kinh dị, giếng của Linh An **cố ý không có gì trèo lên** — xem §1.5 của chính tài liệu này (danh sách CẤM tuyệt đối, dòng đầu tiên).

Aspect ratio: **16:9 — 1920 x 1080**

**Midjourney (đuôi tham số)**

```plaintext
--ar 16:9 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179615 --chaos 0 --no ghost, Sadako, long hair, pale hand, face in water, people, bright light, modern kitchen, full moon, text, 3D render, photorealistic
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 34 | CFG 6.5 | Seed 179615 | Size 1024x576 -> Hires Latent 1.5x denoise 0.38 -> 1920x1080
ControlNet lineart weight 0.55, ảnh điều khiển = sketch dựng lại từ bản phác 03_world.md §1.4.1
LoRA linhanthon_style_v1 : 0.75 | Clip skip 2
Ghi chú: xuất thêm bản "đã thắp đèn" — cùng seed, sửa prompt thành ambient brightness fifty-five percent within one oil-lamp halo radius 520px, đặt tên bg_bep_gieng_lit_*
```

**Chốt bố cục (14 hotspot — `03_world.md` §1.4.2):**

- Mọi hotspot "trong bếp" có `x + width ≤ 1150`; mọi hotspot "ngoài sân sau" có `x ≥ 1200`.
- `hs_gieng_khoi` `{1300,520,460,420}` là hotspot **to nhất area** — miệng giếng phải chiếm khối lớn rõ ràng vì người chơi sẽ chạm nó trong điều kiện màn hình tối.
- Cột bếp năm vạch dao `hs_cot_bep_vach_dao` `{680,420,130,520}` là cột **dọc cao**, năm vạch ở năm độ cao khác nhau, **vạch thứ năm phải trống** (không có năm kèm bên cạnh).
- Hình que trên vách bồ hóng `hs_vach_bo_hong_hinh_ve` `{60,420,180,300}`: **ba hình lớn, một hình nhỏ bị gạch chéo**.

---

## A5 · `bg_gac_xep` — `area_gac_xep` "Gác xép thờ Bà Cô"

*19h40. Gác gỗ thấp, **không đứng thẳng người được** — khung hình bị ép dẹt theo chiều dọc, mép trên là đòn tay và mái ngói. Nguồn sáng duy nhất là cây đèn dầu trong tay người chơi: toàn area dùng ánh sáng động bám con trỏ, bán kính ~520px, ngoài quầng là **nâu tối chứ không đen tuyền** để mắt người chơi luôn cố nhìn ra thứ gì đó. Cột trái = bằng chứng giấy tờ, cột giữa = hình nhân, cột phải = đồ nghi lễ.*

**Prompt**

```plaintext
2D hand-painted background plate for a point-and-click horror game — a low wooden loft above the ancestral altar of a Northern Vietnamese house at 19:40, too low to stand up in, packed with votive paper goods, lit only by a single oil lamp the player carries so most of the room falls away into warm dark brown rather than black.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: BACKGROUND LAYER — underside of flat lotus-tip (mui hai) clay roof tiles laid in overlapping fish-scale courses, sooted battens and low timber purlins pressing down on the top of the frame, heavy cobwebs, one thin blade of light coming up through a gap in the floorboards. MIDGROUND LAYER — dead centre stands a life-sized substitute effigy woven from bamboo splints and pasted over with do paper, its face drawn in ink as two dots and one stroke, standing with its back to the ladder hatch; on the right a large portrait frame turned to face the wall, its back fitted with nine sliding wooden panels in a three-by-three track with one empty slot exactly where a face should be; further right a full-sized paper wedding dress in votive red hanging on a wooden hook behind the frame, its hem still flat and uncreased, its shoulders sagging very slightly as if someone tried it on; a chest-high stack of votive paper goods in the right corner, paper horse, paper hat and robe, paper house, all brand new. FOREGROUND LAYER — a big wooden chest in the lower left with its lid open and turned up, the inside of the lid covered in dense ink writing, a brown-covered ruled register and a blue diary lying on the lid weighted by a brick, an old birth certificate in a plastic sleeve, a brand-new sedge mat laid out neatly on the floor below the effigy with a coin holding each corner, floorboards with a visible gap, a gaping ladder hatch in the far left corner dropping into darkness. FX LAYER — a soft oil-lamp halo about 520 pixels across, heavy paper dust suspended inside the halo, everything outside the halo reading as dark warm brown at ninety-four percent, faint rustle-implying motion on the votive paper.
Format: 1920x1080, 16:9, flat orthographic front elevation, locked low camera, frame vertically compressed to feel cramped, three readable columns left evidence / centre effigy / right ritual goods, every interactive prop fully inside frame with an 80px safe margin top and bottom, no people, no hands, no ghosts, no faces other than the ink two-dots-one-stroke on the effigy, no text, delivered as four separate layers BACKGROUND / MIDGROUND / FOREGROUND / FX on transparent PNG.
```

**Negative prompt**

```plaintext
NEG-CORE, yin-yang clay roof tiles, tube-and-pan roof tiles, Chinese temple roof underside, creepy porcelain doll, mannequin, wax figure, realistic human face on the effigy, detailed facial features, Chinese paper offering shop, bright attic, daylight through a window, cobweb cliche with giant spider, people, ghost bride with a real face, white wedding dress, western wedding gown
```

> **Ghi chú quan trọng:** hình nhân thế mạng **nằm trong bản nền** (nó là vật thể có thật, ở đó suốt phần còn lại của chương sau `scare_hinh_nhan_chan_loi`). Bản cận cảnh dùng cho cú doạ là sprite riêng — xem **C7**. Áo cưới giấy trong nền là **bản treo trên móc**; bản khoác lên hình nhân là sprite riêng — xem **C8** và **C10**.

Aspect ratio: **16:9 — 1920 x 1080**

**Midjourney (đuôi tham số)**

```plaintext
--ar 16:9 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179616 --chaos 0 --no yin yang roof tiles, tube and pan tiles, curved Chinese eaves, realistic face, porcelain doll, mannequin, people, ghost, white wedding gown, bright attic, daylight, giant spider, text, 3D render, photorealistic
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 34 | CFG 6.5 | Seed 179616 | Size 1024x576 -> Hires Latent 1.5x denoise 0.38 -> 1920x1080
ControlNet lineart weight 0.55, ảnh điều khiển = sketch dựng lại từ bản phác 03_world.md §1.5.1
LoRA linhanthon_style_v1 : 0.75 | Clip skip 2
Ghi chú: lớp _l3_fx xuất RIÊNG quầng đèn dạng radial alpha 520px để engine gắn theo con trỏ, KHÔNG nung quầng sáng vào _l1_mid
```

**Chốt bố cục (11 hotspot — `03_world.md` §1.5.2). Hai chỗ dễ sai:**

- `hs_ao_cuoi_giay` `{1650,200,230,370}` **chỉ hiện sau khi giải `puz_xep_anh_gia_pha`** → vẽ thành lớp bật/tắt riêng, nền mặc định là **móc gỗ trống sau lưng khung ảnh**.
- `hs_hinh_nhan` `{820,280,290,620}` kết thúc ở `y = 900`; `hs_chieu_coi_trai_san` có **vùng chạm** `{730,901,440,120}` bắt đầu ngay ở `y = 901` — **cách nhau đúng 1 px**, cặp sát nhất toàn chương. **Nhưng phần VẼ của chiếu vẫn là `{730,910,440,88}`** (`visual_bounds`), tức mép trên nét vẽ vẫn cách chân hình nhân 10 px. **Hoạ sĩ vẽ theo `visual_bounds`, không vẽ theo vùng chạm.** Phải giữ ranh giới chân hình nhân / mép chiếu thật rõ, đừng vẽ tà giấy tràn xuống chiếu.

---

# 4. MỤC B — PROMPT ZOOM CẬN CẢNH GIẢI ĐỐ

**6 prompt riêng biệt, mỗi câu đố một prompt.** Khung zoom, kích thước phần tử và vùng chạm lấy nguyên từ `02_puzzle.md`.

> **Luật chung của MỤC B — đọc trước khi sinh tấm đầu tiên:**
> 1. Mỗi câu đố xuất **hai file**: `_plate` (nền tĩnh, không có phần tử thao tác được) và `_parts` (atlas các phần tử rời, nền trong suốt). Nếu vẽ dính vào nhau thì không lập trình được.
> 2. **Không vẽ UI.** Nút bấm, thanh nhịp, ô chiếu lễ do tổ UI dựng bằng 9-slice. Prompt chỉ mô tả **chỗ trống đã chừa sẵn** cho chúng.
> 3. **Mỗi phần tử thao tác được phải ≥ 120 x 120 px @1920** — sàn chạm chính thức của dự án (`01_KICH_BAN_CHAPTER_01.md` §6 mục X18, `docs/03_DATA_SPEC.md` §2.2 mức G3). **Ngưỡng 88 px của bản cũ đã bị bãi bỏ** vì quy đổi *"88 px ≈ 44 pt"* là sai số học: fit-width cho ra 29–43 pt/dp, dưới cả Apple HIG lẫn Material. Phần tử còn phải có silhouette phân biệt được **khi nhìn ở 30% độ sáng** — vì Area 4 và Area 5 tối.
>
>    **Một ngoại lệ, và chỉ một:** **bề rộng NÉT** trong `B2 · PATTERN_TRACE` là **≥ 44 px**, không phải 120 px. Nét là **đường vuốt**, không phải mục tiêu chạm: ngón tay bám theo nét chứ không phải bấm trúng nó một lần. Sàn 120 px áp cho **mục tiêu chạm rời rạc** — nút, icon, ô, phần tử kéo-thả. Mọi con số khác của MỤC B đều đã ở trên sàn: B1 vành 800/600/400, B3 icon 150×150, B5 phần tử ≥ 160×160, B6 ô 280×280.
> 4. Ánh sáng zoom **kế thừa ánh sáng của area mẹ**, không được đột ngột sáng lên chỉ vì đang "cận cảnh".

---

## B1 · `zoom_puz_khoa_bat_quai` — `ROTATION_LOCK` · Ổ khoá gỗ tám quẻ (`area_san_gach`)

*Khung zoom `{x:560, y:140, width:800, height:800}`. Ba vòng đồng tâm Ø760 / Ø520 / Ø300 px, mỗi vòng 8 nấc, mỗi nấc một quẻ Bát quái kèm một chữ số Hán (一…八) khắc chìm. Rãnh chỉ đỏ thẳng đứng ở 12 giờ là "khe đọc". Then gỗ giữa `{900,480,120,120}` trong khung zoom là nút xác nhận. Lời giải `[6,3,8]` = Khảm / Ly / Khôn.*

**Prompt**

```plaintext
2D hand-painted close-up puzzle plate for a point-and-click horror game — a hand-carved wooden combination padlock of three concentric rotating rings clamped between the leaves of an old Vietnamese village gate, seen straight on at arm's length in wet twilight.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: three concentric wooden discs of aged dark jackfruit wood centred in frame, outer disc 760 pixels across, middle disc 520 pixels, inner disc 300 pixels, each disc divided into exactly eight equal notches by shallow carved grooves, each notch bearing one incised eight-trigram symbol of three broken or unbroken bars plus one small incised Han numeral beside it, the carving worn and grey with rain, a vertical red-lacquer index groove painted at the twelve o'clock position of the outer rim marking the reading slot, a square wooden bolt in the dead centre 120 pixels across with a finger-polished dip in the middle, iron staples and a weathered gate-leaf edge visible left and right, moss in the wood grain, one dried water trail running down across the discs. Lighting inherits the courtyard dusk: cold violet fill #3A3F55 from above, a single weak warm bounce from the right.
Format: 1920x1080, 16:9, flat orthographic dead-on view, lock centred, wooden gate surface filling the rest of the frame, no UI, no buttons, no arrows, no numbers rendered in Arabic digits, no hands, no people, no text; deliver as two files — a static plate with the three discs removed, and a transparent-background parts atlas containing the three discs and the central bolt as separate rotatable elements with their pivot at the exact disc centre.
```

**Negative prompt**

```plaintext
NEG-CORE, metal padlock, modern combination lock, brass dial safe, Chinese feng shui compass luopan, yin yang symbol, colourful trigram chart, arrows, glowing runes, magic circle, UI buttons, Arabic numerals, hands turning the dial, motion blur
```

Aspect ratio: **16:9 — 1920 x 1080** (phần tử thao tác nằm gọn trong `{560,140,800,800}`)

**Midjourney (đuôi tham số)**

```plaintext
--ar 16:9 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179621 --chaos 0 --no metal lock, feng shui compass, yin yang, glowing runes, arrows, UI, hands, text, 3D render, photorealistic
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 34 | CFG 6.5 | Seed 179621 | Size 1024x576 -> Hires Latent 1.5x denoise 0.38 -> 1920x1080
ControlNet lineart weight 0.70 (hình học tròn đồng tâm, phải siết rất chặt) — ảnh điều khiển = ba đường tròn Ø760/520/300 chia 8 nấc dựng bằng vector
LoRA linhanthon_style_v1 : 0.75 | Clip skip 2
```

**Yêu cầu xuất riêng:** 8 quẻ phải vẽ **rời thành 8 sprite nhỏ** (`zoom_puz_khoa_bat_quai_parts` ô 1–8) để engine xoay vòng mà không phải xoay cả ảnh — nếu không, chữ số Hán sẽ bị lộn ngược khi vòng quay 180°.

---

## B2 · `zoom_puz_rap_chu_the_menh` — `PATTERN_TRACE` · Rập chữ trên bình phong (`area_hien_nha`)

*Khung rập chia hai ô dọc: ô trên chữ "Thế" 世, ô dưới chữ "Mệnh" 命, mỗi chữ vẽ theo lối chân giản lược **4 nét**. Trên giấy chỉ hiện **8 vệt mờ** (bóng nét gỗ hằn qua giấy). **Ràng buộc mỹ thuật bắt buộc: mỗi nét rộng tối thiểu 44px** để vừa đầu ngón tay. Lời giải `[2,1,4,3,7,5,8,6]`.*

**Prompt**

```plaintext
2D hand-painted close-up puzzle plate for a point-and-click horror game — a sheet of thin Vietnamese do paper laid flat over the worn face of a dark wooden screen, ready for a charcoal rubbing, lit by the last cold light of dusk on a veranda.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: a single sheet of fibrous cream do paper #D9C9A3 fills the centre of the frame, its edges deckled and slightly curling, the dark grain of the jackfruit-wood screen showing faintly through, the paper area divided into two stacked square cells, upper cell and lower cell, and inside each cell exactly four extremely faint depressed stroke shadows pressed up through the paper from the carving beneath, so eight pale ghost strokes total, every stroke rendered as a broad simplified regular-script brush stroke at least forty-four pixels wide with a clear start end and direction, none of them yet blackened; a sharpened charcoal stick rests along the bottom edge of the paper, its tip already blunted and shining; two more blank sheets of do paper wait in a small stack at the lower left corner; a rusty thumbtack pins each top corner of the sheet to the wood. Lighting inherits the veranda: cold blue wash from the left, a warm seam of orange light from the door on the right just grazing the paper edge, deep shadow around the frame.
Format: 1920x1080, 16:9, flat orthographic dead-on view, paper centred and filling seventy percent of the frame, strokes faint but unmistakably readable in silhouette, no UI, no buttons, no numbered order markers, no finished black characters, no hands, no people, no legible modern text; deliver as two files — a static plate showing the blank paper with only the faint depressions, and a transparent-background parts atlas containing the eight blackened charcoal strokes as separate elements aligned to the same coordinates.
```

**Negative prompt**

```plaintext
NEG-CORE, finished calligraphy, bold black Chinese characters already written, ink brush painting, red seal stamp, gold ink, rice paper scroll hanging, glowing strokes, numbered arrows showing stroke order, hands holding charcoal, modern pencil, clean white paper
```

Aspect ratio: **16:9 — 1920 x 1080**

**Midjourney (đuôi tham số)**

```plaintext
--ar 16:9 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179622 --chaos 0 --no finished calligraphy, bold black characters, red seal, glowing strokes, arrows, hands, UI, 3D render, photorealistic
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 34 | CFG 6.5 | Seed 179622 | Size 1024x576 -> Hires Latent 1.5x denoise 0.38 -> 1920x1080
ControlNet lineart weight 0.75 — ảnh điều khiển = 8 nét chữ 世 / 命 dựng bằng vector, mỗi nét đã đánh số 1..8 theo solution [2,1,4,3,7,5,8,6]
LoRA linhanthon_style_v1 : 0.75 | Clip skip 2
```

**Yêu cầu xuất riêng:** mỗi nét trong `_parts` phải có **hai trạng thái** — `_ghost` (vệt mờ chưa ăn than) và `_inked` (đen đậm đã ăn than) — cùng toạ độ, để engine chỉ đổi alpha.

---

## B3 · `zoom_puz_tuan_tu_le_cung` — `SEQUENCE_ORDER` · Một tuần lễ cúng (`area_gian_tho`)

*Mặt bàn thờ bày lộn xộn sau đám tang. **6 lễ vật/thao tác** dạng icon gỗ ~150x150px rải trên mặt bàn; phía dưới là **dải 6 ô vuông trống** `{x:360, y:830, width:1200, height:170}` (mỗi ô 190x170, cách nhau 12px) — "chiếu lễ". Nút "Vái" ở `{1620,860,220,120}`. Lời giải `[3,6,4,1,5,2]`.*

**Prompt**

```plaintext
2D hand-painted close-up puzzle plate for a point-and-click horror game — the cluttered top of a Northern Vietnamese clan ancestral altar photographed straight down the axis, still half-cleared from a funeral, with a bare woven mat area waiting at the bottom of the frame.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: the lacquered altar surface fills the upper two thirds of the frame, worn black lacquer with flaking gold at the edges, scattered across it in no order are six ritual objects each fitting a 150 by 150 pixel square and each with a completely distinct silhouette — a folded cleaning cloth beside a small offering tray, a pair of squat brass oil lamps, a bundle of three joss sticks, a small wine ewer with three tiny cups, a hand-copied prayer book open with purple ink, and a folded stack of gold votive paper ready for burning; behind them the crazed-glaze incense bowl still sitting rotated out of line, an upturned rice bowl with a halved boiled egg, a fruit tray pushed off centre; the lower third of the frame is deliberately clear and empty, showing only a plain sedge ritual mat surface with six faint rectangular impressions in the weave where objects are meant to be set down. Lighting inherits the altar room: one weak warm lamp from the left, dead cold from the right, smoke haze crossing the top.
Format: 1920x1080, 16:9, flat orthographic dead-on view, six ritual objects readable as six distinct silhouettes at thirty percent brightness, the bottom strip from y 830 to y 1000 kept visually empty for the UI tray, no UI, no buttons, no numbers, no arrows, no hands, no people, no legible text; deliver as two files — a static plate of the altar with the six objects removed, and a transparent-background parts atlas with the six objects as separate draggable elements, each on its own 190 by 170 pixel cell with pivot at cell centre.
```

**Negative prompt**

```plaintext
NEG-CORE, Chinese ancestor shrine, Buddha statue, tidy symmetrical offering setup, bright fresh flowers, burning incense with visible flame, red and gold festive decoration, numbers on objects, arrows, glowing outlines, hands placing offerings, top-down perspective distortion
```

Aspect ratio: **16:9 — 1920 x 1080**

**Midjourney (đuôi tham số)**

```plaintext
--ar 16:9 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179623 --chaos 0 --no Buddha, tidy altar, festive red gold, burning flame, numbers, arrows, glowing outline, hands, UI, 3D render, photorealistic
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 34 | CFG 6.5 | Seed 179623 | Size 1024x576 -> Hires Latent 1.5x denoise 0.38 -> 1920x1080
ControlNet lineart weight 0.60 — ảnh điều khiển = 6 ô 150x150 rải trên mặt bàn + dải 6 ô trống ở đáy khung
LoRA linhanthon_style_v1 : 0.75 | Clip skip 2
```

**Yêu cầu xuất riêng:** 6 icon phải phân biệt **bằng hình bóng**, không bằng màu — 12% người chơi nam mù màu đỏ-lục, và area này tối.

---

## B4 · `zoom_puz_ba_hoi_chin_tieng` — `AUDIO_MATCH` · Ba hồi chín tiếng (`area_gian_tho`)

> **⚠️ HOÁN VAI NHẠC KHÍ — X14, đã chốt. Bản trước của mục B4 vẽ NGƯỢC.** Bản trước đặt **mõ cá** vào ô lớn `{520,420,520,420}` và **chuông** vào ô nhỏ `{1240,380,260,260}`, đồng thời khắc ba chữ số Hán lên thân mõ. **Sai cả ba chỗ.** Theo `01_KICH_BAN_CHAPTER_01.md` §3.3.6: **CHUÔNG ĐỒNG** mang trọn phần *"ba hồi chín tiếng"* nên nó là **nhạc khí chính, chiếm ô LỚN**; **MÕ** chỉ điểm **một tiếng chốt mỗi hồi**, ba lần trong cả bài, nên nó là **nhạc khí phụ, ô NHỎ**; và **ba chữ 三 五 七 khắc trên VÀNH CHUÔNG**, không khắc trên mõ — vì chuông mới là thứ mang ba con số ấy (clue C2). `solution` `[3,3,5,3,7,3]` **không đổi một chữ số nào**.

*Chỉ **hai nút gõ**: **chuông đồng nhỏ treo trên giá gỗ chữ U** `{520,420,520,420}` *(nhạc khí chính, chiếm phần lớn khung)* và **mặt mõ cá** `{1240,380,260,260}` *(chỉ dùng đúng ba lần cả bài)*. Thanh nhịp chạy ngang phía trên `{360,180,1200,90}`. Nút "Áp tai vào vách" `{1620,180,220,120}`. Nền là vách buồng trống — nơi **tiếng chuông** vọng ra, mỗi hồi khép lại bằng một tiếng mõ cụt lủn. Lời giải `[3,3,5,3,7,3]` — **cả sáu số đều là số tiếng CHUÔNG**.*

**Prompt**

```plaintext
2D hand-painted close-up puzzle plate for a point-and-click horror game — a small bronze temple bell hanging in a U-shaped wooden stand, with a jackfruit-wood fish-shaped temple block set beside it, in front of the cracked plank partition of an empty inner chamber, seen straight on in a very quiet dark ancestral room.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: left of centre and dominating the frame, a dark bronze temple bell hanging inside a U-shaped wooden stand on a low stool, unpolished and green-tarnished at the lip, three incised Han numerals cut into the outer rim of the bell with a clear gap between each one, the bronze rubbed bright in one small patch where it has been struck for decades; right of centre and much smaller, a carved wooden fish-shaped temple block resting directly on the same low stool, its lacquer worn to bare wood on the striking face, its mouth slot a deep black opening, no numerals and no carving on its flank; behind them the plank wall of the empty chamber, boards split into long vertical gaps with absolute darkness behind, one board rubbed pale and smooth at ear height where someone has leaned against it many times; a mallet-shaped hollow on the stool where the beater usually rests, currently empty; dust on every horizontal surface except the striking face of the block and the struck patch of the bell. The top strip of the frame and the top right corner are deliberately left as plain dark wall with nothing on them. Lighting inherits the altar room: one weak warm lamp far left, the wall gaps reading colder than the wood, heavy vignette.
Format: 1920x1080, 16:9, flat orthographic dead-on view, bell and its wooden stand occupying roughly 520 by 420 pixels left of centre, temple block occupying roughly 260 by 260 pixels right of centre, the strip from y 180 to y 270 across the top kept visually empty for the UI rhythm bar, no UI, no buttons, no musical notation, no sound wave graphics, no hands, no people, no legible text apart from the three incised numerals on the bell rim; deliver as two files — a static plate of the wall and stool, and a transparent-background parts atlas containing the bell with its stand, the temple block and the mallet as separate elements.
```

**Negative prompt**

```plaintext
NEG-CORE, Chinese temple wooden fish with dragon carving, gold bell, Japanese mokugyo lacquered red, monk hands, prayer beads, musical notes, sound waves, equalizer bars, glowing impact effect, bright polished brass, clean new wood
```

Aspect ratio: **16:9 — 1920 x 1080**

**Midjourney (đuôi tham số)**

```plaintext
--ar 16:9 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179624 --chaos 0 --no dragon carving, gold bell, musical notes, sound waves, glowing impact, monk, hands, UI, 3D render, photorealistic
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 34 | CFG 6.5 | Seed 179624 | Size 1024x576 -> Hires Latent 1.5x denoise 0.38 -> 1920x1080
ControlNet lineart weight 0.60 — ảnh điều khiển = chuông + giá gỗ 520x420 trái, khối mõ 260x260 phải, dải trống 1200x90 phía trên
LoRA linhanthon_style_v1 : 0.75 | Clip skip 2
```

**Yêu cầu xuất riêng:** cần **2 khung phản hồi gõ** cho mỗi nút (`_idle`, `_hit`) — `_hit` chỉ khác ở **biến dạng 3% và một vòng bụi bật lên**, tuyệt đối **không phát sáng**. Game này không có vật thể phát quang.

**Cây dùi phải vẽ hai đầu khác nhau.** `item_dui_mo` là **một cây dùi dùng cho cả hai nhạc khí**: **một đầu quấn một lớp vải điều đã bạc — đầu ấy đánh CHUÔNG**, **đầu kia để trần — gõ MÕ**. Đây vừa là clue C4 của câu đố vừa là điều kiện mở khoá, nên hai đầu phải phân biệt được **ngay trong icon túi đồ** (`icon_item_dui_mo.png`, §C13) chứ không chỉ ở atlas `_parts`. Cán mòn nhẵn **đúng ba chỗ** — chỗ ngón cái, chỗ ngón trỏ, chỗ lòng bàn tay.

---

## B5 · `zoom_puz_thap_lai_den_dau` — `ITEM_COMBINE` · Thắp lại cây đèn Hoa Kỳ (`area_bep_gieng`)

*Cây đèn tháo rời nằm giữa khung `{760,380,400,520}`, **5 phần tử** xếp quanh (mỗi vùng chạm ≥ 160x160px): dải vải điều, tim đèn, chai dầu hoả, núm vặn, que đóm. Có thước nhỏ cạnh núm vặn với **vùng xanh** = mức tim đúng ("nhô khoảng một hạt gạo"). Lời giải `[2,5,1,3,4]`. Đây là area tối nhất — plate phải đọc được ở 18% độ sáng.*

**Prompt**

```plaintext
2D hand-painted close-up puzzle plate for a point-and-click horror game — a dismantled American-style kerosene hurricane lamp laid out on a plain wooden kitchen table in an almost pitch-dark Vietnamese earth-floor kitchen, the only light a bed of live embers off to one side.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: centre of frame, the lamp in pieces on a scarred wooden table top — a heavy glass fount with a measuring notch scratched on its side, a brass collar with an empty wick tube, a soot-blackened glass chimney standing separately, a small knurled wick-raising knob with a tiny scale beside it whose correct zone is marked by a scratch, everything matte and greasy with old oil; arranged around the lamp at the four corners and the bottom, five clearly separated objects each at least 160 by 160 pixels — a strip of faded red altar cloth, a twisted fibre wick half made, a glass bottle of kerosene stoppered with dried banana leaf, a split bamboo taper, and the knurled knob; at the right edge, a heap of husk-banked ash with red embers breathing under it, the only light source in frame, throwing a low raking orange glow across the table and leaving long soft shadows to the left; soot-furred wall behind, faint cold blue sliver from a bamboo door panel at the far right.
Format: 1920x1080, 16:9, flat orthographic dead-on view, lamp parts occupying roughly 400 by 520 pixels in the centre, five loose objects fully separated with at least 40px between them, everything still readable in silhouette at eighteen percent screen brightness, no UI, no buttons, no arrows, no step numbers, no flame yet, no hands, no people, no legible text; deliver as two files — a static plate of the table and embers, and a transparent-background parts atlas containing the fount, collar, chimney, knob, cloth strip, wick, kerosene bottle and taper as separate draggable elements.
```

**Negative prompt**

```plaintext
NEG-CORE, lamp already lit, bright flame, glowing lantern, romantic warm cosy light, clean polished brass lamp, antique shop display, modern camping lantern, electric bulb, candle, hands assembling, instruction diagram, exploded technical view with callout lines
```

Aspect ratio: **16:9 — 1920 x 1080**

**Midjourney (đuôi tham số)**

```plaintext
--ar 16:9 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179625 --chaos 0 --no lit lamp, bright flame, glowing, polished brass, candle, hands, diagram, callout lines, UI, 3D render, photorealistic
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 34 | CFG 6.5 | Seed 179625 | Size 1024x576 -> Hires Latent 1.5x denoise 0.38 -> 1920x1080
ControlNet lineart weight 0.65 — ảnh điều khiển = cây đèn 400x520 giữa + 5 ô 160x160 quanh
LoRA linhanthon_style_v1 : 0.70 | Clip skip 2
Ghi chú: xuất thêm bản _lit (cùng seed, thêm "wick lit, flame the size of a rice grain, halo radius 520px") dùng cho khoảnh khắc giải xong
```

**Yêu cầu xuất riêng:** ngọn lửa cuối cùng **cao đúng bằng một hạt thóc** (`03_world.md` §2, mô tả `item_den_dau_sang`). Vẽ ngọn lửa to là phá vỡ toàn bộ thiết kế ánh sáng của Area 4 và Area 5.

---

## B6 · `zoom_puz_xep_anh_gia_pha` — `SLIDING_TILE` · Bức ảnh thờ chín mảnh (`area_gac_xep`)

*Lật mặt sau khung ảnh, lộ **khung gỗ 3x3**, khung zoom `{660,120,840,840}`, mỗi ô **280x280px**. **8 mảnh ván + 1 ô trống**, ô trống **đúng chỗ khuôn mặt bị khoét**. Nút "Áp ảnh vào khung" `{1560,860,280,140}`. Đèn dầu đặt cạnh khung, quầng sáng chỉ phủ trung tâm. Lời giải `[2,5,7,4,8,3,6,1,0]`.*

**Prompt**

```plaintext
2D hand-painted close-up puzzle plate for a point-and-click horror game — the back of a large Vietnamese ancestral portrait frame turned face to the wall in a cramped loft, its backing rebuilt as a three by three wooden sliding track holding eight carved panels and one empty slot, lit only by an oil lamp standing on the floorboards beside it.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: a heavy dark wooden frame fills the centre of the composition, 840 by 840 pixels, divided into a three by three grid of 280 pixel cells by shallow routed runners worn shiny from sliding; eight thin wooden panels sit in the track, each carrying a fragment of one old sepia family memorial photograph pasted and varnished onto the wood — fragments of stiff collars, folded hands, a row of shoulders, the edge of an altar behind the group — the photo tone kept brown-grey and faded so no individual face is ever fully legible, the panel edges chipped and the varnish crazed; one cell is completely empty, showing bare backing board, and it sits exactly where a head would be; around the frame, loft floorboards, paper dust, a bamboo splint or two, and at the lower left the oil lamp itself with a rice-grain flame casting a halo that covers only the centre of the frame and lets the corner cells fall into warm dark brown; the lower right corner of the frame is kept clear and empty. Lighting inherits the loft: a single warm 520 pixel halo, ninety-four percent darkness outside it, dust suspended in the beam.
Format: 1920x1080, 16:9, flat orthographic dead-on view, sliding frame centred on the zoom rect x660 y120 840 by 840, every one of the nine cells readable, the strip at the lower right kept visually empty for the UI confirm button, no UI, no buttons, no numbers on the tiles, no arrows, no hands, no people, no ghost faces, no legible text; deliver as two files — a static plate of the empty wooden track and the loft around it, and a transparent-background parts atlas with the eight photo panels as separate 280 by 280 pixel tiles.
```

**Negative prompt**

```plaintext
NEG-CORE, clear sharp faces, recognisable portrait, smiling family photo, colour photograph, modern photo print, Chinese ancestor portrait with formal robe, ghost face appearing in the photo, glowing tile, numbered tiles, arrows, hands sliding tiles, bright even lighting
```

Aspect ratio: **16:9 — 1920 x 1080**

**Midjourney (đuôi tham số)**

```plaintext
--ar 16:9 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179626 --chaos 0 --no clear faces, smiling photo, colour photo, ghost face, glowing tile, numbers, arrows, hands, UI, 3D render, photorealistic
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 34 | CFG 6.5 | Seed 179626 | Size 1024x576 -> Hires Latent 1.5x denoise 0.38 -> 1920x1080
ControlNet lineart weight 0.80 (lưới 3x3 phải tuyệt đối vuông vắn, sai lưới là không trượt được) — ảnh điều khiển = lưới 3x3 ô 280px dựng vector
LoRA linhanthon_style_v1 : 0.70 | Clip skip 2
```

**Yêu cầu xuất riêng:**
- Bức ảnh gốc phải vẽ **một lần liền mạch ở 840x840** rồi **mới cắt** thành 9 ô — vẽ rời từng ô sẽ không bao giờ ghép khớp.
- Ô trống nằm đúng **chỗ khuôn mặt**: khi xếp xong, bức ảnh hoàn chỉnh **vẫn khuyết đúng một khuôn mặt**. Đây là cú chốt hình ảnh của cả chương, không được "vá" lại cho đẹp.
- Xuất thêm biến thể `zoom_puz_xep_anh_gia_pha_parts_khoet` — chín mảnh **mặt sau bị khoét thủng hình đầu người** — dùng cho `scare_anh_tho_thieu_mat` (xem **C9**).

---

# 5. MỤC C — PROMPT NHÂN VẬT & JUMP-SCARE SPRITE

**13 prompt riêng biệt.** Tất cả sinh trên **nền xám đặc `#808080`** để tách nền sạch.

## C0. Quy ước chung bắt buộc cho MỌI sprite ở MỤC C

| Quy tắc | Giá trị | Vì sao |
|---|---|---|
| **Nền** | `#808080` đặc, phẳng tuyệt đối | Xám trung tính không nằm trong bảng màu chương → không trùng với bất kỳ pixel nào của chủ thể, tách nền bằng ngưỡng màu là sạch. Nền trắng sẽ ăn mất giấy bản `#D9C9A3`, nền đen sẽ ăn mất bóng `#0E0F12`. |
| **Đổ bóng** | **Không** đổ bóng lên nền | Bóng xám lên nền xám = viền bẩn không tách được. Bóng tiếp đất do engine vẽ. |
| **Chừa mép** | ≥ 10% mỗi cạnh | Chống cụt khi scale / punch camera. |
| **Pivot** | vật đứng = `bottom-center`; vật quét/bay = `center` | Khớp §2.4 của tài liệu này và bảng 8 jump-scare ở `docs/06_AN_TOAN_NGUOI_CHOI.md` §4.4.1. |
| **Mặt ma** | **CẤM TUYỆT ĐỐI** | Không hốc mắt đen, không miệng hét, không mặt người thật. Chỉ được: **bóng phẳng**, **khói**, hoặc **mặt vẽ than hai chấm một vạch** trên giấy. |
| **Phát sáng** | **Cấm** vật thể tự phát quang | Nguồn sáng duy nhất của game là đèn dầu và than hồng, đều diegetic. |
| **Biến thể bắt buộc** | `_soft` (biên độ scale ≤ 1.04, tốc độ 60%) và `_static` (một khung kết quả, không animation) | Chế độ an toàn `gentle_mode` / `reduce_motion` / `scare_intensity = 0`. **Hợp đồng đặt tên và nội dung biến thể: `docs/06_AN_TOAN_NGUOI_CHOI.md` §4.3; bảng đối chiếu mặc định ↔ `gentle_mode` cho từng cú doạ: §4.4.** Thiếu một file biến thể = engine rơi về bản gốc = người chơi bật chế độ an toàn vẫn ăn nguyên cú doạ đầy đủ → **chặn build**. **Không tài sản an toàn nào được đặt sau tường trả phí** (§1 của `docs/06`). |

**Dòng `Format:` dùng chung cho 13 prompt (đã nhúng sẵn trong từng prompt, ghi ở đây để đối chiếu):**

```plaintext
centred on a flat solid #808080 grey background, no cast shadow on the background, no gradient, no vignette, no ground plane, subject fully inside frame with a ten percent margin on every side, clean hard alpha edge ready for background removal, no text, no UI, no watermark
```

---

## C1 · `spr_bong_khan_xo` — Bóng khăn xô trong chum nước (S1, `scare_bong_trong_chum`)

*`area_san_gach` · `ON_PUZZLE_FAIL_COUNT` max_fails 3 · `screen_flash: true` · `anim_bong_khan_xo_trong_chum`. Bóng người **không bao giờ tiến về phía camera** — nó chỉ đứng. Cái giật đến từ gáo dừa; cái lạnh ở lại đến từ việc có người đứng sau lưng suốt lúc đó mà ta không biết.*

**Prompt**

```plaintext
2D hand-painted game sprite for a point-and-click horror game — the reflection of a person standing in white mourning headcloth, seen as a flat dark silhouette on black rainwater, meant to be composited under a water-surface layer inside a stoneware jar.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: a single standing human silhouette rendered almost entirely as flat near-black #0E0F12 with only the coarse white mourning headcloth reading as a slightly paler wrapped shape around the head #F2EDE3 at twenty percent opacity, arms hanging straight down, shoulders level, absolutely motionless, no facial features at all, no eyes, no mouth, nothing but the outline; the silhouette is slightly wider and softer at the edges as a reflection in still water would be, with a faint horizontal ripple distortion across it; it must read correctly when composited under a dark water layer at 85 percent opacity.
Format: 2D sprite sheet of 6 frames showing only a fade-in from alpha 0 to alpha 0.85 over 60 milliseconds and then complete stillness, no walking, no approaching, no turning; centred on a flat solid #808080 grey background, no cast shadow on the background, no gradient, no vignette, no ground plane, subject fully inside frame with a ten percent margin on every side, clean hard alpha edge ready for background removal, no text, no UI, no watermark.
```

**Negative prompt**

```plaintext
NEG-CORE, visible face, eyes, glowing eyes, mouth, teeth, long hair, hair over face, reaching hands, figure walking toward camera, white ghost dress, transparent wispy ghost, Sadako, horror movie ghost, detailed clothing folds, cast shadow, background scenery
```

Aspect ratio: **1:1 — 1024 x 1024 / khung**

**Midjourney (đuôi tham số)**

```plaintext
--ar 1:1 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179631 --chaos 0 --no face, eyes, mouth, long hair, hands, white dress, Sadako, shadow, background, text
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 28 | CFG 7.0 | Seed 179631 | Size 1024x1024 | Hires Latent 1.5x denoise 0.30
LoRA linhanthon_style_v1 : 0.65 | Clip skip 2 | Tách nền: ngưỡng màu #808080, tolerance 12, feather 1px
```

**File xuất:** `spr_bong_khan_xo_f00..f05.png` → `anim_bong_khan_xo_trong_chum.png` + `_soft` + `_static`. Kèm sprite phụ cùng bộ: **`spr_nuoc_vo`** (mặt nước vỡ tan, 8 khung, dùng làm **mask cut** xoá bóng ở mốc 200ms — sinh bằng chính prompt này, thay Details thành *"a splash of black rainwater breaking apart, concentric shatter ripples, no figure"*).

---

## C2 · `spr_ban_tay_vang_ma` — Bàn tay vàng mã quét ngang mặt kính (S2, `scare_ban_tay_giay_sau_manh`)

*`area_hien_nha` · `ON_COLLECT_ITEM` (`item_ban_rap_chu_the`) · `screen_flash: true` · `anim_ban_tay_vang_ma_quet`. Chỉ hiện diện **130 ms** — mắt thấy, não không kịp phân tích. Quét từ mép phải sang, scale 1.0 → 1.45, vận tốc 2.400 px/s.*

**Prompt**

```plaintext
2D hand-painted game sprite for a point-and-click horror game — a dry votive-paper hand, a hand cut and pasted from joss paper the way funeral paper effigies are made, sweeping horizontally across the very front of the camera.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: a flat hand and forearm built from layered votive paper, pale straw-yellow and faded gold leaf #D9C9A3 and #C9A227, the fingers stiff and slightly splayed with visible paste seams and fibre edges, one fingertip already torn and curling, the paper creased where a joint would be, no skin, no nails, no flesh tone whatsoever, absolutely no realistic anatomy; the hand enters from the right edge so the composition is heavily weighted right, motion implied by trailing paper scraps and a single ghost-edge streak, no motion blur filter.
Format: 2D sprite sheet of 8 frames showing the hand entering from the right edge, crossing the frame while scaling from 1.0 to 1.45, and exiting left within 130 milliseconds, plus 3 extra frames of loose votive paper scraps drifting after it; centred on a flat solid #808080 grey background, no cast shadow on the background, no gradient, no vignette, no ground plane, subject fully inside frame with a ten percent margin on every side, clean hard alpha edge ready for background removal, no text, no UI, no watermark.
```

**Negative prompt**

```plaintext
NEG-CORE, realistic human hand, skin texture, fingernails, veins, flesh tone, zombie hand, rotting hand, claws, blood, motion blur filter, radial blur, glowing hand, cast shadow, background scenery
```

Aspect ratio: **16:9 — 1408 x 792 / khung**

**Midjourney (đuôi tham số)**

```plaintext
--ar 16:9 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179632 --chaos 0 --no realistic hand, skin, fingernails, flesh, zombie, claws, blood, motion blur, glowing, shadow, background, text
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 28 | CFG 7.0 | Seed 179632 | Size 1344x768 | Hires Latent 1.5x denoise 0.30
LoRA linhanthon_style_v1 : 0.65 | Clip skip 2 | Tách nền: ngưỡng #808080, tolerance 12
```

**File xuất:** `anim_ban_tay_vang_ma_quet.png` + **`anim_ban_tay_vang_ma_quet_soft.png`** (bắt buộc: scale ≤ 1.04, tốc độ 60% — đây là biến thể `_soft` duy nhất được `docs/06_AN_TOAN_NGUOI_CHOI.md` §4.4.2 gọi tên đích danh: bàn tay quét ở **mép phải màn hình**, không quét sát mặt kính) + `_static`.

---

## C3 · `spr_chan_nhang_chay` — Bó chân nhang bốc cháy một nhịp (S3, `scare_di_anh_quay_mat`)

*`area_gian_tho` · `ON_COLLECT_ITEM` (`item_dui_mo`) · `screen_flash: false`. Lửa cam, **cao 180 px**, ramp 0 → đỉnh trong 180 ms (chậm hơn flash nên không kích hoạt phản xạ nhạy sáng), vùng sáng phủ ≤ 30% màn hình quanh `(960, 520)`.*

**Prompt**

```plaintext
2D hand-painted game sprite for a point-and-click horror game — a dense bundle of old dry joss-stick stems standing in a ceramic incense bowl, catching fire all at once in a single upward flare.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: a thick packed bundle of thin bamboo joss-stick stems, their lower ends dyed the dull dark red of old incense, packed so tightly they lean as one mass, planted in grey ash inside a crazed-glaze ceramic bowl; the flame is hand-painted in flat orange and amber shapes about 180 pixels tall, tapering, with visible brush edges rather than soft glow, a little black smoke curling off the tips, a few stems already blackening and shrinking; the fire must look like dry sticks catching, not like a magical effect, no sparks shower, no embers flying, no light bloom.
Format: 2D sprite sheet of 10 frames — 3 frames of the bundle leaning 2 degrees further before ignition, 4 frames of the flare rising over 180 milliseconds, 3 frames of it dying back to blackened stems; centred on a flat solid #808080 grey background, no cast shadow on the background, no gradient, no vignette, no ground plane, subject fully inside frame with a ten percent margin on every side, clean hard alpha edge ready for background removal, no text, no UI, no watermark.
```

**Negative prompt**

```plaintext
NEG-CORE, magical fire, blue flame, green flame, fireball, explosion, sparks shower, light bloom, lens glow, realistic fire photography, campfire, candle, torch, Chinese incense burner with dragons, gold censer, cast shadow, background scenery
```

Aspect ratio: **1:1 — 1024 x 1024 / khung**

**Midjourney (đuôi tham số)**

```plaintext
--ar 1:1 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179633 --chaos 0 --no magical fire, blue flame, fireball, sparks, bloom, lens glow, dragons, gold censer, shadow, background, text
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 28 | CFG 7.0 | Seed 179633 | Size 1024x1024 | Hires Latent 1.5x denoise 0.30
LoRA linhanthon_style_v1 : 0.65 | Clip skip 2 | Tách nền: ngưỡng #808080, tolerance 12
```

---

## C4 · `spr_di_anh_quay_mat` — Bảy di ảnh đồng loạt quay mặt vào vách (S3)

*Cùng cú doạ với C3. Bảy di ảnh quay quanh trục dọc 0° → 180°, **đồng loạt, cùng tốc độ**. Khung hình khó chịu nhất là mốc 200 ms: quay được ~90°, đúng cạnh mỏng, bàn thờ trông như **trống trơn**. Trạng thái cuối là **vĩnh viễn** — di ảnh không bao giờ quay lại trong Chapter 1.*

**Prompt**

```plaintext
2D hand-painted game sprite set for a point-and-click horror game — one old Vietnamese memorial portrait frame rendered through a full 180 degree rotation about its vertical axis, from front-facing to fully turned to the wall, to be instanced seven times across an altar.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: a modest wooden memorial frame with cracked glass varnish, the photograph inside deliberately illegible — brown-grey sepia tone, a stiff collar and a pale oval where a face would be, never resolved into features, never a recognisable person; the rotation frames show the frame narrowing to a thin edge at 90 degrees where it is almost invisible and only the frame's dark edge and a hairline of glass remain, then opening out again to show the back — corrugated cardboard backing, old paper tape, dried paste marks and a pencil date written by hand and scribbled over; the wood must read the same at every angle, no perspective foreshortening beyond simple horizontal scaling.
Format: 2D sprite sheet of 9 frames covering 0, 22, 45, 67, 90, 112, 135, 157 and 180 degrees, all at identical scale and baseline so seven copies can be offset in engine and rotate in perfect sync; centred on a flat solid #808080 grey background, no cast shadow on the background, no gradient, no vignette, no ground plane, subject fully inside frame with a ten percent margin on every side, clean hard alpha edge ready for background removal, no text, no UI, no watermark.
```

**Negative prompt**

```plaintext
NEG-CORE, clear human face, recognisable portrait, smiling person, colour photograph, modern photo, ghost face appearing in the glass, eyes following the viewer, glowing frame, ornate gold rococo frame, Chinese ancestor portrait in formal robes, cast shadow, background scenery
```

Aspect ratio: **1:1 — 1024 x 1024 / khung**

**Midjourney (đuôi tham số)**

```plaintext
--ar 1:1 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179634 --chaos 0 --no clear face, smiling person, colour photo, ghost face, glowing frame, rococo gold frame, shadow, background, text
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 28 | CFG 7.0 | Seed 179634 | Size 1024x1024 | Hires Latent 1.5x denoise 0.30
LoRA linhanthon_style_v1 : 0.65 | Clip skip 2 | Tách nền: ngưỡng #808080, tolerance 12
```

**File xuất:** `anim_di_anh_dong_loat_quay.png` + `_soft` + `_static`. `_static` = **khung 180°** (mặt sau bìa các-tông), vì đó là trạng thái vĩnh viễn sau cú doạ.

---

## C5 · `spr_khoi_tu` — Khói tụ thành dáng người chắp tay (S4, `scare_khoi_tu_hinh_nguoi`)

*`area_gian_tho` · **DREAD scare** — không transient, không punch, không flash. Tụ rất chậm (alpha 0 → 0.5 trong 400 ms), thành **dáng người đứng chắp tay cao 620 px**, **không có mặt**, và **ở lại bất động cho tới khi người chơi chạm màn hình** (tối đa 12 s). Cú doạ duy nhất người chơi phải tự tay xua đi.*

**Prompt**

```plaintext
2D hand-painted game sprite for a point-and-click horror game — incense smoke gathering upward into the standing shape of a person with palms pressed together, painted as smoke and nothing else.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: a column of pale grey incense smoke #7E8B93 at fifty percent opacity that has thickened just enough to suggest a standing human of 620 pixels height — shoulders, a bowed neck line, two forearms brought together in front of the chest — while every edge stays smoke, tearing and reforming, never hardening into cloth or skin; the head is present only as a slightly denser rounded mass with absolutely no features, no eyes, no mouth, no hair; the lower third dissolves into loose drifting strands with no feet and no contact with any ground; the whole thing must read as smoke that happens to be person-shaped, not as a person made of smoke.
Format: 2D sprite sheet of 12 frames — 6 frames of very slow gathering over 600 milliseconds, then 6 nearly identical hold frames with only internal smoke drift and no silhouette change, plus a 6 frame dissipation set for when the player taps; centred on a flat solid #808080 grey background, no cast shadow on the background, no gradient, no vignette, no ground plane, subject fully inside frame with a ten percent margin on every side, clean hard alpha edge ready for background removal, no text, no UI, no watermark.
```

**Negative prompt**

```plaintext
NEG-CORE, visible face, eyes in the smoke, screaming face in smoke, skull, demon shape, glowing smoke, coloured smoke, fog machine, dry ice, solid ghost body, robe, hair, feet, standing on floor, cast shadow, background scenery
```

Aspect ratio: **9:16 — 768 x 1365 / khung**

**Midjourney (đuôi tham số)**

```plaintext
--ar 9:16 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179635 --chaos 0 --no face, eyes, skull, demon, glowing smoke, coloured smoke, solid body, hair, feet, shadow, background, text
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 28 | CFG 7.0 | Seed 179635 | Size 768x1344 | Hires Latent 1.5x denoise 0.30
LoRA linhanthon_style_v1 : 0.65 | Clip skip 2 | Tách nền: ngưỡng #808080, tolerance 12, feather 2px (mép khói cần mềm hơn)
```

> **Lưu ý alpha:** đây là sprite **duy nhất** được phép có mép alpha mềm. Tất cả sprite còn lại phải có mép cứng.

---

## C6 · `spr_mat_trang_ngoai_cua` — Khuôn mặt trắng bệch ngoài cửa bếp (S5, `scare_mat_duoi_day_gieng`)

*`area_bep_gieng` · `ON_PUZZLE_FAIL_COUNT` max_fails 3 · `screen_flash: true` (`#FFE9C4`, **vàng nến chứ không phải trắng**). Mặt áp sát cửa liếp, cách khung 1,2 m, **không chuyển động, không há miệng, mắt mở bình thường** — và chỉ nhìn thấy trong đúng quầng sáng của que đóm loé.*

**Prompt**

```plaintext
2D hand-painted game sprite for a point-and-click horror game — a bloodless pale human face pressed close to the outside of a split-bamboo kitchen door panel, glimpsed for a fraction of a second in the flare of a burning taper.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: a face painted flat and chalk-pale like unfired clay, ordinary proportions, ordinary calm expression, eyes open in a completely normal way and looking straight ahead, mouth closed, no distortion, no snarl, no black sockets, no blood, no wound, hair simply dark and flat behind it, the whole face partly broken up by the horizontal bamboo slats of the door panel it is pressed against so it is never fully visible at once; the pallor comes from the taper light hitting it from below at a shallow angle, leaving the eye sockets only slightly cooler, not black; it must be unsettling because it is calm and close and should not be there, not because it is monstrous.
Format: 2D sprite sheet of 6 frames — 1 frame of empty door slats, 3 frames of the face lit by the flare with no movement at all between them, 2 frames of it going dark again; centred on a flat solid #808080 grey background, no cast shadow on the background, no gradient, no vignette, no ground plane, subject fully inside frame with a ten percent margin on every side, clean hard alpha edge ready for background removal, no text, no UI, no watermark.
```

**Negative prompt**

```plaintext
NEG-CORE, hollow black eye sockets, screaming mouth, open jaw, sharp teeth, bloodshot eyes, glowing eyes, distorted face, zombie, rotting skin, blood, wounds, long wet hair covering the face, Sadako, jump scare face, extreme close up nostrils, cast shadow, background scenery
```

> **Kiểm duyệt bắt buộc:** đây là sprite **sát ranh giới cấm nhất** của cả bộ (`01_narrative.md` B.1 cấm "mặt ma cận cảnh hốc mắt đen"). Được phép **duy nhất** vì khuôn mặt này **bình thường** và **đứng yên**. Art Lead phải ký duyệt từng bản trước khi đóng bundle; bất kỳ bản nào có biểu cảm dữ tợn đều **loại**.

Aspect ratio: **1:1 — 1024 x 1024 / khung**

**Midjourney (đuôi tham số)**

```plaintext
--ar 1:1 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179636 --chaos 0 --no black eye sockets, screaming, open mouth, teeth, glowing eyes, distorted, zombie, blood, long hair over face, Sadako, shadow, background, text
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 28 | CFG 7.5 (cần bám mô tả "bình thường, bình thản" rất chặt) | Seed 179636 | Size 1024x1024 | Hires Latent 1.5x denoise 0.28
LoRA linhanthon_style_v1 : 0.65 | Clip skip 2 | Tách nền: ngưỡng #808080, tolerance 12
```

---

## C7 · `spr_hinh_nhan_the_mang` — Hình nhân thế mạng chắn lối (S6, `scare_hinh_nhan_chan_loi`)

*`area_gac_xep` · `ON_ENTER_AREA`, lần vào **đầu tiên duy nhất** · `screen_flash: false`. **Cú doạ duy nhất không thể tránh** của chương. Ở mốc 600 ms đèn cháy lại, hình nhân **đã đứng sẵn** cách chưa đầy một gang tay, chiếm **68% chiều cao khung**, mặt than hai chấm một vạch, **mặt quay vào phía trong nhà** (phạm điều Sáu trong bảy điều cấm kỵ). Sau envelope nó **KHÔNG biến mất** — người chơi phải đi vòng qua nó suốt phần còn lại của chương.*

**Prompt**

```plaintext
2D hand-painted game sprite for a point-and-click horror game — a life-sized Vietnamese substitute effigy woven from bamboo splints and pasted with do paper, standing directly in front of the viewer at less than arm's length, seen by oil-lamp light.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: a human-sized figure whose armature of split bamboo shows through wherever the paper has torn or sagged, the body surfaced in overlapping sheets of cream do paper #D9C9A3 with visible paste seams, fibre and brush-applied glue shine, the shoulders slightly uneven because it was made by hand and made fast, the arms straight down and a little too long, the hands only mitten shapes of folded paper; the head is a paper-covered bamboo ball bearing a face drawn in black ink in exactly three marks — two dots for eyes and one horizontal stroke for a mouth — and nothing else, no nose, no expression, no detail; paper dust on the shoulders, one loose splint sticking out at the hip; warm lamp light #FFD9A0 rakes it from the lower left, the right side falling into warm dark brown.
Format: 2D sprite sheet of 4 frames only — full dark, then a lamp-relight luminance ramp over 180 milliseconds bringing the already-standing figure into view, then 2 hold frames with no movement whatsoever; the figure must occupy 68 percent of the frame height; centred on a flat solid #808080 grey background, no cast shadow on the background, no gradient, no vignette, no ground plane, subject fully inside frame with a ten percent margin on every side, clean hard alpha edge ready for background removal, no text, no UI, no watermark.
```

**Negative prompt**

```plaintext
NEG-CORE, realistic human face, painted doll face, porcelain doll, mannequin, wax figure, scarecrow with sackcloth head, wicker man, Halloween effigy, glowing eyes, moving arms, reaching toward camera, blood on paper, cast shadow, background scenery
```

Aspect ratio: **9:16 — 768 x 1365 / khung**

**Midjourney (đuôi tham số)**

```plaintext
--ar 9:16 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179637 --chaos 0 --no realistic face, doll face, mannequin, scarecrow, wicker man, glowing eyes, reaching arms, blood, shadow, background, text
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 28 | CFG 7.0 | Seed 179637 | Size 768x1344 | Hires Latent 1.5x denoise 0.30
LoRA linhanthon_style_v1 : 0.65 | Clip skip 2 | Tách nền: ngưỡng #808080, tolerance 12 | Pivot bottom-center
```

**File xuất:** `spr_hinh_nhan_the_mang_f00..f03.png` → `anim_hinh_nhan_hien_gan.png` + `_soft` + `_static`. Xuất thêm **`spr_hinh_nhan_the_mang_idle.png`** — bản đứng yên dùng cho lớp MIDGROUND của `bg_gac_xep` và cho mọi lượt vào area sau lần đầu.

---

## C8 · `spr_ao_cuoi_giay` — Áo cưới giấy khổ người lớn (cô dâu giấy / Bà Cô)

*`item_ao_cuoi_giay` · vật phẩm nhan đề của cả dự án ("Áo Cưới Giấy Style"). Treo trên móc gỗ sau lưng khung ảnh, **tà áo còn phẳng như chưa ai mặc**, nhưng **vai áo hơi trĩu xuống, như vừa có ai mặc thử** (`01_narrative.md` §2.2). Gấu áo có mấy con số bằng bút chì — **khớp số đo của chính người chơi**.*

**Prompt**

```plaintext
2D hand-painted game sprite for a point-and-click horror game — an adult-sized Vietnamese wedding dress made entirely of votive paper, hanging empty on a wooden hook, the title object of the game.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: a traditional Northern Vietnamese bridal ao dai cut and pasted from votive paper in deep offering red #A63328 with flaking gold leaf trim #C9A227 at the collar and cuffs, the panels joined by visible rice-paste seams that have dried shiny, the hem still perfectly flat and uncreased because nobody has ever walked in it, the paper crisp enough to hold its own shape so it hangs stiff rather than draping like cloth, the shoulders however sagging very slightly as though someone recently tried it on; a few pencil measurement numbers written small and faint along the inside hem; a plain wooden hook and a short length of hemp cord at the top; one corner of the sleeve already softened by damp air; no body inside, no figure, nothing filling it.
Format: 2D sprite set of 3 states — hanging on the hook, lifted and held out flat, and draped over a standing bamboo effigy — plus a 6 frame loop of the empty dress swaying two degrees; centred on a flat solid #808080 grey background, no cast shadow on the background, no gradient, no vignette, no ground plane, subject fully inside frame with a ten percent margin on every side, clean hard alpha edge ready for background removal, no text, no UI, no watermark.
```

**Negative prompt**

```plaintext
NEG-CORE, western white wedding gown, lace, tulle, satin, silk drape, Chinese qipao, Japanese kimono, bride wearing the dress, human body inside, floating dress with a ghost in it, glowing dress, blood stains, torn shredded rags, cast shadow, background scenery
```

Aspect ratio: **9:16 — 768 x 1365 / khung**

**Midjourney (đuôi tham số)**

```plaintext
--ar 9:16 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179638 --chaos 0 --no white wedding gown, lace, satin, qipao, kimono, bride, body inside, glowing, blood, rags, shadow, background, text
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 28 | CFG 7.0 | Seed 179638 | Size 768x1344 | Hires Latent 1.5x denoise 0.30
LoRA linhanthon_style_v1 : 0.65 | Clip skip 2 | Tách nền: ngưỡng #808080, tolerance 12
```

**File xuất:** `spr_ao_cuoi_giay_treo.png` (nền Area 5, lớp bật sau khi giải P6), `spr_ao_cuoi_giay_cam.png`, `spr_ao_cuoi_giay_khoac.png` (đã khoác lên hình nhân — dùng ở cutscene kết chương), `icon_item_ao_cuoi_giay.png` (xem C13).

---

## C9 · `spr_van_khoet_mat` — Chín mảnh ván lật úp, mỗi mảnh khoét thủng một khuôn mặt (S7, `scare_anh_tho_thieu_mat`)

*`area_gac_xep` · `ON_PUZZLE_FAIL_COUNT` max_fails 3 trên `puz_xep_anh_gia_pha` · `screen_flash: true` màu **`#FFD9A0` (màu đèn dầu, không phải trắng)`. Chín mảnh lật **cùng pha tuyệt đối** trong 140 ms — sự đồng bộ hoàn hảo là thứ không tự nhiên, và đó là điểm. Sau envelope, chín mảnh **tự lật trở lại** và **bố cục người chơi đang xếp được giữ nguyên 100%**.*

**Prompt**

```plaintext
2D hand-painted game sprite set for a point-and-click horror game — nine thin wooden photo panels in a three by three frame flipping over in perfect unison to reveal that every one of them has a head-shaped hole punched clean through it.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: nine identical thin panels of dark aged wood, 280 by 280 pixels each, front faces carrying fragments of a faded sepia memorial photograph, backs showing raw grain and old paste; through the centre of every single back a rough oval hole the size and shape of a human head has been cut, its edges furred with torn paper fibre and splintered wood as if gouged with a knife rather than drilled; behind the holes there is nothing to see, only flat dark board, no eyes looking through, no face behind, absolutely nothing; the flip is rendered as horizontal scaling through a thin edge, all nine at the identical angle in every frame.
Format: 2D sprite sheet of 8 frames covering the 140 millisecond synchronised flip, 4 hold frames of the nine holes completely motionless, and a 6 frame reverse flip back to the photo side; centred on a flat solid #808080 grey background, no cast shadow on the background, no gradient, no vignette, no ground plane, subject fully inside frame with a ten percent margin on every side, clean hard alpha edge ready for background removal, no text, no UI, no watermark.
```

**Negative prompt**

```plaintext
NEG-CORE, eyes peering through the holes, face behind the hole, ghost in the gap, glowing hole, red light from behind, blood on the wood, gore, drilled perfect circles, machine cut, clean modern plywood, cast shadow, background scenery
```

Aspect ratio: **1:1 — 1024 x 1024 / khung**

**Midjourney (đuôi tham số)**

```plaintext
--ar 1:1 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179639 --chaos 0 --no eyes in the hole, face behind, glowing hole, red light, blood, clean plywood, shadow, background, text
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 28 | CFG 7.0 | Seed 179639 | Size 1024x1024 | Hires Latent 1.5x denoise 0.30
ControlNet lineart weight 0.70 — dùng lại đúng lưới 3x3 của B6 để chín mảnh khớp pixel với bàn cờ đang chơi
LoRA linhanthon_style_v1 : 0.65 | Clip skip 2 | Tách nền: ngưỡng #808080, tolerance 12
```

---

## C10 · `spr_dau_nan_tre_quay` — Đầu nan tre quay ngược 180° (S8, `scare_ao_cuoi_quay_dau`, cú đóng chương)

*`area_gac_xep` · `ON_TIMER` delay 400 ms từ nhịp 4 của `seq_ending_ch01_khoac_ao` · **DREAD scare**: không flash, không punch, không stinger. Chỉ có **tiếng nan tre nghiến** và **một cái đầu quay rất chậm**. Giữ **2,5 giây** — dài đến mức khó chịu. Người chơi không được phép giật mình rồi quên; họ phải **nhìn**.*

**Prompt**

```plaintext
2D hand-painted game sprite for a point-and-click horror game — the head of a paper-and-bamboo substitute effigy, now wearing a paper wedding dress, turning a full 180 degrees backwards on its neck, very slowly.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: the upper third of the effigy — paper-covered bamboo ball head, a collar of votive red paper #A63328 with flaking gold trim, shoulders of pasted do paper; the head begins turned away from the viewer and rotates backwards through profile to face the viewer directly, and at every stage the neck shows the bamboo splints twisting and crimping against each other with the paper wrinkling and tearing slightly at the throat; the face when it arrives is the same three ink marks as before, two dots and one stroke, and nothing more — no expression change, no new detail, no eyes opening; the motion must read as mechanical and patient, never snapping, never lunging toward the camera.
Format: 2D sprite sheet of 14 frames spread evenly across a slow 180 degree rotation plus 6 identical hold frames for a 2.5 second stare, no zoom, no scale change, no camera move implied; centred on a flat solid #808080 grey background, no cast shadow on the background, no gradient, no vignette, no ground plane, subject fully inside frame with a ten percent margin on every side, clean hard alpha edge ready for background removal, no text, no UI, no watermark.
```

**Negative prompt**

```plaintext
NEG-CORE, realistic face, doll face, glowing eyes, opening mouth, snarl, lunging at camera, snapping motion, blood at the neck, broken bone, gore, exorcist head spin, horror movie poster, cast shadow, background scenery
```

Aspect ratio: **1:1 — 1024 x 1024 / khung**

**Midjourney (đuôi tham số)**

```plaintext
--ar 1:1 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179640 --chaos 0 --no realistic face, doll face, glowing eyes, open mouth, lunging, blood, bone, gore, exorcist, shadow, background, text
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 28 | CFG 7.0 | Seed 179640 | Size 1024x1024 | Hires Latent 1.5x denoise 0.30
LoRA linhanthon_style_v1 : 0.65 | Clip skip 2 | Tách nền: ngưỡng #808080, tolerance 12
Ghi chú: DÙNG LẠI seed của C7 cho phần thân (179637) khi ghép, để chất giấy và nan tre khớp tuyệt đối
```

---

## C11 · `spr_ba_dong_to` — Bà đồng Tơ, bóng người dưới sân ở khung hình cuối

*Nhân vật sống duy nhất có tác động trong Chapter 1, và **không xuất hiện trên màn hình cho tới khung hình cuối cùng** (`01_narrative.md` §2.6, §6.1 nhịp 7–8). 84 tuổi, lưng còng, khăn mỏ quạ, tay cầm một nắm hương vòng đang cháy đỏ. Nhìn từ trên gác xuống, **qua khe ván sàn**, nên chỉ thấy **bóng nhỏ ở đầu ngõ tre**, tách khỏi hai hàng đuốc.*

**Prompt**

```plaintext
2D hand-painted game sprite for a point-and-click horror game — a very old Vietnamese village woman seen small and far below from a loft, standing apart at the mouth of a bamboo lane, holding a bundle of burning coil incense.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: a small stooped figure barely 300 pixels tall, back deeply curved with age, wearing a dark brown four-panel peasant tunic and the black crow-beak headscarf of Northern Vietnamese village women, face left almost entirely in shadow with only the jawline catching light and no readable expression, one hand holding a loose bundle of coil incense whose tips glow dull red and cast a small warm pool no wider than her hands; she stands completely still and faces the house; her feet are bare on wet brick; a faint twist of incense smoke rises past her shoulder; she must read as a living old woman, not as a ghost — solid, opaque, ordinary, and all the more disturbing for it.
Format: 2D sprite sheet of 6 frames with almost no movement — only the incense embers pulsing and the smoke drifting — plus one separate near-silhouette variant for the darker composite; centred on a flat solid #808080 grey background, no cast shadow on the background, no gradient, no vignette, no ground plane, subject fully inside frame with a ten percent margin on every side, clean hard alpha edge ready for background removal, no text, no UI, no watermark.
```

**Negative prompt**

```plaintext
NEG-CORE, witch, hag caricature, hooked nose, warts, glowing eyes, floating ghost, transparent figure, Chinese peasant costume, Japanese kimono, conical hat non la worn indoors, cheerful grandmother, smiling, bright clothing, cast shadow, background scenery
```

> Bà Tơ **không phải phù thuỷ**. `01_narrative.md` nói rõ: trong đầu bà, bà đang **cứu cả làng**. Vẽ bà thành mụ phù thuỷ là phá hỏng luận điểm chủ đề lớn nhất của dự án — *hủ tục là do người sống bịa ra, và người sống tin rằng mình đang làm điều tốt*.

Aspect ratio: **9:16 — 768 x 1365 / khung**

**Midjourney (đuôi tham số)**

```plaintext
--ar 9:16 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179641 --chaos 0 --no witch, hag, hooked nose, glowing eyes, floating ghost, transparent, kimono, smiling, bright clothing, shadow, background, text
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 28 | CFG 7.0 | Seed 179641 | Size 768x1344 | Hires Latent 1.5x denoise 0.30
LoRA linhanthon_style_v1 : 0.65 | Clip skip 2 | Tách nền: ngưỡng #808080, tolerance 12 | Pivot bottom-center
```

**Cùng bộ (sinh bằng biến thể prompt này):** `spr_hang_duoc_duoi_san.png` — hai hàng đốm sáng đuốc và đèn pin xếp dọc hai bên sân, **không ai nói một câu nào**; 12–14 đốm, không thấy rõ người.

---

## C12 · `spr_ban_tay_nguoi_choi` — Bàn tay người chơi (thợ may)

*Người chơi **không có sprite toàn thân** (`01_narrative.md` §2.1). Chỉ thấy **bàn tay** khi tương tác, **bóng đổ** trên sân gạch, và mặt phản chiếu trong chum nước (luôn bị che/mờ). Nhân vật là **thợ may bậc 3** — bàn tay phải kể được điều đó.*

**Prompt**

```plaintext
2D hand-painted game sprite set for a point-and-click horror game — the hands of a 27-year-old Vietnamese seamstress, seen from the player's own point of view, performing adventure-game interactions.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: slim working hands, short unpolished nails, a faint permanent callus on the right middle finger where scissors rest and small old needle marks on the left index finger, plain cuffs of a dark cotton shirt at the wrist, no jewellery, no watch, no nail polish, skin tone warm but painted in the same desaturated key as the rest of the game, lamp light from one side only; separate poses required — flat open palm hovering, index finger pointing, pinch grip holding a small object, two fingers rubbing charcoal across paper, both hands smoothing a collar flat; every pose reads clearly at 260 pixels wide.
Format: 2D sprite set of 5 separate poses, each on its own frame, consistent hand size and light direction across all five; centred on a flat solid #808080 grey background, no cast shadow on the background, no gradient, no vignette, no ground plane, subject fully inside frame with a ten percent margin on every side, clean hard alpha edge ready for background removal, no text, no UI, no watermark.
```

**Negative prompt**

```plaintext
NEG-CORE, extra fingers, six fingers, fused fingers, deformed hand, muscular male hand, child hand, long painted nails, rings, bracelet, watch, gloves, blood, wounds, tattoos, cast shadow, background scenery
```

Aspect ratio: **4:3 — 1024 x 768 / khung**

**Midjourney (đuôi tham số)**

```plaintext
--ar 4:3 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179642 --chaos 0 --no extra fingers, deformed hand, male hand, long nails, rings, watch, gloves, blood, tattoo, shadow, background, text
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 30 | CFG 7.5 | Seed 179642 | Size 1024x768 | Hires Latent 1.5x denoise 0.28
LoRA linhanthon_style_v1 : 0.60 (hạ weight để giữ giải phẫu bàn tay đúng) | Clip skip 2
Bắt buộc: chạy ADetailer hand_yolov8n + inpaint tay ở mọi bản trước khi duyệt
```

---

## C13 · `icon_item_*` — Bộ 10 icon vật phẩm trong túi đồ

*Thanh inventory 6 ô ở dải `y ∈ [1000, 1080]`, mỗi ô **vẽ 160 x 80 px**, **vùng chạm mở rộng lên 160 x 120** để đạt sàn chạm 120 px @1920 — vùng chạm trùm dải `y ∈ [960, 1080]`, không đụng hotspot nào vì luật bố cục đã chừa `y + height ≤ 1000` cho hotspot trong cảnh. Mười `item_id` đúng và đủ theo SPINE — **không phát sinh id mới**.*

**Prompt**

```plaintext
2D hand-painted inventory icon set for a point-and-click horror game — ten 1990s Northern Vietnamese rural objects painted as separate flat inventory icons.
Style: Vietnamese folk horror, "Ao Cuoi Giay" paper-bride style, hand-painted 2D point-and-click adventure art, 1990s Northern Vietnam village, muted desaturated palette #0E0F12 #2E2A24 #55604A #8C3A2E #FFD9A0, one warm oil-lamp key light against cold twilight fill, dry-brush stroke and paper grain visible, flat orthographic front view, no perspective distortion, no lens effects.
Details: ten objects, each rendered alone, three-quarter tilted flat with no perspective, lit identically from the upper left so the whole set reads as one family — 1 a small verdigris-green brass key with a worn Han character on its bow, 2 a stack of three thin do paper sheets weighted by a sharpened charcoal stick, 3 a single do paper sheet bearing two black charcoal-rubbed Han characters, 4 an unlit American-style kerosene hurricane lamp with soot-blackened glass and a dry fount, 5 a jackfruit-wood temple-block mallet with its handle polished smooth in exactly three places and a frayed cloth-wrapped head, 6 a blank ancestral tablet of pale new wood with a bare unlettered face and a cut tenon visible at its foot, 7 a strip of faded brick-red altar cloth, thick weave, one end already frayed into threads, 8 a glass bottle of kerosene half full, stoppered with a twist of dried banana leaf, 9 the same hurricane lamp now lit with a flame the size of a grain of rice, 10 an adult-sized votive-paper wedding dress in offering red with flaking gold trim, folded; every object slightly worn, nothing new, nothing shiny.
Format: ten separate square icons, each object centred and occupying seventy percent of its own cell, consistent scale logic and identical light direction across the whole set, readable in silhouette at 160 by 80 pixels; centred on a flat solid #808080 grey background, no cast shadow on the background, no gradient, no vignette, no ground plane, subject fully inside frame with a ten percent margin on every side, clean hard alpha edge ready for background removal, no text, no UI, no watermark, no frames, no borders.
```

**Negative prompt**

```plaintext
NEG-CORE, icon frame, rounded border, drop shadow, glow outline, rarity colour, RPG loot icon, cartoon outline, sticker style, new shiny objects, plastic, chrome, gemstones, magical aura, cast shadow, background scenery
```

Aspect ratio: **1:1 — 512 x 512 / icon** (xuất 320x320 → atlas 160x160 @1x)

**Midjourney (đuôi tham số)**

```plaintext
--ar 1:1 --style raw --v 6.1 --sref {STYLE_ANCHOR} --sw 140 --seed 179643 --chaos 0 --no icon frame, border, drop shadow, glow, rarity color, RPG loot, sticker, shiny, chrome, gems, magic aura, shadow, background, text
```

**Stable Diffusion**

```plaintext
Sampler DPM++ 2M Karras | Steps 28 | CFG 7.0 | Seed 179643 | Size 1024x1024 | Hires Latent 1.5x denoise 0.30
LoRA linhanthon_style_v1 : 0.65 | Clip skip 2 | Tách nền: ngưỡng #808080, tolerance 12
Sinh TỪNG icon một với cùng seed 179643, chỉ đổi phần mô tả object — KHÔNG sinh cả sheet trong một lần (sheet sinh một lần sẽ lệch scale và lệch hướng sáng giữa các ô)
```

**Ánh xạ tên file (khớp `item_id` trong JSON):**

| # | `item_id` | File xuất |
|---|---|---|
| 1 | `item_chia_khoa_dong` | `icon_item_chia_khoa_dong.png` |
| 2 | `item_giay_ban_va_than` | `icon_item_giay_ban_va_than.png` |
| 3 | `item_ban_rap_chu_the` | `icon_item_ban_rap_chu_the.png` |
| 4 | `item_den_dau` | `icon_item_den_dau.png` |
| 5 | `item_dui_mo` | `icon_item_dui_mo.png` |
| 6 | `item_bai_vi_khuyet_danh` | `icon_item_bai_vi_khuyet_danh.png` |
| 7 | `item_dai_vai_dieu` | `icon_item_dai_vai_dieu.png` |
| 8 | `item_chai_dau_hoa` | `icon_item_chai_dau_hoa.png` |
| 9 | `item_den_dau_sang` | `icon_item_den_dau_sang.png` |
| 10 | `item_ao_cuoi_giay` | `icon_item_ao_cuoi_giay.png` |

---

# 6. BẢNG TỔNG HỢP TÀI SẢN & CHECKLIST QA

## 6.1. MỤC A — 5 bối cảnh

| Prompt | Asset id | `area_id` | Seed | `background_asset_url` trong JSON |
|---|---|---|---|---|
| A1 | `bg_san_gach` | `area_san_gach` | 179612 | `https://cdn.linhanthon.game/assets/bg_san_gach.bundle` |
| A2 | `bg_hien_nha` | `area_hien_nha` | 179613 | `https://cdn.linhanthon.game/assets/bg_hien_nha.bundle` |
| A3 | `bg_gian_tho` | `area_gian_tho` | 179614 | `https://cdn.linhanthon.game/assets/bg_gian_tho.bundle` |
| A4 | `bg_bep_gieng` | `area_bep_gieng` | 179615 | `https://cdn.linhanthon.game/assets/bg_bep_gieng.bundle` |
| A5 | `bg_gac_xep` | `area_gac_xep` | 179616 | `https://cdn.linhanthon.game/assets/bg_gac_xep.bundle` |

Mỗi bối cảnh = **4 lớp PNG + 1 bản dẹt duyệt**. A4 có thêm bản `_lit`, A5 có thêm lớp quầng đèn rời → **22 file lớp**.

## 6.2. MỤC B — 6 zoom câu đố

| Prompt | Asset id | `puzzle_id` | `type` | Seed | Khung zoom |
|---|---|---|---|---|---|
| B1 | `zoom_puz_khoa_bat_quai` | `puz_khoa_bat_quai` | `ROTATION_LOCK` | 179621 | `{560,140,800,800}` |
| B2 | `zoom_puz_rap_chu_the_menh` | `puz_rap_chu_the_menh` | `PATTERN_TRACE` | 179622 | 2 ô dọc, 8 nét ≥ 44px |
| B3 | `zoom_puz_tuan_tu_le_cung` | `puz_tuan_tu_le_cung` | `SEQUENCE_ORDER` | 179623 | 6 icon 150x150 + chiếu lễ `{360,830,1200,170}` |
| B4 | `zoom_puz_ba_hoi_chin_tieng` | `puz_ba_hoi_chin_tieng` | `AUDIO_MATCH` | 179624 | **chuông** `{520,420,520,420}` + **mõ** `{1240,380,260,260}` |
| B5 | `zoom_puz_thap_lai_den_dau` | `puz_thap_lai_den_dau` | `ITEM_COMBINE` | 179625 | đèn `{760,380,400,520}` + 5 phần tử ≥ 160x160 |
| B6 | `zoom_puz_xep_anh_gia_pha` | `puz_xep_anh_gia_pha` | `SLIDING_TILE` | 179626 | `{660,120,840,840}`, ô 280x280 |

Mỗi zoom = **`_plate` + `_parts`** → **12 file**, cộng 2 biến thể phụ (`B5 _lit`, `B6 _parts_khoet`) → **14 file**.

## 6.3. MỤC C — 13 bộ sprite (nền `#808080`)

| Prompt | Asset id | `sprite_animation` trong JSON | `scare_id` / vai trò | Seed | Tỉ lệ |
|---|---|---|---|---|---|
| C1 | `spr_bong_khan_xo` (+`spr_nuoc_vo`) | `anim_bong_khan_xo_trong_chum` | `scare_bong_trong_chum` | 179631 | 1:1 |
| C2 | `spr_ban_tay_vang_ma` | `anim_ban_tay_vang_ma_quet` | `scare_ban_tay_giay_sau_manh` | 179632 | 16:9 |
| C3 | `spr_chan_nhang_chay` | `anim_di_anh_dong_loat_quay` (lớp 1) | `scare_di_anh_quay_mat` | 179633 | 1:1 |
| C4 | `spr_di_anh_quay_mat` | `anim_di_anh_dong_loat_quay` (lớp 2) | `scare_di_anh_quay_mat` | 179634 | 1:1 |
| C5 | `spr_khoi_tu` | `anim_khoi_tu_dang_nguoi` | `scare_khoi_tu_hinh_nguoi` *(chờ Lead duyệt)* | 179635 | 9:16 |
| C6 | `spr_mat_trang_ngoai_cua` | `anim_mat_trang_ngoai_cua_bep` | `scare_mat_duoi_day_gieng` | 179636 | 1:1 |
| C7 | `spr_hinh_nhan_the_mang` | `anim_hinh_nhan_hien_gan` | `scare_hinh_nhan_chan_loi` | 179637 | 9:16 |
| C8 | `spr_ao_cuoi_giay` | — (vật phẩm + cutscene) | `item_ao_cuoi_giay` | 179638 | 9:16 |
| C9 | `spr_van_khoet_mat` | `anim_chin_manh_van_lat_up` | `scare_anh_tho_thieu_mat` *(chờ Lead duyệt)* | 179639 | 1:1 |
| C10 | `spr_dau_nan_tre_quay` | `anim_dau_nan_tre_quay_180` | `scare_ao_cuoi_quay_dau` | 179640 | 1:1 |
| C11 | `spr_ba_dong_to` (+`spr_hang_duoc_duoi_san`) | — (cutscene kết chương) | Bà đồng Tơ | 179641 | 9:16 |
| C12 | `spr_ban_tay_nguoi_choi` | — (con trỏ tương tác) | Người chơi | 179642 | 4:3 |
| C13 | `icon_item_*` x 10 | — (inventory) | 10 `item_id` của SPINE | 179643 | 1:1 |

**Biến thể an toàn bắt buộc:** 8 sprite jump-scare (C1–C3, C5–C7, C9, C10) x 2 biến thể (`_soft`, `_static`) = **16 file bổ sung**.

## 6.4. Tổng tài sản Chương 1

| Nhóm | Số file nguồn | Ước lượng sau nén (ASTC 6x6) |
|---|---|---|
| Bối cảnh (5 area x 4 lớp + phụ) | 22 | ~11.5 MB |
| Zoom câu đố (6 x `_plate` + `_parts` + phụ) | 14 | ~4.2 MB |
| Sprite jump-scare + biến thể an toàn | 24 sheet | ~3.6 MB |
| Sprite nhân vật / bàn tay / hàng đuốc | 4 | ~0.7 MB |
| Icon vật phẩm (10, đóng 1 atlas) | 1 atlas | ~0.3 MB |
| **TỔNG ĐỒ HOẠ CHƯƠNG 1** | **65** | **~20.3 MB** |

> **Đối chiếu ràng buộc nền tảng:** APK engine ≤ 30MB và **toàn bộ tài sản tải qua Unity Addressables (remote bundle)** → không một file nào trong bảng này được đóng vào APK. Chi tiết nhóm bundle và luật nạp trước xem `docs/05_TICH_HOP_UNITY_ADDRESSABLES.md`. Tổ âm thanh chiếm thêm ~18.8 MB (ngân sách tài sản âm thanh Chương 1 do tổ Horror/Audio bàn giao, **đã gồm 8 file stinger biến thể `_soft`** theo `docs/06_AN_TOAN_NGUOI_CHOI.md` §4.3), tổng remote Chương 1 ≈ **39 MB**.

## 6.5. Checklist QA trước khi đóng bundle

**Nhất quán phong cách**
- [ ] Mọi prompt đã dùng **đúng nguyên văn** chuỗi `SL-CORE` ở dòng `Style:`.
- [ ] Mọi lần sinh đều có `--sref {STYLE_ANCHOR}` (MJ) hoặc `linhanthon_style_v1` (SD). Không có tài sản nào "sinh vội không neo".
- [ ] Không xuất hiện màu ngoài bảng §1.1. Kiểm bằng cách giảm ảnh về 16 màu và soi bảng màu kết quả.
- [ ] Độ bão hoà trung bình mỗi bối cảnh ≤ 25%, trừ điểm nhấn `votive_red`.
- [ ] Mỗi khung hình có **đúng một** mảng trắng `xo_white`.
- [ ] Đã khoá `--v 6.1` / model hash trong suốt chương, không đổi giữa chừng.

**Đúng ngữ cảnh văn hoá (soát theo `01_narrative.md` B.1)**
- [ ] Không có chi tiết Trung Hoa / Nhật Bản / Thái Lan lẫn vào (đèn lồng đỏ, torii, kimono, mái cong chùa Tàu).
- [ ] Không có thánh giá, ngũ giác, ouija, phù thuỷ phương Tây.
- [ ] **Giếng ở A4 không có gì trèo lên.** Không tóc dài, không bàn tay trên thành giếng.
- [ ] Không máu, không nội tạng, không xác phân huỷ trong bất kỳ tài sản nào.
- [ ] Không vẽ mặt ma. Kiểm từng sprite: chỉ được bóng phẳng / khói / mặt than hai chấm một vạch. C6 là ngoại lệ duy nhất và **phải có chữ ký Art Lead**.
- [ ] Bà đồng Tơ **không** bị vẽ thành mụ phù thuỷ.

**Khớp dữ liệu (soát chéo `03_world.md` + `data/areas/*.json`)**
- [ ] Mỗi đồ vật tương tác được nằm **đúng vùng `visual_bounds`** của hotspot tương ứng, sai số ≤ 24px. **Đừng soát theo `bounds`** — `bounds` là VÙNG CHẠM và cố ý lớn hơn hình vẽ (sàn 120 x 120 px @1920). Luật hoà giải đầy đủ ở `docs/03_DATA_SPEC.md` §2.3.5.4.
- [ ] Không có hai đồ vật tương tác vẽ dính nhau ở chỗ bounds cách nhau 20px (đặc biệt `hs_binh_phong` ↔ `hs_o_lom_binh_phong`, `hs_mo_ca` ↔ `hs_dui_mo`, `hs_hinh_nhan` ↔ `hs_chieu_coi_trai_san`).
- [ ] Không đồ vật quan trọng nào nằm trong dải `y < 80` (notch) hoặc `y > 1000` (inventory bar) — luật này áp cho **nét vẽ** (`visual_bounds`); vùng chạm được phép chạm mép dưới khung.
- [ ] Hotspot **hiện sau khi giải câu đố** (`hs_bai_vi_khuyet_danh`, `hs_dai_vai_dieu`, `hs_ao_cuoi_giay`) đã tách thành lớp bật/tắt, **không nung vào nền**.
- [ ] Tên file khớp **chính xác** asset id trong JSON (§2). Chạy `tools/validate_level.py` để đối chiếu.

**Kỹ thuật**
- [ ] Alpha sprite sạch ở zoom 400%, không sót viền `#808080` (soi kỹ mép giấy bản và nan tre).
- [ ] Pivot đúng: `bottom-center` cho C7 / C11, `center` cho C2 / C10.
- [ ] Đủ **cả hai** biến thể `_soft` và `_static` cho 8 sprite jump-scare — **16 file**, tên nối hậu tố đúng `docs/06_AN_TOAN_NGUOI_CHOI.md` §4.3. Thiếu 1 file = **chặn build**.
- [ ] Biến thể `_soft` dùng **đúng seed của bản gốc** (§1.4) — phải là **cùng một hình**, chỉ khác biên độ; `_static` là **khung trạng thái kết quả**, không phải khung đầu.
- [ ] **Không biến thể an toàn nào được đặt sau tường trả phí, sau quảng cáo thưởng hay sau mốc tiến trình** (`docs/06_AN_TOAN_NGUOI_CHOI.md` §1, N1–N3).
- [ ] Overlay flash chỉ dùng **3 mã hợp lệ** `#FFF2DC` / `#FFE9C4` / `#FFD9A0`, alpha toàn màn ≤ 0.35 (`docs/06_AN_TOAN_NGUOI_CHOI.md` §2.4). Không sắc đỏ, không `#FFFFFF`.
- [ ] Atlas ≤ 2048x2048, padding 4px, không rotate.
- [ ] Không vật thể nào tự phát quang. Mọi ánh sáng đều có nguồn trong cảnh.
- [ ] Bản `_lo` 1280x720 đã xuất cho toàn bộ bối cảnh.

---

## 7. BÀN GIAO

| Tài liệu / tổ đích | Thứ tài liệu này cung cấp |
|---|---|
| `docs/03_DATA_SPEC.md` | Asset id chuẩn cho `background_asset_url`, `sprite_animation`, `item_id` icon |
| `data/areas/*.json` | 5 `background_asset_url`, 8 `sprite_animation` khớp bảng §4.4.1 của `docs/06_AN_TOAN_NGUOI_CHOI.md` |
| `docs/05_TICH_HOP_UNITY_ADDRESSABLES.md` | 65 file nguồn, ~20.3 MB sau nén, quy ước bundle `bg_* / zoom_* / scare_*` |
| `tools/validate_level.py` | Luật đối chiếu tên file ↔ asset id (§2), luật bounds ↔ vị trí đồ vật (§3, §6.5) |
| `docs/04_LIVEOPS_MONETIZATION.md` | **Ràng buộc cứng**: biến thể `_soft` / `_static` là tài sản khả dụng miễn phí, không được bán |
| `docs/06_AN_TOAN_NGUOI_CHOI.md` | 16 file biến thể an toàn (`_soft` / `_static`) cho 8 sprite jump-scare; xác nhận bảng màu flash `#FFF2DC` / `#FFE9C4` / `#FFD9A0` nằm trong trần alpha cho phép |
| Tổ mỹ thuật | 24 prompt đã chuẩn ngữ cảnh + bảng seed + tấm neo phong cách |

---

*Hết tài liệu `02_PROMPT_DO_HOA.md` — Linh An Thôn, Chapter 1.*
*Nguồn sự thật: SPINE. Không một `area_id`, `item_id`, `puzzle_id` hay `scare_id` nào bị thay đổi.*
