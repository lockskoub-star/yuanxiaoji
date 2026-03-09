#!/usr/bin/env python3
"""
Railway 部署前检查工具
检查项目配置是否满足 Railway 部署要求
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    if filepath.exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} 未找到: {filepath}")
        return False

def check_env_vars():
    """检查环境变量"""
    print("\n🔍 环境变量检查:")
    print("=" * 50)

    required_vars = [
        ("COZE_WORKLOAD_IDENTITY_API_KEY", "Coze API 密钥"),
        ("COZE_INTEGRATION_MODEL_BASE_URL", "Coze 基础 URL"),
    ]

    all_present = True
    for var_name, description in required_vars:
        value = os.getenv(var_name)
        if value:
            print(f"✅ {var_name} ({description})")
        else:
            print(f"❌ {var_name} ({description}) - 未设置")
            all_present = False

    return all_present

def check_git_repo():
    """检查 Git 仓库"""
    print("\n🔍 Git 仓库检查:")
    print("=" * 50)

    if (PROJECT_ROOT / ".git").exists():
        print(f"✅ Git 仓库存在: {PROJECT_ROOT}")

        # 检查远程仓库
        import subprocess
        try:
            result = subprocess.run(
                ["git", "remote", "-v"],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✅ 远程仓库配置:\n{result.stdout}")
                return True
        except Exception as e:
            print(f"⚠️  无法获取远程仓库信息: {e}")
            return False
    else:
        print(f"❌ 不是 Git 仓库: {PROJECT_ROOT}")
        return False

def main():
    print("🚀 Railway 部署前检查")
    print("=" * 50)

    # 检查必要文件
    print("\n🔍 必要文件检查:")
    print("=" * 50)

    required_files = [
        (PROJECT_ROOT / "Dockerfile", "Dockerfile"),
        (PROJECT_ROOT / "Procfile", "Procfile"),
        (PROJECT_ROOT / "railway.toml", "Railway 配置"),
        (PROJECT_ROOT / "requirements.txt", "Python 依赖"),
        (PROJECT_ROOT / "src", "源代码目录"),
        (PROJECT_ROOT / "config", "配置目录"),
    ]

    files_ok = all(check_file_exists(path, desc) for path, desc in required_files)

    # 检查环境变量
    env_ok = check_env_vars()

    # 检查 Git 仓库
    git_ok = check_git_repo()

    # 总结
    print("\n" + "=" * 50)
    print("📊 检查结果:")
    print("=" * 50)

    if files_ok and git_ok:
        print("✅ 项目文件检查通过")
    else:
        print("❌ 项目文件检查失败")

    if env_ok:
        print("✅ 环境变量配置正确")
    else:
        print("⚠️  环境变量未配置（需要在 Railway 中配置）")

    print("\n" + "=" * 50)
    print("📝 部署建议:")
    print("=" * 50)

    if not env_ok:
        print("\n⚠️  重要提示:")
        print("   以下环境变量必须在 Railway 中配置:")
        print("   1. COZE_WORKLOAD_IDENTITY_API_KEY")
        print("   2. COZE_INTEGRATION_MODEL_BASE_URL")
        print("\n   在 Railway 控制台的 'Variables' 标签中添加这些变量")

    if files_ok and git_ok:
        print("\n✅ 项目已准备好部署到 Railway!")
        print("   下一步:")
        print("   1. 访问 https://railway.app")
        print("   2. 创建新项目并连接 GitHub 仓库")
        print("   3. 配置环境变量")
        print("   4. 部署并测试")
    else:
        print("\n❌ 项目还未准备好部署")
        print("   请修复上述问题后再次检查")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
