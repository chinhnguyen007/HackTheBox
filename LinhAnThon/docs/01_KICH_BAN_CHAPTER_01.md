# LINH AN THÔN — CHƯƠNG 1
## KỊCH BẢN CHI TIẾT MÀN CHƠI (MASTER SCRIPT — BƯỚC 1)

| Trường | Giá trị |
|---|---|
| Dự án | **Linh An Thôn — Chapter 1** |
| Tài liệu | `docs/01_KICH_BAN_CHAPTER_01.md` — deliverable **BƯỚC 1** của Master Form |
| Phạm vi | Vị trí vật phẩm · cốt truyện · logic câu đố · nhịp kinh dị · chứng minh khả giải |
| Thể loại | 2D Point-and-Click folk horror Việt Nam, "Áo Cưới Giấy Style" (Paper Bride) |
| Bối cảnh | Thôn Linh An, xã Linh Nam, huyện Thuận Thành, tỉnh Hà Bắc — chiều rằm tháng Bảy năm Bính Tý (28-8-1996) |
| Chủ đề | Hủ tục **"cúng thế mạng"** — hiến tế một người sống để thay mạng cho người khác, để yên lòng "Bà Cô" trong nhà |
| Nền tảng | Android & iOS · APK engine ≤ 30 MB · toàn bộ asset tải qua Unity Addressables (remote bundle) |
| Cơ chế | Orthographic 2D phẳng · Hotspots + Inventory + Puzzles + Jump-scare theo trigger |
| Độ phân giải thiết kế | **1920 × 1080**, gốc toạ độ **(0,0) ở góc trên-bên trái**, x sang phải, y xuống dưới |
| Ngôn ngữ | Văn bản: tiếng Việt có dấu. Mã định danh & khoá JSON: snake_case không dấu |
| Nguồn sự thật | **SPINE đã chốt** — không đổi, không thêm bất kỳ `area_id` / `item_id` / `puzzle_id` / `scare_id` nào |

> **Tài liệu này đọc được độc lập.** Nó tổng hợp và hoà giải bốn tài liệu thiết kế nội bộ (narrative · puzzle · world · horror) thành một bản kịch bản duy nhất, đủ để tổ đồ hoạ, tổ dữ liệu, tổ âm thanh và QA làm việc mà không cần mở thêm tài liệu nào khác.

---

# 0. CÁCH ĐỌC & QUY ƯỚC HỢP NHẤT

## 0.1. Quy ước trình bày

| Ký hiệu | Nghĩa |
|---|---|
| Khối trích dẫn `>` kèm `text_key` | **Văn bản thành phẩm** — đưa thẳng vào file localization, không viết lại |
| `[[ ... ]]` | Ghi chú sản xuất, không hiển thị trong game |
| ★ | Beat gốc thuộc SPINE (14 beat), giữ nguyên thứ tự và nội dung |
| 🔔 | Beat có jumpscare bắn |
| 😮‍💨 | Nhịp nghỉ bắt buộc (relief window), khoá cứng bằng hệ thống |
| *(phái sinh)* | Phần tử **không thuộc SPINE**, do tổ thiết kế đề xuất bổ sung, **chờ Lead ký duyệt** |

## 0.2. Thứ tự ưu tiên khi các tài liệu thiết kế lệch nhau

Bốn tài liệu nguồn viết song song nên có chỗ mâu thuẫn. Bảng dưới là **phán quyết cuối cùng**, áp dụng cho toàn bộ khâu sản xuất:

| Hạng mục | Tài liệu nắm quyền | Ghi chú |
|---|---|---|
| `area_id` · `item_id` · `puzzle_id` · `scare_id` · logline · twist · 14 beat gốc | **SPINE** | Tuyệt đối. Không tài liệu nào được sửa |
| Lore, niên biểu, tên nhân vật, nội dung văn bản đọc được, độc thoại | **01_narrative** | Chủ sở hữu tường thuật |
| `bounds`, id hotspot, `action_type`, tham số hotspot, quy ước `text_key` | **03_world** | Chủ sở hữu toạ độ; đã hợp nhất bí danh ở mục 0.4 |
| `solution`, manh mối, hành vi khi sai, bậc gợi ý, đồ thị phụ thuộc | **02_puzzle** | Chủ sở hữu logic câu đố |
| Thông số jumpscare (envelope, flash, haptic, cooldown), thiết kế âm thanh | **04_horror** | Chủ sở hữu nhịp kinh dị |

## 0.3. Bảng xử lý xung đột đã phát hiện (đã chốt trong tài liệu này)

| # | Điểm lệch | Bản A | Bản B | **Phán quyết** |
|---|---|---|---|---|
| X1 | Tuổi Bà Cô lúc mất | 17 tuổi *(niên biểu 1936–1953)* | 19 tuổi *(vài chuỗi văn bản)* | **17 tuổi.** Mọi chuỗi ghi "mười chín" phải sửa thành "mười bảy" |
| X2 | Năm khắc trên năm vạch dao ở cột bếp | 1953 / 1961 / 1968 / 1976 / *(trống)* | 1992 → 1996 | **1953 / 1961 / 1968 / 1976 / (trống).** Năm vạch = năm lần lễ, gắn niên biểu hủ tục |
| X3 | Nội dung Bảy Điều Cấm Kỵ | Bản gắn chặt với cơ chế câu đố | Bản khác nội dung | **Bản gắn cơ chế** (mục 2.4.5). Mỗi điều phải ánh xạ được vào một câu đố hoặc một jumpscare |
| X4 | Tuổi thọ bà nội trên cáo phó | 79 *(1918–1996)* | 78 | **79 tuổi** |
| X5 | Số ngày nhà bỏ không | 10 ngày | 9 ngày | **10 ngày** (tang 25-8, chơi 28-8, tính từ hôm đưa tang) |
| X6 | Chữ khắc lòng gáo dừa | "ĐỪNG SOI" | "ĐỪNG SOI LÂU" | **"ĐỪNG SOI"** — ngắn hơn, lạnh hơn |
| X7 | Quy ước `text_key` | `txt_<area>_<doi_tuong>` | `txt_examine_* / txt_thoai_* / txt_khoa_*` | **Quy ước 03_world** cho hotspot. Khoá ngoài hotspot (lore, déjà vu, cảnh kết) giữ tên gốc |
| X8 | Nhãn đặt hàng mã | Bà Tơ đặt, 1996 | Bà nội mua, 24-8-1996 | **Bà Tơ đặt** — đây là mũi neo "có người sống đang dọn đường lễ" |

## 0.4. Danh mục ID toàn chương

**Thuộc SPINE — bất biến:**

| Loại | Số lượng | Danh sách |
|---|---|---|
| `area_` | 5 | `area_san_gach` · `area_hien_nha` · `area_gian_tho` · `area_bep_gieng` · `area_gac_xep` |
| `item_` | 10 | `item_chia_khoa_dong` · `item_giay_ban_va_than` · `item_ban_rap_chu_the` · `item_den_dau` · `item_dui_mo` · `item_bai_vi_khuyet_danh` · `item_dai_vai_dieu` · `item_chai_dau_hoa` · `item_den_dau_sang` · `item_ao_cuoi_giay` |
| `puz_` | 6 | `puz_khoa_bat_quai` · `puz_rap_chu_the_menh` · `puz_tuan_tu_le_cung` · `puz_ba_hoi_chin_tieng` · `puz_thap_lai_den_dau` · `puz_xep_anh_gia_pha` |
| `scare_` | 6 | `scare_bong_trong_chum` · `scare_ban_tay_giay_sau_manh` · `scare_di_anh_quay_mat` · `scare_mat_duoi_day_gieng` · `scare_hinh_nhan_chan_loi` · `scare_ao_cuoi_quay_dau` |

**Phái sinh — KHÔNG thuộc SPINE, chờ Lead ký duyệt:**

| `scare_id` phái sinh | Area | Lý do cần | Nếu Lead **không duyệt** |
|---|---|---|---|
| `scare_khoi_tu_hinh_nguoi` | `area_gian_tho` | 3 scare gốc của chương đã bị "chiếm" trigger khác; P3 và P4 không còn phản hồi thất bại | Đặt `wrong_action_jumpscare: null` cho P3/P4; giữ nguyên phản hồi sai không-jumpscare |
| `scare_anh_tho_thieu_mat` | `area_gac_xep` | P6 là câu đố dài nhất chương, không có phản hồi thất bại thì đường cong võng ngay trước cú kết | Đặt `wrong_action_jumpscare: null` cho P6 |

> **Nội dung của hai scare phái sinh lấy nguyên từ mô tả sai-lầm đã có sẵn trong `y_tuong` của SPINE** ("nhang tắt ngấm, khói tụ lại thành hình người"; "mảnh nào cũng mang một khuôn mặt bị khoét"), nên **không phát sinh nội dung mới**, chỉ nâng cấp thành cú dọa có tên. Toàn bộ logic giải đố **không phụ thuộc** vào chúng.

**Hotspot (`hs_`)** — 66 hotspot, id lấy theo bảng canonical của 03_world. Đây **không phải id thuộc SPINE**, mà là lớp triển khai bắt buộc phải có để màn chơi vận hành; danh sách đầy đủ ở Phần 3.

## 0.5. Ánh xạ `trigger_type` của SPINE sang tập hợp lệ của schema

SPINE mô tả trigger bằng ngôn ngữ kịch bản, không trùng tập hợp lệ của hợp đồng schema. **Giữ nguyên `scare_id`, chỉ ánh xạ trigger:**

| `scare_id` (SPINE) | `trigger_type` trong SPINE | `trigger_type` hợp lệ theo schema | Tham số | Lý do ánh xạ |
|---|---|---|---|---|
| `scare_bong_trong_chum` | ON_HOTSPOT_CLICK | `ON_PUZZLE_FAIL_COUNT` | `max_fails: 3` trên `puz_khoa_bat_quai` | Chum nước nằm ngay sau lưng người chơi khi cúi vặn ổ khoá → mô tả gốc giữ nguyên 100 % |
| `scare_ban_tay_giay_sau_manh` | ON_PUZZLE_SOLVE | `ON_COLLECT_ITEM` | `item_ban_rap_chu_the` | Giải xong P2 là khoảnh khắc vật phẩm được trao = trùng khít "nét than cuối cùng hiện lên" |
| `scare_di_anh_quay_mat` | ON_ITEM_PICKUP | `ON_COLLECT_ITEM` | `item_dui_mo` | Nguyên văn |
| `scare_mat_duoi_day_gieng` | ON_PUZZLE_FAIL | `ON_PUZZLE_FAIL_COUNT` | `max_fails: 3` trên `puz_thap_lai_den_dau` | Nguyên văn, thêm ngưỡng đếm |
| `scare_hinh_nhan_chan_loi` | ON_AREA_ENTER | `ON_ENTER_AREA` | lần vào đầu tiên duy nhất | Nguyên văn |
| `scare_ao_cuoi_quay_dau` | ON_INVENTORY_USE | `ON_TIMER` | delay 0.4 s trong cutscene kết chương | **Không** dùng `ON_WRONG_ITEM_USE` vì đây là thao tác **đúng**. Cutscene khởi động bởi hotspot `USE_ITEM`, jumpscare bám timer của cutscene |

---

# 1. TÓM TẮT CHƯƠNG

## 1.1. Logline (nguyên văn SPINE)

> Trở về ngôi nhà tổ ở làng Linh An sau đám tang bà nội, bạn lần theo mùi nhang lạnh và tiếng mõ vọng trong đêm để hiểu vì sao tên mình bị xóa khỏi gia phả — và phát hiện cả làng vẫn âm thầm giữ tục "cúng thế mạng" cho Bà Cô trong nhà.

## 1.2. Một câu pitch cho store

> Bạn về chịu tang muộn. Cổng nhà khóa trái từ bên trong. Trên mâm cúng, quả còn tươi. Trong bếp, than còn đỏ. Nhà đã bỏ không mười ngày — vậy ai vừa thắp hương?

## 1.3. Chủ đề

**Chủ đề gốc:** *Cái tên là sợi dây duy nhất buộc một con người vào cõi sống. Xóa tên một người là giết người ấy trước khi người ấy kịp chết.*

| # | Trục chủ đề | Cách nó hiện ra trong gameplay |
|---|---|---|
| 1 | **Tên gọi và sự tồn tại** | Tục đặt tên xấu ở Bắc Bộ ("cái Đĩ", "thằng Cu") vốn là hành vi thương con; Linh An lật ngược nó thành công cụ xoá danh tính. Hình ảnh chốt: bức ảnh thờ xếp xong vẫn khuyết đúng một khuôn mặt |
| 2 | **Tình thương làm hỏng nghi lễ, và nghi lễ trả thù tình thương** | Bà nội bỏ dở lễ vì thương cháu; hai mươi năm sau chính cái lễ dở dang ấy gọi đứa cháu quay về. Không có con quỷ nào săn đuổi — chỉ có một thủ tục hành chính của cõi âm chưa được đóng dấu |
| 3 | **Đám đông và sự đồng thuận im lặng** | Không ai trong làng là ác nhân. Tất cả đều là người tử tế đang sợ. Cái đáng sợ không phải một hồn ma, mà là cả một cộng đồng cùng gật đầu |

> **Tuyên ngôn tông cho toàn ê-kíp:** Linh An Thôn không dọa bằng quái vật. Nó dọa bằng **thủ tục**. Mọi thứ trong nhà đều đã được bày sẵn, đúng trình tự, chờ người chơi tự tay làm nốt.

## 1.4. Cú twist (nguyên văn SPINE)

> Bản rập chữ "Thế Mệnh", bài vị khuyết danh và cuốn sổ ghi tên trên gác xép ghép lại thành một sự thật: hai mươi năm trước, chính người chơi là đứa trẻ được dân làng chọn để cúng thế mạng cho Bà Cô — người ta đổi tên, xóa tên khỏi gia phả và khoét khuôn mặt của người chơi khỏi bức ảnh thờ, coi như đã "chết thay" xong. Bài vị khuyết danh mà người chơi tra vào khe cửa gác xép làm then thực ra là bài vị của chính mình, và bộ áo cưới giấy treo cạnh hình nhân được may vừa in số đo người chơi. Khoảnh khắc người chơi tự tay khoác áo cưới giấy lên hình nhân thế mạng, nghi lễ bị bỏ dở hai mươi năm được hoàn tất — tiếng mõ nổi lên khắp làng, báo rằng "người thế mạng" đã tự nguyện quay về nhận phần của mình.

### 1.4.1. Kiến trúc cài cắm twist — ba tầng, chín mũi neo

**Tầng A — người chơi tinh ý bắt được ngay ở Khu 1–2** *(tạo cảm giác "tôi đoán đúng")*

| # | Mũi neo | Đặt ở | Nghĩa thật |
|---|---|---|---|
| A1 | Cáo phó ở cột cổng liệt kê con cháu chịu tang, **không có tên người chơi** | `area_san_gach` | Người chơi đã bị khai tử trên giấy tờ họ tộc |
| A2 | Dây phơi có **một mảnh khăn xô còn ướt** giữa cái sân khô, nhà bỏ không mười ngày | `area_san_gach` | Có người vẫn đang để tang, và vẫn đang ở đây |
| A3 | Dòng than sau bình phong: *"TRONG NHÀ NÀY KHÔNG AI CÓ TÊN"* | `area_hien_nha` | Quy tắc vận hành của hủ tục |

**Tầng B — lộ dần ở Khu 3–4** *(từ "nhà này có chuyện" sang "chuyện này liên quan đến tôi")*

| # | Mũi neo | Đặt ở | Nghĩa thật |
|---|---|---|---|
| B1 | Trang gia phả có **một dòng bị cạo bằng dao**, giấy mỏng đến mức soi lên thấy sáng | `area_gian_tho` | Tên người chơi từng ở đó |
| B2 | Khám thờ Bà Cô chỉ chứa **bài vị gỗ mới, chưa khắc chữ** | `area_gian_tho` | Bài vị chờ một cái tên không bao giờ được viết |
| B3 | Cột bếp có **năm vạch dao kèm năm**, vạch thứ năm **chưa điền năm** | `area_bep_gieng` | Lễ thứ năm chưa kết thúc — nó đang diễn ra |
| B4 | Sổ chợ của bà nội ghi số đo áo cưới giấy: **dài 1 thước 52 — ngực 82 — dài tay 56** | `area_bep_gieng` | Số đo người lớn, đặt may cho một đứa bé bảy tuổi |

**Tầng C — chốt hạ ở Khu 5** *(không còn đường chối)*

| # | Mũi neo | Đặt ở | Nghĩa thật |
|---|---|---|---|
| C1 | Sổ ghi tên: dòng **Bính Thìn 1976 — Nguyễn Thị Liên, tên tục cái Đĩ Con — LỄ CHƯA THÀNH** | `area_gac_xep` | Tên khai sinh gốc của người chơi |
| C2 | Bức ảnh xếp xong vẫn **khuyết đúng một khuôn mặt** ở vị trí đứa cháu út | `area_gac_xep` | Mặt người chơi bị khoét khỏi ảnh thờ |

**Mũi neo mang theo người chơi (inventory-side):** người chơi mang trong túi áo **phiếu đo của hiệu may** nơi cô làm việc ở Hà Nội. Khi so với sổ chợ ở `area_bep_gieng`, số đo trùng khít.

`[[ Phiếu đo KHÔNG phải item hành trang. Nó là nội dung EXAMINE của hs_xe_dap_tui_vai, luôn đọc lại được — để không phát sinh item_id ngoài SPINE. ]]`

### 1.4.2. Cú đảo cuối — "hành động của người chơi chính là nghi lễ"

Suốt chương, hệ thống dạy người chơi rằng *làm đúng thủ tục thì cửa mở*. Đến `area_gac_xep`, người chơi đã được huấn luyện thành một người hành lễ thành thạo. Hành động cuối — khoác áo cưới giấy lên hình nhân — với người chơi chỉ là "bước giải đố tiếp theo". Với dân làng, đó là **nghi thức thành**.

Điều cấm kỵ số Bảy đã ghi rõ trên mặt trong nắp hòm, **đặt đúng chỗ người chơi phải mở hòm mới lấy được vàng mã** — nghĩa là phần lớn người chơi sẽ đọc lướt qua rồi vẫn tự tay làm. Đây là thiết kế cố ý: cảm giác tội lỗi hậu-twist ("mình đã đọc mà") mạnh hơn cảm giác bị lừa.

## 1.5. Thời lượng chơi ước tính

| Khu vực | Thứ tự | Thời lượng mục tiêu | Câu đố | Ghi chú nhịp |
|---|---|---|---|---|
| `area_san_gach` | 1 | **6–8 phút** | P1 | Khu dạy cơ chế hotspot |
| `area_hien_nha` | 2 | **8–10 phút** | P2 | Khu dạy cơ chế `USE_ITEM`, mật độ dọa thấp có chủ ý |
| `area_gian_tho` | 3 | **12–15 phút** | P3 + P4 | Khu dài nhất, trung tâm thông tin, hai câu đố |
| `area_bep_gieng` | 4 | **10–12 phút** | P5 | Khu tối nhất chương |
| `area_gac_xep` | 5 | **10–12 phút** | P6 | Khu tiết lộ và đóng chương |
| **Tổng** | | **≈ 43 phút** (trung vị) · **45–60 phút** lần chơi đầu | 6 câu đố | Thuần giải đố ≈ 15 phút; còn lại là khám phá, đọc và cutscene |

**Đối chiếu độ khó:** 2/5 → 3/5 → 3/5 → **4/5** → 3/5 → **4/5**. Hai đỉnh khó (P4, P6) rơi đúng Beat 8 (giữa chương, trước khi đổi không gian xuống bếp) và Beat 13 (ngay trước twist).

## 1.6. Bản đồ luồng chơi

```
                    ┌──────────────────────────────┐
                    │   area_san_gach  (thứ tự 1)  │
                    │   mở màn — không điều kiện    │
                    └───────────┬──────────────────┘
               hs_cua_vao_hien  │  ▲  hs_xuong_san_gach
   GATE: có item_chia_khoa_dong │  │  (tự do, hai chiều)
                                ▼  │
                    ┌──────────────┴───────────────┐
                    │   area_hien_nha  (thứ tự 2)  │
                    └───────────┬──────────────────┘
                 hs_cua_buc_ban │  ▲  hs_ra_hien
   GATE: flag_binh_phong_da_tra │  │  (tự do, hai chiều)
                                ▼  │
                    ┌──────────────┴───────────────┐
        ┌───────────┤   area_gian_tho  (thứ tự 3)  ├───────────┐
        │           │      ★ NÚT CỔ CHAI CHƯƠNG     │           │
        │           └──────────────────────────────┘           │
hs_cua_hau_xuong_bep│                                │hs_cau_thang_gac
GATE: đã giải P3    │                    GATE: có item_den_dau_sang
        │           ▲                       VÀ flag_then_gac_da_tra
        ▼           │ hs_len_gian_tho                ▼           ▲
┌───────────────────┴──────┐            ┌────────────────────────┴─┐
│ area_bep_gieng (thứ tự 4)│            │  area_gac_xep (thứ tự 5) │
│  hai chiều, tự do        │            │  hs_xuong_gian_tho —     │
└──────────────────────────┘            │  KHOÁ LẠI sau khi nhặt   │
                                        │  item_ao_cuoi_giay       │
                                        └──────────────────────────┘
```

**Thứ tự bắt buộc tối thiểu (chuỗi phụ thuộc cứng):**
`puz_khoa_bat_quai` → `puz_rap_chu_the_menh` → `puz_tuan_tu_le_cung` → *(`puz_ba_hoi_chin_tieng` chen vào bất cứ đâu sau khi vào gian thờ)* → `puz_thap_lai_den_dau` → `puz_xep_anh_gia_pha`.

**Điểm không-quay-lại duy nhất của chương:** sau khi nhặt `item_ao_cuoi_giay` trên gác xép, `hs_xuong_gian_tho` khoá vĩnh viễn.

---

# 2. NHÂN VẬT & LORE HỦ TỤC "CÚNG THẾ MẠNG"

## 2.1. Bảng nhân vật tổng

| # | Nhân vật | Trạng thái | Vai trò thiết kế | Hiện diện trên màn hình |
|---|---|---|---|---|
| 1 | **"Hương" / Nguyễn Thị Liên** | Sống — người chơi | Chủ thể; cũng là vật tế | Chỉ thấy **bàn tay**, **bóng đổ**, và mặt phản chiếu trong chum (luôn bị che/mờ) |
| 2 | **"Bà Cô" / Nguyễn Thị Gái** | Vong — người nhận lễ | Áp lực nền của cả chương | **Không bao giờ hiện hình, không bao giờ nói.** Chỉ hiện qua nước, mõ, hương, hình nhân |
| 3 | **Bà nội / Nguyễn Thị Nhỡ** | Vong — đồng minh | Lực duy nhất đẩy người chơi ra; và bà thất bại | Chữ viết tay (`hw_ba_noi`), mảnh khăn xô ướt, giọng gọi vọng qua khe ván sàn |
| 4 | **"cái Đĩ Nhài" & "thằng Cu Tý"** | Vong — hai đứa trẻ thế mạng đời trước | Chỉ đường, cho người chơi thấy cái giá | Vệt tay bùn, guốc trẻ con dưới giếng, hình que trên vách bồ hóng, tiếng cười hai giọng < 0,4 s |
| 5 | **Ông từ Nguyễn Văn Đối** | Vong — thủ tục | Tác giả của toàn bộ nghi lễ | Chữ nho chân phương (`hw_ong_tu`), mùi mực tàu, văn khấn tự lật trang khi người chơi bí |
| 6 | **Bà đồng Tơ / Nguyễn Thị Tơ** | **Sống**, 84 tuổi | Phản diện thật; nguồn gốc hủ tục | Không lên hình cho tới **khung hình cuối cùng**. Suốt chương chỉ là dấu vết của người còn sống |

## 2.2. Hồ sơ nhân vật

### 2.2.1. NGƯỜI CHƠI — "Hương" / Nguyễn Thị Liên

| Trường | Nội dung |
|---|---|
| Tên đang dùng | **Trần Thị Hương**, 27 tuổi |
| Tên khai sinh gốc | **Nguyễn Thị Liên**, sinh 16-9-1969 tại thôn Linh An |
| Tên tục (tên xấu) | **cái Đĩ Con** |
| Nghề | **Thợ may bậc 3**, hiệu may nhỏ khu Hàng Đào, Hà Nội |
| Gia cảnh | Cha Nguyễn Văn Đoan hy sinh 1972 · mẹ Phạm Thị Vân mất 1975 · bà nội Nguyễn Thị Nhỡ nuôi tới 1976 rồi gửi lên Hà Nội cho bà dì Trần Thị Tư, làm lại khai sinh mang họ Trần |
| Ký ức về làng | Gần như trắng. Chỉ ba mảnh: mùi dầu hỏa, tiếng gầu tôn va thành giếng, và cảm giác bị bế đi trong đêm lạnh |

**Động cơ, theo thứ tự trồi lên:**

| Tầng | Động cơ |
|---|---|
| Bề mặt | Về chịu tang muộn, thắp cho bà nội nén nhang, xin lỗi vì mười lăm năm không về |
| Tầng giữa | Tìm hiểu vì sao giấy báo tang và cáo phó không có tên mình, trong khi bà nội để lại thư dặn *"đừng về"* |
| Tầng sâu | Cô cần một bằng chứng rằng mình **thuộc về** một dòng họ. Cả đời sống với tờ khai sinh cấp lại không có ngày nhập hộ khẩu gốc. Chính khao khát "được ghi tên" này đẩy cô lên gác xép — và cũng chính nó khiến cô khoác áo lên hình nhân |

**Bí mật (người chơi không biết, hệ thống biết):** cô là **người thế mạng đời thứ tư, lễ chưa thành**; cô đã có **giấy khai tử số 41/KT năm 1976** — về hộ tịch làng, cô chết đã hai mươi năm; bộ áo cưới giấy trên gác được đặt may năm 1976 theo **số đo người lớn**, nghĩa là người ta đã tính trước rằng cô sẽ quay về khi đã trưởng thành.

**Kể qua môi trường:**

| Chi tiết | Ở đâu | Nói điều gì |
|---|---|---|
| **Xe đạp Thống Nhất** dựng gốc cau, chắn bùn buộc túi vải: bánh khảo chợ Dâu, áo bông, **phiếu đo hiệu may** | `area_san_gach` | Toàn bộ "tiểu sử" của cô, kể bằng ba món đồ |
| **Bóng trên sân gạch** dài hơn bình thường một chút; có nhịp nó **đứng yên chậm hơn cô nửa giây** khi cô quay người | `area_san_gach` | `[[ VFX subtle, không âm thanh — 8/10 người chơi không nhận ra lần đầu ]]` |
| **Đôi guốc mộc** đặt xuôi mũi, **vừa khít chân cô**; nhà không có ai đi guốc cỡ ấy | `area_hien_nha` | Thân thể cô khớp với chỗ trống người khác để lại |
| **Vết lõm sờn hình người nhỏ** giữa chiếu cói trước bàn thờ — dấu người quỳ rất nhiều lần, nhưng là một đứa trẻ | `area_gian_tho` | Cô đã từng quỳ ở đây năm bảy tuổi |

### 2.2.2. "BÀ CÔ" / CÔ DÂU GIẤY — Nguyễn Thị Gái

| Trường | Nội dung |
|---|---|
| Tên | **Nguyễn Thị Gái**, con gái út đời thứ ba họ Nguyễn |
| Sinh — mất | 1936 — 1953 (năm Quý Tỵ), mất năm **17 tuổi** |
| Cái chết | Chết đuối dưới **giếng khơi sau nhà**, đêm trước ngày cưới. Áo cưới chưa kịp mặc |
| Danh xưng | Không ai gọi tên. Chỉ gọi **"Bà Cô"** — theo tục thờ bà cô tổ, người con gái chết trẻ chưa có nơi có chốn, không được nhập từ đường, phải lập khám thờ riêng |
| Vị trí thờ | Khám thờ gỗ nhỏ bịt vải điều, đặt **bên trái** bàn thờ họ, thấp hơn bát hương gia tiên một tấc |

**Động cơ:** Bà Cô **không muốn giết người**. Bà Cô **muốn được hoàn tất**. Cô chết ở trạng thái dở dang tuyệt đối: cưới chưa cưới, chôn chưa chôn tử tế, thờ chưa thờ chính thức. Toàn bộ hành vi ma quái của cô trong chương đều là hành vi **đòi cho đủ thủ tục** — đòi đủ đôi đèn, đòi đủ ba hồi chín tiếng mõ, đòi đủ một cái áo.

**Bí mật:**
- Dân làng kể cô **trượt chân**. Nhật ký bà nội ghi cô **tự nhảy** vì bị ép gả cho người cô không muốn lấy — nghĩa là chính cái làng này đã đẩy cô xuống giếng, rồi hai mươi năm sau lại nộp trẻ con cho cô để chuộc lỗi. **Chapter 1 không xác nhận dị bản nào đúng.**
- Cô **không hề đòi trẻ con**. Câu *"Bà Cô đòi người theo hầu"* là **lời phán của bà đồng Tơ năm 1953**. Đây là mũi dao thật của chủ đề: hủ tục là do người sống bịa ra.

**Kể qua môi trường:**

| Chi tiết | Ở đâu |
|---|---|
| **Vệt nước** loang hình bàn chân trần + mùi tanh nhẹ nước giếng lâu ngày | Mọi nơi Bà Cô vừa đi qua; ở gian thờ bắt đầu từ chân khám thờ; ở gác xép **đi ngược lên cầu thang** |
| **Bát hương xoay lệch 45° so với hoành phi**, chân nhang nghiêng cả bó | `area_gian_tho` — theo tục Bắc Bộ, bát hương động là điềm nặng nhất, không cần một chữ thoại nào |
| **Đôi đèn lệch**: một cây cháy, một cây tắt ngóm dù bầu đầy dầu, không có gió | `area_gian_tho` |
| **Vòng hương** cháy dở trên xà, tàn rơi thành xoáy ốc — một vòng chỉ cháy được một ngày một đêm, mà nhà bỏ không mười ngày | `area_gian_tho` |
| **Tiếng guốc mộc** gõ trên gạch đi từ trái sang phải ngoài khung hình rồi dừng — ba lần trong chương, khi người chơi đứng yên quá 12 giây | Toàn chương |
| **Áo cưới giấy** treo sau khung ảnh, vai áo hơi trĩu xuống như vừa có ai mặc thử | `area_gac_xep` |

### 2.2.3. VONG HỒN — BÀ NỘI, Nguyễn Thị Nhỡ (1918 – 25/8/1996)

**Vai trò thiết kế:** vong hồn **đồng minh**. Trong một căn nhà mà mọi thứ đều dẫn người chơi xuống, bà Nhỡ là lực duy nhất đẩy lên — và bà thất bại.

**Động cơ:** giữ cháu khỏi nghi lễ, ngay cả sau khi chết. Biết mình sắp mất thì lễ dở sẽ bị làng khơi lại, mấy tháng cuối bà **cố tình giấu chìa hòm, giấu bài vị vào khám, tháo dùi mõ** — và để lại giấy tờ rải rác như một chuỗi cảnh báo.

**Bí mật:**
- Năm 1976 chính bà bế cháu ra giếng, đọc xong văn khấn, cầm áo cưới giấy lên — rồi **buông tay** khi đứa bé gọi *"bà ơi"*.
- Bà **nói dối cả làng rằng đứa bé chết**, và **để tang cháu ba năm** trong khi cháu vẫn sống ở Hà Nội.
- Bà **không hề gửi giấy báo tang**. Giấy báo tang gửi lên Hà Nội là do **bà đồng Tơ nhờ người viết**.

**Kể qua môi trường:** mảnh khăn xô còn ướt trên dây phơi giữa cái sân khô · nét chữ run nghiêng trái, hay thiếu dấu, dùng chung font viết tay `hw_ba_noi` cho toàn bộ nhật ký / sổ chợ / thư tay · mâm cúng cơm 49 ngày (bát cơm úp, trứng luộc bổ đôi, đôi đũa bông) nhưng **bát cơm đã mốc** còn **mâm ngũ quả tươi mới** — hai người khác nhau bày hai thứ này · ba chữ khắc vụng trong lòng gáo dừa · tiếng **lẩm nhẩm khấn** sau vách buồng, dừng đúng lúc người chơi lại gần.

### 2.2.4. VONG HỒN — "CÁI ĐĨ NHÀI" và "THẰNG CU TÝ"

| | Nhài | Tý |
|---|---|---|
| Tên chữ | Nguyễn Thị Nhài | Nguyễn Văn Tý |
| Tên tục | cái Đĩ | thằng Cu |
| Năm lễ | **Tân Sửu 1961**, 8 tuổi | **Mậu Thân 1968**, 5 tuổi |
| Kết quả | Lễ thành | Lễ thành — guốc còn dưới giếng, không vớt |

**Động cơ:** chúng **không dọa, chúng chỉ đường**. Cả hai đã "xong phần của mình" và không còn gì để mất, nên chúng là thứ duy nhất trong nhà cố gắng cho người chơi biết cái giá. Mỗi lần người chơi sắp bước qua một ngưỡng không thể quay lại, sẽ có một dấu vết trẻ con xuất hiện.

**Bí mật:** chúng **không bị xoá tên** — tên vẫn còn nguyên trong sổ ghi tên. Chỉ lễ của người chơi bị xoá tên, vì lễ của người chơi là **lễ dở**. Người chơi đối chiếu kỹ sẽ bật ra rằng trường hợp của cô là **ngoại lệ**.

**Kể qua môi trường:** vệt tay nhỏ in bùn trên thành chum, cao ngang tầm đứa bé năm tuổi, chỉ hiện khi mặt nước gợn · năm vạch dao trên cột bếp · **guốc trẻ con mắc gờ gạch trong lòng giếng**, chỉ thấy khi soi đèn dầu · tiếng cười trẻ con hai giọng, dưới 0,4 giây, thấp hơn nền 6 dB · hình que vẽ bằng ngón tay trên vách bồ hóng ở độ cao 90 cm: một nhà ba gian, một cái giếng, ba hình người — hai đứng cạnh giếng, **một nằm**.

### 2.2.5. VONG HỒN — ÔNG TỪ NGUYỄN VĂN ĐỐI (trưởng họ, mất 1989)

**Vai trò thiết kế:** vong hồn **thủ tục**. Ông không hiện hình. Ông hiện ra bằng **chữ viết và luật lệ**.

**Động cơ:** lễ phải đúng. Ông không ác — ông chỉ là một ông từ Bắc Bộ tin rằng làm sai một bước thì cả làng gánh hạn. Toàn bộ văn khấn, gia phả, danh sách cấm kỵ, bài vị đều do tay ông.

**Bí mật:** ông là người **đề nghị khắc bài vị khuyết danh** — sáng kiến riêng, lệ cũ không có. Lý lẽ ghi ở lề văn khấn: *"người thế mạng phải là người không tên, có tên thì Bà Cô nhận nhầm."* Chính sáng kiến này đã đẩy việc xoá tên người chơi khỏi gia phả.

**Kể qua môi trường:** mùi mực tàu đọng ở gian thờ, mạnh nhất cạnh cuốn văn khấn · nét chữ nho cứng, sổ thẳng, chân phương (`hw_ong_tu`), đối lập hoàn toàn với nét run nghiêng của bà nội · chõng tre ở hiên có chỗ ngồi lõm hằn, cạnh đó điếu bát và miếng trầu nhai dở đã khô đen · **cuốn văn khấn tự lật sang trang đúng bước tiếp theo** nếu người chơi loay hoay quá 40 giây trong `puz_tuan_tu_le_cung`.

`[[ Văn khấn tự lật trang vừa là hint system vừa là characterization — ông từ đang kèm người chơi làm lễ. ]]`

### 2.2.6. NHÂN VẬT SỐNG — BÀ ĐỒNG TƠ (Nguyễn Thị Tơ, 84 tuổi)

| Trường | Nội dung |
|---|---|
| Nhận dạng | 84 tuổi, lưng còng, răng đen, khăn mỏ quạ, tay luôn cầm một nắm hương vòng |
| Chỗ ở | Nhà tranh đầu làng, cạnh **cây gạo** bên bờ ao |
| Vị thế | Bà đồng cuối cùng của Linh An. Người duy nhất còn nhớ trọn nghi thức thế mạng |

**Động cơ:** đóng lại cái lễ dở dang. Từ 1976 đến 1996, Linh An liên tiếp có người chết trẻ — với bà, đó là bằng chứng không cần bàn cãi rằng **lễ dở còn độc hơn lễ không làm**. Bà không muốn hại người chơi; trong đầu bà, bà đang **cứu cả làng**, và người chơi là món nợ mà bà Nhỡ đã quỵt hai mươi năm.

**Bí mật:**
1. Chính bà **phán năm 1953** rằng Bà Cô đòi người theo hầu. Toàn bộ hủ tục bắt nguồn từ một câu nói của bà lúc 41 tuổi.
2. Bà là người **gửi giấy báo tang lên Hà Nội**, và **khóa trái cổng từ bên trong** rồi ra lối cửa hậu.
3. Bà đã **dọn sẵn cả ngôi nhà thành một đường lễ**: xấp giấy bản và thỏi than đặt đúng tầm tay ở hiên, dùi mõ gác sẵn trên bàn thờ, chai dầu hỏa nút lá chuối để ngay cửa bếp, than hồng ủ trấu cho còn đỏ. Người chơi tưởng mình đang khám phá; thực ra người chơi đang **đi đúng trình tự sáu bước mà bà bày ra**.

> **Ghi chú thiết kế quan trọng:** đây là lý do *game-logic* khiến mọi câu đố đều có đủ đạo cụ ở đúng chỗ. **Convenience của thể loại point-and-click được biến thành nội dung kinh dị: sự tiện lợi chính là bằng chứng có người bày.**

**Kể qua môi trường:** than hồng còn đỏ ủ trấu theo lối nhà quê · mâm ngũ quả mới thay (chuối xanh còn phấn, bưởi chưa héo cuống) cạnh bát cơm cúng đã mốc · nắm hương vòng đặt ngay ngắn ở bậc tam cấp, còn nguyên dây lạt buộc của nhà hàng mã · **vết chân đất bùn cỡ bàn chân người già, đi từ trong nhà ra cửa hậu — không có vết đi vào** · loa phát thanh xã (nguồn âm off-screen, lặp 3 lần trong chương) · **cổng khóa trái từ bên trong** — câu đố mở màn chính là dấu vết đầu tiên của bà.

---

## 2.3. LORE HỦ TỤC "CÚNG THẾ MẠNG" — CANON

> Toàn bộ mục này là **canon**. Mọi câu đố, mọi văn bản đều phải tra về đây. Không được phát sinh biến thể mới ở khâu sản xuất.

### 2.3.1. Nguồn gốc

**Năm Quý Tỵ 1953.** Nguyễn Thị Gái, 17 tuổi, con út ông trưởng họ Nguyễn thôn Linh An, được gả cho con nhà cai tổng bên Đình Bảng. Đêm trước ngày cưới, người ta tìm thấy cô dưới **giếng khơi sau nhà**. Áo cưới còn nguyên trong hòm, chưa mặc lần nào.

Theo lệ Bắc Bộ, con gái chết trẻ, chết chưa có nơi có chốn thì **không được đưa vào từ đường**, không được ghi vào gia phả theo ngôi thứ, chỉ được lập một **khám thờ nhỏ bịt vải điều** đặt bên trái ban thờ họ, gọi chung là **Bà Cô**.

Ba năm sau đó, trong họ liên tiếp có con gái chết yểu và trẻ con ốm dặt dẹo. Làng mời **bà đồng Tơ**. Bà Tơ lên đồng ở sân gạch rồi phán ba câu — về sau được ông từ Đối chép nguyên văn vào đầu cuốn văn khấn:

> **`txt_lore_loi_phan_1953`**
>
> *"Người dưới ấy chưa có áo.*
> *Người dưới ấy đi một mình, lạnh.*
> *Muốn yên thì đưa xuống một người, lấy một thân thế một thân, lấy một tên thế một tên."*

Từ đó thành lệ. Làng gọi tránh là **"lễ thế mệnh"** — dân gian gọi thẳng là **cúng thế mạng**.

### 2.3.2. Bốn luật vận hành của hủ tục

Phải nhất quán tuyệt đối trong mọi văn bản:

| # | Luật | Nội dung | Hệ quả trong game |
|---|---|---|---|
| 1 | **LUẬT TÊN** | Cõi âm nhận người bằng **tên**, không bằng mặt. Muốn nộp ai thì phải **cắt tên người ấy khỏi cõi sống**: xoá khỏi gia phả, khai tử, và từ đó trong nhà **không ai được gọi tên người ấy** nữa. Người thế mạng phải là **người không tên** — nên bài vị của họ **khuyết danh** | `item_bai_vi_khuyet_danh` · trang gia phả bị cạo · dòng than sau bình phong |
| 2 | **LUẬT HÌNH NHÂN** | Vì người thế mạng còn sống, phải có một **thân thay thế**: hình nhân nan tre dán giấy bản, may đúng số đo thật. Hình nhân là **thân**. Áo là **danh phận**. Khoác áo lên hình nhân = **trao thân và danh phận cho Bà Cô** | `hs_hinh_nhan` · `item_ao_cuoi_giay` · sổ chợ ghi số đo |
| 3 | **LUẬT TỰ TAY** | Lễ chỉ **thành** khi cái áo được khoác lên hình nhân. Người khác khoác hộ thì lễ thành nhưng "lỏng", về sau còn gỡ được bằng lễ giải. **Chính người thế mạng tự tay khoác** thì lễ thành **chặt**, không lễ nào giải nổi, vì đó là **tự nguyện** | Chính là hành động kết chương |
| 4 | **LUẬT DỞ DANG** | Lễ bỏ dở giữa chừng thì **nặng hơn không làm**. Tên đã cắt mà thân chưa nộp: người ấy thành **món nợ treo** giữa hai cõi, và cái nợ ấy **đè lên cả làng**, không riêng một nhà | Động lực của toàn chương và của bà Tơ |

### 2.3.3. Trình tự nghi lễ — lớp trong: SÁU BƯỚC TUẦN LỄ CÚNG

Chuẩn cúng Bắc Bộ, dùng chung mọi lễ. **Đây chính là nội dung `puz_tuan_tu_le_cung`.**

| Thứ tự | Bước | Chi tiết |
|---|---|---|
| **Nhất** | Lau bài vị và bày mâm lễ | Lau bài vị bằng khăn sạch nhúng nước mưa; bày mâm ngũ quả, đĩa xôi trắng, gà luộc, chén nước lã |
| **Nhị** | Thắp đôi đèn | Hai cây đèn dầu hai bên. **Phải đủ đôi. Lệch đèn là lệch mạng** |
| **Tam** | Thắp ba nén nhang | Ba nén, cắm thẳng, không cắm chéo |
| **Tứ** | Rót sơ tuần rượu | Rót ba chén, mỗi chén một phần ba |
| **Ngũ** | Đọc văn khấn rồi vái ba vái | Đọc hết bài, không được bỏ đoạn |
| **Lục** | Hóa vàng | Hóa sau cùng. **Hóa trước khi khấn là đại kỵ** |

### 2.3.4. Trình tự nghi lễ — lớp ngoài: BẢY PHẦN CỦA LỄ THẾ MỆNH

Bảng này là **xương sống cài cắm**: mỗi phần lễ tương ứng đúng một câu đố hoặc một nút hành động. **Người chơi tưởng mình giải đố; thực ra người chơi đang hành lễ.**

| Phần | Tên phần lễ | Mục đích tâm linh | Cài vào | Area |
|---|---|---|---|---|
| **I** | **Khóa hướng** — khóa cổng bằng ổ khoá gỗ khắc bát quái theo thế nhà tọa Bắc hướng Nam, thêm quẻ Khôn cho phận nữ | Nhốt hồn trong phạm vi sân, không cho lẫn ra ngõ | `puz_khoa_bat_quai` (ROTATION_LOCK) | `area_san_gach` |
| **II** | **Rập chữ Thế Mệnh** — rập chữ lên giấy bản, dán lên bình phong chắn lối | Dựng "biển báo" cho cõi âm: nhà này có người thế mạng | `puz_rap_chu_the_menh` (PATTERN_TRACE) | `area_hien_nha` |
| **III** | **Trình tổ** — làm trọn tuần lễ cúng sáu bước trước bàn thờ họ, xin tổ tiên cho "đổi sổ" | Xin phép gia tiên gạch một tên khỏi sổ nhà | `puz_tuan_tu_le_cung` (SEQUENCE_ORDER) | `area_gian_tho` |
| **IV** | **Thỉnh Bà Cô** — gõ mõ ba hồi chín tiếng, xen tiếng chuông đúng chỗ | Gọi Bà Cô lên nhận người | `puz_ba_hoi_chin_tieng` (AUDIO_MATCH) | `area_gian_tho` |
| **V** | **Soi đường** — thắp đèn dầu, soi xuống lòng giếng nơi Bà Cô mất | Chỉ mặt người thế mạng cho người dưới ấy nhìn rõ | `puz_thap_lai_den_dau` (ITEM_COMBINE) | `area_bep_gieng` |
| **VI** | **Cắt mặt cắt tên** — khoét mặt khỏi ảnh thờ, cạo tên khỏi gia phả, khắc bài vị khuyết danh | Cắt người ấy khỏi cõi sống | `puz_xep_anh_gia_pha` (SLIDING_TILE) | `area_gac_xep` |
| **VII** | **Khoác áo** — khoác áo cưới giấy lên hình nhân thế mạng | **Giao thân và danh phận. Lễ thành** | Hành động kết chương: `USE_ITEM` `item_ao_cuoi_giay` lên `hs_hinh_nhan` | `area_gac_xep` |

> **Kiểm tra nhất quán:** 7 phần lễ = **6 câu đố + 1 hành động kết**. Không thừa, không thiếu. Mọi câu đố trong SPINE đều có chỗ đứng trong lore, và mọi phần lore đều có chỗ đứng trong gameplay.

### 2.3.5. Vì sao người chơi làm lại được đúng trình tự

Hai lý do, cả hai đều là nội dung chứ không phải tiện lợi thiết kế:

1. **Bà đồng Tơ đã bày sẵn** (mục 2.2.6, bí mật 3).
2. **Người chơi đã từng đi qua đúng trình tự này năm 1976, khi lên bảy.** Ở ba điểm trong chương, khi người chơi **giải đúng câu đố ngay lần đầu**, hệ thống bật một dòng độc thoại rất ngắn:

> **`txt_deja_vu_01`** — "Tay mình biết làm cái này. Mình không nhớ đã học ở đâu."
>
> **`txt_deja_vu_02`** — "Ba hồi, chín tiếng. Đúng chỗ tiếng chuông. Sao mình lại biết chỗ tiếng chuông?"
>
> **`txt_deja_vu_03`** — "Mình đã đứng ở đây rồi. Thấp hơn. Ngang tầm cái chấn song này."

### 2.3.6. BẢY ĐIỀU CẤM KỴ

Văn bản thành phẩm, viết bằng than trên **mặt trong nắp hòm gỗ** ở `area_gac_xep`, nét chữ `hw_ong_tu`.

> **`txt_examine_nap_hom`** *(trang 2 — trang 1 là sơ đồ ngôi thứ, xem mục 3.5.4)*
>
> **NHÀ CÓ NGƯỜI THẾ MỆNH — BẢY ĐIỀU CHỚ PHẠM**
>
> **Một.** Chớ gọi tên thật người thế mệnh trong nhà. Gọi tên là gọi về.
> **Hai.** Chớ soi gương, soi nước sau lúc mặt trời lặn, trong ba ngày lễ.
> **Ba.** Chớ để bát hương xoay, chớ rút chân nhang. Bát hương động là người dưới ấy trở mình.
> **Bốn.** Chớ hóa vàng trước khi khấn. Lễ chưa tới tay mà tiền đã tới tay, người dưới ấy sẽ tự đi mà lấy.
> **Năm.** Chớ thắp một cây đèn. Đèn phải đủ đôi. Lệch đèn là lệch mạng.
> **Sáu.** Chớ để hình nhân quay mặt vào trong nhà. Mặt nó quay vào thì nó tìm người trong nhà.
> **Bảy.** Chớ để chính người thế mệnh tự tay khoác áo cho hình nhân. Áo phải có người khoác hộ. Người thế mệnh tự khoác thì là tự nguyện, mà tự nguyện thì trời không gỡ, đất không gỡ, không ai gỡ được.
>
> *Kính cáo. Nguyễn Văn Đối, trưởng họ, viết năm Kỷ Dậu.*

**Ánh xạ bắt buộc kiểm tra khi implement — mỗi điều phải có chỗ trong cơ chế:**

| Điều | Cài vào cơ chế | Hệ quả trong game |
|---|---|---|
| **Một** — gọi tên | Dòng than sau bình phong (`area_hien_nha`); khi EXAMINE sổ ghi tên ở gác xép, nhân vật **đọc thành tiếng** tên "Nguyễn Thị Liên" | Đúng **6 giây** sau khi đọc tên, hình nhân **xoay 30° về phía người chơi**. Không âm thanh, không flash. Nếu người chơi không quay lại nhìn, nó cứ thế mà đứng |
| **Hai** — soi nước | `scare_bong_trong_chum` kích hoạt đúng khi người chơi soi chum lúc nhập nhoạng | Trả thẳng hậu quả cho việc phạm điều Hai |
| **Ba** — bát hương | Bát hương xoay lệch 45° ngay khi vào `area_gian_tho`; EXAMINE có cảnh báo | `scare_di_anh_quay_mat` khi nhặt `item_dui_mo`: cả bó chân nhang bốc cháy một nhịp |
| **Bốn** — hóa vàng trước khấn | **Chính là bẫy sai của `puz_tuan_tu_le_cung`** | Hóa vàng trước bước Ngũ → nhang tắt ngấm, khói tụ thành hình người, reset câu đố |
| **Năm** — đôi đèn | **Chính là lý do `puz_thap_lai_den_dau` tồn tại** — cây đèn thứ hai đã tắt | Bếp tối om cho tới khi người chơi phục hồi đủ đôi đèn |
| **Sáu** — hình nhân quay mặt | `scare_hinh_nhan_chan_loi` — vào gác thì hình nhân **đã đứng chắn lối, mặt quay vào trong nhà** | Báo rằng điều Sáu đã bị phạm **từ trước khi người chơi tới** |
| **Bảy** — tự tay khoác áo | **Chính là hành động kết chương** | `scare_ao_cuoi_quay_dau` + twist |

### 2.3.7. Vật phẩm nghi lễ — đối chiếu lore ↔ SPINE

| Vật phẩm nghi lễ | `item_id` (SPINE) | Ý nghĩa trong hủ tục | Kiêng kỵ gắn kèm |
|---|---|---|---|
| Ổ khóa gỗ bát quái + **chìa khóa đồng** | `item_chia_khoa_dong` | Chìa của "khóa hướng". Theo lệ, sau lễ chìa phải **thả xuống giếng**, không được giữ trong nhà | Chìa còn trong nhà = lễ chưa xong |
| **Giấy bản và than củi** | `item_giay_ban_va_than` | Giấy dó thô dùng cho vàng mã và rập chữ. Than củi, **không dùng mực — mực là của người sống** | Rập hỏng thì phải **hóa tờ hỏng ngay**, không vứt |
| **Bản rập chữ "Thế Mệnh"** (世命) | `item_ban_rap_chu_the` | Biển báo cõi âm, dán lên bình phong chắn lối vào nhà | Không được gấp làm tư — gấp là "gãy mệnh" |
| **Đèn dầu Hoa Kỳ** | `item_den_dau` / `item_den_dau_sang` | Một trong đôi đèn của bước Nhị. Đèn soi đường cho người dưới giếng nhìn lên | Thắp một cây là **lệch đèn, lệch mạng** |
| **Dải vải điều** | `item_dai_vai_dieu` | Vải đỏ phủ khám thờ Bà Cô. Khi lễ tiến hành thì tuột xuống, nghĩa là **"Bà Cô đã mở mắt"** | Vải điều tuột rồi **không được phủ lại** giữa chừng lễ |
| **Dùi mõ gỗ mít** | `item_dui_mo` | Gỗ mít là gỗ nhà chùa. Dùi là thứ duy nhất "gọi" được Bà Cô | Gõ sai nhịp = gọi nhầm, phải gõ lại từ hồi đầu |
| **Bài vị khuyết danh** | `item_bai_vi_khuyet_danh` | Bài vị của người thế mạng. **Không khắc tên** theo Luật Tên | Khắc tên lên là **trả người về**, hỏng lễ |
| **Chai dầu hỏa nút lá chuối** | `item_chai_dau_hoa` | Dầu thắp cho đủ một đêm lễ | Dầu lễ không được dùng việc khác |
| **Áo cưới giấy khổ người lớn** | `item_ao_cuoi_giay` | **Danh phận.** Cái áo Bà Cô chưa kịp mặc năm 1953, nay may lại cho người thế mạng | **Người thế mạng không được tự tay khoác** |
| **Hình nhân nan tre dán giấy** | *(không phải item — hotspot cố định `hs_hinh_nhan`)* | **Thân thay thế**, cao đúng tầm người thế mạng | Không để hình nhân **quay mặt vào trong nhà** |

Vật phẩm bối cảnh thuộc bộ lễ nhưng không vào hành trang: **chiếu cói** (trải cho hình nhân nằm khi lễ xong) · **mâm ngũ quả** · **hương vòng** (một vòng cháy hết là hết một canh) · **gáo dừa** · **chum nước mưa** (nước lau bài vị) · **gầu tôn** · **guốc mộc** · **que đóm và than hồng**.

### 2.3.8. Niên biểu canon

| Năm | Can chi | Sự kiện |
|---|---|---|
| 1936 | Bính Tý | Nguyễn Thị Gái sinh |
| **1953** | **Quý Tỵ** | Gái chết dưới giếng khơi, **17 tuổi**, đêm trước ngày cưới. Lập khám thờ Bà Cô. Bà đồng Tơ phán ba câu |
| **1961** | **Tân Sửu** | Lễ thế mạng lần 1 — Nguyễn Thị Nhài, tên tục cái Đĩ, 8 tuổi. **Lễ thành** |
| **1968** | **Mậu Thân** | Lễ thế mạng lần 2 — Nguyễn Văn Tý, tên tục thằng Cu, 5 tuổi. **Lễ thành**. Guốc còn dưới giếng |
| 1969 | Kỷ Dậu | Nguyễn Thị Liên (người chơi) sinh 16-9. Cùng năm, ông từ Đối viết bảng Bảy Điều |
| 1972 | Nhâm Tý | Cha người chơi hy sinh |
| 1975 | Ất Mão | Mẹ người chơi mất |
| **1976** | **Bính Thìn** | Lễ thế mạng lần 3 — Nguyễn Thị Liên, 7 tuổi. **LỄ DỞ DANG.** Tên đã xoá, mặt đã khoét, bài vị đã khắc, **áo chưa khoác**. Bà nội gửi cháu lên Hà Nội, khai tử số 41/KT ngày 22-12 |
| 1976–1996 | | Linh An liên tiếp có người chết trẻ. Làng đổ cho lễ dở |
| 1989 | Kỷ Tỵ | Ông từ Đối mất |
| 25-8-1996 | Bính Tý, 12 tháng Bảy | Bà nội Nguyễn Thị Nhỡ mất, thọ **79** |
| **28-8-1996** | **rằm tháng Bảy** | **CHAPTER 1.** Người chơi về tới sân gạch lúc nhập nhoạng, 17 giờ 40 |

---

# 3. KỊCH BẢN TỪNG KHU VỰC (THEO THỨ TỰ CHƠI)

Mỗi khu vực trình bày theo cùng một khung: **không khí → khung hình mở → bảng hotspot → văn bản đọc được → câu đố → jumpscare → mục tiêu → cách khu vực đẩy cốt truyện tiến lên**.

**Luật bố cục bắt buộc áp cho toàn bộ bounds dưới đây:**

| Luật | Giá trị |
|---|---|
| Vùng đặt hotspot hợp lệ | `80 ≤ y` và `y + height ≤ 1000` (chừa notch trên và thanh vật phẩm dưới) |
| Trong khung | `0 ≤ x` và `x + width ≤ 1920` |
| Kích thước chạm tối thiểu | **88 × 88 px @1920** cho mọi hotspot, không ngoại lệ. Sprite nhỏ hơn thì dùng **vùng chạm mở rộng** (đánh dấu 🔹) |
| Khoảng cách tối thiểu giữa hai bounds kề nhau | **20 px** |
| Chồng lấn | **Không hotspot nào chồng lấn hotspot khác trong cùng một area.** Đã kiểm 415 cặp trên toàn chương: **0 cặp giao nhau** |

---

## 3.1. KHU VỰC 1 — `area_san_gach` · "Sân gạch và ngõ vào"

| Trường | Giá trị |
|---|---|
| Thứ tự | **1** |
| Gate vào | **Mở màn chương — không điều kiện.** Người chơi dắt xe đạp từ ngõ tre bước vào sân |
| `background_asset_url` | `https://cdn.linhanthon.game/assets/bg_san_gach.bundle` |
| Thời lượng | 6–8 phút |
| Câu đố | `puz_khoa_bat_quai` |
| Jumpscare | `scare_bong_trong_chum` |

### 3.1.1. Không khí

Chiều rằm tháng Bảy, **17 giờ 40**, trời vừa tạnh mưa rào. Ánh sáng nhập nhoạng màu nước dưa — khoảng thời gian dân quê gọi là "giờ chạng vạng", giờ người và bóng lẫn vào nhau. Sân gạch Bát Tràng còn ẩm, rêu ở mạch gạch xanh đen.

**Mùi:** hương trầm nguội trộn mùi bùn ao và mùi lá chuối cháy dở từ đống tro hóa vàng.

**Âm thanh nền `amb_san_gach_chieu`** (−30 dBFS): nước nhỏ giọt từ tàu cau (chu kỳ 3,2 s **không đều**); ve cuối mùa kêu từng đợt rời rạc; chó sủa vọng từ xóm dưới; **loa phát thanh xã** rè rè ở rất xa, nghe chữ được chữ mất. **Không có nhạc, không có drone trong 45 giây đầu** — cố tình để người chơi tưởng đây là game giải đố nhẹ nhàng.

**Bảng màu:** xám chì, nâu bùn, xanh rêu, và **một điểm trắng duy nhất** — mảnh khăn xô trên dây phơi. Mắt người chơi sẽ tự tìm tới nó.

**Ba lớp dựng cảnh:**

| Lớp | Nội dung |
|---|---|
| BACKGROUND | Bầu trời nhập nhoạng tím-xám, luỹ tre đen thành mảng bẹt, cột loa phát thanh xã, mái ngói nhà ba gian, khói bếp hàng xóm |
| MIDGROUND | Cổng gỗ hai cánh + hai cột gạch câu đối (trái màn hình), gương bát quái treo trên xà cổng, mặt tiền nhà với cửa bức bàn + bậc tam cấp (phải-giữa), cột hiên dán cáo phó, dây phơi căng sang cây cau |
| FOREGROUND | Mặt sân gạch Bát Tràng rêu phủ, xe đạp dựng sát chân tường trái, chum nước mưa góc Bắc, gáo dừa rơi trên sân, chậu hoá vàng còn ấm giữa sân, khe chân tường phải-dưới |
| FX | Bụi chiều bay ngược sáng, muỗi vo ve, vignette xanh lạnh, mưa bụi 10 % opacity |

### 3.1.2. Khung hình mở

Camera tĩnh, góc chính diện phẳng. Người chơi đứng ở mép dưới khung, ngoài tầm nhìn. Trước mặt là **cánh cổng gỗ hai cánh đã khép**, hai bên là hai cột gạch dán đôi câu đối giấy đỏ đã bợt màu. Sau lưng cổng thấp thoáng ba gian nhà ngói ta.

Ba giây đầu, **không có gì chuyển động ngoại trừ mảnh khăn xô đung đưa** — dù cây cau đứng im.

Thao tác đầu tiên hầu như ai cũng làm: bấm vào cổng. Cổng **không mở**. Tiếng then gỗ kêu cạch một tiếng ở phía bên kia.

> **`txt_san_gach_doc_thoai_mo_dau`**
> "Khóa trái. Từ bên trong. Mà nhà thì bỏ không từ hôm đưa tang."

### 3.1.3. Bảng hotspot (13 hotspot)

| # | id | bounds {x, y, w, h} | action_type | Tham số | Vai trò kịch bản |
|---|---|---|---|---|---|
| 1 | `hs_guong_bat_quai` 🔹 | `{x:296, y:150, width:130, height:130}` | `EXAMINE` | `txt_examine_guong_bat_quai` | **Từ điển của câu đố P1** — bảng tra quẻ ↔ số ↔ ngũ hành ↔ tượng người. Sprite thật 96×96 |
| 2 | `hs_loa_phat_thanh` 🔹 | `{x:700, y:120, width:200, height:150}` | `DIALOGUE` | `txt_thoai_loa_phat_thanh` | Neo bối cảnh 1996 + thông tin "nhờ bà con trông hộ cái nhà". Sprite thật 150×84 |
| 3 | `hs_cau_doi_trai` | `{x:88, y:300, width:110, height:420}` | `EXAMINE` | `txt_examine_cau_doi_trai` | **Clue C2 của P1**: lưng nhà = Bắc = nước = Khảm |
| 4 | `hs_o_khoa_cong` | `{x:280, y:430, width:180, height:180}` | `ZOOM_PUZZLE` | `target_puzzle_id: puz_khoa_bat_quai` | **Câu đố mở màn** — ổ khoá gỗ ba vòng đồng tâm |
| 5 | `hs_cau_doi_phai` | `{x:520, y:300, width:110, height:420}` | `EXAMINE` | `txt_examine_cau_doi_phai` | **Clue C3 của P1**: mặt nhà = Nam = lửa = Ly |
| 6 | `hs_cao_pho` | `{x:1000, y:330, width:150, height:210}` | `EXAMINE` | `txt_examine_cao_pho` | **Mũi neo twist A1** — cáo phó không có tên người chơi |
| 7 | `hs_cua_vao_hien` | `{x:1180, y:380, width:300, height:520}` | `CHANGE_AREA` | `target_area_id: area_hien_nha` · gate: có `item_chia_khoa_dong` · `txt_khoa_cua_vao_hien` | Lối đi tiếp |
| 8 | `hs_day_phoi_khan_xo` | `{x:1540, y:230, width:340, height:150}` | `EXAMINE` | `txt_examine_khan_xo` | **Mũi neo twist A2** + **clue C5 của P1** (Bà Cô là phận nữ) |
| 9 | `hs_xe_dap_tui_vai` | `{x:60, y:760, width:240, height:230}` | `EXAMINE` | `txt_examine_xe_dap_tui_vai` | **Phiếu đo hiệu may** — mũi neo inventory-side của twist |
| 10 | `hs_chum_nuoc_mua` | `{x:330, y:730, width:300, height:260}` | `EXAMINE` | `txt_examine_chum_nuoc` | **Clue C4 của P1** (chum kê góc Bắc) + nơi `scare_bong_trong_chum` diễn ra |
| 11 | `hs_gao_dua` 🔹 | `{x:648, y:800, width:130, height:110}` | `EXAMINE` | `txt_examine_gao_dua` | **Cảnh báo duy nhất trước jumpscare.** Sprite thật 86×62 |
| 12 | `hs_dong_tro_hoa_vang` | `{x:820, y:820, width:280, height:170}` | `EXAMINE` | `txt_examine_dong_tro_hoa_vang` | Giấy trắng bị hóa = dấu vết người sống đang rập chữ |
| 13 | `hs_khe_gach_thu_tay` 🔹 | `{x:1560, y:800, width:220, height:120}` | `EXAMINE` | `txt_examine_khe_gach_thu_tay` | **Thư tay bà nội** — đặt ba điều cấm mà chương sẽ phá đủ cả ba. Sprite thật 150×40 |

**Tự kiểm tra bố cục:** 13 hotspot · 78 cặp so sánh · **0 cặp giao nhau** · `y_min = 120` (> 80 ✓) · `y_max(y+h) = 990` (< 1000 ✓) · `x_max(x+w) = 1880` (≤ 1920 ✓) · nhỏ nhất 110×420 ✓ · 3 hotspot dùng vùng chạm mở rộng 🔹. Cụm tương tác chính (cổng + ổ khoá) nằm **trái-giữa**, lối đi tiếp nằm **phải-giữa** — ngón cái trái và phải đều với tới ở chế độ cầm ngang.

### 3.1.4. Văn bản đọc được (thành phẩm)

**① CÁO PHÓ DÁN Ở CỘT CỔNG** — giấy trắng, chữ đánh máy, mực tím, góc dưới bị mưa loang.

> **`txt_examine_cao_pho`**
>
> **CÁO PHÓ**
>
> Gia đình chúng tôi vô cùng thương tiếc báo tin:
> Cụ bà **NGUYỄN THỊ NHỠ**, sinh năm 1918,
> từ trần hồi 4 giờ 20 phút ngày 12 tháng Bảy năm Bính Tý
> (tức ngày 25 tháng 8 năm 1996), hưởng thọ 79 tuổi.
>
> Lễ phát tang: 7 giờ ngày 13 tháng Bảy.
> An táng tại nghĩa trang đồng Sau, thôn Linh An, xã Linh Nam, huyện Thuận Thành, tỉnh Hà Bắc.
>
> **TANG GIA ĐỒNG BÁI TẠ**
> Trưởng nam: Nguyễn Văn Đoan *(đã mất)* — con dâu trưởng: Phạm Thị Vân *(đã mất)*
> Thứ nam: Nguyễn Văn Đoàn
> Trưởng nữ: Nguyễn Thị Đoài
> Các cháu nội, ngoại đồng bái.

> **`txt_san_gach_cao_pho_doc_thoai`**
> "Cháu nội. Cháu ngoại. Đồng bái.
> Không ai viết tên mình ra. Kể cả ở chỗ người ta viết tên tất cả mọi người."

**② ĐÔI CÂU ĐỐI TRÊN HAI CỘT CỔNG** — giấy điều bợt, chữ nho viết tay mực tàu. Tách làm hai hotspot, mỗi cột một vế.

> **`txt_examine_cau_doi_phai`** *(vế phải)*
> 坐北朝南 家門永固
> *Tọa Bắc triều Nam, gia môn vĩnh cố* — "Ngồi hướng Bắc, quay mặt Nam, cửa nhà bền vững."
> *(Bên dưới khắc thêm một dòng nhỏ:)* "Nhà ba gian dựng năm Quý Hợi, tọa Bắc hướng Nam." — và chú thích quốc ngữ khắc bằng mũi dao: *"Hướng Nam — mặt đón lửa trời."*

> **`txt_examine_cau_doi_trai`** *(vế trái)*
> 幼女未歸 香火長存
> *Ấu nữ vị quy, hương hỏa trường tồn* — "Con gái út chưa về nhà chồng, hương khói vẫn còn đây."
> *(Chân cột, nét dao mới hơn hẳn:)* **CHƯA VỀ THÌ CÒN ĐỢI** — và: *"Tọa Bắc — lưng dựa dòng nước."*

> **`txt_san_gach_cau_doi_doc_thoai`**
> "Nhà tọa Bắc hướng Nam. Còn vế bên kia... người ta viết về một cô gái út chưa kịp lấy chồng.
> Trong họ mình có ai như thế à?"

**③ GƯƠNG BÁT QUÁI TREO TRÊN XÀ CỔNG** — clue trung tâm của P1.

> **`txt_examine_guong_bat_quai`**
> "Tấm gương tròn viền gỗ, quanh mép khắc tám quẻ kèm số: Càn một — trời; Đoài hai — đầm; **Ly ba — lửa**; Chấn bốn — sấm; Tốn năm — gió; **Khảm sáu — nước**; Cấn bảy — núi; **Khôn tám — đất, tượng người đàn bà**.
> Mặt gương mờ quá, soi vào chỉ thấy một vệt trắng."

**④ THƯ TAY BÀ NỘI** — giấy kẻ ngang xé từ vở học sinh, gấp tư, nhét sâu trong khe gạch chân tường, chữ run nghiêng trái.

> **`txt_examine_khe_gach_thu_tay`**
>
> Cháu Hương,
>
> Bà viết cái này rồi nhét vào khe tường ngoài cổng, vì bà biết nếu bà gửi bưu điện thì người ta sẽ đọc trước cháu.
>
> Bà biết cháu giận bà. Bà không dám viết dài.
>
> Nếu cháu nhận được thư này thì cháu **đừng về**. Cháu cứ ở ngoài ấy, cứ để bà chết một mình cũng được, bà quen rồi.
>
> Còn nếu cháu đã về đến đây rồi thì cháu nghe bà: vào nhà thì **đừng gọi tên ai, cũng đừng để ai gọi tên cháu**. Trong nhà mình có người nghe thấy.
>
> Cái hòm trên gác thì cháu đừng mở. Bà giữ chìa hai mươi năm nay, bà giấu rồi.
>
> Bà thương cháu.
> *Bà Nhỡ.*

`[[ Thư đặt ba điều cấm: đừng về · đừng gọi tên · đừng mở hòm. Chương 1 sẽ phá cả ba, theo đúng thứ tự ấy. ]]`

**⑤ CHỮ KHẮC TRONG LÒNG GÁO DỪA** — ba chữ khắc vụng bằng đầu dao, nét nông.

> **`txt_examine_gao_dua`**
> "Cái gáo dừa cán tre nằm lăn cách miệng chum một bước chân, như vừa có ai buông tay.
> Trong lòng gáo khắc ba chữ nhỏ, nét dao cùn: **ĐỪNG SOI**."

`[[ Cảnh báo duy nhất trước jumpscare. Người chơi nào đọc gáo trước khi soi chum sẽ được thưởng một khoảnh khắc "biết trước mà vẫn bấm". ]]`

**⑥ MẢNH KHĂN XÔ TRÊN DÂY PHƠI**

> **`txt_examine_khan_xo`**
> "Một mảnh khăn xô cắt dở còn vắt trên dây, ướt sũng dù trời không mưa từ hôm qua. Vải sổ, cắt vội.
> Mặt trong có mấy chữ viết vội bằng bút bi: *'Bà Cô — gái út — mất năm mười bảy tuổi — chưa chồng'*.
> Đám tang bà xong ba hôm rồi. Ai còn để tang? Mà để tang ai?"

**⑦ CHUM NƯỚC MƯA**

> **`txt_examine_chum_nuoc`**
> "Chum sành kê đúng góc Bắc của sân, theo lối các cụ: *nước ở lưng nhà thì phúc không chảy đi*.
> Nước mưa đầy tới miệng, đen và phẳng lì. Cúi xuống soi thử..."

**⑧ XE ĐẠP VÀ TÚI VẢI**

> **`txt_examine_xe_dap_tui_vai`**
> "Chiếc xe đạp của mình, giỏ trước còn cái túi vải: hai phong bánh khảo mua ở chợ Dâu, một chiếc áo bông cũ.
> Và **phiếu đo của hiệu may** — chị Bảy đo cho mình hồi tháng Ba để cắt cái áo dài đi ăn cưới.
> **Dài 1 thước 52. Vòng ngực 82. Dài tay 56.**"

`[[ flag_da_doc_phieu_do = true. Nếu người chơi đã đọc, độc thoại lúc nhặt áo cưới ở Khu 5 đổi thành "Số đo này... mình đã thấy nó rồi." ]]`

**⑨ ĐỐNG TRO HÓA VÀNG**

> **`txt_examine_dong_tro_hoa_vang`**
> "Chậu nhôm móp đựng tro hóa vàng giữa sân. Sờ vào còn âm ấm.
> Trong tro có mấy mẩu giấy chưa cháy hết. Toàn **giấy bản**. Không phải tiền vàng, không phải quần áo — **giấy trắng**.
> Ai lại đi hóa giấy trắng?"

> **`txt_san_gach_dong_tro_hint`** *(chỉ bật khi người chơi rập hỏng lần đầu ở Khu 2 rồi quay lại)*
> "À. Là những tờ rập hỏng. Người ta rập hỏng thì hóa ngay, không vứt."

**⑩ LOA PHÁT THANH XÃ** — nguồn âm off-screen, giọng nam trung niên đọc lè nhè, tín hiệu nhiễu, băng hẹp 300 Hz–3.4 kHz.

> **`txt_thoai_loa_phat_thanh`**
> "...Alô, alô. Đây là đài truyền thanh xã Linh Nam. Mời bà con nghe bản tin chiều...
> Kính báo bà con, hôm nay rằm tháng Bảy, đề nghị các hộ **hóa vàng trước bảy giờ tối**, không đốt rải rác ngoài ngõ, đề phòng hỏa hoạn...
> ...Thôn Linh An báo: hộ cụ Nguyễn Thị Nhỡ đã làm xong lễ tang. Thôn nhờ bà con **trông hộ cái nhà** ít hôm... *(nhiễu)* ...cho đến khi có người về nhận."

### 3.1.5. Câu đố — `puz_khoa_bat_quai`

| Trường | Giá trị |
|---|---|
| Type | `ROTATION_LOCK` · Tên hiển thị: **"Ổ khoá gỗ tám quẻ"** |
| `solution` | **`[6, 3, 8]`** — đọc từ **vòng ngoài vào vòng trong** |
| `reward_item_id` | `item_chia_khoa_dong` |
| `wrong_action_jumpscare` | `scare_bong_trong_chum` |
| Độ khó / thời gian kỳ vọng | **2/5** · 90 giây (P25 = 55 s, P75 = 160 s) |

**Cơ chế:** camera zoom vào ổ khoá gỗ chiếm khung `{x:560, y:140, width:800, height:800}`. **Ba vòng tròn đồng tâm** (ngoài Ø760, giữa Ø520, trong Ø300), **mỗi vòng 8 nấc**, mỗi nấc khắc một quẻ Bát quái kèm **một chữ số Hán (一…八)**. Đặt một ngón lên vòng rồi **kéo theo vòng cung**, snap **45°** mỗi nấc kèm haptic nhẹ + tiếng gỗ "khực". Xác nhận bằng cách **nhấn giữ 0,8 giây vào then gỗ** ở giữa — không có nút "Kiểm tra" riêng, mỗi lần ấn then là một lần thử. Không gian tìm kiếm 8³ = **512**.

**Lời giải và lý do:**

| Vị trí mảng | Vòng | Giá trị | Quẻ | Vì sao |
|---|---|---|---|---|
| 1 | **NGOÀI** | `6` | **Khảm** ☵ | Khảm = nước, phương Bắc. Nhà "**tọa** Bắc" → lưng nhà tựa Bắc → vòng ngoài (lưng, phía sau) ăn về Khảm. Số Tiên Thiên của Khảm là 6 |
| 2 | **GIỮA** | `3` | **Ly** ☲ | Ly = lửa, phương Nam. Nhà "**hướng** Nam" → mặt nhà quay Nam. Số Tiên Thiên của Ly là 3 |
| 3 | **TRONG** | `8` | **Khôn** ☷ | Khôn = đất, quẻ thuần âm, tượng người nữ / người mẹ. Vòng trong cùng = "người ở trong nhà" = **Bà Cô**, phận gái út chết trẻ. Số Tiên Thiên của Khôn là 8 |

**Bảng ánh xạ ID phần tử** *(khắc ngay trên mặt ổ khoá, người chơi đọc được trong game)*: `1 = Càn ☰ trời` · `2 = Đoài ☱ đầm` · `3 = Ly ☲ lửa` · `4 = Chấn ☳ sấm` · `5 = Tốn ☴ gió` · `6 = Khảm ☵ nước` · `7 = Cấn ☶ núi` · `8 = Khôn ☷ đất`.

**Sáu manh mối, tất cả nằm trong cùng khu vực, đều `EXAMINE` không cần vật phẩm:**

| # | Clue | Hotspot | Suy ra |
|---|---|---|---|
| C1 | Gương bát quái | `hs_guong_bat_quai` | **Từ điển**: quẻ ↔ số ↔ ngũ hành ↔ tượng người |
| C2 | Câu đối vế trái | `hs_cau_doi_trai` | Lưng nhà = Bắc = nước = Khảm → vòng ngoài |
| C3 | Câu đối vế phải | `hs_cau_doi_phai` | Mặt nhà = Nam = lửa = Ly → vòng giữa |
| C4 | Chum nước góc Bắc | `hs_chum_nuoc_mua` | Xác nhận chéo C2 |
| C5 | Mảnh khăn xô | `hs_day_phoi_khan_xo` | Bà Cô là phận nữ → quẻ thuần âm = Khôn → vòng trong |
| C6 | Trục then ổ khoá khắc ba chữ chìm **"Tọa — Hướng — Người"** | `hs_o_khoa_cong` (trong khung zoom) | **Thứ tự đọc mảng**: ngoài = tọa, giữa = hướng, trong = người trong nhà |

> **Tự kiểm tra công bằng:** chuỗi suy luận khép kín — C6 cho ý nghĩa 3 vòng → C2/C3/C4 cho hướng và ngũ hành → C5 cho giới tính Bà Cô → C1 dịch ngược ra ba con số 6/3/8. **Không cần kiến thức phong thuỷ ngoài đời.**

**Hành vi khi sai:**

| Lần sai | Phản hồi |
|---|---|
| 1 | Ba vòng **tự trả về vị trí cũ** theo chiều ngược, kèm **tiếng gỗ nghiến** 1,2 s (`fol_cua_go_nghien`). Then không nhúc nhích |
| 2 | Như trên, cộng: **gáo dừa trên miệng chum khẽ xoay một vòng** ở hậu cảnh (`fol_gao_dua_lach_cach`, rất nhỏ, camera không cắt) — gợi ý môi trường đẩy người chơi đi soi chum |
| 3 | **JUMPSCARE `scare_bong_trong_chum`**, sau đó `fail_count` reset về 0, ba vòng **giữ nguyên vị trí người chơi vừa đặt** (không phạt thêm) |

**Ba mức gợi ý** (nút "Thắp nhang xin keo", `{x:1700, y:930, width:150, height:110}`):

| Tier | Mở sau | Nội dung |
|---|---|---|
| 1 | 60 s / 1 lần sai | *"Ổ khoá này không hỏi bạn là ai. Nó hỏi ngôi nhà này nằm thế nào, quay mặt về đâu, và ai là người còn ở lại trong đó. Trục then giữa ổ khoá có khắc ba chữ — hãy đọc chúng trước khi xoay bất cứ vòng nào."* |
| 2 | 150 s / 2 lần sai | *"Đôi câu đối ngoài cổng nói nhà tọa Bắc hướng Nam: lưng tựa nước, mặt đón lửa. Tấm gương bát quái trên cổng đã ghi sẵn quẻ nào là nước, quẻ nào là lửa, và quẻ nào là đất — tượng người đàn bà. Bà Cô, theo mảnh khăn xô ngoài dây phơi, là phận gái út. Ba vòng, theo thứ tự ngoài vào trong: nước, lửa, đất."* |
| 3 | 300 s / 4 lần sai — **đáp án trực tiếp** | *"Xoay vòng ngoài về quẻ Khảm — số sáu. Xoay vòng giữa về quẻ Ly — số ba. Xoay vòng trong về quẻ Khôn — số tám. Tức là dãy **6 – 3 – 8**, đọc từ vòng ngoài vào vòng trong. Rồi ấn giữ then gỗ ở giữa."* |

`[[ Tier 1 & 2 miễn phí. Tier 3 gắn LiveOps nhưng LUÔN có đường mở miễn phí bằng thời gian chờ 300 s — không được phép biến thành tường trả phí. ]]`

### 3.1.6. Jumpscare — `scare_bong_trong_chum`

| Trường | Giá trị |
|---|---|
| `trigger_type` | `ON_PUZZLE_FAIL_COUNT` · `max_fails: 3` trên `puz_khoa_bat_quai` |
| Loại | **Impulse scare** · `screen_flash: true` · envelope **1200 ms** |
| `audio_asset` | `sfx_scare_gao_dua_roi.ogg` · `sprite_animation`: `anim_bong_khan_xo_trong_chum` |
| Delay | 1400 ms sau khi ba vòng trả về vị trí cũ |

**Mô tả (SPINE):** người chơi cúi soi vào chum nước mưa; mặt nước phản chiếu **một người đội khăn xô đứng ngay sau lưng**, rồi cái gáo dừa rơi đánh "cạch" làm mặt nước vỡ tan — quay lại thì sân vắng.

**Diễn biến theo khung hình:**

| Mốc | Sprite | Camera | Ánh sáng | Âm thanh | Haptic |
|---|---|---|---|---|---|
| **−6000 ms** | Mặt nước bắt đầu **gợn rất nhẹ** (1,1 Hz, biên độ 3 px) dù không có gió | Tĩnh | — | `tell_nuoc_gon_trong_chum.ogg` fade-in tới −34 dBFS, pan 0.4 trái | — |
| **−2000 → −1 ms** | Gợn nước **dừng phẳng lì** | Tĩnh | — | **IM LẶNG TUYỆT ĐỐI.** Mọi bus về −∞, kể cả ve, kể cả chó sủa | — |
| **0 ms** | `spr_bong_khan_xo` fade-in **trong mặt nước** (alpha 0 → 0.85 trong 60 ms). **Không có thực thể nào trên sân** | Punch-in **+6 %** trong 80 ms, tâm = tâm chum `(380, 750)` | — | Transient `sfx_scare_gao_dua_roi`, đỉnh **−5 dBTP** | `hap_thump_single` 40 ms, 0.80 |
| **80 ms** | Bóng người **đứng yên**, không lại gần. Gáo dừa rơi khỏi miệng chum | Punch đỉnh, shake **8 px** ngang, 9 Hz | **FLASH** `#FFF2DC`, alpha 0 → **0.30** trong 40 ms, một xung, toàn màn | Đỉnh stinger; dải 2–5 kHz giới hạn ≤ −10 dBFS | — |
| **200 ms** | Gáo chạm nước → **mặt nước vỡ tan**, `spr_nuoc_vo` che hoàn toàn bóng (**mask cut**) | Shake còn 4 px | Alpha 0.30 → 0.06 | `fol_gao_dua_lach_cach` chồng lên, −18 dBFS | `hap_tap_light` 12 ms, 0.30 |
| **600 ms** | Sóng lăn tăn, **bóng đã biến mất hoàn toàn**. Gáo dừa nổi, xoay chậm | Về 100 %, hết shake | Alpha 0 | Đuôi vang nước | — |
| **1200 ms** | **Envelope kết thúc.** Mặt nước phẳng lại. Sân sau lưng: trống | Tĩnh | — | Recovery: `amb_san_gach_chieu` từ −45 dBFS bò lên −30 trong 20 s | — |

> **Ghi chú đạo diễn:** bóng người **không bao giờ chuyển động về phía camera**. Nó chỉ đứng. Cảm giác giật đến từ **gáo dừa** (âm thanh + flash); cảm giác lạnh ở lại đến từ việc **có người đứng sau lưng suốt lúc đó mà ta không biết**. Đây là mô hình dùng chung cho cả tám cú dọa: **giật bằng vật vô tri, lạnh bằng sự hiện diện.**

**Vì sao đặt ở đây:** (a) đây là cú dọa **duy nhất của khu hướng dẫn** và nó gắn với **thất bại** — người chơi giỏi sẽ không bao giờ thấy nó; cú dọa mở màn không được là thuế bắt buộc. (b) Cú dọa **chỉ thẳng vào cái chum** — vốn là clue C4 của chính câu đố người chơi đang bí; nó **trả lại thông tin**, không chỉ lấy đi nhịp tim. (c) Đặt ở phút 3–5 để **thiết lập ngôn ngữ**: game này dọa bằng đồ vật đời thường, không bằng quái vật.

### 3.1.7. Mục tiêu người chơi

| Cấp | Mục tiêu |
|---|---|
| Bề mặt | Vào được trong nhà để thắp hương cho bà |
| Cơ học | Giải `puz_khoa_bat_quai` → nhận `item_chia_khoa_dong` → `CHANGE_AREA` qua `hs_cua_vao_hien` sang `area_hien_nha` |
| Cảm xúc (ngầm) | Xác nhận một nghi ngờ: *"cái nhà này không muốn mình vào, hay không muốn mình đi?"* |

**Dạy cơ chế:** đây là khu dạy học. Hotspot phát sáng nhẹ (outline 2 px, alpha 30 %) trong 20 giây đầu rồi tắt hẳn. `puz_khoa_bat_quai` là câu đố duy nhất có nút GỢI Ý hiện ngay sau 60 giây bế tắc.

### 3.1.8. Khu vực này đẩy cốt truyện tiến lên thế nào

1. **Đặt câu hỏi trung tâm bằng một tờ giấy công khai.** Cáo phó là tài liệu hành chính, dán nơi ai cũng đọc được — và nó không có tên người chơi. Cách rẻ nhất, sạch nhất để cắm câu hỏi *"tại sao tên tôi bị xóa"* ngay phút thứ hai.
2. **Thiết lập rằng có người sống.** Cổng khóa trái, khăn xô ướt, tro còn ấm, giấy trắng bị hóa — bốn dấu vết độc lập cùng chỉ về một kết luận. Người chơi kết luận sai (nghĩ là ma); kết luận đúng chỉ lộ ở cảnh kết và Chapter 2.
3. **Dạy luật chơi cũng là dạy luật lễ.** Câu đố mở màn không phải "mở khóa", mà là **khóa hướng** — phần lễ thứ nhất. Người chơi vừa vô tình làm bước một của chính nghi lễ dành cho mình.
4. **Cấp cho người chơi lời dặn sẽ bị phá vỡ.** Thư bà nội đặt ba điều cấm: đừng về, đừng gọi tên, đừng mở hòm. Chương 1 phá cả ba, đúng thứ tự ấy.

---

## 3.2. KHU VỰC 2 — `area_hien_nha` · "Hiên nhà và bức bình phong"

| Trường | Giá trị |
|---|---|
| Thứ tự | **2** |
| Gate vào | **Có `item_chia_khoa_dong`** (phần thưởng P1) — dùng mở ổ khóa cửa bức bàn |
| `background_asset_url` | `https://cdn.linhanthon.game/assets/bg_hien_nha.bundle` |
| Thời lượng | 8–10 phút |
| Câu đố | `puz_rap_chu_the_menh` |
| Jumpscare | `scare_ban_tay_giay_sau_manh` — **bắn khi GIẢI ĐÚNG**, không phải khi sai |

### 3.2.1. Không khí

**18 giờ 10.** Trời sập hẳn. Ánh sáng duy nhất là thứ sáng xanh lạnh còn sót của hoàng hôn hắt qua sân. Hiên gạch khô, bậc tam cấp ba bậc. Gió lùa dọc hiên làm **mành nứa** đập vào khung cửa theo **nhịp không đều** (`fol_manh_nua_dap`, ngẫu nhiên 2,1–4,8 s) — âm thanh đặc trưng của khu vực này, và là tiền đề cho jumpscare.

**Mùi:** mốc chiếu cói, dầu hỏa, và mùi giấy bản mới (mùi giấy dó — hơi ngai ngái, hơi ngọt).

**Tông chuyển:** Khu 1 là "ngoài", Khu 2 là "ngưỡng". Không gian hẹp lại, trần thấp xuống, camera đẩy gần hơn 15 %. Người chơi bắt đầu thấy tù túng mà chưa biết vì sao.

| Lớp | Nội dung |
|---|---|
| BACKGROUND | Vách gỗ ba gian tối màu, hoành phi nhỏ đã mờ hẳn, khe cửa hắt ra một vệt sáng vàng cam yếu |
| MIDGROUND | Bức bình phong gỗ chính giữa (ngôi sao của khu vực), ô lõm hình chữ nhật trên khung bên phải, cột hiên treo đèn dầu Hoa Kỳ, cánh cửa bức bàn khép (phải) |
| FOREGROUND | Mành nứa sát mép trên khung hình, chõng tre + điếu bát (trái), bậc tam cấp mép trái, đôi guốc mộc và xấp giấy bản trên nền gạch hiên |
| FX | Khói hương loãng bay ngang, mành nứa đung đưa **lệch pha với gió**, quầng sáng đèn dầu chưa thắp = xám |

### 3.2.2. Khung hình mở

**Bức bình phong gỗ** chắn gần trọn lối vào gian giữa — cao quá đầu người, mặt gỗ mít lên nước đen bóng, trên đó **hai chữ Hán đã bị bào mờ gần hết**, chỉ còn vệt lõm rất nông. Rìa phải bình phong có một **ô lõm hình chữ nhật** khoét sẵn, kích thước đúng một tờ giấy bản.

Ngay dưới chân bình phong, trên bậc tam cấp: **một xấp giấy bản và một thỏi than củi** đặt ngay ngắn, như ai vừa đặt xuống rồi đi.

Bên trái: **chõng tre** trải nửa chiếc chiếu cói cuộn dở, trên chõng có điếu bát và miếng trầu nhai dở đã khô đen; dưới chiếu ló ra một mép giấy. Bên phải, trên cột hiên, treo **đèn dầu Hoa Kỳ** vỏ ám khói dày, bầu đèn cạn khô. Dưới bậc, **đôi guốc mộc** đặt xuôi mũi.

### 3.2.3. Bảng hotspot (11 hotspot)

| # | id | bounds {x, y, w, h} | action_type | Tham số | Vai trò kịch bản |
|---|---|---|---|---|---|
| 1 | `hs_manh_nua` | `{x:360, y:96, width:1000, height:130}` | `EXAMINE` | `txt_examine_manh_nua` | **Clue C2 của P2** (bố cục hai chữ) + tiền đề `scare_ban_tay_giay_sau_manh` |
| 2 | `hs_den_dau_treo` | `{x:1500, y:180, width:160, height:250}` | `COLLECT_ITEM` | `item_id: item_den_dau` · `required_item: null` | **Clue C3 của P5** — danh sách ba thứ còn thiếu, dựng mục tiêu từ khu vực 2 |
| 3 | `hs_binh_phong` | `{x:640, y:300, width:420, height:560}` | `ZOOM_PUZZLE` | `target_puzzle_id: puz_rap_chu_the_menh` · fallback `txt_khoa_binh_phong_thieu_giay` | **Câu đố chính của khu vực** |
| 4 | `hs_o_lom_binh_phong` | `{x:1080, y:470, width:130, height:180}` | `USE_ITEM` | `required_item: item_ban_rap_chu_the` · `item_id: item_ban_rap_chu_the` | Tra bản rập → then gian giữa nhả ra |
| 5 | `hs_cua_buc_ban` | `{x:1420, y:470, width:280, height:450}` | `CHANGE_AREA` | `target_area_id: area_gian_tho` · gate: `flag_binh_phong_da_tra` · `txt_khoa_cua_buc_ban` | Lối đi tiếp |
| 6 | `hs_vo_tap_viet` | `{x:170, y:430, width:220, height:140}` | `EXAMINE` | `txt_examine_vo_tap_viet` | **Clue C1 của P2** — toàn bộ bốn phép viết chữ + ba chữ mẫu đã giải sẵn |
| 7 | `hs_xuong_san_gach` | `{x:30, y:600, width:120, height:270}` | `CHANGE_AREA` | `target_area_id: area_san_gach` · **không gate** | Đường lùi, luôn mở |
| 8 | `hs_chong_tre` | `{x:170, y:600, width:390, height:270}` | `EXAMINE` | `txt_examine_chong_tre` | Dấu vết ông từ + dấu vết người sống mới rót chè |
| 9 | `hs_nhat_ky_duoi_chieu` | `{x:160, y:890, width:280, height:105}` | `EXAMINE` | `txt_examine_nhat_ky_1976` | **Lần đầu người chơi nghe một người trong nhà thú nhận** |
| 10 | `hs_guoc_moc` | `{x:640, y:890, width:240, height:105}` | `EXAMINE` | `txt_examine_guoc_moc` | **Mô-típ "vừa chân"** — thân thể người chơi khớp chỗ trống người khác |
| 11 | `hs_giay_ban_va_than` | `{x:940, y:890, width:200, height:105}` | `COLLECT_ITEM` | `item_id: item_giay_ban_va_than` · `required_item: null` | **Điều kiện mở khoá P2** |

**Tự kiểm tra bố cục:** 11 hotspot · 55 cặp · **0 giao nhau** · `y_min = 96` ✓ · `y_max = 995` ✓ · nhỏ nhất cao 105 px ✓. Cặp sát nhau nhất: `hs_binh_phong` (kết thúc x = 1060) và `hs_o_lom_binh_phong` (bắt đầu x = 1080) — **cách đúng 20 px**, **cố ý tách rời** vì một cái là `ZOOM_PUZZLE`, một cái là `USE_ITEM`; nếu chồng nhau người chơi sẽ tra bản rập nhầm vào ô chữ.

### 3.2.4. Văn bản đọc được (thành phẩm)

**① TRANG NHẬT KÝ BÀ NỘI, KẸP DƯỚI CHIẾU CÓI** — giấy vở ô ly, mực tím đã nhòe, chữ run.

> **`txt_examine_nhat_ky_1976`**
>
> *Ngày mồng bảy tháng Chạp năm Bính Thìn.*
>
> Ông từ bảo phải rập chữ dán lên bình phong, chặn lối ngõ, để **nó** có chạy thì cũng chỉ chạy vòng quanh sân chứ không ra được đến cây gạo.
>
> Ông bảo rập phải rập bằng than, không được dùng mực. **Mực là của người sống.**
>
> Tôi rập ba lần hỏng cả ba. Tay tôi run. Hỏng tờ nào phải hóa ngay tờ ấy, không được vứt, ông từ dặn thế.
>
> Con bé ngồi ở chõng ăn khoai lang. Nó hỏi: *bà ơi sao nhà mình dán giấy kín thế.*
>
> Tôi bảo: *nhà mình sắp có đám cưới.*
>
> Nó cười. Nó bảo *thế cháu được ăn cỗ à bà.*

`[[ "Con bé ngồi ở chõng ăn khoai lang" — người chơi đọc như một chi tiết vặt. Ở area_gac_xep, con bé ấy hóa ra là chính cô. ]]`

**② DÒNG CHỮ THAN Ở MẶT SAU BÌNH PHONG** — chỉ thấy khi ZOOM vào bình phong ở góc nghiêng, nét than to, viết vội.

> **`txt_hien_nha_chu_than_sau_binh_phong`**
> **GỌI TÊN LÀ GỌI VỀ.**
> **TRONG NHÀ NÀY KHÔNG AI CÓ TÊN.**

**③ NHÃN DÁN TRÊN XẤP GIẤY BẢN** — nhãn giấy nhỏ của nhà hàng mã, chữ viết tay. Hiện khi nhặt `item_giay_ban_va_than`.

> **`txt_hien_nha_nhan_giay_ban`**
> *Hàng mã bà Xuyến — chợ Dâu*
> Giấy bản loại một, 3 xấp.
> Ghi sổ, chưa lấy tiền.
> **Người đặt: bà Tơ.**
> *(Dưới cùng, nét chữ khác, nhỏ hơn:)* Cụ dặn để ở bậc hiên, đừng mang vào trong nhà.

`[[ Đây là lần đầu tên "bà Tơ" xuất hiện trong game. Người chơi chưa biết bà Tơ là ai. Tên này xuất hiện lại đúng hai lần nữa: nhật ký 1996 trên gác xép, và câu thoại cuối chương. Ba lần — đủ để thành một cái tên, chưa đủ để thành một con người. Con người ấy để dành cho Chapter 2. ]]`

**④ VỞ TẬP VIẾT CHỮ NHO CỦA TRẺ CON** — clue trung tâm của P2.

> **`txt_examine_vo_tap_viet`**
> "Cuốn vở tập viết chữ Nho của một đứa trẻ. Trang đầu chép tay:
> *'**Bốn phép viết chữ.** Một — ngang trước, sổ sau. Hai — trái trước, phải sau. Ba — trên trước, dưới sau. Bốn — nét phẩy, nét mác viết sau cùng (phép này trùm lên ba phép trên).'*
> Bên cạnh có ba chữ mẫu đánh số từng nét: **三** (①②③ ba nét ngang từ trên xuống) · **川** (①②③ ba nét sổ từ trái sang) · **大** (① ngang, ② phẩy, ③ mác)."

**⑤ ĐÔI GUỐC MỘC**

> **`txt_examine_guoc_moc`**
> "Guốc mộc, quai da đã sờn, đế mòn lệch về bên trái. Dưới đế còn dính vụn than đen.
> Người ta đặt xuôi mũi — theo lệ, guốc dép của người vừa mất thì quay mũi ra ngoài, để người ấy còn biết đường mà đi.
> Mình ướm thử. **Vừa khít chân mình.**
> Bà thì chân nhỏ hơn thế nhiều."

**⑥ CHÕNG TRE**

> **`txt_examine_chong_tre`**
> "Chõng tre bóng mồ hôi tay. Điếu bát còn nước, đóm gãy vứt bên cạnh. Một miếng trầu nhai dở, khô đen lại. Và một chén nước chè nguội **mới rót nửa chừng**.
> Chỗ ngồi hằn lõm xuống một vệt — kiểu vệt của người ngồi đúng một chỗ suốt mấy chục năm.
> Ông nội mình mất trước khi mình sinh ra. Vậy ai ngồi?"

**⑦ MÀNH NỨA**

> **`txt_examine_manh_nua`**
> "Mành nứa cũ, dây gai mục, ám khói đen. Bụi bám thành hai vệt sáng in đúng khuôn hai chữ vuông trên bức bình phong phía dưới — chữ trên nhỏ hơn chữ dưới.
> Nó đập vào khung cửa. Đập, ngừng, đập hai cái, ngừng.
> Gió thì thổi đều. Cái này thì không đều."

**⑧ BÌNH PHONG KHI CHƯA CÓ GIẤY** — fallback của `ZOOM_PUZZLE`.

> **`txt_khoa_binh_phong_thieu_giay`**
> "Hai chữ Hán bị bào gần phẳng. Ngón tay lần theo thì vẫn thấy rãnh chìm — phải có giấy bản và một thỏi than mới ăn được nét."

**⑨ ĐỘC THOẠI KHI CHỮ HIỆN RA** — kết thúc `puz_rap_chu_the_menh`, ngay trước `scare_ban_tay_giay_sau_manh`.

> **`txt_hien_nha_doc_thoai_the_menh`**
> "Hai chữ.
> 世 — Thế. 命 — Mệnh.
> **Thế Mệnh.** Thay mạng.
> Ai thay mạng cho ai, trong cái nhà này?"

### 3.2.5. Câu đố — `puz_rap_chu_the_menh`

| Trường | Giá trị |
|---|---|
| Type | `PATTERN_TRACE` · Tên hiển thị: **"Rập chữ trên bình phong"** |
| `solution` | **`[2, 1, 4, 3, 7, 5, 8, 6]`** |
| `reward_item_id` | `item_ban_rap_chu_the` |
| `wrong_action_jumpscare` | **`null`** — jumpscare của khu vực bắn khi **giải đúng** |
| Độ khó / thời gian kỳ vọng | **3/5** · 150 giây (P25 = 95 s, P75 = 240 s) |
| Điều kiện mở khoá | **Bắt buộc có `item_giay_ban_va_than`** (nhặt tự do tại `hs_giay_ban_va_than`, cùng khu vực) |

**Cơ chế:** zoom vào mặt bình phong, cutscene 2 s phủ tờ giấy bản lên gỗ, thỏi than nằm sẵn ở mép dưới. Khung rập chia **hai ô dọc**: ô trên = chữ **Thế 世**, ô dưới = chữ **Mệnh 命**, mỗi chữ vẽ theo **lối chân giản lược 4 nét**. Trên giấy chỉ hiện **8 vệt mờ** (bóng nét gỗ hằn qua giấy). Người chơi **đặt ngón lên đầu một nét và miết dọc theo nét đó**; miết đủ **85 %** chiều dài thì nét "ăn than", hiện đen đậm.

**Hướng miết có tính điểm:** nét ngang miết **trái → phải**, nét sổ miết **trên → xuống**, nét mái miết **từ phía phẩy (trái) sang phía mác (phải)**. Miết ngược chiều = sai. Không có nút xác nhận — nét thứ 8 đúng là tự hoàn tất. Có **nút "Bóc tờ giấy"** để tự nguyện làm lại (không tính là lần sai).

`[[ Ràng buộc mỹ thuật bắt buộc: mỗi nét phải rộng tối thiểu 44 px để vừa đầu ngón tay. ]]`

**Bảng ánh xạ ID phần tử** *(cố định theo atlas sprite, KHÔNG theo thứ tự viết — cố ý, để chống brute-force bấm trái→phải)*:

| ID | Nét | Thuộc chữ | Vị trí |
|---|---|---|---|
| 1 | Nét **sổ trái** | Thế 世 | ô trên, cột trái |
| 2 | Nét **ngang dài trên cùng** | Thế 世 | ô trên, vắt ngang |
| 3 | Nét **sổ-gập phải** (sổ rồi gập ngang tạo đáy chữ) | Thế 世 | ô trên, cột phải + đáy |
| 4 | Nét **sổ giữa** | Thế 世 | ô trên, cột giữa |
| 5 | **Bộ Khẩu 口** (nét gập vuông) | Mệnh 命 | ô dưới, trái |
| 6 | **Nét mái 人** (phẩy + mác gộp thành mái nhà) | Mệnh 命 | ô dưới, trên cùng |
| 7 | Nét **ngang** dưới mái | Mệnh 命 | ô dưới, giữa |
| 8 | **Bộ Tiết 卩** (sổ móc) | Mệnh 命 | ô dưới, phải |

**Giải thích từng phần tử của mảng:**

| Thứ tự miết | Giá trị | Nét | Vì sao đứng ở đây |
|---|---|---|---|
| 1 | `2` | Ngang dài của Thế | Phép 1 — **ngang trước sổ sau**; và phép 3 — nó ở trên cùng |
| 2 | `1` | Sổ trái của Thế | Hết ngang thì tới sổ. Ba nét sổ, phép 2 — **trái trước phải sau** |
| 3 | `4` | Sổ giữa của Thế | Nét sổ thứ hai tính từ trái |
| 4 | `3` | Sổ-gập phải của Thế | Nét sổ ngoài cùng bên phải; phần gập tạo đáy chữ nên cũng thoả phép 3 |
| 5 | `7` | Ngang của Mệnh | Phép 3 — **trên trước dưới sau**, xong chữ Thế mới tới Mệnh. Trong chữ Mệnh: phép 1 — ngang đi đầu |
| 6 | `5` | Bộ Khẩu 口 | Phép 2 — **trái trước phải sau** |
| 7 | `8` | Bộ Tiết 卩 | Bên phải, viết sau Khẩu |
| 8 | `6` | Nét mái 人 | Phép 4 — **phẩy và mác viết sau cùng**. Phép 4 là phép trùm, thắng cả phép 3 |

> **Ghi chú khảo cứu (minh bạch cho Lead & QA):** bút thuận thật ngoài đời của chữ 命 bắt đầu bằng phẩy-mác, không kết thúc bằng chúng. Bản game **theo đúng bốn phép ghi trong SPINE**, và bốn phép đó được **chép nguyên văn vào tờ vở tập viết trong game (clue C1)**, có ví dụ minh hoạ. Vì mọi quy tắc cần thiết đều nằm trong game và nhất quán với nhau, suy luận vẫn **công bằng và khép kín**; người chơi không bị phạt vì biết hay không biết Hán tự ngoài đời.

**Manh mối:**

| # | Clue | Hotspot | Suy ra |
|---|---|---|---|
| C1 | Vở tập viết chữ Nho | `hs_vo_tap_viet` | **Toàn bộ bộ luật + ba ví dụ đã giải sẵn** (三 / 川 / 大) |
| C2 | Mành nứa ám khói | `hs_manh_nua` | Xác nhận bố cục hai chữ, chữ trên viết trước |
| C3 | Đôi guốc mộc dính vụn than | `hs_guoc_moc` | Nhắc rằng **thỏi than là thứ dùng ở đây** |
| C4 | Bình phong khi chưa có giấy | `hs_binh_phong` (fallback) | Dạy **điều kiện mở khoá** |

**Hành vi khi sai** (sai = miết nhầm nét, hoặc miết đúng nét nhưng ngược chiều):

| Lần sai | Phản hồi |
|---|---|
| 1 | Nét vừa miết **lem nhoè thành vệt than bẩn**, cả tờ giấy **tự cuốn lên và rơi xuống**, rút tờ kế tiếp, làm lại từ nét 1. Bộ đếm hiển thị *"Còn 2 tờ"* |
| 2 | Như trên, *"Còn 1 tờ"*. Đồng thời **mành nứa khẽ đung đưa** dù không có gió |
| 3 | Hết tờ thứ 3 → **`item_giay_ban_va_than` KHÔNG bị mất**: độc thoại *"Vẫn còn cả xấp. Bình tĩnh."* và xấp giấy **được nạp lại đầy 3 tờ**. Đồng thời **tự động mở Hint Tier 1 miễn phí** |

> **Ràng buộc chống soft-lock:** tuyệt đối **không tiêu huỷ vĩnh viễn** vật phẩm bắt buộc. Xấp giấy là tài nguyên **giả hữu hạn** — nó tự nạp lại, và tiếng giấy sột soạt ở sau lưng lúc nạp lại là một cách dọa im lặng, không phải jumpscare.

**Ba mức gợi ý:**

| Tier | Nội dung |
|---|---|
| 1 | *"Đừng vẽ theo cái mình thấy, hãy vẽ theo cái người ta dạy. Trên đôn gỗ có cuốn vở tập viết chữ Nho của một đứa trẻ — trang đầu chép đủ bốn phép viết chữ, lại có ba chữ mẫu đánh số sẵn từng nét."* |
| 2 | *"Bốn phép: ngang trước sổ sau; trái trước phải sau; trên trước dưới sau; và phẩy-mác thì luôn để sau cùng, phép này trùm lên ba phép kia. Rập chữ trên (Thế) trọn vẹn rồi mới xuống chữ dưới (Mệnh). Chữ Thế: một nét ngang rồi ba nét sổ từ trái sang phải. Chữ Mệnh: nét ngang trước, rồi bộ bên trái, rồi bộ bên phải, và cái mái nhà ở trên đầu — vì nó là phẩy với mác — miết sau rốt."* |
| 3 — **đáp án** | *"Miết tám nét theo thứ tự: (1) ngang dài chữ trên, trái sang phải. (2) sổ trái chữ trên, trên xuống. (3) sổ giữa chữ trên. (4) sổ-gập bên phải chữ trên. (5) ngang chữ dưới. (6) ô vuông bên trái chữ dưới. (7) nét móc bên phải chữ dưới. (8) sau cùng là nét mái nhà trên đầu chữ dưới. Theo số hiệu nét: **2 – 1 – 4 – 3 – 7 – 5 – 8 – 6**."* |

### 3.2.6. Jumpscare — `scare_ban_tay_giay_sau_manh`

| Trường | Giá trị |
|---|---|
| `trigger_type` | `ON_COLLECT_ITEM` · `item_ban_rap_chu_the` · delay **350 ms** · **1 lần duy nhất** |
| Loại | **Impulse scare** · `screen_flash: true` · envelope **1100 ms** (ngắn hơn trần — cú này cần *nhanh và bẩn*) |
| `audio_asset` | `sfx_scare_manh_nua_bat.ogg` · `sprite_animation`: `anim_ban_tay_vang_ma_quet` |

**Mô tả (SPINE):** ngay khi nét than cuối cùng của chữ "Mệnh" hiện lên, tấm mành nứa bật tung, **một bàn tay vàng mã khô quét sát mặt kính màn hình** kèm tiếng giấy sột soạt rất gần.

| Mốc | Sprite | Camera | Ánh sáng | Âm thanh | Haptic |
|---|---|---|---|---|---|
| **−5000 ms** | Mành nứa vẫn đập nhịp không đều | Tĩnh | — | **SILENCE TELL**: `fol_manh_nua_dap` và lớp gió **rút về 0 trong 600 ms và không trở lại**. Người chơi không ý thức được, nhưng phòng vừa "chết" | — |
| **−2000 → −1 ms** | Nét than cuối đang được miết | Tĩnh | — | **IM LẶNG TUYỆT ĐỐI** (tiếng than cũng tắt ở −400 ms, khi người chơi nhấc ngón tay) | — |
| **0 ms** | Chữ "Mệnh" hiện trọn. `spr_manh_nua` **bật tung lên trên** (rotation −38° trong 70 ms) | Punch-in **+12 %**, tâm giữa màn hình | — | Transient tre gãy, đỉnh **−4 dBTP** — cú **nhọn nhất chương** | `hap_double_knock` (25 · 60 · 25 ms) |
| **80 ms** | `spr_ban_tay_vang_ma` xuất hiện từ mép phải, **quét ngang sát mặt kính**, scale 1.0 → **1.45**, vận tốc 2 400 px/s | Shake **12 px** chéo, 10 Hz; tilt +2,5° | **FLASH** `#FFF2DC` alpha 0 → **0.34**, 40 ms. Diegetic: **mành bật tung làm lọt ánh sáng còn sót ngoài sân vào hiên tối**; đồng thời là **mask cut** để tráo sprite bàn tay vào khung | `fol_giay_ban_sot_soat` −12 dBFS, dry 100 % | — |
| **200 ms** | Bàn tay **đã quét qua khỏi khung** — chỉ hiện diện **130 ms**: mắt thấy, não không kịp phân tích. Còn lại vài mẩu vàng mã bay lơ lửng | Shake 5 px, tilt về 0 | Alpha 0.34 → 0.08 | Đuôi giấy | `hap_tap_light` |
| **600 ms** | Mành nứa **rơi trở lại vị trí cũ**, đứng im. Mẩu giấy còn rơi | Nhả về 102 % | Alpha 0 | Chỉ tiếng giấy rơi chạm gạch | — |
| **1100 ms** | **Envelope kết thúc** | 100 % | — | Recovery — **nhưng lớp `fol_manh_nua_dap` KHÔNG trở lại nữa trong phần còn lại của khu vực. Gió đã ngừng vĩnh viễn** | — |

> **Ghi chú đạo diễn:** việc lớp mành nứa **không bao giờ quay lại** là một cú dread trả góp — người chơi ở lại khu vực thêm 2 phút trong một sự im lặng mới, và hầu hết sẽ không hiểu tại sao mình thấy khó ở.

**Vì sao đặt ở khoảnh khắc GIẢI ĐÚNG thay vì giải sai:** đây là **điểm nhấn chủ đề đắt nhất chương** — *mỗi bước người chơi làm đúng là một bước tiến sâu hơn vào nghi lễ*. Người chơi được thưởng và bị phạt bằng cùng một hành động. Không một cú dọa theo-thất-bại nào nói được điều đó. Tiền đề đã xây sẵn bằng `fol_manh_nua_dap` suốt 4–5 phút: cái mành đã đập hàng chục lần và chưa lần nào có gì xảy ra; người chơi đã ngừng để ý tới nó. Đó chính là lúc dùng nó.

### 3.2.7. Mục tiêu người chơi

| Cấp | Mục tiêu |
|---|---|
| Bề mặt | Đi qua bức bình phong để vào gian thờ thắp hương |
| Cơ học | Nhặt `item_giay_ban_va_than` **và** `item_den_dau` → giải `puz_rap_chu_the_menh` → nhận `item_ban_rap_chu_the` → `USE_ITEM` vào `hs_o_lom_binh_phong` → mở `area_gian_tho` |
| Cảm xúc | Chuyển từ "nhà này lạ" sang "nhà này **đang chờ mình làm một việc gì đó**" |

**Dạy cơ chế:** khu vực này dạy `USE_ITEM` (kéo item từ hành trang thả lên hotspot). Bản rập là item đầu tiên phải **dùng** chứ không chỉ nhặt.

`[[ CẢNH BÁO SẢN XUẤT: item_den_dau nhặt ở đây nhưng chỉ dùng ở Khu 4. Nếu người chơi bỏ sót nó, P5 sẽ tắc. Biện pháp: hs_den_dau_treo đặt ở cột hiên ngang tầm mắt, và txt_examine_den_dau lúc nhặt nêu đủ ba thứ còn thiếu — dựng mục tiêu ngay từ đây. ]]`

### 3.2.8. Khu vực này đẩy cốt truyện tiến lên thế nào

1. **Gọi tên hủ tục.** Hết khu vực này, người chơi đã có hai chữ "Thế Mệnh" trong tay — nghĩa đen là một **vật chứng cầm được**. Từ đây mọi thứ tìm thấy sau đều quy chiếu về hai chữ ấy.
2. **Giới thiệu giọng bà nội.** Trang nhật ký 1976 là lần đầu người chơi nghe một người trong nhà *thú nhận*. Quan trọng: nó thú nhận về **thủ tục**, không về tội. Bà kể chuyện rập giấy như kể chuyện gói bánh chưng. **Sự bình thường hóa đó đáng sợ hơn mọi lời kể tội.**
3. **Cài đứa trẻ.** *"Con bé ngồi ở chõng ăn khoai lang"*.
4. **Cài bà Tơ.** Nhãn hàng mã cho biết có người đang đặt hàng cho lễ này **năm 1996**, không phải 1976.
5. **Người chơi tự tay làm phần lễ thứ hai.** Rập chữ và dán lên bình phong chính là nghi thức dựng "biển báo cõi âm". Người chơi tưởng mình mở khóa; thực ra người chơi vừa treo biển lên cửa nhà mình.

---

## 3.3. KHU VỰC 3 — `area_gian_tho` · "Gian thờ giữa và bàn thờ họ"

| Trường | Giá trị |
|---|---|
| Thứ tự | **3** |
| Gate vào | **Đã dùng `item_ban_rap_chu_the` tại `hs_o_lom_binh_phong`** (`flag_binh_phong_da_tra = true`) — then cửa gian giữa nhả ra |
| `background_asset_url` | `https://cdn.linhanthon.game/assets/bg_gian_tho.bundle` |
| Thời lượng | **12–15 phút** — khu vực dài nhất chương |
| Câu đố | `puz_tuan_tu_le_cung` **và** `puz_ba_hoi_chin_tieng` (độc lập với nhau) |
| Jumpscare | `scare_di_anh_quay_mat` · `scare_khoi_tu_hinh_nguoi` *(phái sinh)* |
| Vai trò | **NÚT CỔ CHAI (hub) của chương** — 4 trong 8 cạnh chuyển khu đi qua đây |

### 3.3.1. Không khí

**18 giờ 40.** Gian giữa của nhà ba gian, trần cao, xà gỗ đen. Tối hơn hiên một bậc. Nguồn sáng: **một cây đèn dầu leo lét bên trái bàn thờ — cây bên phải tắt ngóm** (phạm điều Năm, và là lý do tồn tại của P5), ánh đỏ của một **vòng hương đang cháy dở** treo trên xà, và ánh sáng lạnh hắt qua chấn song gỗ.

**Mùi:** **nhang lạnh** — mùi nhang đã tắt, khác hẳn nhang đang cháy; cộng mùi mực tàu và mùi gỗ mít.

**Âm thanh `amb_gian_tho_tinh`** (−34 dBFS, **ambience tĩnh nhất chương**, loop 120 s để không ai phát hiện ra nó lặp trong 6 phút đọc): gần như chỉ là tiếng phòng + `fol_huong_vong_lach_tach` rất khẽ. Và — đúng **25 giây** sau khi vào khu vực — **tiếng mõ vọng ra từ sau vách buồng bên phải**: ba hồi, thưa rồi mau, rồi lặng. Lặp lại theo chu kỳ 25 giây khi người chơi chưa giải P4.

> **Nguyên tắc dàn cảnh:** đây là *trung tâm thông tin* của chương. **Mật độ chữ cao nhất, mật độ dọa thấp nhất.** Người chơi cần được yên để đọc — vì thế khoá L1 (khoá đọc) phải hoạt động tuyệt đối ở đây.

| Lớp | Nội dung |
|---|---|
| BACKGROUND | Vách gỗ ba gian ám khói đen, hoành phi sơn son thếp vàng đã tróc, xà ngang treo vòng hương, cửa buồng tối om bên phải |
| MIDGROUND | Bàn thờ họ chính giữa, khám thờ Bà Cô bịt vải điều sát vách trái, cầu thang gỗ mọt lên gác xép + khe mộng cửa gác phía trên, trang gia phả mở trên tủ chè bên phải |
| FOREGROUND | Chiếu cói trải giữa nhà (có vết lõm hình người rất nhỏ), mõ cá trên đôn gỗ thấp bên trái, dùi mõ nằm cạnh, chậu hoá vàng, cửa hậu thấp góc trái |
| FX | Khói ba nén nhang bốc thẳng rồi **bẻ ngang giữa chừng**, bụi lơ lửng trong vệt sáng, ánh nến vàng đục dao động 0,5 Hz, vignette nặng nhất chương (trừ gác xép) |

### 3.3.2. Khung hình mở

Bàn thờ họ chiếm chính giữa khung hình, và nó **bày lộn xộn** — cái lộn xộn của một đám tang vừa dọn dở: mâm ngũ quả đẩy lệch sang bên, đĩa xôi, chén rượu đổ, bát cơm úp có quả trứng bổ đôi và đôi đũa bông cắm thẳng, vàng mã chất đống dưới chân.

Trên cao là hoành phi sơn son thếp vàng đã bong, ba chữ **德流光** (Đức Lưu Quang).

Và thứ mắt người chơi Việt sẽ dính vào ngay: **bát hương xoay lệch chừng bốn mươi lăm độ so với hoành phi**, cả bó chân nhang nghiêng theo.

Bên trái bàn thờ, thấp hơn một tấc, là **khám thờ gỗ nhỏ bịt vải điều** — không ảnh, không tên, không bát hương riêng. Bên trái nữa, dưới chân tường, là **mõ cá gỗ mít**, và gác trên mõ là một cái **dùi**.

### 3.3.3. Bảng hotspot (17 hotspot — đông nhất chương)

| # | id | bounds {x, y, w, h} | action_type | Tham số | Vai trò kịch bản |
|---|---|---|---|---|---|
| 1 | `hs_hoanh_phi` | `{x:640, y:96, width:700, height:140}` | `EXAMINE` | `txt_examine_hoanh_phi` | **Clue C2 của P3** — "đèn trước, nhang sau, vàng sau rốt" |
| 2 | `hs_huong_vong` | `{x:1420, y:110, width:260, height:170}` | `EXAMINE` | `txt_examine_huong_vong` | Đồng hồ cõi âm: một vòng = một ngày đêm, mà nhà bỏ không mười ngày |
| 3 | `hs_khe_mong_cua_gac` | `{x:430, y:120, width:150, height:110}` | `USE_ITEM` | `required_item: item_bai_vi_khuyet_danh` · `item_id: item_bai_vi_khuyet_danh` · fallback `txt_khoa_khe_mong_cua_gac` | **Tra bài vị làm then** — một nửa gate lên gác xép |
| 4 | `hs_cau_thang_gac` | `{x:430, y:250, width:150, height:330}` | `CHANGE_AREA` | `target_area_id: area_gac_xep` · gate: có `item_den_dau_sang` **VÀ** `flag_then_gac_da_tra` · `txt_khoa_cau_thang_gac` | Lối lên Khu 5 |
| 5 | `hs_kham_tho_ba_co` | `{x:110, y:240, width:290, height:240}` | `EXAMINE` | `txt_examine_kham_tho` | **Vệt tay lau sạch giữa lớp bụi** — dấu vết người sống |
| 6 | `hs_bai_vi_khuyet_danh` | `{x:130, y:500, width:250, height:120}` | `COLLECT_ITEM` | `item_id: item_bai_vi_khuyet_danh` · `required_item: null` | **Chỉ hiện sau khi giải P3.** Mũi neo twist B2 |
| 7 | `hs_dai_vai_dieu` | `{x:130, y:640, width:250, height:110}` | `COLLECT_ITEM` | `item_id: item_dai_vai_dieu` · `required_item: null` | **Chỉ hiện sau khi giải P4.** Nguyên liệu tim đèn cho P5 |
| 8 | `hs_ban_tho_ho` | `{x:640, y:300, width:660, height:420}` | `ZOOM_PUZZLE` | `target_puzzle_id: puz_tuan_tu_le_cung` | **Câu đố P3** |
| 9 | `hs_gia_pha` | `{x:1600, y:330, width:260, height:300}` | `EXAMINE` | `txt_examine_gia_pha` | **Mũi neo twist B1** + **lời giải ngôi thứ của P6** |
| 10 | `hs_bat_huong` | `{x:1330, y:520, width:150, height:150}` | `EXAMINE` | `txt_examine_bat_huong` | Điều cấm kỵ thứ Ba đã bị phạm |
| 11 | `hs_vach_buong` | `{x:1620, y:690, width:240, height:290}` | `DIALOGUE` | `txt_thoai_vach_buong` | **Clue C1 của P4** — nghe lại vô hạn |
| 12 | `hs_van_khan` | `{x:1330, y:740, width:230, height:140}` | `EXAMINE` | `txt_examine_van_khan` | **Văn bản quan trọng nhất chương** — clue C1 của P3 **và** clue C3 của P4 |
| 13 | `hs_mo_ca` | `{x:300, y:780, width:240, height:210}` | `ZOOM_PUZZLE` | `target_puzzle_id: puz_ba_hoi_chin_tieng` · fallback `txt_khoa_mo_ca_thieu_dui` | **Câu đố P4** |
| 14 | `hs_dui_mo` | `{x:560, y:780, width:110, height:120}` | `COLLECT_ITEM` | `item_id: item_dui_mo` · `required_item: null` | Mở khoá P4 · **kích hoạt `scare_di_anh_quay_mat`** |
| 15 | `hs_chieu_coi` | `{x:700, y:800, width:520, height:190}` | `EXAMINE` | `txt_examine_chieu_coi` | Vết quỳ của một đứa bé lên bảy |
| 16 | `hs_cua_hau_xuong_bep` | `{x:60, y:790, width:200, height:200}` | `CHANGE_AREA` | `target_area_id: area_bep_gieng` · gate: **đã giải P3** · `txt_khoa_cua_hau` | Xuống Khu 4 |
| 17 | `hs_ra_hien` | `{x:1300, y:900, width:280, height:95}` | `CHANGE_AREA` | `target_area_id: area_hien_nha` · **không gate** | Đường lùi, luôn mở |

**Tự kiểm tra bố cục:** 17 hotspot · 136 cặp · **0 giao nhau** · `y_min = 96` ✓ · `y_max = 995` ✓ · nhỏ nhất `hs_dui_mo` 110×120 ✓ và `hs_ra_hien` 280×95 ✓. Ba cặp sát nhau nhất cách 20–50 px theo x.

**Nguyên tắc đọc cảnh:** **cột trái là "trục Bà Cô"** (khám → bài vị → vải điều → mõ) xếp dọc từ trên xuống, đọc như một câu chuyện; **cột phải là "trục tài liệu"** (gia phả → bát hương → văn khấn → vách buồng). Bàn thờ giữ trọn tâm màn hình. Ba hotspot `CHANGE_AREA` đặt ở **ba mép khác nhau** (trái-dưới xuống bếp, giữa-trên lên gác, phải-dưới ra hiên) — người chơi không bao giờ nhầm lối.

> **Lưu ý dữ liệu:** phần thưởng của hai câu đố **không rơi thẳng vào túi đồ** mà **spawn hotspot** `hs_bai_vi_khuyet_danh` / `hs_dai_vai_dieu`. Người chơi phải tự tay nhặt — giữ nhịp nghi lễ và cho jumpscare một khoảng thở. `reward_item_id` trong JSON vẫn giữ nguyên để engine biết puzzle nào mở hotspot nào.

### 3.3.4. Văn bản đọc được (thành phẩm)

**① CUỐN VĂN KHẤN CHÉP TAY** — sổ bìa các-tông, giấy ố vàng, chữ nho và quốc ngữ xen kẽ, nét `hw_ong_tu`. **Văn bản quan trọng nhất chương**, chia nhiều trang đọc, mỗi trang ≤ 220 ký tự để vừa khung đọc màn hình 6.1".

> **`txt_examine_van_khan`** *(trang 1 — trình tự)*
>
> **VĂN KHẤN LỄ THẾ MỆNH**
> *(Nguyễn Văn Đối, trưởng họ Nguyễn thôn Linh An, kính chép.)*
>
> *"Phàm làm một tuần lễ: **trước hết phải sạch sẽ**, lau bài vị, bày mâm lễ cho tề chỉnh. **Đèn sáng thì hồn mới thấy đường mà về**, nên đôi đèn châm trước. **Hương thơm thì mới thỉnh được người**, ba nén nhang châm theo lửa đèn. **Sơ tuần rượu dâng khi hương đã bén.** Bấy giờ mới đọc lời khấn, khấn xong vái ba vái. **Khấn xong vái xong mới được hoá vàng — hoá vàng là tiễn, tiễn thì phải sau rốt.**"*
>
> **Thứ tự chớ sai:** Nhất — lau bài vị, bày mâm lễ. Nhị — thắp đôi đèn. Tam — thắp ba nén nhang. Tứ — rót sơ tuần rượu. Ngũ — đọc văn, vái ba vái. Lục — hóa vàng.
>
> Sai một bước thì nhang tắt, phải làm lại từ đầu.
> **Hóa vàng trước khi khấn là đại kỵ.** Lễ chưa tới tay mà tiền đã tới tay, thì người dưới ấy sẽ tự đi mà lấy.

> **`txt_examine_van_khan`** *(trang 2 — bài khấn)*
>
> Nam mô A Di Đà Phật *(ba lần)*.
>
> Con lạy chín phương Trời, mười phương Chư Phật, Chư Phật mười phương.
> Con kính lạy Hoàng Thiên Hậu Thổ chư vị Tôn thần.
> Con kính lạy Cao Tằng Tổ Khảo, Cao Tằng Tổ Tỷ, chư vị Hương linh họ Nguyễn thôn Linh An.
> Con kính lạy **Bà Cô tổ khuất mặt, phận gái út, mất năm Quý Tỵ, chưa có nơi có chốn.**
>
> Hôm nay là ngày … tháng … năm …
> Tín chủ chúng con là … , ngụ tại thôn Linh An, xã Linh Nam.
>
> Nhà có người mắc hạn, mệnh treo đầu sợi tóc. Chúng con kính sắm lễ mọn, hương hoa trà quả, giấy tiền vàng bạc, dâng lên trước án.
>
> Cúi xin Bà Cô thương đến, **cho lấy một thân thế một thân, lấy một tên thế một tên.**
> Thân này xin dâng, tên này xin xóa. Từ nay trong nhà không ai nhắc đến nữa.
>
> Kính xin Bà Cô nhận cho, **thôi đừng ngoảnh lại.**
>
> Chúng con lễ bạc tâm thành, cúi xin chứng giám. Cẩn cáo.

> **`txt_examine_van_khan`** *(trang 3 — chữ nhỏ viết chen ở lề, cùng người, mực khác)*
>
> Chú: người thế mệnh **phải là người không tên**. Có tên thì Bà Cô nhận nhầm, nhận sang người khác trong nhà.
> Cho nên: cạo tên khỏi gia phả, khoét mặt khỏi ảnh thờ, khắc bài vị **để trống**.
> Đây là phép của tôi nghĩ ra, lệ cũ không có. Nếu sai, tội tôi chịu.
> *— Đ.*

> **`txt_examine_van_khan`** *(trang 4 — dòng cuối, mực khác, là clue C3 của P4)*
>
> *"Lễ Bà Cô thì gọi bằng mõ: **ba hồi chín tiếng**. Mỗi hồi gõ dồn rồi **chốt ba tiếng rời**, **điểm một tiếng chuông** thì hồi ấy mới trọn.*
> *Gõ đủ ba hồi chín tiếng là mời. Gõ thiếu là gọi suông, người ta không lên. **Gõ thừa là giục. Chớ giục.**"*

**② TRANG GIA PHẢ BỊ CẠO** — sổ gia phả họ Nguyễn, giấy dó đóng chỉ.

> **`txt_examine_gia_pha`**
>
> **GIA PHẢ HỌ NGUYỄN — THÔN LINH AN** · *Chi thứ hai, đời thứ tư.*
>
> **Hàng trên — ông bà:** Nguyễn Văn Trác *(1912 – 1968)* — phối: Nguyễn Thị Nhỡ *(1918 – …)*
>
> **Hàng giữa — các con, theo ngôi thứ trưởng · thứ · út:**
> 1. Trưởng nam: **Nguyễn Văn Đoan** *(1940 – 1972)*
> 2. Thứ nam: **Nguyễn Văn Đoàn** *(1943 – )*
> 3. Út nữ: **Nguyễn Thị Đoài** *(1947 – )*
>
> **Hàng dưới — các cháu:**
> 1. *(dòng này bị cạo bằng dao, lớp giấy mỏng hẳn đi, chỉ còn thấy chân chữ "N", một nét sổ, và chữ đệm "Thị")*
> 2. Nguyễn Văn Thuấn *(1974 – )*
> 3. Nguyễn Thị Thoa *(1979 – )*

> **`txt_gian_tho_gia_pha_doc_thoai`**
> "Cạo. Không phải gạch, không phải bôi — **cạo**, bằng dao, cho hết hẳn nét.
> Giấy chỗ ấy mỏng đến mức soi lên thấy sáng.
> Người ta không muốn xóa một cái tên. Người ta muốn cái tên ấy **chưa từng được viết**."

`[[ Ngôi thứ trong trang gia phả này chính là LỜI GIẢI của puz_xep_anh_gia_pha ở area_gac_xep: hàng trên ông bà, hàng giữa trưởng-thứ-út, hàng dưới cháu theo thứ tự. Người chơi đọc kỹ ở đây thì giải nhanh ở đó. Đây là cách thưởng cho người đọc. ]]`

**③ BÁT HƯƠNG**

> **`txt_examine_bat_huong`**
> "Bát hương sứ men rạn kê lệch hẳn khỏi tâm bàn thờ, không còn thẳng với hoành phi.
> Chân nhang nghiêng cả bó theo một chiều, như có người đẩy. Trong tro có một vết ngón tay ấn sâu.
> Các cụ bảo bát hương động là **người dưới ấy trở mình**. Chưa bao giờ mình tin. Bây giờ mình cũng chưa tin.
> Mình chỉ không dám nắn nó lại."

**④ KHÁM THỜ BÀ CÔ** *(trước khi giải P3)*

> **`txt_examine_kham_tho`**
> "Một cái khám gỗ nhỏ, bịt kín bằng vải điều, đặt thấp hơn bàn thờ chính đúng một tấc.
> Không ảnh. Không bài vị nhìn thấy được. Không bát hương riêng.
> Trên mặt vải, bụi phủ đều — trừ **một vệt tay lau sạch ở ngay chính giữa**, cỡ bàn tay người lớn.
> Có người vẫn lau chỗ này. Thường xuyên."

**⑤ BÀI VỊ KHUYẾT DANH** — độc thoại khi nhận `item_bai_vi_khuyet_danh`.

> **`txt_gian_tho_bai_vi`**
> "Bài vị gỗ vàng tâm. **Gỗ mới** — thớ còn sáng, cạnh chưa lên nước.
> Có khung, có đế, có cả chỗ sơn son chờ khắc chữ.
> Mà mặt bài vị thì trắng trơn. Không một nét.
> Trong nhà này ai cũng có tên, kể cả người chết. Trừ người này."

> **`txt_gian_tho_bai_vi_doi_chieu`** *(chỉ bật nếu người chơi đang có `item_ban_rap_chu_the` — nhánh thưởng cho người chơi chủ động)*
> "Mình giơ bản rập lên cạnh cái bài vị.
> Nét gỗ trên bài vị, chỗ định khắc, có sẵn một khung dấu chì mờ — rộng đúng bằng **hai chữ**.
> Hai chữ, không phải ba, không phải bốn. Tên người ta thì ít nhất cũng ba chữ.
> Hai chữ. Vừa đúng **Thế Mệnh**.
> Cái bài vị này không chờ một cái tên. Nó chờ một **chức danh**."

**⑥ VÒNG HƯƠNG**

> **`txt_examine_huong_vong`**
> "Vòng hương thẻ treo trên xà, cháy được chừng hai phần ba rồi tắt.
> Tàn hương rơi thành vòng tròn đều tăm tắp dưới sàn — trừ **một chỗ khuyết, đúng bằng một bàn chân người đứng**.
> Một vòng hương cháy hết đúng một ngày một đêm — nhà hàng mã vẫn quảng cáo thế.
> Bà mất mười hôm rồi. Vậy vòng này ai thắp, và thắp lúc nào?"

**⑦ CHIẾU CÓI TRƯỚC BÀN THỜ**

> **`txt_examine_chieu_coi`**
> "Chiếu cói, viền đã tướp.
> Giữa chiếu có một vệt sờn bạc, hình hai đầu gối và hai bàn tay — vết của người quỳ đúng một chỗ, nhiều lần, rất nhiều lần.
> Vệt ấy nhỏ. **Nhỏ bằng một đứa bé lên bảy.**
> Đưa tay vào thì thấy còn ấm."

**⑧ VÁCH BUỒNG** — node `DIALOGUE`, nghe lại vô hạn. **Đây là nguồn clue chính của P4.**

> **`txt_thoai_vach_buong`**
> *(Áp tai vào khe ván.)*
> Bên kia vách có tiếng mõ: **ba hồi**, mỗi hồi gõ dồn từ thưa đến mau rồi lặng, chốt lại bằng **ba tiếng rời** và **một tiếng chuông**.
> Xen giữa là giọng một bà lão lẩm nhẩm: *"...con lạy Bà, năm nay nhà con có người về rồi. Người ta tự về, Bà ạ. Con không phải đi tìm nữa..."*
>
> *(Chọn: **[Gõ lại vào vách]** / **[Nghe tiếp]** / **[Lùi ra]**. Gõ vào vách thì bên kia im bặt đúng ba giây, rồi tiếng mõ bắt đầu lại **từ đầu bài**.)*

`[[ dialogue_choices lưu lựa chọn, bàn giao sang Chapter 2. ]]`

**⑨ HOÀNH PHI**

> **`txt_examine_hoanh_phi`**
> "Bốn chữ đại tự sơn son đã tróc: **德流光** — *Đức Lưu Quang*, đức sáng để lại cho con cháu.
> Chữ 光 — chữ *Quang*, chữ *sáng* — bong nhiều nhất, gần như mất hẳn.
> Bên dưới có dán một tờ lịch cũ, mặt sau ghi tay: *'Giỗ Bà Cô — đèn trước, nhang sau, vàng sau rốt.'*"

**⑩ MÕ CÁ KHI CHƯA CÓ DÙI** — fallback của `ZOOM_PUZZLE`. **Bảo hiểm cho người chơi tắt tiếng / khiếm thính.**

> **`txt_khoa_mo_ca_thieu_dui`**
> "Mõ cá gỗ mít, miệng há đen ngòm. Trên tang mõ khắc chìm ba chữ số Hán: **三 五 七**.
> Gõ bằng đốt ngón tay thì mõ chỉ kêu đục một tiếng — phải có dùi mới ra tiếng."

**⑪ KHE MỘNG CỬA GÁC** — fallback của `USE_ITEM`.

> **`txt_khoa_khe_mong_cua_gac`**
> "Khe mộng gỗ hẹp trên khuôn cửa gác, sâu chừng một đốt tay.
> Chỗ này lẽ ra phải có một thanh then ngang — mà thanh then đã bị ai rút đi từ lâu rồi."

### 3.3.5. Câu đố A — `puz_tuan_tu_le_cung`

| Trường | Giá trị |
|---|---|
| Type | `SEQUENCE_ORDER` · Tên hiển thị: **"Một tuần lễ cúng"** |
| `solution` | **`[3, 6, 4, 1, 5, 2]`** |
| `reward_item_id` | `item_bai_vi_khuyet_danh` |
| `wrong_action_jumpscare` | `scare_khoi_tu_hinh_nguoi` *(phái sinh — nếu Lead không duyệt thì `null`)* |
| Độ khó / thời gian kỳ vọng | **3/5** · 120 giây (P25 = 75 s, P75 = 200 s) |
| Điều kiện mở khoá | **Không cần cầm vật phẩm.** Chỉ cần đọc văn khấn (`hs_van_khan`, `EXAMINE` tự do, cùng khu vực) |

**Cơ chế:** zoom vào mặt bàn thờ bày lộn xộn. **Sáu lễ vật/thao tác** nằm rải trên mặt bàn dưới dạng 6 icon gỗ (~150×150 px). Phía dưới màn hình có **một dải 6 ô vuông trống** — "chiếu lễ" — `{x:360, y:830, width:1200, height:170}`, mỗi ô 190×170 px, cách nhau 12 px. Thao tác: **kéo-thả** từng icon từ mặt bàn xuống ô, từ trái sang phải; **chạm hai lần** vào icon đã đặt để trả nó về bàn. Khi đủ 6 ô, nút **"Vái"** (hình hai bàn tay chắp) sáng lên ở `{x:1620, y:860, width:220, height:120}`; **chạm giữ 1 giây** để xác nhận. Không gian tìm kiếm 6! = **720**.

**Bảng ánh xạ ID phần tử** *(cố định theo atlas; vị trí bày trên bàn cố ý xáo trộn)*:

| ID | Icon | Thao tác nó đại diện |
|---|---|---|
| 1 | Nậm rượu + ba chén hạt mít | Rót sơ tuần rượu |
| 2 | Tập vàng mã + chậu hoá | Hoá vàng |
| 3 | Khăn lau trắng + mâm ngũ quả | Lau bài vị, bày mâm lễ |
| 4 | Bó **ba** nén nhang | Thắp ba nén nhang |
| 5 | Cuốn văn khấn chép tay | Đọc văn khấn rồi vái ba vái |
| 6 | Đôi đèn (chân nến đồng) | Thắp đôi đèn |

**Giải thích từng phần tử của mảng:**

| Ô trên chiếu | Giá trị | Bước lễ | Vì sao ở đây |
|---|---|---|---|
| 1 | `3` | **Lau bài vị & bày mâm lễ** | *"Trước hết phải sạch"* — không ai thắp nhang lên bàn thờ còn bụi. Văn khấn mở đầu bằng câu này |
| 2 | `6` | **Thắp đôi đèn** | *"Đèn sáng thì hồn mới thấy đường mà về"*. Trong lễ Bắc Bộ, đôi đèn/nến luôn châm trước |
| 3 | `4` | **Thắp ba nén nhang** | Có lửa đèn mới châm được nhang; *"hương thơm thì mới thỉnh được người"* |
| 4 | `1` | **Rót sơ tuần rượu** | *"Sơ tuần rượu dâng khi hương đã bén"* — tức là sau nhang |
| 5 | `5` | **Đọc văn khấn & vái ba vái** | Bày xong, thỉnh xong, dâng xong mới trình bày lời |
| 6 | `2` | **Hoá vàng** | *"Khấn xong vái ba vái mới được hoá vàng — hoá vàng là tiễn."* Tiễn thì phải cuối cùng |

**Manh mối:**

| # | Clue | Hotspot | Suy ra |
|---|---|---|---|
| C1 | **Cuốn văn khấn chép tay** *(clue CHÍNH)* | `hs_van_khan` | **Toàn bộ 6 bước và quan hệ trước-sau**, viết dưới dạng văn xuôi — người chơi phải đọc và sắp, không được đánh số sẵn |
| C2 | Hoành phi + tờ lịch cũ dán dưới | `hs_hoanh_phi` | **Xác nhận nhanh 3 mốc quan trọng nhất** (đèn → nhang → vàng) cho người chơi lười đọc dài |
| C3 | Sáp nến trên đôi đèn chảy **dày hơn** phần chân nhang | chi tiết nền trong khung zoom | Bằng chứng vật lý: **đèn được châm trước nhang** |
| C4 | Chậu hoá vàng còn ấm, **nằm ngoài cùng, gần cửa** | chi tiết nền trong khung zoom | Thứ dùng sau chót luôn được kê sát lối ra → **hoá vàng là bước cuối** |

> **Tự kiểm tra công bằng:** C1 nằm ngay trên bàn thờ, `EXAMINE` không cần vật phẩm, xuất hiện **trước** khi người chơi mở được câu đố. **C1 một mình đã đủ suy ra trọn vẹn 6 bước.** C2 là lưới an toàn cho người đọc lướt. Không đòi hỏi kiến thức lễ nghi ngoài đời.

**Thiết kế cái sai — cố ý:** hệ thống đặt **chồng vàng mã ngay tầm tay, sáng hơn các vật khác**, để dụ người chơi hóa vàng sớm. Đây chính là bẫy của **điều cấm kỵ thứ Tư**.

| Lần sai | Phản hồi |
|---|---|
| 1 | **Ba nén nhang tắt ngấm cùng lúc**, khói bốc ngược. Cả 6 icon **bay trả về mặt bàn** (xáo lại vị trí). Độc thoại: *"Sai rồi. Cúng sai còn tệ hơn không cúng."* |
| 2 | Như trên + **đôi đèn phụt tắt một ngọn**, ánh sáng gian thờ giảm 20 % cho tới khi giải xong (chỉ là khí quyển, **không** ảnh hưởng khả năng giải) |
| 3 | **JUMPSCARE `scare_khoi_tu_hinh_nguoi`** — khói không bay lên mà **tụ giữa gian thành dáng một người đứng chắp tay**, tan khi người chơi chạm màn hình. `screen_flash: false`. Sau đó `fail_count` reset, ánh sáng phục hồi |

`[[ Hint system kèm characterization: nếu người chơi loay hoay quá 40 giây, cuốn văn khấn TỰ LẬT sang trang đúng bước tiếp theo — ông từ đang kèm người chơi làm lễ. ]]`

**Ba mức gợi ý:**

| Tier | Nội dung |
|---|---|
| 1 | *"Không phải bày cho đẹp, mà bày cho đúng phép. Cuốn văn khấn chép tay ngay trên bàn thờ đã kể thứ tự từ đầu tới cuối — có điều nó kể bằng văn xuôi chứ không đánh số. Đọc kỹ những chỗ nói 'trước hết', 'bấy giờ mới', 'sau rốt'."* |
| 2 | *"Sạch trước đã: lau bài vị, bày mâm. Rồi đèn — vì hồn phải thấy đường mới về được. Có lửa đèn mới châm được nhang. Hương bén rồi mới dâng rượu. Dâng xong mới nói — đọc khấn, vái ba vái. Và hoá vàng là tiễn, nên hoá vàng phải sau rốt. Sáu bước, đúng sáu ô."* |
| 3 — **đáp án** | *"Kéo vào sáu ô theo đúng thứ tự: (1) khăn lau và mâm ngũ quả, (2) đôi đèn, (3) bó ba nén nhang, (4) nậm rượu, (5) cuốn văn khấn, (6) tập vàng mã. Theo số hiệu icon: **3 – 6 – 4 – 1 – 5 – 2**. Rồi chạm giữ nút Vái."* |

**Giải xong thì gì mở ra:** chốt gỗ khám thờ Bà Cô bật ra → spawn `hs_bai_vi_khuyet_danh`; **đồng thời** thanh gỗ chèn cửa hậu tự rơi xuống → `hs_cua_hau_xuong_bep` mở.

### 3.3.6. Câu đố B — `puz_ba_hoi_chin_tieng`

| Trường | Giá trị |
|---|---|
| Type | `AUDIO_MATCH` · Tên hiển thị: **"Ba hồi chín tiếng"** |
| `solution` | **`[3, 3, 5, 3, 7, 3]`** |
| `reward_item_id` | `item_dai_vai_dieu` |
| `wrong_action_jumpscare` | `scare_khoi_tu_hinh_nguoi` *(dùng chung với P3)* |
| Độ khó / thời gian kỳ vọng | **4/5 — câu đố khó nhất nửa đầu chương** · 180 giây (P25 = 120 s, P75 = 300 s) |
| Điều kiện mở khoá | **Bắt buộc có `item_dui_mo`** (nhặt tự do tại `hs_dui_mo`, cùng khu vực) |
| Quan hệ với P3 | **Hoàn toàn độc lập.** Giải theo thứ tự nào cũng được |

**Cơ chế:** zoom vào mõ cá gỗ mít treo cạnh bàn thờ, sau lưng là vách buồng trống. Màn hình puzzle có **đúng hai nút gõ**:

| Nút | Vùng chạm | Kết quả |
|---|---|---|
| **Mặt mõ cá** | `{x:520, y:420, width:520, height:420}` | Mỗi tap = 1 tiếng mõ "cốc" |
| **Chuông đồng nhỏ** (treo bên phải) | `{x:1240, y:380, width:260, height:260}` | Mỗi tap = 1 tiếng chuông "keng" |

**Thanh nhịp** chạy ngang phía trên `{x:360, y:180, width:1200, height:90}`: hiển thị **số tiếng đã gõ trong cụm hiện tại** bằng các chấm sáng, và **tự chốt cụm** khi người chơi ngừng tay quá **1,2 giây** (khoảng lặng = dấu ngắt cụm). Đây là cách người chơi "phân cụm" mà không cần nút phụ.

**Nút "Áp tai vào vách"** `{x:1620, y:180, width:220, height:120}`: phát lại **toàn bộ đoạn mõ mẫu** bên kia vách. **Không giới hạn số lần nghe, không tốn tài nguyên, không tính là lần sai.**

**Tiết tấu "dồn":** trong một hồi, các tiếng mõ phải **thưa dần → mau dần**; engine chỉ kiểm **số tiếng** và **xu hướng khoảng cách giảm dần** (dung sai ±35 %), **không** đòi khớp mili-giây — tránh phạt oan trên thiết bị yếu.

**Quy ước mã hoá mảng lời giải:** mảng gồm **ba cặp**, mỗi cặp ứng với **một hồi** — `[dồn_hồi1, rời_hồi1, dồn_hồi2, rời_hồi2, dồn_hồi3, rời_hồi3]`. Sau **mỗi cặp** người chơi bắt buộc gõ **đúng 1 tiếng chuông** — con số này **cố định, không mã hoá trong mảng** (luôn = 1, ba lần).

| Vị trí | Giá trị | Nghĩa |
|---|---|---|
| 1 | `3` | **Hồi 1 — phần dồn**: 3 tiếng mõ, gõ thưa rồi mau dần |
| 2 | `3` | **Hồi 1 — phần rời**: 3 tiếng mõ rời, đều nhau, cách rõ ràng. Sau đó: **1 tiếng chuông** |
| 3 | `5` | **Hồi 2 — phần dồn**: 5 tiếng mõ dồn |
| 4 | `3` | **Hồi 2 — phần rời**: 3 tiếng mõ rời. Sau đó: **1 tiếng chuông** |
| 5 | `7` | **Hồi 3 — phần dồn**: 7 tiếng mõ dồn |
| 6 | `3` | **Hồi 3 — phần rời**: 3 tiếng mõ rời. Sau đó: **1 tiếng chuông** (tiếng chuông thứ ba khép bài) |

> **Kiểm chứng tên gọi:** "**ba hồi**" = 3 cặp dồn/rời. "**chín tiếng**" = 3 + 3 + 3 = **9 tiếng mõ rời**. Phần dồn 3-5-7 là số lẻ tăng dần (lối gõ "thưa đến mau" của nhà chùa). Tổng tap = (3+3) + (5+3) + (7+3) + 3 chuông = **33 tap**.

**Manh mối — hai đường độc lập:**

| # | Clue | Hotspot | Đường | Suy ra |
|---|---|---|---|---|
| C1 | **Tiếng mõ bên kia vách** *(clue CHÍNH)* | `hs_vach_buong` + nút "Áp tai vào vách" trong puzzle | **Thính giác** | **Toàn bộ lời giải nghe được bằng tai**, nghe lại vô hạn |
| C2 | **Chữ khắc trên tang mõ: 三 五 七** | `hs_mo_ca` (fallback `txt_khoa_mo_ca_thieu_dui`) | **Văn bản** | **Ba con số của phần dồn: 3 – 5 – 7** |
| C3 | Dòng cuối cuốn văn khấn | `hs_van_khan` | **Văn bản** | **Cấu trúc**: mỗi hồi = dồn + 3 tiếng rời + 1 chuông; "chín tiếng" = ba lần ba |
| C4 | Cán dùi mõ **mòn nhẵn đúng ba chỗ tay cầm** | `hs_dui_mo` | Mô-típ | Tô đậm mô-típ "ba"; đồng thời là **điều kiện mở khoá** |

> **Tự kiểm tra công bằng & khả tiếp cận:** người chơi **tắt tiếng hoặc khiếm thính vẫn giải được 100 %** bằng C2 + C3, và thanh nhịp hiển thị **trực quan bằng chấm sáng** thay cho âm thanh. Mỗi tiếng mõ còn kèm **một nhịp haptic** — có thể giải hoàn toàn bằng xúc giác. Tier 2 hiện thẳng con số. **Ràng buộc bắt buộc triển khai, không phải tuỳ chọn.**

**Hành vi khi sai** (sai = kết thúc một cụm với số tiếng không khớp, gõ nhầm chuông/mõ, hoặc kết bài khi chưa đủ ba hồi):

| Lần sai | Phản hồi |
|---|---|
| 1 | Tiếng mõ bên kia vách **trả lời chậm hơn nửa nhịp**, như đang **nhại lại** đúng chuỗi người chơi vừa gõ sai. Thanh nhịp xoá trắng, làm lại từ hồi 1 |
| 2 | Bên kia vách nhại lại **to hơn và gần hơn** (pre-delay giảm từ 120 ms → 35 ms, pan dịch từ giữa sang sát tai phải — nghe như **đang tiến lại gần**). Trên thanh nhịp **hiện mờ số tiếng đúng của hồi 1** trong 2 giây rồi tắt. **Tier 1 tự mở miễn phí ở đây** thay vì ở lần sai thứ nhất |
| 3 | **JUMPSCARE `scare_khoi_tu_hinh_nguoi`** (dùng chung với P3). Sau đó `fail_count` reset |

**Ba mức gợi ý:**

| Tier | Nội dung |
|---|---|
| 1 | *"Đừng gõ bừa. Áp tai vào vách nghe lại — nghe bao nhiêu lần cũng được, bên ấy không mệt. Mà nếu không nghe rõ thì nhìn: trên tang mõ có khắc ba chữ số, và cuốn văn khấn trên bàn thờ có một dòng nói riêng về cách gọi Bà Cô bằng mõ."* |
| 2 | *"Ba hồi. Mỗi hồi hai phần: phần dồn gõ thưa rồi mau dần, phần rời gõ đúng ba tiếng tách bạch — ba lần ba là chín tiếng, đúng như tên gọi. Hết mỗi hồi thì điểm một tiếng chuông rồi mới sang hồi sau. Ba chữ khắc trên tang mõ — tam, ngũ, thất — chính là số tiếng của ba phần dồn."* |
| 3 — **đáp án** | *"Hồi một: 3 tiếng mõ dồn, ngừng, 3 tiếng mõ rời, rồi 1 tiếng chuông. Hồi hai: 5 tiếng mõ dồn, ngừng, 3 tiếng mõ rời, rồi 1 tiếng chuông. Hồi ba: 7 tiếng mõ dồn, ngừng, 3 tiếng mõ rời, rồi 1 tiếng chuông. Theo dãy số: **3 – 3 – 5 – 3 – 7 – 3**, xen một tiếng chuông sau mỗi cặp. Nhớ ngừng tay hơn một giây để chốt mỗi cụm."* |

**Giải xong thì gì mở ra:** dải vải điều phủ trong khám thờ **tuột xuống** → spawn `hs_dai_vai_dieu`. Theo lore: **"Bà Cô đã mở mắt"**, và vải điều tuột rồi **không được phủ lại** giữa chừng lễ.

### 3.3.7. Jumpscare của khu vực

#### A. `scare_di_anh_quay_mat` — thuộc SPINE

| Trường | Giá trị |
|---|---|
| `trigger_type` | `ON_COLLECT_ITEM` · `item_dui_mo` · delay **250 ms** · **1 lần duy nhất** |
| Loại | **Impulse scare "mềm"** — không transient nhọn, **không camera punch** · `screen_flash: false` · envelope **1200 ms** |
| `audio_asset` | `sfx_scare_chan_nhang_boc.ogg` · `sprite_animation`: `anim_di_anh_dong_loat_quay` |

**Mô tả (SPINE):** lúc người chơi nhặt dùi mõ, **cả bó chân nhang trong bát hương bốc cháy ngùn ngụt một nhịp**, và **tất cả di ảnh trên bàn thờ đồng loạt quay mặt vào trong vách**.

| Mốc | Sprite | Camera | Ánh sáng | Âm thanh | Haptic |
|---|---|---|---|---|---|
| **−5000 ms** | Bó chân nhang **khẽ nghiêng thêm 2°** | Tĩnh | — | `tell_chan_nhang_kho_co.ogg`, −35 dBFS, pan giữa | — |
| **−2000 → −1 ms** | Tay người chơi khép quanh cán dùi | Tĩnh | — | **IM LẶNG TUYỆT ĐỐI.** Cả `fol_huong_vong_lach_tach` cũng tắt | — |
| **0 ms** | Dùi rời khỏi mõ. **Cả bó chân nhang bốc cháy một nhịp** — `spr_chan_nhang_chay`, lửa cam, cao 180 px | **Không punch** (cố ý — cú này không "lao vào mặt") | **Không screen_flash.** Thay bằng **ánh lửa diegetic**: `light_bat_huong` ramp **0 → đỉnh trong 180 ms** (chậm hơn nhiều so với flash → không kích hoạt phản xạ nhạy sáng). Vùng sáng phủ **≤ 30 %** màn hình quanh `(960, 520)` | Tiếng bùng lửa, **attack 45 ms** (mềm), đỉnh −9 dBTP | `hap_long_rumble` 220 ms, 0.50, ramp xuống — mô phỏng **hơi nóng phả**, không mô phỏng cú đấm |
| **80 ms** | Lửa đỉnh. Trong ánh lửa, **toàn bộ 7 di ảnh bắt đầu quay** quanh trục dọc, 0° → 180°, **đồng loạt, cùng tốc độ** | Shake **4 px**, 6 Hz (chỉ để phá sự tĩnh) | Ánh lửa đỉnh | Lửa | — |
| **200 ms** | Di ảnh quay được ~90° — **đúng cạnh mỏng, gần như vô hình**. Khung hình khó chịu nhất: bàn thờ trông như **trống trơn** | Shake tắt | Ánh lửa tụt | Khung gỗ cọ kính, −20 dBFS | — |
| **600 ms** | **Tất cả di ảnh đã quay mặt vào vách.** Chỉ còn mặt sau bìa các-tông và mấy vệt hồ dán cũ. Lửa lụi | Tĩnh | Ánh sáng vùng bàn thờ **thấp hơn trước cú dọa 15 %** và giữ vậy | Im | — |
| **1200 ms** | **Envelope kết thúc. Trạng thái này VĨNH VIỄN** — di ảnh không bao giờ quay lại trong Chapter 1 | Tĩnh | — | Recovery 20 s; `fol_huong_vong_lach_tach` trở lại | — |

> **Ghi chú đạo diễn:** cú này cố ý **không có transient nhọn và không có punch** — impulse scare "mềm" nhất trong tám cú. Sức nặng nằm ở **hậu quả không thể hoàn tác**: người chơi phải ở lại căn phòng đó thêm 4–6 phút nữa để giải P4, với **bảy tấm ảnh úp mặt vào tường sau lưng**.

**Vì sao đặt ở đây:** (a) gian thờ là **phòng đọc** của chương — chỉ được có một jumpscare. (b) Cú dọa duy nhất ấy phải đặt ở **hành vi phạm thượng**: người chơi **lấy một vật ra khỏi bàn thờ**. Với người chơi Việt Nam, chạm vào đồ thờ là điều có trọng lượng văn hoá thật — cú dọa không cần giải thích một chữ nào. (c) Nó cũng là **chuyển tiếp chức năng**: ngay sau đó người chơi phải cầm dùi ấy gõ mõ, nên cú dọa biến cái dùi từ "vật phẩm" thành "vật đã bị đánh dấu". (d) **Không flash** vì đây là phòng đọc và người chơi còn phải đọc tiếp; flash làm mỏi mắt và kéo tụt khả năng đọc trong 10–15 giây kế tiếp.

#### B. `scare_khoi_tu_hinh_nguoi` — *(phái sinh, chờ Lead duyệt)*

| Trường | Giá trị |
|---|---|
| `trigger_type` | `ON_PUZZLE_FAIL_COUNT` · `max_fails: 3` · **dùng chung** cho `puz_tuan_tu_le_cung` và `puz_ba_hoi_chin_tieng` (hai bộ đếm riêng) · tối đa **2 lần/chương**, lần thứ 2 dùng biến thể rút gọn 700 ms |
| Loại | **DREAD scare** — không transient, không punch, không flash · `screen_flash: false` |
| `audio_asset` | `sfx_scare_khoi_tu.ogg` · `sprite_animation`: `anim_khoi_tu_dang_nguoi` |

| Mốc | Sprite | Camera | Ánh sáng | Âm thanh | Haptic |
|---|---|---|---|---|---|
| **−4000 ms** | Khói ba nén nhang bắt đầu bay **ngược xuống** thay vì lên (rất chậm, dễ bỏ qua) | Tĩnh | — | `tell_khoi_hut_nguoc.ogg` — sub 42 Hz cực khẽ, −36 dBFS. Người chơi **cảm** chứ không **nghe** | — |
| **−2000 → −1 ms** | Ba nén nhang **tắt ngấm cùng lúc** | Tĩnh | Gian thờ tụt 20 % | **IM LẶNG TUYỆT ĐỐI** | — |
| **0 ms** | `spr_khoi_tu` bắt đầu **tụ** ở giữa gian, alpha 0 → 0.5 trong 400 ms (**rất chậm**) | **Không punch, không shake** | Không flash | **Không transient** — chỉ một lớp sub 38 Hz + tiếng hút khí ngược, attack **900 ms**, đỉnh −16 dBTP | **Không haptic ở 0 ms** |
| **600 ms** | Khói thành **dáng một người đứng chắp tay**, cao 620 px, alpha 0.5, **không có mặt** *(nguyên tắc: không bao giờ vẽ mặt ma trong game này)* | Tĩnh | — | Sub đạt đỉnh | `hap_long_rumble` 220 ms, **0.25**, đặt ở 600 ms chứ không 0 ms → không phải cú giật, mà là cảm giác **phòng đang rung** |
| **1200 ms** | **Envelope kết thúc — nhưng sprite Ở LẠI.** `spr_khoi_tu` giữ tĩnh, alpha 0.5, **hoàn toàn bất động** cho tới khi người chơi **chạm màn hình** (tối đa 12 s rồi tự tan) | Tĩnh | — | Sub giữ đều −16 dBFS, không biến thiên | — |
| *(người chơi chạm)* | Khói **tan trong 700 ms** như khói thật, không âm thanh nào | Tĩnh | Phục hồi 100 % | Sub tắt trong 700 ms | — |

> **Có vi phạm trần 1200 ms không?** Không. Trần 1200 ms áp cho **envelope xung** (âm thanh có transient, camera, flash, haptic) — thứ gây tải sinh lý. `spr_khoi_tu` sau 1200 ms là **một phần tử cảnh tĩnh**, không transient, không chuyển động, và **người chơi kiểm soát thời điểm kết thúc**. Trường `static_hold_ms` là trường riêng, chỉ hợp lệ khi `impulse: false`.

**Vì sao là dread chứ không phải shock:** hai câu đố này là hai câu **dài nhất nửa đầu chương**. Người chơi sai 3 lần ở đây là người chơi **đang bực** — và một cú đấm lên người đang bực sinh ra **giận**, không sinh ra **sợ**. Vì vậy S4 là cú dọa **duy nhất trong game mà người chơi phải chạm màn hình để nó biến mất**. Nó không tấn công; nó **đứng đó chờ**. Người chơi lấy lại quyền kiểm soát bằng chính ngón tay mình → cảm xúc chuyển từ "bị làm phiền" sang "**bị nhìn**".

**Luật hoãn bắt buộc (cặp rủi ro S4 → S3):** nếu người chơi sai P3 ba lần (S4 bắn), rồi 40 giây sau nhặt `item_dui_mo`, thì S3 **chuyển sang biến thể hậu quả im lặng**: người chơi nhặt dùi bình thường, **không có gì xảy ra**; nhưng lần kế tiếp camera quét qua bàn thờ, **bảy di ảnh đã quay mặt vào vách rồi**. Không stinger, không flash, không haptic. *Đây là biến thể đáng sợ hơn bản gốc — thế giới đã đổi mà người chơi không thấy nó đổi.*

### 3.3.8. Mục tiêu người chơi

| Cấp | Mục tiêu |
|---|---|
| Bề mặt | Thắp cho bà nội nén nhang cho tử tế — nghĩa là phải dọn lại bàn thờ cho đúng lệ |
| Cơ học 1 | Đọc văn khấn → giải `puz_tuan_tu_le_cung` → khám thờ bật chốt → nhặt `item_bai_vi_khuyet_danh`; **đồng thời cửa hậu xuống bếp hết bị chèn** |
| Cơ học 2 | Nhặt `item_dui_mo` → giải `puz_ba_hoi_chin_tieng` → dải vải điều tuột → nhặt `item_dai_vai_dieu` |
| Cơ học 3 | `USE_ITEM` `item_bai_vi_khuyet_danh` vào `hs_khe_mong_cua_gac` (làm then — có thể làm ngay, nhưng cầu thang vẫn khoá tới khi có đèn sáng) |
| Cảm xúc | Từ "nhà này đang chờ mình làm gì đó" sang "**mình đang làm đúng cái việc ấy, và mình không dừng lại được**" |

### 3.3.9. Khu vực này đẩy cốt truyện tiến lên thế nào

1. **Biến nghi ngờ thành hệ thống.** Trước khu vực này, người chơi có những mảnh rời. Cuốn văn khấn biến chúng thành **một quy trình có tên, có tác giả, có sáu bước và một lời chú**. Kinh dị chuyển từ mơ hồ sang **hành chính**.
2. **Đặt trách nhiệm lên tay người chơi.** Đây là lần đầu người chơi **hành lễ trọn vẹn**. Sau khoảnh khắc này, người chơi không còn là khách. Người chơi là **người chủ lễ**.
3. **Trả về một vật chứng không thể giải thích khác đi.** Bài vị khuyết danh. Gỗ mới. Khung chì rộng đúng hai chữ.
4. **Mở hai cửa cùng lúc.** Cửa hậu xuống bếp (mở ngay) và cầu thang lên gác (còn khóa, cần đèn). Người chơi **thấy rõ đích đến là gác xép ngay từ đây** — tạo lực kéo suốt Khu 4.
5. **Trồng câu hỏi "ai đang sống trong nhà này".** Vệt tay lau trên vải điều, vòng hương cháy dở, tiếng khấn sau vách, chén chè mới rót. Ba dấu vết của người sống xếp cạnh ba dấu vết của người chết, và **game không phân loại hộ người chơi**.

---

## 3.4. KHU VỰC 4 — `area_bep_gieng` · "Bếp tro và giếng khơi sau nhà"

| Trường | Giá trị |
|---|---|
| Thứ tự | **4** |
| Gate vào | **Đã giải `puz_tuan_tu_le_cung`** — hóa vàng xong thì thanh gỗ chèn cửa hậu tự rơi xuống |
| `background_asset_url` | `https://cdn.linhanthon.game/assets/bg_bep_gieng.bundle` |
| Thời lượng | 10–12 phút |
| Câu đố | `puz_thap_lai_den_dau` |
| Jumpscare | `scare_mat_duoi_day_gieng` |

### 3.4.1. Không khí

**19 giờ 05. Khu vực tối nhất chương.** Trong 2–3 phút đầu, **70 % khung hình là đen tuyền**; độ sáng nền chỉ **18 %** cho tới khi thắp đèn, sau đó **55 %** trong bán kính quầng đèn. Người chơi chỉ thấy được **một quầng đỏ mờ từ đống tro còn than hồng** và một vệt sáng xanh rất nhạt hắt qua khe cửa liếp từ sân sau.

Gian bếp đất nện, thấp, trần ám bồ hóng dày đến mức sờ vào là dính. **Mùi:** tro nguội, dầu hỏa, mỡ cháy cũ — và khi mở cửa liếp ra sân sau thì đổi hẳn sang **mùi tanh lạnh của nước giếng lâu ngày không ai múc**.

**Âm thanh:** ambience đổi hẳn màu so với gian thờ — từ "cao, khô, vang gỗ" sang "thấp, ẩm, chết tiếng" (**RT60 tụt từ 1,4 s xuống 0,35 s**). `fol_than_no_lep_bep` là lớp duy nhất có sự sống; chuột chạy trên gác bếp; và từ ngoài sân sau, **đều đặn 9–11 giây một lần, tiếng "tõm" rất khẽ** — như có gì rơi xuống giếng. **Không bao giờ thấy vật gì rơi.**

Ngoài bờ ao, in bóng lên nền trời còn sót chút sáng, là **cây gạo** — thân xù xì, cành khô chĩa ngang. *"Thần cây đa, ma cây gạo"*: người chơi Việt không cần giải thích.

| Lớp | Nội dung |
|---|---|
| BACKGROUND | **Nửa trái:** vách bếp trát bùn rơm ám bồ hóng đen kịt, mái tranh thấp. **Nửa phải:** trời đêm sau nhà, tán cây gạo đen, bờ ao lấp loáng. **Cửa liếp tre chia đôi khung hình ở x ≈ 1170** |
| MIDGROUND | Gác bếp treo bó đóm và chai lọ, cột bếp có năm vạch dao khắc, bàn gỗ kê sát cửa liếp (nơi ghép đèn), thành giếng khơi xây gạch, gầu tôn treo trên cọc |
| FOREGROUND | Kiềng ba chân với nồi cơm còn ấm, đống tro ủ trấu còn than hồng, chai dầu hoả dựng chân cột, mép giếng rêu trơn |
| FX | Than hồng thở đỏ 0,3 Hz, hơi nước bốc lên miệng giếng, đom đóm thưa ngoài sân |

### 3.4.2. Khung hình mở

Bóng tối, rồi mắt quen dần. Thứ đầu tiên hiện ra là **kiềng ba chân** giữa bếp — và trên kiềng là một **nồi gang đậy vung**. Người chơi mở: **cơm còn trong nồi, còn ấm, mặt cơm chưa se**. Nhà bỏ không mười ngày.

Đảo mắt sang trái: **vách bếp ám bồ hóng**, ở độ cao ngang thắt lưng, có những **hình que vẽ bằng đầu ngón tay** miết vào lớp bồ hóng.

Sang phải: **cột bếp** bằng gỗ xoan, trên đó có **năm vạch khắc bằng dao**, mỗi vạch kèm một con số.

Qua cửa liếp là mảnh sân sau lát gạch vỡ, và **giếng khơi** xây gạch, thành cao ngang hông, miệng đen ngòm. Gầu tôn móc ở cọc tre, **dây gầu còn ướt**.

### 3.4.3. Bảng hotspot (14 hotspot)

| # | id | bounds {x, y, w, h} | action_type | Tham số | Vai trò kịch bản |
|---|---|---|---|---|---|
| 1 | `hs_so_cho_ba_noi` | `{x:700, y:110, width:220, height:130}` | `EXAMINE` | `txt_examine_so_cho` | **Mũi neo twist B4 — mạnh nhất trước gác xép** |
| 2 | `hs_gac_bep_bo_dom` | `{x:260, y:200, width:400, height:190}` | `EXAMINE` | `txt_examine_gac_bep` | **Clue C1 của P5** — mẫu đèn tháo rời để tham chiếu |
| 3 | `hs_cay_gao` | `{x:1200, y:96, width:260, height:260}` | `EXAMINE` | `txt_examine_cay_gao` | Ranh giới vùng hồn bị nhốt; nhà bà Tơ ở cạnh gốc gạo |
| 4 | `hs_den_dau_ghep` | `{x:850, y:280, width:290, height:300}` | `ZOOM_PUZZLE` | `target_puzzle_id: puz_thap_lai_den_dau` · fallback `txt_khoa_ghep_den_thieu_do` | **Câu đố P5** |
| 5 | `hs_gau_ton` | `{x:1500, y:280, width:170, height:190}` | `EXAMINE` | `txt_examine_gau_ton` | Dây gầu còn ướt — ai vừa múc nước? |
| 6 | `hs_thanh_gieng_chu_khac` | `{x:1700, y:290, width:180, height:160}` | `EXAMINE` | `txt_examine_thanh_gieng` | **Cái giếng gọi thẳng tên hủ tục ra** |
| 7 | `hs_vach_bo_hong_hinh_ve` | `{x:60, y:420, width:180, height:300}` | `EXAMINE` | `txt_examine_vach_bo_hong` | Hình que của Nhài và Tý |
| 8 | `hs_vach_bep_chu_than` | `{x:270, y:420, width:300, height:160}` | `EXAMINE` | `txt_examine_vach_bep_chu_than` | **Clue C2 của P5** — hai ràng buộc thứ tự quyết định |
| 9 | `hs_cot_bep_vach_dao` | `{x:680, y:420, width:130, height:520}` | `EXAMINE` | `txt_examine_cot_vach_dao` | **Mũi neo twist B3** — vạch thứ năm để trống |
| 10 | `hs_gieng_khoi` | `{x:1300, y:520, width:460, height:420}` | `USE_ITEM` | `required_item: item_den_dau_sang` · `item_id: item_den_dau_sang` · fallback `txt_khoa_gieng_toi` | **Phần lễ V — soi đường.** Hotspot to nhất khu vực vì người chơi chạm trong điều kiện màn hình tối |
| 11 | `hs_kieng_ba_chan` | `{x:340, y:620, width:260, height:130}` | `EXAMINE` | `txt_examine_kieng_ba_chan` | Nồi cơm còn ấm — dấu vết bà Tơ |
| 12 | `hs_chai_dau_hoa` | `{x:850, y:640, width:120, height:180}` | `COLLECT_ITEM` | `item_id: item_chai_dau_hoa` · `required_item: null` | Nguyên liệu P5 |
| 13 | `hs_len_gian_tho` | `{x:1000, y:700, width:150, height:290}` | `CHANGE_AREA` | `target_area_id: area_gian_tho` · **không gate** | Đường lùi, luôn mở |
| 14 | `hs_dong_tro_than` | `{x:300, y:780, width:340, height:210}` | `EXAMINE` | `txt_examine_dong_tro_than` | **Clue C5 của P5** — nguồn lửa duy nhất |

**Tự kiểm tra bố cục:** 14 hotspot · 91 cặp · **0 giao nhau** · `y_min = 96` ✓ · `y_max = 990` ✓ · nhỏ nhất `hs_chai_dau_hoa` 120×180 ✓.

**Ranh giới hai nửa:** mọi hotspot "trong bếp" đều có `x + width ≤ 1150`; mọi hotspot "ngoài sân sau" đều có `x ≥ 1200`. Dải cửa liếp (x 1150–1200) là **dải trung tính, không có hotspot** — người chơi đọc được ranh giới không gian chỉ bằng mắt.

### 3.4.4. Văn bản đọc được (thành phẩm)

**① SỔ CHỢ CỦA BÀ NỘI** — quyển sổ con gài trên mái tranh gác bếp, giấy ố khói, chữ `hw_ba_noi`. **Đây là mũi neo twist mạnh nhất trước gác xép.**

> **`txt_examine_so_cho`**
>
> *Chạp, Bính Thìn — chi cho việc nhà*
>
> Giấy bản loại một, 3 xấp ……………… 1 đ 2
> Than củi, 1 gói ……………………………… 0 đ 3
> Vải điều, 1 thước ………………………… 0 đ 8
> Dầu hỏa, 1 chai ……………………………… 1 đ 0
> Nan tre, hồ dán ……………………………… 0 đ 5
>
> **Áo cưới giấy, đặt bà Xuyến hàng mã chợ Dâu:**
> **dài 1 thước 52 — vòng ngực 82 — dài tay 56.**
> Ứng trước ………………………………………… 5 đ 0
>
> *(Dòng dưới, chữ nhỏ hơn, viết chen vào lề:)*
> Bà Xuyến hỏi tôi may cho người sống hay người chết.
> Tôi không trả lời được.
> Bà ấy lại hỏi sao may to thế, con bé mới lên bảy.
> Tôi bảo: **để dành đến lúc nó về.**

> **`txt_bep_gieng_so_cho_doi_chieu`** *(bật ngay sau, tự động — người chơi rút phiếu đo trong túi áo ra)*
> "Mình rút cái phiếu đo trong túi áo ra. Phiếu của hiệu may, tháng Ba năm nay, chị Bảy đo cho mình để cắt cái áo dài đi ăn cưới.
> **Dài 1 thước 52. Vòng ngực 82. Dài tay 56.**
> Chữ trong sổ này viết năm bảy mươi sáu.
> Hai mươi năm trước ai đó đã đo mình, ở một tuổi mình còn chưa có cái thân này."

`[[ Âm thanh: CẮT PHẲNG toàn bộ nền về −50 dBFS trong 3 giây ngay khi hai con số khớp. Không thêm âm thanh nào. Đây là cú dread mạnh thứ hai chương — và nó không tiêu tốn một jumpscare nào. ]]`

**② CỘT BẾP — NĂM VẠCH DAO**

> **`txt_examine_cot_vach_dao`**
>
> *(Năm vạch khắc sâu vào gỗ xoan, cách nhau đều. Cạnh mỗi vạch có một hàng chữ nhỏ, phần tên đã bị bào phẳng đi, chỉ còn đọc được năm:)*
>
> ▌ ……………… **Quý Tỵ — 1953**
> ▌ ……………… **Tân Sửu — 1961**
> ▌ ……………… **Mậu Thân — 1968**
> ▌ ……………… **Bính Thìn — 1976**
> ▌ ……………… *(vạch này khắc mới hơn hẳn, gỗ chưa lên màu. Chỗ ghi năm còn để trống.)*

> **`txt_bep_gieng_cot_vach_dao_doc_thoai`**
> "Bốn vạch cũ. Một vạch mới.
> Người ta đánh dấu như đánh dấu chiều cao cho trẻ con. Nhưng trẻ con thì phải cao dần lên.
> Năm vạch này **cao bằng nhau**."

**③ CHỮ KHẮC TRÊN THÀNH GIẾNG** — khắc sâu vào gạch, rêu ăn vào nét chữ.

> **`txt_examine_thanh_gieng`**
>
> **QUÝ TỴ NIÊN**
> **NƯỚC GIẾNG NÀY KHÔNG DÙNG ĂN.**
> **CHỈ DÙNG RỬA MẶT CHO NGƯỜI THẾ MẠNG.**
>
> *(Bên dưới là ba cái tên bị đục nát.)*

> **`txt_bep_gieng_thanh_gieng_doc_thoai`**
> "Người thế mạng.
> Cả buổi chiều nay mình đã đọc được hai chữ *Thế Mệnh*, đã cầm một cái bài vị không tên, đã đứng trên cái chiếu có vết quỳ của một đứa bé.
> Giờ thì cái giếng gọi thẳng tên cái việc ấy ra."

**④ HÌNH VẼ TRÊN VÁCH BỒ HÓNG** — miết bằng đầu ngón tay trẻ con, cao 90 cm.

> **`txt_examine_vach_bo_hong`**
> "Hình vẽ bằng ngón tay, miết vào lớp bồ hóng. Cao chừng đến thắt lưng mình — tức là tầm với của một đứa bé.
>
> Một cái nhà ba gian, mái vẽ bằng ba nét ngang.
> Một cái vòng tròn có cái gạch ngang bên trên — cái giếng, có cái gầu.
> Ba hình người que.
>
> Hai hình đứng cạnh giếng. Một hình **nằm ngang**, ở phía trong vòng tròn.
>
> Bên dưới, có ai đó cố viết một chữ, viết đi viết lại ba lần đều hỏng. Chỉ đọc được nét đầu: một chữ **L**.
> Cạnh đó, nguệch ngoạc: *'con ko muon di'*."

**⑤ CHỮ THAN TRÊN VÁCH BẾP** — clue C2 của P5.

> **`txt_examine_vach_bep_chu_than`**
> "Mấy dòng chữ than to tướng trên vách, nét người lớn dạy trẻ con:
> *'**Tim ngấm dầu hẵng châm lửa**, kẻo cháy cụt tim. **Vặn tim cao quá thì khói đen bám bóng** — vặn xong mới châm.'*"

**⑥ GÁC BẾP** — clue C1 của P5.

> **`txt_examine_gac_bep`**
> "Gác bếp treo bó đóm chẻ sẵn, mấy cái chai không, và một cây đèn dầu cũ đã hỏng nằm lăn lóc: **tim đã xỏ sẵn qua cổ đèn**, nhưng bầu khô cong, tim cụt ngủn không nhô lên nổi."

**⑦ ĐỐNG TRO CÒN THAN HỒNG**

> **`txt_examine_dong_tro_than`**
> "Đống tro ủ trấu giữa nền bếp. Bới nhẹ là than đỏ lộ ra, còn thở.
> Nhà bỏ không nhiều ngày mà bếp chưa tắt — nghĩa là **có người vẫn ủ than mỗi tối**. Ủ theo lối người quen bếp củi, ủ để mai khỏi phải nhóm lại.
> Chỉ cần một que đóm là có lửa."

**⑧ NỒI CƠM TRÊN KIỀNG**

> **`txt_examine_kieng_ba_chan`**
> "Kiềng ba chân bằng gang, trên bắc nồi cơm đậy vung. Mở ra: cơm còn ấm, mặt cơm chưa se, chưa đóng váng — nấu chưa quá hai tiếng.
> Xới sẵn **hai bát**, cắm hai đôi đũa dựng đứng giữa bát — kiểu cúng, không phải kiểu ăn.
> Người ấy tính ở đây lâu."

**⑨ GẦU TÔN**

> **`txt_examine_gau_ton`**
> "Gầu tôn móp treo trên cọc tre. Dây thừng **còn ướt sũng**, nước nhỏ thành vũng dưới chân cọc.
> Thành giếng cấm nước ăn.
> Vậy vừa nãy ai múc, và múc để làm gì?"

**⑩ CÂY GẠO**

> **`txt_examine_cay_gao`**
> "Cây gạo già ngoài bờ ao, đứng một mình giữa đồng, cành đen chĩa lên trời. Dưới gốc có mấy chân hương cắm thành một hàng thẳng, hương mới, chưa tàn hết.
> *Thần cây đa, ma cây gạo, cú cáo cây đề.*
> Trong nhật ký bà viết là rập chữ dán bình phong để *nó có chạy thì cũng không ra được đến cây gạo.*
> Từ cái giếng này đến gốc gạo, đi bộ chắc hai phút.
> Hai phút. Với một đứa bé thì là bao xa?"

**⑪ SOI LÒNG GIẾNG** — chỉ hiện khi `USE_ITEM` `item_den_dau_sang` lên `hs_gieng_khoi`. **Beat B11.**

> **`txt_bep_gieng_guoc_tre_con`**
> "Đèn hạ xuống. Ánh sáng bò dọc thành giếng, qua từng lớp gạch trơn rêu.
> Xuống chừng hai sải, ở một gờ gạch lồi ra, có **một chiếc guốc trẻ con**. Guốc mộc, quai vải đã mục, cỡ chân đứa bé chừng bốn năm tuổi.
> **Chỉ một chiếc.**
> Mặt nước ở dưới cùng phẳng lì, không gợn. Trong mặt nước ấy có ánh đèn của mình, và **có thêm một quầng sáng nữa**, nhỏ hơn, ở sâu hơn.
> Mình rụt tay lên."

**⑫ GIẾNG KHI CHƯA CÓ ĐÈN** — fallback.

> **`txt_khoa_gieng_toi`**
> "Lòng giếng đen đặc, thả mắt xuống chỉ thấy một khoảng tối tròn. Thành giếng mòn lõm chỗ người ta vẫn tì tay. Phải có đèn mới soi được xuống dưới."

**⑬ GHÉP ĐÈN KHI THIẾU ĐỒ** — fallback, **liệt kê đích danh thứ còn thiếu** (chống bí bách).

> **`txt_khoa_ghep_den_thieu_do`**
> "Mặt bàn đủ rộng để tháo cây đèn ra lắp lại. Nhưng còn thiếu: **{danh sách động: chính cây đèn / một sợi tim / một ít dầu hoả}**.
> *Ví dụ khi thiếu tim:* Có thân đèn, có chai dầu. Nhưng bầu đèn không có tim thì dầu nằm im. Phải tìm một mảnh vải dày, xé ra se được thành sợi."

### 3.4.5. Câu đố — `puz_thap_lai_den_dau`

| Trường | Giá trị |
|---|---|
| Type | `ITEM_COMBINE` · Tên hiển thị: **"Thắp lại cây đèn Hoa Kỳ"** |
| `solution` | **`[2, 5, 1, 3, 4]`** |
| `reward_item_id` | `item_den_dau_sang` |
| `wrong_action_jumpscare` | `scare_mat_duoi_day_gieng` |
| Độ khó / thời gian kỳ vọng | **3/5** · 110 giây (P25 = 70 s, P75 = 190 s) |
| Điều kiện mở khoá | **Bắt buộc có đồng thời ba vật phẩm:** `item_den_dau` (Khu 2) + `item_dai_vai_dieu` (thưởng P4) + `item_chai_dau_hoa` (nhặt tại chỗ) |

**Cơ chế:** zoom vào mặt bàn bếp cạnh kiềng ba chân; cây đèn dầu tháo rời nằm giữa khung `{x:760, y:380, width:400, height:520}`. **Năm phần tử** xếp quanh cây đèn (mỗi vùng chạm ≥ 160×160 px). Thao tác là **kéo phần tử thả vào cây đèn**, riêng núm vặn là **xoay**:

| Thao tác | Chi tiết tương tác |
|---|---|
| Kéo **dải vải điều** vào | Minigame phụ 1,5 s: **miết hai ngón theo chiều dọc** để se vải thành sợi tim |
| Kéo **tim** vào **cổ đèn** | Luồn qua ống |
| Kéo **chai dầu hoả** nghiêng trên bầu đèn | **Giữ ngón** cho tới khi vạch dầu chạm mức khắc trên bầu |
| **Núm vặn tim** | Đặt ngón lên núm và **xoay tròn**; đầu tim nhô lên/thụt xuống theo thời gian thực. Ngưỡng đúng: nhô **khoảng một hạt gạo** (vùng xanh trên thước nhỏ cạnh núm) |
| Kéo **que đóm** vào **đống than hồng** | Đóm bén lửa → kéo đóm sang **đầu tim** → chụp bóng thuỷ tinh xuống (tự động) |

**Không có nút xác nhận** — mỗi thao tác kéo/xoay là một bước, làm sai bước nào là biết ngay.

`[[ Thiết kế cố ý: bước 5 bắt người chơi thò tay vào đống tro. Đây là hành động vật lý duy nhất trong chương mà người chơi phải "chạm vào lửa". Rung haptic ngắn 40 ms. ]]`

**Bảng ánh xạ ID phần tử:**

| ID | Phần tử | Vị trí quanh cây đèn |
|---|---|---|
| 1 | **Chai dầu hoả nút lá chuối** | mép phải bàn |
| 2 | **Dải vải điều** | mép trái bàn |
| 3 | **Núm vặn tim** (gắn trên thân đèn) | thân đèn, bên phải |
| 4 | **Bó đóm trên gác bếp + đống than hồng** | góc dưới-trái khung |
| 5 | **Cổ đèn** (ống luồn tim, tháo rời) | ngay trước cây đèn |

**Giải thích từng phần tử của mảng:**

| Bước | Giá trị | Thao tác | Vì sao ở đây |
|---|---|---|---|
| 1 | `2` | **Xé & se dải vải điều thành tim đèn** | Chưa có tim thì không có gì để luồn, để ngấm, để châm. **Gốc của cả chuỗi** |
| 2 | `5` | **Luồn tim qua cổ đèn** | Tim phải nằm trong ống cổ đèn **trước khi đổ dầu**; đổ dầu rồi mới luồn thì dầu tràn ra tay và cổ đèn trơn, không xỏ được |
| 3 | `1` | **Chắt dầu hoả vào bầu đèn** | Có tim trong cổ rồi thì đầu dưới của tim ngập trong bầu, dầu thấm ngược lên theo mao dẫn |
| 4 | `3` | **Vặn núm cho tim nhô vừa một hạt gạo** | Chỉnh **trước khi châm**: nhô cao thì khói đen bám bóng, thụt quá thì lửa không bén. Phải chỉnh lúc chưa có lửa |
| 5 | `4` | **Rút đóm, mồi vào than hồng, châm vào tim** | Bước cuối. Tim đã ngấm dầu, đã chỉnh độ cao → lửa bén và giữ |

**Manh mối:**

| # | Clue | Khu vực | Hotspot | Suy ra |
|---|---|---|---|---|
| C1 | **Cây đèn hỏng bỏ trên gác bếp** | Khu 4 | `hs_gac_bep_bo_dom` | **Mẫu tham chiếu tháo rời**: tim đi **xuyên qua cổ đèn** (bước 2), bầu dầu là bộ phận riêng. Cũng chỉ ra **bó đóm** ở đâu |
| C2 | **Chữ than trên vách bếp** | Khu 4 | `hs_vach_bep_chu_than` | **Hai ràng buộc thứ tự quyết định**: dầu **trước** lửa (3 < 5); vặn núm **trước** lửa (4 < 5) |
| C3 | **Đèn dầu ở hiên, lượt EXAMINE khi nhặt** | Khu 2 | `hs_den_dau_treo` | **Danh sách nguyên liệu** phải đi gom — dựng mục tiêu ngay từ khu vực 2 |
| C4 | **Dải vải điều, lượt EXAMINE trong túi đồ** | Khu 3 | `hs_dai_vai_dieu` | **Vải điều = tim đèn**, và phải **se** trước khi dùng (bước 1) |
| C5 | **Đống tro còn than hồng** | Khu 4 | `hs_dong_tro_than` | **Nguồn lửa duy nhất** — đóng đinh bước 5 |

> **Tự kiểm tra công bằng:** bốn ràng buộc rút ra được — *tim trước cổ đèn* (C1), *tim + cổ trước dầu* (C1, cấu tạo bầu/cổ), *dầu trước lửa* (C2), *vặn trước lửa* (C2). Ghép lại chỉ còn **đúng một thứ tự hợp lệ**: 2 → 5 → 1 → 3 → 4. Mọi clue đều `EXAMINE` không tốn tài nguyên và đọc lại được.

**Hành vi khi sai** (sai = thực hiện bước không đúng phần tử kế tiếp):

| Lần sai | Phản hồi |
|---|---|
| 1 | Phản hồi **theo ngữ cảnh, có tính dạy**: châm lửa khi tim chưa ngấm dầu → *"lửa loé một cái rồi tắt, đầu tim cháy cụt thành tàn đen"*; đổ dầu khi tim chưa luồn → *"dầu tràn ra mặt bàn, mùi hắc xộc lên"*; vặn núm khi chưa có tim → *"núm quay lỏng lẻo, chẳng có gì nhô lên"*. Phần tử tự trả về chỗ cũ, **các bước đã làm đúng trước đó được giữ nguyên** |
| 2 | Như trên + **ánh than trong bếp lụi hẳn xuống** một nhịp, gian bếp tối thêm; tiếng nước khẽ dội dưới giếng ngoài sân sau |
| 3 | **JUMPSCARE `scare_mat_duoi_day_gieng`**. Sau đó `fail_count` reset; **tiến độ các bước đúng vẫn được giữ** |

> **Ràng buộc chống soft-lock:** `item_chai_dau_hoa` **không bị tiêu hao khi sai** — chai luôn còn dầu. **Không có tài nguyên hữu hạn nào trong câu đố này.**

**Ba mức gợi ý:**

| Tier | Nội dung |
|---|---|
| 1 | *"Cây đèn này không cần phép thuật, chỉ cần làm đúng như người quê vẫn làm. Trên gác bếp còn một cây đèn hỏng đã tháo rời — nhìn nó thì biết bộ phận nào lắp vào bộ phận nào. Và trên vách bếp có mấy chữ viết bằng than, ai đó dặn rất rõ thứ gì phải làm trước lửa."* |
| 2 | *"Bắt đầu từ sợi tim: vải điều xé dọc, se lại thành sợi. Tim phải luồn qua cổ đèn trước — đổ dầu rồi mới xỏ thì trơn tuột, không xỏ nổi. Có tim trong cổ rồi mới chắt dầu vào bầu cho tim ngấm. Chữ trên vách dặn hai điều: tim phải ngấm dầu hẵng châm lửa, và vặn tim cho vừa rồi mới châm — nên cái núm vặn phải xoay trước khi có lửa. Que đóm mồi vào than hồng là việc sau rốt."* |
| 3 — **đáp án** | *"Năm bước theo thứ tự: (1) kéo dải vải điều vào, miết hai ngón se thành tim. (2) luồn tim qua cổ đèn. (3) kéo chai dầu hoả, giữ cho tới khi dầu tới vạch trên bầu. (4) xoay núm vặn tim cho đầu tim nhô lên bằng một hạt gạo — vào vùng xanh trên thước. (5) kéo que đóm vào đống than hồng cho bén lửa rồi châm vào đầu tim. Theo số hiệu: **2 – 5 – 1 – 3 – 4**."* |

`[[ Que đóm và than hồng KHÔNG phải vật phẩm túi đồ — chúng là phần tử nội bộ trong khung zoom, đúng với danh sách item của SPINE, không phát sinh item_id mới. ]]`

`[[ item_den_dau BIẾN MẤT khỏi túi khi giải xong và được thay bằng item_den_dau_sang. Đây là biến đổi hợp lệ, không phải mất mát. ]]`

### 3.4.6. Jumpscare — `scare_mat_duoi_day_gieng`

| Trường | Giá trị |
|---|---|
| `trigger_type` | `ON_PUZZLE_FAIL_COUNT` · `max_fails: 3` trên `puz_thap_lai_den_dau` · delay **600 ms** · tối đa 2 lần/chương |
| Loại | **Impulse scare** · `screen_flash: true` · envelope **1000 ms** (ngắn hơn trần — sức mạnh nằm ở **bóng tối sau nó**) |
| `audio_asset` | `sfx_scare_mat_gieng.ogg` · `sprite_animation`: `anim_mat_trang_ngoai_cua_bep` |

**Mô tả (SPINE):** ghép đèn sai, que đóm loé lửa một giây — **trong quầng sáng chớp đó, một khuôn mặt trắng bệch úp sát cửa bếp nhìn vào**, rồi tất cả tối sầm cùng tiếng nước dội dưới giếng.

| Mốc | Sprite | Camera | Ánh sáng | Âm thanh | Haptic |
|---|---|---|---|---|---|
| **−6000 ms** | Không đổi | Tĩnh | Than trong bếp lụi thêm một nhịp | `tell_tom_gieng_gan.ogg` — tiếng "tõm" **đổi chu kỳ từ 9–11 s xuống 4 s**, pan dịch từ 0.7 phải về 0.2 phải (nghe như **giếng đang lại gần**), −32 dBFS | — |
| **−2000 → −1 ms** | Tay người chơi đưa que đóm về phía tim đèn | Tĩnh | Tối gần như hoàn toàn | **IM LẶNG TUYỆT ĐỐI.** Cả than nổ cũng tắt | — |
| **0 ms** | Que đóm **bén lửa** — `spr_dom_loe`, quầng sáng bán kính 420 px quanh `(760, 640)` | Không punch ở 0 ms | **FLASH** `#FFE9C4` (vàng nến, **không phải trắng**), alpha 0 → **0.28**, ramp 50 ms, một xung | `fol_dom_boc_lua` + transient, đỉnh **−5 dBTP** | `hap_thump_single` 40 ms, 0.75 |
| **80 ms** | **Trong quầng sáng**: `spr_mat_trang_ngoai_cua` — một khuôn mặt trắng bệch **áp sát cửa liếp**, cách khung 1,2 m, **không chuyển động, không há miệng, mắt mở bình thường** | Punch-in **+9 %** hướng về cửa liếp `(1480, 430)` trong 120 ms | Flash đỉnh 0.28 | Đỉnh stinger | — |
| **200 ms** | Khuôn mặt vẫn **bất động**. Quầng sáng co lại | Shake **10 px** dọc, 8 Hz | Flash 0.28 → 0.05; quầng đóm thu về 260 px | Tiếng tim đèn xèo | `hap_tap_light` |
| **600 ms** | **Lửa tắt.** Màn hình **tối sầm hoàn toàn** trong 90 ms. Khuôn mặt biến mất cùng ánh sáng — **không hề thấy nó rời đi** | Nhả về 100 %, shake tắt | Về độ sáng nền ≈ 4 % luminance | `fol_nuoc_tom_gieng` **một tiếng duy nhất, rất to** (−8 dBFS) ở 640 ms — nghe như có vật lớn rơi xuống giếng | `hap_thump_single` 40 ms, 0.50 đồng bộ tiếng nước |
| **1000 ms** | **Envelope kết thúc** | Tĩnh | Tối | Recovery: **20 giây im lặng gần tuyệt đối** (−48 dBFS) rồi than nổ trở lại. Tiếng "tõm" trở về chu kỳ 9–11 s như chưa có gì | — |

**Vì sao đặt ở đây:** (a) đây là khu vực tối nhất chương — cú dọa gần như miễn phí về dàn cảnh, nên nó **buộc phải có lý do diegetic**. (b) Lý do đó là: **người chơi tự tạo ra ánh sáng dọa chính mình.** Bước sai duy nhất tạo ra ánh sáng là *"mồi lửa khi tim chưa ngấm dầu → que đóm loé một giây rồi tắt"*; cú dọa **trùng khít** với một giây ánh sáng đó. (c) Vì thế `screen_flash: true` được biện minh hoàn toàn bằng diegetic — **trường hợp flash "sạch" nhất trong tám cú**. (d) Chức năng cân bằng: P5 có **nhiều bước tuần tự nhất**; một cú dọa ở lần sai thứ 3 tái nạp adrenaline và đẩy người chơi **đọc lại vách bếp** — nơi có clue.

### 3.4.7. Beat B11 — soi giếng: CỐ Ý KHÔNG CÓ JUMPSCARE

> **Đây là quyết định thiết kế quan trọng nhất của toàn bộ nhịp kinh dị chương.**

Giếng + đèn dầu + bóng tối + một chiếc guốc trẻ con = mọi người chơi Việt Nam (và mọi người chơi từng xem phim Nhật) đều **biết chắc** có thứ gì sắp trèo lên. Danh sách cấm của dự án đã **cấm tuyệt đối** mô-típ ma tóc dài trèo khỏi giếng.

Chúng ta khai thác chính sự chờ đợi ấy:

| Cơ chế | Chi tiết |
|---|---|
| Mức căng | Tự leo lên **9/10** mà **không tiêu tốn một cú dọa nào** — nó được trả bằng ba mươi năm phim ảnh nằm sẵn trong đầu người chơi |
| Nội dung dưới đáy giếng | Chỉ có **một chiếc guốc mắc gờ gạch**, và **một quầng sáng thứ hai** phản chiếu dưới mặt nước — nhưng người chơi chỉ cầm **một** cây đèn |
| Âm thanh | `fol_nuoc_tom_gieng` **ngừng hẳn** khi người chơi soi xuống (**silence tell không bao giờ được giải quyết**). Giữ im **7 giây**. Không có gì xảy ra. Rồi ambience trở lại |
| Hiệu ứng tâm lý | Người chơi **tự dọa mình** trong 7 giây; khi không có gì xảy ra, họ không thấy nhẹ nhõm — họ thấy **bị lừa bởi chính mình**, và từ đó **không còn tin vào sự im lặng** ở nửa sau chương. Đây chính xác là trạng thái ta cần trước khi lên gác xép |

> **Nguyên tắc rút ra: cú dọa mạnh nhất chương là cú dọa ta quyết định không bắn.**

### 3.4.8. Mục tiêu người chơi

| Cấp | Mục tiêu |
|---|---|
| Bề mặt | **Có ánh sáng.** Cả khu vực này người chơi chỉ nghĩ đúng một việc: *thắp cái đèn lên* |
| Cơ học | Nhặt `item_chai_dau_hoa` → giải `puz_thap_lai_den_dau` → nhận `item_den_dau_sang` → `USE_ITEM` lên `hs_gieng_khoi` → đủ điều kiện lên `area_gac_xep` |
| Cảm xúc | Từ "chuyện này có thật" sang "**chuyện này là chuyện của tôi**" |

### 3.4.9. Khu vực này đẩy cốt truyện tiến lên thế nào

1. **Đổi quy mô của tội ác.** Ba khu đầu, người chơi nghĩ đây là chuyện của một nhà. Cột bếp năm vạch và chữ trên thành giếng cho biết đây là **một tập tục có niên đại, có số lượng, có sổ sách**. Từ một bi kịch thành một **thiết chế**.
2. **Đưa nạn nhân trước lên hình.** Chiếc guốc trẻ con là hình ảnh đắt nhất khu vực — không máu, không mặt ma, chỉ một chiếc guốc mục mắc ở gờ gạch. Nó làm những cái tên trên sổ ở Khu 5 **có trọng lượng trước khi người chơi kịp đọc chúng**.
3. **Cắm mũi dao vào người chơi.** Sổ chợ + phiếu đo là **lần đầu tiên bằng chứng chỉ thẳng vào thân thể người chơi**. Không còn là "ai đó trong nhà này", mà là "**số đo của tôi**".
4. **Đưa vạch thứ năm để trống.** Bốn lễ đã xong có năm. Lễ thứ năm chưa có năm — người chơi hiểu rằng **nó đang diễn ra**. Áp lực thời gian tâm lý bắt đầu từ đây, dù game không có đồng hồ đếm ngược.
5. **Trao chìa khóa cuối.** Đèn sáng = điều kiện lên gác. Ánh sáng, thứ người chơi tưởng là cứu cánh, hóa ra là **phần lễ thứ năm: soi đường cho người dưới ấy nhìn rõ mặt người thế mạng**.

---

## 3.5. KHU VỰC 5 — `area_gac_xep` · "Gác xép thờ Bà Cô"

| Trường | Giá trị |
|---|---|
| Thứ tự | **5** |
| Gate vào | **Có `item_den_dau_sang`** (soi cầu thang gỗ mọt) **VÀ** **đã tra `item_bai_vi_khuyet_danh` vào `hs_khe_mong_cua_gac`** làm then (`flag_then_gac_da_tra`) |
| `background_asset_url` | `https://cdn.linhanthon.game/assets/bg_gac_xep.bundle` |
| Thời lượng | 10–12 phút |
| Câu đố | `puz_xep_anh_gia_pha` |
| Jumpscare | `scare_hinh_nhan_chan_loi` · `scare_anh_tho_thieu_mat` *(phái sinh)* · `scare_ao_cuoi_quay_dau` |
| Đặc thù | **Khu vực nặng nhất về asset** → preload từ lúc người chơi bước vào `area_bep_gieng` |

### 3.5.1. Không khí

**19 giờ 40.** Gác xép gỗ thấp, **không đứng thẳng người được** — camera hạ xuống, khung hình **bị ép dẹt theo chiều dọc**, mép trên khung là đòn tay và mái ngói. Cảm giác **bị nén**.

Nóng và ngột. Bụi giấy lơ lửng, thấy rõ trong luồng sáng đèn dầu. **Mùi:** hồ dán nấu bằng bột gạo (mùi chua nhẹ đặc trưng của hàng mã), giấy bản, nan tre tươi, và mùi gỗ mọt.

**Ánh sáng:** nguồn sáng duy nhất là cây đèn dầu **trong tay người chơi**. Toàn khu vực dùng **ánh sáng động theo con trỏ** — quầng đèn bán kính ~520 px bám theo ngón tay; **ngoài quầng là nâu tối (alpha 0.94), không đen tuyền**, để mắt người chơi luôn cố nhìn ra thứ gì đó.

**Âm thanh:** ván sàn kêu dưới mỗi bước; **giấy sột soạt khi không có gió** (chi tiết then chốt); và — chỉ một lần, ở phút thứ 3 — tiếng **nan tre cọ vào nhau**, rất khẽ, **từ phía sau lưng người chơi**. Drone `drn_gac_xep_ep`: chật, nóng, băng hẹp 120–800 Hz, **cắt sạch trên 2 kHz** để tạo cảm giác trần thấp đè xuống.

| Lớp | Nội dung |
|---|---|
| BACKGROUND | Mái ngói âm dương nhìn từ dưới lên, xà gồ gỗ thấp tè, mạng nhện dày, một khe sáng mảnh hắt lên từ sàn |
| MIDGROUND | **Hình nhân thế mạng** bằng nan tre dán giấy đứng chính giữa (cao gần bằng người thật), khung ảnh thờ chín mảnh bên phải, bộ áo cưới giấy treo trên móc sát vách phải, chồng vàng mã góc phải |
| FOREGROUND | Hòm gỗ nắp mở (trái-dưới), cuốn sổ ghi tên và tập nhật ký trên nắp hòm, **chiếu cói mới tinh** trải sát mép dưới khung hình, ván sàn hở khe |
| FX | Bụi bay dày trong quầng sáng; giấy vàng mã sột soạt khi camera nhích |

### 3.5.2. Khung hình mở

**Đèn tắt phụt vì gió lùa ngay khi vừa nhô đầu lên sàn gác** (`scare_hinh_nhan_chan_loi`). Đèn cháy lại — và **hình nhân thế mạng đã đứng chắn ngay trước mặt, cách chưa đầy một gang tay**.

Hình nhân đan bằng nan tre, dán giấy bản, **cao đúng tầm người chơi**. Mặt vẽ bằng than: hai chấm mắt, một vạch miệng. **Mặt nó quay vào phía trong nhà** — **phạm điều Sáu**, và điều Sáu đã bị phạm từ trước khi người chơi tới.

Sau khi tim người chơi đập lại bình thường, quầng đèn quét được cả gác:
- Một **hòm gỗ** to, nắp mở ngửa, **khóa đã bị gỡ sẵn** — bà nội giấu chìa hai mươi năm, ai đó đã tìm ra.
- **Chồng vàng mã** cao ngang ngực: ngựa giấy, mũ giấy, tiền âm phủ, một cái nhà giấy ba gian có cả sân gạch — **tất cả mới nguyên, hồ dán chưa khô hẳn**.
- Một **khung ảnh lớn úp mặt vào tường**, mặt sau là ván gỗ chia ô.
- Một **chiếc chiếu cói trải sẵn** giữa sàn — chiếu mới, chưa ai nằm, bốn góc chặn bốn đồng xu.
- Một cuốn **sổ bìa giấy xi măng** đặt trên nắp hòm, có chặn một hòn gạch cho khỏi lật.

### 3.5.3. Bảng hotspot (11 hotspot)

| # | id | bounds {x, y, w, h} | action_type | Tham số | Vai trò kịch bản |
|---|---|---|---|---|---|
| 1 | `hs_khe_van_san` | `{x:250, y:120, width:300, height:150}` | `DIALOGUE` | `txt_thoai_khe_van_san` | **Cảnh báo point-of-no-return** — giọng bà nội gọi vọng lên |
| 2 | `hs_nhat_ky_trang_cuoi` | `{x:600, y:170, width:200, height:160}` | `EXAMINE` | `txt_examine_nhat_ky_1996` | Hai trang 1976 và 1996, cùng một nét chữ |
| 3 | `hs_xuong_gian_tho` | `{x:60, y:200, width:170, height:380}` | `CHANGE_AREA` | `target_area_id: area_gian_tho` · **không gate cho tới khi `flag_ao_cuoi_da_nhat = true`, sau đó khoá vĩnh viễn** · `txt_khoa_gac_xep_sap_cua` | **Điểm không-quay-lại duy nhất của chương** |
| 4 | `hs_ao_cuoi_giay` | `{x:1650, y:200, width:230, height:370}` | `COLLECT_ITEM` | `item_id: item_ao_cuoi_giay` · `required_item: null` | **Chỉ hiện sau khi giải P6** |
| 5 | `hs_hinh_nhan` | `{x:820, y:280, width:290, height:620}` | `USE_ITEM` | `required_item: item_ao_cuoi_giay` · `item_id: item_ao_cuoi_giay` · fallback `txt_khoa_hinh_nhan_chua_co_ao` | **HÀNH ĐỘNG KẾT CHƯƠNG — phần lễ thứ VII** |
| 6 | `hs_so_ghi_ten` | `{x:270, y:300, width:280, height:170}` | `EXAMINE` | `txt_examine_so_ghi_ten` | **Mũi neo twist C1** — bốn đời người thế mạng |
| 7 | `hs_khung_anh_tho` | `{x:1200, y:330, width:400, height:400}` | `ZOOM_PUZZLE` | `target_puzzle_id: puz_xep_anh_gia_pha` · fallback `txt_khoa_gac_xep_toi_qua` | **Câu đố P6** |
| 8 | `hs_hom_go_nap` | `{x:250, y:600, width:420, height:290}` | `EXAMINE` | `txt_examine_nap_hom` | **Hai trang**: gia phả (clue C1 của P6) + **BẢY ĐIỀU CẤM KỴ** |
| 9 | `hs_vang_ma_chong` | `{x:1640, y:620, width:240, height:340}` | `EXAMINE` | `txt_examine_vang_ma` | Đủ một bộ tiễn người, sắm sẵn **từ trước khi bà nội mất** |
| 10 | `hs_giay_khai_sinh` | `{x:1200, y:790, width:280, height:150}` | `EXAMINE` | `txt_examine_giay_khai_sinh` | Khai sinh gốc + dấu **ĐÃ KHAI TỬ** |
| 11 | `hs_chieu_coi_trai_san` | `{x:730, y:910, width:440, height:88}` | `EXAMINE` | `txt_examine_chieu_moi` | Chiếu trải sẵn cho hình nhân — mà hình nhân cao bằng người chơi |

**Tự kiểm tra bố cục:** 11 hotspot · 55 cặp · **0 giao nhau** · `y_min = 120` ✓ · `y_max = 998` ✓ · nhỏ nhất `hs_chieu_coi_trai_san` 440×**88** — **đúng bằng ngưỡng tối thiểu, không được rút thêm**.

⚠️ Cặp sát nhau nhất: `hs_hinh_nhan` (kết thúc y = 900) và `hs_chieu_coi_trai_san` (bắt đầu y = 910) — **cách 10 px theo trục y**, dưới ngưỡng đệm 20 px. **Chấp nhận** vì chiếu nằm dưới chân hình nhân là bố cục bắt buộc về mặt kể chuyện, và hai hotspot có phản hồi hoàn toàn khác nhau (một cái là hành động kết chương có xác nhận 2 bước, một cái chỉ đọc chữ). *Quy tắc kỹ thuật "không overlap" vẫn đạt.*

**Nguyên tắc đọc cảnh:** **cột trái = bằng chứng giấy tờ** (sổ, nhật ký, hòm, gia phả) · **cột giữa = hình nhân** (chỗ hành động) · **cột phải = đồ nghi lễ** (khung ảnh, áo cưới, vàng mã). Quầng đèn dầu bắt người chơi **quét màn hình từ trái sang phải — đúng thứ tự mà cú twist cần được đọc**.

### 3.5.4. Văn bản đọc được (thành phẩm)

**① SỔ GHI TÊN** — sổ bìa giấy xi măng, chia cột kẻ tay bằng thước, hai nét chữ khác nhau (`hw_ong_tu` cho bốn dòng đầu, `hw_ba_noi` cho phần ghi chú).

> **`txt_examine_so_ghi_ten`**
>
> **SỔ GHI TÊN — nhà thờ họ Nguyễn, thôn Linh An**
> *Phép thế mệnh. Chớ để người ngoài xem.*
>
> | Năm | Tên chữ | Tên tục | Tuổi | Kết quả |
> |---|---|---|---|---|
> | Quý Tỵ 1953 | Nguyễn Thị Gái | cái Gái | 17 | *Không phải người thế. Là **người nhận**.* |
> | Tân Sửu 1961 | Nguyễn Thị Nhài | cái Đĩ | 8 | **Lễ thành.** |
> | Mậu Thân 1968 | Nguyễn Văn Tý | thằng Cu | 5 | **Lễ thành.** Guốc còn dưới giếng, không vớt. |
> | Bính Thìn 1976 | **Nguyễn Thị Liên** | **cái Đĩ Con** | 7 | **LỄ CHƯA THÀNH.** |
>
> *(Phần ghi chú dưới dòng thứ tư, chữ run nghiêng trái:)*
>
> Đã xóa tên khỏi gia phả — xong.
> Đã cạo mặt khỏi ảnh thờ — xong.
> Đã khắc bài vị khuyết danh — xong.
> Đã làm giấy khai tử, số 41/KT — xong.
>
> **Còn thiếu một việc.**
>
> Cái áo vẫn treo trên gác. Tôi không đốt được, đốt là thành lễ. Tôi cũng không giấu đi được, giấu là nó tìm.
> Tôi để đấy. Tôi chết thì ai nhặt lên người ấy chịu.
> **Miễn đừng là con bé.**

> **`txt_gac_xep_so_ghi_ten_doc_thoai`**
> "Nguyễn Thị Liên.
> *(Mình đọc thành tiếng. Mình không định đọc thành tiếng.)*
> Bảy tuổi. Năm bảy mươi sáu.
> Mình sinh năm sáu mươi chín.
> Năm bảy mươi sáu mình lên bảy."

`[[ HẬU QUẢ PHẠM ĐIỀU MỘT: ngay sau dòng độc thoại này, đúng 6 giây, hình nhân thế mạng XOAY 30 ĐỘ về phía người chơi. Không âm thanh. Không flash. Nếu người chơi không quay lại nhìn, nó cứ thế mà đứng. Âm thanh: hạ toàn bộ nền xuống −42 dBFS và giữ im 4 giây sau câu cuối. ]]`

`[[ flag_da_doc_so_ghi_ten = true → mở nhánh độc thoại đối chiếu nét chữ với item_ban_rap_chu_the: "Nét chữ này... giống hệt nét chữ trên bản rập chữ 'Thế Mệnh' đang cầm trong tay." Đây là clue C4 của P6. ]]`

**② MẶT TRONG NẮP HÒM — TRANG 1: SƠ ĐỒ NGÔI THỨ** *(lời giải của `puz_xep_anh_gia_pha`)*

> **`txt_examine_nap_hom`** *(trang 1 — mực tàu viết thẳng lên gỗ)*
>
> **ẢNH THỜ — XẾP THEO NGÔI THỨ, CHỚ ĐẢO**
>
> *Hàng trên:* **cụ tổ ở giữa, ông bên tả, bà bên hữu.**
> *Hàng giữa* — các con: **cả (trưởng), thứ, rồi út**; út là em gái, mất năm mười bảy tuổi.
> *Hàng dưới* — các cháu, **kể theo tuổi từ lớn xuống bé**: ~~[một tên đã bị gạch nát, chỉ còn đọc được chữ đệm "Thị"]~~ …
>
> Ảnh xếp sai ngôi thứ thì người trong ảnh **không ngồi yên**.

**③ MẶT TRONG NẮP HÒM — TRANG 2: BẢY ĐIỀU CẤM KỴ**

Xem văn bản thành phẩm đầy đủ ở **mục 2.3.6**, `text_key` = `txt_examine_nap_hom` (trang 2).

`[[ flag_da_doc_bay_dieu_cam_ky = true → cutscene kết chương thêm một nhịp "Điều thứ bảy..." trước khi khoác áo. Cờ này KHÔNG đổi kết cục Chapter 1, nhưng Chapter 2 dùng nó để đổi một nhánh thoại với bà Tơ: nếu người chơi ĐÃ đọc Bảy Điều, bà Tơ nói "vậy là cháu biết rồi mà cháu vẫn khoác" — nặng hơn nhiều so với nhánh còn lại. ]]`

**④ TRANG NHẬT KÝ 1976** — trang rời, kẹp giữa sổ ghi tên và nắp hòm.

> **`txt_gac_xep_nhat_ky_1976`**
>
> *Ngày hai mươi tháng Chạp năm Bính Thìn.*
>
> Tôi bế nó ra giếng. Trời rét, nó mặc cái áo bông vá vai, chân đi guốc.
>
> Ông từ đã đọc xong văn. Nhang cháy đều. Đèn đủ đôi. Vàng đã hóa. Mọi việc đúng phép, không sai một bước nào.
>
> Chỉ còn khoác áo.
>
> Tôi cầm cái áo giấy lên. Nó ngẩng đầu nhìn tôi, nó gọi: **bà ơi.**
>
> Tôi buông tay. Áo rơi xuống chiếu.
>
> Ông từ đứng dậy, ông bảo tôi: *lễ dở dang còn độc hơn lễ không làm.* Ông bảo bà cứ liệu, cả làng gánh chứ không riêng nhà bà.
>
> Tôi biết. Tôi biết cả rồi.
>
> Nhưng tôi không làm được.
>
> Sáng hôm sau tôi gửi nó lên Hà Nội cho dì nó, đổi khai sinh sang họ Trần, đặt lại tên là Hương. Tôi bảo với làng là nó chết rồi. Tôi ra ủy ban làm giấy. Tôi để tang nó ba năm.
>
> **Từ hôm ấy tôi không dám gọi tên nó nữa.**

**⑤ TRANG NHẬT KÝ 1996** — trang cuối cùng, chữ run đến mức có chỗ trượt khỏi dòng.

> **`txt_examine_nhat_ky_1996`**
>
> *Ngày mồng ba tháng Bảy năm Bính Tý.*
>
> Tôi yếu rồi. Nằm không dậy được nữa.
>
> Bà Tơ sang. Bà ấy ngồi ở chõng ngoài hiên, nhai trầu, bảo tôi:
> *— Lễ dở thì người dở. Bà đi rồi thì ai gánh?*
>
> Tôi bảo để tôi mang xuống. Tôi chết thì tôi mang cái nợ ấy xuống theo.
>
> Bà Tơ cười. Bà ấy bảo: *không mang được đâu. Cái áo nó vẫn treo trên gác. Nó vẫn đợi. **Áo đợi người, chứ có đợi bà đâu.***
>
> Rồi bà ấy hỏi địa chỉ con bé ở Hà Nội. Tôi không nói.
>
> Nhưng cái địa chỉ ấy tôi ghi ở sau ảnh thờ, ghi từ năm bảy chín, ghi để nhỡ tôi quên.
>
> Bà Tơ có mắt.
>
> Nếu con Liên nó về — ai đó làm ơn, **đừng để nó lên gác.**

**⑥ GIẤY KHAI SINH CŨ** — bản gốc, giấy mỏng, có dấu đỏ, gấp tư, kẹp trong lần lót đáy hòm.

> **`txt_examine_giay_khai_sinh`**
>
> **VIỆT NAM DÂN CHỦ CỘNG HÒA**
> *Độc lập — Tự do — Hạnh phúc*
>
> **GIẤY KHAI SINH** — Số: 118
>
> Họ và tên: **NGUYỄN THỊ LIÊN**
> Sinh ngày 16 tháng 9 năm 1969
> Nơi sinh: thôn Linh An, xã Linh Nam, huyện Thuận Thành
> Cha: Nguyễn Văn Đoan · Mẹ: Phạm Thị Vân
>
> *(Đóng chéo lên toàn bộ tờ giấy, mực đỏ đã bợt:)*
> **ĐÃ KHAI TỬ — SỐ 41/KT — NGÀY 22.12.1976**

> **`txt_gac_xep_khai_sinh_doc_thoai`**
> "Ngày hai mươi hai tháng Chạp năm bảy sáu.
> Hôm ấy mình đang ngồi trên tàu lên Hà Nội với dì Tư. Mình nhớ mỗi cái ghế gỗ lạnh và mùi than tổ ong ở ga Hàng Cỏ.
> Trong lúc mình đang đi, ở đây người ta đã làm xong giấy tờ cho mình **chết**."

**⑦ BỨC ẢNH SAU KHI XẾP XONG** — độc thoại tự động khi hoàn thành P6. **Beat B13.**

> **`txt_gac_xep_anh_hoan_chinh`**
> "Chín mảnh khớp vào nhau. Bức ảnh thờ chụp cả nhà, năm bảy nhăm, trước hiên, đứng theo đúng ngôi thứ.
>
> Hàng trên: ông, cụ tổ, bà.
> Hàng giữa: bác cả, bố, cô út.
> Hàng dưới: ba đứa cháu.
>
> Đứa đứng cuối hàng dưới **không có mặt**.
>
> Không phải mờ, không phải mất nét. Có người lấy dao nhỏ **khoét đúng khuôn mặt ấy ra khỏi tấm ảnh**, khoét sát, đến tận chân tóc, để lại một lỗ hình bầu dục.
>
> Thân người thì vẫn còn. **Áo bông vá vai. Chân đi guốc.**
>
> Mình nhìn cái áo bông ấy lâu hơn mình muốn."

**⑧ MẶT SAU KHUNG ẢNH** — hiện cùng lúc với `item_ao_cuoi_giay`. **Beat B13a.**

> **`txt_gac_xep_sau_khung_anh`**
> *(Sau lưng khung ảnh, có ai đó viết bằng bút chì, nét đã mờ:)*
>
> **Trần Thị Hương — 47 Hàng Chỉ, Hà Nội — nhà dì Tư, gác hai.**
> *Ghi phòng khi tôi lẫn. Không được đưa cho ai. N.T.N. 1979.*
>
> *(Bên dưới, nét chữ khác hẳn, mực mới, viết đè lên:)*
> **Đã gửi giấy báo. 14.8.1996.**

`[[ Âm thanh: một nốt drn_gac_xep_ep LÊN NỬA CUNG — thay đổi cao độ duy nhất trong cả chương. ]]`

**⑨ ÁO CƯỚI GIẤY** — độc thoại khi nhận `item_ao_cuoi_giay`.

> **`txt_gac_xep_ao_cuoi_giay`**
> "Áo cưới bằng giấy. Giấy bản nhuộm điều, gấp nếp, khâu bằng chỉ gai, cổ áo viền giấy trang kim đã xỉn.
> Khổ người lớn. Tay áo dài, thân dài.
> Treo hai mươi năm trên gác mà giấy chưa mủn — **có người thay giấy**.
>
> Mình giơ nó lên ướm.
>
> Vai vừa. Tay vừa. Thân vừa.
> **Vừa in.**"

> *(Nhánh thay thế nếu `flag_da_doc_phieu_do = true`:)* "…Gấu áo có ghi mấy con số bằng bút chì. **Số đo này… mình đã thấy nó rồi.**"

**⑩ CHIẾU CÓI TRẢI SẴN**

> **`txt_examine_chieu_moi`**
> "Chiếu cói mới tinh, còn mùi cói, viền chưa tướp, bốn góc chặn bốn đồng xu. Sạch không một hạt bụi, giữa cái gác xép dày bụi này.
> Theo lệ, lễ xong thì đặt hình nhân nằm xuống chiếu, phủ vải, để đấy ba ngày.
> Chiếu này trải cho hình nhân.
> **Mà hình nhân thì cao bằng mình.**"

**⑪ HÌNH NHÂN** — fallback khi chưa có áo.

> **`txt_khoa_hinh_nhan_chua_co_ao`**
> "Nan tre chẻ mỏng, uốn thành khung người, dán giấy bản, hồ nấu bằng bột gạo.
> Mặt vẽ bằng than: hai chấm, một vạch.
> Cao một thước năm mươi hai. Vòng ngực, nếu đo, chắc tám mươi hai.
> Thân nó trống trơn — chưa có gì khoác lên.
>
> Nó không có tên. Cũng như cái bài vị dưới nhà không có tên.
> Trong nhà này chỉ có đúng ba thứ không tên: cái bài vị, cái hình nhân, và **tôi**.
>
> *(Điều cấm kỵ thứ bảy: không ai được tự tay khoác áo lên hình nhân.)*"

**⑫ VÀNG MÃ**

> **`txt_examine_vang_ma`**
> "Vàng mã chất tới trần: ngựa giấy, mũ áo giấy, một cái nhà giấy ba gian có cả sân gạch.
> Tất cả **mới nguyên**, hồ dán chưa khô hẳn. Đủ một bộ tiễn người — và người ta đã sắm sẵn **từ trước khi bà nội mất**."

**⑬ KHE VÁN SÀN** — node `DIALOGUE`. **Đây là cảnh báo point-of-no-return duy nhất.**

> **`txt_thoai_khe_van_san`**
> *(Cúi xuống khe ván sàn, nhìn thẳng vào gian thờ bên dưới.)*
> Bàn thờ vẫn sáng đèn. Và có tiếng bà nội gọi vọng lên, rõ từng chữ như đang đứng ngay sau lưng:
> *"Cháu ơi. Xuống đi. Xuống bây giờ thì còn kịp."*
>
> *(Chọn: **[Đáp lại]** → "Bà ơi, con tìm ra rồi." / **[Không đáp, quay đi]**. Dù chọn gì, nhìn xuống lần nữa thì gian thờ **tối om** — mà đèn dầu trong tay vẫn cháy.)*

`[[ Chọn [Đáp lại] → flag_da_dap_loi_ba_noi = true → VI PHẠM ĐIỀU CẤM KỴ THỨ TƯ (chớ đáp lời ai gọi từ sau lưng). Không phạt ở Chương 1; ghi nhận cho Chapter 2. ]]`

**⑭ GÁC XÉP KHI CHƯA CÓ ĐÈN / CỬA GÁC ĐÃ SẬP** — fallback.

> **`txt_khoa_gac_xep_toi_qua`**
> "Tối quá, không nhìn ra cái gì cả. Chỉ sờ thấy mặt gỗ nhám và mấy đường rãnh chạy dọc chạy ngang. Phải có đèn."

> **`txt_khoa_gac_xep_sap_cua`**
> "Cửa gác đã sập xuống, then gỗ cài từ bên dưới. Từ đây chỉ còn một đường: **quay lại phía hình nhân**."

### 3.5.5. Câu đố — `puz_xep_anh_gia_pha`

| Trường | Giá trị |
|---|---|
| Type | `SLIDING_TILE` · Tên hiển thị: **"Bức ảnh thờ chín mảnh"** |
| `solution` | **`[2, 5, 7, 4, 8, 3, 6, 1, 0]`** — đọc **row-major** (hàng ngang, trái→phải, trên→dưới). `0` = **ô trống** |
| `reward_item_id` | `item_ao_cuoi_giay` |
| `wrong_action_jumpscare` | `scare_anh_tho_thieu_mat` *(phái sinh — nếu Lead không duyệt thì `null`)* |
| Độ khó / thời gian kỳ vọng | **4/5** · 240 giây (P25 = 160 s, P75 = 420 s) — **câu đố dài nhất chương** |
| Điều kiện mở khoá | **Bắt buộc có `item_den_dau_sang`** (gác xép tối hoàn toàn) |

**Cơ chế:** chạm `hs_khung_anh_tho` → lật mặt sau khung ảnh, lộ **khung gỗ 3×3**, khung zoom `{x:660, y:120, width:840, height:840}`; mỗi ô **280×280 px** (thoải mái cho ngón tay). **8 mảnh ván + 1 ô trống.** Thao tác: **chạm vào mảnh nằm cạnh ô trống** để nó trượt vào, **hoặc vuốt mảnh về phía ô trống**; hỗ trợ **trượt cả hàng/cột** (vuốt mạnh thì 2–3 mảnh cùng dồn).

Nút **"Áp ảnh vào khung"** `{x:1560, y:860, width:280, height:140}`: người chơi tự xác nhận khi cho là đã xếp xong. Đây cũng là **cơ chế đếm lần sai**.

Nút **"Lật mảnh"**: lật xem mặt sau một mảnh, **không tốn lượt, không tính sai** — nguồn clue C2.

> **⚠️ RÀNG BUỘC KỸ THUẬT BẮT BUỘC (gửi Data Architect & Dev):** trạng thái xáo trộn ban đầu **PHẢI** được sinh bằng cách **áp 60–80 nước đi hợp lệ ngẫu nhiên từ trạng thái đã giải**, tuyệt đối **không** hoán vị ngẫu nhiên tự do — nếu không sẽ có **50 % khả năng rơi vào cấu hình không giải được** (bất biến chẵn-lẻ của bài toán 15-puzzle). Thêm ràng buộc: trạng thái sinh ra phải cách đích **≥ 18 nước** để không quá dễ.

**Bảng ánh xạ ID phần tử** *(cố định theo thứ tự chín mảnh ván nằm chồng trong hòm gỗ lúc người chơi mở ra)*:

| ID mảnh | Nội dung trên mảnh ván |
|---|---|
| 1 | Người chị họ, tóc tết, áo hoa nhí |
| 2 | Ông nội, khăn xếp, tay chống gối |
| 3 | **Bà Cô** — thiếu nữ áo dài trắng, đứng nép ngoài cùng |
| 4 | Bác cả, áo đại cán, đứng thẳng |
| 5 | Di ảnh cụ tổ đặt trên đôn, giữa khung |
| 6 | Người anh họ, quần đùi, cầm cành cau |
| 7 | Bà nội, áo the nâu, ôm cơi trầu |
| 8 | Bố (con thứ), áo sơ mi trắng bỏ trong quần |

**Giải thích từng phần tử của mảng:**

| Ô | Giá trị | Là ai | Vì sao ở đây (theo gia phả chép ở nắp hòm) |
|---|---|---|---|
| 1 (trên-trái) | `2` | **Ông nội** | Hàng trên là hàng ông bà. **Nam tả nữ hữu**: ông bên trái |
| 2 (trên-giữa) | `5` | **Di ảnh cụ tổ** | Bậc cao nhất, luôn đặt chính giữa và cao nhất trong ảnh thờ |
| 3 (trên-phải) | `7` | **Bà nội** | Nữ bên phải, đối xứng với ông nội |
| 4 (giữa-trái) | `4` | **Bác cả** | Hàng giữa là hàng các con, xếp **trưởng – thứ – út** từ trái sang |
| 5 (giữa-giữa) | `8` | **Bố (con thứ)** | Con thứ hai, đứng giữa |
| 6 (giữa-phải) | `3` | **Bà Cô** | Con út, gái, chết trẻ — đứng ngoài cùng bên phải, hơi lùi khỏi khung |
| 7 (dưới-trái) | `6` | **Anh họ** | Hàng dưới là hàng cháu, xếp theo tuổi từ lớn tới bé |
| 8 (dưới-giữa) | `1` | **Chị họ** | Cháu thứ hai |
| 9 (dưới-phải) | `0` | **Ô TRỐNG** | **Cháu út — chính là người chơi.** Khuôn mặt đã bị khoét khỏi bức ảnh. Bức ảnh xếp xong **vẫn khuyết đúng một khuôn mặt**: cú twist của chương |

`[[ LƯU Ý IMPLEMENT — điểm khác biệt quan trọng so với một SLIDING_TILE thông thường: ô trống của trò trượt được lấp bằng mảnh cuối ở nước đi cuối cùng. Giải xong, ảnh đầy đủ chín mảnh trong khung, MÀ VẪN khuyết một khuôn mặt — vì mảnh ở vị trí cháu út là mảnh CÓ THẬT, có thân người, nhưng phần mặt đã bị khoét thủng. ]]`

**Manh mối:**

| # | Clue | Hotspot | Suy ra |
|---|---|---|---|
| C1 | **Gia phả chép trong nắp hòm** *(clue CHÍNH)* | `hs_hom_go_nap` trang 1 | **Toàn bộ quy tắc xếp**: 3 hàng, nam tả nữ hữu, trưởng-thứ-út, cháu theo tuổi. Và **ô trống nằm ở cuối hàng dưới** vì cái tên ở đó đã bị xoá |
| C2 | **Mặt sau mỗi mảnh ván** — chữ Nho ghi vai vế: 祖 (tổ) · 祖父 (ông) · 祖母 (bà) · 伯 (bác) · 父 (bố) · 姑 (cô) · 孫 (cháu trai) · 孫女 (cháu gái), kèm chú thích quốc ngữ bút chì | nút "Lật mảnh" trong khung zoom | **Xác định danh tính từng mảnh** mà không cần đoán qua trang phục — lưới an toàn cho người chơi không đọc được nét vẽ |
| C3 | **Trang gia phả ở gian thờ** | `hs_gia_pha` (Khu 3) | Ngôi thứ hàng giữa và hàng dưới — **thưởng cho người đọc kỹ từ khu vực trước** |
| C4 | **Bản rập chữ "Thế Mệnh"** đối chiếu nét chữ với sổ ghi tên | `item_ban_rap_chu_the` trong túi + `hs_so_ghi_ten` | **Cùng một người viết** → nối bình phong ngoài hiên với cuốn sổ trên gác: hủ tục là việc của cả nhà, có chủ đích |

> **Tự kiểm tra công bằng:** C1 cho đủ quy tắc ngôi thứ; C2 cho đủ danh tính từng mảnh; hai thứ ghép lại xác định **duy nhất** một bố cục. Tất cả nằm trong cùng khu vực, `EXAMINE` không cần vật phẩm, đọc lại không giới hạn. Người chơi **không cần** biết trước tập tục thờ tự ngoài đời.

**Hành vi khi sai.** `SLIDING_TILE` không có "nước đi sai" theo nghĩa thông thường — mọi nước trượt đều hợp lệ. Vì vậy:

> **Một lần sai = một lần ấn nút "Áp ảnh vào khung" trong khi bố cục chưa khớp `solution`.**

| Lần sai | Phản hồi |
|---|---|
| 1 | Khung ảnh **không khít**, một mảnh **bật ra rồi rơi trở lại**. Độc thoại: *"Chưa đúng ngôi thứ. Người ta không đứng lẫn chỗ nhau trong ảnh thờ."* |
| 2 | Như trên + **ngọn đèn dầu chao một nhịp**, quầng sáng thu hẹp. Đồng thời **hai mảnh đang đứng đúng vị trí phát sáng viền vàng nhạt trong 2 giây** rồi tắt (gợi ý động, thưởng cho tiến độ) |
| 3 | **JUMPSCARE `scare_anh_tho_thieu_mat`**. Sau đó `fail_count` reset và **bố cục hiện tại được giữ nguyên** — **không bao giờ xáo lại bàn cờ** (xáo lại là hình phạt tàn nhẫn và làm hỏng tiến độ hợp lệ) |

**Ba mức gợi ý:**

| Tier | Nội dung |
|---|---|
| 1 | *"Đây không phải trò xếp hình cho khớp màu, mà là xếp cho đúng ngôi thứ trong nhà. Nắp cái hòm gỗ bên cạnh có chép gia phả bằng mực tàu — đọc nó trước. Còn muốn biết mảnh nào là ai thì lật mặt sau mảnh ván, có chữ ghi vai vế."* |
| 2 | *"Ba hàng. Hàng trên là ông bà: cụ tổ ở giữa, ông bên trái, bà bên phải — nam tả nữ hữu. Hàng giữa là các con, kể từ trái sang: bác cả trước, đến bố, rồi Bà Cô — em gái út. Hàng dưới là các cháu, lớn trước bé sau. Và cái tên ở cuối hàng cháu đã bị gạch nát trong gia phả — nên chỗ ấy trong ảnh cũng trống."* |
| 3 — **đáp án** | *"Hàng trên: ông nội (mảnh 2) – di ảnh cụ tổ (mảnh 5) – bà nội (mảnh 7). Hàng giữa: bác cả (mảnh 4) – bố (mảnh 8) – Bà Cô áo dài trắng (mảnh 3). Hàng dưới: anh họ (mảnh 6) – chị họ (mảnh 1) – và để trống ô cuối cùng bên phải. Theo số hiệu, đọc từng hàng từ trái sang phải: **2 – 5 – 7 / 4 – 8 – 3 / 6 – 1 – trống**. Xếp xong thì ấn Áp ảnh vào khung."* |

**Chuỗi sau khi giải (không phải câu đố):**

1. Bức ảnh hoàn chỉnh lộ ra, **vẫn khuyết đúng một khuôn mặt** → `txt_gac_xep_anh_hoan_chinh`.
2. Sau lưng khung ảnh treo **bộ áo cưới giấy khổ người lớn** → spawn `hs_ao_cuoi_giay` (`COLLECT_ITEM`, `required_item: null`).
3. Đồng thời lộ ra **mặt sau khung ảnh** với địa chỉ Hà Nội và dòng *"Đã gửi giấy báo. 14.8.1996."*
4. Nhặt áo cưới → `flag_ao_cuoi_da_nhat = true` → **cửa gác kêu rắc một tiếng và sập xuống, `hs_xuong_gian_tho` khoá vĩnh viễn**. **Điểm không-quay-lại.**
5. `USE_ITEM` `item_ao_cuoi_giay` lên `hs_hinh_nhan` → khởi động cutscene kết chương `seq_ending_ch01_khoac_ao`.

### 3.5.6. Jumpscare của khu vực

#### A. `scare_hinh_nhan_chan_loi` — thuộc SPINE · **cú dọa duy nhất KHÔNG THỂ TRÁNH**

| Trường | Giá trị |
|---|---|
| `trigger_type` | `ON_ENTER_AREA` · lần vào **đầu tiên duy nhất** (`seen_scare_hinh_nhan`) · delay **900 ms** sau khi fade-in hoàn tất · **không bao giờ lặp** |
| Loại | **Impulse scare** · `screen_flash: false` · envelope **1200 ms** |
| `audio_asset` | `sfx_scare_hinh_nhan.ogg` · `sprite_animation`: `anim_hinh_nhan_hien_gan` |

| Mốc | Sprite | Camera | Ánh sáng | Âm thanh | Haptic |
|---|---|---|---|---|---|
| **−6000 ms** *(còn trên thang)* | Người chơi đang leo | Camera đi lên theo từng bậc | Quầng đèn 380 px | `tell_nan_tre_dich.ogg` — nan tre cọ nhau **một lần duy nhất**, −34 dBFS, **pan 0.0 (ngay sau lưng), rất gần** | `hap_tap_light` mỗi bậc thang |
| **−2000 → −1 ms** | Đầu người chơi nhô lên khỏi mặt sàn gác. **Gió lùa** làm ngọn lửa đèn nghiêng | Camera dừng, **hạ thấp (ép dẹt khung)** | Quầng đèn **co từ 380 px → 90 px** trong 1100 ms | **IM LẶNG TUYỆT ĐỐI.** Chỉ tiếng lửa đèn chao, rồi tắt ở −400 ms | — |
| **0 ms** | **Đèn tắt phụt.** Màn hình **đen 100 %** | Tĩnh, đen | Luminance ≈ 0 | Tiếng "phụt" của lửa tắt, −14 dBTP. Sau đó **im hoàn toàn 520 ms** | `hap_tap_light` 12 ms — rất nhẹ, báo "có chuyện" |
| **200 ms** | Đen. **Người chơi không thấy gì trong 520 ms — khoảng dài nhất của cả tám cú dọa** | Đen | 0 | Im | — |
| **600 ms** | **Đèn cháy lại** (ramp luminance **180 ms, không xung**). `spr_hinh_nhan_the_mang` **đã đứng sẵn** chắn trước mặt, cách chưa đầy một gang tay — chiếm **68 % chiều cao khung**, mặt than hai chấm một vạch, **mặt quay vào phía trong nhà** | Punch-in **+8 %** trong 100 ms rồi giữ | Quầng đèn mở lại 90 → 300 px trong 180 ms | **Tiếng giấy bản căng** + sub 45 Hz, đỉnh −7 dBTP. **Không có tiếng hét, không stinger kim loại** | `hap_thump_single` 40 ms, 0.85 đồng bộ khung đèn cháy lại |
| **1200 ms** | **Envelope kết thúc.** Hình nhân **KHÔNG biến mất** — nó là vật thể có thật, nó ở đó suốt phần còn lại của chương, và người chơi sẽ phải **đi vòng qua nó** | Nhả về 100 % | Quầng đèn ổn định | Recovery 20 s; `amb_gac_xep_bui_giay` + `drn_gac_xep_ep` vào | — |

> **Ghi chú đạo diễn:** 520 ms bóng tối hoàn toàn ở giữa envelope là thiết kế đắt nhất của cú này. Trong 520 ms ấy người chơi **không bị tấn công** — họ chỉ **bị bỏ lại**. Cú dọa thật sự không phải là hình nhân; cú dọa là **nửa giây mù**.

**Vì sao đây là ngoại lệ duy nhất của nguyên tắc "người chơi phải tự bấm":** hình nhân thế mạng **bắt buộc phải được giới thiệu bằng thân thể** trước khi cảnh kết chương dùng nó. Nếu người chơi có thể bỏ lỡ hình nhân, cú twist mất một nửa sức nặng. Bù lại: người chơi vừa mất 20–30 giây leo thang gỗ mọt, **mỗi bậc một tiếng do chính họ bấm** — nghĩa là họ **tự đặt nhịp** cho cú dọa, họ đến với nó ở đúng tốc độ mà họ chọn. **Không flash** vì cấu trúc ánh sáng của cú này đã là **tối → sáng**; thêm flash trắng lên trên sẽ vừa thừa vừa nguy hiểm về nhạy sáng.

#### B. `scare_anh_tho_thieu_mat` — *(phái sinh, chờ Lead duyệt)*

| Trường | Giá trị |
|---|---|
| `trigger_type` | `ON_PUZZLE_FAIL_COUNT` · `max_fails: 3` trên `puz_xep_anh_gia_pha` · delay **500 ms** · tối đa 2 lần/chương |
| Loại | **Impulse scare** · `screen_flash: true` (màu đèn dầu `#FFD9A0`, không phải trắng) · envelope **1200 ms** |
| `audio_asset` | `sfx_scare_van_anh_lat.ogg` · `sprite_animation`: `anim_chin_manh_van_lat_up` |

| Mốc | Sprite | Camera | Ánh sáng | Âm thanh | Haptic |
|---|---|---|---|---|---|
| **−5000 ms** | Chín mảnh ván **kêu rất khẽ** khi trượt, như đang ép vào nhau | Tĩnh | Đèn ổn định | `tell_van_go_ep_nhau.ogg`, −33 dBFS | — |
| **−2000 → −1 ms** | Người chơi ấn nút *Áp ảnh vào khung* | Tĩnh | Đèn ổn định | **IM LẶNG TUYỆT ĐỐI** (kể cả tiếng ván trượt) | — |
| **0 ms** | **Chín mảnh ván đồng loạt lật úp** — rotation 0° → 180° trong 140 ms, **cùng pha tuyệt đối** *(sự đồng bộ hoàn hảo là thứ không tự nhiên, và đó là điểm)* | Punch-in **+10 %**, tâm khung ảnh `(900, 520)` | **FLASH** `#FFD9A0` alpha 0 → **0.32**, ramp 45 ms, một xung. Diegetic: **đèn dầu chao vì luồng khí chín tấm ván** | Chín tiếng gỗ đập **lệch nhau 6–14 ms** (tạo cảm giác "dày"), đỉnh −4 dBTP | `hap_double_knock` |
| **200 ms** | Ván đã úp. Mặt sau ván hiện ra: **mỗi mảnh đều mang đúng một khuôn mặt bị khoét thủng** — chín lỗ thủng hình đầu người, mép giấy xơ | Shake 6 px | Flash 0.32 → 0.07 | `fol_van_go_keo_kot` kéo dài | `hap_tap_light` |
| **600 ms** | Chín lỗ thủng **giữ nguyên, bất động**. **Không có gì nhìn qua lỗ** — đằng sau chỉ là nền ván tối | Nhả về 102 % | Đèn về bình thường, thấp hơn 8 % | Đuôi gỗ | — |
| **1200 ms** | **Envelope kết thúc.** Chín mảnh **tự lật trở lại** mặt trước trong 400 ms tiếp theo (ngoài envelope, không âm thanh giật) — **bố cục người chơi đang xếp được giữ nguyên 100 %** | Tĩnh | — | Recovery 20 s | — |

**Vì sao đặt ở đây:** (a) cuối chương người chơi đã ở mức căng nền 7–8; nếu P6 (câu đố dài nhất) không có phản hồi thất bại nào, đường cong **võng xuống đúng trước cú kết**. (b) Nội dung cú dọa **chính là lời giải sai được hiện thực hoá**: người chơi đang cố ghép lại một khuôn mặt bị khoét; cú dọa trả lời bằng cách cho **mọi** khuôn mặt đều bị khoét. Nó là một **câu trả lời có nghĩa**, không phải tiếng động ngẫu nhiên.

**Luật hoãn bắt buộc (cặp rủi ro S6 → S7):** nếu người chơi vào gác (S6 bắn) rồi lao ngay vào P6 và sai 3 lần trong 80 giây, S7 **chuyển sang biến thể câm**: chín mảnh ván vẫn lật úp và lộ chín lỗ khoét, nhưng **không flash, không stinger** (chỉ `fol_van_go_keo_kot` ở −22 dBFS), **không haptic, không punch**. Sau đó S7 **tự nạp lại**; bản đầy đủ có thể bắn ở lần sai thứ 3 tiếp theo nếu đã qua 90 s.

#### C. `scare_ao_cuoi_quay_dau` — thuộc SPINE · **cú đóng chương**

Xem chi tiết ở **Phần 8 — Kết chương** (nhịp 4 của `seq_ending_ch01_khoac_ao`).

### 3.5.7. Mục tiêu người chơi

| Cấp | Mục tiêu |
|---|---|
| Bề mặt | **Biết sự thật.** Đến đây người chơi không còn đi tìm bà nội nữa — người chơi **đi tìm chính mình** |
| Cơ học | EXAMINE sổ ghi tên, nắp hòm, hai trang nhật ký, khai sinh → giải `puz_xep_anh_gia_pha` → nhặt `item_ao_cuoi_giay` → **`USE_ITEM` lên `hs_hinh_nhan`** |
| Cảm xúc | Tê dại → nhận ra → và cuối cùng là **một quyết định tưởng là vô hại** |

### 3.5.8. Khu vực này đẩy cốt truyện tiến lên thế nào

1. **Đóng toàn bộ mạch thông tin.** Năm tài liệu (sổ ghi tên, hai trang nhật ký, khai sinh, chữ sau khung ảnh) trả lời gọn năm câu hỏi đã đặt từ Khu 1: *tên tôi đâu / ai để tang / ai đặt hàng mã / ai gửi giấy báo tang / vì sao bà dặn đừng về.*
2. **Đảo ngược ý nghĩa của mọi thứ đã làm.** Người chơi nhìn lại: khóa hướng, rập chữ, tuần lễ cúng, ba hồi chín tiếng, thắp đèn soi giếng — **năm việc đã làm không phải là năm câu đố. Là năm phần lễ.** Chỉ còn phần thứ bảy.
3. **Đưa quyền quyết định cho người chơi — rồi lấy nó đi.** Bảy Điều nằm ngay trên nắp hòm. Người chơi *có thể* đã đọc. Nhưng game không cho lựa chọn nào khác để tiến: `USE_ITEM` áo cưới lên hình nhân là **hành động duy nhất khả dụng**. Cảm giác "bị dồn" này chính là cảm giác của một đứa trẻ bảy tuổi năm 1976.
4. **Trả lại cho bà nội một chiến thắng nhỏ và một thất bại lớn.** Bà cứu được cháu năm 1976. Bà thua năm 1996, vì chính lòng thương của bà (ghi địa chỉ sau ảnh thờ để khỏi quên) là thứ dẫn bà Tơ tìm ra người chơi.
5. **Mở chương sau bằng âm thanh, không bằng chữ.** Tiếng mõ nổi rền khắp làng. Chương 1 đóng lại ở quy mô **một ngôi nhà**; tiếng mõ nói rằng Chương 2 có quy mô **một cái làng**.

---

# 4. BẢNG VẬT PHẨM ĐẦY ĐỦ

**10 vật phẩm — đúng và đủ theo SPINE. Không phát sinh `item_id` mới.**

## 4.1. Bảng chính — vị trí nhặt / công dụng

| # | `item_id` | Tên tiếng Việt | **Nhặt ở đâu** (area · hotspot / phần thưởng) | **Dùng để làm gì** (area · hotspot / puzzle) | Mô tả trong túi đồ |
|---|---|---|---|---|---|
| 1 | `item_chia_khoa_dong` | **Chìa khóa đồng gỉ** | `area_san_gach` · **phần thưởng `puz_khoa_bat_quai`** (rơi ra từ ruột ổ khoá) | `area_san_gach` · **gate của `hs_cua_vao_hien`** → mở `area_hien_nha` | Chiếc chìa khoá đồng nhỏ, thân gỉ xanh, đầu chìa khắc một chữ Nho đã mòn. Cầm lên thấy **còn ấm**, dù nó nằm trong ruột khoá gỗ đã lâu lắm rồi |
| 2 | `item_giay_ban_va_than` | **Xấp giấy bản và thỏi than củi** | `area_hien_nha` · `hs_giay_ban_va_than` *(`required_item: null`)* | `area_hien_nha` · `hs_binh_phong` → **mở khoá `puz_rap_chu_the_menh`** | Ba tờ giấy bản mỏng như cánh chuồn và một thỏi than củi vót nhọn đầu. Loại giấy các cụ vẫn dùng để rập lại chữ trên bia mộ |
| 3 | `item_ban_rap_chu_the` | **Bản rập chữ "Thế Mệnh"** | `area_hien_nha` · **phần thưởng `puz_rap_chu_the_menh`** | `area_hien_nha` · `hs_o_lom_binh_phong` (**mở `area_gian_tho`**) · `area_gian_tho` đối chiếu với bài vị · `area_gac_xep` đối chiếu nét chữ với `hs_so_ghi_ten` (**clue C4 của P6**) | Tờ giấy bản đã hiện rõ hai chữ than đen: "Thế Mệnh" — thay mạng. Nét chữ nghiêng về bên phải, của một người thuận tay trái |
| 4 | `item_den_dau` | **Đèn dầu Hoa Kỳ vỏ ám khói** | `area_hien_nha` · `hs_den_dau_treo` *(`required_item: null`)* | `area_bep_gieng` · `hs_den_dau_ghep` → **nguyên liệu `puz_thap_lai_den_dau`** | Vỏ thuỷ tinh ám khói đen. **Bầu cạn, tim cụt, cổ đèn rỗng** — thiếu đúng ba thứ: sợi tim, một ít dầu, và một mồi lửa |
| 5 | `item_dui_mo` | **Dùi mõ gỗ mít** | `area_gian_tho` · `hs_dui_mo` *(`required_item: null`)* — **kích hoạt `scare_di_anh_quay_mat`** | `area_gian_tho` · `hs_mo_ca` → **mở khoá `puz_ba_hoi_chin_tieng`** | Chiếc dùi gỗ mít nặng tay, cán mòn nhẵn **đúng ba chỗ** — chỗ ngón cái, chỗ ngón trỏ, chỗ lòng bàn tay. Ai đó đã cầm nó rất nhiều năm |
| 6 | `item_bai_vi_khuyet_danh` | **Bài vị khuyết danh** | `area_gian_tho` · `hs_bai_vi_khuyet_danh` *(hotspot chỉ spawn sau khi giải `puz_tuan_tu_le_cung`)* | `area_gian_tho` · `hs_khe_mong_cua_gac` — **làm then, một nửa gate lên `area_gac_xep`** | Tấm bài vị gỗ vàng tâm còn mới, mặt trước nhẵn thín **không một nét chữ**. Lật sau thì thấy mộng gỗ đã đẽo sẵn — như đẽo cho vừa một cái khe nào đó |
| 7 | `item_dai_vai_dieu` | **Dải vải điều phủ bài vị** | `area_gian_tho` · `hs_dai_vai_dieu` *(hotspot chỉ spawn sau khi giải `puz_ba_hoi_chin_tieng`)* | `area_bep_gieng` · `puz_thap_lai_den_dau` — **se làm tim đèn (bước 1)** | Dải vải điều đỏ đã bạc thành màu gạch, dệt dày. **Xé dọc thì tước ra thành sợi** — các cụ vẫn se loại vải này làm tim đèn |
| 8 | `item_chai_dau_hoa` | **Chai dầu hoả nút lá chuối** | `area_bep_gieng` · `hs_chai_dau_hoa` *(`required_item: null`)* | `area_bep_gieng` · `puz_thap_lai_den_dau` — **chắt vào bầu đèn (bước 3)** | Chai thuỷ tinh còn hơn nửa dầu hoả, nút bằng lá chuối khô vê chặt. Mở nút ra là mùi hắc xộc lên tận óc, mùi của những đêm mất điện |
| 9 | `item_den_dau_sang` | **Đèn dầu đã thắp** | `area_bep_gieng` · **phần thưởng `puz_thap_lai_den_dau`** | `area_bep_gieng` · `hs_gieng_khoi` (**soi lòng giếng — phần lễ V**) · **gate lên `area_gac_xep`** · điều kiện mở `puz_xep_anh_gia_pha` | Cây đèn đã cháy, ngọn lửa cao bằng hạt thóc, quầng sáng vàng đục chỉ soi được chừng một sải tay. Ngoài cái vòng sáng ấy thì tối đặc |
| 10 | `item_ao_cuoi_giay` | **Áo cưới giấy khổ người lớn** | `area_gac_xep` · `hs_ao_cuoi_giay` *(hotspot chỉ spawn sau khi giải `puz_xep_anh_gia_pha`)* | `area_gac_xep` · `hs_hinh_nhan` → **cutscene kết chương — phần lễ VII** | Bộ áo cưới bằng giấy đỏ, khổ người lớn, đường hồ dán còn mới. Gấu áo có ghi mấy con số bằng bút chì — và **chúng khớp với số đo của chính bạn** |

## 4.2. Phân loại theo nguồn gốc

| Nguồn | Vật phẩm | Ghi chú |
|---|---|---|
| **Phần thưởng câu đố** (4) | `item_chia_khoa_dong` · `item_ban_rap_chu_the` · `item_den_dau_sang` · *(gián tiếp)* `item_bai_vi_khuyet_danh`, `item_dai_vai_dieu`, `item_ao_cuoi_giay` | Ba vật phẩm sau **không rơi thẳng vào túi** mà **spawn hotspot** để người chơi tự tay nhặt — giữ nhịp nghi lễ và cho jumpscare một khoảng thở |
| **Nhặt tự do** (4) | `item_giay_ban_va_than` · `item_den_dau` · `item_dui_mo` · `item_chai_dau_hoa` | Tất cả `required_item: null`, đều nằm **trong cùng khu vực với chỗ cần dùng**, trừ `item_den_dau` (nhặt Khu 2, dùng Khu 4) |

## 4.3. Ràng buộc hệ thống túi đồ

| # | Ràng buộc | Chi tiết |
|---|---|---|
| 1 | **Không vật phẩm bắt buộc nào bị tiêu huỷ vĩnh viễn khi giải sai** | Chống soft-lock. Xấp giấy bản tự nạp lại khi hết 3 tờ; chai dầu luôn còn dầu |
| 2 | `item_den_dau` **biến mất** khi `puz_thap_lai_den_dau` giải xong | Được thay bằng `item_den_dau_sang`. **Biến đổi hợp lệ, không phải mất mát** |
| 3 | `item_giay_ban_va_than` **ở lại trong túi** sau khi giải P2 | Xấp giấy vẫn còn tờ — dùng làm neo hồi tưởng cho Chapter 2 |
| 4 | `item_ban_rap_chu_the` **KHÔNG bị tiêu thụ** khi tra vào ô lõm bình phong | Người chơi **rút lại được**, vì nó còn phải dùng để đối chiếu nét chữ trên gác xép (clue C4 của P6). **Ghi rõ cho Data Architect: `hs_o_lom_binh_phong` không xoá item khỏi túi đồ** |
| 5 | `item_bai_vi_khuyet_danh` **bị giữ lại** tại `hs_khe_mong_cua_gac` | Nó làm then cửa vĩnh viễn. Sau khi dùng, vật phẩm **chuyển sang mục "Đã dùng"** trong túi đồ chứ **không xoá** — để cú twist cuối chương còn chỗ quay lại nhắc. **Không câu đố nào sau đó cần tới nó** |
| 6 | `item_ao_cuoi_giay` **mất vĩnh viễn** sau khi dùng | Đây là vật phẩm duy nhất bị tiêu thụ hẳn, và nó là hành động cuối chương |
| 7 | **Sức chứa túi đồ: tối đa 6 vật phẩm cùng lúc** trong Chương 1 | Đỉnh là lúc cầm: đèn + vải điều + dầu + bản rập + giấy than + bài vị. Thanh inventory 6 ô ở dải `y ∈ [1000, 1080]`, mỗi ô **160 × 80 px**, vùng chạm mở rộng lên **160 × 88** |

## 4.4. Bảng cổng khu vực (`CHANGE_AREA`) — 8 cạnh

| # | Hotspot | Từ | Tới | Chiều | **Điều kiện mở (gate)** | Text khi chưa mở |
|---|---|---|---|---|---|---|
| E1 | `hs_cua_vao_hien` | `area_san_gach` | `area_hien_nha` | đi | **Có `item_chia_khoa_dong`** | `txt_khoa_cua_vao_hien` |
| E2 | `hs_xuong_san_gach` | `area_hien_nha` | `area_san_gach` | về | **Không gate** — quay lại tự do mọi lúc | — |
| E3 | `hs_cua_buc_ban` | `area_hien_nha` | `area_gian_tho` | đi | **`flag_binh_phong_da_tra = true`** (đã dùng `item_ban_rap_chu_the` tại `hs_o_lom_binh_phong`) | `txt_khoa_cua_buc_ban` |
| E4 | `hs_ra_hien` | `area_gian_tho` | `area_hien_nha` | về | **Không gate** | — |
| E5 | `hs_cua_hau_xuong_bep` | `area_gian_tho` | `area_bep_gieng` | đi | **`puz_tuan_tu_le_cung_solved = true`** (hoá vàng xong → thanh gỗ chèn cửa tự rơi) | `txt_khoa_cua_hau` |
| E6 | `hs_len_gian_tho` | `area_bep_gieng` | `area_gian_tho` | về | **Không gate** | — |
| E7 | `hs_cau_thang_gac` | `area_gian_tho` | `area_gac_xep` | đi | **Có `item_den_dau_sang`** VÀ **`flag_then_gac_da_tra = true`** | `txt_khoa_cau_thang_gac` — **báo đúng thứ còn thiếu**: thiếu đèn / thiếu then / thiếu cả hai |
| E8 | `hs_xuong_gian_tho` | `area_gac_xep` | `area_gian_tho` | về | **Không gate** cho tới khi `flag_ao_cuoi_da_nhat = true`; sau đó **khoá vĩnh viễn** | `txt_khoa_gac_xep_sap_cua` |

> **Ràng buộc bắt buộc:** mọi cổng đều **hai chiều**. Không khu vực nào là ngõ cụt một chiều — **trừ đúng một chỗ**: sau khi nhặt `item_ao_cuoi_giay`. Đây là điều kiện cần để bảo đảm không soft-lock (xem Phần 7, Bổ đề 3).

---

# 5. BẢNG LOGIC CÂU ĐỐ ĐẦY ĐỦ

## 5.1. Bảng tổng hợp nhanh — 6 câu đố, 6 loại schema, mỗi loại dùng đúng một lần

| # | `puzzle_id` | `type` | Area | `solution` | `reward_item_id` | `wrong_action_jumpscare` | `max_fails` | Khó | Giây | Beat |
|---|---|---|---|---|---|---|---|---|---|---|
| **P1** | `puz_khoa_bat_quai` | `ROTATION_LOCK` | `area_san_gach` | **`[6, 3, 8]`** | `item_chia_khoa_dong` | `scare_bong_trong_chum` | 3 | 2/5 | 90 | B03 |
| **P2** | `puz_rap_chu_the_menh` | `PATTERN_TRACE` | `area_hien_nha` | **`[2, 1, 4, 3, 7, 5, 8, 6]`** | `item_ban_rap_chu_the` | `null` *(scare bắn khi **GIẢI ĐÚNG**)* | — | 3/5 | 150 | B04 |
| **P3** | `puz_tuan_tu_le_cung` | `SEQUENCE_ORDER` | `area_gian_tho` | **`[3, 6, 4, 1, 5, 2]`** | `item_bai_vi_khuyet_danh` | `scare_khoi_tu_hinh_nguoi` * | 3 | 3/5 | 120 | B06→B07 |
| **P4** | `puz_ba_hoi_chin_tieng` | `AUDIO_MATCH` | `area_gian_tho` | **`[3, 3, 5, 3, 7, 3]`** | `item_dai_vai_dieu` | `scare_khoi_tu_hinh_nguoi` * | 3 | **4/5** | 180 | B08 |
| **P5** | `puz_thap_lai_den_dau` | `ITEM_COMBINE` | `area_bep_gieng` | **`[2, 5, 1, 3, 4]`** | `item_den_dau_sang` | `scare_mat_duoi_day_gieng` | 3 | 3/5 | 110 | B10 |
| **P6** | `puz_xep_anh_gia_pha` | `SLIDING_TILE` | `area_gac_xep` | **`[2, 5, 7, 4, 8, 3, 6, 1, 0]`** | `item_ao_cuoi_giay` | `scare_anh_tho_thieu_mat` * | 3 | **4/5** | 240 | B13→B14 |

`*` = jumpscare **phái sinh**, chờ Lead duyệt; nếu không duyệt thì đặt `null`.

**Tổng thời gian giải đố kỳ vọng: 890 giây ≈ 15 phút** thuần giải đố. **Đường cong độ khó:** 2 → 3 → 3 → **4** → 3 → **4**.

## 5.2. Bảng logic chi tiết — lời giải + clue + reward

| Câu đố | Lời giải & ý nghĩa từng phần tử | Manh mối dẫn tới lời giải (tất cả đều `EXAMINE` tự do, không cần vật phẩm) | Hành vi khi sai | Reward mở ra gì |
|---|---|---|---|---|
| **P1** `puz_khoa_bat_quai`<br>`ROTATION_LOCK` | `[6, 3, 8]` đọc **ngoài → trong**<br>• `6` = **Khảm ☵** (nước, Bắc) — nhà *tọa* Bắc, lưng nhà tựa Bắc → vòng ngoài<br>• `3` = **Ly ☲** (lửa, Nam) — nhà *hướng* Nam → vòng giữa<br>• `8` = **Khôn ☷** (đất, thuần âm, tượng người nữ) — "người ở trong nhà" = Bà Cô → vòng trong<br>*Không gian tìm kiếm 8³ = 512* | **C1** `hs_guong_bat_quai` — từ điển quẻ ↔ số ↔ ngũ hành ↔ tượng người<br>**C2** `hs_cau_doi_trai` — *"Tọa Bắc — lưng dựa dòng nước"*<br>**C3** `hs_cau_doi_phai` — *"Hướng Nam — mặt đón lửa trời"*<br>**C4** `hs_chum_nuoc_mua` — chum kê đúng góc Bắc (xác nhận chéo C2)<br>**C5** `hs_day_phoi_khan_xo` — *"Bà Cô — gái út — mất năm mười bảy tuổi"*<br>**C6** trục then khắc **"Tọa — Hướng — Người"** — thứ tự đọc mảng | 1: ba vòng trả về vị trí cũ + tiếng gỗ nghiến 1,2 s<br>2: + gáo dừa xoay một vòng ở hậu cảnh (gợi ý môi trường)<br>3: **`scare_bong_trong_chum`**, reset đếm, **giữ nguyên vị trí vòng** | `item_chia_khoa_dong` → mở `hs_cua_vao_hien` → `area_hien_nha` |
| **P2** `puz_rap_chu_the_menh`<br>`PATTERN_TRACE` | `[2, 1, 4, 3, 7, 5, 8, 6]` — thứ tự miết 8 nét theo **bốn phép bút thuận**<br>Chữ **Thế 世**: ngang dài (2) → sổ trái (1) → sổ giữa (4) → sổ-gập phải (3)<br>Chữ **Mệnh 命**: ngang (7) → bộ Khẩu 口 (5) → bộ Tiết 卩 (8) → **nét mái 人 (6) sau cùng**<br>*Hướng miết có tính điểm: ngang trái→phải, sổ trên→xuống*<br>*8! = 40 320 hoán vị → clue thu về duy nhất một* | **C1** `hs_vo_tap_viet` — **bốn phép** + ba chữ mẫu đã đánh số nét (三 · 川 · 大)<br>**C2** `hs_manh_nua` — bụi in khuôn hai chữ, chữ trên viết trước<br>**C3** `hs_guoc_moc` — đế dính vụn than → than là thứ dùng ở đây<br>**C4** `hs_binh_phong` fallback — dạy điều kiện mở khoá | 1: nét lem, hỏng tờ, *"Còn 2 tờ"*<br>2: *"Còn 1 tờ"* + mành nứa đung đưa không gió<br>3: **xấp giấy tự nạp lại đầy 3 tờ** + mở Hint Tier 1 miễn phí. **Không mất vật phẩm** | `item_ban_rap_chu_the` → tra `hs_o_lom_binh_phong` → mở `area_gian_tho`; đồng thời `scare_ban_tay_giay_sau_manh` bắn |
| **P3** `puz_tuan_tu_le_cung`<br>`SEQUENCE_ORDER` | `[3, 6, 4, 1, 5, 2]` — sáu bước tuần lễ cúng Bắc Bộ<br>① `3` lau bài vị & bày mâm — *"trước hết phải sạch"*<br>② `6` thắp đôi đèn — *"đèn sáng thì hồn mới thấy đường"*<br>③ `4` thắp ba nén nhang — có lửa đèn mới châm được<br>④ `1` rót sơ tuần rượu — *"dâng khi hương đã bén"*<br>⑤ `5` đọc văn khấn, vái ba vái<br>⑥ `2` **hóa vàng** — *"hóa vàng là tiễn, tiễn thì phải sau rốt"*<br>*6! = 720 hoán vị* | **C1** `hs_van_khan` *(clue CHÍNH)* — **toàn bộ 6 bước và quan hệ trước-sau**, viết bằng văn xuôi, không đánh số<br>**C2** `hs_hoanh_phi` — tờ lịch cũ: *"đèn trước, nhang sau, vàng sau rốt"*<br>**C3** sáp nến chảy dày hơn phần chân nhang → đèn châm trước nhang<br>**C4** chậu hoá vàng kê sát lối ra → hoá vàng là bước cuối | 1: ba nén nhang tắt ngấm, 6 icon bay trả về bàn<br>2: + một ngọn đèn phụt tắt, sáng −20 %<br>3: **`scare_khoi_tu_hinh_nguoi`** (dread, người chơi phải chạm màn hình để khói tan)<br>*Bẫy cố ý: vàng mã đặt ngay tầm tay, sáng hơn — dụ hóa vàng sớm = phạm điều cấm kỵ thứ Tư* | `item_bai_vi_khuyet_danh` (spawn `hs_bai_vi_khuyet_danh`) **+ mở cửa hậu** `hs_cua_hau_xuong_bep` → `area_bep_gieng` |
| **P4** `puz_ba_hoi_chin_tieng`<br>`AUDIO_MATCH` | `[3, 3, 5, 3, 7, 3]` = **3 cặp `[dồn, rời]`**, sau mỗi cặp gõ **1 tiếng chuông** (cố định, không mã hoá trong mảng)<br>Hồi 1: 3 dồn + 3 rời + chuông<br>Hồi 2: 5 dồn + 3 rời + chuông<br>Hồi 3: 7 dồn + 3 rời + chuông<br>*"Ba hồi" = 3 cặp · "chín tiếng" = 3+3+3 tiếng rời · phần dồn 3-5-7 số lẻ tăng dần · tổng **33 tap*** | **C1** `hs_vach_buong` + nút *"Áp tai vào vách"* — **nghe lại lời giải vô hạn**, không tính lần sai<br>**C2** tang mõ khắc **三 五 七** (đọc được cả khi chưa có dùi)<br>**C3** dòng cuối `hs_van_khan` — cấu trúc dồn / 3 rời / 1 chuông<br>**C4** `hs_dui_mo` — cán mòn đúng ba chỗ (mô-típ "ba")<br>**→ Hai đường độc lập: thính giác (C1) và văn bản (C2+C3)** | 1: mõ bên kia vách **nhại lại chậm nửa nhịp**<br>2: nhại **to hơn, gần hơn** (pre-delay 120→35 ms, pan sang phải) + hiện mờ số tiếng hồi 1 trong 2 s. **Tier 1 tự mở ở đây**<br>3: **`scare_khoi_tu_hinh_nguoi`** | `item_dai_vai_dieu` (spawn `hs_dai_vai_dieu` — vải điều tuột khỏi khám thờ: *"Bà Cô đã mở mắt"*) |
| **P5** `puz_thap_lai_den_dau`<br>`ITEM_COMBINE` | `[2, 5, 1, 3, 4]` — năm bước thắp đèn đúng lối nhà quê 1990<br>① `2` xé & se **vải điều** thành tim — gốc của cả chuỗi<br>② `5` luồn tim qua **cổ đèn** — đổ dầu rồi mới xỏ thì trơn, không xỏ nổi<br>③ `1` chắt **dầu hoả** vào bầu — tim ngấm theo mao dẫn<br>④ `3` vặn **núm** cho tim nhô bằng hạt gạo — phải chỉnh lúc chưa có lửa<br>⑤ `4` rút **que đóm**, mồi vào than hồng, châm vào tim<br>*5! = 120 hoán vị → 4 ràng buộc thu về duy nhất một* | **C1** `hs_gac_bep_bo_dom` — **cây đèn hỏng tháo rời** làm mẫu tham chiếu (tim xuyên qua cổ đèn; bầu là bộ phận riêng)<br>**C2** `hs_vach_bep_chu_than` — *"tim ngấm dầu hẵng châm lửa"* + *"vặn xong mới châm"* → **hai ràng buộc thứ tự quyết định**<br>**C3** `hs_den_dau_treo` (Khu 2) — danh sách ba thứ còn thiếu<br>**C4** `hs_dai_vai_dieu` (Khu 3) — vải điều = tim đèn, phải **se** trước<br>**C5** `hs_dong_tro_than` — nguồn lửa duy nhất | 1: phản hồi **theo ngữ cảnh, có tính dạy** (lửa loé rồi tắt / dầu tràn ra bàn / núm quay lỏng lẻo). **Các bước đúng trước đó được giữ nguyên**<br>2: + than lụi một nhịp, bếp tối thêm, tiếng nước dội dưới giếng<br>3: **`scare_mat_duoi_day_gieng`**, reset đếm, **giữ tiến độ** | `item_den_dau_sang` → soi `hs_gieng_khoi` (**Beat B11**) + **gate lên `area_gac_xep`** + mở khoá P6 |
| **P6** `puz_xep_anh_gia_pha`<br>`SLIDING_TILE` | `[2, 5, 7, 4, 8, 3, 6, 1, 0]` — row-major 3×3, `0` = ô trống<br>**Hàng trên:** ông nội (2) – cụ tổ (5) – bà nội (7) → *nam tả nữ hữu, cụ tổ giữa*<br>**Hàng giữa:** bác cả (4) – bố (8) – Bà Cô (3) → *trưởng – thứ – út*<br>**Hàng dưới:** anh họ (6) – chị họ (1) – **trống (0)**<br>*Ô trống = cháu út = **chính người chơi**, khuôn mặt đã bị khoét* | **C1** `hs_hom_go_nap` trang 1 *(clue CHÍNH)* — **toàn bộ quy tắc ngôi thứ**, dòng cháu út **bị gạch nát**<br>**C2** nút *"Lật mảnh"* — mặt sau mỗi mảnh khắc chữ Nho vai vế (祖/祖父/祖母/伯/父/姑/孫/孫女)<br>**C3** `hs_gia_pha` (Khu 3) — ngôi thứ đã chép sẵn, **thưởng cho người đọc kỹ**<br>**C4** `item_ban_rap_chu_the` đối chiếu nét chữ `hs_so_ghi_ten` — cùng một người viết | *Định nghĩa sai: một lần ấn **"Áp ảnh vào khung"** khi bố cục chưa khớp*<br>1: khung không khít, một mảnh bật ra rồi rơi lại<br>2: + đèn chao một nhịp; **hai mảnh đúng vị trí phát sáng viền vàng 2 s** (gợi ý động)<br>3: **`scare_anh_tho_thieu_mat`**. **TUYỆT ĐỐI KHÔNG xáo lại bàn cờ** | `item_ao_cuoi_giay` (spawn `hs_ao_cuoi_giay`) + lộ mặt sau khung ảnh + **`flag_ao_cuoi_da_nhat` → point of no return** → `USE_ITEM` lên `hs_hinh_nhan` = **KẾT CHƯƠNG** |

## 5.3. Quy ước chung cho cả sáu câu đố

| Hạng mục | Quy ước |
|---|---|
| **Mảng `solution`** | Luôn là **mảng số nguyên**, đọc **từ trái sang phải = từ bước đầu đến bước cuối** (hoặc **từ vòng ngoài vào vòng trong** với `ROTATION_LOCK`) |
| **Ý nghĩa các con số** | **Không phải toạ độ**, mà là **ID phần tử do engine đánh cố định** (atlas index của sprite/nút), cố định trong build, ghi rõ ở bảng ánh xạ của từng câu đố |
| **Vì sao ID không trùng thứ tự đúng** | **Cố ý** — tránh việc người chơi brute-force bằng cách bấm theo thứ tự tự nhiên trái→phải |
| **Bộ đếm sai** | Mỗi câu đố có `fail_count` riêng, **reset về 0** sau khi (a) giải đúng, hoặc (b) jumpscare đã bắn |
| **Mốc phản hồi chung** | Sai 1 = phản hồi nhẹ (âm thanh + animation, không phạt) · Sai 2 = phản hồi nặng hơn + gợi ý môi trường · Sai 3 = bắn jumpscare (`max_fails: 3`) rồi reset đếm |
| **Không khoá vĩnh viễn** | **Không câu đố nào khoá vĩnh viễn người chơi khi sai. Không mất vật phẩm vĩnh viễn.** Số lần thử là **vô hạn** ở mọi câu đố |
| **Hệ thống gợi ý** | Nút **"Thắp nhang xin keo"** ở `{x:1700, y:930, width:150, height:110}`. **Tier 1** mở sau 60 s kẹt hoặc 1 lần sai · **Tier 2** sau 150 s hoặc 2 lần sai · **Tier 3** sau 300 s hoặc 4 lần sai. **Tier 3 luôn là đáp án trực tiếp** |
| **Ràng buộc LiveOps** | Tier 1 & 2 **miễn phí**. Tier 3 gắn LiveOps nhưng **luôn có đường mở miễn phí bằng thời gian chờ 300 s** — **không được phép biến thành tường trả phí** |
| **Ràng buộc an toàn** | `max_fails`, `solution`, `reward_item_id`, `type`, `wrong_action_jumpscare`, thời gian mở hint — **KHÔNG BAO GIỜ** bị tuỳ chọn an toàn override. Chỉ cường độ trình diễn của jumpscare thay đổi |

## 5.4. Đồ thị phụ thuộc và phân tầng tô-pô

```
item_chia_khoa_dong ─→ [vào area_hien_nha]
                          ├─→ item_giay_ban_va_than ─→ P2 ─→ item_ban_rap_chu_the
                          └─→ item_den_dau ──────────────────────────────┐
                                                                         │
item_ban_rap_chu_the ─→ [vào area_gian_tho]                              │
                          ├─→ P3 ─→ item_bai_vi_khuyet_danh ──────┐      │
                          │         └─→ [mở cửa hậu xuống bếp]    │      │
                          └─→ item_dui_mo ─→ P4 ─→ item_dai_vai_dieu ─┐  │
                                                                      │  │
[vào area_bep_gieng] ─→ item_chai_dau_hoa ────────────────────────────┤  │
                                                                      ▼  ▼
                                              P5 ─→ item_den_dau_sang ────┐
                                                                          │
item_bai_vi_khuyet_danh ─────────────────────────────────────────────┐    │
                                                                     ▼    ▼
                                                    [vào area_gac_xep]
                                                              │
                                                              ▼
                                            P6 ─→ item_ao_cuoi_giay ─→ KẾT CHƯƠNG
```

**Phân tầng tô-pô — mọi cạnh chỉ đi từ tầng thấp lên tầng cao, KHÔNG có cạnh ngược:**

| Tầng | Phần tử |
|---|---|
| 0 | **P1** (không cần gì) |
| 1 | `item_chia_khoa_dong` |
| 2 | vào `area_hien_nha` · `item_giay_ban_va_than` · `item_den_dau` |
| 3 | **P2** |
| 4 | `item_ban_rap_chu_the` |
| 5 | vào `area_gian_tho` · `item_dui_mo` |
| 6 | **P3** · **P4** *(hai câu đố song song, độc lập với nhau)* |
| 7 | `item_bai_vi_khuyet_danh` · `item_dai_vai_dieu` · mở cửa hậu |
| 8 | vào `area_bep_gieng` · `item_chai_dau_hoa` |
| 9 | **P5** |
| 10 | `item_den_dau_sang` |
| 11 | vào `area_gac_xep` |
| 12 | **P6** |
| 13 | `item_ao_cuoi_giay` → kết chương |

**Kết luận:** tồn tại một **thứ tự tô-pô hoàn chỉnh** cho toàn bộ đồ thị ⇒ đồ thị là **DAG** ⇒ **KHÔNG CÓ VÒNG TRÒN PHỤ THUỘC**.

**Kiểm tra thủ công từng cặp nghi vấn:**

| Cặp nghi vấn | Có vòng? | Lý do |
|---|---|---|
| `item_bai_vi_khuyet_danh` ↔ `item_den_dau_sang` *(cả hai cùng cần để lên gác xép)* | **KHÔNG** | Cả hai là **đầu vào của cùng một cổng** (tầng 11). Chúng **không cần nhau**: bài vị ra từ P3 (tầng 6), đèn sáng ra từ P5 (tầng 9); **P5 không cần bài vị** |
| `item_dai_vai_dieu` ↔ `item_chai_dau_hoa` | **KHÔNG** | Vải điều lấy ở gian thờ (tầng 7), dầu hoả lấy ở bếp (tầng 8). Vào bếp cần **giải P3**, **không** cần vải điều. P4 (sinh vải điều) **không** cần dầu hoả |
| `item_den_dau` ↔ `item_den_dau_sang` | **KHÔNG** | Quan hệ một chiều: thân đèn (tầng 2) → nguyên liệu P5 → đèn sáng (tầng 10) |
| P3 ↔ P4 *(cùng ở `area_gian_tho`)* | **KHÔNG** | Hoàn toàn độc lập. P3 cần đọc văn khấn; P4 cần dùi mõ. **Giải theo thứ tự nào cũng được** |
| `item_ban_rap_chu_the` bị "tiêu" khi đặt vào ô lõm | **KHÔNG** | Bản rập **không bị tiêu huỷ**: sau khi then nhả, người chơi **lấy lại** |
| `item_bai_vi_khuyet_danh` bị "tiêu" khi làm then | **KHÔNG tạo vòng** | Bài vị **ở lại vĩnh viễn** làm then, nhưng **không câu đố nào sau đó cần tới nó** (P6 chỉ cần `item_den_dau_sang`). An toàn |

## 5.5. Tự kiểm tra ràng buộc kỹ thuật

| Kiểm tra | Kết quả |
|---|---|
| Tổng số hotspot toàn chương | **66** (13 + 11 + 17 + 14 + 11) |
| Mọi bounds là **số nguyên** | ✅ ĐẠT |
| Mọi bounds nằm trọn trong 1920 × 1080 | ✅ ĐẠT (`x+w` lớn nhất = 1880) |
| Mọi bounds ≥ 88 × 88 px | ✅ ĐẠT (nhỏ nhất: cao 88 px ở `hs_chieu_coi_trai_san`; rộng 110 px ở `hs_dui_mo`) |
| Không hotspot nào có `y < 80` | ✅ ĐẠT (`y` nhỏ nhất = 96) |
| Không hotspot nào có `y + height > 1000` | ✅ ĐẠT (`y+h` lớn nhất = 998) |
| **Không cặp hotspot nào chồng lấn trong cùng area** | ✅ **415 cặp so sánh toàn chương — 0 cặp giao nhau** |
| Mọi `id` duy nhất trên toàn chương | ✅ ĐẠT (0 trùng) |
| Mọi `target_puzzle_id` trỏ tới puzzle **trong cùng file area** | ✅ ĐẠT (6/6) |
| Mọi `target_area_id` tồn tại trong chapter manifest | ✅ ĐẠT (8/8 hotspot `CHANGE_AREA`) |
| Mọi `required_item` của `USE_ITEM` khác `null` | ✅ ĐẠT (4/4: `hs_o_lom_binh_phong`, `hs_khe_mong_cua_gac`, `hs_gieng_khoi`, `hs_hinh_nhan`) |
| Mọi `COLLECT_ITEM` có `item_id` và trường `required_item` | ✅ ĐẠT (7/7) |
| Mọi `EXAMINE` / `DIALOGUE` có `text_key` | ✅ ĐẠT |
| Mọi `reward_item_id` trùng khớp SPINE | ✅ 6/6 |
| Mọi `type` nằm trong tập hợp lệ | ✅ ROTATION_LOCK / PATTERN_TRACE / SEQUENCE_ORDER / AUDIO_MATCH / ITEM_COMBINE / SLIDING_TILE — **mỗi loại dùng đúng một lần, phủ trọn 6/6 loại** |
| Mọi `wrong_action_jumpscare` trỏ tới jumpscare **trong cùng file area** hoặc `null` | ✅ ĐẠT |
| Mọi `ON_PUZZLE_FAIL_COUNT` có `max_fails` nguyên ≥ 1 | ✅ ĐẠT (đều = 3) |
| `solution` của `puz_xep_anh_gia_pha` là hoán vị hợp lệ của {0..8} | ✅ Hợp lệ, ô trống ở vị trí 9 |
| Đồ thị phụ thuộc là DAG | ✅ Có thứ tự tô-pô 14 tầng |

---

# 6. BẢNG BEATS VÀ ĐƯỜNG CONG SỢ HÃI

## 6.1. Hai thang đo và cách quy đổi

`01_narrative` dùng thang **1–5** cho tổ kịch bản. Tổ audio/VFX dùng thang **1–10** vì cần phân giải mịn hơn ở vùng 6–10, nơi mọi quyết định mix xảy ra.

| Thang 1–5 (kịch bản) | Thang 1–10 (audio/VFX) | Định nghĩa vận hành | Trạng thái mix |
|---|---|---|---|
| **1 — Bình thản, tò mò** | 1–2 | Người chơi đang quan sát, chưa nghi ngờ | Chỉ `amb_*`. **Không drone, không nhạc** |
| **2 — Bất an nhẹ** | 3–4 | Có một chi tiết lệch chuẩn | Thêm `drn_nen_sub_50hz` ở −38 dBFS. Người chơi không "nghe" thấy, chỉ thấy ngực hơi nặng |
| **3 — Căng, nghi ngờ rõ rệt** | 5–6 | Người chơi đã kết luận "có chuyện" | Drone lên −32 dBFS. `mus_*` một nốt kéo dài, không giai điệu |
| **4 — Lạnh sống lưng, kinh hoàng nhận thức** | 7–8 | **Sợ vì hiểu ra**, không phải vì bị dọa | **Rút nhạc gần hết.** Chỉ còn tiếng phòng + drone + một lớp folk diegetic. Vùng khó mix nhất và hay nhất của game |
| **5 — Đỉnh điểm** | 9–10 | Jumpscare, hoặc cú lật nhận thức lớn | Đầy dải, flash (nếu được phép), haptic |

**Luật đường cong bắt buộc:**

| # | Luật | Trạng thái |
|---|---|---|
| 1 | Không quá **hai** beat mức 5 (≥ 9) liền nhau | ✅ — chỉ cặp B14/B14a ở cuối, **cố ý**: chúng là **một cú duy nhất kéo dài**, đóng chương |
| 2 | Sau mỗi mức 5 phải có ít nhất một beat tụt xuống ≤ 3 (≤ 6) để người chơi "thở" | ✅ |
| 3 | Mỗi beat ≥ 9 phải có beat ≤ 6 **trước đó** trong vòng 3 beat | ✅ — B02←B01a(4) · B04a←B03(3) · B07a←B06(5) · B10a←B10(5) · B11←B10(5) · B12a←B12(7, kèm khoá L2) · B13b←B13(7, kèm khoá L1) · B14←B12c(7) |
| 4 | Mỗi beat ≥ 9 phải có beat ≤ 7 **sau** nó trong vòng 2 beat | ✅ trừ cặp đóng chương |
| 5 | Biên độ trung bình nửa đầu chương < nửa sau | ✅ — nửa đầu (B01→B08) TB **5,6**; nửa sau (B09→B14a) TB **8,0**. **Đường cong đi lên, không răng cưa phẳng** |
| 6 | Có ít nhất 1 đỉnh ≥ 9 **không phải jumpscare** | ✅ — **B11 (giếng khơi)**; gần đạt: B07 (8) và B09b (8) |
| 7 | Tổng số beat mức 5 toàn chương | **7** — 6 jumpscare theo SPINE + cú twist kết chương |

## 6.2. BẢNG BEATS ĐẦY ĐỦ

★ = beat gốc trong SPINE (14 beat, giữ nguyên thứ tự và nội dung). Beat chữ thường là beat phụ triển khai, **không thay đổi SPINE**.
🔔 = jumpscare bắn · 😮‍💨 = nhịp nghỉ bắt buộc.

| Beat | Area | Sự kiện | 1–5 | 1–10 | Kỹ thuật dùng |
|---|---|---|---|---|---|
| **B01 ★** | `area_san_gach` | Người chơi dắt xe đạp qua ngõ tre về ngôi nhà tổ ở Linh An khi trời vừa nhập nhoạng, mùi hương trầm còn vương trên sân gạch | **1** | 2 | Chỉ `amb_san_gach_chieu` ở −30 dBFS. **Không drone, không nhạc trong 45 giây đầu** — cố tình để người chơi tưởng đây là game giải đố nhẹ nhàng. `fol_xe_dap_dat_go` là âm thanh đầu tiên của game |
| B01a | `area_san_gach` | Loa xã đọc bản tin rằm tháng Bảy: *"nhờ bà con trông hộ cái nhà, cho đến khi có người về nhận"*. Người chơi đọc cáo phó — **không có tên mình** | **2** | 4 | `drn_nen_sub_50hz` fade-in 12 s lên −38 dBFS **đúng lúc mở cáo phó**. Ve cuối mùa đang kêu thì **ngưng** (silence tell sớm). `vox_loa_phat_thanh_01` ở xa, −26 dBFS, băng hẹp 300 Hz–3.4 kHz |
| **B02 ★** 🔔 | `area_san_gach` | Mảnh khăn xô còn vắt trên dây phơi và **chum nước phản chiếu một bóng người đứng sau lưng** — `scare_bong_trong_chum` | **5** | **9** | Impulse scare **đầu tiên của game** — thiết lập "ngôn ngữ đe doạ" cho toàn bộ phần còn lại. Xem mục 3.1.6 |
| B02b 😮‍💨 | `area_san_gach` | Thư tay bà nội trong khe gạch: *"cháu đừng về… đừng gọi tên ai… cái hòm trên gác thì cháu đừng mở"* | **3** | 4 | **Recovery window 20 s**: mọi lớp về −45 dBFS rồi bò lên. Mở UI đọc thư → **khoá L1** cứng. **Nhạc không vào** |
| **B03 ★** | `area_san_gach` | Giải ổ khóa gỗ khắc bát quái (Khảm – Ly – Khôn), lấy chìa khóa đồng, mở cửa bức bàn bước lên hiên | **2** | 3 | Chế độ thao tác: `ui_khoa_snap_go` mỗi nấc 45°, haptic `hap_tap_light`. Nền duck −6 dB cho người chơi tập trung. Giải xong: `fol_khoa_bat_then` + drone tụt về −38 |
| **B04 ★** | `area_hien_nha` | Ở hiên, người chơi phủ giấy bản lên bình phong và rập than theo đúng bút thuận, làm hiện ra hai chữ **"Thế Mệnh"** | **3** | 5 | `amb_hien_nha_gio_manh` với `fol_manh_nua_dap` nhịp **không đều** (2,1–4,8 s ngẫu nhiên) — tai người luôn cố dự đoán và luôn sai. Tiếng than miết giấy là âm thanh duy nhất ở tiền cảnh |
| B04a 🔔 | `area_hien_nha` | Nét than cuối của chữ "Mệnh" vừa hiện, mành nứa bật tung, **một bàn tay vàng mã khô quét sát mặt kính** — `scare_ban_tay_giay_sau_manh` | **5** | **9** | Đặt ở **khoảnh khắc thắng lợi** — điểm nhấn chủ đề đắt nhất chương. Xem mục 3.2.6 |
| B04b 😮‍💨 | `area_hien_nha` | Đọc nhật ký 1976 (*"nhà mình sắp có đám cưới"*); ướm đôi guốc mộc — **vừa khít chân người chơi**; đọc nhãn hàng mã ghi tên **"bà Tơ"** | **3** | 5 | Recovery. Guốc vừa khít → **không dọa**, chỉ để một nốt `drn_nhi_keo_dai` vào rất khẽ (−34) và **giữ nguyên không đổi trong 40 giây**. Sự bất động của âm thanh mới là thứ gây khó chịu |
| **B05 ★** 😮‍💨 | `area_hien_nha` → `area_gian_tho` | Bản rập vừa khớp vào ô lõm trên bình phong thì **then cửa gian giữa nhả ra**, mùi nhang lạnh ùa từ bàn thờ họ | **2** | 4 | Chuyển area = **khoá L2** cứng 15 s. Crossfade ambience 2,5 s. "Mùi nhang lạnh" được dịch sang âm thanh bằng cách **cắt hết lớp gió**: gian thờ tĩnh hơn hiên rất nhiều, và **sự tĩnh đó tự nó là đe doạ** |
| B05a | `area_gian_tho` | Bát hương xoay lệch 45°, vòng hương trên xà cháy dở, một cây đèn tắt ngóm. Đọc văn khấn và **trang gia phả bị cạo bằng dao** | **3** | 6 | `fol_huong_vong_lach_tach` loop ở −38. `mus_mot_not_keo_dai` vào: **một nốt đàn nhị kéo dài duy nhất**, không vibrato, −28 dBFS |
| **B06 ★** 😮‍💨 | `area_gian_tho` | Đọc cuốn văn khấn chép tay, sắp lại đúng **sáu bước tuần lễ cúng** và hóa vàng để chốt khám thờ Bà Cô bật mở | **3** | 5 | Vùng đọc. **Khoá L1 bật mỗi lần mở văn khấn.** Mix rút xuống còn 2 lớp. Đây là **nhịp nghỉ dài nhất chương (~6 phút)** — cố ý, để dồn cho B07→B08 |
| **B07 ★** | `area_gian_tho` | Trong khám thờ chỉ có **một tấm bài vị khuyết danh** — gỗ mới, chữ chưa từng được khắc tên người | **4** | **8** | **Đỉnh dread không có jumpscare.** Nhạc **rút sạch**. Chỉ còn drone + `vox_hoi_tho_gan` (−30 dBFS, mono, không reverb). **Sợ vì hiểu ra, không vì bị dọa** |
| B07a 🔔 | `area_gian_tho` | Lúc nhặt dùi mõ, cả bó chân nhang bốc cháy một nhịp và **toàn bộ di ảnh đồng loạt quay mặt vào vách** — `scare_di_anh_quay_mat` | **5** | **9** | Bắn đúng lúc người chơi **lấy một thứ khỏi bàn thờ** — hành vi phạm thượng. Xem mục 3.3.7A |
| **B08 ★** | `area_gian_tho` | **Ba hồi chín tiếng** mõ vọng ra từ sau vách buồng trống, buộc người chơi cầm dùi gõ lại đúng nhịp cho tới khi dải vải điều tuột xuống | **4** | **8** | **Câu đố chính là cao trào âm thanh.** `fol_mo_*` ở tiền cảnh; bên kia vách trả lời với pan dịch dần sang phải và pre-delay giảm **120 ms → 35 ms** (nghe như **đang tiến lại gần**). **Không jumpscare — câu đố tự nó đủ căng** |
| **B09 ★** 😮‍💨 | `area_gian_tho` → `area_bep_gieng` | Cửa hậu hết bị chèn, người chơi lần xuống gian bếp tro tối om nơi kiềng ba chân còn ấm dù nhà đã bỏ không nhiều ngày | **3** | 5 | Chuyển area = relief. Ambience đổi hẳn màu: từ "cao, khô, vang gỗ" sang "thấp, ẩm, chết tiếng" (**RT60 1,4 s → 0,35 s**) |
| B09a | `area_bep_gieng` | Cột bếp có **năm vạch dao** (1953/1961/1968/1976), **vạch thứ năm để trống**. Hình que trẻ con trên vách bồ hóng | **4** | **7** | `fol_than_no_lep_bep` là lớp duy nhất có sự sống. `fol_nuoc_tom_gieng` đều đặn 9–11 s/lần từ ngoài sân sau, pan cố định 0.7 phải |
| B09b | `area_bep_gieng` | Sổ chợ ghi số đo áo cưới giấy; người chơi rút phiếu đo hiệu may ra đối chiếu — **trùng khít từng con số** | **4** | **8** | **Cắt phẳng toàn bộ nền về −50 dBFS trong 3 giây** ngay khi hai con số khớp. **Không thêm âm thanh nào.** Cú dread mạnh thứ hai chương |
| **B10 ★** 😮‍💨 | `area_bep_gieng` | Người chơi se vải điều làm tim, chắt dầu hỏa vào bầu và mồi đóm thắp lại cây đèn dầu Hoa Kỳ | **3** | 5 | Vùng thao tác, nền trở lại. Mỗi bước đúng có `ui_buoc_dung_go` rất khẽ — phản hồi tích cực để **kéo mức xuống trước B10a/B11** |
| B10a 🔔 | `area_bep_gieng` | *(Nhánh thất bại — sai 3 lần)* Que đóm loé một giây, trong quầng sáng ấy **một khuôn mặt trắng bệch úp sát cửa bếp** — `scare_mat_duoi_day_gieng` | **5** | **9** | Xem mục 3.4.6. **Flash "sạch" nhất chương** — hoàn toàn diegetic |
| **B11 ★** | `area_bep_gieng` | Ánh đèn soi xuống lòng giếng để lộ **một chiếc guốc trẻ con** mắc ở gờ gạch và hàng chữ khắc trên thành giếng nhắc tới **"người thế mạng"** | **5** | **9** | **CỐ Ý KHÔNG CÓ JUMPSCARE.** `fol_nuoc_tom_gieng` **ngừng hẳn**, giữ im **7 giây**, không có gì xảy ra. `mus_gieng_khoi` ngưng ở giây 12 và không quay lại. Xem mục 3.4.7 |
| **B12 ★** 😮‍💨 | `area_gian_tho` → `area_gac_xep` | Tấm bài vị khuyết danh vừa khít khe mộng cửa gác xép, người chơi dùng nó **làm then** và trèo lên giữa đống vàng mã | **4** | 7 | Relief tương đối: leo thang là hành động cơ học, `fol_van_go_keo_kot` từng bậc một, **nhịp do người chơi tự bấm → người chơi tự đặt nhịp tim của chính mình** |
| B12a 🔔 | `area_gac_xep` | Vừa nhô đầu lên sàn gác, đèn tắt phụt vì gió lùa; đèn cháy lại thì **hình nhân nan tre đã đứng chắn trước mặt** — `scare_hinh_nhan_chan_loi` | **5** | **10** | **Cú dọa duy nhất không thể tránh của chương.** 520 ms đen hoàn toàn ở giữa envelope. Xem mục 3.5.6A |
| B12b | `area_gac_xep` | Đọc sổ ghi tên: bốn đời người thế mạng, dòng thứ tư ghi **Nguyễn Thị Liên — cái Đĩ Con — 7 tuổi — LỄ CHƯA THÀNH**. Người chơi đọc cái tên **thành tiếng** | **4** | **8** | **Không dọa.** Hệ thống hạ toàn bộ nền xuống −42 dBFS và **giữ im 4 giây sau câu cuối**. 6 giây sau, hình nhân **xoay 30°** — hậu quả phạm điều Một |
| B12c 😮‍💨 | `area_gac_xep` | Đọc hai trang nhật ký (1976 và 1996) và giấy khai sinh gốc đóng chéo dấu đỏ **ĐÃ KHAI TỬ — SỐ 41/KT — 22.12.1976** | **4** | 7 | Relief tương đối bằng khối lượng đọc. **Khoá L1 bật liên tục** |
| **B13 ★** | `area_gac_xep` | Chín mảnh ván ảnh thờ được xếp lại thành bức ảnh gia phả hoàn chỉnh **nhưng vẫn khuyết đúng một khuôn mặt bị khoét** | **4** | 7 | `fol_gach_van_lat` mỗi nước trượt. Khi còn đúng **một nước** là xong: drone **ngưng thở** (rút về 0 trong 400 ms) và giữ im cho tới khi người chơi trượt nốt |
| B13b 🔔 | `area_gac_xep` | *(Nhánh thất bại — sai 3 lần)* Chín mảnh ván đồng loạt lật úp; lật lại thì **mảnh nào cũng mang một khuôn mặt bị khoét thủng** — `scare_anh_tho_thieu_mat` | **5** | **9** | Xem mục 3.5.6B. Có **luật hoãn** nếu S6 vừa bắn |
| B13a | `area_gac_xep` | Mặt sau khung ảnh: địa chỉ người chơi ở Hà Nội do bà nội ghi năm 1979, và một nét chữ mới viết đè lên — **"Đã gửi giấy báo. 14.8.1996."** | **4** | **8** | **Không dọa.** Một nốt `drn_gac_xep_ep` **lên nửa cung** — thay đổi cao độ **duy nhất trong cả chương** |
| **B14 ★** 🔔 | `area_gac_xep` | Bộ áo cưới giấy khổ người lớn được may **vừa in số đo người chơi**, và khi chiếc áo được khoác lên, **tiếng mõ nổi rền khắp làng** — `scare_ao_cuoi_quay_dau` | **5** | **10** | **DREAD scare**, không impulse. Cái đầu nan tre quay ngược 180° rất chậm, giữ 2,5 giây. Xem Phần 8 |
| B14a | `area_gac_xep` | Đóng chương: đèn dầu lụi hẳn, dưới sân gạch hiện ánh đuốc và đèn pin của người làng kéo vào, **một bóng người lưng còng đứng sẵn ở ngõ tre** | **5** | **10** | `fol_mo_ca_lang_lop` mở từ mono trung tâm ra full stereo, **+9 dB trong 6 giây**. Đây là cú swell **duy nhất được phép vượt −10 dBFS RMS** trong cả chương |

**Dãy mức (thang 1–10):**
`2 → 4 → 9 → 4 → 3 → 5 → 9 → 5 → 4 → 6 → 5 → 8 → 9 → 8 → 5 → 7 → 8 → 5 → (9) → 9 → 7 → 10 → 8 → 7 → 7 → (9) → 8 → 10 → 10`

**Dãy mức (thang 1–5):**
`1 → 2 → 5 → 3 → 2 → 3 → 5 → 3 → 2 → 3 → 3 → 4 → 5 → 4 → 3 → 4 → 4 → 3 → (5) → 5 → 4 → 5 → 4 → 4 → 4 → 4 → 5 → 5`

**Kết luận kiểm tra:** không có ba beat mức 5 liên tiếp; mỗi mức 5 đều được theo sau bởi ít nhất một beat ≤ 4. Hai beat mức 5 cuối cùng (B14, B14a) là **ngoại lệ có chủ ý** — chúng là **một cú duy nhất kéo dài**, đóng chương.

## 6.3. Bảng tổng hợp tám jumpscare

| # | `scare_id` | Area | `trigger_type` (hợp lệ schema) | Điều kiện số học | Loại | `screen_flash` | Thời lượng | SPINE? |
|---|---|---|---|---|---|---|---|---|
| S1 | `scare_bong_trong_chum` | `area_san_gach` | `ON_PUZZLE_FAIL_COUNT` | `max_fails: 3` trên `puz_khoa_bat_quai` | Impulse | **true** | 1200 ms | ✅ |
| S2 | `scare_ban_tay_giay_sau_manh` | `area_hien_nha` | `ON_COLLECT_ITEM` | `item_ban_rap_chu_the`, delay 350 ms, **1 lần duy nhất** | Impulse | **true** | 1100 ms | ✅ |
| S3 | `scare_di_anh_quay_mat` | `area_gian_tho` | `ON_COLLECT_ITEM` | `item_dui_mo`, delay 250 ms, **1 lần duy nhất** | Impulse *(mềm)* | false | 1200 ms | ✅ |
| S4 | `scare_khoi_tu_hinh_nguoi` | `area_gian_tho` | `ON_PUZZLE_FAIL_COUNT` | `max_fails: 3`, **dùng chung** P3 + P4, tối đa 2 lần/chương | **Dread** | false | 1200 ms *(+ static_hold)* | ⚠️ **phái sinh** |
| S5 | `scare_mat_duoi_day_gieng` | `area_bep_gieng` | `ON_PUZZLE_FAIL_COUNT` | `max_fails: 3` trên `puz_thap_lai_den_dau`, tối đa 2 lần/chương | Impulse | **true** | 1000 ms | ✅ |
| S6 | `scare_hinh_nhan_chan_loi` | `area_gac_xep` | `ON_ENTER_AREA` | Lần vào **đầu tiên** duy nhất, delay 900 ms | Impulse | false | 1200 ms | ✅ |
| S7 | `scare_anh_tho_thieu_mat` | `area_gac_xep` | `ON_PUZZLE_FAIL_COUNT` | `max_fails: 3` trên `puz_xep_anh_gia_pha`, tối đa 2 lần/chương | Impulse | **true** | 1200 ms | ⚠️ **phái sinh** |
| S8 | `scare_ao_cuoi_quay_dau` | `area_gac_xep` | `ON_TIMER` | delay **400 ms** từ đầu nhịp 4 của cutscene kết chương | **Dread** | false | 1200 ms *(+ sustain 1300 ms)* | ✅ |

**Cân bằng flash: 4 bật / 4 tắt.**

**Mật độ:** 6–8 cú dọa / 43 phút ≈ **một cú mỗi 5,4–7,2 phút**. Chuẩn ngành cho horror di động phiên ngắn là 4–8 phút/cú — chúng ta nằm giữa.

## 6.4. Ba nguyên tắc dọa bất di bất dịch

| # | Nguyên tắc | Cách kiểm |
|---|---|---|
| 1 | **Dọa bằng vật đời thường sai vị trí, không bằng sinh vật** | Tám cú dọa của chương là: một cái **gáo dừa**, một **bàn tay vàng mã**, một **bó chân nhang**, một **cụm khói**, một **khuôn mặt ngoài cửa bếp**, một **hình nhân nan tre**, **chín mảnh ván ảnh**, một **cái đầu nan tre quay** |
| 2 | **Im lặng đắt hơn tiếng động** | Mọi jumpscare bắt buộc có **≥ 2 000 ms im lặng tuyệt đối** ngay trước nó (`pre_silence_ms ≥ 2000`). **Không ngoại lệ**, kể cả cú dọa lúc vào khu vực. S8 dùng **4 000 ms** |
| 3 | **Người chơi phải tự bấm** | **7/8** cú dọa kích hoạt từ hành động chủ động. Đây không phải mẹo kỹ thuật, đây là **chủ đề**: người chơi tự nguyện từng bước một. Ngoại lệ duy nhất là S6, có lý do cấu trúc |

## 6.5. Nhịp nghỉ được KHOÁ CỨNG BẰNG HỆ THỐNG, không chỉ viết trong kịch bản

Khi bất kỳ khoá nào đang bật, mọi jumpscare bị **HOÃN** (không bị huỷ) và chuyển sang trạng thái `ARMED`.

| Khoá | Điều kiện bật | Thời lượng | Lý do |
|---|---|---|---|
| **L1 — Khoá đọc** | UI đọc tài liệu toàn màn hình đang mở | Suốt thời gian mở **+ 3 000 ms** sau khi đóng | **Dọa người đang đọc = ăn cắp thông tin của họ.** Gian thờ và gác xép là hai phòng đọc, mà lại là hai phòng nhiều scare nhất → khoá này bắt buộc |
| **L2 — Khoá cửa** | Vừa vào một area mới | **15 000 ms** | Ngoại lệ duy nhất: scare có `trigger_type = ON_ENTER_AREA` (`scare_hinh_nhan_chan_loi`) |
| **L3 — Khoá hành trang** | Mở/đóng inventory | **8 000 ms** | Người chơi đang ở "chế độ quản lý", không ở "chế độ hiện diện" |
| **L4 — Khoá gợi ý** | Bảng gợi ý Tier 1/2/3 đang hiện | Suốt thời gian hiện **+ 5 000 ms** | **Người chơi đang bế tắc = đang bực. Dọa lúc bực sinh ra giận, không sinh ra sợ** |
| **L5 — Khoá hồi phục** | Vừa có một scare bắn | **20 000 ms** (nằm trong 90 s cooldown) | Nền kéo về −45 dBFS rồi bò lên. 20 giây người chơi **cần** để tim đập lại bình thường; nếu không có, cú dọa kế tiếp vô nghĩa vì hệ thần kinh chưa reset |

> **Tại sao phải có nhịp nghỉ trước mỗi đỉnh?** Phản xạ giật mình hoạt động trên **độ chênh lệch**, không trên giá trị tuyệt đối. Một cú 90 dB sau 60 giây ở 85 dB gần như không có tác dụng; cũng cú đó sau 2 giây im lặng ở 0 dB thì đủ làm người chơi rơi điện thoại. Vì vậy **nhịp nghỉ không phải là phần thưởng cho người chơi — nó là đạn dược cho cú dọa kế tiếp.** Mỗi 😮‍💨 trong bảng 6.2 là một lần nạp đạn.

## 6.6. Cooldown và cơ chế HOÃN (không phải HUỶ)

```
if (now - t_last_impulse_scare) < 90s  AND  scare.impulse == true:
        scare.state = ARMED        // KHÔNG huỷ, KHÔNG bắn
else:
        FIRE(scare); t_last_impulse_scare = now
```

Một scare ở trạng thái `ARMED` sẽ **bắn ở khoảnh khắc đủ điều kiện kế tiếp**, nhưng chỉ khi **ngữ cảnh diegetic vẫn còn hợp lệ**. Nếu ngữ cảnh đã trôi qua, nó **chuyển sang biến thể dread** và được tiêu thụ.

| Cặp rủi ro | Kịch bản | Xử lý |
|---|---|---|
| **S4 → S3** (`area_gian_tho`) | Sai P3 ba lần (S4 bắn), rồi 40 giây sau nhặt `item_dui_mo` | S3 chuyển sang **biến thể hậu quả im lặng**: nhặt dùi bình thường, **không có gì xảy ra**; nhưng lần kế tiếp camera quét qua bàn thờ, **bảy di ảnh đã quay mặt vào vách rồi**. *Đây là biến thể đáng sợ hơn bản gốc* |
| **S6 → S7** (`area_gac_xep`) | Vào gác (S6 bắn), lao ngay vào P6 và sai 3 lần trong 80 giây | S7 chuyển sang **biến thể câm**: ván vẫn lật úp và lộ chín lỗ khoét, nhưng không flash, không stinger, không haptic, không punch. Sau đó S7 **tự nạp lại** |
| **S7 → S8** (`area_gac_xep`) | Sai P6 lần cuối rồi giải ngay và vào cảnh kết trong 60 giây | **Không xử lý gì** — S8 được **miễn trừ cooldown** vì nó không tạo xung. Nhưng `pre_silence_ms` của S8 tự động nâng **4 000 → 5 500 ms** |

**Luật miễn trừ cooldown (ghi vào validator):** một scare được miễn cooldown **khi và chỉ khi** `impulse == false` **và** `screen_flash == false` **và** `camera_punch_pct == 0` **và** `haptic_pattern_at_0ms == null`. **S8 và S4** là hai scare duy nhất thoả — và S4 vẫn **tự nguyện** tuân thủ cooldown vì nó nằm trong khu vực có scare khác.

**Trần cứng `SCARE_MAX_PER_CHAPTER = 10`.** Người chơi kém nhất có thể gặp: S1×2 + S2 + S3 + S4×2 + S5×2 + S6 + S7×2 + S8 = **13 → vượt trần**. Khi chạm trần, mọi scare còn lại **chuyển vĩnh viễn sang biến thể dread câm** trong phần còn lại của chương. *Người chơi gặp 13 cú dọa trong 45 phút là người chơi đã hết sợ — tiếp tục dọa chỉ làm tài liệu này trở thành thứ nó cấm.*

## 6.7. Quy tắc vàng chống "jumpscare rẻ tiền"

> ## **Một cú dọa chỉ được phép bắn khi ngôi nhà đã nói trước — và người chơi đã bỏ qua lời nói ấy.**
>
> Jumpscare không phải là **nguồn** của nỗi sợ. Nó là **hoá đơn** của nỗi sợ đã được tích luỹ. Nếu chưa có gì được tích luỹ thì không có gì để thanh toán, và cú dọa chỉ là một tiếng động lớn — thứ mà bất kỳ ai cũng làm được, và không ai nhớ.

**Bảy điều kiện — một cú dọa phải đạt CẢ BẢY mới được bắn:**

| # | Điều kiện | Ngưỡng kiểm được |
|---|---|---|
| **Đ1** | Đã có xây dựng không khí trong khu vực | Người chơi ở trong area **≥ 40 giây** và đã tương tác **≥ 2 hotspot**. *(Ngoại lệ duy nhất: `ON_ENTER_AREA` của S6 — bù lại có 20–30 giây leo thang)* |
| **Đ2** | Có audio tell | `tell_asset != null`, vào trước **≥ 4 000 ms**, ở −30 → −36 dBFS |
| **Đ3** | Có im lặng trước | `pre_silence_ms ≥ 2000`. **Không ngoại lệ** |
| **Đ4** | Nguồn dọa là vật đời thường sai vị trí, không phải sinh vật | Kiểm định thủ công trong review nghệ thuật |
| **Đ5** | Người chơi tự bấm | ≥ 7/8 cú dọa kích hoạt từ hành động chủ động |
| **Đ6** | Tôn trọng cooldown ≥ 90 s và các khoá L1–L5 | Kiểm tự động lúc chạy |
| **Đ7** | **Cú dọa trả lại thông tin** | Sau khi cú dọa kết thúc, thế giới **hoặc** hiểu biết của người chơi **phải khác đi**. Nếu gỡ cú dọa ra mà không mất gì → đó là trang trí → **cắt** |

**Bảng kiểm định 8 × 7:**

| Scare | Đ1 xây dựng | Đ2 tell | Đ3 im lặng | Đ4 vật đời thường | Đ5 tự bấm | Đ6 cooldown | Đ7 thông tin trả lại |
|---|---|---|---|---|---|---|---|
| **S1** | ✅ ~3 phút, ≥ 5 hotspot | ✅ nước gợn | ✅ 2000 | ✅ gáo dừa | ✅ ấn then lần 3 | ✅ đầu tiên | ✅ **chỉ vào cái chum** = clue C4 của chính câu đố đang bí |
| **S2** | ✅ ~4 phút ở hiên | ✅ silence tell | ✅ 2000 | ✅ bàn tay **vàng mã** | ✅ hoàn tất nét than cuối | ✅ ≥ 180 s | ✅ vàng mã **đã ở sau bình phong từ đầu** |
| **S3** | ✅ ~6 phút đọc | ✅ chân nhang cọ | ✅ 2000 | ✅ bó chân nhang + di ảnh | ✅ nhặt dùi mõ | ⚠️ có luật hoãn | ✅ **thay đổi vĩnh viễn**: 7 di ảnh úp mặt suốt phần còn lại chương |
| **S4** | ✅ sau ≥ 3 lần sai = ≥ 2 phút | ✅ khói hút ngược | ✅ 2000 | ✅ khói nhang | ✅ ấn "Vái" lần 3 | ✅ | ✅ dạy rằng **cúng sai còn tệ hơn không cúng** — kiến thức dùng lại ở Chapter 2 |
| **S5** | ✅ ~3 phút trong bếp tối | ✅ tiếng tõm lại gần | ✅ 2000 | ✅ khuôn mặt **ngoài cửa bếp** (người, không phải quái) | ✅ mồi lửa sai | ✅ ≥ 240 s | ✅ xác nhận **có người ngoài kia** trước khi người chơi ra sân sau |
| **S6** | ⚠️ ngoại lệ hợp lệ — bù bằng 20–30 s leo thang có tell | ✅ nan tre dịch | ✅ 2000 | ✅ hình nhân nan tre | ❌ **ngoại lệ duy nhất** (1/8, đúng chỉ tiêu) | ✅ ≥ 240 s | ✅ **giới thiệu hình nhân bằng thân thể** — bắt buộc cho twist B14 |
| **S7** | ✅ ≥ 3 phút đọc trên gác | ✅ ván ép nhau | ✅ 2000 | ✅ chín mảnh ván gỗ | ✅ ấn "Áp ảnh vào khung" lần 3 | ⚠️ có luật hoãn | ✅ **trả lời sai lầm bằng nghĩa**: mọi khuôn mặt đều bị khoét |
| **S8** | ✅ toàn bộ 43 phút chương | ✅ giấy chạm vải | ✅ **4000** | ✅ đầu nan tre | ✅ **tự tay khoác áo** | ✅ miễn trừ hợp lệ | ✅ **xác nhận nghi lễ đã thành** — là chính cú twist |

**Kết quả: 8/8 đạt.** Hai ⚠️ là **luật hoãn đã được thiết kế**, không phải lỗ hổng. Một ❌ là **ngoại lệ có chủ đích duy nhất**, đúng chỉ tiêu 7/8.

## 6.8. Danh sách CẤM (áp cho art, audio, code, marketing)

| Cấm | Lý do |
|---|---|
| Quỷ ám kiểu phương Tây, exorcism, thánh giá, nước thánh, linh mục | Sai hệ tín ngưỡng hoàn toàn |
| Búp bê ma kiểu Annabelle, hề ma, gương vỡ có tay thò ra | Cliché nhập khẩu, đã mòn |
| Ma tóc dài trắng bò ra khỏi giếng theo kiểu Nhật | **Cảnh giếng của ta phải chống lại chính liên tưởng này**: giếng Linh An chỉ trả về **một chiếc guốc** và một quầng sáng thứ hai. **Không có gì trèo lên** |
| Mặt ma cận cảnh hốc mắt đen + tiếng hét kim loại | Jumpscare rẻ tiền. Tám cú dọa của ta đều dựa vào **vật thể đời thường lệch vị trí** |
| Máu, nội tạng, xác phân hủy | Sai tông. Đây là *folk horror*, không phải *body horror* |
| Ouija, nến ngũ giác, pentagram, phù thủy | Sai văn hoá |
| Stinger violin/dây cao vút kiểu Hollywood | Thay bằng: **mõ, gỗ, giấy, tre, nước, và im lặng** |
| Nhân vật chính nói to *"Ai đó?"* / *"Có ai ở đây không?"* | Nhân vật của ta nói ít, nói thầm, và chủ yếu **quan sát bằng nghề nghiệp** — cô là thợ may, cô nhìn số đo, đường chỉ, nếp gấp |
| Cú dọa bắn **ngay khi vào area** (trừ S6 đã có lý do cấu trúc) | Người chơi chưa có gì để mất, chưa có gì để tin, chưa có gì để bị phản bội |
| Cú dọa **lặp lại nguyên xi** lần thứ hai | Lần 2 phải là biến thể rút gọn hoặc biến thể câm. **Cú dọa được nhận ra là cú dọa đã chết** |
| Cú dọa **không đổi gì trong thế giới** | Vi phạm Đ7 — đó là trang trí |
| **Fake-out** (giả dọa rồi hoá ra là con mèo) | Tiêu tiền tin cậy của người chơi mà không mua được gì. **Chương này không có một fake-out nào** |
| Flash đỏ bão hoà hoặc flash trắng thuần `#FFFFFF` | Vi phạm luật nhạy sáng. Bảng màu flash của chương chỉ gồm `#FFF2DC`, `#FFE9C4`, `#FFD9A0` |
| Hai cú dọa cách nhau **< 90 giây** | Cú thứ hai không thể hoạt động: hệ thần kinh chưa reset |

## 6.9. Chi tiết dân gian Bắc Bộ BẮT BUỘC dùng (kiểm kê)

| Chi tiết | Xuất hiện ở | Vai trò |
|---|---|---|
| **Chiếu cói** | Khu 2 (chõng) · Khu 3 (vết quỳ trẻ con) · Khu 5 (trải sẵn cho hình nhân) | **Mô-típ lặp ba lần — mỗi lần một nghĩa nặng hơn** |
| **Mâm ngũ quả** | Khu 3 | Quả còn tươi vs bát cơm cúng đã mốc = **hai người khác nhau bày** |
| **Hương vòng** | Khu 3 (treo trên xà) · tay bà Tơ ở cảnh kết | Đồng hồ đếm giờ của cõi âm: một vòng = một ngày đêm |
| **Bát hương bị động** | Khu 3 | Điềm nặng nhất trong tín ngưỡng thờ cúng Bắc Bộ, **không cần một chữ giải thích** |
| **Giấy bản** | Khu 1 (giấy trắng bị hóa trong tro) · Khu 2 (rập chữ) · Khu 5 (hình nhân, áo cưới) | Vật liệu xuyên suốt của cả hủ tục |
| **Áo cưới giấy hàng mã** | Khu 5 | **Vật phẩm nhan đề**, cú chốt của twist |
| **Tiếng mõ** (ba hồi chín tiếng) | Khu 3 (câu đố) · cảnh kết (cả làng) | **Nhịp điệu nhận dạng của game; cũng là "giọng" của Bà Cô** |
| **Giếng khơi** | Khu 4 | Nơi Bà Cô chết; nơi guốc trẻ con còn mắc |
| **Cây gạo** | Khu 4 (ngoài bờ ao) | *Thần cây đa, ma cây gạo* — ranh giới của vùng hồn bị nhốt |
| **Tên tục "cái Đĩ" / "thằng Cu"** | Sổ ghi tên · câu thoại cuối của bà Tơ | Tục đặt tên xấu tránh ma — **bị hủ tục lật ngược thành công cụ xoá danh tính** |
| **Bà đồng** | Bà Tơ — dấu vết khắp chương, hiện hình ở cảnh kết | Nguồn gốc hủ tục, và là phản diện Chapter 2 |
| **Lễ cúng cơm** (bát cơm úp, trứng bổ đôi, đũa bông) | Khu 3 | Dấu hiệu tang trong 49 ngày, và dấu hiệu bị bỏ bê |
| **Đèn dầu Hoa Kỳ, que đóm, tro ủ trấu, kiềng ba chân** | Khu 4 | Chân thực đời sống nông thôn thập niên 1990 |
| **Guốc mộc** | Khu 2 (vừa chân người chơi) · Khu 4 (guốc trẻ con dưới giếng) | **Mô-típ "vừa chân"** — thân thể người chơi khớp với chỗ trống người khác để lại |
| **Khăn xô, cáo phó, hóa vàng, loa phát thanh xã** | Khu 1 | Neo bối cảnh 1996 và trạng thái tang gia |

---

# 7. CHỨNG MINH KHẢ GIẢI (PROOF OF SOLVABILITY)

## 7.1. Mệnh đề

> **Tồn tại ít nhất một thứ tự hành động hợp lệ đưa người chơi từ đầu Chương 1 tới cảnh kết, và tại mỗi bước trong thứ tự đó, mọi điều kiện tiên quyết đều đã được thoả mãn bằng những gì người chơi chắc chắn đang có.**

Chứng minh bằng **kiến thiết** — đưa ra một lộ trình cụ thể (walkthrough đường tối ưu, đánh số bước) và kiểm bất biến sau từng bước. Ký hiệu `INV` = túi đồ sau bước đó.

## 7.2. Walkthrough đường tối ưu — 25 bước

| Bước | Hành động | Điều kiện tiên quyết | Thoả mãn? | `INV` sau bước |
|---|---|---|---|---|
| **1** | Bắt đầu Chương 1 tại `area_san_gach` *(Beat B01)* | Không | ✅ Mặc định | ∅ |
| **2** | `EXAMINE` `hs_guong_bat_quai`, `hs_cau_doi_trai`, `hs_cau_doi_phai`, `hs_chum_nuoc_mua`, `hs_day_phoi_khan_xo` *(Beat B01a–B02)* | Đều `required_item: null` | ✅ | ∅ *(đã nắm clue C1–C5 của P1)* |
| **3** | `ZOOM_PUZZLE` `hs_o_khoa_cong`, giải **P1** với `[6, 3, 8]` *(Beat B03)* | P1 cần **∅** vật phẩm | ✅ Bước 2 đã cấp đủ thông tin (C6 nằm trong khung zoom) | `{chia_khoa_dong}` |
| **4** | `CHANGE_AREA` `hs_cua_vao_hien` → `area_hien_nha` | Cần `item_chia_khoa_dong` | ✅ Có từ bước 3 | `{chia_khoa_dong}` |
| **5** | `COLLECT_ITEM` `hs_giay_ban_va_than`; `COLLECT_ITEM` `hs_den_dau_treo` | Cả hai `required_item: null` | ✅ | `+{giay_ban_va_than, den_dau}` |
| **6** | `EXAMINE` `hs_vo_tap_viet`, `hs_manh_nua`, `hs_guoc_moc`, `hs_nhat_ky_duoi_chieu` *(Beat B04b)* | `null` | ✅ | như trên *(đã nắm bốn phép viết chữ)* |
| **7** | `ZOOM_PUZZLE` `hs_binh_phong`, giải **P2** với `[2, 1, 4, 3, 7, 5, 8, 6]` *(Beat B04)* → `scare_ban_tay_giay_sau_manh` bắn *(B04a)* | Cần `item_giay_ban_va_than` | ✅ Có từ bước 5 | `+{ban_rap_chu_the}` |
| **8** | `USE_ITEM` `hs_o_lom_binh_phong` → then nhả; `CHANGE_AREA` `hs_cua_buc_ban` → `area_gian_tho` *(Beat B05)* | Cần `item_ban_rap_chu_the` | ✅ Có từ bước 7, **và không bị tiêu huỷ** | không đổi |
| **9** | `EXAMINE` `hs_van_khan` (đọc cả **trang 4** về "ba hồi chín tiếng"), `hs_hoanh_phi`, `hs_gia_pha`, `hs_bat_huong` *(Beat B05a)* | `null` | ✅ | không đổi |
| **10** | `ZOOM_PUZZLE` `hs_ban_tho_ho`, giải **P3** với `[3, 6, 4, 1, 5, 2]` *(Beat B06)* | P3 cần **∅** vật phẩm | ✅ Bước 9 đã cấp đủ thông tin | không đổi |
| **11** | `COLLECT_ITEM` `hs_bai_vi_khuyet_danh` *(hotspot spawn nhờ P3)* → nhận bài vị *(Beat B07)* | Khám thờ mở nhờ P3 | ✅ | `+{bai_vi_khuyet_danh}` |
| **12** | `COLLECT_ITEM` `hs_dui_mo` → kích hoạt `scare_di_anh_quay_mat` *(Beat B07a)* | `required_item: null` | ✅ | `+{dui_mo}` |
| **13** | `DIALOGUE` `hs_vach_buong`; `ZOOM_PUZZLE` `hs_mo_ca`, giải **P4** với `[3, 3, 5, 3, 7, 3]` *(Beat B08)* | Cần `item_dui_mo` | ✅ Có từ bước 12 | không đổi |
| **14** | `COLLECT_ITEM` `hs_dai_vai_dieu` *(vải tuột xuống sau P4)* | P4 đã giải | ✅ | `+{dai_vai_dieu}` |
| **15** | `USE_ITEM` `hs_khe_mong_cua_gac` với `item_bai_vi_khuyet_danh` làm then → `flag_then_gac_da_tra = true` | Cần `bai_vi_khuyet_danh` | ✅ Có từ bước 11 | bài vị chuyển sang mục **"Đã dùng"** |
| **16** | `CHANGE_AREA` `hs_cua_hau_xuong_bep` → `area_bep_gieng` *(Beat B09)* | **Đã giải P3** | ✅ Từ bước 10 | không đổi |
| **17** | `COLLECT_ITEM` `hs_chai_dau_hoa`; `EXAMINE` `hs_gac_bep_bo_dom`, `hs_vach_bep_chu_than`, `hs_dong_tro_than`, `hs_cot_bep_vach_dao`, `hs_so_cho_ba_noi` *(Beat B09a–B09b)* | Đều `null` | ✅ | `+{chai_dau_hoa}` |
| **18** | `ZOOM_PUZZLE` `hs_den_dau_ghep`, giải **P5** với `[2, 5, 1, 3, 4]` *(Beat B10)* | Cần `den_dau` (b.5) + `dai_vai_dieu` (b.14) + `chai_dau_hoa` (b.17) | ✅ **Cả ba đều có** | `−{den_dau, dai_vai_dieu, chai_dau_hoa}` `+{den_dau_sang}` |
| **19** | `USE_ITEM` `hs_gieng_khoi` với `item_den_dau_sang` — soi lòng giếng; `EXAMINE` `hs_thanh_gieng_chu_khac` *(Beat B11)* | `required_item: item_den_dau_sang` | ✅ Có từ bước 18 | không đổi |
| **20** | `CHANGE_AREA` `hs_len_gian_tho` → `area_gian_tho` | **Không gate** — luôn mở | ✅ | không đổi |
| **21** | `CHANGE_AREA` `hs_cau_thang_gac` → `area_gac_xep`; vào khu vực → `scare_hinh_nhan_chan_loi` *(Beat B12, B12a)* | Cần `den_dau_sang` (b.18) **VÀ** `flag_then_gac_da_tra` (b.15) | ✅ **Cả hai đều có** | không đổi |
| **22** | `EXAMINE` `hs_hom_go_nap` (2 trang), `hs_so_ghi_ten`, `hs_nhat_ky_trang_cuoi`, `hs_giay_khai_sinh`; dùng nút **"Lật mảnh"** xem mặt sau các mảnh ván *(Beat B12b–B12c)* | Đều `null` | ✅ | không đổi |
| **23** | `ZOOM_PUZZLE` `hs_khung_anh_tho`, giải **P6** với `[2, 5, 7, 4, 8, 3, 6, 1, 0]` *(Beat B13)* | Cần `item_den_dau_sang` | ✅ Có từ bước 18 | không đổi |
| **24** | `COLLECT_ITEM` `hs_ao_cuoi_giay` *(hotspot spawn sau P6)*; đọc mặt sau khung ảnh *(Beat B13a)* → `flag_ao_cuoi_da_nhat = true` → **`hs_xuong_gian_tho` khoá vĩnh viễn** | P6 đã giải | ✅ | `+{ao_cuoi_giay}` |
| **25** | `USE_ITEM` `hs_hinh_nhan` với `item_ao_cuoi_giay` → cutscene `seq_ending_ch01_khoac_ao` + `scare_ao_cuoi_quay_dau` *(Beat B14 → B14a)* | Cần `item_ao_cuoi_giay` | ✅ Có từ bước 24 | **KẾT CHƯƠNG 1** |

## 7.3. Năm bổ đề bảo đảm tính đúng đắn của chứng minh

### Bổ đề 1 — Không bước nào tiêu huỷ tiền đề của bước sau

Chỉ có **hai** vật phẩm bị "đặt xuống":

| Vật phẩm | Bước | Số phận | Có phá tiền đề sau không? |
|---|---|---|---|
| `item_ban_rap_chu_the` | 8 | **Lấy lại được** sau khi then nhả — ràng buộc đã ghi ở mục 4.3 #4 | **Không** — vẫn còn trong túi cho clue C4 của P6 |
| `item_bai_vi_khuyet_danh` | 15 | **Ở lại vĩnh viễn** làm then, chuyển sang mục "Đã dùng" | **Không** — không câu đố nào sau bước 15 cần tới nó (P6 chỉ cần đèn sáng) |

Ba nguyên liệu của P5 (`den_dau`, `dai_vai_dieu`, `chai_dau_hoa`) bị tiêu ở bước 18, nhưng chúng **không xuất hiện trong bất kỳ tiền đề nào sau bước 18**.

⇒ **Bất biến "tiền đề luôn còn nguyên" được giữ.** ∎

### Bổ đề 2 — Không câu đố nào có thể làm người chơi mất tiến độ vĩnh viễn

| Câu đố | Khi sai | Có tài nguyên hữu hạn? |
|---|---|---|
| P1 | Ba vòng quay về vị trí cũ, thử lại vô hạn | Không |
| P2 | Tốn giấy, **nhưng xấp giấy tự nạp lại đầy 3 tờ khi hết** | Không (hữu hạn giả) |
| P3 | 6 icon trả về bàn, thử lại vô hạn | Không |
| P4 | Làm lại từ hồi 1, thử lại vô hạn; nghe lại mẫu vô hạn | Không |
| P5 | **Giữ nguyên các bước đã đúng**, dầu không hao | Không |
| P6 | **Giữ nguyên bố cục**, không bao giờ xáo lại bàn cờ | Không |

Jumpscare chỉ là hiệu ứng nghe-nhìn: **không trừ tài nguyên, không khoá thao tác, không đổi `solution`, không đổi `max_fails`**.

⇒ **Số lần thử là vô hạn ở mọi câu đố.** ∎

### Bổ đề 3 — Mọi khu vực đều quay lui được

Bảng cổng ở mục 4.4 cho thấy **4/4 cổng đi đều có cạnh lùi luôn mở** (E2, E4, E6, E8). Cạnh lùi duy nhất bị khoá là **E8 sau bước 24** — và tại thời điểm đó **chỉ còn đúng một hành động khả dụng để kết chương** (bước 25), nên không cần quay lui.

Thêm lưới an toàn: nút **"Về gian thờ"** trong menu, mở sau khi vào hub lần đầu.

⇒ **Người chơi đi lệch lộ trình trên (ví dụ xuống bếp trước khi giải P4) LUÔN quay lại được để lấy thứ còn thiếu ⇒ không tồn tại trạng thái chết.** ∎

### Bổ đề 4 — P6 luôn giải được về mặt toán học

Bài toán 8-puzzle chia không gian trạng thái thành **hai lớp tương đương không thông nhau** (bất biến chẵn-lẻ của hoán vị). Vì trạng thái ban đầu được sinh bằng cách **áp 60–80 nước đi hợp lệ ngẫu nhiên từ chính trạng thái đích**, nó **luôn nằm cùng lớp với đích**.

⇒ **Luôn tồn tại chuỗi nước đi tới lời giải.** Đây là **ràng buộc triển khai bắt buộc, không phải khuyến nghị** — nếu dùng hoán vị ngẫu nhiên tự do thì **50 % số ván không giải được**. ∎

### Bổ đề 5 — Mọi lời giải đều suy ra được, không cần đoán mò

| Câu đố | Không gian tìm kiếm thô | Clue thu hẹp về | Kết luận |
|---|---|---|---|
| P1 | 8³ = **512** | C1–C6 xác định **duy nhất** một bộ ba | ✅ |
| P2 | 8! = **40 320** | Bốn phép trong C1 xác định **duy nhất** một thứ tự | ✅ |
| P3 | 6! = **720** | Văn khấn C1 cho **chuỗi quan hệ trước-sau đầy đủ** | ✅ |
| P4 | tổ hợp nhịp | **Hai đường độc lập**: nghe lại vô hạn (C1) **hoặc** đọc 三五七 + cấu trúc (C2+C3) | ✅ |
| P5 | 5! = **120** | Bốn ràng buộc thứ tự từ C1+C2 rút về **duy nhất** một chuỗi | ✅ |
| P6 | 9!/2 = **181 440** | C1 (ngôi thứ) + C2 (danh tính từng mảnh) xác định **duy nhất** một bố cục | ✅ |

⇒ **Không câu đố nào bắt người chơi thử mò.** Và không câu đố nào đòi kiến thức ngoài đời (phong thuỷ, Hán tự, lễ nghi) — **mọi quy tắc cần thiết đều nằm trong game và nhất quán với nhau**. ∎

## 7.4. Điểm rủi ro duy nhất của chương và biện pháp bảo đảm

**Vấn đề:** cổng xuống bếp (E5) chỉ đòi **giải P3**. Người chơi có thể **bỏ qua P4** (không nhặt dùi mõ / không gõ mõ), xuống bếp, và khi đó **thiếu `item_dai_vai_dieu`** → không ghép được đèn → P5 tắc.

**Vì sao đây KHÔNG phải soft-lock:** `hs_len_gian_tho` (bếp → gian thờ) **luôn mở**; người chơi quay ngược lên gian thờ làm P4 bất cứ lúc nào. Trạng thái vẫn **khả giải 100 %**, chỉ là người chơi có thể **bối rối**.

**Ba biện pháp bắt buộc:**

| # | Biện pháp | Chi tiết |
|---|---|---|
| 1 | **Thông báo thiếu đồ có chỉ dẫn** | Chạm `hs_den_dau_ghep` khi thiếu → `txt_khoa_ghep_den_thieu_do` liệt kê **đích danh** thứ còn thiếu: *"Có thân đèn, có chai dầu. Nhưng bầu đèn không có tim thì dầu nằm im. Phải tìm một mảnh vải dày, xé ra se được thành sợi."* |
| 2 | **Neo clue sớm** | C3 của P5 (`hs_den_dau_treo` lúc nhặt đèn ở **khu vực thứ 2**) đã nêu **đủ ba thứ còn thiếu** ngay từ đầu chương |
| 3 | **Kéo P4 vào nhịp bắt buộc về mặt tường thuật** | Tiếng mõ sau vách phát **lặp lại theo chu kỳ 25 giây** khi người chơi đứng trong `area_gian_tho` và chưa giải P4 — người chơi khó lòng rời gian thờ mà không xử lý nó. Beat B08 nằm **trước** Beat B09 đúng theo SPINE |

**Khuyến nghị bổ sung (tuỳ Lead duyệt):** thêm điều kiện kép cho `hs_cua_hau_xuong_bep` — yêu cầu **giải cả P3 và P4** mới mở cửa hậu.
*Ưu điểm:* triệt tiêu hoàn toàn rủi ro bối rối, khớp chính xác thứ tự Beat B08 → B09 của SPINE. *Nhược điểm:* giảm tự do.
**Thiết kế hiện tại không cần điều này để đúng — nhưng nếu playtest cho thấy tỉ lệ quay lui > 20 % thì bật lên.**

## 7.5. Kiểm thử khôi phục save — 12 điểm bắt buộc

Thử nghiệm bắt buộc trước khi bàn giao QA: **tắt app đột ngột (kill process) tại 12 điểm dưới đây, mở lại, phải khôi phục đúng 100 %.**

| # | Điểm kiểm tra | Cờ phải đúng |
|---|---|---|
| 1 | Vừa vào sân gạch, chưa làm gì | `current_area_id`, `save_version`, `chapter_id` |
| 2 | Đang xoay ổ khoá, vòng đã đặt 6-3-x | `puzzle_progress.puz_khoa_bat_quai.rings` |
| 3 | Vừa sai ổ khoá lần 2 | `puzzle_fail_count` |
| 4 | Vừa bị `scare_bong_trong_chum` | `seen_scare_bong_trong_chum`, `puzzle_fail_count` (đã reset về 0) |
| 5 | Cầm chìa khoá, chưa mở cửa | `inventory`, `puz_khoa_bat_quai_solved` |
| 6 | Đã tra bản rập, chưa vào gian thờ | `inventory`, `flag_binh_phong_da_tra`, `used_hotspots` |
| 7 | Vừa hoá vàng xong, chưa nhặt bài vị | `puz_tuan_tu_le_cung_solved` + cờ spawn `hs_bai_vi_khuyet_danh` |
| 8 | Đã nhặt bài vị và vải điều | `inventory`, `collected_hotspots` |
| 9 | Đèn đã thắp, chưa soi giếng | `inventory`, `puz_thap_lai_den_dau_solved`, `flag_gieng_da_soi` |
| 10 | Đang xếp ảnh 3×3 dở dang | `puzzle_progress.puz_xep_anh_gia_pha.tiles` — **bắt buộc lưu**; bắt người chơi xếp lại từ đầu 240 giây là **lý do bỏ game số một** |
| 11 | Đã nhặt áo cưới — **point of no return** | `flag_ao_cuoi_da_nhat`, `collected_hotspots`, và `hs_xuong_gian_tho` **phải khoá** |
| 12 | Cutscene kết chương chạy được nửa chừng | `flag_chapter_01_completed = false`; cutscene phải **phát lại từ đầu** khi mở app — **không cho bỏ qua nhịp twist** |

---

# 8. KẾT CHƯƠNG VÀ HOOK SANG CHAPTER 2

## 8.1. Cảnh kết — `seq_ending_ch01_khoac_ao`, kịch bản quay từng nhịp

| Trường | Giá trị |
|---|---|
| Tên cảnh | `seq_ending_ch01_khoac_ao` |
| Địa điểm | `area_gac_xep` |
| Khởi động bởi | `hs_hinh_nhan` · `USE_ITEM` · `required_item: item_ao_cuoi_giay` |
| Thời lượng | **95–110 giây** · **không bấm bỏ qua được sau nhịp 3** |
| Jumpscare gắn kèm | `scare_ao_cuoi_quay_dau` — `ON_TIMER`, delay **400 ms** tính từ đầu **nhịp 4** |

---

**NHỊP 1 — Hành động (người chơi tự bấm).**
Người chơi kéo `item_ao_cuoi_giay` từ hành trang, thả lên `hs_hinh_nhan`. **Không có hộp thoại xác nhận. Không có cảnh báo.** Con trỏ chỉ đổi thành hình bàn tay.

`[[ Nếu flag_da_doc_bay_dieu_cam_ky = true, chèn thêm một nhịp phụ 2 giây: dòng chữ "Điều thứ bảy…" hiện mờ rồi tan, trước khi hai bàn tay đưa áo lên. KHÔNG cho người chơi lựa chọn dừng lại — đây là điểm mấu chốt của chủ đề. ]]`

---

**NHỊP 2 — Bốn giây im lặng tuyệt đối.**
Toàn bộ âm nền **cắt phẳng về 0**, kể cả `fol_den_dau_chay` (tiếng đèn dầu). Trên màn hình chỉ có động tác **hai bàn tay người chơi luồn tay áo giấy qua hai cánh tay nan tre của hình nhân, vuốt lại cổ áo**. Âm thanh duy nhất: `fol_giay_miet_tre` ở −24 dBFS — **giấy miết vào tre**.

`[[ fol_giay_miet_tre PHẢI ghi thật, không tổng hợp. Đây là âm thanh duy nhất của nhịp này. ]]`

---

**NHỊP 3 — Độc thoại.**

> **`txt_ending_doc_thoai_01`**
> "Vai vừa. Tay vừa.
> Mình vuốt lại cái cổ áo cho nó ngay ngắn — kiểu vuốt mà chị Bảy vẫn dạy mình làm cho khách, trước khi khách soi gương."

`[[ Thì thầm, −22 dBFS, dry 100 %, không reverb. Đây là chỗ nghề nghiệp của nhân vật đóng đinh chủ đề: cô là thợ may, và cô đang làm đúng nghề của mình cho một hình nhân. ]]`

---

**NHỊP 4 — `scare_ao_cuoi_quay_dau`. DREAD SCARE.**

| Mốc | Nội dung |
|---|---|
| **0 ms** | Cái đầu nan tre **bắt đầu quay** — góc 0° → 180°, đường cong **tuyến tính tuyệt đối** (không ease-in, không ease-out: **chuyển động máy móc, không sinh học**). **Camera tĩnh hoàn toàn: không punch, không shake, không tilt. Không flash. Độ sáng không đổi một chút nào.** `sfx_scare_dau_nan_quay.ogg` — tiếng nan tre nghiến, attack **300 ms**, **không transient**, −15 dBTP, trải đều suốt 1200 ms. **Không haptic ở 0 ms** |
| **200 ms** | 30°. Bắt đầu thấy cạnh mặt |
| **600 ms** | **90° — đúng cạnh, mặt gần như biến mất**, chỉ thấy vành nan tre mỏng. **Khung hình khó chịu nhất.** Tiếng nghiến to nhất tại đây. `hap_long_rumble` 220 ms, **0.20** — cực khẽ, đặt ở 600 ms nên **không phải cú giật** |
| **1200 ms** | **180°.** Mặt than hai chấm một vạch **nhìn thẳng vào người chơi**. **Envelope kết thúc.** Tiếng nghiến dứt đúng 1200 ms |
| **1200 → 2500 ms** *(sustain shot)* | **Bất động tuyệt đối. Không một pixel đổi.** Camera tĩnh. **Im hoàn toàn** — không nhạc, không nền, không thở. **Dài đến mức khó chịu** |

> **Vì sao đây là cú dọa CHẬM:** đây là cú dọa duy nhất mà người chơi **đã tự tay hoàn tất một nghi lễ** để kích hoạt. Mọi cú dọa trước là **phản ứng** của ngôi nhà; cú này là **xác nhận**. Một cú giật 80 ms sẽ biến hai mươi năm hủ tục thành một trò giật mình. Người chơi **không được phép giật mình rồi quên — họ phải nhìn**. Chương phải đóng lại bằng **bất an**, không phải bằng **nhẹ nhõm**. *Nhẹ nhõm giết hook sang Chapter 2.*

> **Hoà giải trần 1200 ms:** kịch bản yêu cầu giữ **2,5 giây**; tài liệu kinh dị giới hạn envelope **1 200 ms**. Hai điều này **không mâu thuẫn** — chúng là hai lớp khác nhau: **envelope jumpscare** (0 → 1200 ms, cái đầu quay + tiếng nan tre nghiến) tính vào trần; **sustain shot** (1200 → 2500 ms, đầu đã quay xong, hoàn toàn bất động, không âm thanh mới) **không tính** vì đó là **một cú máy tĩnh, không phải một sự kiện dọa**. Nguyên tắc chung áp cho toàn dự án: **trần 1200 ms áp cho sự kiện, không áp cho khung hình.**

---

**NHỊP 5 — Tiếng mõ.**
Một tiếng mõ. Rồi tiếng thứ hai từ hướng khác. Rồi ba, bốn, mười — **từ khắp làng**, chồng lớp lên nhau, lệch nhịp nhau, **không còn ra tiết tấu ba hồi chín tiếng nữa**, chỉ còn là một khối tiếng gỗ dày đặc.
Mix: `fol_mo_ca_lang_lop` mở từ **mono trung tâm ra full stereo, +9 dB trong 6 giây** — cú swell **duy nhất được phép vượt −10 dBFS RMS** trong cả chương.

> **`txt_ending_doc_thoai_02`**
> "Mõ.
> Không phải một cái. Nhà thờ họ, chùa làng, điếm canh, từ đường bên kia ao.
> **Cả làng đang gõ.**"

---

**NHỊP 6 — Đèn tắt.**
Ngọn đèn dầu trong tay người chơi **lụi dần chứ không phụt tắt** — **tim đèn tự tụt xuống**. Màn hình tối dần trong 3 giây, chỉ còn một vệt sáng lọt qua khe ván sàn gác.

`[[ Chi tiết đắt: tim đèn tự tụt xuống là hành động NGƯỢC với bước 4 của puz_thap_lai_den_dau mà người chơi vừa tự tay làm. Ngôi nhà đang tháo lại cái lễ, từng bước một. ]]`

---

**NHỊP 7 — Nhìn xuống qua khe ván.**
Camera hạ, nhìn xuyên khe ván sàn xuống sân gạch bên dưới. Trên sân, **ánh đuốc và đèn pin** lần lượt hiện ra — bảy, tám, rồi hơn chục đốm sáng, **xếp thành hai hàng dọc hai bên sân, không ai nói một câu nào**.

Ở đầu ngõ tre, tách khỏi hai hàng, có **một bóng người nhỏ, lưng còng, khăn mỏ quạ**, tay cầm **một nắm hương vòng đang cháy đỏ**.

> **`txt_ending_doc_thoai_03`**
> "Cổng vẫn khóa trái. Mà sân thì đầy người."

---

**NHỊP 8 — Câu thoại có lời DUY NHẤT của Chapter 1.**
Giọng bà đồng Tơ: già, khàn, **bình thản như người gọi cháu vào ăn cơm**. `vox_ba_to_ket_chuong`, −18 dBFS, **không vang, không xử lý reverb, dry tuyệt đối** — dù bà đứng dưới sân, tiếng nghe như **ngay sau lưng người chơi**.

> **`txt_ending_thoai_ba_to`**
> "Về rồi đấy à.
> **Cái Đĩ Con.**"

`[[ Đây là lần thứ ba và cũng là lần cuối cái tên "bà Tơ" / giọng bà Tơ xuất hiện trong chương. Và đây là lần đầu tiên trong đời người chơi nghe ai gọi tên tục của mình. QUY TẮC KHÔNG ĐƯỢC VI PHẠM: Bà Cô không bao giờ nói. Câu thoại duy nhất của chương là của MỘT NGƯỜI SỐNG. ]]`

---

**NHỊP 9 — Cắt đen.**
Cắt phẳng sang đen. Âm thanh cắt cùng lúc, **trừ một tiếng mõ cuối cùng ngân trong khoảng đen**.

---

**NHỊP 10 — Thẻ kết chương.**
Trên nền đen, chữ trắng, font viết tay `hw_ba_noi`, hiện từng dòng một:

> **`txt_ending_card_ch01`**
>
> **CHƯƠNG MỘT — HẾT**
>
> *Lễ đã thành.*
> *Còn ba ngày nữa mới đến lễ rước.*

---

**KHUNG HÌNH CUỐI CÙNG SAU THẺ KẾT CHƯƠNG** *(post-card stinger, 6 giây)*

Mở lại trên nền đen. Tiếng ván sàn gác kêu một cái. Ánh sáng xám của rạng đông lọt qua khe mái.

Trên **chiếc chiếu cói trải sẵn** giữa sàn gác, **hình nhân mặc áo cưới giấy đã nằm xuống, ngay ngắn, tay xếp trước bụng** — đúng phép: *lễ xong thì đặt hình nhân nằm, phủ vải, để đấy ba ngày.*

Camera đẩy chậm vào mặt hình nhân. Mặt than hai chấm một vạch **đã bị xóa đi**, thay bằng một mảnh giấy dán đè lên — và trên mảnh giấy ấy là **khuôn mặt bị khoét khỏi bức ảnh thờ, dán vừa khít**.

Cắt đen. Hết.

## 8.2. Trạng thái người chơi khi đóng chương (bàn giao sang Chapter 2)

| Trường | Giá trị khi kết Chapter 1 |
|---|---|
| Vị trí | `area_gac_xep`, gác xép **bị khóa lại từ dưới** |
| Hành trang giữ lại | `item_den_dau_sang` *(đã tắt)* · `item_ban_rap_chu_the` · `item_giay_ban_va_than` |
| Hành trang mục "Đã dùng" | `item_bai_vi_khuyet_danh` *(ở lại làm then cửa gác)* |
| Hành trang mất vĩnh viễn | `item_ao_cuoi_giay` *(đã dùng)* |
| Cờ trạng thái | `flag_chapter_01_completed = true` · `flag_le_da_thanh = true` · `flag_biet_ten_that = true` · `flag_da_doc_bay_dieu_cam_ky` *(true/false tuỳ người chơi)* · `flag_da_dap_loi_ba_noi` *(true/false)* · `flag_da_doc_phieu_do` *(true/false)* · `dialogue_choices` |
| **Điều người chơi ĐÃ biết** | Tên thật (Nguyễn Thị Liên) · việc bị khai tử số 41/KT · bốn đời người thế mạng · sự tồn tại của bà Tơ · toàn bộ bảy phần của lễ thế mệnh |
| **Điều người chơi CHƯA biết** | Bà Cô chết vì **bị ép gả** hay **tự nhảy giếng** · chuyện gì xảy ra với Nhài và Tý **sau khi "lễ thành"** · **"lễ rước" là gì** · vì sao chỉ có **một** hình nhân trên gác |

`[[ flag_da_doc_bay_dieu_cam_ky KHÔNG đổi kết cục Chapter 1, nhưng Chapter 2 dùng nó để đổi một nhánh thoại với bà Tơ: nếu người chơi ĐÃ đọc Bảy Điều, bà Tơ nói "vậy là cháu biết rồi mà cháu vẫn khoác" — nặng hơn nhiều so với nhánh còn lại. ]]`

`[[ flag_da_dap_loi_ba_noi = true nghĩa là người chơi đã VI PHẠM ĐIỀU CẤM KỴ THỨ TƯ (chớ đáp lời ai gọi từ sau lưng). Không phạt ở Chương 1; Chapter 2 tính sổ. ]]`

## 8.3. Hook sang Chapter 2

**Tên chương 2 (tạm):** *LINH AN THÔN — Chương 2: **LỄ RƯỚC***

Hook được gieo bằng **ba mũi**, theo thứ tự người chơi gặp:

| Mũi | Nội dung | Vì sao nó kéo được người chơi đi tiếp |
|---|---|---|
| **1 — Câu hỏi chưa trả lời, đặt ngay trong Chapter 1** | Sổ ghi tên viết *"Lễ thành"* cho Nhài (1961) và Tý (1968). Nhưng **chiếc guốc của Tý vẫn còn dưới giếng**, và **hình nhân trên gác chỉ có một**. Nếu lễ đã thành thì **hình nhân của hai đứa kia đâu?** Người chơi đã cầm đèn soi khắp gác và không thấy | Đây là mồi kéo **do chính người chơi tự phát hiện**, không do game nói ra. Người chơi tinh ý sẽ mang câu hỏi này sang Chapter 2 mà không cần ai nhắc |
| **2 — Thẻ kết chương** | *"Còn ba ngày nữa mới đến lễ rước."* Một câu, ba thông tin mới: **lễ chưa xong** · có **thời hạn** · có **một nghi thức thứ hai tên là lễ rước** | Chapter 1 kết ở trạng thái **lễ thành nhưng chưa "giao hàng"** — trạng thái căng nhất có thể |
| **3 — Post-card stinger** | Hình nhân **đã tự nằm xuống chiếu**, và mặt nó **đã được dán khuôn mặt bị khoét khỏi bức ảnh thờ** | Xác nhận thị giác cuối cùng: **hình nhân bây giờ có mặt của người chơi**. Từ giờ nó không còn là "một hình nhân" — nó là **cô** |

**Nội dung Chapter 2 mà hook này mở ra:**

| Trục | Chapter 1 | Chapter 2 |
|---|---|---|
| **Quy mô** | Một ngôi nhà (5 khu vực trong nhà) | **Cả làng**: nhà thờ họ, chùa làng, điếm canh, gốc **cây gạo**, nghĩa trang đồng Sau, và **giếng khơi trở lại như một địa điểm chính** chứ không còn là hotspot |
| **Đối thủ** | Vô hình — một thủ tục, một ngôi nhà | **Hữu hình: bà đồng Tơ và dân làng** — những người sống, đang làm một việc họ tin là đúng |
| **Mục tiêu người chơi** | *Đi vào và tìm hiểu* | **Đảo chiều: đi ra và tìm cách phá lễ** — trong khi **mọi lối ra đều đã được khóa hướng từ chiều hôm trước, bằng chính ổ khóa bát quái mà người chơi tự tay mở** |
| **Nhịp kinh dị** | Dread nền + 8 cú dọa vật đời thường | Áp lực đám đông; cái đáng sợ không còn là một hồn ma mà là **một cộng đồng cùng gật đầu** |

---

# PHỤ LỤC A — CHỈ MỤC KHOÁ LOCALIZATION

**Quy ước:** `txt_examine_*` (EXAMINE) · `txt_thoai_*` (DIALOGUE) · `txt_khoa_*` (fallback khi chưa đủ điều kiện) · các khoá độc thoại / lore / cảnh kết giữ tên mô tả.
**File nguồn:** `Localization/vi-VN/chapter_01.json`. **Không hard-code chuỗi trong scene.**

| Nhóm | Khoá |
|---|---|
| **`area_san_gach`** | `txt_examine_guong_bat_quai` · `txt_thoai_loa_phat_thanh` · `txt_examine_cau_doi_trai` · `txt_examine_cau_doi_phai` · `txt_examine_cao_pho` · `txt_examine_khan_xo` · `txt_examine_xe_dap_tui_vai` · `txt_examine_chum_nuoc` · `txt_examine_gao_dua` · `txt_examine_dong_tro_hoa_vang` · `txt_examine_khe_gach_thu_tay` · `txt_khoa_cua_vao_hien` · `txt_san_gach_doc_thoai_mo_dau` · `txt_san_gach_cao_pho_doc_thoai` · `txt_san_gach_cau_doi_doc_thoai` · `txt_san_gach_dong_tro_hint` |
| **`area_hien_nha`** | `txt_examine_manh_nua` · `txt_examine_vo_tap_viet` · `txt_examine_chong_tre` · `txt_examine_nhat_ky_1976` · `txt_examine_guoc_moc` · `txt_khoa_binh_phong_thieu_giay` · `txt_khoa_cua_buc_ban` · `txt_hien_nha_chu_than_sau_binh_phong` · `txt_hien_nha_nhan_giay_ban` · `txt_hien_nha_doc_thoai_the_menh` |
| **`area_gian_tho`** | `txt_examine_hoanh_phi` · `txt_examine_huong_vong` · `txt_examine_kham_tho` · `txt_examine_gia_pha` · `txt_examine_bat_huong` · `txt_examine_van_khan` *(4 trang)* · `txt_examine_chieu_coi` · `txt_thoai_vach_buong` · `txt_khoa_mo_ca_thieu_dui` · `txt_khoa_khe_mong_cua_gac` · `txt_khoa_cua_hau` · `txt_khoa_cau_thang_gac` · `txt_gian_tho_gia_pha_doc_thoai` · `txt_gian_tho_bai_vi` · `txt_gian_tho_bai_vi_doi_chieu` |
| **`area_bep_gieng`** | `txt_examine_so_cho` · `txt_examine_gac_bep` · `txt_examine_cay_gao` · `txt_examine_gau_ton` · `txt_examine_thanh_gieng` · `txt_examine_vach_bo_hong` · `txt_examine_vach_bep_chu_than` · `txt_examine_cot_vach_dao` · `txt_examine_kieng_ba_chan` · `txt_examine_dong_tro_than` · `txt_khoa_ghep_den_thieu_do` · `txt_khoa_gieng_toi` · `txt_bep_gieng_so_cho_doi_chieu` · `txt_bep_gieng_cot_vach_dao_doc_thoai` · `txt_bep_gieng_thanh_gieng_doc_thoai` · `txt_bep_gieng_guoc_tre_con` |
| **`area_gac_xep`** | `txt_thoai_khe_van_san` · `txt_examine_nhat_ky_1996` · `txt_examine_so_ghi_ten` · `txt_examine_nap_hom` *(2 trang: gia phả + Bảy Điều)* · `txt_examine_vang_ma` · `txt_examine_giay_khai_sinh` · `txt_examine_chieu_moi` · `txt_khoa_gac_xep_toi_qua` · `txt_khoa_hinh_nhan_chua_co_ao` · `txt_khoa_gac_xep_sap_cua` · `txt_gac_xep_so_ghi_ten_doc_thoai` · `txt_gac_xep_nhat_ky_1976` · `txt_gac_xep_khai_sinh_doc_thoai` · `txt_gac_xep_anh_hoan_chinh` · `txt_gac_xep_sau_khung_anh` · `txt_gac_xep_ao_cuoi_giay` |
| **Lore & cảnh kết** | `txt_lore_loi_phan_1953` · `txt_deja_vu_01` · `txt_deja_vu_02` · `txt_deja_vu_03` · `txt_ending_doc_thoai_01` · `txt_ending_doc_thoai_02` · `txt_ending_doc_thoai_03` · `txt_ending_thoai_ba_to` · `txt_ending_card_ch01` |

**Ràng buộc localization:**

| # | Ràng buộc |
|---|---|
| 1 | Mỗi khoá phải có cả bản `vi-VN` (**bản gốc, ưu tiên tuyệt đối**) và slot `en-US` để dịch sau |
| 2 | **Không dùng dấu ngoặc kép cong** trong chuỗi JSON; dùng `\"` hoặc dấu nháy đơn để tránh vỡ parser |
| 3 | Chuỗi dài nhất (`txt_examine_van_khan`, `txt_examine_nap_hom`) được **chia nhiều trang đọc**, mỗi trang **≤ 220 ký tự** để vừa khung đọc màn hình 6.1" |
| 4 | Ước lượng ~9 800 ký tự tiếng Việt cho Chapter 1 — nằm gọn trong một bundle localization remote **dưới 64 KB** |

---

# PHỤ LỤC B — BÀN GIAO SANG CÁC DELIVERABLE KHÁC

| Tài liệu đích | Tài liệu này cung cấp gì |
|---|---|
| `docs/02_PROMPT_DO_HOA.md` | Bảng màu và mô tả khung hình mở của từng khu vực (mục 3.x.1 và 3.x.2); bố cục ba lớp BG/MG/FG; mô tả hình nhân, áo cưới giấy, bài vị khuyết danh, bức ảnh khuyết mặt; danh sách sprite jumpscare cần vẽ kèm biến thể `_soft` và `_static` |
| `docs/03_DATA_SPEC.md` | Toàn bộ bảng hotspot + bounds (mục 3.x.3); chỉ mục `text_key` (Phụ lục A); ánh xạ puzzle ↔ reward ↔ jumpscare (mục 5.1–5.2); bảng cổng khu vực (mục 4.4); ánh xạ `trigger_type` (mục 0.5) |
| `data/areas/*.json` | **5 area · 10 item · 6 puzzle · 6 (+2 phái sinh) jumpscare** — id lấy **nguyên từ SPINE**, không phát sinh id mới. Bounds lấy nguyên từ mục 3.x.3 |
| `data/chapter_01.json` | Thứ tự area 1 → 5 và điều kiện gate (mục 1.6 và 4.4) |
| `docs/04_LIVEOPS_MONETIZATION.md` | Điểm bế tắc tự nhiên để đặt gợi ý có thưởng: `puz_khoa_bat_quai` (60 s) · `puz_rap_chu_the_menh` (hỏng 3 tờ) · `puz_ba_hoi_chin_tieng` (sai 2 hồi) · `puz_xep_anh_gia_pha` (90 s). **RÀNG BUỘC CỨNG: Tier 3 luôn có đường mở miễn phí bằng thời gian chờ 300 s; không tuỳ chọn an toàn nào được đặt sau tường trả phí** |
| `docs/05_TICH_HOP_UNITY_ADDRESSABLES.md` | Ranh giới nhóm bundle theo khu vực; `area_gac_xep` nặng nhất (hình nhân + áo cưới + 9 mảnh ván + ảnh thờ) → **preload từ lúc người chơi bước vào `area_bep_gieng`**; ~18,8 MB âm thanh chia 8 nhóm |
| `schema/level.schema.json` · `tools/validate_level.py` | 18 luật kiểm ở mục 5.5; ràng buộc sinh trạng thái SLIDING_TILE (Bổ đề 4); 12 ca kiểm thử save (mục 7.5) |

---

# PHỤ LỤC C — BA QUY TẮC NHẤT QUÁN KHÔNG ĐƯỢC VI PHẠM

Khi viết thêm bất kỳ nội dung nào cho Chapter 1:

| # | Quy tắc | Vì sao |
|---|---|---|
| **1** | **Không con số nào mâu thuẫn niên biểu ở mục 2.3.8.** Mọi năm, mọi tuổi, mọi can chi phải tra lại bảng đó | Toàn bộ cú twist đứng trên phép tính "1969 + 7 = 1976". Sai một con số là hỏng cả chương |
| **2** | **Không nhân vật nào biết nhiều hơn phần của mình.** Bà nội **không biết** bà Tơ đã gửi giấy báo tang. Ông từ (mất 1989) **không biết gì sau 1989**. Bà Tơ **không biết** nội dung nhật ký | Mỗi tài liệu trong game là một **góc nhìn cục bộ**. Người chơi ghép chúng lại; nhân vật thì không |
| **3** | **Bà Cô KHÔNG BAO GIỜ NÓI.** Bà Cô chỉ hiện qua **nước, mõ, hương và hình nhân**. Trong toàn Chapter 1, **không có một câu thoại nào thuộc về Bà Cô**. Câu thoại có lời duy nhất của chương là của **một người sống** | Đây là mũi dao của chủ đề: **hủ tục là do người sống bịa ra.** Cho Bà Cô nói một câu là phá hỏng toàn bộ luận điểm |

Và một quy tắc thứ tư cho khâu kinh dị:

> **4. Không bao giờ giải thích ma bằng lời.** Mọi thông tin siêu nhiên trong Chapter 1 đến từ **tài liệu do người sống viết**: văn khấn, gia phả, nhật ký, sổ chợ, sổ ghi tên, bảy điều cấm kỵ, chữ khắc thành giếng. Không có narrator, không có tiếng vọng giải thích, không có ghi chú của "một thế lực".

---

*Hết `docs/01_KICH_BAN_CHAPTER_01.md` — Linh An Thôn, Chương 1.*
*Nguồn sự thật: **SPINE**. Không một `area_id`, `item_id`, `puzzle_id` hay `scare_id` nào bị thay đổi hay phát sinh thêm.*
