# LINH AN THÔN — CHAPTER 1
## AN TOÀN NGƯỜI CHƠI & TRỢ NĂNG (PLAYER SAFETY / ACCESSIBILITY)

Tài liệu: `docs/06_AN_TOAN_NGUOI_CHOI.md` — **Deliverable bắt buộc, không phải phụ lục.**
Chủ sở hữu: Horror/Audio Designer (nội dung) · QA Lead (nghiệm thu) · LiveOps (ràng buộc thương mại).
Nguồn sự thật: **SPINE đã chốt** + `data/areas/*.json` (**6 trường `jumpscares[]` của Master Form**) + `data/liveops_chapter_01.json` (khoá cấu hình).
Nền tảng: Android / iOS. Chơi bằng **loa điện thoại ở nơi công cộng** là trường hợp phổ biến, không phải ngoại lệ.
Độ phân giải thiết kế: **1920 x 1080**, gốc toạ độ **(0,0) ở góc TRÊN-BÊN TRÁI**.
Ngôn ngữ: giải thích **tiếng Việt có dấu**; mọi `id` / khoá JSON **snake_case không dấu**.

> **Vì sao tài liệu này tồn tại và vì sao nó phải là deliverable.**
> Chương 1 có **8 jump-scare**, **4 cú có `screen_flash: true`** (S1, S2, S5, S7 — đếm từ `data/areas/*.json`), **haptic ở cả 8 cú** (bảng §4.4.1 không có một ô Haptic nào trống; bốn cú "tĩnh" S3/S4/S6/S8 vẫn rung, chỉ là `hap_long_rumble` biên độ thấp), và đề tài tang lễ / cái chết của trẻ em. Tổ mỹ thuật phải xuất **16 file biến thể an toàn** (`_soft`, `_static`), tổ code phải dựng **`ScareConfigResolver`**, tổ LiveOps phải giữ **5 cờ `*_free`**, QA phải chạy **kiểm định nhạy sáng đo được** trước mỗi build. Bốn tổ đọc chung một hợp đồng. Nếu hợp đồng đó chỉ nằm trong file nháp nội bộ thì mọi liên kết chéo đều gãy và mỗi tổ tự suy diễn một kiểu — đúng lúc phần rủi ro pháp lý và rủi ro sức khoẻ cao nhất.

---

## 0. MỤC LỤC & CÁCH DÙNG

| Mục | Nội dung | Ai đọc bắt buộc |
|---|---|---|
| **§1** | **Nguyên tắc bất biến** — an toàn miễn phí, ngay màn hình đầu, không sau cổng nào | Tất cả, đặc biệt LiveOps & Product |
| **§2** | Chính sách nhấp nháy / nhạy sáng — động kinh quang. Số đo + cách kiểm | VFX, Kỹ thuật đồ hoạ, QA |
| **§3** | Màn hình cảnh báo trước khi vào game + chỗ đổi lại trong Cài đặt | UI/UX, Localization |
| **§4** | **`gentle_mode`** — định nghĩa chính xác + bảng đối chiếu từng jump-scare | Code, Audio, Art |
| **§5** | `photosensitive_safe` — hồ sơ độc lập | VFX, Code |
| **§6** | Haptic, rung lắc màn hình, giảm âm stinger, **luật nghỉ 90 giây giữa hai cú doạ và điều kiện miễn trừ duy nhất (§6.3)** | Code, Audio, **LiveOps** |
| **§7** | Các tuỳ chọn còn lại + phụ đề âm thanh + người chơi khiếm thính | Code, Audio, Narrative |
| **§8** | Kiến trúc override (lớp trang trí, **không sửa dữ liệu gốc**) | Code |
| **§9** | Đối chiếu tuân thủ cửa hàng ứng dụng cho game kinh dị | Product, Legal, LiveOps |
| **§10** | **Bảng truy vết** tuỳ chọn an toàn ↔ khoá trong `data/liveops_chapter_01.json` | LiveOps, QA |
| **§11** | Checklist nghiệm thu — chặn build nếu trượt | QA |

---

## 1. NGUYÊN TẮC BẤT BIẾN

### 1.1. Bốn câu, không thương lượng

> **N1 — MIỄN PHÍ.** Mọi tuỳ chọn an toàn đều **miễn phí tuyệt đối**. Không gem, không quảng cáo thưởng, không IAP, không gói, không "phiên bản đầy đủ".
>
> **N2 — NGAY TỪ MÀN HÌNH ĐẦU.** Bật được **trước khi** nội dung kinh dị đầu tiên chạy, trên **màn hình cảnh báo** ở §3 — tức trước cả `area_san_gach`.
>
> **N3 — KHÔNG SAU BẤT KỲ CỔNG NÀO.** Không sau cổng **tiến trình** (không cần qua beat nào, area nào, chương nào), không sau cổng **tiền tệ**, không sau cổng **tài khoản**, không sau cổng **quảng cáo**, không sau tường "xem hết cutscene mới bỏ qua được".
>
> **N4 — KHÔNG MẤT GÌ KHI BẬT.** Người chơi bật tuỳ chọn an toàn **không mất** nội dung, manh mối, vật phẩm, thoại, thành tựu hay phần thưởng nào. Họ nhận **đúng nội dung ấy ở cường độ sinh lý thấp hơn**.

### 1.2. Hệ quả kỹ thuật của N4 — cái gì **không bao giờ** bị đụng vào

| Không bao giờ bị override | Vì sao |
|---|---|
| `puzzles[].solution` của cả 6 câu đố | Lời giải là hợp đồng cứng đã đối chiếu 3 nguồn. An toàn **không** được làm câu đố dễ đi hay khác đi. |
| `puzzles[].type` · `puzzles[].reward_item_id` · `puzzles[].required_items` · `puzzles[].grants_flag` | Đổi = đổi luồng tiến trình = người bật chế độ an toàn chơi một game khác. |
| `jumpscares[].max_fails` | Giữ nguyên tuyệt đối, để chứng minh khả giải của tổ câu đố vẫn đúng từng chữ. |
| `jumpscares[].trigger_type` · `jumpscares[].id` | Cú doạ vẫn bắn, đúng chỗ, đúng lý do. |
| `puzzles[].wrong_action_jumpscare` | Vẫn trỏ tới cú doạ ấy; **chỉ cường độ đổi**. |
| `hotspots[].*` — cả bảy khoá Master Form: `id`, `bounds`, `action_type`, `item_id`, `required_item`, `target_puzzle_id`, `target_area_id`, cộng `consumes_item` trên các hotspot `USE_ITEM` | Không tuỳ chọn an toàn nào được đụng vào vùng chạm hay hành vi tương tác. Đặc biệt: **`bounds` không bao giờ bị thu nhỏ** — sàn chạm **120 × 120 px @1920** (`docs/03_DATA_SPEC.md` §2.2, mức G3) là sàn **trợ năng**, không phải sàn thẩm mỹ, nên không chế độ nào được hạ nó. Và **`consumes_item` không bao giờ bị lật** — lật nó là đổi luồng vật phẩm, tức người bật chế độ an toàn chơi một game khác. |
| `chapter_id` · `area_id` · `background_asset_url` | — |
| 6 khoá Master Form của LiveOps: `hint_cost_gems`, `ads_reward_hints`, `iap_product_id`, `price_usd`, `event_start`, `override_bg` | An toàn **không nằm trong mạch tiền tệ**. Không một tuỳ chọn nào trong tài liệu này đọc, ghi hay phụ thuộc vào 6 khoá này. |

### 1.3. Hệ quả nội dung: cú doạ **vẫn xảy ra**

Mỗi cú doạ của Chương 1 mang **thông tin cốt truyện**: bảy di ảnh quay mặt vào vách, hình nhân đứng chắn lối, chín mảnh ván bị khoét thủng hình đầu người. **Bỏ cú doạ = bỏ thông tin = người chơi không hiểu chương 2.** Vì vậy chế độ an toàn **không xoá sự kiện**, nó chỉ hạ tải sinh lý:

- Hạ **biên độ** (scale, punch, shake, flash, haptic, độ ồn chênh).
- Hạ **tốc độ** (envelope ngắn hơn, transient bị bào mềm).
- **Tăng** khả năng dự đoán (tell to hơn, sớm hơn; có vignette báo trước).
- **Giữ nguyên** hậu quả trong thế giới và mọi `text_key`.

Chỉ ở mức cực đại `scare_intensity = 0` mới không còn envelope — và ngay cả khi đó, **sự kiện vẫn được kể** bằng trạng thái kết quả + một dòng mô tả (§4.5).

---

## 2. CHÍNH SÁCH NHẤP NHÁY / NHẠY SÁNG (PHOTOSENSITIVE EPILEPSY)

### 2.1. Sáu luật cứng — áp cho **mọi lớp hình ảnh**, không riêng jump-scare

Áp cho: flash jump-scare, lửa đèn dầu chao, chân nhang bốc, que đóm loé, than hồng thở, hương vòng, chuyển cảnh, hiệu ứng UI, vignette, animation loading — **và tổng hợp của tất cả các lớp cộng lại sau khi composite**.

| # | Luật | Con số đo được | Ghi chú |
|---|---|---|---|
| **P1** | **Tần số nhấp nháy ≤ 3,0 Hz** | Tối đa **3 lần đổi sáng↔tối trong bất kỳ cửa sổ trượt 1,000 ms nào** | **Đo trên khung đã composite**, không đo từng lớp. Cạm bẫy kinh điển: hai lớp mỗi lớp 2 Hz cộng lại thành 4 Hz → **trượt**. |
| **P2** | **Cấm flash đỏ bão hoà toàn màn** | Cấm mọi khung có `R ≥ 0xCC` **và** `G ≤ 0x40` **và** `B ≤ 0x40` phủ **> 25 %** diện tích. Cấm mọi chuyển tiếp **sang** hoặc **từ** đỏ bão hoà. | Kiểm chéo theo định nghĩa chuẩn: cấm chuyển tiếp mà thành phần đỏ chiếm `R/(R+G+B) ≥ 0,80`. Bảng màu flash của chương (§2.4) **không có mã nào chạm ngưỡng**. |
| **P3** | **Trần độ sáng chênh lệch (ΔL)** | Vùng **> 25 %** diện tích: `ΔL_rel ≤ 0,10`. Vùng **≤ 25 %**: `ΔL_rel ≤ 0,20`. | `L_rel` = độ chói tương đối ITU-R BT.709 trên sRGB đã tuyến tính hoá: `L = 0,2126·R + 0,7152·G + 0,0722·B`. |
| **P4** | **Trần diện tích màn hình được phép flash** | **Xung đơn** (đúng 1 xung, không lặp trong 1 s): tối đa **100 %** màn hình, alpha ≤ **0,35**. · **Chuỗi ≥ 2 xung / 1 s**: tối đa **25 % diện tích** (≤ **518.400 px²** trên khung 1920 x 1080), alpha ≤ **0,55**, và ≤ 3,0 Hz. · **Chuỗi ≥ 2 xung phủ > 25 % diện tích: CẤM TUYỆT ĐỐI.** | 25 % là ngưỡng xấp xỉ trường thị giác 10° khi cầm điện thoại ở khoảng 30 cm. |
| **P5** | **Trần biên độ của nguồn sáng dao động (LFO)** | Tần số ≤ **2,4 Hz**, biên độ độ sáng **± 12 %** | Áp cho lửa đèn dầu, than hồng, hương vòng, quầng đèn bám con trỏ ở `area_gac_xep`. |
| **P6** | **Cấm cắt cứng sáng↔tối** | Mọi chuyển tiếp độ sáng biên độ > 30 % phải có **ramp ≥ 150 ms**, không được cắt theo khung | Đưa các đoạn "tối phụt rồi sáng lại" ra khỏi định nghĩa "flash" hoàn toàn. |

### 2.2. Kiểm định 4 cú doạ có `screen_flash: true`

| # | `scare_id` | Số xung | Tần số hiệu dụng | Alpha đỉnh | Màu | Diện tích | P1 | P2 | P3 | P4 | Kết luận |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | `scare_bong_trong_chum` | **1** | **0 Hz** (sự kiện đơn) | 0,30 | `#FFF2DC` | toàn màn | ✅ | ✅ | ✅ | ✅ | **Đạt** |
| S2 | `scare_ban_tay_giay_sau_manh` | **1** | 0 Hz | 0,34 | `#FFF2DC` | toàn màn | ✅ | ✅ | ✅ | ✅ | **Đạt** |
| S5 | `scare_mat_duoi_day_gieng` | **1** | 0 Hz | 0,28 | `#FFE9C4` | toàn màn | ✅ | ✅ | ✅ | ✅ | **Đạt** |
| S7 | `scare_anh_tho_thieu_mat` | **1** | 0 Hz | 0,32 | `#FFD9A0` | toàn màn | ✅ | ✅ | ✅ | ✅ | **Đạt** |

**Toàn Chương 1 không có một hiệu ứng nhấp nháy lặp nào.** Mọi flash đều là **một xung đơn**, ramp lên **40–50 ms**, suy giảm tuyến tính **400–500 ms**.

**Điểm nguy hiểm duy nhất còn lại** là `scare_hinh_nhan_chan_loi` (S6): màn hình đen 100 % trong 520 ms rồi sáng trở lại. Xử lý bắt buộc theo **P6**: đèn cháy lại bằng **ramp luminance 180 ms**, **không cắt khung**, và quầng đèn mở từ 90 px → 300 px trong cùng 180 ms. Sau xử lý, S6 nằm ngoài định nghĩa "flash".

### 2.3. Luật đặt `screen_flash: true` — phải thoả **cả hai** điều kiện

Không cú doạ nào được bật flash chỉ vì "cho giật hơn".

| Điều kiện | Nội dung |
|---|---|
| **(A) Nguồn sáng diegetic** | Phải có **một vật trong cảnh** giải thích được ánh sáng ấy: gáo dừa làm vỡ mặt nước hắt sáng (S1), mành nứa bật tung cho lọt sáng còn sót ngoài sân (S2), que đóm bén lửa (S5), ngọn đèn dầu trong tay người chơi chao vì luồng khí (S7). |
| **(B) Mask cut** | Flash phải **có việc để làm**: nó che khung hình đúng lúc engine tráo sprite. Flash không phục vụ mask cut là flash trang trí → **cấm**. |

Kết quả: **4 bật / 4 tắt**. `scare_di_anh_quay_mat` (S3) và `scare_khoi_tu_hinh_nguoi` (S4) ở `area_gian_tho` — **phòng đọc của chương** — bắt buộc `screen_flash: false`, vì flash làm mỏi mắt và kéo tụt khả năng đọc trong 10–15 giây kế tiếp, mà ngay sau đó người chơi còn phải đọc gia phả và văn khấn.

### 2.4. Bảng màu flash hợp lệ — danh sách đóng

Chỉ **ba mã** này được phép dùng làm overlay flash trong toàn Chương 1. Thêm mã mới phải qua kiểm P2 + P3 và có chữ ký Art Lead.

| Mã | Tên | Dùng ở | `R/(R+G+B)` | Đạt P2 |
|---|---|---|---|---|
| `#FFF2DC` | `flash_bone` — trắng ngà | S1, S2 | 0,347 | ✅ (ngưỡng cấm ≥ 0,80) |
| `#FFE9C4` | vàng nến | S5 | 0,352 | ✅ |
| `#FFD9A0` | `lamp_warm` — màu đèn dầu | S7 | 0,362 | ✅ |

**Cấm tuyệt đối làm màu flash:** mọi sắc đỏ (`votive_red #A63328`, `dieu_red #8C3A2E`), trắng tinh `#FFFFFF`, và mọi màu ngoài bảng màu chương.

### 2.5. Kiểm thế nào — quy trình đo, không phải cảm nhận

**Bắt buộc chạy trên mỗi build ứng viên (release candidate). Trượt một mục = chặn build.**

| Bước | Việc làm | Đầu ra |
|---|---|---|
| **1. Ghi hình** | Quay màn hình **60 fps, không nén mất dữ liệu (lossless / ProRes)**, độ phân giải gốc. Bao phủ: toàn bộ 5 area ở trạng thái nghỉ (mỗi area ≥ 120 s), **8 cú doạ × 2 lần**, mọi chuyển cảnh, màn hình loading, toàn bộ luồng UI gợi ý. | 1 bộ clip / build |
| **2. Chạy công cụ chuẩn** | **Harding Flash & Pattern Analyser (Harding FPA)** hoặc **PEAT** (Photosensitive Epilepsy Analysis Tool) trên toàn bộ clip. | Báo cáo PASS/FAIL |
| **3. Chạy gate tự động trong CI** | Script tính `L_rel` trung bình theo BT.709 trên **khung đã composite**, trượt cửa sổ 1.000 ms bước 1 khung, đếm số lần đổi dấu có `ΔL_rel` vượt ngưỡng P3, và tính **diện tích** vùng vượt ngưỡng theo px². Fail nếu: `flash_per_sec > 3,0` **hoặc** `ΔL_rel` vượt trần P3 **hoặc** vi phạm P2 **hoặc** vi phạm P4. | `build/reports/photosensitivity_<build_id>.json` |
| **4. Kiểm lớp cộng dồn** | Chạy lại bước 3 với **tất cả lớp FX bật đồng thời** ở area sáng nhất (`area_san_gach`) và area có LFO mạnh nhất (`area_gac_xep`, quầng đèn bám con trỏ). | Mục riêng trong cùng báo cáo |
| **5. Kiểm hồ sơ an toàn** | Lặp bước 2–3 với `gentle_mode = true` và với `photosensitive_safe = true`. Hai hồ sơ này phải **đạt với biên rộng hơn**, không chỉ "vừa đủ đạt". | 3 báo cáo / build |
| **6. Lưu vết** | Đính báo cáo vào release note. Giữ **tối thiểu 400 ngày** (khớp `retention_days` của LiveOps) để trả lời rà soát của cửa hàng. | — |

**Ngưỡng chặn build (hard gate):**

```
flash_rate_hz_max          <= 3.0      // P1, trên khung composite
red_saturated_area_pct_max <= 0        // P2, tuyet doi khong cho phep
delta_luminance_max        <= 0.10     // P3, vung > 25% dien tich
delta_luminance_max_small  <= 0.20     // P3, vung <= 25% dien tich
flash_area_px2_max_repeat  <= 518400   // P4, chuoi >= 2 xung
overlay_alpha_max_full     <= 0.35     // P4, xung don toan man
overlay_alpha_max_partial  <= 0.55     // P4, vung <= 25%
light_lfo_hz_max           <= 2.4      // P5
light_lfo_amplitude_max    <= 0.12     // P5
brightness_ramp_ms_min     >= 150      // P6
```

---

## 3. CẢNH BÁO TRƯỚC KHI VÀO GAME & CHỖ ĐỔI LẠI

### 3.1. Màn hình cảnh báo bắt buộc

Hiện **trước khi vào Chương 1**, trước `area_san_gach`, **trước mọi nội dung kinh dị**. **Không bỏ qua được trong 4 giây đầu** (chống bấm vô thức), sau đó bỏ qua được bất cứ lúc nào.

```
TRÒ CHƠI NÀY CÓ:
  • Cảnh giật mình bất ngờ (jump-scare)
  • Ánh sáng nhấp nháy đột ngột
  • Nội dung về tang lễ, cái chết của trẻ em, và hủ tục hiến tế
  • Rung phản hồi

Bạn có thể bật "Chế độ nhẹ nhàng" ngay bây giờ,
hoặc đổi bất cứ lúc nào trong Cài đặt → An toàn.
Không tuỳ chọn nào làm bạn mất nội dung hay phần thưởng.

        [ Chế độ nhẹ nhàng ]     [ Đầy đủ ]     [ Tuỳ chỉnh ]
```

**Ràng buộc của màn hình này:**

| Ràng buộc | Giá trị |
|---|---|
| Ba nút **ngang hàng về thị giác** | Cấm làm nút "Đầy đủ" to hơn, sáng hơn, hoặc đặt mặc định-nhấn-Enter. Không dark pattern. |
| Không quảng cáo, không IAP, không popup nào chồng lên | Khớp `player_safety_compliance.ads_placement_safety.never_on_safety_warning_screen = true`. |
| Không đếm ngược gây áp lực | Khớp `price_transparency.no_dark_pattern_countdown = true`. |
| Nút gợi ý bị chặn | `hint_system.hint_button.blocked_during` phải chứa `SAFETY_WARNING_SCREEN`. |
| Bản địa hoá | Toàn bộ chuỗi qua `text_key`, tiếng Việt có dấu là bản gốc. |
| Hiện lại | Mỗi lần cài mới, mỗi lần cập nhật **major**, và bất cứ lúc nào người chơi bấm "Xem lại cảnh báo" trong Cài đặt. |

### 3.2. Chỗ đổi lại: **Cài đặt → An toàn**

| Ràng buộc | Giá trị |
|---|---|
| **Vị trí** | Mục **cấp một** trong Cài đặt, **không** chôn dưới "Nâng cao" hay "Khác". Đặt **trên** mục Âm thanh và mục Tài khoản. |
| **Số lần chạm để tới** | ≤ **2 lần chạm** từ bất kỳ màn hình chơi nào (nút Cài đặt → tab An toàn). |
| **Đổi được lúc nào** | **Bất cứ lúc nào, kể cả đang trong envelope của một cú doạ.** Đổi có hiệu lực **ngay khung hình kế tiếp**, không cần khởi động lại, không cần về màn hình chính. |
| **Preset nhanh** | Ba nút: **Nhẹ nhàng** · **Đầy đủ** · **Tuỳ chỉnh** — đúng ba nút của màn hình cảnh báo, cùng nhãn, cùng nghĩa. |
| **Mô tả từng tuỳ chọn** | Mỗi tuỳ chọn có một dòng giải thích bằng tiếng Việt thường ngày. Không dùng từ kỹ thuật (`alpha`, `envelope`, `LFO`) trong UI. |
| **Nhãn trấn an** | Ngay dưới tiêu đề mục: *"Mọi tuỳ chọn ở đây đều miễn phí và không làm bạn mất nội dung hay phần thưởng nào."* |
| **Không cổng** | Không khoá theo tiến trình, không khoá theo tài khoản, không "mở khoá sau chương 1". |
| **Kích thước chạm** | Mọi nút, công tắc và tay trượt trong mục này **≥ 120 × 120 px @1920** — cùng sàn chạm với hotspot trong game (`docs/03_DATA_SPEC.md` §2.2 mức G3, `docs/01_KICH_BAN_CHAPTER_01.md` §0.3 mục X18). Người đang run tay sau một cú doạ là **đúng** người đang cần bấm trúng ngay lần đầu. Ngưỡng 88 px của bản cũ đã bị bãi bỏ. |

---

## 4. "CHẾ ĐỘ NHẸ NHÀNG" (`gentle_mode`) — ĐỊNH NGHĨA CHÍNH XÁC

### 4.1. Mười ba thay đổi, không hơn không kém

| # | Thay đổi | Từ | Thành | Vì sao |
|---|---|---|---|---|
| 1 | **Rút ngắn envelope** | 1200 ms | **≤ 500 ms** | Cắt phần "giữ" của cú doạ. Sự kiện vẫn thấy, nhưng không kéo dài đủ để kích hoạt phản ứng hoảng loạn kéo theo. |
| 2 | **Sprite không lao vào camera** | scale đỉnh 1,35–1,45 | **≤ 1,04** | Sprite xuất hiện **ở nguyên khoảng cách của nó trong cảnh**. Bàn tay vàng mã của S2 quét ở mép phải màn hình thay vì quét sát mặt kính. |
| 3 | **Tắt camera punch** | +6 % → +12 % | **0 %** | |
| 4 | **Tắt camera shake** | 4–13 px | **0 px** | |
| 5 | **Ép `screen_flash = false` toàn cục** | `true` / `false` | **luôn `false`** | Thay bằng **ramp sáng 250 ms** ở cùng vùng, biên độ ≤ **12 %**. |
| 6 | **Thay stinger bằng bản `_soft`** | `sfx_scare_*.ogg` | `sfx_scare_*_soft.ogg` | **−12 dB**, low-pass **6 kHz**, **attack ép ≥ 25 ms**. Xoá transient — đây là thay đổi quan trọng nhất: **transient mới là thứ làm giật, không phải độ to.** |
| 7 | **Giảm chênh lệch độ ồn** | ≤ 22 LU | **≤ 10 LU** | `pre_silence` không hạ về −∞ mà chỉ hạ **−12 dB**. Cú doạ không "nổ ra từ hư không". |
| 8 | **Haptic xuống mức nhẹ nhất** | 0,75–0,85 | **0,25**, hoặc **tắt hẳn** nếu `haptic_enabled = false` | |
| 9 | **Kéo dài cooldown** | 90 s | **180 s** | |
| 10 | **Kéo dài & khuếch đại tell** | −34 dBFS, 4–6 s trước | **−26 dBFS, 8–10 s trước** | Tell trở nên **nghe rõ được**. Người chơi nhận ra "sắp có chuyện" và tự chuẩn bị. |
| 11 | **Bật `scare_pre_warning`** *(tuỳ chọn con, mặc định BẬT trong chế độ nhẹ nhàng)* | không có | **Vignette mờ dần ở viền màn hình trong 1.500 ms trước cú doạ** | Dấu hiệu thị giác trung tính, **không** phải icon cảnh báo kiểu y tế. Người chơi biết trước **chính xác khi nào**. |
| 12 | **Giữ nguyên nội dung & hậu quả** | — | — | Di ảnh **vẫn** quay mặt vào vách. Hình nhân **vẫn** đứng chắn lối. Chín lỗ khoét **vẫn** hiện ra. Mọi `text_key`, mọi vật phẩm, mọi `reward_item_id` **không đổi**. |
| 13 | **KHÔNG ĐỔI** | — | — | `solution`, `max_fails`, `type`, `trigger_type`, `id`, hint tier, thời gian mở hint, thứ tự area, cảnh kết chương, mọi `hotspots[]`. |

### 4.2. Trường Master Form nào bị override lúc chạy

> **Không một tuỳ chọn nào ghi đè lên file trên đĩa.** `data/areas/*.json` luôn giữ **đủ và đúng** **6 trường** Master Form của `jumpscares[]` (`id`, `trigger_type`, `max_fails`, `audio_asset`, `sprite_animation`, `screen_flash`) với giá trị thiết kế gốc, để `tools/validate_level.py` luôn kiểm được đúng thứ designer định. Xem §8.

| Trường schema | Bị override bởi | Gốc → sau override |
|---|---|---|
| `jumpscares[].screen_flash` | `gentle_mode` · `photosensitive_safe` · `scare_intensity ≤ 0,5` | `true` → **`false`**. **Một chiều:** không tuỳ chọn nào bật flash lên được từ `false`. |
| `jumpscares[].audio_asset` | `gentle_mode` · `scare_intensity ≤ 0,5` | nối hậu tố `_soft` trước phần mở rộng: `sfx_scare_hinh_nhan.ogg` → **`sfx_scare_hinh_nhan_soft.ogg`** |
| `jumpscares[].audio_asset` | `vol_scare = 0` | → **`null`** (không phát; **cú doạ vẫn diễn ra bằng hình**) |
| `jumpscares[].sprite_animation` | `gentle_mode` · `reduce_motion` | nối hậu tố `_soft`: `anim_ban_tay_vang_ma_quet` → **`anim_ban_tay_vang_ma_quet_soft`** |
| `jumpscares[].sprite_animation` | `scare_intensity = 0` | nối hậu tố `_static`: → **`anim_ban_tay_vang_ma_quet_static`** (một khung trạng thái kết quả, không animation) |
| `jumpscares[].max_fails` | **KHÔNG BAO GIỜ** | Giữ nguyên tuyệt đối — bảo toàn chứng minh khả giải của tổ câu đố. |
| `jumpscares[].trigger_type` · `jumpscares[].id` | **KHÔNG BAO GIỜ** | |
| `puzzles[].solution` · `type` · `reward_item_id` · `wrong_action_jumpscare` | **KHÔNG BAO GIỜ** | |
| `hotspots[].*` | **KHÔNG BAO GIỜ** | |
| `chapter_id` · `area_id` · `background_asset_url` | **KHÔNG BAO GIỜ** | |

### 4.3. Quy tắc đặt tên biến thể — hợp đồng với tổ mỹ thuật và tổ âm thanh

Engine sinh tên biến thể bằng **nối hậu tố thuần tuý**. Thiếu một file = engine rơi về bản gốc = **người chơi bật chế độ an toàn vẫn ăn nguyên cú doạ đầy đủ**. Đây là lỗi mức chặn phát hành.

| Loại | Công thức | Ví dụ | Yêu cầu nội dung |
|---|---|---|---|
| Sprite giảm chuyển động | `<sprite_animation>` + `_soft` | `anim_bong_khan_xo_trong_chum_soft` | **Cùng một hình**, chỉ khác biên độ: scale đỉnh **≤ 1,04**, tốc độ **60 %**. Dùng lại **đúng seed** của bản gốc. |
| Sprite tĩnh | `<sprite_animation>` + `_static` | `anim_bong_khan_xo_trong_chum_static` | **Một khung duy nhất**, là **trạng thái kết quả** sau cú doạ. Không animation. |
| Stinger mềm | `<audio_asset>` + `_soft` trước `.ogg` | `sfx_scare_gao_dua_roi_soft.ogg` | −12 dB, low-pass 6 kHz, **attack ép ≥ 25 ms** (xoá transient). |

**Số lượng phải xuất:** 8 sprite jump-scare × 2 biến thể = **16 file sprite**, cộng **8 file stinger `_soft`**. Quy ước file xuất, bảng seed và prompt sinh biến thể nằm ở `docs/02_PROMPT_DO_HOA.md` §2.2 và §5.

### 4.4. BẢNG ĐỐI CHIẾU "MẶC ĐỊNH ↔ `gentle_mode`" CHO TỪNG JUMP-SCARE

#### 4.4.1. Mặc định — giá trị trên đĩa trong `data/areas/*.json`

| # | `scare_id` | `area_id` | `trigger_type` | `max_fails` | `screen_flash` | `audio_asset` | `sprite_animation` | Envelope | Camera | Haptic |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | `scare_bong_trong_chum` | `area_san_gach` | `ON_PUZZLE_FAIL_COUNT` | `3` | **`true`** · `#FFF2DC` α 0,30 | `sfx_scare_gao_dua_roi.ogg` | `anim_bong_khan_xo_trong_chum` | 1200 ms | punch +6 %, shake 8 px @ 9 Hz | `hap_thump_single` 0,80 |
| S2 | `scare_ban_tay_giay_sau_manh` | `area_hien_nha` | `ON_COLLECT_ITEM` | — | **`true`** · `#FFF2DC` α 0,34 | `sfx_scare_manh_nua_bat.ogg` | `anim_ban_tay_vang_ma_quet` | 1100 ms | punch +12 %, shake 12 px @ 10 Hz, tilt +2,5° | `hap_double_knock` 0,70 |
| S3 | `scare_di_anh_quay_mat` | `area_gian_tho` | `ON_COLLECT_ITEM` | — | `false` | `sfx_scare_chan_nhang_boc.ogg` | `anim_di_anh_dong_loat_quay` | 1200 ms | không punch, shake 4 px @ 6 Hz | `hap_long_rumble` 0,50 |
| S4 | `scare_khoi_tu_hinh_nguoi` | `area_gian_tho` | `ON_PUZZLE_FAIL_COUNT` | `3` | `false` | `sfx_scare_khoi_tu.ogg` | `anim_khoi_tu_dang_nguoi` | 1200 ms *(giữ tĩnh tới 12.000 ms)* | **tĩnh hoàn toàn** | `hap_long_rumble` 0,25 @ 600 ms |
| S5 | `scare_mat_duoi_day_gieng` | `area_bep_gieng` | `ON_PUZZLE_FAIL_COUNT` | `3` | **`true`** · `#FFE9C4` α 0,28 | `sfx_scare_mat_gieng.ogg` | `anim_mat_trang_ngoai_cua_bep` | 1000 ms | shake 10 px @ 8 Hz | `hap_thump_single` 0,75 |
| S6 | `scare_hinh_nhan_chan_loi` | `area_gac_xep` | `ON_ENTER_AREA` | — | `false` *(đen 520 ms → ramp 180 ms)* | `sfx_scare_hinh_nhan.ogg` | `anim_hinh_nhan_hien_gan` | 1200 ms | punch +8 % | `hap_thump_single` 0,85 |
| S7 | `scare_anh_tho_thieu_mat` | `area_gac_xep` | `ON_PUZZLE_FAIL_COUNT` | `3` | **`true`** · `#FFD9A0` α 0,32 | `sfx_scare_van_anh_lat.ogg` | `anim_chin_manh_van_lat_up` | 1200 ms | punch +10 %, shake 6 px | `hap_double_knock` 0,70 |
| S8 | `scare_ao_cuoi_quay_dau` | `area_gac_xep` | `ON_TIMER` | — | `false` | `sfx_scare_dau_nan_quay.ogg` | `anim_dau_nan_tre_quay_180` | 1200 ms | **tĩnh hoàn toàn** | `hap_long_rumble` 0,20 @ 600 ms |

#### 4.4.2. `gentle_mode = true` — giá trị sau lớp trang trí lúc chạy

| # | `scare_id` | `screen_flash` | `audio_asset` | `sprite_animation` | Envelope | Camera | Haptic | Tell | Cooldown |
|---|---|---|---|---|---|---|---|---|---|
| S1 | `scare_bong_trong_chum` | `true` → **`false`** *(ramp sáng 250 ms, ≤ 12 %)* | → `sfx_scare_gao_dua_roi_soft.ogg` | → `anim_bong_khan_xo_trong_chum_soft` | 1200 → **500 ms** | punch **0 %**, shake **0 px** | `hap_tap_light` **0,25** | −26 dBFS, **8–10 s** trước | 90 → **180 s** |
| S2 | `scare_ban_tay_giay_sau_manh` | `true` → **`false`** | → `sfx_scare_manh_nua_bat_soft.ogg` | → `anim_ban_tay_vang_ma_quet_soft` *(scale ≤ 1,04, tốc độ 60 % — bàn tay quét ở **mép phải**, không sát mặt kính)* | 1100 → **500 ms** | punch **0 %**, shake **0 px**, tilt **0°** | `hap_tap_light` **0,25** | −26 dBFS, 8–10 s | → **180 s** |
| S3 | `scare_di_anh_quay_mat` | `false` → `false` *(không đổi)* | → `sfx_scare_chan_nhang_boc_soft.ogg` | → `anim_di_anh_dong_loat_quay_soft` | 1200 → **500 ms** | shake **0 px** | `hap_tap_light` **0,25** | −26 dBFS, 8–10 s | → **180 s** |
| S4 | `scare_khoi_tu_hinh_nguoi` | `false` → `false` | → `sfx_scare_khoi_tu_soft.ogg` | → `anim_khoi_tu_dang_nguoi_soft` | 1200 → **500 ms**; `static_hold_ms` 12.000 → **4.000** | vốn đã tĩnh | `hap_tap_light` **0,25** | −26 dBFS, 8–10 s | → **180 s** |
| S5 | `scare_mat_duoi_day_gieng` | `true` → **`false`** | → `sfx_scare_mat_gieng_soft.ogg` | → `anim_mat_trang_ngoai_cua_bep_soft` | 1000 → **500 ms** | shake **0 px** | `hap_tap_light` **0,25** | −26 dBFS, 8–10 s | → **180 s** |
| S6 | `scare_hinh_nhan_chan_loi` | `false` → `false`; đoạn đen **520 → 220 ms**, ramp giữ **180 ms** | → `sfx_scare_hinh_nhan_soft.ogg` | → `anim_hinh_nhan_hien_gan_soft` | 1200 → **500 ms** | punch **0 %** | `hap_tap_light` **0,25** | −26 dBFS, 8–10 s | → **180 s** |
| S7 | `scare_anh_tho_thieu_mat` | `true` → **`false`** | → `sfx_scare_van_anh_lat_soft.ogg` | → `anim_chin_manh_van_lat_up_soft` | 1200 → **500 ms** | punch **0 %**, shake **0 px** | `hap_tap_light` **0,25** | −26 dBFS, 8–10 s | → **180 s** |
| S8 | `scare_ao_cuoi_quay_dau` | `false` → `false` | → `sfx_scare_dau_nan_quay_soft.ogg` | → `anim_dau_nan_tre_quay_180_soft` *(tốc độ 60 %)* | 1200 → **500 ms** | vốn đã tĩnh | `hap_tap_light` **0,25** | −26 dBFS, 8–10 s | → **180 s** |

**Bốn điều bảng trên KHÔNG đổi ở bất kỳ dòng nào:** `id`, `trigger_type`, `max_fails`, và **hậu quả trong thế giới**. Bảy di ảnh vẫn quay mặt vào vách vĩnh viễn (S3). Hình nhân vẫn đứng đó suốt phần còn lại của chương (S6). Chín mảnh ván vẫn lộ chín lỗ khoét rồi tự lật lại, **bố cục người chơi đang xếp giữ nguyên 100 %** (S7).

**Ngoại lệ có chủ ý ở S8 (`scare_ao_cuoi_quay_dau`):** cái đầu nan tre **vẫn quay đủ 180°**. `gentle_mode` chỉ hạ tốc độ animation và làm mềm tiếng nghiến; nó **không** cắt ngắn chuyển động này, vì cú quay đầu là **nội dung cốt truyện**, không phải hiệu ứng doạ. Áp dụng đúng nguyên tắc N4.

### 4.5. Mức cực đại: `scare_intensity = 0`

Người chơi kéo thanh trượt về **0**. Khi đó cú doạ **không có envelope nào cả**:

- `sprite_animation` → **`anim_<ten>_static`**: sprite **đã ở đó** khi cảnh hiện lại, không có chuyển động vào.
- `audio_asset` → **`null`** nếu người chơi đồng thời đặt `vol_scare = 0`; ngược lại là bản `_soft` ở mức thấp nhất.
- `screen_flash` → **`false`**. Camera, haptic → **0**.
- Kèm **một dòng mô tả ngắn ở góc dưới màn hình**, ví dụ: *"Bảy tấm di ảnh đã quay mặt vào vách."*

Đây là chế độ dành cho người chơi muốn **biết chuyện gì xảy ra** mà không chịu được cú giật. **Cốt truyện nguyên vẹn 100 %.**

| `scare_intensity` | Nghĩa |
|---|---|
| `1.0` | Đầy đủ (mặc định) |
| `0.5` | Tương đương `gentle_mode` |
| `0.0` | Không envelope — chỉ trạng thái kết quả + dòng mô tả |

---

## 5. `photosensitive_safe` — HỒ SƠ ĐỘC LẬP

Dành cho người chơi muốn **cú doạ đầy đủ** nhưng không chịu được ánh sáng. **Độc lập hoàn toàn** với `gentle_mode`; bật một cái không ép bật cái kia.

| Thay đổi | Chi tiết |
|---|---|
| Ép `screen_flash = false` toàn cục | Thay bằng **ramp sáng 250 ms**, biên độ ≤ **10 %** |
| Ép `flash_max_hz = 1.0` | Siết hơn trần chung 3,0 Hz của §2 |
| Tắt mọi LFO ánh sáng | Đèn dầu, than hồng, hương vòng, quầng đèn bám con trỏ → **độ sáng tĩnh** |
| Giảm tương phản chuyển cảnh | Fade đen ↔ sáng kéo từ 250 ms lên **600 ms** |
| S6: đoạn đen 520 ms | Thay bằng **fade 400 ms** thay vì tắt phụt |
| **Giữ nguyên** | Envelope 1200 ms, camera punch/shake, haptic, âm thanh đầy đủ, cooldown 90 s, tell 4–6 s |

---

## 6. HAPTIC, RUNG LẮC MÀN HÌNH, ÂM LƯỢNG STINGER

### 6.1. Bảng tuỳ chọn

| Tuỳ chọn (nhãn UI) | Khoá JSON | Kiểu / mặc định | Hành vi |
|---|---|---|---|
| **Tắt rung** | `haptic_enabled` | `bool`, mặc định `true` | **Mọi lệnh haptic bị bỏ qua hoàn toàn.** **Không** thay thế bằng âm thanh hay hình ảnh bù — thay thế sẽ làm lộ ra chỗ lẽ ra có rung và phá trải nghiệm. **Tự đặt `false`** nếu OS báo "Reduce Motion" hoặc rung hệ thống đang tắt. |
| **Cường độ rung** | `haptic_intensity` | `float 0.0–1.0`, mặc định `1.0` | Nhân với cường độ của pattern. |
| **Tắt rung lắc màn hình** | `screen_shake_scale` | `float 0.0–1.0`, mặc định `1.0` | Nhân với `camera_shake_px`. `0.0` = **tắt hẳn**, không còn một pixel dịch chuyển nào. |
| **Giảm chuyển động** | `reduce_motion` | `bool`, mặc định `false` | **Gói tổng**: ép `screen_shake_scale = 0`, `camera_punch_pct = 0`, tắt parallax nền, tắt hiệu ứng zoom khi vào câu đố (thay bằng cross-fade 200 ms), giảm tốc độ mọi sprite animation của jump-scare còn **60 %** (dùng biến thể `_soft`). **Tự bật** nếu OS báo `prefers-reduced-motion`. |
| **Giảm âm cú doạ** | `vol_scare` | `float 0.0–1.0`, mặc định `1.0` | Bus `BUS_SCARE` **độc lập** với ambience, foley, nhạc và thoại. Kéo về `0.0` = **không nghe stinger nào**, vẫn nghe đủ thoại và không khí, **cú doạ vẫn diễn ra bằng hình**. |
| **Giới hạn độ ồn đỉnh** | `peak_limit_db` | `0` (tắt) / `−6` / `−12`, mặc định `0` | Hạ trần `BUS_SCARE` tương ứng. Dành cho người chơi dùng tai nghe ban đêm. |

### 6.2. Bốn pattern haptic chuẩn và cách chúng bị hạ cấp

| `haptic_pattern` | Thông số gốc | Dùng ở | Sau `gentle_mode` | Sau `haptic_enabled = false` |
|---|---|---|---|---|
| `hap_tap_light` | 12 ms, cường độ 0,30 | Snap nấc ổ khoá, bước thang, đuôi các cú doạ | 0,25 | **`null`** |
| `hap_thump_single` | 40 ms, cường độ 0,75–0,85 | S1, S5, S6 | → `hap_tap_light` 0,25 | **`null`** |
| `hap_double_knock` | 25 ms · nghỉ 60 ms · 25 ms, cường độ 0,70 | S2, S7 | → `hap_tap_light` 0,25 | **`null`** |
| `hap_long_rumble` | 220 ms, cường độ 0,20–0,50, ramp xuống | S3, S4, S8 | → `hap_tap_light` 0,25 | **`null`** |

**Luật kỹ thuật bắt buộc:**
- iOS: `UIImpactFeedbackGenerator` (light/medium/heavy) + `CHHapticEngine` cho pattern có ramp. Android: `VibrationEffect.createWaveform`.
- Máy **không có haptic engine** → **bỏ qua im lặng**. Cấm thay bằng rung thô của motor ERM: một xung ERM kéo dài 400 ms sẽ phá hoàn toàn timing của envelope.
- Không bao giờ đặt haptic > 0,5 ở mốc **0 ms** cho một **dread scare** (S4, S8) — làm vậy biến nó thành impulse scare.

### 6.3. LUẬT NGHỈ 90 GIÂY GIỮA HAI CÚ DOẠ — và điều kiện miễn trừ duy nhất

> **Tài liệu này là chủ sở hữu của luật 90 giây.** Mọi tài liệu khác trích dẫn về đây: `docs/03_DATA_SPEC.md` §2.7.9 (`cooldown_sec`, `cooldown_exempt`), `docs/04_LIVEOPS_MONETIZATION.md` §7.1 (`ad_cooldown_after_scare_sec`) và §9.1 mục 16.

**Luật:** giữa hai cú doạ bất kỳ phải có **tối thiểu 90 giây**. Trong dữ liệu, luật này được khai bằng `jumpscares[].cooldown_sec: 90`. Lý do là sinh lý chứ không phải nhịp kể: nhịp tim và mức cortisol cần khoảng một phút rưỡi để về nền; doạ dồn dập không làm người chơi sợ hơn, nó làm người chơi **tê**, và cú doạ thứ ba trở đi mất sạch hiệu lực.

**Cùng con số, ba nơi, phải bằng nhau:**

| Nơi | Khoá | Giá trị |
|---|---|---|
| `data/areas/*.json` | `jumpscares[].cooldown_sec` | **90** |
| `data/liveops_chapter_01.json` | `ad_cooldown_after_scare_sec` | **90** — chỉ được **tăng**, không bao giờ hạ (§10.2) |
| Cửa sổ cấm quảng cáo | `WITHIN_90S_AFTER_ANY_JUMPSCARE` | **90** |

Trong `gentle_mode`, con số này **tăng lên 180 giây** (§4.1 mục 9, §8.2). Tăng thì được, hạ thì không — đây là chiều duy nhất mà tuỳ chọn an toàn được phép đi.

#### 6.3.1. Điều kiện miễn trừ — cả bốn phải đúng cùng lúc

Một cú doạ được phép **không khai** `cooldown_sec` khi và chỉ khi nó thoả **cả bốn** điều kiện sau. Thiếu một điều là mất quyền miễn trừ:

Đây là **nguyên văn luật miễn trừ đã ghi ở `01_KICH_BAN_CHAPTER_01.md` §6.6**, viết lại dưới dạng bảng để QA soát được từng dòng:

```
mien_tru  ==  (impulse == false)
          AND (screen_flash == false)
          AND (camera_punch_pct == 0)
          AND (haptic_pattern_at_0ms == null)
```

| # | Điều kiện | Kiểm bằng |
|---|---|---|
| 1 | `impulse == false` — **không transient**: attack của stinger ép ≥ 25 ms, không có xung sắc ở mốc 0 ms | Đo envelope file `.ogg`, §2.5 |
| 2 | `screen_flash == false` | Đọc thẳng từ `data/areas/*.json` |
| 3 | `camera_punch_pct == 0` (và `camera_shake_px == 0`) | Bảng §4.4.1 |
| 4 | `haptic_pattern_at_0ms == null` — tức không có haptic > 0,5 ở mốc 0 ms (§6.2) | Bảng pattern haptic §6.2 |

Cú doạ thoả cả bốn là **dread scare** (hoặc ambience scare): nó không tạo phản xạ giật mình, nên nó không tiêu hao quỹ sinh lý mà luật 90 giây bảo vệ.

#### 6.3.2. Khai miễn trừ thế nào — bằng dữ liệu, không bằng văn xuôi

Đặt `"cooldown_exempt": true` **và** kèm `ghi_chu_vi` nêu rõ căn cứ. Trường boolean là thứ trình kiểm đọc được; `ghi_chu_vi` là thứ người sau đọc được. Cần cả hai.

**Hai cú doạ THOẢ điều kiện, nhưng chỉ MỘT thực sự dùng quyền miễn trừ:**

| Cú doạ | `trigger_type` | Thoả 4 điều kiện? | Có dùng miễn trừ không? |
|---|---|---|---|
| `scare_ao_cuoi_quay_dau` (S8, cú đóng chương) | `ON_TIMER`, `delay_sec: 0.4` | **Có** — dread scare thuần: `screen_flash: false`, không punch, không shake, `hap_long_rumble` ramp **lên** chứ không đánh ở mốc 0 ms | **CÓ.** `cooldown_exempt: true`, không khai `cooldown_sec`. Nó cũng là **cú cuối cùng của chương** — không có cú nào sau nó để mà giữ khoảng nghỉ |
| `scare_khoi_tu_hinh_nguoi` (S4) | `ON_PUZZLE_FAIL_COUNT`, `max_fails: 3` | **Có** — `screen_flash: false`, dread scare | **KHÔNG — tự nguyện tuân thủ.** Vẫn khai `cooldown_sec: 90`. Lý do ở `01_KICH_BAN_CHAPTER_01.md` §6.6: nó nằm trong `area_gian_tho`, khu vực **còn một cú doạ khác** (`scare_di_anh_quay_mat`, S3, là impulse thật). Miễn trừ cho S4 sẽ làm cặp S4 → S3 dồn sát nhau |

Bảy cú doạ còn lại đều khai `cooldown_sec: 90`. Một cú doạ thiếu `cooldown_sec` mà **không** khai `cooldown_exempt: true` là **[CẢNH BÁO]** của bất biến B15 (`docs/03_DATA_SPEC.md` §5.1); khai `cooldown_exempt: true` mà **không** thoả bốn điều kiện ở §6.3.1 là **[LỖI] nghiệm thu** của §11.

> **Luật miễn trừ KHÔNG phải luật bắt buộc dùng.** Thoả điều kiện chỉ cho *quyền*; quyết định dùng hay không thuộc về nhịp kinh dị, mà chủ sở hữu là `01_KICH_BAN_CHAPTER_01.md` §6.4–§6.7. Tài liệu này chỉ đặt **trần an toàn**, không đặt sàn nhịp.

#### 6.3.3. Ba cơ chế khác của nhịp nghỉ mà tài liệu này KHÔNG sở hữu

Luật 90 giây không đứng một mình. Ba cơ chế dưới đây do `01_KICH_BAN_CHAPTER_01.md` sở hữu; ghi ra đây để QA không đi tìm nhầm chỗ, và để không ai "tối ưu" mất chúng khi chỉnh tuỳ chọn an toàn:

| Cơ chế | Chủ sở hữu | Vì sao nó cũng là chuyện an toàn |
|---|---|---|
| **Năm khoá hoãn L1–L5** (khoá đọc, khoá cửa, khoá hành trang, **khoá gợi ý**, khoá hồi phục) | `01` §6.5 | **L4 — khoá gợi ý** là ràng buộc an toàn trực tiếp: người đang bế tắc là người đang bực, doạ lúc bực sinh ra giận chứ không sinh ra sợ. Nó khớp với ràng buộc của `docs/04_LIVEOPS_MONETIZATION.md` §2.6 (bảng gợi ý bị chặn trong `JUMPSCARE_ENVELOPE`) — **hai chiều, cả hai đều phải giữ** |
| **HOÃN chứ không HUỶ** (`ARMED`) + bốn cặp rủi ro S1→S2, S4→S3, S6→S7, S7→S8 | `01` §6.6 | Cú doạ bị hoãn **chuyển sang biến thể dread**, không biến mất. Đây cùng một triết lý với §1.3 ở đây: *hạ tải sinh lý, giữ nguyên sự kiện* |
| **Trần cứng `SCARE_MAX_PER_CHAPTER = 10`** | `01` §6.6 | Chạm trần → mọi cú còn lại chuyển vĩnh viễn sang biến thể dread câm. Đây là một **`gentle_mode` tự động** dành cho người chơi kém nhất, và nó chạy **kể cả khi người chơi chưa bật gì cả** |

---

## 7. CÁC TUỲ CHỌN CÒN LẠI

### 7.1. Bảng đầy đủ

| Tuỳ chọn | Khoá JSON | Mặc định | Hành vi |
|---|---|---|---|
| Thanh trượt cường độ doạ | `scare_intensity` | `1.0` | `1.0` đầy đủ · `0.5` = `gentle_mode` · `0.0` = không envelope (§4.5) |
| Báo trước cú doạ | `scare_pre_warning` | `false` *(mặc định BẬT trong `gentle_mode`)* | Vignette mờ dần ở viền màn hình **1.500 ms** trước cú doạ |
| Âm lượng riêng theo bus | `vol_amb` · `vol_drn` · `vol_fol` · `vol_mus` · `vol_vox` · `vol_ui` · `vol_scare` | `1.0` | `vol_scare` kéo được về `0` **độc lập** với các bus khác |
| Phụ đề cho âm thanh | `subtitle_sfx` | `false` | Hiện mô tả chữ cho **âm thanh có nghĩa**: *"[tiếng chuông vọng sau vách — ba tiếng]"*, *"[một tiếng mõ chốt hồi]"*, *"[tiếng nước dội dưới giếng]"*. **Bắt buộc phải có** — xem §7.2 |
| Giới hạn độ ồn đỉnh | `peak_limit_db` | `0` | `−6` / `−12` |

### 7.2. Ràng buộc bắt buộc: `puz_ba_hoi_chin_tieng` và người chơi khiếm thính

`puz_ba_hoi_chin_tieng` là câu đố kiểu **`AUDIO_MATCH`**. Nó **không được phép** là bức tường chặn người chơi khiếm thính hoặc người chơi tắt tiếng (chơi nơi công cộng).

**Giải pháp — bắt buộc triển khai, KHÔNG phải tuỳ chọn:**

> **Nhạc khí — đọc trước, đây là chỗ hay bị chép sai (hoán vai X14, `01_KICH_BAN_CHAPTER_01.md` §3.3.6).** **CHUÔNG ĐỒNG** mang trọn phần *"ba hồi chín tiếng"* — cả sáu cụm mã hoá trong `solution` `[3, 3, 5, 3, 7, 3]` đều là **số tiếng chuông**. **MÕ** giữ đúng một vai: **điểm một tiếng chốt khép mỗi hồi**, ba lần trong cả bài, và con số ấy **không** nằm trong mảng. Chuông là thứ **gọi**, mõ là thứ **chốt**.

1. Khi bên kia vách gõ, một **thanh nhịp trực quan** ở cạnh dưới màn hình hiện từng xung — **chấm tròn** cho tiếng **chuông**, **chấm vuông** cho tiếng **mõ**, cộng **một vạch ngắt dọc** mỗi lần một cụm tự chốt — đồng bộ từng mili-giây. Người chơi nhìn thấy **đúng thứ engine đang kiểm**: số tiếng mỗi cụm, và thứ tự chuông/mõ.
2. **Hai mẫu haptic phân biệt được bằng tay**, để người chơi vừa khiếm thính vừa tắt màn hình vẫn đếm được: **chuông** = xung **12 ms, biên độ 0,35** (sắc, ngắn); **mõ** = xung **30 ms, biên độ 0,70** (nặng, đục). Nếu `haptic_enabled = true`, người chơi giải được câu đố **hoàn toàn bằng xúc giác**. Khi `haptic_enabled = false`, kênh thị giác ở điểm 1 phải đủ một mình — nó **không** được phép là kênh phụ.
3. Nút **"Nghe lại"**: **không giới hạn số lần, không tính là lần sai** — tức không đẩy `fail_count` lên và không kích hoạt `scare_khoi_tu_hinh_nguoi`.
4. **Đường giải bằng chữ số luôn tồn tại**: gợi ý Tier 2 hiện thẳng dãy số của lời giải.

> **Ràng buộc bất biến:** không giải pháp trợ năng nào ở đây được **đổi `solution`** của `puz_ba_hoi_chin_tieng`, cũng không được đổi `max_fails`. Chúng chỉ mở thêm **kênh cảm nhận** (thị giác, xúc giác) cho **cùng một lời giải**.

---

## 8. KIẾN TRÚC OVERRIDE — LỚP TRANG TRÍ, KHÔNG SỬA DỮ LIỆU GỐC

### 8.1. Thứ tự ưu tiên

**Không tuỳ chọn nào ghi đè lên file trong `data/areas/*.json`.** File trên đĩa luôn giữ giá trị thiết kế gốc và **đủ toàn bộ trường Master Form**, để `tools/validate_level.py` luôn kiểm được đúng thứ designer định. Override xảy ra ở **lớp trang trí lúc chạy** (`ScareConfigResolver`):

```
gia tri goc trong data/areas/<area_id>.json          (nguon su that, bat bien - TANG 2)
        v
ho so an toan (gentle_mode / photosensitive_safe / reduce_motion)
        v
tuy chon le do nguoi choi dat trong persistent/      (thang tat ca)
        v
=> ScareRuntimeConfig thuc thi (chi ton tai trong bo nho, khong ghi ra dia)
```

> **⚠️ `data/config/scare_runtime.json` KHÔNG TỒN TẠI — và ở kiến trúc hôm nay thì nó không cần tồn tại.** Bản trước của mục này đặt một tầng *"giá trị bổ sung trong `data/config/scare_runtime.json` (theo `scare_id`)"* vào giữa sơ đồ. **Đường dẫn ấy không có trong repo**, và nó cũng **không nằm trong kiến trúc ba tầng** của `docs/03_DATA_SPEC.md` §1 (tầng 1 `data/chapter_01.json` · tầng 2 `data/areas/*.json` · tầng 3 `data/liveops_chapter_01.json`). Một tầng dữ liệu thứ tư không ai khai báo là một tầng không validator nào kiểm.
>
> **Mọi giá trị bản trước định đặt vào file ấy đều đã có chỗ:** thông số doạ trên đĩa nằm ở `jumpscares[]` của `data/areas/*.json` và được in đầy đủ ở **§4.4.1**; phép biến đổi theo hồ sơ an toàn nằm ở **§4.4.2** và **§8.2** ngay dưới; tuỳ chọn của người chơi nằm ở `persistent/player_settings.json` (**§8.3**). `ScareRuntimeConfig` là **đối tượng dựng trong bộ nhớ** bởi `ScareConfigResolver`, không phải một file.

### 8.2. Trường runtime bị ảnh hưởng (trường của `ScareRuntimeConfig` **trong bộ nhớ**)

> **Đọc bảng này thế nào.** Cột đầu **không** phải khoá trong một file JSON — không có file nào tên `scare_runtime.json` trong repo (§8.1). Đó là tên **trường của đối tượng `ScareRuntimeConfig`** mà `ScareConfigResolver` dựng lúc chạy. Giá trị khởi điểm của mỗi trường lấy từ `jumpscares[]` trong `data/areas/*.json` khi trường ấy có mặt trên đĩa (`screen_flash`, `audio_asset`, `sprite_animation`, `cooldown_sec`, `delay_sec`, `max_fails`, `trigger_item_id`), và từ bảng **§4.4.1** của tài liệu này khi không — envelope, camera, haptic, tell và `loudness_jump_lu_max` **không** nằm trên đĩa, chúng là hợp đồng do tài liệu này sở hữu.

| Trường runtime | `gentle_mode` | `photosensitive_safe` | `reduce_motion` | `haptic_enabled = false` |
|---|---|---|---|---|
| `duration_ms` | 1200 → **500** | giữ | giữ | giữ |
| `pre_silence_ms` | giữ **2000**, nhưng đáy chỉ **−12 dB** thay vì −∞ | giữ | giữ | giữ |
| `tell_lead_ms` | 4000–6000 → **8000–10000** | giữ | giữ | giữ |
| `tell_gain_db` | −34 → **−26** | giữ | giữ | giữ |
| `flash_alpha` | → **0** | → **0** | giữ | giữ |
| `flash_color` | → không dùng | → không dùng | giữ | giữ |
| `camera_punch_pct` | → **0** | giữ | → **0** | giữ |
| `camera_shake_px` | → **0** | giữ | → **0** × `screen_shake_scale` | giữ |
| `camera_tilt_deg` | → **0** | giữ | → **0** | giữ |
| `sprite_scale_peak` | 1,35–1,45 → **≤ 1,04** | giữ | → **× 0,6 biên độ** | giữ |
| `haptic_pattern` | → `hap_tap_light` | giữ | giữ | → **`null`** |
| `haptic_intensity` | → **0,25** | giữ | giữ | → **0** |
| `cooldown_sec` | 90 → **180** | giữ | giữ | giữ |
| `loudness_jump_lu_max` | 22 → **10** | giữ | giữ | giữ |
| `pre_warning_ms` | 0 → **1500** | giữ | giữ | giữ |
| `static_hold_ms` *(chỉ S4)* | 12000 → **4000** | giữ | giữ | giữ |

### 8.3. File cài đặt người chơi

`persistent/player_settings.json` — **không** nằm trong bundle, **không** nằm trong repo dữ liệu, **không** đồng bộ lên server như điều kiện chơi:

```json
{
  "safety": {
    "gentle_mode": false,
    "photosensitive_safe": false,
    "reduce_motion": false,
    "scare_intensity": 1.0,
    "scare_pre_warning": false,
    "haptic_enabled": true,
    "haptic_intensity": 1.0,
    "screen_shake_scale": 1.0,
    "subtitle_sfx": false,
    "peak_limit_db": 0
  },
  "audio": {
    "vol_master": 1.0,
    "vol_amb": 1.0,
    "vol_drn": 1.0,
    "vol_fol": 1.0,
    "vol_mus": 1.0,
    "vol_vox": 1.0,
    "vol_ui": 1.0,
    "vol_scare": 1.0
  }
}
```

**Ba ràng buộc của file này:**
1. Đọc được và ghi được **offline**, không cần đăng nhập, không cần mạng.
2. Mất file (cài lại, xoá dữ liệu) → quay về mặc định **và màn hình cảnh báo §3.1 hiện lại**.
3. **Không** có bất kỳ trường nào liên quan tới gem, IAP, quảng cáo hay tiến trình. An toàn và tiền tệ nằm ở hai file khác nhau, **có chủ ý**.

---

## 9. ĐỐI CHIẾU TUÂN THỦ CỬA HÀNG ỨNG DỤNG

### 9.1. Phân loại độ tuổi và mô tả nội dung

Khớp `player_safety_compliance.age_rating` trong `data/liveops_chapter_01.json`.

| Cửa hàng / hệ | Mức nhắm | Căn cứ |
|---|---|---|
| Apple App Store | **17+** | Kinh dị, giật mình thường xuyên, đề tài cái chết của trẻ em |
| Google Play (IARC) | **Mature 17+** | Cùng bộ câu trả lời bảng hỏi IARC |
| PEGI | **16** | Horror, fear |
| ESRB | **Mature 17+** | — |
| Việt Nam | **16+** *(dự kiến — cần bộ phận pháp chế xác nhận theo quy định phân loại trò chơi điện tử trên mạng hiện hành)* | — |

**Bảy mô tả nội dung bắt buộc khai báo** (`age_rating.content_descriptors_vi`): *Kinh dị · Cảnh giật mình · Đề tài tang lễ · Cái chết của trẻ em · Hủ tục hiến tế · Ánh sáng nhấp nháy · Rung phản hồi.*

`store_questionnaire_answers_locked = true` — bảng hỏi phân loại **khoá lại**, đổi phải qua Legal, để mô tả trên trang cửa hàng không bao giờ nhẹ hơn nội dung thật.

### 9.2. Checklist tuân thủ theo từng hạng mục

| Hạng mục | Yêu cầu | Ta đáp ứng bằng |
|---|---|---|
| **Cảnh báo nhạy sáng** | Cảnh báo hiện **trước** nội dung, dễ đọc, không bỏ qua được ngay | §3.1 — khoá 4 giây, 3 nút ngang hàng |
| **Ngưỡng nhấp nháy** | Đạt ngưỡng công nghiệp về ánh sáng nhấp nháy (WCAG 2.1 SC 2.3.1 "Three Flashes or Below Threshold", SC 2.3.2, và kiểm Harding FPA) | §2.1 P1–P6, §2.5 quy trình đo, báo cáo lưu 400 ngày |
| **Trợ năng hệ điều hành** | Tôn trọng cờ hệ thống của máy | `reduce_motion` **tự bật** theo `prefers-reduced-motion` (iOS Reduce Motion / Android Remove animations); `haptic_enabled` **tự tắt** theo rung hệ thống |
| **Trợ năng thính giác** | Nội dung âm thanh có nghĩa phải có kênh thay thế | `subtitle_sfx` + thanh nhịp trực quan + haptic cho `puz_ba_hoi_chin_tieng` (§7.2) |
| **Không bán trợ năng** | Trợ năng không được là hàng hoá | §1 N1–N3, 5 cờ `*_free` (§10), `accessibility_never_gated = true` |
| **Quảng cáo** | Không xen quảng cáo vào lúc dễ tổn thương | `no_interstitial_ads`, `rewarded_opt_in_only`, `never_interrupt_jumpscare`, `min_sec_after_jumpscare: 90`, `never_on_safety_warning_screen` |
| **Quảng cáo theo độ tuổi** | Không quảng cáo cho người dưới tuổi; lọc nội dung quảng cáo | `no_ads_for_under_age_users`, `ad_content_rating_max`, chặn cờ bạc/rượu bia/hẹn hò/giả lập giao diện hệ thống |
| **Không hộp quà ngẫu nhiên** | Minh bạch nội dung mọi thứ trả phí | `no_loot_box.randomized_paid_rewards = false` |
| **Minh bạch giá** | Giá bản địa hoá + danh sách nội dung + xác nhận hai bước, không đếm ngược gây áp lực | `price_transparency.*` |
| **Bảo vệ chi tiêu** | Trần chi mềm, không mời mua đúng lúc căng thẳng | `spending_protection.daily_spend_soft_cap_usd`, `no_purchase_prompt_during_horror_peak = true` |
| **Quyền riêng tư dữ liệu** | Không PII trong telemetry, có đồng thuận, xoá được theo yêu cầu | `data_privacy.*` (GDPR, GDPR-K, CCPA, Nghị định 13/2023/NĐ-CP) |

### 9.3. Ba câu trả lời sẵn cho rà soát của cửa hàng

| Câu hỏi thường gặp khi rà soát | Trả lời + bằng chứng đính kèm |
|---|---|
| *"Game có ánh sáng nhấp nháy. Đã kiểm ngưỡng chưa?"* | Rồi. Đính `build/reports/photosensitivity_<build_id>.json` cho cả 3 hồ sơ (mặc định, `gentle_mode`, `photosensitive_safe`) + báo cáo Harding FPA. Trần cứng: **≤ 3,0 Hz**, không có chuỗi nhấp nháy lặp nào trong toàn chương. |
| *"Tuỳ chọn trợ năng có bị tính phí hoặc khoá sau tiến trình không?"* | Không. 5 cờ `accessibility_never_monetized.*` đều `true`, `hint_system.constraints.accessibility_never_gated = true`, và mọi tuỳ chọn bật được **ngay màn hình đầu tiên** trước nội dung kinh dị. |
| *"Mô tả nội dung trên trang cửa hàng có đủ không?"* | Đủ 7 mô tả (§9.1), khớp đúng bảng hỏi đã khoá, và cùng nội dung ấy hiện lại trong game ở màn hình cảnh báo §3.1. |

---

## 10. BẢNG TRUY VẾT — TUỲ CHỌN AN TOÀN ↔ `data/liveops_chapter_01.json`

Cột "Khoá cấu hình" là **đường dẫn JSON nguyên văn** trong `data/liveops_chapter_01.json`. QA và LiveOps dùng bảng này để kiểm từng dòng.

### 10.1. Cờ "không bao giờ bán trợ năng"

| Tuỳ chọn an toàn | Khoá trong `data/liveops_chapter_01.json` | Giá trị bắt buộc | Ý nghĩa |
|---|---|---|---|
| Chế độ nhẹ nhàng | `player_safety_compliance.accessibility_never_monetized.gentle_mode_free` | `true` | `gentle_mode` miễn phí vĩnh viễn |
| Hồ sơ nhạy sáng | `player_safety_compliance.accessibility_never_monetized.photosensitive_safe_free` | `true` | `photosensitive_safe` miễn phí |
| Giảm chuyển động | `player_safety_compliance.accessibility_never_monetized.reduce_motion_free` | `true` | `reduce_motion` miễn phí |
| Tắt / giảm rung | `player_safety_compliance.accessibility_never_monetized.haptic_toggle_free` | `true` | `haptic_enabled`, `haptic_intensity` miễn phí |
| Phụ đề âm thanh | `player_safety_compliance.accessibility_never_monetized.subtitle_free` | `true` | `subtitle_sfx` miễn phí — điều kiện sống còn của `puz_ba_hoi_chin_tieng` |
| **Toàn bộ trợ năng** | `hint_system.constraints.accessibility_never_gated` | `true` | Không cổng tiến trình, không cổng tiền tệ, không cổng quảng cáo |

### 10.2. Chống quảng cáo / mời mua chen vào lúc dễ tổn thương

| Ràng buộc an toàn | Khoá trong `data/liveops_chapter_01.json` | Giá trị bắt buộc |
|---|---|---|
| Không quảng cáo trên màn hình cảnh báo §3.1 | `player_safety_compliance.ads_placement_safety.never_on_safety_warning_screen` | `true` |
| Không quảng cáo xen giữa envelope cú doạ | `player_safety_compliance.ads_placement_safety.never_interrupt_jumpscare` | `true` |
| Khoảng cách tối thiểu sau cú doạ | `player_safety_compliance.ads_placement_safety.min_sec_after_jumpscare` | `90` |
| Không quảng cáo tự bật | `player_safety_compliance.ads_placement_safety.no_interstitial_ads` · `.rewarded_opt_in_only` | `true` · `true` |
| Không quảng cáo giữa thao tác giải đố / cutscene | `.never_interrupt_puzzle_input` · `.never_interrupt_cutscene` | `true` · `true` |
| Không mời mua đúng đỉnh kinh dị | `player_safety_compliance.spending_protection.no_purchase_prompt_during_horror_peak` | `true` |
| Nút gợi ý bị chặn ở màn cảnh báo & trong envelope | `hint_system.hint_button.blocked_during` | phải chứa `SAFETY_WARNING_SCREEN`, `JUMPSCARE_ENVELOPE`, `CUTSCENE`, `AREA_TRANSITION` |
| Không quảng cáo ngay khoảnh khắc giải sai | `hint_system.constraints.no_ad_inside_puzzle_fail_moment` | `true` |
| `max_fails` không bị override bởi bất cứ thứ gì | `hint_system.constraints.max_fails_never_overridden` | `true` |

### 10.3. Khai báo nội dung & phân loại

| Ràng buộc an toàn | Khoá trong `data/liveops_chapter_01.json` | Giá trị bắt buộc |
|---|---|---|
| 7 mô tả nội dung của màn cảnh báo §3.1 | `player_safety_compliance.age_rating.content_descriptors_vi` | phải chứa `"Ánh sáng nhấp nháy"` và `"Rung phản hồi"` |
| Bảng hỏi phân loại khoá lại | `player_safety_compliance.age_rating.store_questionnaire_answers_locked` | `true` |
| Không quảng cáo cho người dưới tuổi | `player_safety_compliance.age_rating.no_ads_for_under_age_users` | `true` |
| Cần Legal duyệt trước phát hành | `player_safety_compliance.age_rating.legal_review_required` | `true` |

### 10.4. Đo lường hiệu quả của chính sách an toàn (telemetry)

| Cái ta cần biết | Khoá / sự kiện trong `data/liveops_chapter_01.json` | Tham số dùng |
|---|---|---|
| Hồ sơ an toàn của mọi sự kiện | `telemetry.common_params` | `safety_profile` |
| Bao nhiêu người cần chế độ nhẹ nhàng, đổi ở đâu, sau cú doạ nào | `telemetry` — sự kiện `safety_setting_change` | `setting_key`, `old_value`, `new_value`, `changed_at_screen`, `after_scare_id` |
| Cú doạ nào thực sự bắn, có flash hay không, cách cú trước bao lâu | `telemetry` — sự kiện `jumpscare_play` | `scare_id`, `area_id`, `trigger_type`, `intensity_profile`, `screen_flash_applied`, `deferred_by_cooldown`, `sec_since_last_scare` |
| Cú doạ nào làm người chơi thoát app | `telemetry` — sự kiện `jumpscare_quit_signal` | `scare_id`, `area_id`, `sec_after_scare`, `safety_profile` |

> **Luật đọc số:** nếu `jumpscare_quit_signal` của một `scare_id` vượt **3 %** lượt gặp, cú doạ ấy phải được xem lại ở bản vá — **hạ cường độ mặc định**, tuyệt đối không "đẩy người chơi sang chế độ nhẹ nhàng rồi coi như xong".

### 10.5. Kill switch liên quan

| Tình huống | Khoá | Ghi chú |
|---|---|---|
| Sự cố nhạy sáng phát hiện sau phát hành | `rollout.kill_switches.kill_switch_event_theme` | Tắt theme sự kiện (nguồn `override_bg` mới) để loại biến số đồ hoạ trong khi điều tra |
| Sự cố quảng cáo chen vào envelope | `rollout.kill_switches.kill_switch_ads` | Tắt toàn bộ quảng cáo ngay, không cần bản vá |

> **Cấm tuyệt đối:** **không** tạo kill switch nào tắt được các tuỳ chọn an toàn. Không có `kill_switch_gentle_mode`, không có `kill_switch_accessibility`. Trợ năng không phải là tính năng có thể tắt từ xa.

### 10.6. Sáu khoá Master Form — không đụng tới

| Khoá Master Form | Quan hệ với an toàn |
|---|---|
| `hint_cost_gems` | **Không liên quan.** Không tuỳ chọn an toàn nào đọc, ghi hay phụ thuộc vào nó. |
| `ads_reward_hints` | **Không liên quan.** |
| `iap_product_id` | **Không liên quan.** Không có sản phẩm nào bán tuỳ chọn an toàn. |
| `price_usd` | **Không liên quan.** |
| `event_start` | **Không liên quan.** Tuỳ chọn an toàn không theo mùa, không theo sự kiện. |
| `override_bg` | Chỉ ràng buộc một chiều: **mọi `override_bg` của mọi sự kiện đều phải qua kiểm §2.5** trước khi bật, y như bối cảnh gốc. |

---

## 11. CHECKLIST NGHIỆM THU — TRƯỢT MỘT MỤC LÀ CHẶN BUILD

**Nhạy sáng (§2)**
- [ ] Báo cáo Harding FPA / PEAT **PASS** cho cả 3 hồ sơ: mặc định, `gentle_mode`, `photosensitive_safe`.
- [ ] Gate CI đo trên **khung đã composite** (không đo từng lớp) — `flash_rate_hz ≤ 3,0` ở mọi cửa sổ trượt 1 s.
- [ ] Đã chạy riêng ca **cộng dồn nhiều lớp FX** ở `area_san_gach` và `area_gac_xep`.
- [ ] Không overlay flash nào dùng màu ngoài 3 mã ở §2.4. Không sắc đỏ, không `#FFFFFF`.
- [ ] `scare_hinh_nhan_chan_loi` (S6): đèn cháy lại bằng **ramp ≥ 180 ms**, không cắt khung.
- [ ] Mọi LFO ánh sáng ≤ 2,4 Hz, biên độ ≤ ±12 %.

**Chế độ nhẹ nhàng (§4)**
- [ ] Đủ **16 file sprite** biến thể (`_soft` + `_static`) cho **cả 8** jump-scare, tên nối hậu tố đúng §4.3.
- [ ] Đủ **8 file stinger** `_soft`: −12 dB, low-pass 6 kHz, attack ≥ 25 ms.
- [ ] Bật `gentle_mode` → chạy hết chương: **không** cú nào còn flash, punch, shake. Envelope ≤ 500 ms ở cả 8 cú.
- [ ] Bật `gentle_mode` → **mọi hậu quả trong thế giới vẫn xảy ra** (di ảnh quay mặt, hình nhân chắn lối, chín lỗ khoét, đầu nan tre quay đủ 180°).
- [ ] `scare_intensity = 0` → sprite `_static` + dòng mô tả hiện đúng ở cả 8 cú.
- [ ] **Không file biến thể nào bị thiếu.** Thiếu 1 file = engine rơi về bản gốc = người chơi bật chế độ an toàn vẫn ăn cú doạ đầy đủ. **Chặn build.**

**Bất biến dữ liệu (§1.2, §4.2, §8)**
- [ ] `tools/validate_level.py` chạy sạch: `data/areas/*.json` còn **đủ** các trường Master Form, không thiếu trường nào.
- [ ] Không hồ sơ an toàn nào đổi `solution`, `max_fails`, `type`, `reward_item_id`, `wrong_action_jumpscare`, `required_items`, `grants_flag`, `trigger_type`, `id`, hay bất kỳ `hotspots[].*` — kể cả `consumes_item` và `locks_item`.
- [ ] Đối chiếu 6 lời giải sau khi bật từng hồ sơ an toàn — phải **khớp 100 %** với bản mặc định.
- [ ] Không có ghi đè nào chạm vào file trên đĩa; toàn bộ override nằm ở `ScareConfigResolver`.

**Cổng & tiền tệ (§1, §10)**
- [ ] 5 cờ `accessibility_never_monetized.*` = `true`; `accessibility_never_gated` = `true`.
- [ ] Bật được **mọi** tuỳ chọn an toàn trên tài khoản mới, 0 gem, chưa xem quảng cáo, chưa qua beat nào.
- [ ] Mục **Cài đặt → An toàn** cách màn hình chơi ≤ **2 lần chạm**, nằm ở cấp một.
- [ ] Đổi tuỳ chọn **giữa một cú doạ** có hiệu lực ngay khung hình kế tiếp.
- [ ] Không kill switch nào tắt được trợ năng.

**Luật nghỉ 90 giây (§6.3)**
- [ ] Bảy cú doạ khai `cooldown_sec: 90` trong `data/areas/*.json`; **đúng một** cú (`scare_ao_cuoi_quay_dau`) khai `cooldown_exempt: true` kèm `ghi_chu_vi` nêu căn cứ.
- [ ] Cú doạ được miễn trừ thoả **cả bốn** điều kiện §6.3.1 — đo lại envelope, `screen_flash`, punch/shake, haptic ở mốc 0 ms.
- [ ] Ba con số 90 bằng nhau: `jumpscares[].cooldown_sec`, `ad_cooldown_after_scare_sec`, cửa sổ `WITHIN_90S_AFTER_ANY_JUMPSCARE`.
- [ ] Bật `gentle_mode` → cả ba thành **180**, không nơi nào còn 90.

**Thính giác & khiếm thính (§7.2)**
- [ ] Giải trọn `puz_ba_hoi_chin_tieng` với **âm lượng tổng = 0** — bằng thanh nhịp trực quan: **chấm tròn = chuông, chấm vuông = mõ**.
- [ ] Giải trọn `puz_ba_hoi_chin_tieng` **tắt màn hình chỉ dùng haptic** (kiểm bằng log xung): chuông 12 ms / 0,35 và mõ 30 ms / 0,70 phân biệt được bằng tay.
- [ ] "Nghe lại" không tăng `fail_count` và không kích hoạt `scare_khoi_tu_hinh_nguoi`.

**Cảnh báo & cửa hàng (§3, §9)**
- [ ] Màn hình cảnh báo hiện **trước** `area_san_gach`, khoá 4 giây, 3 nút ngang hàng thị giác.
- [ ] Không quảng cáo / IAP / popup nào chồng lên màn hình cảnh báo.
- [ ] 7 mô tả nội dung khớp giữa **trang cửa hàng** và **màn hình cảnh báo trong game**.
- [ ] `reduce_motion` tự bật theo `prefers-reduced-motion`; `haptic_enabled` tự tắt theo rung hệ thống.

---

## 12. BÀN GIAO

| Tài liệu / tổ đích | Thứ tài liệu này cung cấp |
|---|---|
| `docs/01_KICH_BAN_CHAPTER_01.md` | Chủ sở hữu của nhịp kinh dị và đường cong sợ hãi (§6 của tài liệu ấy) trích về đây cho **mọi** ràng buộc an toàn; và §3.3.6 của tài liệu ấy là nguồn cho hoán vai nhạc khí X14 mà §7.2 dưới đây phải theo |
| `docs/02_PROMPT_DO_HOA.md` | Yêu cầu **16 file biến thể** `_soft` / `_static` (§4.3), trần độ sáng & bảng màu flash hợp lệ (§2.4), ràng buộc "không tài sản an toàn nào sau tường trả phí" (§1) |
| `docs/03_DATA_SPEC.md` | Ranh giới dữ liệu ↔ runtime: **những trường nào của `jumpscares[]` bị `gentle_mode` ghi đè lúc chạy** (ghi ở §2.5.1 của tài liệu ấy), điều kiện miễn trừ `cooldown_exempt` (§2.7.9 ↔ §6.3.1 ở đây), và sàn chạm 120 × 120 px là **sàn trợ năng** không được hạ (§2.2 mức G3 ↔ §1.2 ở đây) |
| `docs/05_TICH_HOP_UNITY_ADDRESSABLES.md` | Luật đóng gói: **24 file biến thể an toàn** (16 sprite + 8 stinger `_soft`) phải nằm **cùng bundle, cùng nhãn** với bản gốc — một nhãn tải riêng là một **cổng mạng**, vi phạm N3. Luật gốc: **§2.1** của tài liệu ấy (khung *"Vì sao `_soft` và `_static` KHÔNG được tách nhãn riêng"*); cổng kiểm trước phát hành: **§8.2**. `docs/02_PROMPT_DO_HOA.md` §2.3 đã được sửa cho khớp ở vòng này |
| `docs/04_LIVEOPS_MONETIZATION.md` | **Ràng buộc cứng**: 5 cờ `*_free`, `accessibility_never_gated`, chặn quảng cáo quanh cú doạ, cấm kill switch cho trợ năng (§10) |
| `data/areas/*.json` | Danh sách 8 jump-scare với **6 trường** Master Form giữ nguyên trên đĩa (§4.4.1) — **không** tuỳ chọn nào sửa file |
| `data/liveops_chapter_01.json` | Bảng truy vết đầy đủ ở §10 — mọi khoá đã tồn tại, không thêm khoá mới, không đổi tên khoá nào |
| `tools/validate_level.py` | Luật kiểm: đủ trường Master Form, `max_fails` / `solution` không bị override, đủ file biến thể `_soft` / `_static` |
| Tổ QA | Quy trình đo nhạy sáng §2.5 + ngưỡng chặn build + checklist §11 |
| Tổ UI/UX | Màn hình cảnh báo §3.1 + mục Cài đặt → An toàn §3.2 |
| Legal / Product | Đối chiếu tuân thủ cửa hàng §9 + ba câu trả lời sẵn cho rà soát §9.3 |

---

*Hết tài liệu `docs/06_AN_TOAN_NGUOI_CHOI.md` — Linh An Thôn, Chapter 1.*
*Nguồn sự thật: SPINE. Không một `area_id`, `item_id`, `puzzle_id`, `scare_id` hay `solution` nào bị thay đổi.*
*Mọi tuỳ chọn trong tài liệu này đều **miễn phí**, bật được **ngay từ màn hình đầu**, và **không nằm sau bất kỳ cổng tiến trình hay cổng tiền tệ nào**.*
