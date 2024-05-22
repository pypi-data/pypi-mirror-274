#!/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright (c) 2020 growingio.com, Inc.  All Rights Reserved


"""
用户属性
"""
import argparse
import os
import pathlib
import sys

sys.path.append(str(pathlib.Path(os.path.abspath(__file__)).parent.parent))
from importers.data_import.data_events import events_import
from importers.data_import.data_user_variable import user_variables_import
from importers.common.common_util import get_all_file
from importers.common.log_util import logger
from importers.meta.data_center import getTunnels
from importers.data_import.data_item_variable import item_variables_import

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m',
                        help='必填参数. 用户属性数据导入:user_variables，用户行为数据导入:events，维度表数据导入:item_variables.',
                        required=True,
                        default='',
                        type=str)
    parser.add_argument('-p', '--path',
                        help='必填参数. 需要导入的数据所在的路径',
                        required=True,
                        default='',
                        type=str)
    parser.add_argument('-ds', '--datasource_id',
                        help='必填参数. 数据源ID.',
                        required=False,
                        default='',
                        type=str)
    parser.add_argument('-f', '--format',
                        help='可选参数. 导入数据格式,目前支持JSON,CSV,TSV三种格式.',
                        default='JSON',
                        type=str)
    parser.add_argument('-item_key',
                        help='必填参数. item_key',
                        required=False,  # 根据-m参数判断是否必填
                        default='',
                        type=str)
    # 暂时取消
    parser.add_argument('-d', '--debug',
                        help='可选参数. True-导入数据全量校验但不导,false-立即创建导入任务进入导入队列.',
                        default=True)
    parser.add_argument('-s', '--event_start',
                        help='可选参数. 数据起始时间,导入用户行为数据时指定',
                        default='',
                        type=str)
    parser.add_argument('-e', '--event_end',
                        help='可选参数. 数据结束时间,导入用户行为数据时指定',
                        default='',
                        type=str)
    parser.add_argument('-qf', '--qualifier',
                        help='可选参数. 文本限定符.',
                        default='"',
                        type=str)
    parser.add_argument('-sep', '--separator',
                        help='可选参数. 文本分割符.',
                        default='',
                        type=str)
    parser.add_argument('-skh', '--skip_header',
                        help='可选参数. 设置则自动跳过首行.',
                        action='store_true')
    parser.add_argument('-attr', '--attributes',
                        help='可选参数. 导入文件的各列按顺序映射到属性名，英文逗号分隔.',
                        default='',
                        type=str)
    parser.add_argument('-j', '--jobName',
                        help='可选参数. 可以更改默认jobName',
                        default='',
                        type=str)
    parser.add_argument('-c', '--clear',
                        help='可选参数. True-导入数据成功后清理掉FTP上数据,False-导入数据成功后不清理掉FTP上数据.',
                        default=False)
    parser.add_argument('-v', '--version', action='version', version='Gio_DataImporter_1.0')
    args = parser.parse_args()
    return args.__dict__


def main():
    # Step one: 解析命令行参数
    args = parse_args()
    logger.debug(f"解析命令行参数: {args}")
    # Step one: 校验基础参数,并预处理参数
    # 1. 校验导入文件
    p = args.get('path')
    ps = []
    if os.path.exists(p):
        ps.extend(get_all_file(p))
    else:
        logger.error("需要导入的数据文件不存在")
        return
    args['path'] = ps
    # 2. 校验Debug参数
    # 暂时取下
    d = str(args.get('debug')).upper()
    if 'TRUE'.__eq__(d):
        d = True
    elif 'FALSE'.__eq__(d):
        d = False
    else:
        logger.error("[-d/--debug]参数值不对")
        return
    args['debug'] = d
    # 3. 校验数据格式
    f = str(args.get('format')).upper()
    if 'JSON'.__eq__(f) is False and 'CSV'.__eq__(f) is False and 'TSV'.__eq__(f) is False:
        logger.error("目前支持JSON,CSV,TSV三种格式")
        return
    args['format'] = f
    # 4. 校验数据源
    m = args.get('m')
    if 'user_variables'.__eq__(m) or 'events'.__eq__(m):
        tunnels = getTunnels()
        if args.get('datasource_id') not in tunnels:
            logger.error("数据源不存在")
            return
        args['datasource_id'] = [args.get('datasource_id'), tunnels[args.get('datasource_id')]]
    # Step three:  按导入模块处理
    if 'user_variables'.__eq__(m):
        user_variables_import(args)
    elif 'events'.__eq__(m):
        events_import(args)
    elif 'item_variables'.__eq__(m):
        item_variables_import(args)
    else:
        logger.warn("目前只支持用户行为数据、用户属性数据导入和维度表导入")
        return


if __name__ == '__main__':
    logger.info("Data Importer Start")
    main()
    logger.info("Data Importer Finish")
