#!/usr/bin/env bash
set -e
cd /d/AI-plat-form/01-githubcode/WeKnora
git add -A
git commit -m 'chore: clean temp scripts, update frontend i18n and login, add deploy scripts'
git push origin dev
