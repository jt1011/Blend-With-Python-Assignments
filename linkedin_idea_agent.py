#!/usr/bin/env python3
"""RAM-light Twitter/X -> LinkedIn idea agent MVP.

This script is designed to run without a browser extension loaded all the time.
It consumes captured posts from JSON (from any collector), filters/ranks them,
and produces root ideas in Markdown.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


SE_KEYWORDS = {
    "python", "java", "golang", "rust", "javascript", "typescript", "backend",
    "frontend", "devops", "kubernetes", "docker", "api", "microservice", "llm",
    "ai", "ml", "database", "postgres", "redis", "cloud", "aws", "gcp", "azure",
    "testing", "ci", "cd", "architecture", "scalability", "latency", "debug",
    "git", "system design", "open source", "programming", "engineer", "developer",
    "software", "repo", "deployment", "observability", "sre", "security"
}

STOPWORDS = {
    "the", "and", "for", "with", "this", "that", "from", "have", "you", "your", "about",
    "will", "just", "what", "when", "where", "which", "they", "their", "there", "been",
    "into", "over", "under", "also", "more", "most", "much", "very", "really", "should",
    "could", "would", "than", "then", "them", "some", "only", "good", "great", "like"
}


@dataclass
class Post:
    tweet_id: str
    text: str
    author: str
    url: str
    timestamp: str = ""
    likes: int = 0
    reposts: int = 0
    replies: int = 0


@dataclass
class Idea:
    idea: str
    why_now: str
    linkedin_angle: str
    evidence: list[str]
    confidence: str
    score: float


class IdeaAgent:
    def __init__(self, target_count: int = 100) -> None:
        self.target_count = target_count

    @staticmethod
    def _normalize(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"https?://\S+", "", text)
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return [t for t in IdeaAgent._normalize(text).split() if t and t not in STOPWORDS]

    def _relevance_score(self, text: str) -> float:
        n = self._normalize(text)
        tokens = set(self._tokenize(n))
        overlap = len(tokens.intersection(SE_KEYWORDS))
        if overlap == 0:
            return 0.0
        return min(1.0, overlap / 6)

    @staticmethod
    def _engagement_score(post: Post) -> float:
        weighted = (post.likes * 1.0) + (post.reposts * 2.0) + (post.replies * 1.5)
        return math.log1p(max(weighted, 0)) / 8.0

    def _quality_score(self, post: Post) -> float:
        r = self._relevance_score(post.text)
        e = self._engagement_score(post)
        length_bonus = 0.2 if len(post.text.split()) >= 12 else 0.0
        return (0.65 * r) + (0.25 * e) + (0.10 * length_bonus)

    def _cluster_key(self, text: str) -> str:
        tokens = [t for t in self._tokenize(text) if len(t) > 3]
        top = sorted(tokens)[:8]
        return " ".join(top)

    def select_posts(self, posts: list[Post]) -> list[Post]:
        scored = [(self._quality_score(p), p) for p in posts]
        scored.sort(key=lambda x: x[0], reverse=True)

        cluster_best: dict[str, tuple[float, Post]] = {}
        for score, post in scored:
            if score < 0.20:
                continue
            key = self._cluster_key(post.text)
            if not key:
                continue
            if key not in cluster_best or score > cluster_best[key][0]:
                cluster_best[key] = (score, post)

        selected = [p for _, p in sorted(cluster_best.values(), key=lambda x: self._quality_score(x[1]), reverse=True)]
        return selected[: self.target_count]

    def _idea_from_post(self, post: Post) -> Idea:
        clean = re.sub(r"\s+", " ", post.text.strip())
        sentence = clean[:220].rstrip(" .")

        idea = f"Developers should pay attention to: {sentence}."
        why_now = "This is trending in engineering conversations and likely to influence tooling/workflows soon."
        linkedin_angle = "Share a practical takeaway + your personal opinion on what teams should do next."

        score = self._quality_score(post)
        confidence = "High" if score >= 0.60 else "Medium" if score >= 0.35 else "Low"

        return Idea(
            idea=idea,
            why_now=why_now,
            linkedin_angle=linkedin_angle,
            evidence=[post.url],
            confidence=confidence,
            score=round(score, 3),
        )

    def build_ideas(self, posts: list[Post]) -> list[Idea]:
        selected = self.select_posts(posts)
        ideas = [self._idea_from_post(p) for p in selected]
        ideas.sort(key=lambda i: i.score, reverse=True)
        return ideas


def load_posts(input_path: Path) -> list[Post]:
    raw = json.loads(input_path.read_text(encoding="utf-8"))
    posts: list[Post] = []

    for item in raw:
        posts.append(
            Post(
                tweet_id=str(item.get("tweet_id") or item.get("id") or ""),
                text=str(item.get("text") or ""),
                author=str(item.get("author") or "unknown"),
                url=str(item.get("url") or ""),
                timestamp=str(item.get("timestamp") or ""),
                likes=int(item.get("likes") or 0),
                reposts=int(item.get("reposts") or item.get("retweets") or 0),
                replies=int(item.get("replies") or 0),
            )
        )
    return [p for p in posts if p.text and p.url]


def write_report(ideas: list[Idea], output_path: Path) -> None:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# LinkedIn Root Ideas Report",
        "",
        f"Generated at: {now}",
        f"Total ideas: {len(ideas)}",
        "",
    ]

    for idx, idea in enumerate(ideas, start=1):
        lines.extend(
            [
                f"## {idx}. {idea.idea}",
                f"- **Why now**: {idea.why_now}",
                f"- **LinkedIn angle**: {idea.linkedin_angle}",
                f"- **Evidence**: {', '.join(idea.evidence)}",
                f"- **Confidence**: {idea.confidence} (score={idea.score})",
                "",
            ]
        )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def write_json(ideas: list[Idea], output_path: Path) -> None:
    payload = [asdict(i) for i in ideas]
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate LinkedIn root ideas from captured X feed posts.")
    parser.add_argument("--input", required=True, help="Path to captured_posts.json")
    parser.add_argument("--output-md", default="linkedin_ideas_report.md", help="Output markdown report path")
    parser.add_argument("--output-json", default="linkedin_ideas_report.json", help="Output JSON report path")
    parser.add_argument("--target", type=int, default=100, help="Target number of root ideas")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    posts = load_posts(Path(args.input))
    agent = IdeaAgent(target_count=args.target)
    ideas = agent.build_ideas(posts)
    write_report(ideas, Path(args.output_md))
    write_json(ideas, Path(args.output_json))
    print(f"Generated {len(ideas)} ideas -> {args.output_md}, {args.output_json}")


if __name__ == "__main__":
    main()
