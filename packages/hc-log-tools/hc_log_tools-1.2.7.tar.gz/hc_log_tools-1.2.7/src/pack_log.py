"""This is the description.

  example: src/pack_log.py --prd_type=sort --time_range=100  --timestamp="2022-09-13 17:55:00" --log_root_dir=/tmp/66log
"""
from src.log_utility import *
from src.public import Public
import argparse
import tarfile
import os
from datetime import datetime
from alive_progress import alive_bar



def init_input_args(sub_parser):
    """解析shell传入的参数, 返回结果
    Returns:
        parser Namespace: 返回解析后的结果
    """
    # sub_parser.add_argument("--prd_type", help="产品类型：sort or pick", required=False)
    sub_parser.add_argument(
        "--time_range",
        type=int,
        help="希望抓取日志的有效时间范围：默认前后30分钟。截取的日志范围，距离时间点（--timestamp）前后多少分钟。",
        default=30,
        choices=range(1, 60),
        metavar="[1 ~ 60]",
    )
    sub_parser.add_argument("--log_root_dir", help="log 文件的根目录", required=True)
    sub_parser.add_argument(
        "--timestamp",
        help="时间点, 例如：2022-09-05 09:53:10。 默认为当前时间",
        default=datetime.now().strftime("%m-%d-%Y %:%M:%S"),
        required=True
    )

    sub_parser.add_argument(
        "--output_directory",
        help="输出文件的目录, 默认路径：/tmp/log_trans/",
        default="/tmp/log_trans/",
        required=False
    )
   
    # 添加参数 --not-up-to-cloud，当使用这个参数时，将 up_to_cloud 设置为 False
    sub_parser.add_argument(
        "--not-up-to-cloud",
        action='store_false',
        dest='up_to_cloud',  # 这里指定了dest，这意味着不管是 --not-up-to-cloud 还是 --up-to-cloud，都会影响 up_to_cloud 这个属性
        help="Do not automatically upload the compressed log files to the cloud.",
        required=False
    )

    # 添加参数 --up-to-cloud，显式启用上传功能
    sub_parser.add_argument(
        "--up-to-cloud",
        action='store_true',
        dest='up_to_cloud',  # 确保这里使用的是同一个目的地（dest），这样两个选项可以互相覆盖
        help="Automatically upload the compressed log files to the cloud if specified.",
        required=False
    )
    # DON'T want to allow --feature and --no-feature at the same time
    feature_recursive_parser = sub_parser.add_mutually_exclusive_group(required=False)
    feature_recursive_parser.add_argument('--recursive', dest='recursive', action='store_true', help='递归处理log文件目录的子目录, 默认激活该选项')
    feature_recursive_parser.add_argument('--no-recursive', dest='recursive', action='store_false', help='不处理log文件目录的子目录')
    sub_parser.set_defaults(recursive=True)

    feature_compress_parser = sub_parser.add_mutually_exclusive_group(required=False)
    feature_compress_parser.add_argument('--compress', dest='compress', action='store_true', help="压缩输出文件, 默认激活该选项")
    feature_compress_parser.add_argument('--no-compress', dest='compress', action='store_false', help="不压缩输出文件")
    sub_parser.set_defaults(compress=True)

    return sub_parser


def init_input_args_warp(sub_parser):
    res_parser = init_input_args(sub_parser)
    return res_parser.parse_args()


def pack_log(input_args):
    """找到指定的log，并打包
    Args:
        input_args: shell 传入的参数
    """
    preprocessing_output_directory(input_args.output_directory)

    print(f"input_args.recursive: {input_args.recursive}")
    log_files = set(
        get_file_in_time_range(
            input_args, download_log=True, recursive=input_args.recursive
        )
    )

    print(f"\r\nlog_files: {log_files}")

    if len(log_files) == 0:
        print("no log files in range")
        return

    print(f"\r\ntotlal {len(log_files)} files, compress start ...")

    # get current datetime like 20210913175500
    cur_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    # get system hostname
    hostname = os.popen("hostname").read().strip()
    output_file_name = f"{hostname}-{cur_datetime}.log.tar.gz"
    # join args.output_directory and OUTPUT_FILE_NAME
    output_file_path = os.path.join(input_args.output_directory, output_file_name)
    Public.output_file_path = output_file_path


    # if input_args.compress, tar with gzip
    if input_args.compress:
        with alive_bar(len(log_files),  title='pack with compress') as bar:
            with tarfile.open(output_file_path, "w:gz") as tar:
                for log_file in log_files:
                    try:
                        tar.add(log_file)
                        bar()
                    except FileNotFoundError:
                        print(f"file {log_file} is not exist")

    # else, tar without gzip
    else:
        with alive_bar(len(log_files),  title='pack without compress') as bar:
            with tarfile.open(output_file_path, "w") as tar:
                for log_file in log_files:
                    try:
                        tar.add(log_file)
                        bar()
                    except FileNotFoundError:
                        print(f"file {log_file} is not exist")

    # terminal process bar for compress with alive-progress
    # show the output file size with MB, precision=2
    print(f"compress finished, output file: {output_file_path}, size: {os.path.getsize(output_file_path) / 1024 / 1024:.2f} MB")
    # if input_args.not_up_to_cloud:  # 判断是否设置了 --up-to-cloud 参数
    #     print(f'output_file_path: {Public.output_file_path}') #判断选项是否包含--up-to-cloud，没有则抛出错误及打印压缩文件路径和文件名称

    # else:
    #     upload_to_obs(output_file_path)
    if input_args.up_to_cloud:
        upload_to_obs(output_file_path)
    else:
        print(f"Cloud upload disabled. Output file path: {Public.output_file_path}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    input_args = init_input_args_warp(parser)
   