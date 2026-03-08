#!/bin/bash

# Git 推送脚本 - 需要手动输入认证信息

cd /workspace/projects

echo "========================================="
echo "  推送代码到 GitHub"
echo "========================================="
echo ""
echo "仓库地址：https://github.com/lockskoub-star/yuanxiaoji"
echo ""
echo "========================================="
echo "  需要输入认证信息"
echo "========================================="
echo ""
echo "Username: lockskoub-star"
echo "Password: [粘贴你的 Personal Access Token]"
echo ""
echo "注意："
echo "  - Password 不是你的登录密码"
echo "  - Password 是你在 GitHub 生成的 Personal Access Token"
echo "  - Token 只显示一次，请确保已复制"
echo ""
echo "========================================="
echo ""

git push -u origin main
