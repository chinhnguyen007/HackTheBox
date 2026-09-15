# LINH AN THÔN — CHƯƠNG 1
## TÍCH HỢP UNITY ADDRESSABLES — NGÂN SÁCH APK, ĐÓNG GÓI, PHÂN PHỐI NỘI DUNG

| Trường | Giá trị |
|---|---|
| Dự án | **Linh An Thôn — Chapter 1** |
| Tài liệu | `docs/05_TICH_HOP_UNITY_ADDRESSABLES.md` — bản chốt cho tổ engine và tổ vận hành |
| Nền tảng | Android (AAB, minSdk 24) · iOS (minimum iOS 13) |
| Ràng buộc cứng | **APK engine ≤ 30 MB** · toàn bộ asset nội dung tải qua Addressables remote bundle |
| Độ phân giải thiết kế | 1920 × 1080, gốc (0,0) góc trên-trái |
| Tài liệu liên quan | `03_DATA_SPEC.md` (hợp đồng dữ liệu) · `04_LIVEOPS_MONETIZATION.md` (remote config, sự kiện mùa) |
| Ngôn ngữ | Tài liệu: tiếng Việt có dấu. Mọi tên nhóm / nhãn / khoá: snake_case không dấu |
| Ngày cập nhật | 2026-09-15 |

> **Một câu tóm tắt toàn bộ tài liệu:** APK chỉ chứa *động cơ và cái vỏ*; mọi thứ người chơi nhìn thấy và nghe thấy đều nằm trên CDN, tải theo từng khu vực, và thay được mà không cần đụng tới cửa hàng ứng dụng.

---

# 0. BỐN NGUYÊN TẮC NỀN

| # | Nguyên tắc | Hệ quả kỹ thuật kiểm được |
|---|---|---|
| **A1** | **APK chỉ chứa thứ cần để hiện màn hình tải.** | Nhóm Addressables `local` giới hạn cứng **4 MB**. Mọi nền, mọi cú doạ, mọi âm thanh đều `remote`. |
| **A2** | **Không nội dung nào bắt người chơi chờ thứ họ chưa cần.** | Tải theo **từng khu vực**. Vào `area_san_gach` chỉ tải bundle của sân gạch (~3,5 MB), không tải cả chương. |
| **A3** | **Mạng hỏng không bao giờ được chặn người chơi.** | Mọi đường tải đều có đường lui. Giao diện sự kiện hỏng → nền gốc. Bundle khu vực hỏng → thử lại + màn hình giải thích, **không** màn hình chết. |
| **A4** | **Sửa nội dung không được đụng tới bản build.** | Dữ liệu (`data/**`) và asset đi cùng một catalog có phiên bản. Đẩy catalog mới là xong — không qua duyệt store. |

---

# 1. NGÂN SÁCH KÍCH THƯỚC APK ENGINE ≤ 30 MB

## 1.1. Bảng ngân sách theo từng thành phần

Số liệu dưới đây là **ngân sách chốt**, đo trên bản Release ARM64, IL2CPP, managed stripping `High`.

| # | Thành phần | Chi tiết | Ngân sách | Ai chịu trách nhiệm |
|---|---|---|---|---|
| 1 | `libunity.so` | Nhân engine đã strip module | **11,0 MB** | Engine |
| 2 | `libil2cpp.so` | Mã game đã dịch sang C++ | **2,5 MB** | Engine |
| 3 | `global-metadata.dat` | Siêu dữ liệu IL2CPP | **1,8 MB** | Engine |
| 4 | Nhóm Addressables `local_boot` | Logo, màn hình tải, UI tối thiểu, catalog gốc | **4,0 MB** | Đồ hoạ + Engine |
| 5 | Font tiếng Việt đã subset | Serif có dấu đầy đủ + chữ số, bỏ CJK | **1,2 MB** | Đồ hoạ |
| 6 | Chuỗi localization `vi-VN` | Toàn bộ `txt_*` của Chương 1 | **0,3 MB** | Tường thuật |
| 7 | Unity IAP + Google Play Billing | Thư viện native | **2,2 MB** | Vận hành |
| 8 | SDK quảng cáo thưởng | Chỉ module rewarded, **không** banner/interstitial | **2,5 MB** | Vận hành |
| 9 | Firebase Analytics + Remote Config | Đã loại Crashlytics NDK symbols | **1,8 MB** | Vận hành |
| 10 | `unity default resources` + shader | Shader 2D đã lọc variant | **1,5 MB** | Engine |
| 11 | `AndroidManifest`, `res/`, icon adaptive | Vỏ ứng dụng | **0,7 MB** | Engine |
| 12 | **Dự phòng** | Đệm cho SDK cập nhật ngoài ý muốn | **0,5 MB** | — |
| | **TỔNG** | | **30,0 MB** | |

> **Quy tắc ngân sách:** không hạng mục nào được vượt quá phần của mình mà không lấy bù từ hạng mục khác **trong cùng bản build**. CI đo kích thước APK sau mỗi lần merge vào `main`; vượt 30 MB là **chặn**, vượt 28 MB là **cảnh báo**.

## 1.2. Vì sao dòng số 4 là dòng nguy hiểm nhất

Mười một dòng còn lại gần như cố định — chúng là chi phí của engine và SDK. Dòng **`local_boot` 4 MB** là dòng duy nhất tổ nội dung chạm vào được, nên cũng là dòng duy nhất phình ra. Chỉ bốn thứ được phép nằm trong đó:

| Được phép | Không được phép |
|---|---|
| Logo studio + logo game (một atlas 1024×1024, ASTC 6×6) | Bất kỳ `bg_*.bundle` nào |
| Khung màn hình tải + hoạt ảnh chờ (sprite sheet ≤ 512×512) | Bất kỳ `anim_*` cú doạ nào |
| Font Việt đã subset | Bất kỳ `sfx_*` hay `amb_*` nào |
| Atlas UI tối thiểu: nút, khung thoại, con trỏ, khung túi đồ | Icon vật phẩm (`icon_item_*` — nằm ở remote, xem §3.2) |

`[[ Cám dỗ thường gặp: "nhét tạm icon túi đồ vào local cho nhanh". Mười vật phẩm × 256×256 ASTC 6×6 ≈ 0,3 MB — nghe thì nhỏ, nhưng nó phá nguyên tắc A4: sửa một icon là phải qua duyệt store. ]]`

## 1.3. Cấu hình build để đạt ngân sách

| Thiết lập | Giá trị | Tiết kiệm ước tính |
|---|---|---|
| Scripting Backend | **IL2CPP** | — (bắt buộc cho ARM64) |
| Target Architectures | **ARM64 duy nhất**, phát hành qua **AAB** để Play tách theo ABI | ~8 MB so với ARM64 + ARMv7 |
| Managed Stripping Level | **High** | 1,5 – 2,5 MB |
| C++ Compiler Configuration | **Master** | 0,5 – 1 MB |
| Strip Engine Code | **Bật** | 2 – 4 MB |
| Module đã gỡ | Physics, Physics2D (chỉ dùng raycast UI), Terrain, VR/XR, Video, Cloth, Vehicles, Particle System *(nếu hiệu ứng khói dùng shader)* | 3 – 5 MB |
| Splash Screen | **Tắt** (yêu cầu bản quyền Plus/Pro) | 0,3 MB |
| Accelerometer Frequency | Disabled | — |
| Shader variant stripping | Chỉ giữ 2D Sprite-Lit/Unlit, bỏ Fog/Instancing/Lightmap variant | 1 – 2 MB |

**Mẹo rất dễ bỏ sót:** `link.xml` giữ lại các kiểu bị strip nhầm khi dùng reflection. Addressables và Newtonsoft (nếu dùng) hay bị strip mất provider. Đo bằng **Build Report Inspector**, không đoán.

## 1.4. Ngân sách phía remote (không tính vào 30 MB)

| Nhóm | Nội dung | Kích thước nén | Khi nào tải |
|---|---|---|---|
| `remote_area_san_gach` | Nền + overlay + âm thanh khu vực 1 | ~3,4 MB | Ngay sau màn hình tải |
| `remote_area_hien_nha` | Khu vực 2 | ~3,6 MB | Khi vào khu vực 1 (tải trước) |
| `remote_area_gian_tho` | Khu vực 3 | ~4,1 MB | Khi vào khu vực 2 |
| `remote_area_bep_gieng` | Khu vực 4 | ~3,8 MB | Khi vào khu vực 3 |
| `remote_area_gac_xep` | Khu vực 5 | ~3,9 MB | Khi vào khu vực 4 |
| `remote_shared_ui` | Icon vật phẩm, khung phóng to câu đố | ~1,2 MB | Ngay sau màn hình tải |
| `remote_audio_ambience` | Nhạc nền, tiếng môi trường (streaming) | ~4,5 MB | Phát trực tiếp, không tải trọn |
| `remote_event_*` | Giao diện sự kiện theo mùa | 5 – 7 MB / sự kiện | Chỉ khi sự kiện đang chạy |
| | **Tổng nội dung Chương 1** | **~24,5 MB** | |

**Tổng dung lượng người chơi thực sự tải để chơi hết Chương 1: ~30 MB APK + ~24,5 MB nội dung.** Nhưng họ không bao giờ chờ 24,5 MB một lần — lần chờ dài nhất là **4,6 MB** (khu vực 1 + UI dùng chung), khoảng 6–10 giây trên 3G Việt Nam.

---

# 2. CẤU TRÚC NHÓM ADDRESSABLES

## 2.1. Bảng nhóm

| Tên nhóm | Loại | Build/Load Path | Nhãn (label) | Nén | Nội dung |
|---|---|---|---|---|---|
| `local_boot` | **Local** | `LocalBuildPath` / `LocalLoadPath` | `boot` | **LZ4** | Logo, màn hình tải, font, atlas UI tối thiểu |
| `remote_catalog_data` | **Remote** | `RemoteBuildPath` / `{CDN}/{platform}/{catalog}` | `data` | **LZ4** | `chapter_01.json`, `areas/*.json`, `liveops_chapter_01.json` (TextAsset) |
| `remote_shared_ui` | **Remote** | như trên | `shared` | LZ4 | `icon_item_*`, khung phóng to câu đố, khung túi đồ |
| `remote_area_<area_id>` | **Remote** | như trên | `area`, `<area_id>` | **LZMA** | Nền, overlay hotspot, `anim_*`, `sfx_*` của đúng khu vực đó |
| `remote_audio_ambience` | **Remote** | như trên | `ambience` | LZMA | Nhạc nền và tiếng môi trường dài (Streaming) |
| `remote_event_<event_id>` | **Remote** | như trên | `event`, `<event_id>` | LZMA | `override_bg`, khung giao diện, tiếng môi trường sự kiện |

**Năm nhóm khu vực là năm nhóm riêng biệt, không gộp.** Lý do không phải thẩm mỹ:

1. **Tải lại rẻ.** Unity **không** nối lại được một lượt tải bundle bị đứt giữa chừng — hỏng là tải lại từ đầu. Bundle 3,5 MB tải lại mất 5 giây; bundle 24 MB tải lại mất một phút và người chơi sẽ thoát game.
2. **Cập nhật hẹp.** Sửa một cú doạ ở gác xép chỉ đẩy lại `remote_area_gac_xep`, không bắt người chơi tải lại cả chương.
3. **Bộ nhớ.** Giải phóng bundle khu vực cũ khi rời khu vực, đỉnh RAM giữ dưới 180 MB trên máy 2 GB.

## 2.2. Vì sao dữ liệu JSON có nhóm riêng

`remote_catalog_data` tách khỏi asset vì **dữ liệu thay đổi thường xuyên hơn ảnh gấp nhiều lần**. Cân lại một `max_fails`, đổi một `text_key`, sửa một `bounds` — đó là bundle chỉ vài chục KB. Nếu JSON nằm chung với nền, mỗi lần cân bằng câu đố là người chơi phải tải lại 3,5 MB ảnh không đổi một pixel.

Nhóm này dùng **LZ4** thay vì LZMA vì nó nằm trên đường găng của lúc khởi động: LZ4 giải nén theo khối, đọc được ngay, trong khi LZMA phải giải nén trọn gói trước khi dùng.

## 2.3. Chọn chế độ nén

| Nhóm | Nén | Lý do |
|---|---|---|
| `local_boot` | **LZ4** | Nằm trong APK, đã bị AAB nén một lần nữa. LZ4 cho phép đọc ngẫu nhiên, mở màn hình tải tức thì. |
| `remote_catalog_data` | **LZ4** | Trên đường găng khởi động; kích thước đã nhỏ nên LZMA không lợi bao nhiêu. |
| `remote_area_*`, `remote_event_*` | **LZMA** | Nhỏ hơn LZ4 khoảng 15–25% khi truyền. Addressables tự **nén lại thành LZ4 trong cache** ở lần tải đầu, nên lần mở thứ hai vẫn nhanh. |

`[[ Đừng dùng "Uncompressed" cho remote với lý do "texture đã nén ASTC rồi". Header bundle, dữ liệu sprite, AudioClip metadata và chuỗi văn bản vẫn nén tốt — đo thực tế trên area_gian_tho cho ra 4,1 MB (LZMA) so với 5,3 MB (không nén). ]]`

---

# 3. ĐỊNH DẠNG NÉN ASSET

## 3.1. Texture — Android

| Loại asset | Định dạng | Kích thước gốc | Bits/pixel | Ghi chú |
|---|---|---|---|---|
| Nền khu vực (`bg_*`) | **ASTC 6×6** | 1920 × 1080 | 3,56 | **Tắt mipmap** — 2D orthographic không bao giờ thu nhỏ nền |
| Overlay hotspot (có alpha) | **ASTC 6×6** | theo `bounds` | 3,56 | Cắt sát biên, không để vùng trong suốt thừa |
| Hoạt ảnh cú doạ (`anim_*`) | **ASTC 8×8** | sprite sheet ≤ 2048² | 2,00 | Chạy 0,3–0,8 giây, mắt không kịp bắt lỗi nén |
| Icon vật phẩm (`icon_item_*`) | **ASTC 6×6** | 256 × 256, gói vào SpriteAtlas | 3,56 | Một atlas 1024×1024 chứa đủ 10 vật phẩm |
| UI trong `local_boot` | **ASTC 6×6** | ≤ 1024² | 3,56 | — |

**Một nền 1920×1080 ở ASTC 6×6 = 1920 × 1080 × 3,56 / 8 ≈ 0,88 MB.** Đó là con số neo cho mọi tính toán ngân sách ở §1.4.

**Vì sao ASTC 6×6 chứ không phải 4×4 hay 8×8:**

| Block | Bits/pixel | Một nền 1920×1080 | Đánh giá cho folk horror vẽ tay |
|---|---|---|---|
| 4×4 | 8,00 | 1,98 MB | Chất lượng thừa. Phong cách vẽ tay nhiều vệt mực và hạt nhiễu, mắt không phân biệt được với 6×6 |
| **6×6** | **3,56** | **0,88 MB** | **Chốt.** Giữ được chuyển sắc tối trong bóng đổ, không thấy khối |
| 8×8 | 2,00 | 0,49 MB | Xuất hiện khối bẩn ở vùng chuyển sắc tối — chính là vùng quan trọng nhất của game này |

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
| Tiếng môi trường lặp (`amb_*`, 30–90 giây) | **Vorbis** q = 0,5 | **Streaming** | 44 100 Hz | Stereo | Không chiếm RAM; chất lượng stereo là phần lớn cảm giác không gian |
| Nhạc chủ đề, cảnh kết | **Vorbis** q = 0,6 | Streaming | 44 100 Hz | Stereo | — |
| Lời thoại (nếu Chương 2 có) | Vorbis q = 0,4 | Compressed In Memory | 22 050 Hz | Mono | — |

**Ba quy tắc âm thanh không thương lượng:**

1. **Force To Mono cho mọi thứ dưới 2 giây.** Cú doạ phát ở giữa không gian âm thanh; stereo chỉ nhân đôi dung lượng vô ích.
2. **Không bao giờ dùng Streaming cho cú doạ.** Streaming đọc từ đĩa lúc phát — đúng thứ gây trễ mà §3.3 đang tránh.
3. **Nạp trước `AudioClip` cú doạ khi vào khu vực, không phải khi cú doạ bắn.** Nằm trong bundle khu vực, nên bước tải trước ở §4 đã lo. `04_horror.md` quy định envelope; engine chỉ cần bảo đảm clip đã ở trong RAM trước đó.

`[[ Định dạng file trong dữ liệu ghi là ".ogg" (xem jumpscares[].audio_asset). Đó là tên asset nguồn; thiết lập import của Unity mới quyết định định dạng lúc chạy. Một file .ogg nguồn hoàn toàn có thể được import thành ADPCM — và với sfx_scare_* thì bắt buộc phải thế. ]]`

---

# 4. CHIẾN LƯỢC TẢI TRƯỚC VÀ TẢI LAZY

## 4.1. Dòng thời gian khởi động

```
t=0,0s   Ứng dụng mở, màn hình tải hiện ngay (từ local_boot, không cần mạng)
t=0,1s   Addressables.InitializeAsync()
t=0,3s   Kiểm & cập nhật catalog  (CheckForCatalogUpdates → UpdateCatalogs)
t=0,6s   Tải nhóm nhãn "data"     (~80 KB)  → phân tích chapter_01.json
t=0,8s   Tải song song:
            nhãn "shared"              (~1,2 MB)
            nhãn "area_san_gach"       (~3,4 MB)
t=6-10s  Xong → vào area_san_gach
         ↓ NGAY KHI VÀO, ngầm tải trước area_hien_nha ở mức ưu tiên thấp
```

**Người chơi chỉ chờ đúng một lần.** Từ khu vực 2 trở đi, bundle đã nằm sẵn trong cache trước khi họ chạm vào cánh cửa — vì thời gian một người chơi ở lại một khu vực (90–240 giây, theo `target_solve_sec` trong cấu hình LiveOps) dài gấp nhiều lần thời gian tải 3,6 MB.

## 4.2. Bảng chính sách tải theo từng nhóm

| Nhóm | Chính sách | Kích hoạt bởi | Ưu tiên |
|---|---|---|---|
| `local_boot` | Trong APK | — | — |
| `remote_catalog_data` | **Bắt buộc, chặn** | Khởi động | Cao nhất |
| `remote_shared_ui` | **Bắt buộc, chặn** | Khởi động | Cao |
| `remote_area_<khu vực đầu>` | **Bắt buộc, chặn** | Khởi động | Cao |
| `remote_area_<khu vực kế tiếp>` | **Tải trước, ngầm** | Vào khu vực hiện tại | Thấp |
| `remote_area_<còn lại>` | **Lazy** | Ngay trước khi `CHANGE_AREA` chạy | Theo yêu cầu |
| `remote_audio_ambience` | **Streaming** | Khi phát | Thấp |
| `remote_event_*` | Theo `download_policy` của sự kiện | Xem `04_LIVEOPS` §4 | Thấp nhất |

**Quy tắc "khu vực kế tiếp" đọc từ dữ liệu, không hard-code.** Khu vực kế tiếp lấy từ `area_order` trong `chapter_01.json`; đồng thời tải trước cả những khu vực mà hotspot `CHANGE_AREA` của khu vực hiện tại trỏ tới (người chơi quay lui được). Với `area_gian_tho` — nơi có tới bốn cửa — điều đó nghĩa là quay lui về `area_hien_nha` không bao giờ phải chờ.

## 4.3. Giải phóng bộ nhớ

| Sự kiện | Hành động |
|---|---|
| Rời một khu vực | `Addressables.Release` handle của khu vực đó **sau 30 giây** (đề phòng quay lui ngay) |
| Nhận cảnh báo bộ nhớ thấp | Giải phóng ngay mọi khu vực trừ khu vực hiện tại, rồi `Resources.UnloadUnusedAssets()` |
| Kết thúc chương | Giải phóng tất cả trừ `shared` và `boot` |

**Không bao giờ gọi `Addressables.ClearDependencyCacheAsync` như một cách "dọn dẹp".** Nó xoá file đã tải trên đĩa, buộc tải lại từ CDN. Chỉ dùng đúng một trường hợp: khi phát hiện CRC sai (§7.4).

## 4.4. Hạn mức tải trên mạng di động

Theo `liveops_chapter_01.json`, sự kiện theo mùa đặt `wifi_only_default: true`. Áp dụng cho cả nội dung thường:

| Tình huống | Xử lý |
|---|---|
| Wi-Fi | Tải trước tự do |
| Di động, gói ≤ 5 MB | Tải im lặng, không hỏi |
| Di động, gói > 5 MB | Hỏi một lần bằng `GetDownloadSizeAsync`, nhớ lựa chọn |
| Đặt "chỉ Wi-Fi", đang dùng di động | Hoãn tải trước; nội dung **bắt buộc** vẫn tải kèm giải thích rõ ràng |

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

## 5.3. Ba nguồn cấu hình lúc chạy và thứ tự ưu tiên

| Nguồn | Chứa gì | Đổi được không cần build lại |
|---|---|---|
| **Hằng số trong APK** | URL CDN dự phòng, catalog gốc | Không |
| **Firebase Remote Config** | `addressables_catalog_url`, `liveops_config_version`, 32 khoá ở `remote_config_keys` | **Có**, trong vài phút |
| **Bundle dữ liệu** (`remote_catalog_data`) | Toàn bộ `data/**` — bố cục màn chơi, lời giải câu đố, cú doạ | **Có**, sau khi đẩy catalog |

Ưu tiên khi đọc: **Remote Config → Bundle dữ liệu → Hằng số trong APK**. Remote config hỏng hoặc quá hạn thì client lùi về catalog cuối cùng đã tải thành công; hết cách thì mới dùng hằng số trong APK.

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

Đi kèm là năm `kill_switch_*` trong `liveops_chapter_01.json` — tắt được quảng cáo, IAP, giao diện sự kiện, gợi ý trả phí, telemetry **độc lập với nhau**, mà không cần đụng tới catalog.

---

# 7. XỬ LÝ LỖI MẠNG VÀ TẢI THẤT BẠI

## 7.1. Bảng tình huống lỗi

| Tình huống | Phát hiện bằng | Xử lý | Người chơi thấy gì |
|---|---|---|---|
| Không có mạng lúc khởi động | `InitializeAsync` lỗi hoặc `CheckForCatalogUpdates` hết giờ | Dùng catalog đã cache lần trước | Không thấy gì — game chạy bình thường nếu đã chơi trước đó |
| Không có mạng, **và** chưa từng chơi | Cache trống | Màn hình "cần mạng để tải nội dung lần đầu" + nút thử lại | Thông báo rõ ràng, không phải màn hình lỗi kỹ thuật |
| Catalog tải được, bundle khu vực hỏng | `AsyncOperationHandle.Status == Failed` | Thử lại 3 lần (1 s / 3 s / 8 s + nhiễu ngẫu nhiên), rồi hiện nút thử lại | Vòng xoay chờ → thông báo + nút "Thử lại" |
| Mạng đứt **giữa lúc** tải | Handle lỗi | Như trên. Bundle 3,5 MB nên tải lại rẻ | Như trên |
| Bundle sự kiện theo mùa hỏng | Handle lỗi sau `timeout_sec` | **Lùi về nền gốc** (`USE_BASE_BACKGROUND`), tắt giao diện sự kiện cho phiên này | Chơi bình thường + một toast nhẹ |
| CRC sai / bundle hỏng trong cache | Addressables báo lỗi CRC | `ClearDependencyCacheAsync` cho **đúng khoá đó**, rồi tải lại một lần | Vòng xoay chờ lâu hơn chút |
| Hết dung lượng đĩa | `IOException` lúc ghi cache | Dừng tải trước, giải phóng khu vực không dùng, báo người chơi | Thông báo dọn bớt dung lượng |
| CDN trả 403/404 (sai cấu hình triển khai) | Mã HTTP | Lùi về catalog cuối cùng đã cache, bắn cảnh báo telemetry mức cao | Không thấy gì |

## 7.2. Chính sách thử lại

| Tham số | Giá trị | Lý do |
|---|---|---|
| Số lần thử | **3** | Quá 3 lần thì gần như chắc chắn không phải lỗi thoáng qua |
| Giãn cách | **1 s → 3 s → 8 s**, cộng nhiễu ngẫu nhiên 0–500 ms | Nhiễu tránh cả đám người chơi cùng đập vào CDN sau một sự cố |
| Hết giờ mỗi lần thử | **8 giây** (khớp `fallback.timeout_sec` của LiveOps) | 3G Việt Nam kéo 3,5 MB trong khoảng 6–10 giây; 8 giây là hết giờ *kết nối*, không phải hết giờ *truyền* |
| Sau 3 lần hỏng | Chuyển sang **thao tác thủ công** | Không tự thử lại vô hạn — nó ngốn pin và data của người chơi |

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
- [ ] Kích thước APK/AAB ≤ **30 MB** (CI đo tự động, có ghi lại lịch sử)
- [ ] Nhóm `local_boot` ≤ **4 MB** (Addressables Analyze)
- [ ] Không asset nào bị trùng giữa hai bundle (*Check Duplicate Bundle Dependencies*)
- [ ] `addressables_content_state.bin` đã lưu vào kho artifact của bản phát hành
- [ ] Đã chạy **Check for Content Update Restrictions**, kết quả sạch

## 8.2. Cổng nội dung

- [ ] Mọi `background_asset_url` trong `data/areas/*.json` phân giải được trên CDN
- [ ] Mọi `audio_asset` và `sprite_animation` có mặt trong đúng bundle khu vực của nó
- [ ] Mọi `icon_item_*` có trong `remote_shared_ui`
- [ ] `override_bg` của mọi sự kiện nằm trong `addressables.bundles` của chính sự kiện đó
- [ ] Không texture nào còn ở định dạng không nén hoặc RGBA32

## 8.3. Cổng vận hành

- [ ] Thử trên máy thật: **không mạng**, **mạng chập chờn**, **chỉ 3G**
- [ ] Thử ngắt mạng giữa lúc tải khu vực → phục hồi sạch
- [ ] Thử tải bundle sự kiện hỏng → lùi về nền gốc, **không** chặn người chơi
- [ ] Đã thử quay lui: đổi `addressables_catalog_url` về bản trước, xác nhận có hiệu lực trong 60 giây
- [ ] Đã thử cả năm `kill_switch_*`, từng cái một
- [ ] Cảnh báo `bundle_download_fail > 2%` đã cấu hình và đã bắn thử

---

# 9. BẢNG TRA NHANH

| Câu hỏi | Trả lời | Mục |
|---|---|---|
| APK được phép bao nhiêu? | 30 MB, trong đó nội dung của tổ nghệ thuật chỉ có 4 MB | §1.1 |
| Nền dùng định dạng gì? | ASTC 6×6, không mipmap, cả Android lẫn iOS | §3.1, §3.2 |
| Cú doạ dùng định dạng âm thanh gì? | ADPCM + Decompress On Load — bắt buộc, vì độ trễ | §3.3 |
| Người chơi chờ bao lâu lần đầu? | ~4,6 MB, khoảng 6–10 giây trên 3G | §1.4, §4.1 |
| Sửa `bounds` có cần build lại không? | Không. Sửa JSON → đẩy catalog | §6.1 |
| Thêm `puzzle type` mới có cần build lại không? | **Có.** Engine chưa có mã cơ chế | §6.1 |
| Quay lui thế nào? | Trỏ `addressables_catalog_url` về thư mục phiên bản trước | §6.4 |
| Mạng hỏng thì sao? | Thử lại 3 lần có giãn cách, rồi thao tác thủ công. Nội dung tuỳ chọn thì im lặng lùi về bản gốc | §7.1, §7.2 |
| File nào tuyệt đối không được mất? | `addressables_content_state.bin` của bản đang phát hành | §6.3 |
