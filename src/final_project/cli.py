from __future__ import annotations

import argparse
from pathlib import Path

from .services import ReviewService
from .storage import DEFAULT_DATA_PATH, StorageError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI 学习复盘记录系统")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA_PATH, help="JSON 数据文件路径")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="添加复盘记录")
    add.add_argument("question", help="学习问题（必填）")
    add.add_argument("--ai-summary", default="", help="AI 回答摘要")
    add.add_argument("--understanding", default="", help="自己的理解")
    add.add_argument("--tags", default="", help="标签，逗号分隔，例如 --tags Python,基础")

    subparsers.add_parser("list", help="列出所有复盘记录")

    search = subparsers.add_parser("search", help="搜索复盘记录")
    search.add_argument("keyword")

    delete = subparsers.add_parser("delete", help="删除复盘记录")
    delete.add_argument("id", type=int)

    edit = subparsers.add_parser("edit", help="修改复盘记录")
    edit.add_argument("id", type=int)
    edit.add_argument("--question", default=None)
    edit.add_argument("--ai-summary", default=None)
    edit.add_argument("--understanding", default=None)
    edit.add_argument("--tags", default=None)

    subparsers.add_parser("stats", help="查看统计")
    return parser


def format_review(review) -> str:
    tags_str = ",".join(review.tags) if review.tags else "无标签"
    return f"#{review.id} 问题：{review.question} 标签：[{tags_str}] ({review.created_at})"


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    service = ReviewService(args.data)

    try:
        if args.command == "add":
            tags = [t.strip() for t in args.tags.split(",") if t.strip()]
            review = service.add_review(
                question=args.question,
                ai_summary=args.ai_summary,
                understanding=args.understanding,
                tags=tags,
            )
            print(f"已添加：{format_review(review)}")
        elif args.command == "list":
            reviews = service.list_reviews()
            if not reviews:
                print("暂无复盘记录")
            for review in reviews:
                print(format_review(review))
        elif args.command == "search":
            reviews = service.search_reviews(args.keyword)
            if not reviews:
                print("没有找到匹配记录")
            for review in reviews:
                print(format_review(review))
        elif args.command == "delete":
            if service.delete_review(args.id):
                print(f"已删除记录 #{args.id}")
            else:
                print(f"未找到记录 #{args.id}")
                return 1
        elif args.command == "edit":
            tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else None
            review = service.update_review(
                args.id,
                question=args.question,
                ai_summary=args.ai_summary,
                understanding=args.understanding,
                tags=tags,
            )
            if review:
                print(f"已修改：{format_review(review)}")
            else:
                print(f"未找到记录 #{args.id}")
                return 1
        elif args.command == "stats":
            stats = service.stats()
            print(f"复盘总数：{stats['count']}")
            print(f"标签统计：{stats.get('count_by_tag', {})}")
            print(f"每日记录：{stats.get('count_by_date', {})}")
        return 0
    except (ValueError, StorageError) as exc:
        print(f"错误：{exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
