# Lab 05 — Hotfix flow và bảo trì nhiều phiên bản

## Quy trình và các PR

Mọi thay đổi vào master và release đều đi qua nhánh riêng,
`gh pr create` và `gh pr merge --merge --delete-branch`. Nhánh release mới
được push khi khởi tạo; các thay đổi sau đó đi qua PR theo ruleset release/*.
Các tag cũ không bị sửa hoặc di chuyển.

| PR | Head → base | Kết quả |
| --- | --- | --- |
| [#17](https://github.com/phuonganh317/it3180202417227aims/pull/17) | `feature/search-by-category` → `master` | Thêm category search phía trên title search và hai test. |
| [#18](https://github.com/phuonganh317/it3180202417227aims/pull/18) | `topic/prepare-release-1.1.0` → `master` | Version 1.1.0, CHANGELOG, sau đó tạo release/lab05. |
| [#19](https://github.com/phuonganh317/it3180202417227aims/pull/19) | `topic/basic-ci` → `master` | CI cho PR và push master; mở nháp trước hotfix, đồng bộ và merge sau khi vá cả ba dòng. |
| [#21](https://github.com/phuonganh317/it3180202417227aims/pull/21) | `hotfix/search-case-insensitive` → `release/lab04` | Vá 1.0.1 từ đúng baseline 1.0.0. |
| [#22](https://github.com/phuonganh317/it3180202417227aims/pull/22) | `bugfix/propagate-search-master` → `master` | Cherry-pick fix, bổ sung CHANGELOG, đóng Issue #20. |
| [#23](https://github.com/phuonganh317/it3180202417227aims/pull/23) | `bugfix/propagate-search-lab05` → `release/lab05` | Cherry-pick fix và ghi release notes trước khi gắn v1.1.0. |

Issue #20 chưa tồn tại khi bắt đầu. Sau ba PR thật #17–19, đã tạo đúng
[Issue #20](https://github.com/phuonganh317/it3180202417227aims/issues/20),
mô tả lỗi `lion` không tìm được `The Lion King` trên v1.0.0.

## Hotfix và tách biệt phiên bản

Nhánh hotfix tạo bằng:

```sh
git switch -c hotfix/search-case-insensitive origin/release/lab04
```

Thêm bốn regression test, chạy trước sửa: **2 FAIL** cho từ khóa `lion`
và `STAR`; sau sửa thành `keyword.lower() in dvd.title.lower()`:
**12 test PASS** trên dòng 1.0.x.

Hai commit được tách rõ:

1. `0d8dacb6b421b5549d3566389cd8fbcc4be22311` —
   `fix: make search by title case-insensitive`, body `Refs #20`.
   Chỉ chứa `aims/search.py` và `tests/test_search_title.py`.
2. `c7da98b6dab2d96190bc5e6aa743d93a018d294f` —
   `chore: bump version to 1.0.1`, chỉ sửa version và CHANGELOG.

`FIX_SHA` là commit thứ nhất. Sau PR #21, annotated tag `v1.0.1` trỏ
`6451c58e7bce934f0150a61995458a393c211572` của release/lab04.

Trên cả hai nhánh lan truyền, đã chạy đúng:

```sh
git cherry-pick -x 0d8dacb6b421b5549d3566389cd8fbcc4be22311
```

- Master nhận commit `1116030fa13394658a259dfd669c2319b5bc8a87`.
- Release/lab05 nhận commit `5a9c0bff601fd9e625609c5c3fe90d5494329c9b`.
- Cả hai có trailer `(cherry picked from commit 0d8dacb6b421b5549d3566389cd8fbcc4be22311)`.
- Không cherry-pick commit nâng phiên bản 1.0.1, nên hai dòng mới giữ 1.1.0.
- Category search nằm phía trên title search, cherry-pick tự áp dụng không conflict.
- CHANGELOG cập nhật qua commit riêng trên từng dòng, không gộp vào FIX_SHA.

PR #22 có `Fixes #20`; Issue #20 tự chuyển CLOSED khi merge vào master.
Sau PR #23 mới gắn annotated tag `v1.1.0` tại
`dc241c497774bb431e6172f901400d103d14dad4` và push lên origin.

## Configuration Audit

Kết quả thực tế sau khi lan truyền bản vá:

```text
$ git log --all --oneline --grep "cherry picked from commit"
5a9c0bf fix: make search by title case-insensitive
1116030 fix: make search by title case-insensitive

$ git tag --contains 0d8dacb6b421b5549d3566389cd8fbcc4be22311
v1.0.1

$ git cherry -v origin/master origin/release/lab04
- 0d8dacb6b421b5549d3566389cd8fbcc4be22311 fix: make search by title case-insensitive
+ c7da98b6dab2d96190bc5e6aa743d93a018d294f chore: bump version to 1.0.1
```

`--contains` kiểm tra quan hệ tổ tiên của commit, không kiểm tra nội dung
patch. Do cherry-pick tạo SHA mới, v1.1.0 có bản vá nhưng không chứa commit
FIX_SHA gốc trong lịch sử. Dấu `-` của `git cherry` xác nhận patch tương
đương đã có trên master; dấu `+` cho biết commit bump 1.0.1 riêng chưa được
áp dụng ở master. Đây là kết quả đúng, tránh hạ phiên bản master.

## Kiểm thử độc lập các phiên bản

Đã dùng `git archive` từng ref, giải nén vào thư mục tạm riêng và chạy
`python -B -m unittest discover -s tests -v`, kiểm tra version, hành vi tìm
`lion`, sự hiện diện của category search và output demo.

| Ref | Version | Test PASS | Tìm `lion` | Category search |
| --- | --- | --- | --- | --- |
| `v1.0.0` | 1.0.0 | 8 | Không tìm thấy, tái hiện lỗi cũ | Không |
| `v1.0.1` | 1.0.1 | 12 | Tìm được The Lion King | Không |
| `v1.1.0` | 1.1.0 | 18 | Tìm được The Lion King | Có |
| `origin/master` sau PR #22 | 1.1.0 | 18 | Tìm được The Lion King | Có |

Tất cả demo in đúng banner phiên bản và dòng cuối `Total cost: 63.89 $`.
Tag v1.0.0 vẫn ở `cef939759524a78314b5eb4d8886ad1ad991b434`.

## GitHub Actions CI

`.github/workflows/ci.yml` dùng `pull_request` không lọc nhánh đích và
`push` vào master; runner Ubuntu, Python 3.13, quyền `contents: read`,
timeout 10 phút. Lệnh chạy:

```sh
python -m unittest discover -s tests -v
```

Workflow đã có lần chạy thành công trên PR #19 sau khi đồng bộ hotfix:
[run 41169920015](https://github.com/phuonganh317/it3180202417227aims/actions/runs/41169920015).
Sau merge PR #19, sự kiện push master cũng chạy thành công tại
[run 41169955751](https://github.com/phuonganh317/it3180202417227aims/actions/runs/41169955751).
Các lần chạy tiếp theo của PR báo cáo và merge master được kiểm tra trên
GitHub trước khi kết thúc bài. Workflow được đưa vào master; các baseline
release giữ nguyên nội dung đã chốt, không tự thêm file CI sau khi gắn tag.

Tham khảo cấu hình action chính thức:
[actions/checkout](https://github.com/actions/checkout) và
[actions/setup-python](https://github.com/actions/setup-python).

Tệp untracked có sẵn `t --state merged` được giữ nguyên, không commit.
