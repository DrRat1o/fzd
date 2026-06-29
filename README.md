# fzd

fuzzy file finder with a scoring system. type a partial name, get ranked
results back. the file you actually want shows up first.

## what it does

walks a directory tree and scores every file against your query. ranking
is based on match quality — a file where your query is a prefix scores
higher than one where it's buried somewhere in the middle. shorter,
more specific filenames win over long generic ones at the same match tier.

scoring tiers, strongest to weakest:
- exact match
- prefix match
- substring match
- subsequence (letters appear in order, not necessarily adjacent)

## why I built it

to understand how fuzzy matching works at the algorithm level. the core
idea — subsequence check as a gate, additive scoring on top — is simple
enough to fit in one file. building it was the point.

## install

```bash
git clone https://github.com/DrRat1o/fzd.git
cd fzd
pip install -e . --break-system-packages
```

## usage

```bash
fzd <query> [path]

--type file|dir|all   filter by type (default: all)
--limit N             cap results (default: 20)
--hidden              include dotfiles
--recent N            boost files modified in last N days
```

## examples

```bash
# find a file somewhere in a project
fzd walker ~/Documents/Projects/fzd

# only directories
fzd src . --type dir

# include dotfiles, search from home
fzd zshrc ~ --hidden

# recently modified python files
fzd model . --type file --recent 3

# pipe the top result into an editor
fzd main . --type file --limit 1 | xargs nvim
```

## internals

`scorer.py` — subsequence gate first, then tiered scoring with position
and length bonuses on top.

`walker.py` — recursive generator. yields paths one at a time, memory
usage stays flat regardless of directory size.

`display.py` — ANSI escape codes. matched characters highlighted in the
filename, directory prefix dimmed for readability.

## status

stable for personal use. config file for default flags is a possible
addition down the line.