"""CLI สำหรับระบบค้นหาข้อมูลออนไลน์"""

from __future__ import annotations

import argparse

from search_system import SearchError, format_results, search_online


def main() -> int:
    parser = argparse.ArgumentParser(description="ระบบค้นหาข้อมูลออนไลน์")
    parser.add_argument("query", help="คำค้นหา")
    parser.add_argument("--limit", type=int, default=5, help="จำนวนผลลัพธ์")
    args = parser.parse_args()

    try:
        results = search_online(args.query, max_results=args.limit)
    except (ValueError, SearchError) as exc:
        print(f"เกิดข้อผิดพลาด: {exc}")
        return 1

    print(format_results(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
