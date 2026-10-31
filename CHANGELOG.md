# Changelog

Các thay đổi đáng chú ý của AIMS-mini được ghi tại đây.
Định dạng dựa trên [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
phiên bản theo [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-10-31

### Fixed

- Tìm kiếm tựa đề không phân biệt hoa thường; `lion` tìm được `The Lion King`
  ([#20](https://github.com/phuonganh317/it3180202417227aims/issues/20)).

## [1.0.0] - 2026-10-31

Phiên bản phát hành Lab 04, tổng hợp chức năng và sửa lỗi từ Lab 01–03.

### Added

- Mô hình DVD và giỏ hàng: thêm/xóa DVD, tính tổng tiền và chương trình mẫu.
- In danh sách DVD, tổng tiền và thông báo khi giỏ rỗng.
- Tìm DVD theo tựa đề bằng `search_by_title`, phân biệt hoa thường.
- Tính tổng sau giảm giá phần trăm bằng `Cart.discounted_total`.
- Bộ unittest kiểm tra giới hạn giỏ, giảm giá và thông báo thêm DVD.
- PR template, tài liệu Use Case, câu trả lời và báo cáo thực hành Lab 01–03.
- Khai báo `aims.__version__` và banner `AIMS-mini v1.0.0` trong demo.

### Changed

- Tổ chức mã nguồn thành package `aims`, cập nhật import trong chương trình mẫu.
- Thông báo thêm DVD bằng tiếng Việt, có tên đĩa.

### Fixed

- Chặn DVD thứ 21 khi giỏ đã đủ 20 đĩa ([#7]).
- Tính giảm giá theo phần trăm, từ chối tỷ lệ ngoài 0–100 và NaN;
  giữ nguyên giá gốc, trả tổng 0 cho giỏ rỗng.

[Unreleased]: https://github.com/phuonganh317/it3180202417227aims/compare/v1.0.1...master
[1.0.1]: https://github.com/phuonganh317/it3180202417227aims/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/phuonganh317/it3180202417227aims/releases/tag/v1.0.0
[#7]: https://github.com/phuonganh317/it3180202417227aims/issues/7
