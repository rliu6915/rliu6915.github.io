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

# ---- publish mode: insert card into both listings ----
if [[ "${1:-}" == "--publish" ]]; then
  slug="${2:?usage: ./new_blog.sh --publish <slug>}"
  file="$BLOGS/$slug.html"
  [[ -f "$file" ]] || die "no such post: $file"
  # pull title + date from the post file
  title="$(grep -oP '(?<=<h1>)[^<]+(?=</h1>)' "$file" | head -1)"
  date="$(grep -oP '(?<=post-date">)[^<]+(?=</span>)' "$file" | head -1)"
  [[ -n "$title" ]] || die "could not find <h1> in $file"
  [[ -n "$date" ]] || date="$TODAY"

  card="        <div class=\"col-lg-12\" data-aos=\"fade-up\">\n          <div class=\"col-md-12 mt-4 mt-md-0 icon-box\" data-aos=\"fade-up\" data-aos-delay=\"100\">\n            <span class=\"date\">$date</span>\n            <h4><a href=\"$slug.html\">$title</a></h4>\n            <a href=\"$slug.html\">Read more →</a>\n          </div>\n        </div>\n"

  for idx in "$ROOT/index.html" "$BLOGS/index.html"; do
    [[ -f "$idx" ]] || continue
    # skip if already listed
    grep -q "href=\"$slug.html\"\|href=\"blogs/$slug.html\"" "$idx" && { echo "already listed in $idx"; continue; }
    python3 - "$idx" <<PY
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
anchor = "<!-- BLOG_CARDS -->"
if anchor in s:
    s = s.replace(anchor, anchor + "\n" + '''$card''', 1)
    open(p, "w", encoding="utf-8").write(s)
    print("updated", p)
else:
    print("no BLOG_CARDS anchor in", p)
PY
  done
  echo "published: $slug  (commit & push to go live)"
  exit 0
fi

# ---- create mode ----
title="${1:?usage: ./new_blog.sh \"My Post Title\"}"
excerpt="${2:-}"
slug="$(slugify "$title")"
file="$BLOGS/$slug.html"
[[ -f "$file" ]] && die "post already exists: $file"

mkdir -p "$BLOGS"
cat > "$file" <<HTML
<!DOCTYPE html>
<html lang="en">

<head>

  <link rel="icon" type="image/png" href="../assets/img/logo.png"/>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">

  <title>$title — Daniel Liu</title>
  <meta content="$excerpt" name="description">

  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Raleway:300,300i,400,400i,500,500i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i" rel="stylesheet">

  <link href="../assets/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
  <link href="../assets/vendor/icofont/icofont.min.css" rel="stylesheet">
  <link href="../assets/vendor/remixicon/remixicon.css" rel="stylesheet">
  <link href="../assets/vendor/boxicons/css/boxicons.min.css" rel="stylesheet">

  <link href="../assets/css/style.css" rel="stylesheet">

</head>

<body>

  <video class="background-image" src="../assets/img/background/binary_rain.mp4" muted loop autoplay></video>

  <!-- ======= Header ======= -->
  <header id="header" class="header-tops">
    <div class="container">
      <h1><a href="../index.html">Daniel Liu</a></h1>
      <h2 style="color:#fff">I am <span class="typing" style="color:#12D640"></span></h2>
      <nav class="nav-menu d-none d-lg-block">
        <ul>
          <li><a href="../index.html"> <span>Home</span></a></li>
          <li class="active"><a href="index.html"> <span>Blog</span></a></li>
          <li><a href="../index.html#projects"> <span>Projects</span></a></li>
          <li><a href="../index.html#skills"> <span>Skills</span></a></li>
        </ul>
      </nav>
      <div class="social-links">
        <a href="mailto:rliu6915@163.com" target="_blank" class="google"><i class="bx bxl-google"></i></a>
        <a href="https://github.com/rliu6915" target="_blank" class="github"><i class="bx bxl-github"></i></a>
      </div>
    </div>
  </header>
  <!-- ======= End Header ======= -->

  <!-- ======= Post ======= -->
  <section id="post" class="blog-post">
    <div class="container">
      <div class="post-card" data-aos="fade-up">
        <h1>$title</h1>
        <span class="post-date">$TODAY</span>

        <p>Write your post here.</p>

      </div>
      <a href="index.html" class="back-link" style="text-align:center;display:block;">← Back to all posts</a>
    </div>
  </section>
  <!-- ======= End Post ======= -->

  <script src="../assets/vendor/jquery/jquery.min.js"></script>
  <script src="../assets/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
  <script src="../assets/vendor/jquery.easing/jquery.easing.min.js"></script>
  <script src="../assets/vendor/typed.js/typed.min.js"></script>
  <script type="text/javascript">
    var typed = new Typed('.typing',{
      strings: [ "an Engineer", "a Coder"],
      loop: true,
      typeSpeed: 65,
      backSpeed: 65
    });
  </script>
  <script src="../assets/js/main.js"></script>

</body>
</html>
HTML

echo "created: $file"
echo "next: edit it, then run  ./new_blog.sh --publish $slug"
