import os
import subprocess

SOLUTION_FOLDER_PATH = "solution"
RESOURCE_FOLDER_PATH = os.path.join("test", "resources", "task7")
TAIL_N = 17


def _is_header_line(line: str, path: str) -> bool:
    # Accept common variants: "==> path <==", "path:", or exactly "path"
    return line.strip() == f"==> {path} <==" or line.strip() == f"{path}:" or line.strip() == path


def _strip_optional_single_header(stdout: str, path: str) -> str:
    """
    For single-file runs: students may or may not print a header.
    If the first line looks like a header for 'path', drop it and a single following newline.
    """
    lines = stdout.splitlines(keepends=True)
    if not lines:
        return stdout
    first_line = lines[0].rstrip("\n")
    if _is_header_line(first_line, path):
        # drop the first line; if next line is blank due to formatting, keep behavior natural
        return "".join(lines[1:])
    return stdout


def _split_by_headers(stdout: str, paths: list[str]) -> list[str]:
    """
    For multi-file runs: return list of content blocks (tail output) in the same order as paths.
    Require that each block is preceded by an acceptable header for that path.
    Allow optional blank lines between blocks.
    """
    lines = stdout.splitlines(keepends=True)
    blocks = []
    i = 0
    for idx, path in enumerate(paths):
        # skip blank lines between blocks
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        assert i < len(lines), "expected header, got end of output"
        assert _is_header_line(lines[i].rstrip("\n"), path), f"missing/invalid header for {path!r}"
        i += 1
        # collect until next header (or end)
        start = i
        while i < len(lines):
            # if current line (non-blank) is a header for any path -> stop
            if lines[i].strip() != "" and any(_is_header_line(lines[i].rstrip("\n"), p) for p in paths):
                break
            # if current and following blank lines lead to a header -> treat blanks as separator, do not include
            if lines[i].strip() == "":
                j = i
                while j < len(lines) and lines[j].strip() == "":
                    j += 1
                if j < len(lines) and any(_is_header_line(lines[j].rstrip("\n"), p) for p in paths):
                    break
            i += 1
        blocks.append("".join(lines[start:i]))
    # any trailing lines after last block should be only blank
    tail = "".join(lines[i:])
    assert tail.strip() == "", "unexpected trailing output after last block"
    return blocks


def _normalize_trailing_newline(s: str) -> str:
    # collapse any number of trailing newlines to exactly one
    return s.rstrip("\n") + "\n"


def test_single_file_short() -> None:
    # file has fewer than 17 lines -> print whole file; header optional
    path = os.path.join(RESOURCE_FOLDER_PATH, "short_input.txt")
    result = subprocess.run(
        ["python", os.path.join(SOLUTION_FOLDER_PATH, "task7.py"), path],
        stdout=subprocess.PIPE,
        text=True,
    )
    with open(path, "r", encoding="utf-8") as f:
        expected = f.read()
    out = _strip_optional_single_header(result.stdout, path)
    assert _normalize_trailing_newline(out) == _normalize_trailing_newline(expected)


def test_single_file_long() -> None:
    # file has more than 17 lines -> print last 17; header optional
    path = os.path.join(RESOURCE_FOLDER_PATH, "long_input.txt")
    result = subprocess.run(
        ["python", os.path.join(SOLUTION_FOLDER_PATH, "task7.py"), path],
        stdout=subprocess.PIPE,
        text=True,
    )
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    expected_tail = "".join(lines[-TAIL_N:]) if len(lines) > TAIL_N else "".join(lines)
    out = _strip_optional_single_header(result.stdout, path)
    assert _normalize_trailing_newline(out) == _normalize_trailing_newline(expected_tail)


def test_multiple_files_mixed_lengths() -> None:
    # two files: one short (<=17), one long (>17). Each block must be preceded by a header.
    path1 = os.path.join(RESOURCE_FOLDER_PATH, "short_input.txt")
    path2 = os.path.join(RESOURCE_FOLDER_PATH, "long_input.txt")

    result = subprocess.run(
        ["python", os.path.join(SOLUTION_FOLDER_PATH, "task7.py"), path1, path2],
        stdout=subprocess.PIPE,
        text=True,
    )

    blocks = _split_by_headers(result.stdout, [path1, path2])
    # block 1: full file (<=17 lines)
    with open(path1, "r", encoding="utf-8") as f1:
        expected1 = f1.read()
    assert _normalize_trailing_newline(blocks[0]) == _normalize_trailing_newline(expected1)
    # block 2: last 17 lines
    with open(path2, "r", encoding="utf-8") as f2:
        lines2 = f2.readlines()
    expected2 = "".join(lines2[-TAIL_N:]) if len(lines2) > TAIL_N else "".join(lines2)
    assert _normalize_trailing_newline(blocks[1]) == _normalize_trailing_newline(expected2)
