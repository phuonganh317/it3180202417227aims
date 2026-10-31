# Câu hỏi thảo luận Lab 01

## Câu 1: Cấu hình `--global` được lưu ở đâu và khác gì `--local`?

`git config --global` thường lưu cấu hình trong `~/.gitconfig`, với `~` là
thư mục home của người dùng (trên máy này là `C:\Users\admin`). Cấu hình này
áp dụng cho mọi repository của cùng người dùng. Git cũng hỗ trợ tệp cấu hình
global tại `$XDG_CONFIG_HOME/git/config` (mặc định là `~/.config/git/config`).

`git config --local` lưu cấu hình trong `.git/config` của repository thông
thường và chỉ áp dụng cho repository đó. Khi cùng một khóa được khai báo ở
cả hai phạm vi, giá trị local được ưu tiên hơn global. Ví dụ, có thể đặt
`user.email` global cho tài khoản cá nhân và ghi đè local cho một repo học tập.

Kiểm tra phạm vi và tệp nguồn bằng:

```sh
git config --list --show-origin --show-scope
```

## Câu 2: Vì sao dùng `git mv` thay vì xóa file cũ và tạo file mới?

`git mv` thực hiện việc di chuyển/đổi tên tệp và đưa thay đổi tương ứng vào
staging area trong một lệnh, giúp tránh quên stage việc xóa đường dẫn cũ hoặc
thêm đường dẫn mới. Trong Lab 01, lệnh này dùng để chuyển `dvd.py` và `cart.py`
vào package `aims/`, giúp việc review và truy vết lịch sử đổi tên rõ ràng.

Có thể lần theo lịch sử trước và sau khi di chuyển bằng:

```sh
git log --follow -- aims/dvd.py
git log --follow -- aims/cart.py
```

Về bản chất, Git lưu snapshot và nhận diện đổi tên dựa trên độ tương đồng
nội dung; `git mv` không tạo một loại metadata đổi tên riêng. Xóa tệp cũ rồi
thêm tệp mới có nội dung tương tự vẫn có thể được Git nhận diện là đổi tên.
Dùng `git mv` và tách commit di chuyển khỏi commit sửa nội dung là quy trình
rõ ràng, ít sai sót và thuận tiện để giữ lịch sử truy vết với `--follow`.

## Câu 3: Nhánh `release/lab01` có phải là một baseline không? Vì sao?

Có. Trong quy trình của Lab 01, `release/lab01` đại diện cho phiên bản ổn định
đã tích hợp thay đổi và kiểm thử, được chốt để nghiệm thu hoặc nộp bài.
Baseline cung cấp mốc tham chiếu để tái hiện sản phẩm, đối chiếu thay đổi và
xác định chính xác phiên bản được đánh giá.

Tên nhánh tự nó không bảo đảm tính ổn định: cần chốt nhánh từ `master` đã
kiểm thử và ghi nhận commit tương ứng. Nhánh đã tạo quá sớm phải được cập
nhật để chứa cả phần refactor và câu trả lời thảo luận trước khi chốt bài.
Sau khi chốt, mọi thay đổi phải qua quy trình kiểm soát thay đổi/hotfix,
được review và kiểm thử, đồng thời tích hợp lại vào các nhánh liên quan.
Không tùy tiện sửa trực tiếp hoặc viết lại lịch sử baseline.

## Câu 4: Vì sao không commit thẳng lên `master` dù làm một mình?

`master` cần luôn giữ trạng thái ổn định và có thể chạy được. Phát triển trên
nhánh riêng giúp cô lập công việc chưa hoàn tất; chỉ tích hợp khi đã kiểm tra
diff và kiểm thử. Pull Request ghi lại mục đích, phạm vi thay đổi và kết quả
kiểm thử, tạo cơ hội tự review ngay cả khi chỉ có một người làm.

Quy trình này giúp kiểm soát thay đổi, truy vết quyết định và thuận tiện cho
người khác tham gia sau này. Merge commit với `--no-ff` giữ ranh giới của từng
nhóm thay đổi; khi cần có thể hoàn tác một lần tích hợp bằng
`git revert -m 1 <merge-commit>` mà không viết lại lịch sử đã chia sẻ.

Trong trường hợp CLI chưa đăng nhập, Lab này cho phép phương án merge local
với `--no-ff` rồi push. Đây là phương án thay thế được chỉ định; một merge
commit có thông điệp nhắc tới PR không đồng nghĩa đã tạo PR thực trên GitHub.
