# Câu hỏi thảo luận Lab 02

## Câu 1: Vì sao phải đồng bộ `master` vào nhánh tính năng trước khi gửi/merge PR?

Trong lúc một người phát triển tính năng, `master` có thể đã nhận thay đổi
từ các PR khác. Đồng bộ giúp phát hiện xung đột sớm, kiểm tra sự tương thích
và chạy thử tính năng trên phiên bản tích hợp mới nhất. Nhờ đó, người review
có thể đánh giá thay đổi cùng các phụ thuộc thực tế, giảm rủi ro lỗi sau merge.

Trong bài này, Dev 2 tạo `feature/search-by-title` trước khi PR cart-print
được merge. Sau commit tìm kiếm, Dev 2 thực hiện:

```sh
git fetch origin
git merge origin/master --no-edit
python -B main.py
```

`fetch` cập nhật tham chiếu `origin/master`; `merge` đưa thay đổi mới vào
nhánh tính năng bằng commit đồng bộ khi lịch sử đã phân kỳ. Chạy chương trình
sau đó xác nhận chức năng in giỏ và tổng `63.89 $` vẫn hoạt động. Chỉ cập nhật
nhánh `master` local mà không tích hợp vào nhánh tính năng thì chưa đủ.
Nếu `master` tiếp tục thay đổi trong thời gian review, cần kiểm tra lại trạng
thái tích hợp và các kiểm thử theo quy định của repo trước khi merge.

## Câu 2: Khi nào không được dùng `git rebase`? Vì sao sau Squash/Rebase merge có thể cần `git branch -D`?

Không tự ý rebase các commit đã chia sẻ mà người khác đang dùng làm cơ sở,
đặc biệt trên `master`, nhánh release hoặc baseline đã chốt. Rebase phát lại
commit trên base mới, thường tạo hash mới và viết lại lịch sử. Đẩy lịch sử
đó lên nhánh dùng chung có thể cần force push, làm lịch sử của cộng tác viên
phân kỳ và gây khó khăn khi đồng bộ. Repo có Branch Protection phải tuân thủ
quy tắc bảo vệ; không dùng rebase/force push để vượt quy trình PR.

Rebase phù hợp cho các commit local chưa chia sẻ, hoặc nhánh riêng khi cả
nhóm đã thống nhất cách phối hợp và không ảnh hưởng công việc của người khác.
Rebase-and-merge một PR trên GitHub tích hợp các commit vào base theo phương
thức được repo cho phép; đây không phải việc force push lại lịch sử `master`.

`git branch -d` kiểm tra quan hệ tổ tiên của commit để bảo vệ công việc chưa
merge. Squash merge gộp thay đổi thành một commit mới; rebase merge tạo các
commit mới trên base. Vì vậy, commit gốc của nhánh local có thể không là tổ
tiên của `master`, dù nội dung đã được tích hợp, và `-d` có thể từ chối xóa.

Sau khi xác nhận PR đã merge, cập nhật `master` và kiểm tra không còn công
việc riêng chưa tích hợp, có thể dùng:

```sh
git switch master
git pull --ff-only
git branch -D feature/search-by-title
```

`-D` bỏ qua kiểm tra đã merge, nên không dùng một cách máy móc. Không phải
lúc nào cũng cần `-D`: `gh pr merge --delete-branch` có thể đã xóa nhánh local,
hoặc điều kiện kiểm tra của `-d` đã được thỏa mãn. Nếu nhánh không còn thì
không cần chạy lệnh xóa lại. Merge commit thông thường giữ quan hệ tổ tiên,
nên nhánh đã tích hợp thường xóa được bằng `-d`.

## Câu 3: Nhánh `feature/*` khác nhánh `topic/*` ra sao?

Đây là quy ước đặt tên của nhóm, không phải hai loại nhánh có cơ chế Git khác
nhau. Trong Lab 02:

| Quy ước | Mục đích | Ví dụ |
| --- | --- | --- |
| `feature/*` | Phát triển hành vi/chức năng của sản phẩm. | `feature/cart-print`, `feature/search-by-title` |
| `topic/*` | Công việc có phạm vi cụ thể, thường là tài liệu, quy trình hoặc cấu hình. | `topic/pr-template`, `topic/use-case-diagram`, `topic/answers-lab02` |

Cả hai đều tách từ `master` phù hợp, có commit rõ mục đích, được push lên
remote để mở PR, review và kiểm thử trước khi tích hợp. Sau khi merge và xác
nhận không còn công việc chưa tích hợp, xóa nhánh để giữ repo gọn. Theo nghĩa
rộng, một nhánh tính năng cũng là một topic branch; tiền tố giúp nhóm phân
loại công việc chứ không tự áp đặt quyền hay phương thức merge.
