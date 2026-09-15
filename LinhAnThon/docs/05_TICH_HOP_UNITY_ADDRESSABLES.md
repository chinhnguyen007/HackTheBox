# LINH AN THÔN — CHƯƠNG 1
## TÍCH HỢP UNITY ADDRESSABLES — NGÂN SÁCH APK, ĐÓNG GÓI, PHÂN PHỐI NỘI DUNG

| Trường | Giá trị |
|---|---|
| Dự án | **Linh An Thôn — Chapter 1** |
| Tài liệu | `docs/05_TICH_HOP_UNITY_ADDRESSABLES.md` — bản chốt cho tổ engine và tổ vận hành |
| Nền tảng | Android (AAB, minSdk 24) · iOS (minimum iOS 13) |
| Ràng buộc cứng | **Play Console download size ≤ 30 MB** (mục tiêu thiết kế 27 MB — xem §1.1 và §1.3, trần này **không đạt được** nếu giữ nguyên bộ SDK) · toàn bộ asset nội dung tải qua Addressables remote bundle |
| Độ phân giải thiết kế | 1920 × 1080, gốc (0,0) góc trên-trái |
| Tài liệu liên quan | `03_DATA_SPEC.md` (hợp đồng dữ liệu) · `04_LIVEOPS_MONETIZATION.md` (remote config, sự kiện mùa) |
| Ngôn ngữ | Tài liệu: tiếng Việt có dấu. Mọi tên nhóm / nhãn / khoá: snake_case không dấu |
| Ngày cập nhật | 2026-09-15 |

> **Một câu tóm tắt toàn bộ tài liệu:** APK chỉ chứa *động cơ và cái vỏ*; mọi thứ người chơi nhìn thấy và nghe thấy đều nằm trên CDN, tải theo từng khu vực, và thay được mà không cần đụng tới cửa hàng ứng dụng.

---

# 0. BỐN NGUYÊN TẮC NỀN

| # | Nguyên tắc | Hệ quả kỹ thuật kiểm được |
|---|---|---|
| **A1** | **APK chỉ chứa thứ cần để hiện màn hình tải.** | Nhóm Addressables `local_boot` giới hạn cứng **4 MB** (8 tiếng UI ADPCM 0,08 MB là ngoại lệ duy nhất). Mọi lớp nền, mọi cú doạ — **kể cả biến thể an toàn `_soft` / `_static`** — và mọi âm thanh còn lại đều `remote`. |
| **A2** | **Không nội dung nào bắt người chơi chờ thứ họ chưa cần.** | Tải theo **từng khu vực**. Vào `area_san_gach` chỉ tải bundle của sân gạch (**5,07 MB**, §1.6.5), không tải cả chương (**47,6 MB**). |
| **A3** | **Mạng hỏng không bao giờ được chặn người chơi.** | Mọi đường tải đều có đường lui. Giao diện sự kiện hỏng → nền gốc. Ambience hỏng → im lặng, chơi tiếp. Bundle khu vực hỏng → thử lại + màn hình giải thích, **không** màn hình chết. |
| **A4** | **Sửa nội dung không được đụng tới bản build.** | Dữ liệu (`data/**`) và asset đi cùng một catalog có phiên bản. Đẩy catalog mới là xong — không qua duyệt store. |

---

# 1. NGÂN SÁCH KÍCH THƯỚC APK ENGINE

## 1.1. Cột "Ngân sách" đo đại lượng nào

Trước khi đọc bất kỳ con số nào ở §1.2, phải thống nhất đơn vị — ba đại lượng dưới đây khác nhau tới vài chục phần trăm và lẫn lộn chúng là cách nhanh nhất để tự lừa mình:

| Đại lượng | Nghĩa | Dùng ở đâu trong tài liệu này |
|---|---|---|
| **Play Console download size** | Số byte máy người chơi thực sự kéo về từ Play khi bấm "Cài đặt". Là **AAB đã tách theo ABI + mật độ + ngôn ngữ**, đã nén. Đây là con số hiện trên trang cửa hàng. | **Toàn bộ §1.2, §1.3.** Trần cứng **30 MB** áp vào đúng đại lượng này |
| Play Console install size | Kích thước sau giải nén trên đĩa. Thường gấp **1,3 – 1,8 lần** download size | Không dùng để cưỡng chế. Chỉ theo dõi để đừng vượt chỗ trống máy 16 GB |
| Universal APK / `.aab` thô | File dựng ra từ CI, chứa **mọi** ABI và mọi mật độ | **Không bao giờ** dùng làm số ngân sách. CI phải đo bằng `bundletool get-size total --dimensions=ABI,SCREEN_DENSITY,LANGUAGE` |

> **Quy ước đơn vị toàn tài liệu:** `1 MB = 1 MiB = 1 048 576 byte`, trừ nơi ghi rõ khác. Mọi phép tính ở §1.6 đều viết ra công thức để người khác kiểm lại được.

**Cách CI đo (bắt buộc, không đoán):**

```bash
bundletool build-apks --bundle=app.aab --output=app.apks --mode=default
bundletool get-size total --apks=app.apks --dimensions=ABI,SCREEN_DENSITY,LANGUAGE
# lấy dòng ABI=arm64-v8a, LANGUAGE=vi  -> đó là con số so với trần 30 MB
```

## 1.2. Bảng ngân sách APK engine — dải đo thật, không phải số mong muốn

Bản dựng tham chiếu: **Release, ARM64, IL2CPP, Managed Stripping `High`, Strip Engine Code bật, phát hành qua AAB.** Cột "Dải thực tế" là khoảng mà một dự án Unity 2D có **Addressables + TextMeshPro + Firebase (Analytics + Remote Config) + Unity IAP + SDK quảng cáo thưởng** thường rơi vào; cột "Kế hoạch" là điểm chốt để CI so sánh.

| # | Thành phần | Chi tiết | Dải thực tế | **Kế hoạch** | Ai chịu trách nhiệm |
|---|---|---|---|---|---|
| 1 | `libunity.so` (arm64-v8a) | Nhân engine đã gỡ module (Physics, Terrain, VR/XR, Video, Cloth, Vehicles, Particle) | 9,0 – 13,0 | **11,0** | Engine |
| 2 | `libil2cpp.so` (arm64-v8a) | Mã managed đã dịch sang C++. Kích thước tỉ lệ **thuận với lượng mã managed**, kể cả mã của SDK | 8,0 – 14,0 | **10,0** | Engine |
| 3 | `global-metadata.dat` | Siêu dữ liệu IL2CPP: tên kiểu, chuỗi, bảng phương thức | 3,0 – 6,0 | **4,0** | Engine |
| 4 | `classes.dex` | **Mã Java/Kotlin**: AndroidX core + appcompat, Play Billing, Play Core / Asset Delivery, Firebase Analytics + Remote Config, SDK quảng cáo | 2,0 – 3,5 | **2,5** | Engine + Vận hành |
| 5 | `.so` native của SDK | Phần native của SDK quảng cáo và Firebase (arm64) | 1,2 – 2,2 | **1,6** | Vận hành |
| 6 | `unity default resources` + shader | Shader 2D đã lọc variant + tài nguyên mặc định + shader TextMeshPro | 1,2 – 1,8 | **1,5** | Engine |
| 7 | Font tiếng Việt đã subset | Serif có dấu đầy đủ + chữ số, bỏ CJK, đóng gói SDF cho TMP | 1,0 – 1,4 | **1,2** | Đồ hoạ |
| 8 | Chuỗi localization `vi-VN` | Toàn bộ `txt_*` của Chương 1 | 0,2 – 0,4 | **0,3** | Tường thuật |
| 9 | Nhóm Addressables `local_boot` | Logo, màn hình tải, atlas UI tối thiểu, catalog gốc, 8 tiếng UI ADPCM | ≤ 4,0 | **4,0** | Đồ hoạ + Engine |
| 10 | `res/`, `AndroidManifest`, icon adaptive | Vỏ ứng dụng | 0,5 – 0,9 | **0,7** | Engine |
| 11 | **Dự phòng** | Đệm cho SDK tự cập nhật, cho lần đo đầu lệch khỏi kế hoạch | — | **1,5** | — |
| | **TỔNG — Kịch bản A (giữ nguyên bộ SDK)** | | **30,1 – 47,2** | **38,3** | |

**Đối chiếu với trần 30 MB, nói thẳng:**

- Kế hoạch **38,3 MB** ⇒ **vượt trần 8,3 MB**.
- Ngay cả khi **mọi dòng đều rơi vào cận dưới** của dải và **dự phòng bằng 0**, tổng vẫn vượt:

  | Dòng | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | **Tổng** |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|
  | Cận dưới | 9,0 | 8,0 | 3,0 | 2,0 | 1,2 | 1,2 | 1,0 | 0,2 | 4,0 | 0,5 | 0 | **30,1** |

  `9,0+8,0+3,0+2,0+1,2+1,2+1,0+0,2+4,0+0,5+0 = 30,1 MB` ⇒ **vẫn vượt trần 0,1 MB**, ở một kịch bản may mắn đến mức không nên lên kế hoạch dựa vào nó.
- Kết luận: **với bộ SDK hiện tại, trần 30 MB là KHÔNG ĐẠT ĐƯỢC.** Không có cách xếp lại bảng nào cứu được điều đó. Phải bỏ bớt thứ gì đó — §1.3 liệt kê đúng những thứ đó và cái giá của từng thứ.

`[[ Con số cũ của tài liệu này — libil2cpp 2,5 MB và global-metadata 1,8 MB — là số của một dự án Unity RỖNG (một scene trống, không SDK). Chúng không sai về mặt vật lý; chúng chỉ không mô tả dự án này. Một dự án có Addressables + TMP + Firebase + IAP + SDK ads có khối lượng mã managed lớn hơn nhiều lần, và cả libil2cpp lẫn metadata đều tỉ lệ thuận với khối lượng đó. ]]`

## 1.3. Ba kịch bản — trần 30 MB đạt được với điều kiện nào

| Kịch bản | Bỏ gì / làm gì | Phép trừ | **Download size** | Đạt trần 30? |
|---|---|---|---|---|
| **A** | Giữ nguyên bộ SDK ở §1.2 | — | **38,3 MB** | **KHÔNG** — thiếu 8,3 MB |
| **B** | A **trừ** SDK quảng cáo thưởng, **trừ** Firebase (viết Remote Config tự quản: một endpoint JSON + ETag), **trừ** TextMeshPro (dùng UI Text + font subset), **trừ** Newtonsoft.Json (dùng `JsonUtility` + bộ đọc tay), IL2CPP Code Generation = **"Faster (smaller) builds"** | `38,3 − 1,5 (dex) − 1,4 (.so SDK) − 1,8 (libil2cpp) − 0,6 (metadata) − 0,6 (local_boot bỏ asset TMP) − 0,2 (shader TMP)` = `38,3 − 6,1` | **32,2 MB** | **KHÔNG** — thiếu 2,2 MB |
| **C** | B **cộng** chuyển `local_boot` (3,4) và font (1,2) sang **Play Asset Delivery kiểu `fast-follow`** | `32,2 − 3,4 − 1,2` | **27,6 MB** | **CÓ** — dưới trần 2,4 MB |

**Mục tiêu thiết kế đặt ở 27,0 MB, không phải 30,0 MB.** Lý do: trần 30 là chỗ CI **chặn**; 28 là chỗ CI **cảnh báo**; một bảng ngân sách cộng đúng bằng trần là một bảng không có đệm, và lần cập nhật SDK đầu tiên sẽ phá nó. Kịch bản C cho **27,6 MB**, tức **vượt mục tiêu 0,6 MB** nhưng vẫn còn dòng dự phòng 1,5 MB nguyên vẹn bên trong. Chốt lại sau lần đo thật đầu tiên bằng **Build Report Inspector**; nếu `libil2cpp.so` và `global-metadata.dat` rơi vào nửa dưới của dải (8,0 – 8,5 và 3,0 – 3,4) thì C về đúng 27,0.

**Điều kiện và cái giá của từng đòn bẩy trong B và C — phải có người ký, không phải quyết định kỹ thuật thuần tuý:**

| Đòn bẩy | Tiết kiệm | Ai phải đồng ý | Cái giá thật |
|---|---|---|---|
| Bỏ SDK quảng cáo thưởng | ~2,0 (dex + `.so`) + ~0,6 (libil2cpp/metadata) | **Vận hành** | `04_LIVEOPS_MONETIZATION.md` đang có `ad_placements` và khoá `ads_reward_hints`. Bỏ SDK ⇒ đường gợi ý miễn phí **chỉ còn đường chờ theo thời gian** (`unlock_free_after_sec`, trần 300 s). Nguyên tắc N1 "luôn có đường miễn phí" vẫn giữ được, nhưng mất một nguồn gem. **Đây là xung đột liên tài liệu, phải giải ở `docs/04`, không giải ở đây.** |
| Bỏ Firebase, tự viết Remote Config | ~0,9 (dex) + ~0,6 (libil2cpp/metadata) | Engine + Vận hành | Mất Analytics dựng sẵn ⇒ phải tự làm đường ống telemetry ở §7.4. Mất A/B testing dựng sẵn ⇒ `ab_tests` phải tự phân nhóm theo hash device id. **Không** mất khả năng quay lui: `addressables_catalog_url` chỉ là một chuỗi trong một file JSON trên CDN với `max-age=60` |
| Bỏ TextMeshPro | ~0,6 (asset + shader) | Đồ hoạ | Mất SDF scaling và outline. Với game 1 độ phân giải thiết kế cố định 1920×1080 và font tiếng Việt subset, UI Text + atlas bitmap là đủ |
| IL2CPP "Faster (smaller) builds" | 0,8 – 2,0 | Engine | Mã chạy chậm hơn ~5–10% ở phần logic managed. Game này không có vòng lặp nặng — nó vẽ 4 lớp và chờ người chơi chạm |
| `local_boot` + font sang PAD `fast-follow` | 4,6 | Engine | **Android-only.** iOS phải dùng On-Demand Resources hoặc chấp nhận tổng lớn hơn. Tải về ngay sau khi cài, nên lần mở app đầu tiên **có thể** chưa có font ⇒ bắt buộc có một font dự phòng ≤ 120 KB trong base module và một màn hình chờ chịu được trạng thái đó |
| Bỏ Newtonsoft.Json | 0,3 – 0,6 | Engine | Phải viết bộ đọc `data/**` bằng tay. Hợp đồng dữ liệu ở `03_DATA_SPEC.md` đủ chặt để làm việc đó an toàn |
| Bỏ Addressables, dùng `UnityWebRequest` + `AssetBundle` thô | 0,5 – 0,8 | — | **BÁC BỎ.** Nó xoá sạch §2, §4, §5, §6 của chính tài liệu này. Cái giá không đáng 0,8 MB |

## 1.4. Vì sao dòng `local_boot` vẫn là dòng nguy hiểm nhất

Các dòng còn lại gần như cố định — chúng là chi phí của engine và SDK, và §1.3 đã kê hết cách giảm. Dòng **`local_boot` 4 MB** là dòng duy nhất tổ nội dung chạm vào được, nên cũng là dòng duy nhất phình ra theo từng pull request. Chỉ năm thứ được phép nằm trong đó:

| Được phép | Không được phép |
|---|---|
| Logo studio + logo game (một atlas 1024×1024, ASTC 6×6) | Bất kỳ lớp nền `bg_*_l[0-3]_*` nào |
| Khung màn hình tải + hoạt ảnh chờ (sprite sheet ≤ 512×512) | Bất kỳ sheet `anim_*` cú doạ nào, kể cả `_soft` / `_static` |
| Font Việt đã subset (hoặc font dự phòng ≤ 120 KB nếu dùng PAD) | Bất kỳ `amb_*` hay `mus_*` nào |
| Atlas UI tối thiểu: nút, khung thoại, con trỏ, khung túi đồ | Icon vật phẩm (`icon_item_*` — nằm ở remote, xem §3.1 và §1.6.5) |
| 8 tiếng UI ngắn ADPCM (`ui_tap_hotspot`, `ui_mo_hanh_trang`, …) — tổng **0,08 MB**, xem §1.6.6 | Mọi `sfx_scare_*` |

`[[ Cám dỗ thường gặp: "nhét tạm icon túi đồ vào local cho nhanh". Mười vật phẩm gói trong một atlas 1024x1024 ASTC 6x6 = 0,45 MB — nghe thì nhỏ, nhưng nó phá nguyên tắc A4: sửa một icon là phải qua duyệt store. ]]`

## 1.5. Cấu hình build để đạt ngân sách

| Thiết lập | Giá trị | Tiết kiệm ước tính |
|---|---|---|
| Scripting Backend | **IL2CPP** | — (bắt buộc cho ARM64) |
| Target Architectures | **ARM64 duy nhất**, phát hành qua **AAB** | **0 MB — xem cảnh báo bên dưới** |
| Managed Stripping Level | **High** | 1,5 – 2,5 MB |
| IL2CPP Code Generation | **Faster (smaller) builds** | 0,8 – 2,0 MB |
| C++ Compiler Configuration | **Master** | 0,5 – 1 MB |
| Strip Engine Code | **Bật** | 2 – 4 MB |
| Module đã gỡ | Physics, Physics2D (chỉ dùng raycast UI), Terrain, VR/XR, Video, Cloth, Vehicles, Particle System *(nếu hiệu ứng khói dùng shader — xem nhát cắt **C1** ở §1.6.3, nó biến điều kiện này thành bắt buộc)* | 3 – 5 MB |
| Splash Screen | **Tắt** (yêu cầu bản quyền Plus/Pro) | 0,3 MB |
| Shader variant stripping | Chỉ giữ 2D Sprite-Lit/Unlit, bỏ Fog/Instancing/Lightmap variant | 1 – 2 MB |

> **CẢNH BÁO — "ARM64 duy nhất tiết kiệm ~8 MB" là SAI khi nói về download size.** AAB **đã** tách theo ABI: một máy ARM64 tải về gói ARM64, một máy ARMv7 tải về gói ARMv7. Thêm ARMv7 vào bản dựng làm **`.aab` trên CI** to thêm ~8 MB nhưng **không làm download size của máy ARM64 to thêm một byte nào**. Vì vậy:
>
> - Con số ngân sách ở §1.2 **không đổi** dù có hay không có ARMv7.
> - Bỏ ARMv7 **không** phải là một đòn bẩy ngân sách. Nó là một **quyết định cắt thị trường**: mọi lập luận khác trong tài liệu này (3G chậm, RAM 2 GB, `minSdk 24`) đều lấy máy yếu Việt Nam làm chuẩn, mà máy yếu nhất trong nhóm đó thường chính là máy ARMv7.
> - **Phải đo trước khi chốt:** lấy tỉ lệ thiết bị ARMv7 trong tệp người dùng mục tiêu từ Play Console → *Statistics* → *Device catalog*, lọc theo Việt Nam và `minSdk 24`. Nếu tỉ lệ ấy đáng kể thì bật lại ARMv7 — chi phí là dung lượng CI và thời gian build, **không** phải ngân sách người chơi.
> - `link.xml` giữ lại các kiểu bị strip nhầm khi dùng reflection (Addressables hay bị strip mất provider). Đo bằng **Build Report Inspector**, không đoán.


## 1.6. Ngân sách phía remote — dựng từ manifest asset thật

Mục này **không** tính vào 30 MB của §1.2. Nó được dựng lại từ đầu bằng cách **đếm từng file** trong `02_PROMPT_DO_HOA.md` §6.1 – §6.4 rồi áp công thức nén của §3, chứ không đặt một con số tổng rồi chia ngược.

### 1.6.1. Công thức — mọi ô trong bảng đều tính lại được

ASTC nén theo **khối cố định 128 bit (16 byte) cho mỗi khối pixel**, nên kích thước một texture **không** phụ thuộc vào nội dung:

```
byte = ceil(W / b) * ceil(H / b) * 16          (b = cạnh khối: 6 hoặc 8)
bpp  = 128 / (b * b)
```

| Định dạng | Khối | bpp | Kiểm nhanh trên 1920×1080 |
|---|---|---|---|
| **ASTC 6×6** | 6 × 6 px = 36 px / 16 byte | `128 / 36 = ` **3,5556** *(tài liệu đồ hoạ ghi tròn 3,56)* | `ceil(1920/6)=320` × `ceil(1080/6)=180` × 16 = **921 600 B = 0,8789 MB** |
| **ASTC 8×8** | 8 × 8 px = 64 px / 16 byte | `128 / 64 = ` **2,00** | `240 × 135 × 16 = 518 400 B = 0,4944 MB` |

Ba quy ước nữa, dùng nhất quán trong mọi bảng dưới đây:

1. **Mipmap tắt** cho mọi asset 2D orthographic ⇒ không cộng thêm 33%.
2. **Hệ số LZMA trên payload ASTC = 0,92.** Dữ liệu ASTC đã là dữ liệu entropy cao; LZMA chỉ ăn được phần header bundle, bảng sprite, metadata và chuỗi văn bản. Lấy **8%** làm số kế hoạch. *(Số cũ "LZMA nhỏ hơn LZ4 15–25%" so sánh hai bộ nén với nhau, không phải so với dữ liệu thô — nó không phải hệ số để nhân vào đây.)* **Bắt buộc đo lại** bằng `bundletool`/Addressables Analyze sau bundle đầu tiên và cập nhật hệ số này.
3. **Âm thanh đã nén (Vorbis, ADPCM) không nén thêm được.** Hệ số LZMA cho phần âm thanh = **1,00**.

### 1.6.2. Manifest gốc — chi phí nếu dựng đúng như `02_PROMPT_DO_HOA.md` hôm nay

| Nhóm | Asset | Độ phân giải | Số biến thể | Định dạng | bpp | MB/file | **Tổng MB** |
|---|---|---|---|---|---|---|---|
| Nền | `bg_*_l0_back / _l1_mid / _l2_fore / _l3_fx` + `_lit` A4 + quầng đèn A5 | 1920 × 1080 | 22 | ASTC 6×6 | 3,556 | 0,8789 | **19,336** |
| Zoom | `zoom_*_plate` (6) + `B5_lit` | 1920 × 1080 | 7 | ASTC 6×6 | 3,556 | 0,8789 | **6,152** |
| Zoom | `zoom_*_parts` (6) + `B6_parts_khoet` | 2048 × 2048 | 7 | ASTC 6×6 | 3,556 | 1,7847 | **12,493** |
| Cú doạ | 8 sheet gốc + 8 `_soft` + 8 `_static` | 2048 × 2048 | 24 | ASTC 8×8 | 2,000 | 1,0000 | **24,000** |
| Nhân vật | C8, C11 + hàng đuốc, C12 | 768 × 1365 / 1024 × 768 | 4 | ASTC 6×6 | 3,556 | 0,44 / 0,33 | **1,670** |
| Icon | `icon_item_*` × 10, một atlas | 1024 × 1024 | 1 | ASTC 6×6 | 3,556 | 0,4462 | **0,446** |
| | **Tổng byte GPU** | | **65 file** | | | | **64,097** |
| | **Sau LZMA ×0,92** | | | | | | **58,97** |
| | **Cộng âm thanh** (`04_horror.md` §3.10) | | | | | | **+18,80** |
| | **TỔNG NỘI DUNG REMOTE — chưa cắt** | | | | | | **77,77** |

**Ba con số cũ đều sai, và sai theo hướng có thể giải thích được:**

| Con số cũ | Ở đâu | Thực tế | Vì sao lệch |
|---|---|---|---|
| "Tổng nội dung Chương 1 ~24,5 MB" | §1.4 bản cũ | **77,77 MB** chưa cắt | Là một con số bìa, không dựng từ manifest |
| "~20,3 MB sau nén" cho đồ hoạ | `02_PROMPT_DO_HOA.md` §6.4 | **58,97 MB** | Bảng tự khai, không áp công thức bpp cho từng file. Sai nhiều nhất ở dòng sprite doạ: 24 sheet 2048² ASTC 8×8 là **24,0 MB**, không phải 3,6 MB |
| "Tổng remote Chương 1 ≈ 39 MB" | `02_PROMPT_DO_HOA.md` §6.4, ghi chú cuối | **77,77 MB** chưa cắt | Là `20,3 + 18,8` — cộng một con số tự khai với một con số của tổ khác, không ai tính lại vế đầu |
| "Một nền = 0,88 MB" | §3.1 bản cũ | **0,8789 MB cho MỘT LỚP**; một **bộ nền** là **4 lớp** ⇒ **3,516 MB/khu vực** | Bỏ sót ràng buộc 4 lớp parallax bắt buộc của `02` §2.2 |

### 1.6.3. Ba trần phải thoả — và các nhát cắt để thoả chúng

Trần **không** được bịa. Cả ba đều suy ra từ số liệu mạng mà chính tài liệu này đã nêu: **3G Việt Nam kéo 3,5 MB trong 6–10 giây ⇒ thông lượng 0,35 – 0,58 MB/s, trung vị 0,45 MB/s.**

| Trần | Giá trị | Cách tính |
|---|---|---|
| **T1 — lần chờ đầu tiên** | **≤ 8,5 MB** | Ngưỡng bỏ cuộc ở màn hình tải đầu tiên lấy **25 giây**. `25 s × 0,35 MB/s (cận dưới 3G) = 8,75 MB` ⇒ làm tròn xuống **8,5** |
| **T2 — một bundle khu vực** | **≤ 8,0 MB** | Tải trước ngầm phải xong trong thời gian người chơi ở lại khu vực trước đó (tối thiểu **90 s**, theo `target_solve_sec`), dùng **30%** băng thông để không tranh với nội dung đang chơi: `90 s × 0,35 MB/s × 0,30 = 9,45 MB` ⇒ chốt **8,0** cho có biên |
| **T3 — tổng cache nội dung** | **≤ 52 MB** | Máy phổ thông 32 GB. `APK 27,6 (§1.3 kịch bản C) + cache 52 = 79,6 MB` tổng chiếm chỗ — dưới mốc 100 MB, nơi người dùng bắt đầu rà soát và gỡ app |

Manifest gốc là **77,77 MB**, vượt T3 **25,77 MB**. Phải **cắt nội dung**, không được sửa con số trong bảng. Sáu nhát cắt dưới đây, theo thứ tự "tiết kiệm nhiều nhất trên mỗi đơn vị chất lượng mất đi":

| # | Nhát cắt | Trước | Sau | Tiết kiệm | Đánh đổi thật |
|---|---|---|---|---|---|
| **C1** | **Bỏ 5 lớp `_l3_fx` full-frame.** Khói / bụi / vignette dựng bằng shader; nguồn ảnh còn lại là **1 texture nhiễu tile 512×512** + **1 quầng đèn radial alpha 512×512**, dùng chung cả chương, nằm trong `remote_shared_ui` | 5 × 0,8789 = **4,395** | 2 × 0,1129 = **0,226** | **4,17** | Lớp FX không còn vẽ tay riêng cho từng khu vực; mỗi khu vực chỉ còn tham số (màu, mật độ, tốc độ trôi). **Hệ quả build:** module Particle System **không được gỡ** nữa, hoặc FX phải làm hoàn toàn bằng shader — chốt ở §1.5 |
| **C2** | **`_l2_fore` alpha-trim, trần khung 1920 × 600** thay vì full-frame. Tiền cảnh parallax 0,03–0,06 chỉ chiếm dải dưới và hai mép | 5 × 0,8789 = **4,395** | 5 × 0,4883 = **2,441** | **1,95** | Tổ đồ hoạ phải giữ toàn bộ tiền cảnh trong một dải cao ≤ 600 px. Thêm một mục checklist QA |
| **C3** | **Bỏ bản `_lit` của A4 và lớp quầng đèn rời của A5.** Khoảnh khắc "đã thắp đèn" = quầng đèn dùng chung ở C1 + đổi tham số tint trên `_l1_mid` | 2 × 0,8789 = **1,758** | **0** | **1,76** | Ánh sáng thắp đèn không còn được vẽ tay theo từng vật thể trong cảnh |
| **C4** | **Hạ atlas `_parts` câu đố theo nội dung thật**, thay vì 2048² đồng loạt: B1 **1536×1024** (3 vành đồng tâm 800/600/400), B2 **512²** (8 nét ≥ 44 px), B3 **512²** (6 icon 150×150), B4 **1024²** (mõ 520×420 + chuông 260×260), B5 **1024²** (đèn 400×520 + 5 phần tử ≥160²), B6 **1024²** (9 ô 280×280 = 840×840) | 6 × 1,7847 = **10,708** | **2,232** | **8,48** | Không mất phần tử nào. 2048² vốn là con số mặc định, không phải con số đo |
| **C5** | **Chốt luật đóng sheet cú doạ:** khung dài nhất **768 px**, **tối đa 6 khung** cho sheet gốc (0,3–0,8 s ở 8–12 fps ⇒ 3–10 khung), **3 khung** cho `_soft` (tốc độ 60%, biên độ ≤ 1,04 ⇒ chỉ cần đầu–giữa–cuối), **1 khung** cho `_static` (`02` §2.2 đã định nghĩa đúng như vậy) | 24 × 1,0 = **24,000** | **10,136** | **13,86** | Sprite doạ phóng lên màn 1080 px với hệ số 1,1 – 1,4×. Chính §3.1 đã lập luận: cú doạ chạy 0,3–0,8 giây, mắt không kịp bắt lỗi nén — lập luận đó áp được cho cả độ phân giải |
| **C6** | **Hoãn biến thể `_lo` 1280×720 và biến thể ETC2**, cùng lý do với §3.1: chỉ dựng khi telemetry chứng minh có người dùng thật cần. Cả hai đều chọn bằng **nhãn**, nên chúng **không bao giờ** cộng vào lượt tải của một máy — chúng chỉ cộng vào dung lượng lưu trên CDN | +8,62 lưu trữ CDN | **0** | **0 (tải) / 8,62 (CDN)** | Máy rất yếu chưa có đường lui hạ độ phân giải. Phải theo dõi `bundle_download_fail` và thời gian tải theo phân vị |

> **Nhát cắt KHÔNG được phép:** bỏ, gộp, hoặc đẩy ra sau cổng bất kỳ biến thể `_soft` / `_static` nào. Chúng gắn với tuỳ chọn trợ năng (`gentle_mode`, `reduce_motion`, `scare_intensity = 0`) và `02` §6.5 cùng `04_horror.md` §4.7.5 ghi rõ: **không tài sản an toàn nào được đặt sau tường trả phí** — mà một bundle tải riêng, tải sau, hoặc tải theo điều kiện *chính là* một cổng. Vì vậy `_soft` và `_static` nằm **cùng bundle với khu vực**, tải cùng lúc, cộng thẳng vào ngân sách khu vực. Giá của nguyên tắc ấy là **5,43 MB / 10,14 MB = 54%** ngân sách sprite doạ, và nó được trả đầy đủ trong bảng §1.6.4.

### 1.6.4. Bảng tính sau cắt — kiểm lại được từng dòng

**Nền (mỗi khu vực — một BỘ NỀN, không phải một ảnh):**

| Lớp | Độ phân giải | Định dạng | bpp | Phép tính | MB |
|---|---|---|---|---|---|
| `_l0_back` | 1920 × 1080 | ASTC 6×6 | 3,556 | `320 × 180 × 16` | **0,8789** |
| `_l1_mid` (chứa phần lớn hotspot) | 1920 × 1080 | ASTC 6×6 | 3,556 | `320 × 180 × 16` | **0,8789** |
| `_l2_fore` (trần sau cắt **C2**) | 1920 × 600 | ASTC 6×6 | 3,556 | `320 × 100 × 16` | **0,4883** |
| `_l3_fx` | — | shader + texture dùng chung | — | cắt **C1** | **0** |
| | | | | **BỘ NỀN / khu vực** | **2,2461** |
| | | | | **× 5 khu vực** | **11,231** |

**Zoom câu đố:**

| Asset | Độ phân giải | Số | Định dạng | bpp | MB/file | Tổng MB |
|---|---|---|---|---|---|---|
| `zoom_*_plate` | 1920 × 1080 | 6 | ASTC 6×6 | 3,556 | 0,8789 | **5,273** |
| `zoom_puz_khoa_bat_quai_parts` | 1536 × 1024 | 1 | ASTC 6×6 | 3,556 | 0,6680 | **0,668** |
| `zoom_puz_rap_chu_the_menh_parts` | 512 × 512 | 1 | ASTC 6×6 | 3,556 | 0,1129 | **0,113** |
| `zoom_puz_tuan_tu_le_cung_parts` | 512 × 512 | 1 | ASTC 6×6 | 3,556 | 0,1129 | **0,113** |
| `zoom_puz_ba_hoi_chin_tieng_parts` | 1024 × 1024 | 1 | ASTC 6×6 | 3,556 | 0,4462 | **0,446** |
| `zoom_puz_thap_lai_den_dau_parts` | 1024 × 1024 | 1 | ASTC 6×6 | 3,556 | 0,4462 | **0,446** |
| `zoom_puz_thap_lai_den_dau_lit` | 512 × 512 | 1 | ASTC 6×6 | 3,556 | 0,1129 | **0,113** |
| `zoom_puz_xep_anh_gia_pha_parts` | 1024 × 1024 | 1 | ASTC 6×6 | 3,556 | 0,4462 | **0,446** |
| `zoom_puz_xep_anh_gia_pha_parts_khoet` | 1024 × 1024 | 1 | ASTC 6×6 | 3,556 | 0,4462 | **0,446** |
| | | **14** | | | | **8,065** |

**Cú doạ — mỗi cú doạ là BA file, không phải một:**

| Tỉ lệ khung | Sheet gốc (6 khung) | `_soft` (3 khung) | `_static` (1 khung) | **Bộ / cú doạ** |
|---|---|---|---|---|
| **1 : 1** — khung 768×768 | `2304 × 1536` ASTC 8×8 = `288×192×16` = **0,8438** | `2304 × 768` = `288×96×16` = **0,4219** | `768 × 768` ASTC 6×6 = `128×128×16` = **0,2500** | **1,5156** |
| **16 : 9** — khung 768×432 | `2304 × 864` = `288×108×16` = **0,4746** | `2304 × 432` = **0,2373** | `768 × 432` ASTC 6×6 = **0,1406** | **0,8525** |
| **9 : 16** — khung 432×768 | `1296 × 1536` = `162×192×16` = **0,4746** | `1296 × 768` = **0,2373** | `432 × 768` ASTC 6×6 = **0,1406** | **0,8525** |

*`_static` dùng ASTC 6×6 chứ không phải 8×8: nó là một khung **đứng yên trên màn hình**, mắt có thời gian soi — đúng trường hợp mà §3.1 nói 8×8 sẽ lộ khối ở vùng chuyển sắc tối.*

| Cú doạ | Sprite | Tỉ lệ | Khu vực | MB |
|---|---|---|---|---|
| `scare_bong_trong_chum` | C1 `spr_bong_khan_xo` | 1:1 | `area_san_gach` | 1,5156 |
| `scare_ban_tay_giay_sau_manh` | C2 `spr_ban_tay_vang_ma` | 16:9 | `area_hien_nha` | 0,8525 |
| `scare_di_anh_quay_mat` | C3 + C4 (hai lớp, nung vào **một** sheet) | 1:1 | `area_gian_tho` | 1,5156 |
| `scare_khoi_tu_hinh_nguoi` | C5 `spr_khoi_tu` | 9:16 | `area_gian_tho` | 0,8525 |
| `scare_mat_duoi_day_gieng` | C6 `spr_mat_trang_ngoai_cua` | 1:1 | `area_bep_gieng` | 1,5156 |
| `scare_hinh_nhan_chan_loi` | C7 `spr_hinh_nhan_the_mang` | 9:16 | `area_gac_xep` | 0,8525 |
| `scare_anh_tho_thieu_mat` | C9 `spr_van_khoet_mat` | 1:1 | `area_gac_xep` | 1,5156 |
| `scare_ao_cuoi_quay_dau` | C10 `spr_dau_nan_tre_quay` | 1:1 | `area_gac_xep` | 1,5156 |
| | | | **Tổng 24 file** | **10,136** |

**Còn lại:**

| Asset | Độ phân giải | Số | Định dạng | MB |
|---|---|---|---|---|
| C8 `spr_ao_cuoi_giay` (cutscene) | 576 × 1024 | 1 | ASTC 6×6 | 0,2505 |
| C11 `spr_ba_dong_to` | 576 × 1024 | 1 | ASTC 6×6 | 0,2505 |
| C11 `spr_hang_duoc_duoi_san` | 1024 × 384 | 1 | ASTC 6×6 | 0,1670 |
| C12 `spr_ban_tay_nguoi_choi` (con trỏ, 4 khung 256×192) | 512 × 384 | 1 | ASTC 6×6 | 0,0840 |
| C13 atlas `icon_item_*` × 10 | 1024 × 1024 | 1 | ASTC 6×6 | 0,4462 |
| Atlas UI remote (khung phóng to câu đố, khung túi đồ) | 1024 × 1024 | 1 | ASTC 6×6 | 0,4462 |
| Texture FX dùng chung (nhiễu tile + quầng đèn radial) — cắt **C1** | 512 × 512 | 2 | ASTC 6×6 | 0,2257 |

**Tổng:**

| Dòng | Phép tính | MB |
|---|---|---|
| Nền 5 khu vực | `2,2461 × 5` | 11,231 |
| Zoom câu đố | §1.6.4 bảng zoom | 8,065 |
| Cú doạ (gốc + `_soft` + `_static`) | §1.6.4 bảng cú doạ | 10,136 |
| Nhân vật, con trỏ, icon, UI, FX | `0,2505+0,2505+0,1670+0,0840+0,4462+0,4462+0,2257` | 1,870 |
| **Tổng byte GPU** | | **31,301** |
| **Sau LZMA ×0,92** | `31,301 × 0,92` | **28,80** |
| **Cộng âm thanh** | §1.6.6 | **+18,83** |
| **TỔNG NỘI DUNG REMOTE CHƯƠNG 1** | | **≈ 47,6 MB** |

`47,6 ≤ T3 = 52` ⇒ **đạt**, còn **4,4 MB** biên. Đã cắt `77,77 − 47,6 = 30,2 MB` bằng đúng sáu nhát cắt C1–C6, mỗi nhát ghi rõ mất gì.

### 1.6.5. Ngân sách theo bundle và ba con số người chơi thực sự cảm thấy

| Nhóm | Nội dung | Byte GPU | ×0,92 | Âm thanh kèm | **Tổng MB** | Khi nào tải |
|---|---|---|---|---|---|---|
| `remote_catalog_data` | `chapter_01.json`, `areas/*.json`, `liveops_chapter_01.json` | — | — | — | **0,08** | Khởi động, **chặn** |
| `remote_shared_ui` | Atlas UI + 2 texture FX + con trỏ C12 | 0,7559 | 0,695 | — | **0,70** | Khởi động, **chặn** |
| `remote_area_san_gach` | Bộ nền + B1 (plate + parts) + `scare_bong_trong_chum` ×3 biến thể | 5,3086 | 4,884 | 0,08 stinger + 0,11 `_soft` | **5,07** | Khởi động, **chặn** |
| `remote_ambience_san_gach` | Ambience + độc thoại nội tâm khu vực 1 | — | — | 2,37 | **2,37** | Khởi động, **chặn** (xem §1.6.6) |
| `remote_area_hien_nha` | Bộ nền + B2 + `scare_ban_tay_giay_sau_manh` ×3 | 4,0904 | 3,763 | 0,06 + 0,11 | **3,93** | Tải trước khi vào khu vực 1 |
| `remote_ambience_hien_nha` | | — | — | 2,09 | **2,09** | Tải trước |
| `remote_area_gian_tho` | Bộ nền + B3 + B4 + 2 cú doạ ×3 | 6,9311 | 6,377 | 0,10 + 0,23 | **6,71** | Tải trước khi vào khu vực 2 |
| `remote_ambience_gian_tho` | | — | — | 3,85 | **3,85** | Tải trước |
| `remote_area_bep_gieng` | Bộ nền + B5 + `B5_lit` + `scare_mat_duoi_day_gieng` ×3 | 5,1997 | 4,784 | 0,08 + 0,11 | **4,97** | Tải trước khi vào khu vực 3 |
| `remote_ambience_bep_gieng` | | — | — | 3,27 | **3,27** | Tải trước |
| `remote_area_gac_xep` | Bộ nền + B6 + `B6_khoet` + **3 cú doạ** ×3 | 7,9012 | 7,269 | 0,12 + 0,34 | **7,73** | Tải trước khi vào khu vực 4 |
| `remote_ambience_gac_xep` | | — | — | 3,03 | **3,03** | Tải trước |
| `remote_ending` | C8 + C11 + hàng đuốc + nhạc kết chương | 0,6680 | 0,615 | 2,17 + 0,03 | **2,81** | Tải trước từ `area_bep_gieng` |
| `remote_ambience_shared` | 2 drone dùng chung | — | — | 0,60 | **0,60** | Tải trước, ưu tiên thấp nhất |
| `remote_item_icons` | Atlas `icon_item_*` × 10 | 0,4462 | 0,411 | — | **0,41** | **Bắt đầu ngay khi vào khu vực 1**, không chặn — xem ràng buộc bên dưới |
| `remote_event_*` | Giao diện sự kiện theo mùa | — | — | — | **5 – 7 / sự kiện** | Chỉ khi sự kiện đang chạy |
| | **Tổng nội dung Chương 1 (không tính sự kiện)** | | | | **≈ 47,6** | |

> **Ràng buộc của `remote_item_icons`:** khu vực 1 **không có** hotspot `COLLECT_ITEM` nào, nhưng `puz_khoa_bat_quai` **trao `item_chia_khoa_dong`** khi giải đúng — nên icon vật phẩm **vẫn cần có mặt trong khu vực 1**, chỉ là muộn hơn vài chục giây. Vì vậy atlas này **không** nằm trong lượt tải chặn (0,41 MB đủ đẩy lần chờ đầu lên `8,22 + 0,41 = 8,63 MB`, vượt T1), mà **bắt đầu tải ngay khi màn chơi mở** ở ưu tiên trung bình. Biên an toàn: `target_solve_sec` của `puz_khoa_bat_quai` là 90–240 giây, còn 0,41 MB ở 0,35 MB/s chỉ mất **1,2 giây**. Đường lui bắt buộc: nếu atlas chưa sẵn sàng lúc vật phẩm vào túi đồ thì hiện **icon mặc định trong `local_boot`** kèm `ten_vi`, và thay bằng icon thật khi tải xong — **không bao giờ** chặn người chơi vì một hình 160 × 160.

**Ba con số phải nói đúng:**

| Con số | Giá trị | Cách tính | Đối chiếu trần |
|---|---|---|---|
| **Lần chờ đầu tiên** | **8,22 MB → 14 – 24 giây trên 3G** | `0,08 (data) + 0,70 (shared_ui) + 5,07 (area_san_gach) + 2,37 (ambience khu vực 1)`. Thời gian: `8,22 / 0,58 = 14,2 s` · `8,22 / 0,45 = 18,3 s` · `8,22 / 0,35 = 23,5 s` | `≤ T1 = 8,5` ⇒ **đạt**, biên 0,28 MB |
| **Bundle khu vực lớn nhất** | **7,73 MB** (`remote_area_gac_xep` — ba cú doạ) | Xem bảng trên | `≤ T2 = 8,0` ⇒ **đạt**, biên 0,27 MB |
| **Tổng cache sau khi chơi hết chương** | **≈ 47,6 MB** | Tổng bảng trên | `≤ T3 = 52` ⇒ **đạt**, biên 4,4 MB |

> **Con số cũ "~4,6 MB, khoảng 6–10 giây" là sai gấp đôi:** nó lấy một lớp nền thay cho bộ nền bốn lớp, và nó bỏ ambience của khu vực đầu ra khỏi phép cộng. Con số đúng là **8,22 MB / 14–24 giây**, và nó **bắt buộc** màn hình tải đầu tiên phải là màn hình tiến độ thật (phần trăm + MB đã tải) chịu được việc người chơi khoá máy giữa chừng, chứ không phải một vòng xoay không đáy.

**Hai biên đều dưới 0,3 MB, nên phải có sẵn đòn bẩy tiếp theo trước khi cần đến nó.** Đòn bẩy rẻ nhất, đã đo sẵn: **tách `zoom_*` của mỗi khu vực thành nhóm `remote_puzzle_<puzzle_id>` tải lazy** đúng lúc hotspot `ZOOM_PUZZLE` chạy. Với khu vực 1 điều đó bỏ `(0,8789 + 0,6680) × 0,92 = 1,42 MB` khỏi lần chờ đầu tiên ⇒ còn **6,80 MB / 12–19 giây**. Cái giá: một vòng xoay ngắn ở lần đầu phóng to câu đố. Chỉ kích hoạt khi telemetry `bundle_download_start`/`_success` cho thấy phân vị 90 của lần chờ đầu vượt 25 giây.

### 1.6.6. Âm thanh — phân bổ lại, không tính lại

Tổng **18,80 MB** là số của tổ âm thanh (`04_horror.md` §3.10) và **không bị đụng tới**. Việc của tài liệu này là chia nó theo **cách nạp**, vì §3.3 đặt hai chế độ nạp hoàn toàn khác nhau cho hai loại file.

**Phần ADPCM tính được chính xác** — ADPCM 4 bit/mẫu, 22 050 Hz, mono ⇒ `22050 × 4 / 8 = 11 025 B/s = 10,77 KB/s`:

| Loại | Số file | Thời lượng mỗi file | Phép tính | MB |
|---|---|---|---|---|
| Stinger cú doạ (`sfx_scare_*`) | 8 | ≤ 2,0 s | `8 × 2,0 × 10,77 KB` = 172 KB | 0,17 |
| Tell (cảnh báo trước cú doạ) | 8 | ~1,5 s | `8 × 1,5 × 10,77 KB` = 129 KB | 0,13 |
| `sfx_ui_*`, `sfx_item_*` | ~30 | ~0,8 s | `30 × 0,8 × 10,77 KB` = 258 KB | 0,25 |
| | | | **Tổng ADPCM toàn chương** | **≈ 0,55** |

Tức **97% của 18,80 MB là nội dung dạng streaming** (ambience, độc thoại nội tâm, vox loa phát thanh, drone, nhạc kết chương). Phân bổ:

| Lớp | MB | Nằm ở đâu | Chế độ nạp |
|---|---|---|---|
| 8 tiếng UI ngắn | 0,08 | **`local_boot`** (trong APK) — menu khởi động luôn phải có tiếng | Decompress On Load |
| Stinger + tell của đúng khu vực | 0,47 | `remote_area_<area_id>` | **Decompress On Load**, nạp trước khi vào khu vực (§3.3 quy tắc 3) |
| `aud_soft_variants` (8 file `_soft` + tell kéo dài) | 0,90 | `remote_area_<area_id>` của đúng cú doạ | Decompress On Load — **biến thể an toàn, không được tách nhãn riêng** |
| Ambience + nội tâm + vox theo khu vực | 14,61 | `remote_ambience_<area_id>` | **Streaming từ đĩa**, sau khi bundle đã nằm trong cache |
| 2 drone dùng chung | 0,60 | `remote_ambience_shared` | Streaming từ đĩa |
| Nhạc + vox kết chương | 2,17 | `remote_ending` | Streaming từ đĩa |
| | **18,83** *(lệch +0,03 so với 18,80 do làm tròn hai chữ số thập phân ở bảy dòng)* | | |

> **"Phát trực tiếp, không tải trọn" là bất khả thi với remote AssetBundle — bỏ hẳn cách nói đó.** `AudioClip` đặt Load Type = *Streaming* vẫn đọc từ **file bundle trên đĩa**; Unity không phát nhạc thẳng từ một URL HTTP qua Addressables. Trình tự đúng luôn là: **tải trọn bundle về cache → mount → `AudioSource` streaming đọc từng khối từ file trong cache.** Hệ quả bắt buộc:
>
> 1. Ambience của khu vực đầu **nằm trên đường găng khởi động** và đã được cộng vào lần chờ đầu tiên ở §1.6.5.
> 2. Ambience của các khu vực sau đi cùng lượt tải trước của khu vực đó, ưu tiên thấp hơn bundle hình.
> 3. Ambience hỏng thì **im lặng lùi về không có tiếng nền** (nội dung tuỳ chọn, §7.3 quy tắc 1) — không bao giờ chặn người chơi.
> 4. Mỗi khu vực phải có một trường dữ liệu **trỏ tới** bundle ambience của nó, nếu không engine phải suy ra tên bằng quy ước chuỗi. Trường ấy được đặc tả là **`ambience_address`** trong `03_DATA_SPEC.md` §2.1 (đề nghị bổ sung schema).


---

# 2. CẤU TRÚC NHÓM ADDRESSABLES

## 2.1. Bảng nhóm

| Tên nhóm | Loại | Build/Load Path | Nhãn (label) | Nén | Nội dung | MB |
|---|---|---|---|---|---|---|
| `local_boot` | **Local** | `LocalBuildPath` / `LocalLoadPath` | `boot` | **LZ4** | Logo, màn hình tải, font, atlas UI tối thiểu, 8 tiếng UI ADPCM | ≤ 4,00 |
| `remote_catalog_data` | **Remote** | `RemoteBuildPath` / `{CDN}/{platform}/{catalog}` | `data` | **LZ4** | `chapter_01.json`, `areas/*.json`, `liveops_chapter_01.json` (TextAsset) | 0,08 |
| `remote_shared_ui` | **Remote** | như trên | `shared` | LZ4 | Khung phóng to câu đố, khung túi đồ, con trỏ `spr_ban_tay_nguoi_choi`, **2 texture FX dùng chung** (nhiễu tile + quầng đèn radial) | 0,70 |
| `remote_item_icons` | **Remote** | như trên | `shared`, `icons` | LZ4 | Atlas `icon_item_*` × 10 | 0,41 |
| `remote_area_<area_id>` | **Remote** | như trên | `area`, `<area_id>` | **LZMA** | **BỘ NỀN 4 lớp parallax** (`_l0_back`, `_l1_mid`, `_l2_fore` + lớp `_l3_fx` thủ tục), `zoom_*_plate` + `zoom_*_parts` của câu đố trong khu vực, và **mỗi cú doạ đúng ba file**: sheet gốc + `_soft` + `_static`, cùng stinger/tell ADPCM | 3,93 – 7,73 |
| `remote_ambience_<area_id>` | **Remote** | như trên | `ambience`, `<area_id>` | LZMA | Ambience, độc thoại nội tâm, vox của đúng khu vực đó — **tải trọn về cache rồi Streaming từ đĩa** | 2,09 – 3,85 |
| `remote_ambience_shared` | **Remote** | như trên | `ambience`, `shared` | LZMA | 2 drone dùng chung | 0,60 |
| `remote_ending` | **Remote** | như trên | `ending` | LZMA | `spr_ao_cuoi_giay`, `spr_ba_dong_to`, `spr_hang_duoc_duoi_san`, nhạc + vox kết chương | 2,81 |
| `remote_event_<event_id>` | **Remote** | như trên | `event`, `<event_id>` | LZMA | `override_bg`, khung giao diện, tiếng môi trường sự kiện | 5 – 7 |

**Nội dung một `remote_area_<area_id>` — viết ra để không ai quên lớp nào:**

| Thành phần | Số file | Ghi chú |
|---|---|---|
| Lớp nền `_l0_back` | 1 | 1920 × 1080, ASTC 6×6, **tắt mipmap** |
| Lớp nền `_l1_mid` | 1 | 1920 × 1080, có alpha, **chứa phần lớn hotspot** |
| Lớp nền `_l2_fore` | 1 | alpha-trim, trần **1920 × 600** (parallax 0,03 – 0,06) |
| Lớp `_l3_fx` | **0 file riêng** | Dựng bằng shader từ 2 texture dùng chung ở `remote_shared_ui` — **vẫn là lớp parallax thứ tư**, chỉ là nguồn ảnh dùng chung (nhát cắt **C1**, §1.6.3) |
| `zoom_<puzzle_id>_plate` / `_parts` | 2 – 4 | Theo số câu đố trong khu vực |
| Mỗi cú doạ: sheet gốc + **`_soft`** + **`_static`** | 3 × số cú doạ | **Bắt buộc cùng bundle** — xem khung dưới |
| Stinger + tell ADPCM + biến thể `_soft` âm thanh | 2 – 6 | Decompress On Load |

> **Vì sao `_soft` và `_static` KHÔNG được tách nhãn riêng để tải sau.** Chúng là tài sản của **tuỳ chọn trợ năng** (`gentle_mode`, `reduce_motion`, `scare_intensity = 0`). `02_PROMPT_DO_HOA.md` §6.5 và `04_horror.md` §4.7.5 quy định: *không tuỳ chọn an toàn nào được đặt sau bất kỳ cổng nào*. Một nhãn tải riêng **là** một cổng — cổng mạng. Người chơi bật chế độ nhẹ giữa lúc mất sóng mà biến thể nhẹ chưa có trong cache thì hoặc họ bị ném vào bản gốc (vi phạm), hoặc cú doạ không bắn (vỡ kịch bản). Vì vậy ba file đi cùng một bundle, tải cùng một lúc, và **chi phí của chúng nằm thẳng trong ngân sách khu vực**: 5,43 MB trên tổng 10,14 MB sprite doạ, tức **54%**. Đó là giá của nguyên tắc, và nó đã được trả trong §1.6.4.

**Năm nhóm khu vực là năm nhóm riêng biệt, không gộp.** Lý do không phải thẩm mỹ:

1. **Tải lại rẻ.** Unity **không** nối lại được một lượt tải bundle bị đứt giữa chừng — hỏng là tải lại từ đầu. Bundle 5 MB tải lại mất `5 / 0,45 ≈ 11` giây; bundle 47 MB tải lại mất gần hai phút và người chơi sẽ thoát game.
2. **Cập nhật hẹp.** Sửa một cú doạ ở gác xép chỉ đẩy lại `remote_area_gac_xep`, không bắt người chơi tải lại cả chương.
3. **Bộ nhớ.** Giải phóng bundle khu vực cũ khi rời khu vực, đỉnh RAM giữ dưới 180 MB trên máy 2 GB.
4. **Ambience tách khỏi hình.** Bundle ambience của một khu vực là **2 – 3,9 MB** toàn dữ liệu Vorbis — nó không nén thêm được và nó không cần có mặt cùng lúc với lớp nền. Tách ra cho phép ưu tiên hình trước, tiếng sau, và cho phép **bỏ qua hẳn** khi mạng kém (§7.3 quy tắc 1).

## 2.2. Vì sao dữ liệu JSON có nhóm riêng

`remote_catalog_data` tách khỏi asset vì **dữ liệu thay đổi thường xuyên hơn ảnh gấp nhiều lần**. Cân lại một `max_fails`, đổi một `text_key`, sửa một `bounds` — đó là bundle chỉ vài chục KB. Nếu JSON nằm chung với nền, mỗi lần cân bằng câu đố là người chơi phải tải lại 3,5 MB ảnh không đổi một pixel.

Nhóm này dùng **LZ4** thay vì LZMA vì nó nằm trên đường găng của lúc khởi động: LZ4 giải nén theo khối, đọc được ngay, trong khi LZMA phải giải nén trọn gói trước khi dùng.

## 2.3. Chọn chế độ nén

| Nhóm | Nén | Lý do |
|---|---|---|
| `local_boot` | **LZ4** | Nằm trong APK, đã bị AAB nén một lần nữa. LZ4 cho phép đọc ngẫu nhiên, mở màn hình tải tức thì. |
| `remote_catalog_data` | **LZ4** | Trên đường găng khởi động; kích thước đã nhỏ nên LZMA không lợi bao nhiêu. |
| `remote_area_*`, `remote_ambience_*`, `remote_ending`, `remote_event_*` | **LZMA** | Nhỏ hơn LZ4 khoảng 15–25% **so với LZ4**, không phải so với dữ liệu thô. Trên payload ASTC hệ số thật so với thô chỉ khoảng **0,92** (§1.6.1), trên payload Vorbis là **1,00**. Addressables tự **nén lại thành LZ4 trong cache** ở lần tải đầu, nên lần mở thứ hai vẫn nhanh. |

`[[ Đừng dùng "Uncompressed" cho remote với lý do "texture đã nén ASTC rồi". Header bundle, dữ liệu sprite, AudioClip metadata và chuỗi văn bản vẫn nén được — nhưng đừng kỳ vọng nhiều: hệ số kế hoạch cho phần ASTC là 0,92, tức 8%. Con số đó là ƯỚC LƯỢNG và phải đo lại bằng Addressables Analyze ngay sau bundle đầu tiên; nếu thực đo lệch quá 3 điểm phần trăm thì cập nhật hệ số ở §1.6.1 rồi chạy lại toàn bộ §1.6.4 và §1.6.5. ]]`

---

# 3. ĐỊNH DẠNG NÉN ASSET

## 3.1. Texture — Android

| Loại asset | Định dạng | Kích thước gốc | Bits/pixel | Ghi chú |
|---|---|---|---|---|
| Lớp nền `_l0_back`, `_l1_mid` | **ASTC 6×6** | 1920 × 1080 | 3,556 | **Tắt mipmap** — 2D orthographic không bao giờ thu nhỏ nền |
| Lớp nền `_l2_fore` | **ASTC 6×6** | ≤ 1920 × 600 (alpha-trim) | 3,556 | Trần khung do nhát cắt **C2** (§1.6.3). Cắt sát biên, không để vùng trong suốt thừa |
| Lớp nền `_l3_fx` | **shader** + 2 texture dùng chung | 512 × 512 mỗi texture | 3,556 | Nhát cắt **C1**. Vẫn là lớp parallax thứ tư, chỉ không còn file riêng cho từng khu vực |
| Sheet cú doạ gốc và `_soft` (`anim_*`) | **ASTC 8×8** | khung ≤ 768 px cạnh dài; ≤ 6 khung (gốc) / 3 khung (`_soft`) | 2,000 | Chạy 0,3–0,8 giây, mắt không kịp bắt lỗi nén — lập luận này áp cho **cả độ phân giải lẫn định dạng** |
| Biến thể `_static` | **ASTC 6×6** | một khung ≤ 768 px cạnh dài | 3,556 | Khung **đứng yên trên màn hình**, mắt có thời gian soi ⇒ không dùng 8×8 |
| Atlas `_parts` câu đố | **ASTC 6×6** | theo nội dung: 512² / 1024² / 1536×1024 | 3,556 | Không dùng 2048² mặc định — xem nhát cắt **C4** |
| Icon vật phẩm (`icon_item_*`) | **ASTC 6×6** | 256 × 256, gói vào SpriteAtlas | 3,556 | Một atlas 1024×1024 chứa đủ 10 vật phẩm |
| UI trong `local_boot` | **ASTC 6×6** | ≤ 1024² | 3,556 | — |

**Con số neo — đọc kỹ chữ "lớp":**

| Đơn vị | Phép tính | MB |
|---|---|---|
| **MỘT LỚP** 1920×1080 ASTC 6×6 | `ceil(1920/6)=320 × ceil(1080/6)=180 × 16 B = 921 600 B` | **0,8789** |
| **MỘT BỘ NỀN** = 4 lớp parallax bắt buộc của `02_PROMPT_DO_HOA.md` §2.2 | `_l0_back 0,8789 + _l1_mid 0,8789 + _l2_fore 0,4883 + _l3_fx 0 (dùng chung)` | **2,2461** |
| *Bộ nền nếu không cắt gì* | `4 × 0,8789` | *3,5156* |

> **Con số neo của ngân sách là 2,2461 MB cho MỘT BỘ NỀN, không phải 0,88 MB cho một ảnh.** `02_PROMPT_DO_HOA.md` §2.2 bắt buộc **bốn lớp** — `_l0_back` (parallax 0,00), `_l1_mid` (chứa phần lớn hotspot), `_l2_fore` (parallax 0,03–0,06), `_l3_fx` (khói, bụi, vignette) — cho **mọi** bối cảnh. Dùng 0,88 MB làm con số neo là bỏ sót ba lớp và làm sai lệch mọi ô của §1.6 theo hệ số 4. Xem §1.6.4 để biết phép cắt đã đưa 3,5156 về 2,2461 bằng cách nào.

**Vì sao ASTC 6×6 chứ không phải 4×4 hay 8×8:**

| Block | Bits/pixel | **MỘT LỚP** 1920×1080 | **BỘ NỀN 4 lớp** (2 lớp full + 1 lớp ≤1920×600 + FX dùng chung) | Đánh giá cho folk horror vẽ tay |
|---|---|---|---|---|
| 4×4 | 8,00 | `480×270×16` = **1,9775 MB** | **5,0537 MB** | Chất lượng thừa. Phong cách vẽ tay nhiều vệt mực và hạt nhiễu, mắt không phân biệt được với 6×6 |
| **6×6** | **3,556** | `320×180×16` = **0,8789 MB** | **2,2461 MB** | **Chốt.** Giữ được chuyển sắc tối trong bóng đổ, không thấy khối |
| 8×8 | 2,00 | `240×135×16` = **0,4944 MB** | **1,2634 MB** | Xuất hiện khối bẩn ở vùng chuyển sắc tối — chính là vùng quan trọng nhất của game này |

*Chênh lệch giữa 6×6 và 8×8 cho toàn bộ năm khu vực là `(2,2461 − 1,2634) × 5 = 4,91 MB` — đáng giá, vì vùng chuyển sắc tối là vùng game này sống bằng nó. Đó cũng là lý do 8×8 chỉ được dùng cho sheet cú doạ đang chuyển động, không dùng cho nền và không dùng cho `_static`.*

**Phủ thiết bị:** ASTC cần GLES 3.1 hoặc Vulkan. Với `minSdk 24` (Android 7.0) trở lên, phủ thực tế ~99% máy đang hoạt động năm 2026. Vẫn phải chuẩn bị đường lui:

- Xuất **biến thể ETC2 RGBA8** của nhóm `remote_area_*` (đặt nhãn `tex_etc2`).
- Lúc chạy, kiểm `SystemInfo.SupportsTextureFormat(TextureFormat.ASTC_6x6)`; sai thì chuyển sang nhãn `tex_etc2` bằng `Addressables.ResourceManager.InternalIdTransformFunc`.
- Chỉ dựng biến thể ETC2 **khi telemetry cho thấy có người dùng thật cần nó** — nó làm CDN phình gấp đôi.

## 3.2. Texture — iOS

| Loại asset | Định dạng | Ghi chú |
|---|---|---|
| Toàn bộ nền, overlay, UI | **ASTC 6×6** | Mọi máy Metal (A8 trở lên, iOS 13+) đều hỗ trợ ASTC gốc |
| Hoạt ảnh cú doạ | **ASTC 8×8** | Như Android |

**iOS không cần biến thể dự phòng.** PVRTC là di sản của thời trước A8, và nó bắt texture phải vuông + luỹ thừa của hai — điều kiện mà nền 1920×1080 không thoả. Đừng dùng.

**Hệ quả vận hành rất đáng giá:** vì cả hai nền tảng đều dùng ASTC 6×6 cùng kích thước, **nội dung ảnh giống hệt nhau về mặt bit**. Chỉ cần tách bundle theo nền tảng vì định dạng serialize của Unity khác nhau, còn quy trình sản xuất, bảng ngân sách và khâu QA hình ảnh là **một**.

## 3.3. Âm thanh

| Loại | Compression Format | Load Type | Sample Rate | Kênh | Lý do |
|---|---|---|---|---|---|
| Cú doạ ngắn (`sfx_scare_*`, < 2 giây) | **ADPCM** | **Decompress On Load** | 22 050 Hz | Mono | **Độ trễ bằng không.** Cú doạ trễ 80 ms là cú doạ hỏng. Vorbis phải giải mã lúc phát, ADPCM thì không |
| Âm thanh tương tác (`sfx_ui_*`, `sfx_item_*`) | **ADPCM** | Decompress On Load | 22 050 Hz | Mono | Như trên, và chúng rất ngắn |
| Tiếng môi trường lặp (`amb_*`, 30–120 giây) | **Vorbis** q = 0,5 | **Streaming** (đọc từ **file bundle đã nằm trong cache**, không phải từ HTTP) | 44 100 Hz | Stereo | Không chiếm RAM; chất lượng stereo là phần lớn cảm giác không gian |
| Nhạc chủ đề, cảnh kết | **Vorbis** q = 0,6 | Streaming | 44 100 Hz | Stereo | — |
| Lời thoại (nếu Chương 2 có) | Vorbis q = 0,4 | Compressed In Memory | 22 050 Hz | Mono | — |

**Ba quy tắc âm thanh không thương lượng:**

1. **Force To Mono cho mọi thứ dưới 2 giây.** Cú doạ phát ở giữa không gian âm thanh; stereo chỉ nhân đôi dung lượng vô ích.
2. **Không bao giờ dùng Streaming cho cú doạ.** Streaming đọc từ đĩa lúc phát — đúng thứ gây trễ mà §3.3 đang tránh.
   **Và Streaming không có nghĩa là "phát thẳng từ mạng".** Load Type = *Streaming* đọc từng khối từ **file bundle trên đĩa**; Addressables **không** phát audio thẳng từ URL. Trình tự luôn là *tải trọn bundle → cache → streaming từ cache*. Hệ quả ngân sách nằm ở §1.6.6.
3. **Nạp trước `AudioClip` cú doạ khi vào khu vực, không phải khi cú doạ bắn.** Nằm trong bundle khu vực, nên bước tải trước ở §4 đã lo. `04_horror.md` quy định envelope; engine chỉ cần bảo đảm clip đã ở trong RAM trước đó.

`[[ Định dạng file trong dữ liệu ghi là ".ogg" (xem jumpscares[].audio_asset, 03_DATA_SPEC.md muc 2.5.1 tro nguoc ve DUNG muc 3.3 nay). Đó là tên asset nguồn; thiết lập import của Unity mới quyết định định dạng lúc chạy. Một file .ogg nguồn hoàn toàn có thể được import thành ADPCM — và với sfx_scare_* thì bắt buộc phải thế. ]]`

---

# 4. CHIẾN LƯỢC TẢI TRƯỚC VÀ TẢI LAZY

## 4.1. Dòng thời gian khởi động

```
t=0,0s    Ứng dụng mở, màn hình tải hiện ngay (từ local_boot, không cần mạng)
t=0,1s    Addressables.InitializeAsync()
t=0,3s    Kiểm & cập nhật catalog  (CheckForCatalogUpdates → UpdateCatalogs)
t=0,6s    Tải nhóm nhãn "data"            (0,08 MB)  → phân tích chapter_01.json
t=0,8s    Tải tuần tự theo ưu tiên (KHÔNG song song hết — xem ghi chú):
             [1] nhãn "shared"                    0,70 MB
             [2] nhãn "area_san_gach"             5,07 MB   ← mở được màn chơi từ đây
             [3] nhãn "ambience" + "area_san_gach" 2,37 MB
t=14-24s  Xong cả ba → vào area_san_gach
          ↓ NGAY KHI VÀO, ngầm tải trước theo thứ tự:
             remote_item_icons (0,41)  →  remote_area_hien_nha (3,93)
             →  remote_ambience_hien_nha (2,09)
```

**Cách tính mốc `t=14-24s`:** tổng phải tải là `0,08 + 0,70 + 5,07 + 2,37 = 8,22 MB` (§1.6.5). Chia cho ba mức thông lượng 3G Việt Nam mà §1.6.3 đã chốt: `8,22 / 0,58 = 14,2 s` · `8,22 / 0,45 = 18,3 s` · `8,22 / 0,35 = 23,5 s`. Cộng ~0,8 s cho khởi tạo và catalog.

> **Dòng thời gian này là dòng thời gian trên 3G. Trên Wi-Fi nó chỉ còn 2–4 giây** (`8,22 / 2,5 ≈ 3,3 s`) — nhưng **không được lấy con số Wi-Fi làm mặc định khi thiết kế màn hình tải**, và cũng **không được đặt lần tải bắt buộc này sau bất kỳ điều kiện "chỉ Wi-Fi" nào. Đây là nội dung bắt buộc; §4.4 quy định nó luôn tải, kể cả trên 3G/4G, kèm giải thích rõ ràng.**

**Ba yêu cầu bắt buộc với màn hình tải, là hệ quả trực tiếp của 24 giây:**

1. **Tiến độ thật:** phần trăm + số MB đã tải / tổng, lấy từ `AsyncOperationHandle.PercentComplete` và `GetDownloadSizeAsync`. Không dùng vòng xoay không đáy.
2. **Chịu được gián đoạn:** người chơi khoá máy hoặc chuyển app giữa chừng thì lượt tải tiếp tục hoặc tiếp lại từ bundle chưa xong — **không** bắt đầu lại từ bundle đầu tiên.
3. **Mở được màn chơi trước khi ambience xong:** bước [2] xong là vào được `area_san_gach`; bước [3] chạy tiếp ở nền và tiếng nền vào sau. Một khu vực im lặng trong 5 giây đầu tốt hơn một màn hình tải dài thêm 5 giây.

**Từ khu vực 2 trở đi người chơi không chờ nữa.** Bundle đã nằm sẵn trong cache trước khi họ chạm vào cánh cửa — thời gian một người chơi ở lại một khu vực (90–240 giây, theo `target_solve_sec`) dài hơn nhiều lần thời gian tải bundle lớn nhất: `7,73 / 0,35 = 22 giây` ở tốc độ 3G tệ nhất, và đó cũng chính là cách trần **T2 = 8,0 MB** ở §1.6.3 được đặt ra.

## 4.2. Bảng chính sách tải theo từng nhóm

| Nhóm | Chính sách | Kích hoạt bởi | Ưu tiên |
|---|---|---|---|
| `local_boot` | Trong APK | — | — |
| `remote_catalog_data` | **Bắt buộc, chặn** | Khởi động | Cao nhất |
| `remote_shared_ui` | **Bắt buộc, chặn** | Khởi động | Cao |
| `remote_area_<khu vực đầu>` | **Bắt buộc, chặn** | Khởi động | Cao |
| `remote_ambience_<khu vực đầu>` | **Bắt buộc, KHÔNG chặn** — vào được màn chơi trước, tiếng vào sau | Khởi động, ngay sau bundle hình | Trung bình |
| `remote_item_icons` | **Tải trước, ngầm** — bắt buộc xong **trước khi câu đố đầu tiên được giải**, có đường lui icon mặc định | Vào khu vực đầu | Trung bình |
| `remote_area_<khu vực kế tiếp>` | **Tải trước, ngầm** | Vào khu vực hiện tại | Thấp |
| `remote_ambience_<khu vực kế tiếp>` | **Tải trước, ngầm** — sau bundle hình của cùng khu vực | Vào khu vực hiện tại | Thấp |
| `remote_area_<còn lại>` | **Lazy** | Ngay trước khi `CHANGE_AREA` chạy | Theo yêu cầu |
| `remote_ambience_shared` | **Tải trước, ngầm** | Sau khi khu vực kế tiếp xong | Thấp nhất |
| `remote_ending` | **Tải trước, ngầm** | Vào `area_bep_gieng` (theo `04_horror.md` §3.10) | Thấp |
| `remote_event_*` | Theo `download_policy` của sự kiện | Xem `04_LIVEOPS` §4 | Thấp nhất |

**Quy tắc thứ tự trong một lượt tải trước:** hình trước, tiếng sau. Nếu chỉ tải kịp một thứ trước khi người chơi mở cửa, thì thứ phải kịp là bộ nền — thiếu nền là màn hình chờ, thiếu ambience chỉ là im lặng.

**Quy tắc "khu vực kế tiếp" đọc từ dữ liệu, không hard-code.** Khu vực kế tiếp lấy từ `area_order` trong `chapter_01.json`; đồng thời tải trước cả những khu vực mà hotspot `CHANGE_AREA` của khu vực hiện tại trỏ tới (người chơi quay lui được). Với `area_gian_tho` — nơi có tới bốn cửa — điều đó nghĩa là quay lui về `area_hien_nha` không bao giờ phải chờ.

## 4.3. Giải phóng bộ nhớ

| Sự kiện | Hành động |
|---|---|
| Rời một khu vực | `Addressables.Release` handle của khu vực đó **sau 30 giây** (đề phòng quay lui ngay) |
| Nhận cảnh báo bộ nhớ thấp | Giải phóng ngay mọi khu vực trừ khu vực hiện tại, rồi `Resources.UnloadUnusedAssets()` |
| Kết thúc chương | Giải phóng tất cả trừ `shared` và `boot` |

**Không bao giờ gọi `Addressables.ClearDependencyCacheAsync` như một cách "dọn dẹp".** Nó xoá file đã tải trên đĩa, buộc tải lại từ CDN. Chỉ dùng đúng một trường hợp: khi phát hiện CRC sai (§7.4).

## 4.4. Hạn mức tải trên mạng di động — hai khoá, không phải một

**Lỗi đã sửa:** một khoá `wifi_only_default` duy nhất áp cho **cả** nội dung tuỳ chọn lẫn nội dung bắt buộc sẽ **vô hiệu hoá toàn bộ §4.1 và §4.2** đối với người chơi dùng 3G/4G — tức phần lớn tệp người chơi mục tiêu. Họ sẽ không tải được `remote_area_san_gach`, và game đứng ở màn hình tải. Phải tách làm hai khoá độc lập:

| Khoá trong `remote_config_keys` | Mặc định | Chi phối | Nếu bật `true` thì chuyện gì xảy ra |
|---|---|---|---|
| `bundle_wifi_only_default` | **`false`** | Nội dung **bắt buộc**: `remote_catalog_data`, `remote_shared_ui`, `remote_area_<khu vực đang vào>`, `remote_ambience_<khu vực đang vào>` | Người chơi 3G/4G **không vào được game**. Chỉ đặt `true` khi có sự cố CDN và cần chặn lưu lượng khẩn cấp |
| `prefetch_wifi_only_default` | **`true`** | Nội dung **tải trước**: khu vực kế tiếp, ambience kế tiếp, `remote_ending`, `remote_item_icons`, `remote_event_*` | Tải trước hoãn lại trên mạng di động. Khi người chơi thật sự mở cửa sang khu vực chưa có, nó chuyển thành **tải bắt buộc** và chạy bất kể loại mạng, kèm màn hình tiến độ |

`seasonal_events[].addressables.download_policy = PREFETCH_ON_WIFI` của `liveops_chapter_01.json` đọc **`prefetch_wifi_only_default`**, không đọc `bundle_wifi_only_default`.

| Tình huống | Xử lý |
|---|---|
| Wi-Fi | Tải trước tự do |
| Di động, **nội dung bắt buộc** | **Luôn tải**, kể cả khi người chơi đặt "chỉ Wi-Fi" — kèm một dòng giải thích và số MB, không kèm nút huỷ dẫn tới ngõ cụt |
| Di động, tải trước gói ≤ 5 MB, `prefetch_wifi_only_default = false` | Tải im lặng, không hỏi |
| Di động, tải trước gói > 5 MB | Hỏi một lần bằng `GetDownloadSizeAsync`, nhớ lựa chọn |
| Di động, `prefetch_wifi_only_default = true` (mặc định) | Hoãn toàn bộ tải trước. Vào khu vực mới sẽ có một lần chờ `3,93 – 7,73 MB` ⇒ **11 – 22 giây** ở 0,35 MB/s — chấp nhận được, và đó là cái giá đổi lấy việc không ngốn data của người chơi |

> **Dòng thời gian khởi động ở §4.1 chỉ là dòng thời gian trên Wi-Fi nếu `prefetch_wifi_only_default = true`** — phần tải trước `remote_item_icons` và `remote_area_hien_nha` sau mốc "vào area_san_gach" **không chạy** trên mạng di động. Phần **trước** mốc đó (8,22 MB nội dung bắt buộc) chạy trên mọi loại mạng, không ngoại lệ.

---

# 5. KIẾN TRÚC CMS → CDN → CLIENT

## 5.1. Sơ đồ đường đi của một thay đổi

```
[1] NGUỒN SỰ THẬT — kho Git
        data/chapter_01.json, data/areas/*.json, data/liveops_chapter_01.json
        Assets/Art/**, Assets/Audio/**
                 │  pull request
                 ▼
[2] CỔNG CI — bắt buộc xanh mới được merge
        python3 tools/validate_level.py --strict
        Kiểm JSON Schema · tham chiếu chéo · chồng lấn · chu trình · KHẢ GIẢI
                 │  merge vào main
                 ▼
[3] DỰNG BẢN — Unity Cloud Build / runner tự quản
        Addressables "Update a Previous Build"  (dùng addressables_content_state.bin)
        Xuất: catalog_2026.09.15.1.json + .hash + các bundle đã đổi
                 │  tải lên
                 ▼
[4] CDN — lưu trữ đối tượng + edge cache
        https://cdn.linhanthon.game/assets/{android|ios}/{catalog_version}/...
        Bất biến theo phiên bản · Cache-Control: immutable · TTL 1 năm
                 │  trỏ tới
                 ▼
[5] REMOTE CONFIG — Firebase
        addressables_catalog_url = ".../2026.09.15.1/catalog.json"
        liveops_config_version   = "1.0.1"
                 │  đọc lúc khởi động
                 ▼
[6] CLIENT — máy người chơi
        Đọc remote config → cập nhật catalog → tải bundle đã đổi → chơi
```

## 5.2. Quy ước đường dẫn CDN

```
https://cdn.linhanthon.game/assets/
    android/
        2026.09.15.1/
            catalog.json
            catalog.hash
            remote_catalog_data_assets_<hash>.bundle
            remote_area_san_gach_assets_<hash>.bundle
            ...
        2026.09.22.1/              ← bản kế tiếp, thư mục riêng
    ios/
        2026.09.15.1/
            ...
```

| Quy tắc | Lý do |
|---|---|
| **Thư mục theo phiên bản, không ghi đè** | Bản cũ vẫn chạy được trong lúc bản mới đang triển khai dần. Quay lui chỉ là đổi một chuỗi trong remote config |
| **`Cache-Control: public, max-age=31536000, immutable`** cho bundle | Đường dẫn đã chứa hash, nội dung không bao giờ đổi tại chỗ |
| **`Cache-Control: public, max-age=60`** cho `catalog.json` và `.hash` | Đẩy bản mới có hiệu lực trong vòng một phút |
| Tách hoàn toàn `android/` và `ios/` | Định dạng serialize của bundle khác nhau giữa hai nền tảng |
| Bật nén Brotli/gzip ở tầng HTTP cho `catalog.json` | Catalog là JSON văn bản, nén được 70–80% |

### 5.2.1. Luật hoà giải `background_asset_url` — khoá logic, không phải URL thật

`background_asset_url` là **khoá bắt buộc của Master Form**: cấm đổi tên, cấm bỏ, cấm đổi vị trí. Nhưng giá trị hiện nay của nó trong `data/areas/*.json` là một URL tuyệt đối **phẳng**:

```
https://cdn.linhanthon.game/assets/bg_gian_tho.bundle
```

URL đó **không có `{platform}` và không có `{catalog_version}`**, nên nếu engine dùng nó nguyên văn thì:

- nó trỏ ra ngoài cây thư mục `assets/{android|ios}/{catalog_version}/` của §5.2 ⇒ **404**;
- và quay lui ở §6.4 (trỏ `addressables_catalog_url` về thư mục phiên bản trước) **không có tác dụng** với nền, vì nền vẫn đi thẳng tới đường dẫn phẳng.

**Cách hoà giải — giữ nguyên khoá, đổi cách đọc.** Có đúng một luật, và nó áp cho cả engine lẫn validator:

> **`background_asset_url` là KHOÁ LOGIC (Addressables key), không phải địa chỉ mạng.** Engine **không bao giờ** gọi HTTP bằng chuỗi này. Engine lấy phần `basename` không đuôi làm Addressables key, rồi để **`InternalIdTransformFunc`** ghép nền tảng và phiên bản catalog lúc chạy.

| Bước | Ai làm | Kết quả |
|---|---|---|
| 1. Rút khoá | Lớp nạp dữ liệu | `".../bg_gian_tho.bundle"` → khoá `bg_gian_tho` |
| 2. Tra catalog | Addressables | Tìm bundle chứa `bg_gian_tho` trong catalog đang dùng |
| 3. Ghép đường dẫn thật | `InternalIdTransformFunc` | `{RemoteLoadPath}` = `https://cdn.linhanthon.game/assets/{platform}/{catalog_version}/` |
| 4. Tải | Addressables | `.../assets/android/2026.09.15.1/remote_area_gian_tho_assets_<hash>.bundle` |

```csharp
// Đăng ký MỘT LẦN, ngay sau Addressables.InitializeAsync()
Addressables.ResourceManager.InternalIdTransformFunc = location =>
{
    var id = location.InternalId;
    if (!id.StartsWith("http")) return id;                 // bundle local, để yên
    // {platform} và {catalog_version} đọc từ Remote Config, không hard-code
    return id.Replace("{platform}",        RuntimePlatformSlug)   // "android" | "ios"
             .Replace("{catalog_version}", ActiveCatalogVersion); // "2026.09.15.1"
};

// Nạp nền của một khu vực
static string BundleKey(string assetUrl) =>
    System.IO.Path.GetFileNameWithoutExtension(new System.Uri(assetUrl).AbsolutePath);
// BundleKey("https://cdn.linhanthon.game/assets/bg_gian_tho.bundle") == "bg_gian_tho"
```

**Ba hệ quả kiểm được:**

| Hệ quả | Cưỡng chế ở đâu |
|---|---|
| Phần `https://cdn.linhanthon.game/assets/` trong dữ liệu là **trang trí, có để thoả schema**; đổi CDN **không** cần sửa `data/areas/*.json`, chỉ cần đổi `RemoteLoadPath` trong Remote Config | §5.3, `addressables_catalog_url` |
| Validator kiểm **tồn tại của khoá**, không kiểm với tới được URL: `basename` phải khớp `^bg_[a-z0-9_]+$` và phải bằng `"bg_" + area_id.removePrefix("area_")` | `tools/validate_level.py`, và `03_DATA_SPEC.md` §2.1 |
| Quay lui ở §6.4 **có tác dụng với cả nền**, vì nền cũng đi qua `{catalog_version}` | §6.4, §8.3 |

`[[ Cùng luật này áp cho seasonal_events[].override_bg và cho icon_asset của item_catalog: mọi chuỗi ".bundle" / ".png" trong dữ liệu đều là khoá logic. Quy tắc một câu: dữ liệu nói ĐIỀU GÌ, catalog nói Ở ĐÂU. ]]`

## 5.3. Ba nguồn cấu hình lúc chạy và thứ tự ưu tiên

| Nguồn | Chứa gì | Đổi được không cần build lại |
|---|---|---|
| **Hằng số trong APK** | URL CDN dự phòng, catalog gốc | Không |
| **Firebase Remote Config** *(hoặc endpoint JSON tự quản nếu chọn Kịch bản B ở §1.3)* | `remote_config_keys` — **36 khoá**: 32 khoá hiện có **cộng 4 khoá bắt buộc bổ sung** mà tài liệu này phụ thuộc (§5.3.1) | **Có**, trong vài phút |
| **Bundle dữ liệu** (`remote_catalog_data`) | Toàn bộ `data/**` — bố cục màn chơi, lời giải câu đố, cú doạ | **Có**, sau khi đẩy catalog |

Ưu tiên khi đọc: **Remote Config → Bundle dữ liệu → Hằng số trong APK**. Remote config hỏng hoặc quá hạn thì client lùi về catalog cuối cùng đã tải thành công; hết cách thì mới dùng hằng số trong APK.

### 5.3.1. Bốn khoá bổ sung mà tài liệu này phụ thuộc

`liveops_chapter_01.json` → `remote_config_keys` hiện có **32** khoá. Tài liệu này yêu cầu thêm **4** khoá, và sửa mặc định của **1** khoá đã có. Tổng sau khi bổ sung: **`32 + 4 = 36` khoá**. Chủ quản của bảng là `04_LIVEOPS_MONETIZATION.md`; mục này chỉ ghi lại **vì sao** tài liệu §4 và §7 không chạy được nếu thiếu chúng.

| Khoá | Kiểu | Mặc định | Vì sao bắt buộc | Dùng ở mục |
|---|---|---|---|---|
| `kill_switch_telemetry` | bool | `false` | §6.4 và §8.3 hứa **năm** kill-switch độc lập; `rollout.kill_switches` đã có đủ năm, nhưng `remote_config_keys` mới có bốn ⇒ **telemetry là cái duy nhất không tắt được từ xa**. Đúng cái phải tắt được nhanh nhất khi có sự cố riêng tư hoặc khi đường ống đo đạc tự nó gây lỗi | §6.4, §8.3 |
| `bundle_retry_backoff_sec` | json (mảng số) | `[3, 9]` | §7.2 phải **trỏ tới một nguồn duy nhất** cho giãn cách thử lại thay vì ghi lại con số. Độ dài mảng cũng chính là `bundle_retry_count` ⇒ validator kiểm được hai khoá khớp nhau | §7.2 |
| `bundle_connect_timeout_sec` | int | `8` | Hết giờ **kết nối** phải tách khỏi hết giờ **toàn request** — xem §7.2. Không có khoá này thì hai khái niệm lại dồn vào một con số và lỗi cũ quay lại | §7.2 |
| `prefetch_wifi_only_default` | bool | `true` | Tách khỏi `bundle_wifi_only_default` để chính sách "chỉ Wi-Fi" không chặn **nội dung bắt buộc** — xem §4.4 | §4.4 |

| Khoá đã có, phải **đổi mặc định** | Cũ | Mới | Lý do |
|---|---|---|---|
| `bundle_download_timeout_sec` | `8` | **`90`** (chấp nhận 60 – 120) | 8 giây là hết giờ **toàn bộ request** của `UnityWebRequest`, mà một bundle 7,73 MB trên 3G cần tới 22 giây. Xem §7.2 |
| `bundle_wifi_only_default` | `true` | **`false`** | Áp `true` cho nội dung bắt buộc thì người chơi 3G/4G không vào được game. Xem §4.4 |

---

# 6. QUY TRÌNH CẬP NHẬT NỘI DUNG KHÔNG BUILD LẠI APP

## 6.1. Cái gì đổi được, cái gì không

| Thay đổi | Cần build lại? | Cách làm |
|---|---|---|
| Sửa `bounds` của một hotspot | **Không** | Sửa JSON → đẩy catalog |
| Đổi `solution` của một câu đố | **Không** | Sửa JSON → đẩy catalog |
| Đổi `max_fails` của một cú doạ | **Không** | Sửa JSON → đẩy catalog |
| Vẽ lại một ảnh nền | **Không** | Thay asset → đẩy catalog |
| Thêm cú doạ mới **dùng `trigger_type` đã có** | **Không** | Thêm asset + mục JSON → đẩy catalog |
| Sửa giá gợi ý, lịch sự kiện, cấu hình A/B | **Không** | Chỉ cần Remote Config |
| Thêm khu vực mới vào Chương 1 | **Không** | Nhóm mới + mục manifest → đẩy catalog |
| Thêm **`action_type` mới** (vd `USE_ITEM_ON_ITEM`) | **CÓ** | Engine chưa có mã xử lý |
| Thêm **`puzzle type` mới** | **CÓ** | Cần scene và mã cơ chế mới |
| Nâng phiên bản Unity, đổi SDK | **CÓ** | — |
| Đổi `schema_version` không tương thích ngược | **CÓ** | Bản cũ không đọc được dữ liệu mới |

> **Lằn ranh nằm ở đâu:** thay đổi **dữ liệu** thì đẩy được; thay đổi **từ vựng của hợp đồng** thì phải build lại. Đúng sáu `action_type`, sáu `puzzle type`, năm `trigger_type` là toàn bộ vốn từ mà engine hiểu. Chừng nào nội dung mới còn nói bằng vốn từ đó, cửa hàng ứng dụng không cần biết tới.

## 6.2. Quy trình chín bước

| # | Bước | Lệnh / thao tác | Cổng chặn |
|---|---|---|---|
| 1 | Sửa nội dung trên nhánh riêng | — | — |
| 2 | Kiểm cục bộ | `python3 tools/validate_level.py --strict` | Mã thoát phải là 0 |
| 3 | Mở pull request | — | CI chạy lại bước 2 |
| 4 | Duyệt và merge | — | Một người duyệt |
| 5 | Nạp `addressables_content_state.bin` của **bản phát hành đang chạy** | Từ kho lưu trữ bản build | File phải khớp đúng bản đang live |
| 6 | **Check for Content Update Restrictions** | Cửa sổ Addressables Groups | Không nhóm `Cannot Change Post Release` nào bị đụng |
| 7 | **Update a Previous Build** | Sinh catalog + bundle delta | — |
| 8 | Tải lên CDN theo thư mục phiên bản mới | `aws s3 sync` / `wrangler r2` | Kiểm tổng checksum |
| 9 | Đổi `addressables_catalog_url` trong Remote Config | Triển khai dần: 5% → 25% → 100% | Theo dõi `event_bundle_download_fail` |

## 6.3. Ba cái bẫy chết người

| Bẫy | Hậu quả | Phòng tránh |
|---|---|---|
| **Mất `addressables_content_state.bin`** | Không dựng được bản cập nhật; mọi người chơi phải tải lại toàn bộ nội dung | Lưu file này **cùng với mọi bản phát hành**, trong kho artifact, không phải trong Git |
| **Đụng vào nhóm `Cannot Change Post Release`** | Máy cũ tải bundle không khớp catalog → treo ở màn hình tải | Bước 6 là **bắt buộc**, không phải khuyến nghị |
| **Ghi đè thư mục CDN của bản cũ** | Người chơi đang chơi dở bị đứt giữa chừng | Thư mục theo phiên bản + `immutable`, không bao giờ ghi đè |

## 6.4. Quay lui

Quay lui là **đổi một chuỗi**: trỏ `addressables_catalog_url` về thư mục phiên bản trước. Không cần dựng lại, không cần đụng store, có hiệu lực trong vòng một phút nhờ TTL 60 giây của catalog.

Quay lui **có tác dụng với cả ảnh nền** — nhưng chỉ vì luật hoà giải ở §5.2.1: `background_asset_url` là khoá logic, phiên bản thư mục do `{catalog_version}` quyết định lúc chạy. Nếu engine dùng chuỗi URL phẳng trong dữ liệu làm địa chỉ thật thì cơ chế quay lui này **gãy im lặng**: catalog lùi về bản cũ mà ảnh nền vẫn là ảnh mới.

Đi kèm là **năm** `kill_switch_*` — tắt được quảng cáo, IAP, giao diện sự kiện, gợi ý trả phí, telemetry **độc lập với nhau**, mà không cần đụng tới catalog:

| Kill-switch | Có trong `rollout.kill_switches` | Có trong `remote_config_keys` | Tắt được từ xa? |
|---|---|---|---|
| `kill_switch_ads` | ✓ | ✓ | Có |
| `kill_switch_iap` | ✓ | ✓ | Có |
| `kill_switch_event_theme` | ✓ | ✓ | Có |
| `kill_switch_paid_hints` | ✓ | ✓ | Có |
| `kill_switch_telemetry` | ✓ | **THIẾU → phải bổ sung, xem §5.3.1** | **Chưa** |

> Một kill-switch chỉ có trong `rollout.kill_switches` mà **không** có trong `remote_config_keys` là một công tắc **nằm trong bundle dữ liệu**: muốn bật nó phải dựng lại bundle, đẩy catalog, chờ triển khai — mất hàng chục phút thay vì một phút. Đó không phải công tắc khẩn cấp. Bổ sung `kill_switch_telemetry` vào `remote_config_keys` là điều kiện để §8.3 nói thật khi nó viết "đã thử cả năm kill-switch".

---

# 7. XỬ LÝ LỖI MẠNG VÀ TẢI THẤT BẠI

## 7.1. Bảng tình huống lỗi

| Tình huống | Phát hiện bằng | Xử lý | Người chơi thấy gì |
|---|---|---|---|
| Không có mạng lúc khởi động | `InitializeAsync` lỗi hoặc `CheckForCatalogUpdates` hết giờ | Dùng catalog đã cache lần trước | Không thấy gì — game chạy bình thường nếu đã chơi trước đó |
| Không có mạng, **và** chưa từng chơi | Cache trống | Màn hình "cần mạng để tải nội dung lần đầu" + nút thử lại | Thông báo rõ ràng, không phải màn hình lỗi kỹ thuật |
| Catalog tải được, bundle khu vực hỏng | `AsyncOperationHandle.Status == Failed` | Thử lại theo `bundle_retry_count` / `bundle_retry_backoff_sec` (§7.2), rồi hiện nút thử lại | Vòng xoay chờ → thông báo + nút "Thử lại" |
| Mạng đứt **giữa lúc** tải | Handle lỗi | Như trên. Bundle 3,93 – 7,73 MB nên tải lại tốn 11–22 giây ở 0,35 MB/s — khó chịu nhưng chịu được; đó là lý do trần T2 đặt ở 8,0 MB | Như trên |
| Tải **đứng** — kết nối mở nhưng không có byte nào về | Bộ đếm tiến độ `DownloadHandler` không tăng trong `bundle_connect_timeout_sec` | **Huỷ thủ công** rồi tính là một lần hỏng (§7.2) | Như trên |
| **Ambience** của khu vực hỏng | Handle lỗi | **Im lặng bỏ qua** — nội dung tuỳ chọn (§7.3 quy tắc 1). Thử lại một lần ở lần vào khu vực sau | Không thấy gì; khu vực không có tiếng nền |
| Bundle sự kiện theo mùa hỏng | Handle lỗi sau `bundle_download_timeout_sec` | **Lùi về nền gốc** (`USE_BASE_BACKGROUND`), tắt giao diện sự kiện cho phiên này | Chơi bình thường + một toast nhẹ |
| CRC sai / bundle hỏng trong cache | Addressables báo lỗi CRC | `ClearDependencyCacheAsync` cho **đúng khoá đó**, rồi tải lại một lần | Vòng xoay chờ lâu hơn chút |
| Hết dung lượng đĩa | `IOException` lúc ghi cache | Dừng tải trước, giải phóng khu vực không dùng, báo người chơi | Thông báo dọn bớt dung lượng |
| CDN trả 403/404 (sai cấu hình triển khai) | Mã HTTP | Lùi về catalog cuối cùng đã cache, bắn cảnh báo telemetry mức cao | Không thấy gì |

## 7.2. Chính sách thử lại và hai loại hết giờ

### 7.2.1. Một nguồn sự thật duy nhất cho số lần và giãn cách

Ba nơi đang ghi ba con số khác nhau: tài liệu này ghi **3 lần (1 s / 3 s / 8 s)**, `04_LIVEOPS_MONETIZATION.md` và `liveops_chapter_01.json` ghi **2 lần (3 s / 9 s)`. Chốt một nguồn, và nguồn đó **không phải** tài liệu này:

> **Nguồn sự thật là `remote_config_keys` trong `liveops_chapter_01.json`.** Mục này **chỉ trỏ tới khoá**, không ghi lại giá trị. Muốn đổi chính sách thử lại thì đổi remote config — không sửa tài liệu, không dựng lại app.

| Tham số | Khoá đọc ra | Ràng buộc |
|---|---|---|
| Số lần thử lại | `bundle_retry_count` | `1 ≤ v ≤ 5`. **Phải bằng** `len(bundle_retry_backoff_sec)` |
| Giãn cách giữa các lần | `bundle_retry_backoff_sec` (mảng số giây) | Tăng dần. Mỗi lần chờ cộng **nhiễu ngẫu nhiên 0 – 500 ms** để cả đám người chơi không cùng đập vào CDN sau một sự cố |
| Hết giờ **kết nối** | `bundle_connect_timeout_sec` | Xem §7.2.2 |
| Hết giờ **toàn bộ request** | `bundle_download_timeout_sec` | Xem §7.2.2 |
| Sau khi hết lượt thử | — | Chuyển sang **thao tác thủ công**. Không tự thử lại vô hạn — nó ngốn pin và data của người chơi |

**Validator cưỡng chế** `bundle_retry_count == len(bundle_retry_backoff_sec)`; lệch là `[LỖI]`. Nhờ vậy không thể lặp lại tình trạng ba tài liệu ba con số.

### 7.2.2. `AssetBundleRequestOptions.Timeout` là hết giờ TOÀN BỘ REQUEST

Đây là lỗi nghiêm trọng nhất ở bản trước của mục này, và nó là lỗi **về API**, không phải về khẩu vị:

> `AssetBundleRequestOptions.Timeout` được Addressables đổ thẳng vào **`UnityWebRequest.timeout`**. Tài liệu Unity định nghĩa `UnityWebRequest.timeout` là *"số giây chờ trước khi request bị huỷ"* — tính từ lúc gửi cho tới lúc **nhận xong**. Nó **KHÔNG** phải connect timeout. Không có cách nào cấu hình riêng connect timeout qua `UnityWebRequest`.

Hệ quả của con số cũ: đặt `Timeout = 8` cho một bundle **7,73 MB** trong khi 3G Việt Nam cần `7,73 / 0,35 = 22 giây` ⇒ **mọi lượt tải trên 3G đều bị chính client huỷ ở giây thứ 8**, thử lại, rồi lại bị huỷ, rồi báo lỗi mạng. Trên máy của người chơi mà tài liệu này lấy làm chuẩn, tính năng chính **không bao giờ chạy**.

**Cách làm đúng — hai tham số, hai cơ chế:**

| Tham số | Giá trị | Cơ chế | Bắt cái gì |
|---|---|---|---|
| **Hết giờ toàn request** | `bundle_download_timeout_sec` = **90 s** (chấp nhận 60 – 120) | `AssetBundleRequestOptions.Timeout` | Lượt tải chậm bất thường. Cách tính trần: bundle lớn nhất **7,73 MB** ÷ thông lượng 3G tệ nhất **0,35 MB/s** = **22 s**; nhân hệ số an toàn 4 cho sóng chập chờn ⇒ **88 s** ⇒ chốt **90**. Đặt `0` (không hết giờ) cũng hợp lệ **nếu và chỉ nếu** đồng hồ theo dõi tiến độ dưới đây đã chạy |
| **Hết giờ kết nối** | `bundle_connect_timeout_sec` = **8 s** | **Tự làm** — theo dõi tiến độ `DownloadHandler`, huỷ khi **không có byte mới nào trong 8 giây** | Kết nối treo, DNS hỏng, CDN nhận request rồi im. Đây mới là thứ mà "8 giây" vốn muốn nói |

```csharp
// Đồng hồ kết nối: huỷ khi KHÔNG CÓ BYTE NÀO MỚI trong bundle_connect_timeout_sec.
// KHÔNG huỷ theo tổng thời gian — tải lâu mà vẫn chạy là tải tốt.
async Task<bool> WatchStall(AsyncOperationHandle handle, float connectTimeoutSec)
{
    ulong  lastBytes = 0;
    float  lastProgressAt = Time.realtimeSinceStartup;

    while (!handle.IsDone)
    {
        var status = handle.GetDownloadStatus();
        if (status.DownloadedBytes > lastBytes)          // có byte mới => còn sống
        {
            lastBytes      = status.DownloadedBytes;
            lastProgressAt = Time.realtimeSinceStartup;
        }
        else if (Time.realtimeSinceStartup - lastProgressAt > connectTimeoutSec)
        {
            Addressables.Release(handle);                // đứng quá lâu => huỷ, tính là 1 lần hỏng
            return false;
        }
        await Task.Yield();
    }
    return handle.Status == AsyncOperationStatus.Succeeded;
}
```

**Ba bất biến của mục này, để lỗi cũ không quay lại:**

1. Không con số giây nào của chính sách thử lại được **viết cứng** trong mã hay trong tài liệu — tất cả đọc từ `remote_config_keys`.
2. `bundle_download_timeout_sec` **không bao giờ** nhỏ hơn `T2 / 0,35 × 2 = 44 s`. CI kiểm giá trị này khi validate LiveOps.
3. "Hết giờ kết nối" **không bao giờ** được cài bằng `UnityWebRequest.timeout`. Nếu ai đó thấy `Timeout = 8` trong `AssetBundleRequestOptions`, đó là lỗi hồi quy — chặn ở review.

## 7.3. Bất biến an toàn

Bốn quy tắc này là hệ quả trực tiếp của nguyên tắc **A3** và của `fallback.never_block_gameplay: true` trong `liveops_chapter_01.json`:

1. **Nội dung tuỳ chọn hỏng thì im lặng lùi về bản gốc.** Giao diện sự kiện, tiếng môi trường, hoạt ảnh trang trí — hỏng thì bỏ qua, không hỏi người chơi.
2. **Nội dung bắt buộc hỏng thì giải thích và cho thử lại.** Không bao giờ hiện mã lỗi kỹ thuật, không bao giờ hiện màn hình trắng.
3. **Không bao giờ mất tiến trình chơi vì lỗi tải.** Tiến trình lưu cục bộ, độc lập hoàn toàn với trạng thái bundle.
4. **Không bao giờ mời mua hàng trên màn hình lỗi.** Nguyên tắc N3 của `04_LIVEOPS_MONETIZATION.md` áp dụng cả ở đây: lúc người chơi đang bực là lúc cấm bán hàng.

## 7.4. Telemetry cần bắn

| Sự kiện | Tham số | Dùng để |
|---|---|---|
| `bundle_download_start` | `bundle_label`, `size_mb`, `network_type` | Mẫu số của tỉ lệ thành công |
| `bundle_download_success` | `bundle_label`, `duration_ms`, `network_type` | Phân vị thời gian tải theo vùng |
| `bundle_download_fail` | `bundle_label`, `attempt`, `error_code`, `network_type` | **Cảnh báo tự động khi vượt 2% trong 15 phút** |
| `catalog_update_applied` | `from_version`, `to_version`, `duration_ms` | Theo dõi độ phủ lúc triển khai dần |
| `event_theme_apply` | `event_id`, `result`, `fallback_used` | Đã có trong `liveops_chapter_01.json` |

---

# 8. DANH SÁCH KIỂM TRA TRƯỚC KHI PHÁT HÀNH

## 8.1. Cổng build

- [ ] `python3 tools/validate_level.py --strict` trả về mã thoát **0**
- [ ] **Download size** (không phải universal APK) đo bằng `bundletool get-size total --dimensions=ABI,SCREEN_DENSITY,LANGUAGE`, dòng `arm64-v8a` + `vi`: ≤ **30 MB** chặn, ≤ **28 MB** cảnh báo, **mục tiêu 27 MB**
- [ ] Đã đối chiếu số đo thật với **Kịch bản A/B/C** ở §1.3 và ghi rõ bản build này là kịch bản nào
- [ ] `libunity.so`, `libil2cpp.so`, `global-metadata.dat`, `classes.dex` đo bằng **Build Report Inspector**, so với dải ở §1.2; dòng nào ra ngoài dải thì điều tra trước khi chốt
- [ ] Nhóm `local_boot` ≤ **4 MB** (Addressables Analyze)
- [ ] Không asset nào bị trùng giữa hai bundle (*Check Duplicate Bundle Dependencies*)
- [ ] `addressables_content_state.bin` đã lưu vào kho artifact của bản phát hành
- [ ] Đã chạy **Check for Content Update Restrictions**, kết quả sạch
- [ ] **Hệ số LZMA thực đo** trên bundle khu vực đã cập nhật vào §1.6.1 nếu lệch quá 3 điểm phần trăm so với 0,92

## 8.2. Cổng nội dung

- [ ] Mọi `background_asset_url` phân giải được **qua `InternalIdTransformFunc`** (§5.2.1), không phải bằng cách gọi thẳng chuỗi URL trong dữ liệu
- [ ] Mỗi khu vực có **đủ bốn lớp parallax**: hai texture full-frame, một `_l2_fore` ≤ 1920×600, và lớp `_l3_fx` dựng từ texture dùng chung
- [ ] Mọi `audio_asset` và `sprite_animation` có mặt trong đúng bundle khu vực của nó
- [ ] **Mỗi cú doạ có đủ ba file trong CÙNG bundle khu vực**: sheet gốc + `_soft` + `_static`. Không file nào trong ba file đó nằm ở nhóm khác, nhãn khác, hay bundle tải sau
- [ ] Mỗi khu vực có `ambience_address` trỏ tới `remote_ambience_<area_id>` tồn tại trong catalog
- [ ] Mọi `icon_item_*` có trong `remote_item_icons`
- [ ] `override_bg` của mọi sự kiện nằm trong `addressables.bundles` của chính sự kiện đó
- [ ] Không texture nào còn ở định dạng không nén hoặc RGBA32
- [ ] Đo lại ba con số của §1.6.5 trên catalog thật: lần chờ đầu ≤ **8,5 MB**, bundle khu vực lớn nhất ≤ **8,0 MB**, tổng ≤ **52 MB**

## 8.3. Cổng vận hành

- [ ] Thử trên máy thật: **không mạng**, **mạng chập chờn**, **chỉ 3G**
- [ ] **Thử bóp băng thông xuống 0,35 MB/s** (cận dưới 3G Việt Nam) và xác nhận lần chờ đầu tiên hoàn tất, **không** bị chính client huỷ giữa chừng — đây là bài kiểm trực tiếp cho §7.2.2
- [ ] Thử **kết nối treo** (CDN nhận request rồi im): đồng hồ theo dõi tiến độ `DownloadHandler` huỷ sau `bundle_connect_timeout_sec`, **không** phải sau `bundle_download_timeout_sec`
- [ ] Thử ngắt mạng giữa lúc tải khu vực → phục hồi sạch
- [ ] Thử **tắt Wi-Fi, chỉ để 4G** với `prefetch_wifi_only_default = true`: nội dung **bắt buộc** vẫn tải, tải trước thì hoãn — game vào được màn chơi
- [ ] Thử **ambience hỏng**: khu vực im lặng, người chơi chơi tiếp bình thường, không toast lỗi kỹ thuật
- [ ] Thử tải bundle sự kiện hỏng → lùi về nền gốc, **không** chặn người chơi
- [ ] Đã thử quay lui: đổi `addressables_catalog_url` về bản trước, xác nhận có hiệu lực trong 60 giây **và xác nhận ảnh nền cũng lùi theo** (§5.2.1)
- [ ] Đã thử cả **năm** `kill_switch_*` **từ remote config**, từng cái một — bao gồm `kill_switch_telemetry` (§5.3.1)
- [ ] Cảnh báo `bundle_download_fail > 2%` đã cấu hình và đã bắn thử

---

# 9. BẢNG TRA NHANH

| Câu hỏi | Trả lời | Mục |
|---|---|---|
| Cột "Ngân sách" đo cái gì? | **Play Console download size** của bản ARM64 + `vi`, đo bằng `bundletool get-size total` | §1.1 |
| APK được phép bao nhiêu? | Trần cứng 30 MB, cảnh báo 28, **mục tiêu thiết kế 27** | §1.1, §1.3 |
| Trần 30 MB có đạt được không? | **Không**, nếu giữ nguyên bộ SDK (Kịch bản A = 38,3 MB). Chỉ đạt ở **Kịch bản C** = 27,6 MB: bỏ SDK quảng cáo, bỏ Firebase, bỏ TMP, bỏ Newtonsoft, đẩy `local_boot` + font sang PAD `fast-follow` | §1.2, §1.3 |
| Bỏ ARMv7 tiết kiệm bao nhiêu? | **0 MB trên download size.** AAB đã tách theo ABI. Đó là quyết định cắt thị trường, không phải đòn bẩy ngân sách | §1.5 |
| Một nền tốn bao nhiêu? | **2,2461 MB cho một BỘ NỀN 4 lớp.** `0,8789 MB` là con số của **một lớp** | §1.6.4, §3.1 |
| Nền dùng định dạng gì? | ASTC 6×6, không mipmap, cả Android lẫn iOS | §3.1, §3.2 |
| Sheet cú doạ đóng thế nào? | Khung ≤ 768 px cạnh dài; **6 khung** gốc (ASTC 8×8), **3 khung** `_soft` (8×8), **1 khung** `_static` (6×6) | §1.6.4, §3.1 |
| `_soft` / `_static` nằm ở đâu? | **Cùng bundle với khu vực**, không nhãn riêng, không tải sau. Tuỳ chọn an toàn không được đặt sau bất kỳ cổng nào | §2.1 |
| Cú doạ dùng định dạng âm thanh gì? | ADPCM + Decompress On Load — bắt buộc, vì độ trễ | §3.3 |
| Ambience phát thế nào? | **Tải trọn bundle về cache → Streaming từ đĩa.** Không có chuyện phát thẳng từ mạng | §1.6.6, §3.3 |
| Người chơi chờ bao lâu lần đầu? | **8,22 MB → 14–24 giây trên 3G** (đã gồm ambience khu vực 1) | §1.6.5, §4.1 |
| Tổng nội dung remote bao nhiêu? | **≈ 47,6 MB**, dưới trần T3 = 52 MB | §1.6.4, §1.6.5 |
| `background_asset_url` phân giải thế nào? | Là **khoá logic**. Engine rút `basename` làm Addressables key rồi ghép `{platform}` + `{catalog_version}` bằng `InternalIdTransformFunc` | §5.2.1 |
| Sửa `bounds` có cần build lại không? | Không. Sửa JSON → đẩy catalog | §6.1 |
| Thêm `puzzle type` mới có cần build lại không? | **Có.** Engine chưa có mã cơ chế | §6.1 |
| Quay lui thế nào? | Trỏ `addressables_catalog_url` về thư mục phiên bản trước | §6.4 |
| Mạng hỏng thì sao? | Thử lại theo `bundle_retry_count` / `bundle_retry_backoff_sec` rồi chuyển thủ công. Nội dung tuỳ chọn im lặng lùi về bản gốc | §7.1, §7.2 |
| Hết giờ tải đặt bao nhiêu? | **Hai đồng hồ:** `bundle_download_timeout_sec = 90` (toàn request) và `bundle_connect_timeout_sec = 8` (tự làm bằng theo dõi tiến độ). Không bao giờ đặt `Timeout = 8` | §7.2.2 |
| Bao nhiêu khoá remote config? | **36** = 32 hiện có + 4 bổ sung (`kill_switch_telemetry`, `bundle_retry_backoff_sec`, `bundle_connect_timeout_sec`, `prefetch_wifi_only_default`) | §5.3.1 |
| File nào tuyệt đối không được mất? | `addressables_content_state.bin` của bản đang phát hành | §6.3 |
