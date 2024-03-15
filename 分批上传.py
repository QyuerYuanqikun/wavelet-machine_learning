import os
import subprocess
import sys
from git import Repo

# Windows平台上，设置环境变量，强制Python使用UTF-8读写文件。
# if sys.platform == 'win32':
#     os.environ['PYTHONIOENCODING'] = 'utf-8'

def remove_deleted_files(repo_path):
    os.chdir(repo_path)
    # 获取所有被删除的文件
    deleted_files = subprocess.check_output(['git', 'ls-files', '--deleted'], encoding='utf-8').splitlines()
    for file_path in deleted_files:
        # 在这里，我们确保没有将文件名包含在引号内。
        # subprocess会负责正确处理空格和非ASCII字符。
        try:
            subprocess.run(['git', 'rm', '--cached', file_path], check=True, encoding='utf-8')
        except subprocess.CalledProcessError as e:
            print(f"Error removing file: {file_path}")
            print(e)


def get_all_changed_files(repo_path):
    """获取所有已修改（包括未跟踪的）文件的列表及其大小"""
    os.chdir(repo_path)  # 确保在获取文件大小前切换到仓库路径
    changed_files_with_status = subprocess.check_output(['git', 'ls-files', '--modified', '--others', '--exclude-standard', '-z'], encoding='utf-8')
    changed_files = changed_files_with_status.strip('\x00').split('\x00')
    files_and_sizes = []
    for file in changed_files:
        if file:  # 确保不是空字符串
            full_path = os.path.join(repo_path, file.replace('/', os.sep))
            if os.path.exists(full_path):  # 确保文件存在
                size = os.path.getsize(full_path)
                files_and_sizes.append((file, size))
            else:
                print(f"文件不存在，已跳过: {full_path}")
    return files_and_sizes


def commit_and_push_files(repo_path, files, commit_message):
    """添加、提交并推送一批文件"""
    os.chdir(repo_path)  # 确保在执行git命令前在正确的工作目录
    for file in files:
        subprocess.run(['git', 'add', file], check=True)
    subprocess.run(['git', 'commit', '-m', commit_message], check=True)
    subprocess.run(['git', 'push'], check=True)

def batch_process_files(repo_path, commit_message, max_batch_size=50 * 1024 * 1024):
    """按文件大小分批处理和推送文件"""
    remove_deleted_files(repo_path)  # 移除已删除的文件
    all_files_and_sizes = get_all_changed_files(repo_path)
    batch_files = []
    current_batch_size = 0
    batch_number = 0

    for file, size in all_files_and_sizes:
        if current_batch_size + size > max_batch_size and batch_files:
            batch_commit_message = f"{commit_message} (Batch {batch_number + 1})"
            commit_and_push_files(repo_path, batch_files, batch_commit_message)
            print(f"Batch {batch_number + 1} committed and pushed.")
            batch_files = []
            current_batch_size = 0
            batch_number += 1

        batch_files.append(file)
        current_batch_size += size

    if batch_files:
        batch_commit_message = f"{commit_message} (Batch {batch_number + 1})"
        commit_and_push_files(repo_path, batch_files, batch_commit_message)
        print(f"Batch {batch_number + 1} committed and pushed.")

if __name__ == "__main__":
    repo_path = input("请输入你的仓库路径: ").strip()
    commit_message = input("请输入commit信息: ").strip()
    max_batch_size = int(input("请输入每批处理的最大文件大小（以字节为单位），例如500MB就直接输入524288000: ").strip())

    batch_process_files(repo_path, commit_message, max_batch_size)
