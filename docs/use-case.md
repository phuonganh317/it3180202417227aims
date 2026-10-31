# Use Case — AIMS-mini

## Phạm vi và tác nhân

Hệ thống AIMS-mini quản lý giỏ DVD trong bộ nhớ. Tác nhân là người dùng
chương trình mẫu hoặc mã gọi API Python. `main.py` hiện minh họa thêm DVD
và in giỏ; các thao tác xóa và tìm kiếm được cung cấp qua API, chưa có menu
tương tác hay chức năng thanh toán/lưu dữ liệu.

## Các ca sử dụng

| Mã | Ca sử dụng | Đầu vào | Kết quả |
| --- | --- | --- | --- |
| UC01 | Thêm DVD vào giỏ | Một `DigitalVideoDisc` | `Cart.add_dvd(dvd)` thêm đĩa và thông báo kết quả. |
| UC02 | Xóa DVD khỏi giỏ | Đối tượng DVD cần xóa | `Cart.remove_dvd(dvd)` xóa đĩa nếu có; thông báo nếu không có. |
| UC03 | Xem giỏ hàng | Giỏ hàng hiện tại | `Cart.print_cart()` in danh sách có đánh số và tổng tiền. |
| UC04 | Tìm DVD theo tựa đề | Danh sách DVD và từ khóa | `search_by_title(items, keyword)` trả về các DVD có tựa đề chứa từ khóa. |

Người dùng có thể thực hiện cả bốn ca sử dụng. UC03 sử dụng phép tính
`Cart.total_cost()` để tổng hợp giá các đĩa khi giỏ có phần tử.

## Luồng chính: xem giỏ hàng (UC03)

1. Chương trình tạo một `Cart` và thêm các đối tượng `DigitalVideoDisc`.
2. Người dùng yêu cầu xem giỏ bằng cách gọi `cart.print_cart()`.
3. Hệ thống in từng DVD theo thứ tự trong giỏ, đánh số từ 1.
4. Hệ thống in tổng tiền với hai chữ số thập phân.

Với dữ liệu mẫu trong `main.py`, danh sách gồm The Lion King, Star Wars,
Aladdin và dòng tổng là `Total cost: 63.89 $`.

**Luồng thay thế:** khi giỏ rỗng, hệ thống chỉ in `The cart is empty` rồi
kết thúc phương thức. Thao tác xem không làm thay đổi giỏ hàng.

## Luồng chính: tìm kiếm tựa đề (UC04)

1. Mã gọi cung cấp danh sách DVD và chuỗi từ khóa.
2. Hệ thống kiểm tra `keyword in dvd.title` cho từng đĩa.
3. Hệ thống trả về danh sách kết quả, giữ thứ tự ban đầu và không sửa đầu vào.

Tìm kiếm trong Lab 02 cố ý phân biệt hoa thường: `Star` khớp `Star Wars`,
nhưng `star` không khớp. Không có kết quả hoặc danh sách đầu vào rỗng thì
trả về `[]`; từ khóa rỗng khớp mọi tựa đề.
