# Lab 04 — Release flow và phiên bản phát hành

## Chuẩn bị và phát hành

- [PR #14](https://github.com/phuonganh317/it3180202417227aims/pull/14):
  `topic/prepare-release-1.0.0` → `master`, commit
  `chore: prepare release 1.0.0`. Thêm `aims.__version__ = "1.0.0"`, banner
  lấy phiên bản từ package và CHANGELOG theo Keep a Changelog.
- Tạo `release/lab04` sau PR #14, commit
  `cef939759524a78314b5eb4d8886ad1ad991b434`.
- Annotated tag `v1.0.0` trỏ đúng commit release, thông điệp
  `AIMS-mini 1.0.0 Lab 04 release`.
- [GitHub Release v1.0.0](https://github.com/phuonganh317/it3180202417227aims/releases/tag/v1.0.0)
  đã xuất bản với tiêu đề `AIMS-mini v1.0.0`, notes `Release v1.0.0`
  và asset `aims-1.0.0.zip`.

## Bảo vệ nhánh

Tại thời điểm kiểm tra, API trả `Branch not protected` cho master và danh
sách ruleset rỗng. Mọi thay đổi trong Lab vẫn được tích hợp qua PR bằng
`gh pr create` / `gh pr merge`, không push trực tiếp vào master.

Đã tạo ruleset **Release branches require pull requests**, ID `26260550`,
enforcement `active`, áp dụng `refs/heads/release/*`, không có bypass actor:

- Bắt buộc Pull Request, yêu cầu giải quyết các review thread.
- Không bắt buộc approval của người thứ hai (0 approval), phù hợp bài cá nhân.
- Chặn non-fast-forward và xóa nhánh release.

Đã xác minh các rule hiệu lực bằng:

```sh
gh api repos/phuonganh317/it3180202417227aims/rules/branches/release%2Flab04
```

## Các mốc phiên bản

Tất cả đều là annotated tag đã push, không viết lại các mốc cũ.

| Tag | Nhánh baseline | Commit |
| --- | --- | --- |
| `v0.1.0` | `release/lab01` | `1f1bc5ebd537acac37e3c9e6941acc26a3b29131` |
| `v0.2.0` | `release/lab02` | `4ce83bd2eb0b133197ced864b925aa6de9c300ed` |
| `v0.3.0` | `release/lab03` | `d49b8037deaf63a678229f014cc8a662b2a2efd7` |
| `v1.0.0` | `release/lab04` | `cef939759524a78314b5eb4d8886ad1ad991b434` |

## Phát triển tiếp và Status Accounting

[PR #15](https://github.com/phuonganh317/it3180202417227aims/pull/15) thêm
`Cart.sort_by_title()` và `Cart.sort_by_cost()` từ `feature/sort-cart` vào
master, cùng bốn test và mục Added trong `[Unreleased]`. Sắp xếp tại chỗ,
ổn định; tựa đề không phân biệt hoa thường, giá tăng dần. Không đưa tính năng
này vào release/lab04 hay tag v1.0.0.

Kết quả ngay sau PR #15, trước PR báo cáo này:

```text
$ git log --oneline release/lab04..master
9a37a0a Merge pull request #15 from phuonganh317/feature/sort-cart
1f4453d feat: sort cart by title and cost

$ git diff --stat v0.3.0 v1.0.0
 CHANGELOG.md     | 36 ++++++++++++++++++++++++++++++++++++
 aims/__init__.py |  1 +
 main.py          |  2 ++
 3 files changed, 39 insertions(+)

$ git describe --tags
v1.0.0-2-g9a37a0a
```

Master lúc kiểm toán là `9a37a0a8e3b581ab213ac4bd39374278d42e7a21`;
release vẫn là `cef939759524a78314b5eb4d8886ad1ad991b434`. Sau PR báo cáo,
master có thêm commit tài liệu nên SHA và `git describe` tiếp tục thay đổi.
Hai SHA master/release **khác nhau là kết quả mong đợi** của Lab 04.

## Configuration Audit và tái tạo bản phát hành

Đóng gói trực tiếp từ tag, không lấy working tree hiện tại:

```sh
git -c core.autocrlf=false -c core.eol=lf archive --format=zip --prefix=aims-1.0.0/ --output=aims-1.0.0.zip v1.0.0
```

Các cấu hình chỉ áp dụng cho lệnh archive để giữ newline LF, tránh chuyển
sang CRLF do môi trường Windows; không sửa cấu hình Git của người dùng.

Đã kiểm tra ZIP không lỗi, danh sách tệp khớp `git ls-tree` của v1.0.0,
và từng tệp khớp byte với `git show v1.0.0:<path>`. Sau đó giải nén vào
thư mục tạm và chạy độc lập:

- `python -B -m unittest discover -s tests -v`: **8 test PASS** trên release.
- `python -B main.py`: dòng đầu `AIMS-mini v1.0.0`, dòng cuối
  `Total cost: 63.89 $`.
- Bản phát hành không có `sort_by_title`; master sau PR #15 có **12 test PASS**.

SHA-256 của ZIP đã đính kèm GitHub Release:

```text
7e9833bc727db2172fbd02648a002dce3a5b545b166d13ece77be68bc48051b3
```

ZIP được bỏ qua bởi `.gitignore` và không commit vào nguồn. Tệp untracked
có sẵn `t --state merged` không thuộc bài và được giữ nguyên.

Tham khảo: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) và
[GitHub rulesets API](https://docs.github.com/en/rest/repos/rules).
