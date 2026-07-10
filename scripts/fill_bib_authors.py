#!/usr/bin/env python3
"""fill_bib_authors.py

v3 改稿 B1: 把 survey.bib 里 33 条空 `author={{}}` 从对应 paper note 里
抽取作者列表, 重写 bib 的 author 字段. 保留已有 `{{...}}` verbatim 的
非空 27 条不动.

抽取优先级 (按行内解析顺序):
  1. **完整作者列表**: A, B, C           (首选 - 完整列表)
  2. **作者**(N 位,...):A, B, C           (无完整列表时用这个)
  3. **作者**: A, B, C                   (单行作者行)
  4. **作者**:**A, B, C**               (粗体作者)
  5. **第一作者**: Foo                   (兜底 - 只有单个)

清理规则:
  - 去掉星号 / 下标 / 上标 / 注释: **, ¹²³⁴†*, 等贡献标记
  - 去掉 (Fellow, IEEE), (通讯), PDF 头部实测 等
  - 简化 "A and B and C" -> "A, B, C"
  - 保留 "First Last" 完整姓名
  - 大于 80 字截断: 只保留前 3 + ", et al."
"""
from __future__ import annotations
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BIB_PATH = REPO_ROOT / "docs/survey/survey.bib"
NOTES_DIR = REPO_ROOT / "docs/appendix/paper-notes"


def to_cite_key(stem: str) -> str:
    """2023-kerbl-3dgs -> kerbl20233dgs (与 extract_paper_summary 同规则)."""
    m = re.match(r"^(\d{4})-([a-z0-9-]+)$", stem)
    if not m:
        return stem.replace("-", "")
    year, name = m.groups()
    parts = name.split("-", 1)
    first = parts[0]
    rest = parts[1].replace("-", "") if len(parts) > 1 else ""
    return f"{first}{year}{rest}"


def stem_from_note(notes_dir: Path) -> dict[str, str]:
    """build cite_key -> stem mapping (skip INDEX.md)."""
    m = {}
    for p in sorted(notes_dir.glob("*.md")):
        if p.stem == "INDEX":
            continue
        m[to_cite_key(p.stem)] = p.stem
    return m


def clean_author_string(raw: str) -> str:
    """清理单行作者行, 提取 'A, B, C'."""
    # 去掉粗体星号
    s = re.sub(r"\*\*", "", raw)
    # 去掉下标 / 上标: ¹²³⁴⁰, * 等
    s = re.sub(r"[¹²³⁴⁰˒]", "", s)
    s = re.sub(r"\*†", "", s)
    s = re.sub(r"†", "", s)
    # 去掉 `(通讯)`, `(PDF 头部实测)` 等所有 (...) 注释, 除非名字本身有 `(Fellow, IEEE)` (极少)
    # 简化: 先去掉末尾 "(...)" 注解, 不去掉名字中括号
    s = re.sub(r"\((?:通讯|Fellow|IEEE|PDF[^)]*|[^()]*实测|[^()]*metadata|按[^()]*|[^()]*头部|对应[^()]*|等贡献[^()]*|共同一作[^()]*|⋆[^()]*|Corresponding[^()]*)\)", "", s)
    # 中文全角括号 ((...)) 的同样的注释清理 - 包括 "（..., PDF 头部直引）" 的中文括号内文本
    s = re.sub(r"（[^（）]*PDF[^）]*）", "", s)
    s = re.sub(r"（[^（）]*通讯[^）]*）", "", s)
    s = re.sub(r"（[^（）]*第一作者[^）]*）", "", s)
    s = re.sub(r"（[^（）]*双通讯[^）]*）", "", s)
    # 也清理单独的 (Fellow, IEEE) 不应清掉 - 这个是个特例, 不过这里清掉没关系
    s = re.sub(r"（[^（）]*实测[^）]*）", "", s)
    s = re.sub(r"（[^（）]*⋆[^）]*）", "", s)
    # 去掉数字尾注 "Zicong Chen¹" - 已经处理
    # 把 "and" 替换为 ","
    s = s.replace(" and ", ", ")
    s = s.replace("、", ",")  # 中文顿号
    # 拆分名字 (按 , 分)
    names = [n.strip() for n in s.split(",") if n.strip()]
    # 去掉单字符 (常为 "*" / "†" 残留)
    cleaned = []
    for n in names:
        # 去除两端标点 + 残余 *
        n2 = re.sub(r"^[*†\s]+|[*†\s]+$", "", n).strip()
        if not n2 or len(n2) < 3:
            continue
        # 跳过显然是注释的 (含 "位" / "metadata" / "arxiv" / "PDF" / "等贡献")
        if any(skip in n2.lower() for skip in ["位", "metadata", "arxiv", "pdf", "贡献", "共同一作"]):
            continue
        cleaned.append(n2)
    return ", ".join(cleaned)


def extract_complete_author_list(text: str) -> str:
    """Try 完整作者列表 first; fallback 作者(...)
    Note 段以 `## 年份 / 作者 / ...` 开头 (或 `## 年份 / 作者`).
    """
    # 切到第一个 `## 方法` 段, 因为该段不含作者信息
    years_block_match = re.search(
        r"^##\s*年份[\s\S]*?(?=^##\s+[^\s])", text, re.M
    )
    if not years_block_match:
        # fallback: 整文件
        years_block = text
    else:
        years_block = years_block_match.group(0)

    # 优先级 1: **完整作者列表**
    m = re.search(
        r"^\-\s*\*\*完整作者列表[^*]*\*\*:\s*(.+)$",
        years_block, re.M
    )
    if m:
        return clean_author_string(m.group(1))

    # 优先级 2: **作者**(...位,...) / **作者** (...位...)
    m = re.search(
        r"^\-\s*\*\*作者\*\*\s*\([^)]*\):\s*\*?\*?(.+?)\*?\*?\s*$",
        years_block, re.M
    )
    if m:
        return clean_author_string(m.group(1))

    # 优先级 3: **作者**: (no parens)
    m = re.search(
        r"^\-\s*\*\*作者\*\*\s*:\s*(.+)$",
        years_block, re.M
    )
    if m:
        return clean_author_string(m.group(1))

    # 优先级 4: **作者**:**A, B** (bold only, no colon after bold)
    m = re.search(
        r"^\-\s*\*\*作者\*\*\s*(?:[:：]\s*)?\*?\*?(.+?)\*?\*?\s*$",
        years_block, re.M
    )
    if m:
        return clean_author_string(m.group(1))

    # 优先级 5: **第一作者** + 可选 **其他作者** (兜底)
    first_authors = []
    m = re.search(
        r"^\-\s*\*\*第一作者[^*]*\*\*\s*[:：]?\s*(.+?)\s*$",
        years_block, re.M
    )
    if m:
        fa = clean_author_string(m.group(1))
        if fa:
            first_authors.append(fa)
    # 看是否有 其他作者 / 通讯作者 行, 如有追加
    extra = re.search(
        r"^\-\s*\*\*(?:其他作者|通讯作者)\*\*\s*[:：]?\s*(.+?)\s*$",
        years_block, re.M
    )
    if extra and first_authors:
        ea = clean_author_string(extra.group(1))
        if ea:
            first_authors.append(ea)
    if first_authors:
        combined = ", ".join(first_authors)
        # 兜底: 1 个名字时加 et al.
        if "," not in combined and "et al" not in combined:
            combined = f"{combined}, et al."
        return combined
    return ""


def main() -> int:
    if not BIB_PATH.exists():
        print(f"ERR: bib not found at {BIB_PATH}", flush=True)
        return 1
    bib_text = BIB_PATH.read_text(encoding="utf-8")

    # parse bib entries
    # split on lines starting with @
    entries = re.split(r"(?=^@\w+\{)", bib_text, flags=re.M)

    cite_key_to_stem = stem_from_note(NOTES_DIR)

    filled = 0
    skipped = 0
    failed = 0
    log = []

    new_entries = []
    for entry in entries:
        if not entry.strip().startswith("@"):
            new_entries.append(entry)
            continue
        # 抽 cite key
        mkey = re.match(r"^@(\w+)\{([^,]+),", entry.strip())
        if not mkey:
            new_entries.append(entry)
            continue
        cite_key = mkey.group(2).strip()
        # 检查 author={{}}
        if re.search(r"^  author=\{\{\}\}", entry, re.M):
            stem = cite_key_to_stem.get(cite_key)
            if not stem:
                failed += 1
                log.append(f"NO-NOTE: {cite_key}")
                new_entries.append(entry)
                continue
            note = NOTES_DIR / f"{stem}.md"
            if not note.exists():
                failed += 1
                log.append(f"NO-NOTE-FILE: {cite_key} -> {stem}")
                new_entries.append(entry)
                continue
            text = note.read_text(encoding="utf-8")
            authors = extract_complete_author_list(text)
            if not authors:
                failed += 1
                log.append(f"NO-AUTHOR-EXTRACT: {cite_key}")
                new_entries.append(entry)
                continue
            # 短一作者长截断 (>80 字: 取前 3 + et al.)
            if len(authors) > 80:
                parts = [p.strip() for p in authors.split(",") if p.strip()]
                if len(parts) > 3:
                    authors = ", ".join(parts[:3]) + ", et al."
                # else keep as-is
            # 写入 author
            new_entry = re.sub(
                r"^  author=\{\{\}\}",
                f"  author={{{{{authors}}}}}",
                entry,
                count=1,
                flags=re.M,
            )
            new_entries.append(new_entry)
            filled += 1
            log.append(f"FILL: {cite_key} <- {authors[:60]}{'...' if len(authors) > 60 else ''}")
        else:
            skipped += 1
            new_entries.append(entry)

    new_bib = "".join(new_entries)
    BIB_PATH.write_text(new_bib, encoding="utf-8")

    print(f"=== fill_bib_authors.py ===")
    print(f"Filled:  {filled}")
    print(f"Skipped (already non-empty): {skipped}")
    print(f"Failed:  {failed}")
    print()
    if log:
        print("=== details (first 20) ===")
        for ln in log[:20]:
            print(ln)
        if len(log) > 20:
            print(f"... +{len(log)-20} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
