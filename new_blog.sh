#!/usr/bin/env bash
# Scaffold a new blog post and wire it into the listings.
# Usage: ./new_blog.sh "My Post Title" ["optional one-line excerpt"]
# Then edit blogs/<slug>.html with your content and run ./new_blog.sh --publish <slug>
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
BLOGS="$ROOT/blogs"
TODAY="$(date +%B' '%d,%Y)"

die() { echo "error: $*" >&2; exit 1; }

slugify() {
  echo "$1" | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//'
}

# ---- publish mode: insert card into blog listing ----
if [[ "${1:-}" == "--publish" ]]; then
  slug="${2:?usage: ./new_blog.sh --publish <slug>}"
  file="$BLOGS/$slug.html"
  [[ -f "$file" ]] || die "no such post: $file"
  title="$(grep -oP '(?<=<h1[^>]*>)[^<]+(?=</h1>)' "$file" | head -1)"
  date="$(grep -oP '(?<=post-date">)[^<]+(?=</span>)' "$file" | head -1)"
  [[ -n "$title" ]] || die "could not find <h1> in $file"
  [[ -n "$date" ]] || date="$TODAY"
  excerpt="$(grep -oP '(?<=name="description" content=")[^"]+' "$file" | head -1)"
  [[ -n "$excerpt" ]] || excerpt="Read the full post."

  card="      <li>\n        <a class=\"post-card\" href=\"$slug.html\">\n          <span class=\"post-card__meta\">$date</span>\n          <h2 class=\"post-card__title\">$title</h2>\n          <p class=\"post-card__excerpt\">$excerpt</p>\n          <span class=\"post-card__cta\">Read article →</span>\n        </a>\n      </li>\n"

  idx="$BLOGS/index.html"
  grep -q "href=\"$slug.html\"" "$idx" && die "already listed in $idx"
  python3 - "$idx" <<PY
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
anchor = "<!-- BLOG_CARDS -->"
card = """$card"""
if anchor in s:
    s = s.replace(anchor, anchor + "\n" + card, 1)
    open(p, "w", encoding="utf-8").write(s)
    print("updated", p)
else:
    print("no BLOG_CARDS anchor in", p)
PY
  echo "published: $slug  (commit & push to go live)"
  exit 0
fi

# ---- create mode ----
title="${1:?usage: ./new_blog.sh \"My Post Title\"}"
excerpt="${2:-Write your post here.}"
slug="$(slugify "$title")"
file="$BLOGS/$slug.html"
[[ -f "$file" ]] && die "post already exists: $file"

mkdir -p "$BLOGS"
cat > "$file" <<HTML
<!DOCTYPE html>
<html lang="en">

<head>
  <link rel="icon" type="image/png" href="../assets/img/logo.png" />
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>$title — Daniel Liu</title>
  <meta name="description" content="$excerpt" />
  <link href="https://fonts.googleapis.com/css?family=Raleway:400,500,600,700" rel="stylesheet" />
  <link rel="stylesheet" href="blog.css" />
</head>

<body class="blog-shell">

  <header class="blog-site-header">
    <div class="blog-site-header__inner">
      <nav class="site-nav" aria-label="Site">
        <a class="site-nav__wordmark" href="../index.html">Daniel Liu</a>
        <a href="../index.html">About</a>
        <a href="index.html">Blog</a>
        <a href="../index.html#projects">Projects</a>
        <a href="../index.html#toy-projects">Toy Projects</a>
      </nav>
    </div>
  </header>

  <main class="blog-page blog-prose">
    <h1>$title</h1>
    <span class="post-date">$TODAY</span>

    <p>Write your post here.</p>

    <a href="index.html" class="blog-back">← Back to all posts</a>
  </main>

</body>
</html>
HTML

echo "created: $file"
echo "next: edit it, then run  ./new_blog.sh --publish $slug"
