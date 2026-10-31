# Lab 03 — Bugfix flow, xung đột và hoàn tác

## A. Bugfix từ master: giới hạn 20 DVD

- Issue: [#7](https://github.com/phuonganh317/it3180202417227aims/issues/7).
- Nhánh: `bugfix/cart-limit-off-by-one`.
- Commit test `7e038a0`: `test: reproduce cart limit bug (#7)`.
- Trước sửa, unittest FAIL tại `assertFalse` cho DVD thứ 21: `True is not false`.
- Commit sửa `8e4944e`: đổi `>` thành `>=`; body commit là `Fixes #7`.
- Sau sửa, nhận đủ 20 DVD, từ chối DVD thứ 21 và không đổi số lượng/tổng tiền.
- [PR #8](https://github.com/phuonganh317/it3180202417227aims/pull/8)
  được merge bằng merge commit; Issue #7 tự chuyển thành CLOSED.

## B. Bugfix từ feature

`feature/discount` được tạo từ master, có logic sơ bộ trừ trực tiếp số phần
trăm khỏi tổng tiền (commit `3543233`) và được push trước khi tạo
`bugfix/discount-calculation` từ `origin/feature/discount`.

Commit test `a1098cc` chứng minh lỗi: tổng 200 giảm 20% cho ra 180 thay vì
160; giỏ rỗng cho ra -20; tỷ lệ không hợp lệ không báo lỗi. Trường hợp tổng
100 giảm 20% vẫn tình cờ đúng nên cần kiểm thử thêm tổng khác 100.

Commit sửa `850ef41` tính `total_cost() * (1 - percent / 100)` và kiểm tra
`0 <= percent <= 100`, báo `ValueError` nếu không hợp lệ. Sáu test giảm giá
kiểm tra tổng 100/200, biên 0/100%, tỷ lệ không hợp lệ, giỏ rỗng và không
thay đổi giá gốc. Cùng test giới hạn giỏ, cả 7 test PASS.

- [PR #9](https://github.com/phuonganh317/it3180202417227aims/pull/9):
  **base `feature/discount`**, head `bugfix/discount-calculation`.
- Sau khi sửa trên feature, [PR #10](https://github.com/phuonganh317/it3180202417227aims/pull/10)
  tích hợp `feature/discount` vào `master` để baseline chứa cả code và test.

## C. Xung đột và giải quyết

Hai nhánh `feature/vietnamese-messages` và `feature/detailed-messages` được
tạo cùng base `a872d00`, cùng sửa dòng thông báo thành công trong `add_dvd`.

1. Nhánh tiếng Việt sửa thành `Đã thêm đĩa vào giỏ hàng`, được merge trước
   qua [PR #11](https://github.com/phuonganh317/it3180202417227aims/pull/11).
2. Nhánh chi tiết giữ base cũ, sửa cùng dòng thành thông báo tiếng Anh kèm
   `dvd.title` trong commit `831b353`.
3. Chạy `git fetch origin` và `git merge origin/master --no-edit` thực sự báo:

   ```text
   CONFLICT (content): Merge conflict in aims/cart.py
   Automatic merge failed; fix conflicts and then commit the result.
   ```

4. Xóa các conflict marker và kết hợp thành:

   ```python
   print(f"Đã thêm đĩa vào giỏ hàng: {dvd.title}")
   ```

5. Thêm test kiểm tra tiếng Việt kèm tên DVD, chạy toàn bộ 8 test PASS rồi
   `git add aims/cart.py tests/test_cart.py` và commit hoàn tất merge
   `c0e2867`. [PR #12](https://github.com/phuonganh317/it3180202417227aims/pull/12)
   tích hợp kết quả vào master bằng merge commit.

## D. Reset, reflog và revert

Đã thực hành thực tế trên nhánh local `topic/undo-practice`, với commit tạm
chỉ thêm một dòng vào README, chưa push lên remote. Trước thao tác đã kiểm
tra index và các tệp được theo dõi không có thay đổi ngoài bài thực hành.

- Base: `6d32f290f00b4f500fd37c0622169158c942d7c8`.
- Commit nháp: `514b7c57271ae6a43a455674dad251e69151cb40`.

| Lệnh đã thực hành | Kết quả đã kiểm tra |
| --- | --- |
| `git reset --soft <base>` | HEAD về base, thay đổi README vẫn được stage. |
| `git reset --mixed <base>` | Index trở về base, thay đổi README còn trong working tree nhưng chưa stage. |
| `git reset --hard <base>` | HEAD, index và tệp được theo dõi trở về base; dòng nháp bị loại bỏ. |
| `git reflog -n 8` | Tìm thấy commit nháp tại `HEAD@{3}` ở thời điểm kiểm tra. |
| `git reset --hard <hash-tìm-trong-reflog>` | Khôi phục commit nháp và xác nhận dòng README xuất hiện lại. |

Sau kiểm tra, đã reset nhánh nháp về base, trở lại master và xóa nhánh nháp.
README không còn dòng thực hành. Commit nháp không được push; bản ghi reflog
là dữ liệu local và có thời hạn lưu giữ, không thay thế bản sao lưu.

### Hoàn tác trên nhánh dùng chung

`reset` thay đổi vị trí nhánh; `--hard` còn loại bỏ thay đổi trong các tệp
được theo dõi. Không dùng reset/force push để viết lại lịch sử master hoặc
release đã chia sẻ. `git revert` tạo commit mới đảo ngược thay đổi, giữ lại
lịch sử, nên phù hợp khi cần hoàn tác trên nhánh dùng chung.

Trong repo có Branch Protection, tạo nhánh hoàn tác và đi qua PR:

```sh
git switch master
git pull --ff-only
git switch -c bugfix/revert-change
git revert <commit-can-hoan-tac>
python -m unittest discover -s tests -v
git push -u origin bugfix/revert-change
gh pr create --base master --head bugfix/revert-change
gh pr merge bugfix/revert-change --merge --delete-branch
```

Nếu hoàn tác một merge commit, cần chọn đúng parent làm mainline, thường
là `git revert -m 1 <merge-commit>` khi parent 1 là nhánh đích. Phải kiểm tra
parents và ảnh hưởng trước khi dùng, vì revert merge còn ảnh hưởng cách Git
xử lý các lần merge sau. Lab này không có thay đổi đã merge nào cần loại bỏ,
nên chỉ giải thích revert, không đảo ngược các chức năng vừa hoàn thành.

## Kiểm tra và chốt bài

Tất cả thay đổi vào master đi qua `gh pr create` / `gh pr merge`; không push
trực tiếp lên master. Nhánh nộp `release/lab03` được tạo từ master sau PR tài
liệu này. Các lệnh kiểm tra cuối:

```sh
python -m unittest discover -s tests -v
git log --oneline --graph -n 15
git rev-parse origin/master origin/release/lab03
```

Yêu cầu: 8 test PASS và hai SHA trùng nhau tại thời điểm chốt bài.
