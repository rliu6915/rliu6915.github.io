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
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Raleway:300,300i,400,400i,500,500i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i" rel="stylesheet" />
  <link href="../assets/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet" />
  <link href="../assets/vendor/boxicons/css/boxicons.min.css" rel="stylesheet" />
  <link href="../assets/css/style.css" rel="stylesheet" />
  <link rel="stylesheet" href="blog.css" />
</head>

<body class="blog-shell">

  <header id="header" class="header-top">
    <div class="container">
      <h1><a href="../index.html">Daniel Liu</a></h1>
      <nav class="nav-menu d-none d-lg-block">
        <ul>
          <li><a href="../index.html"><span>About</span></a></li>
          <li class="active"><a href="index.html"><span>Blog</span></a></li>
          <li><a href="../index.html#projects"><span>Projects</span></a></li>
          <li><a href="../index.html#toy-projects"><span>Toy Projects</span></a></li>
        </ul>
      </nav>
      <div class="social-links">
        <a href="mailto:rliu6915@163.com" target="_blank" class="google" rel="noopener"><i class="bx bxl-google"></i></a>
        <a href="https://github.com/rliu6915" target="_blank" class="github" rel="noopener"><i class="bx bxl-github"></i></a>
      </div>
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
