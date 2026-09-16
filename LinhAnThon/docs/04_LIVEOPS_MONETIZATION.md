# LINH AN THÔN — CHƯƠNG 1
## TÀI LIỆU CẤU HÌNH LIVEOPS & MONETIZATION

| Trường | Giá trị |
|---|---|
| Dự án | **Linh An Thôn — Chapter 1** |
| Tài liệu | `04_LIVEOPS_MONETIZATION.md` — bản chốt cho sản xuất |
| File cấu hình đi kèm | `data/liveops_chapter_01.json` (`schema_version: 1`, `config_version: 1.0.0`) |
| Schema kiểm tra | `schema/liveops.schema.json` |
| Công cụ kiểm tra | `tools/validate_level.py --liveops data/liveops_chapter_01.json` |
| Nền tảng | Android & iOS — APK engine ≤ 30 MB, toàn bộ asset qua Unity Addressables |
| Nguồn sự thật | SPINE đã chốt + `02_puzzle.md` (hệ gợi ý 3 tier) + **`docs/06_AN_TOAN_NGUOI_CHOI.md`** (mọi ràng buộc an toàn — **deliverable chính thức, thay cho file nháp `04_horror.md`**) + `data/liveops_chapter_01.json` |
| Ngôn ngữ | Tài liệu: tiếng Việt có dấu. Mọi `id` / khoá JSON: snake_case không dấu |
| Ngày cập nhật | 2026-09-15 |

> **QUY ƯỚC ĐỌC TÀI LIỆU**
> - Bảng có cột "Khoá JSON" là **hợp đồng kỹ thuật** — tên khoá phải khớp tuyệt đối với `data/liveops_chapter_01.json`.
> - Ghi chú vận hành đặt trong `[[ ... ]]`.
> - Ký hiệu **MF** đánh dấu các khoá **bắt buộc theo Master Form**, không được đổi tên: `hint_cost_gems`, `ads_reward_hints`, `iap_product_id`, `price_usd`, `event_start`, `override_bg`.

---

# PHẦN 0 — NĂM NGUYÊN TẮC NỀN

Mọi quyết định trong tài liệu này đều phải tra ngược về năm nguyên tắc dưới đây. Nếu một đề xuất tăng doanh thu mà phá một nguyên tắc, đề xuất đó bị loại, không thương lượng.

| # | Nguyên tắc | Hệ quả kỹ thuật kiểm được |
|---|---|---|
| **N1** | **Chương 1 chơi trọn vẹn mà không tốn một đồng.** | Mọi gợi ý đều có đường mở miễn phí bằng thời gian chờ, trần **300 giây**. `free_path_guaranteed: true`. |
| **N2** | **Chỉ bán NỘI DUNG, TIỆN ÍCH và TRANG TRÍ — không bán lợi thế chơi.** | `iap.fair_play.sellable_categories` chỉ gồm `CONTENT_UNLOCK`, `CONVENIENCE_HINT`, `COSMETIC`. Không có manh mối nào chỉ người trả tiền mới thấy. |
| **N3** | **Không kiếm tiền trên nỗi sợ.** | Không quảng cáo xen giữa cú doạ, giữa cutscene, giữa thao tác giải đố. Không mời mua hàng ở đỉnh sợ. |
| **N4** | **Tuỳ chọn an toàn luôn miễn phí.** Kế thừa nguyên văn bốn câu N1–N4 của **`docs/06_AN_TOAN_NGUOI_CHOI.md` §1.1**, và danh sách *không-bao-giờ-bị-override* ở §1.2 của tài liệu ấy. | `accessibility_never_monetized` = tất cả `true`. Không tuỳ chọn nào nằm sau tường trả phí / quảng cáo / mốc tiến trình. |
| **N5** | **Người chơi luôn biết mình trả bao nhiêu và nhận được gì trước khi bấm.** | Giá bản địa hoá lấy từ store, kèm danh sách nội dung, xác nhận hai bước, không hộp ngẫu nhiên. |

---

# PHẦN 1 — BẢNG MASTER FORM ↔ KHOÁ JSON

Bảng đối chiếu bắt buộc. Cột **"Vị trí trong JSON"** là đường dẫn chính xác trong `data/liveops_chapter_01.json`.

| Hạng mục Master Form | Khoá (MF) | Giá trị chốt | Vị trí trong JSON |
|---|---|---|---|
| Bán gợi ý — giá bằng Gem | `hint_cost_gems` | `5` | `hint_system.hint_cost_gems` |
| Bán gợi ý — xem quảng cáo | `ads_reward_hints` | `1` | `hint_system.ads_reward_hints` |
| Mở khoá chương (IAP) — mã sản phẩm | `iap_product_id` | `"com.game.chapter02"` | `iap.products[0].iap_product_id` |
| Mở khoá chương (IAP) — giá | `price_usd` | `1.99` | `iap.products[0].price_usd` |
| Sự kiện theo mùa — ngày mở | `event_start` | `"2026-10-25"` | `seasonal_events[0].event_start` |
| Sự kiện theo mùa — nền thay thế | `override_bg` | `"bg_halloween.bundle"` | `seasonal_events[0].override_bg` |

**Ý nghĩa vận hành của sáu khoá này:**

- `hint_cost_gems: 5` là **đơn giá cơ sở của một đơn vị gợi ý**, không phải giá cứng của mọi tier. Tier 2 = 1× đơn giá = 5 gem; Tier 3 = 2,4× = 12 gem (xem §2.2).
- `ads_reward_hints: 1` nghĩa là **một lượt xem quảng cáo thưởng đổi được một đơn vị gợi ý**. Tier 3 cần 2 đơn vị nên phải xem 2 lượt, hoặc chờ đủ 300 giây miễn phí.
- `iap_product_id` và `price_usd` là **sản phẩm neo** của toàn bộ hệ IAP. Mọi sản phẩm khác (gói mùa, túi gem, đồ trang trí) đều định giá tương đối so với neo này.
- `event_start` / `override_bg` là **cặp khoá tối thiểu của một sự kiện**. Bản mở rộng bổ sung `event_end`, `theme_override`, `addressables`, `fallback` — nhưng hai khoá gốc giữ nguyên tên và vị trí.

---

# PHẦN 2 — BÁN GỢI Ý (HINT SYSTEM)

## 2.1. Ba tier gợi ý

Kế thừa nguyên vẹn thiết kế ở `02_puzzle.md` §0.3: **Tier 1 và Tier 2 luôn có đường miễn phí, Tier 3 là đáp án trực tiếp.** LiveOps **không** phát minh tier mới, chỉ thêm đường mở sớm.

| Tier | Tên trong game | Loại nội dung | Mở miễn phí sau | Hoặc sau số lần sai | Giá Gem | Số lượt quảng cáo | Khoá JSON |
|---|---|---|---|---|---|---|---|
| **1** | **Hướng mắt** | `NUDGE` — chỉ nói *nhìn vào đâu* | **60 giây** | 1 | **0** | 0 | `hint_system.tiers[0]` |
| **2** | **Giảng phép** | `METHOD` — giảng quy tắc để tự suy ra | **150 giây** | 2 | **5** (= `hint_cost_gems`) | **1** (= `ads_reward_hints`) | `hint_system.tiers[1]` |
| **3** | **Đáp án trực tiếp** | `SOLUTION` — đọc thẳng dãy lời giải | **300 giây** | 4 | **12** | **2** | `hint_system.tiers[2]` |

**Ba đường mở, người chơi tự chọn:**

```
                      ┌─ CHỜ ĐỦ GIỜ ──────────► miễn phí, luôn có, không bao giờ tắt được
   [ Thắp nhang xin keo ]─ XEM QUẢNG CÁO ─────► ads_reward_hints = 1 đơn vị / lượt
                      └─ TIÊU NÉN HƯƠNG ──────► hint_cost_gems = 5 gem / đơn vị
```

`[[ Nút gợi ý có id btn_thap_nhang_xin_keo. VÙNG CHẠM (bounds) = {x:1700, y:920, width:150, height:130} — nguyên văn hint_system.hint_button.bounds trong data/liveops_chapter_01.json. HÌNH VẼ vẫn là 150 x 110 quanh cùng một tâm (1775, 985); vùng chạm nới ra 150 x 130 để đạt sàn chạm 120 x 120 của dự án (mục 2.6 ngay dưới, docs/03_DATA_SPEC.md mục 2.2 mức G3). Vùng chạm không bắt buộc trùng hình vẽ — đừng lấy 110 làm chiều cao vùng chạm. ]]`

## 2.2. Giá tăng dần

Hai cơ chế tăng giá chạy song song:

**(a) Tăng theo tier** — gợi ý càng "nói toạc" thì càng đắt:

| Tier | Hệ số (`gem_cost_multiplier`) | Giá Gem | Lượt quảng cáo |
|---|---|---|---|
| 1 | `0` | 0 | 0 |
| 2 | `1.0` | 5 | 1 |
| 3 | `2.4` | 12 | 2 |

**(b) Tăng theo số lần mua trong cùng phiên** (`hint_system.price_escalation`) — chống lạm dụng, chống việc "mua sạch đáp án cả chương trong mười phút":

| Lần mua gợi ý trả phí trong phiên | Phụ thu | Giá Tier 2 | Giá Tier 3 |
|---|---|---|---|
| Lần 1 | +0 | 5 | 12 |
| Lần 2 | +3 | 8 | 15 |
| Lần 3 | +6 | 11 | 18 |
| Lần 4 | +9 | 14 | **20 (chạm trần)** |
| Lần 5 trở đi | — | 17 → **20 (trần)** | **20 (trần)** |

- Trần cứng `gem_cost_cap: 20`. Phụ thu **reset** khi kết thúc phiên, khi hoàn thành chương, hoặc vào mốc reset ngày (4 giờ sáng giờ máy).
- **Phụ thu không bao giờ áp lên đường miễn phí.** Chờ đủ 300 giây vẫn ra Tier 3, miễn phí, lần thứ nhất cũng như lần thứ mười.

## 2.3. Giới hạn theo ngày

| Hạng mục | Giới hạn | Khoá JSON | Lý do |
|---|---|---|---|
| Quảng cáo thưởng | **6 lượt/ngày** | `daily_limits.rewarded_ads_per_day` | Trên 6 lượt là dấu hiệu game đang bắt người chơi làm việc, không phải chơi |
| Gợi ý mua bằng Gem | **10 lượt/ngày** | `daily_limits.gem_hints_per_day` | Chặn chi tiêu bốc đồng |
| Gợi ý trả phí trên **mỗi câu đố** | **4 lượt/ngày** | `daily_limits.paid_hints_per_puzzle_per_day` | Một câu đố chỉ có 3 tier; quá 4 lượt là đang có lỗi thiết kế, không phải thiếu gợi ý |
| Gợi ý mở bằng **chờ đủ giờ** | **không giới hạn** (`null`) | `daily_limits.free_wait_hints_per_day` | Nguyên tắc N1 |
| Khoảng cách tối thiểu giữa 2 quảng cáo | **60 giây** | `ad_placements[*].min_gap_sec` | |
| Mốc reset | **4 giờ sáng giờ máy** | `daily_limits.reset_hour_local` | Tránh cắt ngang phiên chơi đêm — đúng khung giờ người chơi horror hoạt động |

Khi chạm giới hạn: hiện `txt_liveops_het_luot_xem_ads` / `txt_liveops_het_luot_mua_goi_y` **kèm nhắc lại thời gian chờ miễn phí còn lại**. Không bao giờ chỉ báo "hết lượt" rồi bỏ mặc người chơi.

## 2.4. Gợi ý thương xót — chống rage-quit

Cơ chế quan trọng nhất của toàn hệ gợi ý. Khi người chơi **kẹt thật**, game **tự tặng** gợi ý, **không hỏi tiền, không mời quảng cáo, không hiện paywall**.

| Điều kiện | Game làm gì | Khoá JSON |
|---|---|---|
| Sai **3 lần** trên cùng một câu đố | Tặng **Tier 1** miễn phí | `mercy_hint.escalation[0]` |
| Sai **5 lần** | Tặng **Tier 2** miễn phí | `mercy_hint.escalation[1]` |
| Sai **7 lần** | Tặng **Tier 3** miễn phí (đáp án) | `mercy_hint.escalation[2]` |
| Kẹt **240 giây** liên tục không thao tác đúng | Mở sẵn tier kế tiếp miễn phí | `mercy_hint.stuck_threshold_sec` |

**Ba ràng buộc cứng của gợi ý thương xót:**

1. `never_shows_ad: true` — người chơi đang bực thì không được phép nhìn thấy quảng cáo.
2. `never_shows_paywall: true` — không bán chương sau cho người đang kẹt chương này.
3. `auto_open_panel: false` — **không tự mở bảng gợi ý đè lên màn hình**. Chỉ hiện một dòng chữ nhỏ ở nút gợi ý: *"Thắp hộ nén nhang rồi đấy."* (`txt_hint_mercy_thap_ho_nen_nhang`). Người chơi tự bấm nếu muốn — tôn trọng người vẫn đang thích tự nghĩ.

`[[ Ba ràng buộc này là lằn ranh đạo đức của hệ thống. Bán gợi ý cho người đang kẹt sau ba lần sai là moi tiền từ sự bực bội. ]]`

## 2.5. Ghi đè theo từng câu đố

| Câu đố | Khó | Mục tiêu (giây) | Tier 1 mở sau | Tier 2 | Tier 3 | Ngưỡng thương xót | Ghi chú |
|---|---|---|---|---|---|---|---|
| `puz_khoa_bat_quai` | 2/5 | 90 | 60 s | 150 s | 300 s | 3 sai | Câu đố dạy cơ chế |
| `puz_rap_chu_the_menh` | 3/5 | 150 | 60 s | 150 s | 300 s | 3 sai | Hết tờ giấy thứ 3 → **tự mở Tier 1 miễn phí** |
| `puz_tuan_tu_le_cung` | 3/5 | 120 | **40 s** | 150 s | 300 s | 3 sai | Thêm gợi ý diegetic: **cuốn văn khấn tự lật trang** sau 40 giây |
| `puz_ba_hoi_chin_tieng` | 4/5 | 180 | 60 s / **2 sai** | 150 s | 300 s | **2 sai** | Khó nhất nửa đầu chương; thanh nhịp hiện mờ **số tiếng chuông** của hồi 1 sau lần sai thứ 2. Kênh thị giác + haptic của câu đố này là **ràng buộc trợ năng bắt buộc**, không phải gợi ý bán được — `docs/06_AN_TOAN_NGUOI_CHOI.md` §7.2 |
| `puz_thap_lai_den_dau` | 3/5 | 110 | 60 s | 150 s | 300 s | 3 sai | |
| `puz_xep_anh_gia_pha` | 4/5 | 240 | **90 s** | **210 s** | **420 s** | 3 sai | `SLIDING_TILE` dài nhất chương — giãn mốc để Tier 3 không phá trải nghiệm người đang xếp đúng hướng |

**Gợi ý diegetic (trong thế giới) không tính vào tier, luôn miễn phí:** cuốn văn khấn tự lật trang (`puz_tuan_tu_le_cung`), thanh nhịp nhấp nháy số tiếng **chuông** (`puz_ba_hoi_chin_tieng` — cả sáu cụm của `solution` đều là tiếng chuông, mõ chỉ điểm một tiếng chốt mỗi hồi; xem `01_KICH_BAN_CHAPTER_01.md` §3.3.6), gáo dừa khẽ xoay ở hậu cảnh khi sai lần 2 (`puz_khoa_bat_quai`), mành nứa đung đưa (`puz_rap_chu_the_menh`). Đây vừa là hệ gợi ý vừa là kể chuyện — **không bao giờ được gắn tiền vào chúng**.

## 2.6. Luồng UI khi bấm nút gợi ý

```
[ Thắp nhang xin keo ]
        │
        ├── Tier đã mở sẵn ────────────────────► hiện ngay nội dung gợi ý
        │
        └── Tier chưa mở ───► Bảng ba lựa chọn:
                                 ┌ "Chờ thêm 02:14"      (miễn phí, đếm ngược thật)
                                 ├ "Xem một quảng cáo"   (1 lượt — còn 4 lượt hôm nay)
                                 └ "Dùng 5 nén hương"    (số dư: 32) ──► XÁC NHẬN LẦN HAI
```

Ràng buộc UI bắt buộc:
- **Kích thước nút gợi ý và mọi nút trong bảng ba lựa chọn: ≥ 120 × 120 px @1920.** Đây là **sàn chạm chính thức của dự án**, dùng chung với hotspot trong game — `01_KICH_BAN_CHAPTER_01.md` §6 (mục X18) và `docs/03_DATA_SPEC.md` §2.2 mức G3. **Ngưỡng 88 px của bản cũ đã bị bãi bỏ**: quy đổi *"88 px ≈ 44 pt"* là sai số học, fit-width chỉ cho ra 29–43 pt/dp. Khoảng đệm giữa hai nút kề nhau ≥ 20 px — **người đang bực vì kẹt câu đố là đúng người dễ bấm nhầm nhất**, và bấm nhầm ở đây là bấm nhầm vào nút tiêu gem.
- Đường **miễn phí luôn nằm trên cùng**, cỡ chữ bằng hai đường còn lại, **không làm mờ, không thu nhỏ**.
- Luôn hiện **số dư gem** và **số lượt quảng cáo còn lại** trước khi người chơi chọn.
- Tiêu gem phải **xác nhận hai bước**; Tier 3 còn thêm một lớp hỏi: *"Đọc đáp án thật chứ? Không quay lại được cảm giác tự giải đâu."* (`txt_hint_xac_nhan_doc_dap_an`).
- Bảng gợi ý **bị chặn** trong các cửa sổ: `CUTSCENE`, `JUMPSCARE_ENVELOPE`, `SAFETY_WARNING_SCREEN`, `AREA_TRANSITION`. Ràng buộc `SAFETY_WARNING_SCREEN` do **`docs/06_AN_TOAN_NGUOI_CHOI.md` §3.1** đặt ra và không được nới.

## 2.7. Ràng buộc bất biến (validator bắt lỗi)

| Ràng buộc | Khoá |
|---|---|
| Gợi ý không bao giờ chặn tiến độ | `constraints.hint_never_blocks_progress` |
| Gợi ý không tiêu huỷ vật phẩm (xấp giấy bản luôn được nạp lại) | `constraints.hint_never_consumes_items` |
| Tuỳ chọn an toàn không bao giờ bị khoá sau gợi ý/quảng cáo | `constraints.accessibility_never_gated` |
| Không mời quảng cáo ngay tại khoảnh khắc giải sai | `constraints.no_ad_inside_puzzle_fail_moment` |
| `max_fails` của jumpscare **không bao giờ** bị LiveOps override | `constraints.max_fails_never_overridden` |

---

# PHẦN 3 — MỞ KHOÁ CHƯƠNG (IAP)

## 3.1. Danh mục sản phẩm

| `iap_product_id` | Loại | Tên hiển thị | `price_usd` | Nội dung nhận được |
|---|---|---|---|---|
| **`com.game.chapter02`** **(MF)** | `NON_CONSUMABLE` | Chương 2 — Người thế mạng | **`1.99`** | Mở khoá toàn bộ Chương 2, cờ `flag_chapter_02_unlocked` |
| `com.game.season01.bundle` | `NON_CONSUMABLE` | Trọn mùa 1 — Linh An Thôn | `5.99` | Chương 2, 3, 4 + phần vĩ thanh, tặng 50 gem |
| `com.game.gems.pack_60` | `CONSUMABLE` | Túi 60 nén hương | `0.99` | 60 gem |
| `com.game.gems.pack_200` | `CONSUMABLE` | Bó 200 nén hương | `2.99` | 200 gem + tặng 20 |
| `com.game.cosmetic.den_dau_dong` | `NON_CONSUMABLE` | Đèn dầu vỏ đồng | `0.99` | Đổi hình cây đèn trong hành trang — `gameplay_effect: NONE` |

`[[ Chương 1 KHÔNG có sản phẩm đăng ký định kỳ (subscription). Quyết định này được ghi cứng: no_auto_renew_subscription_in_chapter_01: true. ]]`

## 3.2. Bảng giá theo vùng — `com.game.chapter02`

Giá hiển thị trên máy **luôn lấy từ store** (`StoreKit` / `Google Play Billing`), không bao giờ hardcode. Bảng dưới đây là bảng dựng giá để khai báo trên store và để đối chiếu doanh thu.

| Vùng | Tiền tệ | Giá bản địa | Quy đổi USD | Ghi chú thuế |
|---|---|---|---|---|
| **VN — Việt Nam** | VND | **49.000 ₫** | ~1,93 | Đã gồm VAT do store thu hộ |
| **US — Hoa Kỳ** | USD | **$1.99** | 1,99 | Chưa gồm sales tax theo bang |
| TH — Thái Lan | THB | ฿69 | ~1,95 | Đã gồm VAT 7% |
| ID — Indonesia | IDR | Rp 29.000 | ~1,86 | Đã gồm PPN 11% |
| PH — Philippines | PHP | ₱99 | ~1,75 | Đã gồm VAT 12% |
| MY — Malaysia | MYR | RM 8,90 | ~1,97 | Đã gồm SST 6% |
| SG — Singapore | SGD | S$2,98 | ~2,26 | Đã gồm GST 9% |
| **SEA_DEFAULT** | USD | $1.99 | 1,99 | Áp cho thị trường SEA chưa có bảng giá riêng |

**Nguyên tắc định giá vùng:**
1. **Neo theo sức mua, không neo theo tỷ giá.** Giá VN (~1,93 USD) thấp hơn giá SG (~2,26 USD) là **cố ý**, đúng chuẩn phân tầng của cả hai store.
2. **Số đẹp theo thói quen bản địa.** VN dùng bội số 1.000 (49.000 ₫), không dùng 45.560 ₫.
3. **Chênh lệch quy đổi giữa các vùng ≤ 20%** so với giá neo, tránh bị coi là phân biệt giá.
4. Khi store đổi bậc giá, **cập nhật bảng này trước, đẩy remote config sau** — không bao giờ để hai nguồn lệch nhau quá một phiên bản.

## 3.3. Gói bundle cả mùa — `com.game.season01.bundle`

| Trường | Giá trị |
|---|---|
| Nội dung | Chương 2 + 3 + 4 + phần vĩ thanh + 50 gem |
| Giá neo | `5.99` USD — VN **149.000 ₫** |
| Mua lẻ tương đương | 4 × 1.99 = 7,96 USD → **tiết kiệm ~25%** |
| Quy tắc nâng cấp | Người **đã mua** `com.game.chapter02` vẫn mua được gói mùa và **được bù 60 gem**, ghi rõ trên màn hình **trước khi** bấm mua (`upgrade_rule.credit_gems_if_owns`) |
| Cấm | **Không** bán gói mùa cho người chưa hoàn thành Chương 1 dưới dạng cửa sổ bật lên giữa game |

## 3.4. Khôi phục mua hàng (restore)

| Trường | Giá trị | Khoá JSON |
|---|---|---|
| Nút | **"Khôi phục mua hàng"** | `iap.restore.button_id` |
| Vị trí | Màn hình Cài đặt **và** màn hình paywall | `iap.restore.locations` |
| Loại khôi phục được | `NON_CONSUMABLE` (chương, gói mùa, đồ trang trí) | `restorable_product_types` |
| Gem đã mua (consumable) | Khôi phục bằng **sổ cái phía máy chủ** theo tài khoản store | `consumable_recovery: SERVER_LEDGER` |
| iOS | `StoreKit2 Transaction.currentEntitlements` (fallback `restoreCompletedTransactions`) | `ios_api` |
| Android | `BillingClient.queryPurchasesAsync(INAPP)` | `android_api` |
| Xác thực hoá đơn | **Bắt buộc phía máy chủ** | `verify_receipt_server_side: true` |
| Ân hạn offline | **72 giờ** — mất mạng vẫn chơi tiếp được nội dung đã mua | `offline_grace_hours` |

Ba thông báo bắt buộc: `txt_iap_khoi_phuc_thanh_cong`, `txt_iap_khong_tim_thay_giao_dich`, `txt_iap_khoi_phuc_that_bai`.

`[[ Nút khôi phục là yêu cầu bắt buộc của App Store Review Guideline 3.1.1. Thiếu nút này là bị từ chối phát hành, không phải góp ý. ]]`

## 3.5. Quy tắc "không bán lợi thế chơi"

| Được bán | Không bao giờ được bán |
|---|---|
| `CONTENT_UNLOCK` — chương mới, phần vĩ thanh, trang nhật ký phụ | `PUZZLE_SKIP_ONLY_FOR_PAY` — bỏ qua câu đố mà người miễn phí không bỏ qua được |
| `CONVENIENCE_HINT` — **rút ngắn thời gian chờ** của gợi ý mà ai cũng nhận được miễn phí sau 300 giây | `EXCLUSIVE_CLUE` — manh mối chỉ người trả tiền mới thấy |
| `COSMETIC` — đổi hình cây đèn, khung hành trang, giao diện sự kiện | `TIME_GATE_REMOVAL_REQUIRED` — cổng thời gian bắt buộc phải trả tiền mới qua |
| | `RANDOMIZED_PAID_REWARD` — hộp quà ngẫu nhiên, gacha, quay số |
| | `PAID_SAFETY_OPTION` — bán chế độ nhẹ nhàng, giảm chớp sáng, tắt rung |

**Phép thử một dòng dành cho mọi đề xuất kiếm tiền mới:**

> *Nếu bỏ hết mọi khoản chi, người chơi có hoàn thành Chương 1 với **đúng cùng một nội dung**, chỉ chậm hơn vài phút không?*
> **Có** → được phép bán. **Không** → loại.

## 3.6. Vị trí paywall

| Trường | Giá trị |
|---|---|
| Mã vị trí | `paywall_ket_chuong_01` |
| Điều kiện kích hoạt | `flag_chapter_01_hoan_thanh = true` — **cờ kết chương THẬT**, tức giá trị của `chapter_complete_flag` trong `data/chapter_01.json`. Xem §3.6.1 |
| Thời điểm | **3 giây sau khi cảnh kết chương khép lại** (biến thể A/B: sau credits — xem §8) |
| Đóng được | **Có** — nút đóng rõ ràng, không đếm ngược giả |
| Trần hiển thị | **2 lần/ngày** |
| Cấm tuyệt đối | Trong `CUTSCENE`, trong `PUZZLE`, trong `JUMPSCARE_ENVELOPE`, trên `SAFETY_WARNING_SCREEN` |
| Bắt buộc | Hiện giá bản địa + danh sách nội dung **trước** nút xác nhận |

### 3.6.1. Cờ chặn cổng bán phải là cờ CÓ THẬT — bất biến 17

| Mục | Nội dung |
|---|---|
| **Khoá dữ liệu** | `iap.products[*].requires.flag` trong `data/liveops_chapter_01.json` |
| **Giá trị đúng** | `flag_chapter_01_hoan_thanh` — chính là `chapter_complete_flag` của `data/chapter_01.json`, do `hs_hinh_nhan` cấp qua `grants_flag`, và có mặt trong `exported_flags` |
| **Luật** | Cờ chặn cổng bán phải **hoặc** được Chương 1 cấp **và** khai là bàn giao (`exported_flags` / `chapter_complete_flag`), **hoặc** do chính một `unlock.grants_flags` trong file này cấp |
| **Validator** | `tools/validate_level.py` giai đoạn 11 — đặc tả đầy đủ ở `docs/03_DATA_SPEC.md` §4.4.1 |

> **⚠️ ĐÍNH CHÍNH — bản trước ghi SAI và nó là lỗi chặn doanh thu.** Bản trước chặn bằng `flag_chapter_01_completed`. **Cờ ấy không tồn tại**: Chương 1 không có chỗ nào khai `"grants_flag": "flag_chapter_01_completed"`, nên nó không bao giờ bật lên. Hệ quả là **cổng mua `com.game.chapter02` khoá vĩnh viễn với 100% người chơi** — paywall hiện ra rồi từ chối bán. Cả `data/liveops_chapter_01.json` lẫn `data/chapter_01.json` đều parse sạch và đều đúng schema riêng; lỗi nằm đúng ở chỗ **giữa** hai file, nơi trước vòng này không ai kiểm. Nay có bất biến 17 canh.

`[[ Paywall dat SAU cu twist, khong bao gio dat TRUOC. Cat ngang khoanh khac tieng MO noi ren khap lang — tieng CHOT, ca lang cung chot so — de moi mua hang la pha hong dung thu khien nguoi ta muon mua chuong sau. ]]`

---

# PHẦN 4 — SỰ KIỆN THEO MÙA

## 4.1. Cửa sổ sự kiện

| Trường | Giá trị | Khoá JSON |
|---|---|---|
| Mã sự kiện | `evt_halloween_2026` | `seasonal_events[0].event_id` |
| Tên hiển thị | **Đêm Hồn Ma 2026** | `ten_vi` |
| **Ngày mở** | **`2026-10-25`** | **`event_start`** **(MF)** |
| **Ngày đóng** | **`2026-11-03`** | `event_end` *(mở rộng)* |
| Múi giờ | `Asia/Ho_Chi_Minh` | `timezone` |
| Nguồn thời gian | **Máy chủ NTP**, không tin đồng hồ máy | `server_authoritative_time: true` |
| Ân hạn | **24 giờ** — người đang chơi dở lúc sự kiện đóng vẫn xem trọn phiên | `grace_period_hours` |
| Khu vực áp dụng | `area_san_gach`, `area_hien_nha` | `applies_to_areas` |
| Độ ưu tiên | `10` (số nhỏ thắng khi hai sự kiện chồng nhau) | `priority` |

**Quy tắc cửa sổ:**
1. `event_start < event_end`, kiểm bằng validator.
2. Hai sự kiện `enabled: true` **không được chồng cửa sổ trên cùng một area**. Nếu buộc phải chồng, `priority` nhỏ hơn thắng và sự kiện thua bị vô hiệu hoá hoàn toàn trong area đó.
3. **Chống lùi đồng hồ máy:** nếu máy khai thời gian lệch máy chủ quá 6 giờ, dùng thời gian máy chủ và ghi `remote_config_fetch`.
4. Sự kiện chỉ đổi **lớp trình bày**. Không đổi gameplay — xem §4.2.

## 4.2. Theme UI override

| Thành phần | Giá trị sự kiện Halloween |
|---|---|
| Mã theme | `theme_halloween_2026` |
| Màu nhấn | `#C2571E` |
| Nền bảng UI | `#1A1108` |
| Màu chữ | `#F2E4CE` |
| Viền hotspot | `#C2571E` |
| Khung hành trang | `ui_frame_halloween.bundle` |
| Logo tiêu đề | `logo_halloween.bundle` |
| Ambience thay thế | `amb_halloween_gio_lanh.bundle` |
| **Nền thay thế** | **`bg_halloween.bundle`** **(MF — `override_bg`)** |

**Danh sách KHÔNG ĐƯỢC ĐỔI (`theme_override.does_not_change`) — ràng buộc cứng:**

| Không đổi | Vì sao |
|---|---|
| `hotspot_bounds` | Đổi toạ độ là đổi độ khó và phá chứng minh không-chồng-lấn ở `03_world.md` |
| `puzzle_solution` | Người chơi sự kiện và người chơi thường phải giải cùng một câu đố |
| `jumpscare_trigger_type` | Nhịp doạ thuộc thiết kế kinh dị, không thuộc LiveOps |
| `max_fails` | Kế thừa `data/areas/*.json`; **`docs/06_AN_TOAN_NGUOI_CHOI.md` §1.2** liệt nó vào danh sách không bao giờ bị override — kể cả bởi `gentle_mode` |
| `item_ids` | Phá chuỗi phụ thuộc vật phẩm |
| `area_gate` | Phá chứng minh khả giải |

> **Nguyên tắc một câu:** sự kiện đổi **ngôi nhà trông như thế nào**, không đổi **ngôi nhà vận hành ra sao**.

## 4.3. Asset bổ sung qua Addressables

| Trường | Giá trị |
|---|---|
| Nhãn bundle | `evt_halloween_2026` |
| Danh sách bundle | `bg_halloween.bundle`, `ui_frame_halloween.bundle`, `logo_halloween.bundle`, `amb_halloween_gio_lanh.bundle` |
| Dung lượng ước tính | **6,4 MB** (nén) |
| Chính sách tải | `ON_EVENT_ENTER` — tải khi người chơi vào area có sự kiện |
| Mặc định | **Chỉ tải qua Wi-Fi** (`wifi_only_default: true`), người chơi bật được dữ liệu di động trong Cài đặt |
| Nạp trước | **3 ngày trước `event_start`**, ngầm, ưu tiên thấp |
| Catalog | Lấy từ remote config `addressables_catalog_url` |

**Ràng buộc dung lượng:** APK engine ≤ 30 MB không đổi. Bundle sự kiện **không bao giờ** được đóng vào APK. Toàn bộ asset sự kiện là remote, xoá được, và **xoá xong game vẫn chạy** — đó chính là điều kiện để §4.4 có nghĩa.

## 4.4. Fallback khi tải bundle thất bại

Đây là mục quan trọng nhất của Phần 4. Một sự kiện hỏng **không được phép làm hỏng game**.

| Bước | Hành vi | Khoá JSON |
|---|---|---|
| 1 | Yêu cầu bundle, timeout **8 giây** | `fallback.timeout_sec` |
| 2 | Thất bại → thử lại **2 lần**, giãn cách **3 s rồi 9 s** | `retry_count`, `retry_backoff_sec` |
| 3 | Vẫn thất bại → **dùng nền gốc** của area, đọc từ `data/areas/<area_id>.json:background_asset_url` | `on_download_fail: USE_BASE_BACKGROUND` |
| 4 | **Tắt theme sự kiện cho cả phiên** — không thử lại liên tục làm nóng máy, tốn pin | `disable_theme_for_session_after_fail` |
| 5 | **Không bao giờ chặn gameplay**, **không bao giờ hiện hộp thoại lỗi** | `never_block_gameplay`, `never_show_error_modal` |
| 6 | Hiện một toast nhỏ, một lần: `txt_liveops_khong_tai_duoc_giao_dien_su_kien` | `toast_text_key` |
| 7 | Ghi telemetry `event_theme_apply` với `applied: false` và `fallback_reason` | `telemetry_event` |

**Ba trạng thái hỗn hợp phải xử lý đúng (dễ bỏ sót nhất):**

| Tình huống | Xử lý bắt buộc |
|---|---|
| Tải được nền nhưng **hỏng khung UI** | Áp nền sự kiện, giữ khung gốc. **Không** áp nửa vời màu chữ — ưu tiên đọc được chữ hơn là đẹp |
| Tải xong rồi **mất mạng giữa phiên** | Bundle đã vào RAM thì dùng tiếp đến hết phiên; phiên sau thử lại từ bước 1 |
| **Sự kiện hết hạn giữa phiên** | Giữ theme đến hết phiên (ân hạn 24 giờ), không đổi giao diện đột ngột giữa lúc người chơi đang giải đố |

`[[ Quy tắc vàng của fallback: người chơi không có mạng phải nhận được ĐÚNG trò chơi mà người có mạng nhận được, chỉ khác lớp sơn. ]]`

## 4.5. Lịch sự kiện năm đầu

| Mã sự kiện | Tên | `event_start` | `event_end` | `override_bg` | Trạng thái |
|---|---|---|---|---|---|
| `evt_halloween_2026` | Đêm Hồn Ma 2026 | **2026-10-25** | 2026-11-03 | **`bg_halloween.bundle`** | **Bật** |
| `evt_tet_dinh_mui_2027` | Tết Đinh Mùi — Nhà mới quét vôi | 2027-02-06 | 2027-02-20 | `bg_tet_nguyen_dan.bundle` | Tắt (chờ art) |
| `evt_ram_thang_bay_2027` | Rằm tháng Bảy — Xá tội vong nhân | 2027-08-14 | 2027-08-21 | `bg_ram_thang_bay.bundle` | Tắt (chờ art) |

`[[ Rằm tháng Bảy là sự kiện "chính chủ" của game — Chương 1 diễn ra đúng rằm tháng Bảy năm Bính Tý 1996. Ưu tiên ngân sách art cho sự kiện này hơn Halloween. ]]`

**Phần thưởng sự kiện — ràng buộc:** chỉ gem điểm danh, gem hoàn thành và đồ trang trí. `no_exclusive_gameplay_content: true` — **không có câu đố, khu vực, vật phẩm hay đoạn cốt truyện nào chỉ tồn tại trong sự kiện**, vì người bỏ lỡ sự kiện sẽ mất vĩnh viễn một mảnh của câu chuyện.

---

# PHẦN 5 — KINH TẾ GEM ("NÉN HƯƠNG")

Đơn vị tiền mềm mang tên **"nén hương"** (`currency_id: gem`, icon `icon_gem_nen_huong.png`) — đặt tên theo bối cảnh, vì người chơi "thắp nhang xin keo" mỗi lần cần gợi ý.

## 5.1. Nguồn thu (sources)

| Mã nguồn | Việc người chơi làm | Số gem | Giới hạn | Loại |
|---|---|---|---|---|
| `src_first_launch` | Mở game lần đầu | **15** | Một lần | Miễn phí |
| `src_area_first_clear` | Lần đầu qua mỗi khu vực | **5** × 5 khu vực | Mỗi area một lần — tối đa 25 | Miễn phí |
| `src_chapter_complete` | Hoàn thành Chương 1 | **20** | Một lần | Miễn phí |
| `src_read_all_text_in_area` | Đọc hết mọi hotspot trong một khu vực | **3** × 5 | Mỗi area một lần — tối đa 15 | Miễn phí |
| `src_daily_login` | Mở game mỗi ngày | **2** | Mỗi ngày | Miễn phí |
| `src_event_login` | Điểm danh trong sự kiện | **3** | Mỗi ngày khi sự kiện chạy | Miễn phí |
| `src_rewarded_ad` | Xem quảng cáo thưởng, chọn nhận gem | **2** | 6 lượt/ngày | Quảng cáo |
| `src_iap_gem_pack` | Mua túi nén hương | 60 / 220 | Không giới hạn | IAP |

`[[ src_read_all_text_in_area là nguồn thu cố ý nhất trong bảng: nó trả tiền cho hành vi ĐỌC. Toàn bộ 57 khoá localization phân biệt của chương (đếm từ data/areas/*.json: 39 txt_examine_ + 11 txt_thieu_do_ + 4 txt_khoa_ + 3 txt_thoai_ = 57) đều là cài cắm twist — người đọc hết sẽ hiểu cú twist sâu hơn, và game thưởng cho điều đó. Lưu ý phạm vi của chính nguồn thu này: nó chỉ đếm hotspot EXAMINE và DIALOGUE trong một khu vực, tức nhánh 39 + 3; nhóm txt_thieu_do_ và txt_khoa_ chỉ hiện khi người chơi bấm vào chỗ chưa đủ điều kiện, không tính vào mốc đọc hết. ]]`

## 5.2. Nguồn chi (sinks)

| Mã chi | Dùng vào việc gì | Số gem | Nhóm |
|---|---|---|---|
| `snk_hint_tier2` | Mở sớm gợi ý Tier 2 | **5** | Tiện ích |
| `snk_hint_tier3` | Mở sớm gợi ý Tier 3 (đáp án) | **12** | Tiện ích |
| `snk_lore_page` | Mở trang nhật ký bà nội (nội dung phụ) | 25 | Nội dung phụ |
| `snk_gallery_unlock` | Mở phòng tranh khái niệm | 30 | Nội dung phụ |
| `snk_cosmetic_lantern` | Đổi hình cây đèn hành trang | 40 | Trang trí |

**Gem KHÔNG mua được** (`gem_economy.forbidden.gem_cannot_buy`): tuỳ chọn an toàn, tuỳ chọn trợ năng, manh mối độc quyền, hộp ngẫu nhiên, tự động giải câu đố mà không hiện lời giải bằng chữ.

## 5.3. Bảng cân bằng

| Chỉ số | Giá trị | Ý nghĩa |
|---|---|---|
| Số dư khởi điểm | **15 gem** | Đủ mua 3 gợi ý Tier 2 ngay từ đầu — người chơi được thử cơ chế trước khi phải nghĩ tới tiền |
| Thu miễn phí kỳ vọng trong Chương 1 | **≈ 75 gem** | 15 + 25 + 20 + 15 (chưa tính điểm danh) |
| Chi trung vị (người chơi điển hình) | **0 gem** | Đa số giải hết bằng gợi ý miễn phí |
| Chi ở ngưỡng P90 (người chơi hay kẹt) | **≈ 29 gem** | Hai lần Tier 2 + một lần Tier 3 kèm phụ thu |
| **Kết luận** | **75 > 29** | Cả người chơi kẹt nhiều nhất cũng **không cần mua gem** để qua Chương 1 |

Quy tắc giám sát vận hành: nếu telemetry cho thấy **P90 chi > 60% thu miễn phí** trong hai tuần liên tiếp, đó là dấu hiệu **câu đố quá khó**, không phải cơ hội tăng giá. Hành động đúng là chỉnh mốc chờ hoặc chỉnh câu đố, không phải chỉnh giá gem.

---

# PHẦN 6 — TELEMETRY

## 6.1. Quy ước

| Trường | Quy định |
|---|---|
| Đặt tên sự kiện | `snake_case`, tối đa **40 ký tự** |
| Số tham số | Tối đa **25** mỗi sự kiện |
| Định danh người chơi | `install_id` **ẩn danh do máy sinh**. **Không** gửi email, số điện thoại, IDFA/GAID khi chưa có đồng ý |
| Tham số dùng chung (mọi sự kiện) | `install_id`, `session_id`, `build_version`, `config_version`, `platform`, `country_code`, `ab_variants`, `safety_profile` |
| Nhà cung cấp | Firebase Analytics + xuất BigQuery |
| Tỷ lệ lấy mẫu | `1.0` (chỉnh được qua remote config `telemetry_sampling_rate`) |

## 6.2. Danh mục sự kiện (37 sự kiện)

### Nhóm A — Tiến độ & phễu

| Tên sự kiện | Tham số chính | Đo cái gì |
|---|---|---|
| `chapter_start` | `chapter_id`, `is_first_run`, `resumed_from_save` | Mốc 0 của phễu |
| `area_enter` | `area_id`, `area_order`, `from_area_id`, `entry_source`, `elapsed_sec_in_chapter`, `visit_index` | Bước phễu theo khu vực |
| `area_exit` | `area_id`, `dwell_sec`, `exit_reason`, `hotspots_examined`, `hotspots_total` | Thời gian ở lại, mức khám phá |
| `hotspot_interact` | `area_id`, `hotspot_id`, `action_type`, `is_first_time`, `blocked_by_missing_item`, `required_item` | Hotspot nào bị bỏ sót |
| `item_collect` | `item_id`, `area_id`, `hotspot_id`, `elapsed_sec_in_chapter` | Chuỗi phụ thuộc vật phẩm |
| `item_use` | `item_id`, `hotspot_id`, `area_id`, `is_correct_target` | Dùng vật phẩm sai chỗ |
| `chapter_complete` | `total_playtime_sec`, `puzzles_hinted_count`, `hints_paid_count`, `ads_watched_total`, `gems_spent_total`, `jumpscares_seen` | Đích của phễu |

### Nhóm B — Câu đố & điểm kẹt

| Tên sự kiện | Tham số chính | Đo cái gì |
|---|---|---|
| `puzzle_open` | `puzzle_id`, `puzzle_type`, `attempt_index`, `has_required_item`, `fail_count_carried` | Mẫu số của tỷ lệ giải |
| `puzzle_fail` | `puzzle_id`, `fail_count`, `sec_in_puzzle`, `input_signature`, `hint_tier_unlocked`, `will_trigger_jumpscare` | Độ khó thực tế; `input_signature` cho biết **người chơi sai kiểu gì** |
| `puzzle_solve` | `puzzle_id`, `time_to_solve_sec`, `fail_count_total`, `hint_tier_max_used`, `hint_source`, `solved_after_hint_sec` | Tử số của tỷ lệ giải |
| **`puzzle_abandon`** | `puzzle_id`, `sec_in_puzzle`, `fail_count`, `hint_tier_max_used`, `exit_reason` | **ĐIỂM KẸT** — mở câu đố rồi bỏ đi |
| **`puzzle_stuck`** | `puzzle_id`, `stuck_bucket_sec`, `fail_count`, `hint_tier_available`, `hint_panel_opened` | **ĐIỂM KẸT** — bắn tại mốc 60/150/300/600 giây |

### Nhóm C — Gợi ý

| Tên sự kiện | Tham số chính | Đo cái gì |
|---|---|---|
| `hint_offer_shown` | `puzzle_id`, `tier`, `offer_types`, `gem_cost`, `ads_required`, `gem_balance`, `free_wait_remaining_sec` | Mẫu số chuyển đổi gợi ý |
| `hint_unlock` | `puzzle_id`, `tier`, `unlock_source`, `gem_cost`, `gem_balance_after`, `ads_watched`, `sec_in_puzzle` | Người chơi chọn đường nào: chờ / quảng cáo / gem / thương xót |
| `hint_view` | `puzzle_id`, `tier`, `view_duration_sec`, `solved_within_60s`, `solved_within_180s` | **Gợi ý có thật sự cứu được người chơi không** |
| `hint_mercy_grant` | `puzzle_id`, `tier_granted`, `fail_count`, `sec_in_puzzle` | Tần suất phải can thiệp chống rage-quit |

### Nhóm D — Quảng cáo & IAP

| Tên sự kiện | Tham số chính | Đo cái gì |
|---|---|---|
| `ad_request` / `ad_impression` / `ad_reward_granted` / `ad_fail` | `placement_id`, `network`, `latency_ms`, `ecpm_estimate`, `watched_to_end`, `error_code` | Sức khoẻ nguồn quảng cáo |
| **`ad_blocked_by_rule`** | `placement_id`, `block_reason`, `sec_since_last_jumpscare`, `last_scare_id` | **Kiểm chứng luật cấm chen quảng cáo quanh jumpscare** |
| `paywall_view` / `paywall_dismiss` | `placement_id`, `iap_product_id`, `price_local`, `currency_code`, `price_usd`, `sec_on_screen`, `dismiss_method` | Chuyển đổi & mức khó chịu |
| `iap_purchase_start` / `iap_purchase_success` / `iap_purchase_fail` | `iap_product_id`, `order_id`, `price_local`, `currency_code`, `price_usd`, `store`, `receipt_verified`, `error_code` | Doanh thu và rơi rớt theo vùng |
| `iap_restore_result` | `result`, `restored_product_ids`, `duration_ms`, `error_code` | Khôi phục mua hàng có chạy không |
| `gem_earn` / `gem_spend` | `source_id` / `sink_id`, `amount`, `balance_after`, `context_id` | Lạm phát tiền tệ |

### Nhóm E — Kinh dị, an toàn, kỹ thuật

| Tên sự kiện | Tham số chính | Đo cái gì |
|---|---|---|
| `jumpscare_play` | `scare_id`, `area_id`, `trigger_type`, `intensity_profile`, `screen_flash_applied`, `deferred_by_cooldown`, `sec_since_last_scare` | Cú doạ nào bắn, ở cường độ nào |
| **`jumpscare_quit_signal`** | `scare_id`, `area_id`, `sec_after_scare`, `safety_profile` | **Thoát app trong vòng 20 giây sau cú doạ** — tín hiệu doạ quá tay |
| `safety_setting_change` | `setting_key`, `old_value`, `new_value`, `changed_at_screen`, `after_scare_id` | Bao nhiêu người cần chế độ nhẹ nhàng, và bật sau cú doạ nào |
| `bundle_download` | `bundle_name`, `label`, `result`, `bytes`, `duration_ms`, `error_code`, `network_type`, `retry_index` | Sức khoẻ Addressables |
| `event_theme_apply` | `event_id`, `override_bg`, `applied`, `fallback_reason`, `area_id` | Theme sự kiện áp được hay phải fallback |
| `remote_config_fetch` | `config_version`, `success`, `latency_ms`, `used_cached`, `ab_variants` | Cấu hình tới máy đúng phiên bản chưa |
| `session_start` / `session_end` | `session_index`, `days_since_install`, `session_sec`, `last_area_id`, `last_puzzle_id`, `last_scare_id`, `sec_since_last_scare`, `exit_reason` | Retention và **nơi người chơi rời đi** |

## 6.3. Phễu chuyển đổi (`funnel_chapter_01`)

| Bước | Mã bước | Sự kiện + điều kiện | Mục tiêu |
|---|---|---|---|
| 0 | `f0_first_open` | `session_start` (`session_index = 1`) | 100% |
| 1 | `f1_chapter_start` | `chapter_start` | 96% |
| 2 | `f2_solve_p1` | `puzzle_solve` — `puz_khoa_bat_quai` | 92% |
| 3 | `f3_enter_hien_nha` | `area_enter` — `area_hien_nha` | 90% |
| 4 | `f4_solve_p2` | `puzzle_solve` — `puz_rap_chu_the_menh` | 84% |
| 5 | `f5_enter_gian_tho` | `area_enter` — `area_gian_tho` | 82% |
| 6 | `f6_solve_p3` | `puzzle_solve` — `puz_tuan_tu_le_cung` | 77% |
| 7 | `f7_solve_p4` | `puzzle_solve` — `puz_ba_hoi_chin_tieng` | **68%** ← điểm rơi lớn nhất dự kiến |
| 8 | `f8_enter_bep_gieng` | `area_enter` — `area_bep_gieng` | 72% |
| 9 | `f9_solve_p5` | `puzzle_solve` — `puz_thap_lai_den_dau` | 67% |
| 10 | `f10_enter_gac_xep` | `area_enter` — `area_gac_xep` | 64% |
| 11 | `f11_solve_p6` | `puzzle_solve` — `puz_xep_anh_gia_pha` | 59% |
| 12 | `f12_chapter_complete` | `chapter_complete` | 58% |
| 13 | `f13_paywall_view` | `paywall_view` — `com.game.chapter02` | 55% |
| 14 | `f14_purchase` | `iap_purchase_success` — `com.game.chapter02` | **4%** |

`[[ Bước 7 (P4 - ba hồi chín tiếng) và bước 8 (vào bếp giếng) cố ý KHÔNG nối tiếp nhau trong phễu: P3 và P4 độc lập, người chơi xuống bếp được mà chưa cần giải P4. Khi phân tích phải nhớ điều này, nếu không sẽ đọc nhầm thành "phễu chảy ngược". ]]`

**Luật cảnh báo tự động:**

| Mã | Điều kiện | Mức |
|---|---|---|
| `alrt_step_drop` | Tỷ lệ qua một bước thấp hơn mục tiêu **quá 8 điểm phần trăm** trong 24 giờ | CAO |
| `alrt_p4_wall` | `puzzle_abandon(puz_ba_hoi_chin_tieng) / puzzle_open > 12%` | CAO |
| `alrt_hint_useless` | `hint_view(tier=3).solved_within_180s < 80%` — đáp án mà vẫn không giải được nghĩa là **lỗi trình bày đáp án** | TRUNG BÌNH |
| `alrt_scare_quit` | `jumpscare_quit_signal / jumpscare_play > 6%` ở bất kỳ `scare_id` nào | CAO |
| `alrt_bundle_fail` | `bundle_download(result=FAIL) > 3%` tổng lượt | CAO |

## 6.4. Phát hiện điểm kẹt

| Trường | Giá trị |
|---|---|
| Mốc đo kẹt | **60 / 150 / 300 / 600 giây** — trùng đúng mốc mở gợi ý, để đối chiếu "kẹt" với "được cứu" |
| Định nghĩa bỏ cuộc | Mở câu đố rồi rời khỏi câu đố hoặc kết thúc phiên **mà không có `puzzle_solve` trong 10 phút** |
| Chỉ số theo dõi | `p50_time_to_solve_sec`, `p90_time_to_solve_sec`, `fail_count_mean`, `abandon_rate_pct`, `hint_tier3_rate_pct` |

**Ngưỡng buộc phải chỉnh thiết kế:**

| Ngưỡng | Giá trị | Hành động |
|---|---|---|
| `p50` vượt mục tiêu | **> 2×** thời gian mục tiêu | Xem lại manh mối, **không** hạ giá gợi ý |
| Tỷ lệ bỏ cuộc | **> 12%** | Giãn mốc chờ Tier 1, hoặc hạ ngưỡng thương xót |
| Tỷ lệ dùng Tier 3 | **> 35%** | Câu đố đang bất công — sửa manh mối trong game, không sửa giá |

> **Nguyên tắc đọc số:** mọi điểm kẹt đều là **lỗi thiết kế câu đố**, không phải cơ hội bán gợi ý. Nếu một câu đố sinh ra nhiều doanh thu gợi ý bất thường, đó là báo động đỏ chứ không phải thành tích.

## 6.5. Đo hiệu quả jumpscare

Ba phép đo, đối chiếu chéo với **`docs/06_AN_TOAN_NGUOI_CHOI.md`** (§6.3 luật nghỉ 90 giây, §10.4 telemetry an toàn):

1. **Doạ có tác dụng không:** `jumpscare_play` → `session_end` trong 20 giây → `jumpscare_quit_signal`. Tỷ lệ **lành mạnh là 1–4%**. Trên **6%** là doạ quá tay.
2. **Doạ có bị nhờn không:** so `sec_since_last_scare` với tỷ lệ người chơi đổi `safety_setting`. Nếu khoảng cách trung bình tụt dưới **90 giây** ở bất kỳ phiên nào → luật cooldown đang bị vi phạm → lỗi kỹ thuật, báo tổ kinh dị ngay.
3. **Doạ có đuổi người chơi khỏi chương không:** đối chiếu `scare_id` với bước phễu kế tiếp. Nếu `scare_hinh_nhan_chan_loi` (cú duy nhất không tránh được) làm rơi `f10 → f11` quá **10 điểm phần trăm** → cần hạ cường độ mặc định, **không** cần bán gì thêm.

---

# PHẦN 7 — REMOTE CONFIG

## 7.1. Bảng khoá (**32 khoá** — đếm từ `data/liveops_chapter_01.json`: `len(remote_config_keys) = 32`)

| Khoá | Kiểu | Mặc định | Biên | Cần khởi động lại | Chủ sở hữu |
|---|---|---|---|---|---|
| `liveops_config_version` | string | `1.0.0` | — | Không | LiveOps |
| **`hint_cost_gems`** **(MF)** | int | **5** | 0–50 | Không | LiveOps |
| **`ads_reward_hints`** **(MF)** | int | **1** | 0–5 | Không | LiveOps |
| `hint_tier2_gem_cost` | int | 5 | 0–50 | Không | LiveOps |
| `hint_tier3_gem_cost` | int | 12 | 0–99 | Không | LiveOps |
| `hint_free_wait_sec_tier1` | int | 60 | 10–600 | Không | Design |
| `hint_free_wait_sec_tier2` | int | 150 | 30–900 | Không | Design |
| `hint_free_wait_sec_tier3` | int | 300 | 60–900 | Không | Design |
| `hint_price_escalation_gems` | int | 3 | 0–20 | Không | LiveOps |
| `hint_gem_cost_cap` | int | 20 | 1–99 | Không | LiveOps |
| `mercy_hint_fail_threshold` | int | 3 | 1–10 | Không | Design |
| `mercy_hint_stuck_sec` | int | 240 | 60–900 | Không | Design |
| `rewarded_ads_daily_cap` | int | 6 | 0–20 | Không | LiveOps |
| `ad_cooldown_after_scare_sec` | int | **90** | **90**–600 | Không | **Horror** |
| `iap_chapter02_enabled` | bool | `true` | — | Không | LiveOps |
| `iap_season_bundle_enabled` | bool | `true` | — | Không | LiveOps |
| `paywall_max_impressions_per_day` | int | 2 | 0–5 | Không | LiveOps |
| `paywall_show_after_sec_from_credits` | int | 3 | 0–300 | Không | LiveOps |
| `event_active_id` | string | `""` | — | Không | LiveOps |
| `event_theme_enabled` | bool | `true` | — | Không | LiveOps |
| `addressables_catalog_url` | string | `https://cdn.linhanthon.game/addressables/catalog_chapter_01.json` | — | **Có** | Tech |
| `bundle_download_timeout_sec` | int | **60** ⚠️ | 3–60 *(biên trên đĩa)* | Không | **Tech — `docs/05` §7.2.2 là chủ sở hữu** |
| `bundle_retry_count` | int | 2 | 0–5 | Không | Tech |
| `bundle_wifi_only_default` | bool | `true` | — | Không | Tech |
| `telemetry_sampling_rate` | float | 1.0 | 0.0–1.0 | Không | Data |
| `kill_switch_ads` | bool | `false` | — | Không | LiveOps |
| `kill_switch_iap` | bool | `false` | — | Không | LiveOps |
| `kill_switch_event_theme` | bool | `false` | — | Không | LiveOps |
| `kill_switch_paid_hints` | bool | `false` | — | Không | LiveOps |
| `ab_slot_hint_pricing` | string | `control` | — | Không | Data |
| `ab_slot_paywall_timing` | string | `control` | — | Không | Data |
| `ab_slot_mercy_threshold` | string | `control` | — | Không | Design |

> **⚠️ `bundle_download_timeout_sec` — VÌ SAO Ô "MẶC ĐỊNH" KHÔNG CHÉP LẠI GIÁ TRỊ TRÊN ĐĨA.**
> Đây là ô duy nhất trong bảng trên **cố ý lệch** với `data/liveops_chapter_01.json`, và lệch có khai báo:
>
> | | Giá trị |
> |---|---|
> | Trên đĩa hôm nay (`remote_config_keys[*]`) | `"default": 8`, `"min": 3`, `"max": 60` |
> | `docs/05_TICH_HOP_UNITY_ADDRESSABLES.md` §7.2.2 đòi | **90** *(chấp nhận 60 – 120)*, và **không bao giờ dưới `T2 / 0,35 × 2 = 44 s`* |
> | **Giá trị LiveOps phải đẩy ngay hôm nay** | **60** — mức cao nhất mà biên `max: 60` trên đĩa còn cho phép, đồng thời là **sàn** mà `docs/05` chấp nhận |
>
> **Vì sao 8 là con số hỏng:** `AssetBundleRequestOptions.Timeout` là hết giờ **toàn bộ request**, không phải hết giờ kết nối. Bundle khu vực lớn nhất là **7,73 MB**; ở thông lượng 3G Việt Nam tệ nhất **0,35 MB/s** nó cần **22 giây**. Đặt 8 giây nghĩa là **client tự huỷ mọi lượt tải 3G trước khi chúng kịp xong** — người chơi thấy "lỗi mạng" trên một đường mạng hoàn toàn bình thường. Đồng hồ 8 giây vẫn có chỗ dùng, nhưng là của một khoá **khác**: `bundle_connect_timeout_sec` (theo dõi tiến độ `DownloadHandler`), một trong **4 khoá bổ sung** mà `docs/05` §5.3.1 đòi thêm ngoài 32 khoá của bảng trên.
>
> **Việc còn nợ, ghi ra để không ai quên:** vòng sửa **dữ liệu** kế tiếp phải nâng `bundle_download_timeout_sec` trong `data/liveops_chapter_01.json` lên `"default": 90, "max": 120` và bổ sung 4 khoá của `docs/05` §5.3.1 — **cho tới lúc đó, 60 là giá trị an toàn duy nhất đặt được trong biên hiện có.** Vòng này chỉ sửa tài liệu, không đụng `data/`.

## 7.2. Ba luật của remote config

1. **`ad_cooldown_after_scare_sec` chỉ được tăng, không bao giờ hạ dưới 90.** Đây là luật an toàn, không phải tham số kinh doanh. **Chủ sở hữu của luật 90 giây là `docs/06_AN_TOAN_NGUOI_CHOI.md` §6.3**, nơi ghi cả điều kiện miễn trừ duy nhất và ba nơi con số 90 phải bằng nhau. LiveOps không được sửa.
2. **Không khoá nào được phép biến đường miễn phí thành không tồn tại.** `hint_free_wait_sec_tier3` có trần cứng **900 giây** ở tầng validator; đẩy quá là bị từ chối ở phía máy chủ.
3. **Kill-switch phải có hiệu lực trong vòng một phiên chơi**, không cần cập nhật app. Bật `kill_switch_ads` → nút quảng cáo biến mất, người chơi vẫn dùng được đường chờ miễn phí và đường gem.

## 7.3. Thứ tự ưu tiên khi nạp cấu hình

```
1. Giá trị mặc định đóng trong app (an toàn khi mất mạng hoàn toàn)
2. Bản cache của lần fetch gần nhất
3. Remote config vừa fetch được
4. Ghi đè của biến thể A/B đang gán cho máy này
5. Kill-switch  ←  luôn thắng tất cả
```

---

# PHẦN 8 — Ô THỬ NGHIỆM A/B

## 8.1. Quy tắc gán

| Trường | Giá trị |
|---|---|
| Đơn vị gán | `install_id` |
| Muối băm | `linhanthon_ab_2026` |
| Cố định | **Có** — một máy không bao giờ đổi biến thể giữa chừng |
| Nhóm giữ lại (holdout) | **5%** — không nhận bất kỳ thí nghiệm nào, làm đường cơ sở dài hạn |
| Ô loại trừ lẫn nhau | `ab_slot_hint_pricing` và `ab_slot_paywall_timing` không chạy đồng thời trên cùng một máy |

## 8.2. Ba ô thử nghiệm

### Ô 1 — `ab_slot_hint_pricing` (giá gợi ý)

> **Giả thuyết:** hạ giá Tier 3 xuống 8 gem làm tăng tỷ lệ hoàn thành chương mà không làm giảm doanh thu tổng.

| Biến thể | Phân bổ | Ghi đè |
|---|---|---|
| `control` | 50% | `hint_tier3_gem_cost: 12`, `ads_reward_hints: 1` |
| `cheaper_t3` | 25% | `hint_tier3_gem_cost: 8` |
| `ads_only_t3` | 25% | `hint_tier3_gem_cost: 0`, `ads_reward_hints: 2` |

- Chỉ số chính: `f12_chapter_complete_rate`
- Chỉ số phụ: tỷ lệ dùng Tier 3, gem chi/người, lượt quảng cáo/người
- Lan can: tỷ lệ mua IAP, giữ chân ngày 1, tỷ lệ bỏ câu đố
- Cỡ mẫu tối thiểu **3.000/biến thể**, chạy tối thiểu **14 ngày**
- Dừng sớm nếu bất kỳ lan can nào tụt **> 5% tương đối** với p < 0,05

### Ô 2 — `ab_slot_paywall_timing` (thời điểm paywall)

> **Giả thuyết:** hiện paywall sau khi credits chạy hết làm tăng chuyển đổi, vì người chơi đã tiêu hoá xong cú twist.

| Biến thể | Phân bổ | Ghi đè |
|---|---|---|
| `control` | 50% | `paywall_show_after_sec_from_credits: 3` |
| `after_credits` | 50% | `paywall_show_after_sec_from_credits: 45` |

- Chỉ số chính: `f14_purchase_rate`
- Lan can: giữ chân ngày 1, **điểm đánh giá store**, tỷ lệ thoát app ngay sau paywall
- Dừng sớm nếu điểm store giảm **> 0,2 sao** trong 7 ngày

### Ô 3 — `ab_slot_mercy_threshold` (ngưỡng thương xót)

> **Giả thuyết:** tặng gợi ý miễn phí sau 2 lần sai (thay vì 3) giảm rage-quit ở `puz_ba_hoi_chin_tieng` mà không làm câu đố mất giá trị.

| Biến thể | Phân bổ | Ghi đè |
|---|---|---|
| `control` | 50% | `mercy_hint_fail_threshold: 3` |
| `early_mercy` | 50% | `mercy_hint_fail_threshold: 2` |

- Chỉ số chính: tỷ lệ bỏ cuộc ở `puz_ba_hoi_chin_tieng`
- Dừng nếu tỷ lệ dùng Tier 3 vượt **45%** — dấu hiệu câu đố mất giá trị

## 8.3. Những gì TUYỆT ĐỐI KHÔNG được đem ra A/B test

| Không test | Vì sao |
|---|---|
| Cường độ jumpscare, `screen_flash`, cooldown | Đây là an toàn sinh lý, không phải tham số kinh doanh |
| Có/không có đường gợi ý miễn phí | Vi phạm nguyên tắc N1 |
| Có/không có tuỳ chọn trợ năng | Vi phạm nguyên tắc N4 |
| Lời giải câu đố, `max_fails`, `bounds` hotspot | Phá chứng minh khả giải của `02_puzzle.md` §8 |
| Nội dung cốt truyện của cú twist | Một game chỉ có một sự thật |

---

# PHẦN 9 — AN TOÀN NGƯỜI CHƠI & TUÂN THỦ

## 9.1. Bảng tuân thủ tổng hợp

| # | Yêu cầu | Quy định của dự án | Cài đặt kỹ thuật | Cách kiểm chứng |
|---|---|---|---|---|
| **1** | **Không loot box** | Không hộp quà ngẫu nhiên, không gacha, không quay số. Mọi sản phẩm trả phí liệt kê **chính xác** nội dung nhận được | `no_loot_box.randomized_paid_rewards: false`, `randomized_product_ids: []` | Validator: mọi `products[].grants_*` phải là giá trị xác định; cấm trường mang ngữ nghĩa xác suất |
| **2** | **Rõ giá trước khi mua** | Hiện giá bản địa hoá do store trả về + danh sách nội dung + số dư gem, xác nhận **hai bước** | `price_transparency.*` toàn bộ `true` | QA thủ công 5 vùng; ảnh chụp màn hình lưu hồ sơ phát hành |
| **3** | **Không mẫu tối (dark pattern)** | Không đồng hồ đếm ngược giả, không ô chọn mua tick sẵn, không nút đóng ẩn | `no_dark_pattern_countdown`, `no_pre_checked_purchase_option` | Duyệt UI trước khi build |
| **4** | **Tuân thủ độ tuổi** | Dự kiến: **Apple 17+**, **Google Play/IARC Mature 17+**, **PEGI 16**, **ESRB Mature 17+**, **Việt Nam 16+ (cần pháp chế xác nhận)** | `age_rating.target_rating`, `legal_review_required: true` | Bảng khai nội dung của store khoá lại, không đổi giữa các bản cập nhật |
| **5** | **Mô tả nội dung trung thực** | Khai đủ: kinh dị, cảnh giật mình, đề tài tang lễ, **cái chết của trẻ em**, hủ tục hiến tế, ánh sáng nhấp nháy, rung phản hồi | `age_rating.content_descriptors_vi` | Đối chiếu với màn hình cảnh báo ở **`docs/06_AN_TOAN_NGUOI_CHOI.md` §3.1** — hai nơi phải trùng từng mục |
| **6** | **Lọc nội dung quảng cáo** | Chặn quảng cáo cờ bạc, rượu bia, hẹn hò, nội dung người lớn và quảng cáo **giả lập giao diện hệ thống** | `ad_content_rating_max: MATURE_AUDIENCES_OFF` | Cấu hình phía mạng quảng cáo + kiểm tra mẫu hằng tuần |
| **7** | **Quảng cáo không xen giữa jumpscare** | **Không có interstitial.** Chỉ quảng cáo thưởng, người chơi tự bấm | `no_interstitial_ads: true`, `rewarded_opt_in_only: true` | Sự kiện `ad_blocked_by_rule` phải bắn đúng mọi lần bị chặn |
| **8** | **Khoảng cách với cú doạ** | Không quảng cáo trong **90 giây** sau bất kỳ jumpscare nào | `min_sec_after_jumpscare: 90` | Validator bắt buộc `blocked_windows` chứa `WITHIN_90S_AFTER_ANY_JUMPSCARE` |
| **9** | **Không cắt ngang trải nghiệm** | Cấm quảng cáo trong cutscene, trong thao tác giải đố, trên màn hình cảnh báo an toàn, giữa chuyển cảnh | `blocked_windows` đủ 7 mục | Kiểm tự động lúc chạy |
| **10** | **Âm thanh quảng cáo** | Hạ toàn bộ bus game xuống −∞ trước khi quảng cáo phát, khôi phục sau **400 ms** | `ad_placements[*].audio_rule` | QA tai nghe — quảng cáo không được to hơn game |
| **11** | **Trợ năng luôn miễn phí** | Chế độ nhẹ nhàng, giảm chớp sáng, giảm chuyển động, tắt rung, phụ đề — **tất cả miễn phí, đổi bất cứ lúc nào** | `accessibility_never_monetized.*` toàn bộ `true` | Kế thừa ràng buộc **`docs/06_AN_TOAN_NGUOI_CHOI.md` §1.1** (N1–N3) và bảng truy vết §10.1 |
| **12** | **Không pay-to-win** | Chỉ bán nội dung, tiện ích, trang trí | `fair_play.forbidden_categories` | Phép thử một dòng ở §3.5 |
| **13** | **Quyền riêng tư dữ liệu** | Không PII trong telemetry; dùng `install_id` ẩn danh; ATT trên iOS; quảng cáo cá nhân hoá cần đồng ý | `data_privacy.*` | Tuân thủ GDPR, GDPR-K, CCPA, **Nghị định 13/2023/NĐ-CP** |
| **14** | **Xoá dữ liệu theo yêu cầu** | Hỗ trợ yêu cầu xoá; lưu trữ tối đa **400 ngày** | `data_deletion_request_supported`, `retention_days` | Quy trình hỗ trợ khách hàng |
| **15** | **Bảo vệ chi tiêu** | Trần mềm **20 USD/ngày** → nhắc nhở và xác nhận lại (**không tự chặn**); lịch sử mua hàng xem được trong Cài đặt; có đường dẫn hướng dẫn hoàn tiền | `spending_protection.*` | QA luồng mua nhiều lần liên tiếp |
| **16** | **Không mời mua ở đỉnh sợ** | Không hiện paywall/cửa hàng trong vùng cao trào kinh dị | `no_purchase_prompt_during_horror_peak: true` | Đối chiếu với đường cong sợ hãi ở **`01_KICH_BAN_CHAPTER_01.md` §6** (bảng beats, hai thang đo) và luật nghỉ 90 giây ở **`docs/06_AN_TOAN_NGUOI_CHOI.md` §6.3** |
| **17** | **Khôi phục mua hàng** | Nút rõ ràng ở Cài đặt và paywall | `iap.restore.enabled: true` | Bắt buộc theo App Store Guideline 3.1.1 |

## 9.2. Ba điều tuyệt đối không làm — ghi để người sau đọc

1. **Không bán chế độ nhẹ nhàng.** Người sợ quá mức là người cần giúp, không phải phân khúc khách hàng.
2. **Không bật quảng cáo ngay sau một cú doạ.** Nhịp tim người chơi đang ở đỉnh; chen quảng cáo vào đó là khai thác phản ứng sinh lý, và nó sẽ hiện ra trong điểm đánh giá store trong vòng một tuần.
3. **Không biến điểm kẹt thành điểm bán.** Nếu một câu đố sinh doanh thu gợi ý cao bất thường, việc phải làm là **sửa câu đố**.

---

# PHẦN 10 — VẬN HÀNH

## 10.1. Quy trình phát hành cấu hình

| Bước | Việc | Ai duyệt |
|---|---|---|
| 1 | Sửa `data/liveops_chapter_01.json`, tăng `config_version` | LiveOps |
| 2 | Chạy `tools/validate_level.py --liveops data/liveops_chapter_01.json` — **phải 0 lỗi** | Tự động |
| 3 | Đẩy lên môi trường `STAGING`, QA chạy bộ kiểm tra §10.3 | QA |
| 4 | Phát hành **5% → 25% → 100%**, mỗi bậc cách nhau tối thiểu 24 giờ | LiveOps + Data |
| 5 | Theo dõi 5 luật cảnh báo ở §6.3 suốt 72 giờ | Data |
| 6 | Nếu bất kỳ luật CAO nào bắn → **bật kill-switch tương ứng, quay về bản trước** | Trực vận hành |

## 10.2. Kill-switch

| Kill-switch | Bật lên thì sao | Người chơi mất gì |
|---|---|---|
| `kill_switch_ads` | Ẩn mọi nút quảng cáo | Không mất gì — vẫn còn đường chờ và đường gem |
| `kill_switch_iap` | Ẩn cửa hàng và paywall | Không mất gì trong Chương 1 |
| `kill_switch_event_theme` | Trả về giao diện gốc toàn bộ | Chỉ mất lớp sơn sự kiện |
| `kill_switch_paid_hints` | Gợi ý **chỉ còn đường miễn phí** | Không mất gì — chỉ phải chờ đủ giờ |
| `kill_switch_telemetry` | **Tắt toàn bộ đường ống đo đạc** | Không mất gì trong game — mất số liệu vận hành của phiên đó |

> **Năm kill-switch** được thiết kế sao cho **bật cả năm cùng lúc thì game vẫn chơi trọn vẹn Chương 1**. Đó là phép thử cuối cùng của nguyên tắc N1.
>
> **⚠️ Bốn trong năm bật được từ xa, cái thứ năm thì chưa.** Đếm từ `data/liveops_chapter_01.json`: `rollout.kill_switches` có **5** khoá; `remote_config_keys` mới có **4** khoá `kill_switch_*` — **thiếu đúng `kill_switch_telemetry`** (bảng §7.1). Một công tắc chỉ nằm trong `rollout` là công tắc **nằm trong bundle dữ liệu**: muốn bật phải dựng lại bundle, đẩy catalog, chờ triển khai — hàng chục phút, không phải công tắc khẩn cấp. Mà telemetry lại đúng là cái phải tắt được nhanh nhất khi có sự cố riêng tư. Việc còn nợ ở vòng sửa **dữ liệu**: bổ sung `kill_switch_telemetry` vào `remote_config_keys`. Chủ sở hữu phân tích: `docs/05_TICH_HOP_UNITY_ADDRESSABLES.md` §5.3.1.

## 10.3. Danh sách kiểm tra QA trước khi bàn giao

| # | Hạng mục kiểm tra | Kết quả phải đạt |
|---|---|---|
| 1 | Chơi hết Chương 1 không tiêu một gem, không xem một quảng cáo | Hoàn thành được, không kẹt |
| 2 | Bật cả **5** kill-switch rồi chơi lại (4 từ remote config, `kill_switch_telemetry` từ `rollout`) | Hoàn thành được |
| 3 | Chờ đủ 300 giây ở cả 6 câu đố | Tier 3 mở miễn phí ở cả 6 |
| 4 | Sai 7 lần liên tiếp ở mỗi câu đố | Nhận đủ 3 nấc gợi ý thương xót, **không thấy quảng cáo, không thấy paywall** |
| 5 | Mua `com.game.chapter02`, gỡ app, cài lại, bấm Khôi phục | Nhận lại quyền, không mất tiền lần hai |
| 6 | Mua ở cả 8 vùng giá (VN, US, TH, ID, PH, MY, SG, SEA_DEFAULT) | Giá hiển thị đúng tiền tệ bản địa của store |
| 7 | Bật máy bay giữa lúc tải bundle sự kiện | Nền gốc được dùng, **không hộp thoại lỗi, không treo** |
| 8 | Đặt đồng hồ máy vào `2026-10-25` rồi `2026-11-04` | Theme bật đúng ngày, tắt đúng ngày theo giờ máy chủ |
| 9 | Lùi đồng hồ máy về 2020 | Sự kiện **không** bật; dùng thời gian máy chủ |
| 10 | Kích hoạt jumpscare rồi bấm ngay nút gợi ý | Nút bị chặn trong `JUMPSCARE_ENVELOPE`; `ad_blocked_by_rule` bắn |
| 11 | Xem 6 quảng cáo rồi thử lượt thứ 7 | Báo hết lượt **kèm nhắc thời gian chờ miễn phí còn lại** |
| 12 | Bật `gentle_mode` giữa một cú doạ | Áp dụng ngay, miễn phí, không hỏi mua gì |
| 13 | Đối chiếu mọi `text_key` LiveOps với file localization | Không khoá nào thiếu bản dịch |
| 14 | Chạy validator với `schema/liveops.schema.json` | 0 lỗi, 0 cảnh báo |

---

# PHẦN 11 — BÀN GIAO

## 11.1. File thuộc bước này

| Đường dẫn | Nội dung |
|---|---|
| `/home/user/HackTheBox/LinhAnThon/docs/04_LIVEOPS_MONETIZATION.md` | Tài liệu này |
| `/home/user/HackTheBox/LinhAnThon/data/liveops_chapter_01.json` | Cấu hình LiveOps, `schema_version: 1` |

## 11.2. Phụ thuộc sang bước khác

| File | Quan hệ |
|---|---|
| `schema/liveops.schema.json` | Phải kiểm được **17 bất biến** liệt kê ở `validation.invariants` của file JSON (đếm từ `data/liveops_chapter_01.json`: `len(validation.invariants) = 17`) |
| `tools/validate_level.py` | Cần thêm cờ `--liveops` để kiểm file này |
| `docs/03_DATA_SPEC.md` | Mô tả `hint_tier_unlocked`, `hint_timer_accumulated` trong save state — phải khớp §2.5 tài liệu này |
| `docs/05_TICH_HOP_UNITY_ADDRESSABLES.md` | Nhãn bundle sự kiện (`evt_halloween_2026`) và luật fallback §4.4 |
| `data/areas/*.json` | Nguồn `background_asset_url` cho fallback khi `override_bg` tải hỏng |
| **`docs/06_AN_TOAN_NGUOI_CHOI.md`** | **Chủ sở hữu mọi ràng buộc an toàn mà tài liệu này phải tuân theo** — N1–N4 (§1.1), danh sách không-bao-giờ-override (§1.2), màn hình cảnh báo (§3.1), luật nghỉ 90 giây và điều kiện miễn trừ (§6.3), bảng truy vết tuỳ chọn an toàn ↔ `data/liveops_chapter_01.json` (§10). **Khi tài liệu này lệch với docs/06 ở bất kỳ điểm an toàn nào, docs/06 thắng.** |

## 11.3. Mười bảy bất biến validator phải kiểm

> Danh sách dưới đây là **bản chép một-đối-một** của `validation.invariants` trong `data/liveops_chapter_01.json` — **17 phần tử**, không nhiều hơn, không ít hơn. Bản trước dừng ở 16 vì bất biến 17 được thêm sau khi mục này được viết; xem §3.6.1.

1. `hint_system.tiers[*].gem_cost` tăng dần theo tier.
2. `hint_system.tiers[*].unlock_free_after_sec` tăng dần theo tier.
3. `tiers[3].unlock_free_after_sec ≤ max_wait_sec_to_full_solution` (300).
4. `free_path_guaranteed = true` và mọi tier có ít nhất một `unlock_source` với `gem_cost = 0` và `ads_required = 0`.
5. `iap.products[*].iap_product_id` duy nhất và khớp id đã khai trên store.
6. `regional_pricing[*].region_code` duy nhất trong mỗi sản phẩm, bắt buộc có `VN`, `US`, `SEA_DEFAULT`.
7. `event_start < event_end` ở mọi sự kiện.
8. Hai sự kiện `enabled: true` không chồng cửa sổ trên cùng một area.
9. `override_bg` phải nằm trong `addressables.bundles` của chính sự kiện đó.
10. `theme_override.does_not_change` phải chứa `hotspot_bounds`, `puzzle_solution`, `jumpscare_trigger_type`, `max_fails`.
11. Mọi `ad_placements[*].blocked_windows` chứa `DURING_JUMPSCARE_ENVELOPE` và `WITHIN_90S_AFTER_ANY_JUMPSCARE`.
12. `player_safety_compliance.no_loot_box.randomized_paid_rewards = false`.
13. `telemetry.events[*].event_name` duy nhất, snake_case, độ dài ≤ 40.
14. `ab_tests.slots[*].variants[*].allocation_pct` cộng lại đúng 100 cho mỗi ô.
15. `remote_config_keys[*].key` duy nhất; mọi khoá dùng trong `ab_tests` overrides phải tồn tại trong `remote_config_keys`.
16. `gem_economy.balance_targets.expected_free_earn_chapter_01 ≥ expected_spend_p90_player`.
17. **`iap.products[*].requires.flag` phải có nguồn cấp thật** — hoặc là cờ Chương 1 khai trong `chapter_complete_flag` / `exported_flags` của `data/chapter_01.json`, hoặc do chính một `iap.products[*].unlock.grants_flags` trong file này cấp. Cờ không có nguồn cấp ⇒ **[LỖI]**, vì nó khoá vĩnh viễn cổng bán. Đặc tả đầy đủ ở **§3.6.1**; validator: `tools/validate_level.py` giai đoạn 11.

---

> **Câu chốt của tài liệu này.**
> Linh An Thôn bán một câu chuyện, không bán lối thoát khỏi câu chuyện.
> Người chơi không trả tiền để qua Chương 1 — họ trả tiền vì đến cuối Chương 1, họ cần biết chuyện gì xảy ra tiếp theo.
