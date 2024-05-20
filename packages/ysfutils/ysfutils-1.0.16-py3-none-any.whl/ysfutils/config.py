import json
import os
from pathlib import Path

from box import Box

from ysfutils.github import Repository
from ysfutils.mongo import MongoClient
from ysfutils.sqlites import Sqlite3Client


class Config:
    """ 合并sqlite数据库中的配置, 生成最终的配置字典

    Notes:
        1. 必须有RUN_ENV环境变量, 该变量是个dict的字符串, 包含的键值如下：
            {
                "github_owner": "xxxx",
                "github_repo": "xxxx",
                "github_token": "xxxx",
                "mongo": "['xxxx']",
                "run_job": "['funxxxxds']",
                "path": {
                    "show": "['/xxxx/xxxx/xxxx/xxxx']",
                    "no_show": "[]"
                },
                "sqlite3": {
                    "db": "xxxx.db",
                    "pwd": "xxxx.txt",
                    "path": "/xxxx/xxxx/xxxx/xxxx"
                }
            }
        2. 所有配置都在sqlite数据库中名字以_config结尾的各个表中存储
        3. MongoDB的证书文件存放路径和sqlite数据库文件所在路径平级

    """

    def __init__(self, env_name: str = "RUN_ENV", config_table_list: None | list = None):
        """

        Args:
            env_name: 环境变量名
            config_table_list: 不传该参数时, 获取所有名字以_config结尾的表

        """
        # 获取运行时参数
        self.__run_env_dict = eval(os.getenv(f"{env_name}")) if os.getenv(f"{env_name}") else {}
        self.__config_table_list = config_table_list

    @property
    def all_config(self):
        path_config = self.__makedirs(self.__run_env_dict.get("path", {}))
        db_config = self.__get_config_from_sqlite3()
        all_config = {**path_config, **db_config}

        return Box(dict(sorted(all_config.items())), frozen_box=True)

    @staticmethod
    def __makedirs(path_dict: dict) -> dict:
        """ 根据run_env的path中的内容创建相关目录并返回相关结果

        Notes:
            1. path_dict最多包含两个key, show表示这个路径需要放到const中, no_show不需要, value都是包含路径的list

        Args:
            path_dict: run_env环境变量中的path内容

        Returns:
            {"文件夹名": "文件夹路径"....}

        """
        result = {"path": {}}
        for is_show, path_list in path_dict.items():
            for path in eval(path_list):
                path_name = Path(path).stem
                os.makedirs(path, exist_ok=True)
                if is_show == "show":
                    result["path"][path_name] = path
        return result

    def __get_config_from_sqlite3(self) -> dict:
        """ 从本地sqlite3数据库的配置表中获取配置

        Notes:
            sqlite数据库中各参数表的表结构只有value一个字段, 内容为json字符串

        """
        all_config_from_db = {}

        mongo_db_list = eval(self.__run_env_dict.get("mongo", "[]"))
        run_job_list = eval(self.__run_env_dict.get("run_job", "[]"))

        sqlite3_db_path = self.__run_env_dict.get("sqlite3", {}).get("path", "")
        sqlite3_db_file, sqlite3_db_passwd_file = self.__get_configdb(sqlite3_db_path)
        with open(sqlite3_db_passwd_file, "r", encoding="utf-8") as file:
            db_passwd = file.read().rstrip("\n")
        client = Sqlite3Client(sqlite3_db_file, db_passwd)

        # 如果config_table_list入参的值为None, 则以sqlite数据库中所有以_config结尾的表名作为值
        if self.__config_table_list is None:
            get_table_name_sql = 'select name from sqlite_master where name like "%_config"'
            query_result = client.find(get_table_name_sql, multi=True)
            config_table_list = [table_set[0] for table_set in query_result]
        else:
            config_table_list = self.__config_table_list

        for table_name in config_table_list:
            sql = f'select value from {table_name}'
            config = json.loads(client.find(sql, multi=False)[0])
            if table_name == "mongodb_config" and mongo_db_list and isinstance(mongo_db_list, list):
                mongo_config = {"mongo_client": self.__get_mongo_config(config, mongo_db_list)}
                all_config_from_db = dict(**all_config_from_db, **mongo_config)
                continue
            elif table_name == "run_job_config" and run_job_list and isinstance(run_job_list, list):
                run_job_config = self.__get_run_jobs(config, run_job_list)
                all_config_from_db = dict(**all_config_from_db, **run_job_config)
                continue
            all_config_from_db = dict(**all_config_from_db, **config)

        return all_config_from_db

    def __get_configdb(self, sqlite3_db_path: str) -> tuple[str, str]:
        """ 从本地或github私有仓库获取config.db文件路径和对应的密码

        Args:
            sqlite3_db_path: 数据库文件所在的文件夹

        Returns:
            config.db文件的路径和passwd文件的内容

        """
        os.makedirs(sqlite3_db_path, exist_ok=True)
        github_repo_owner = self.__run_env_dict.get("github_owner", "")
        github_repo_name = self.__run_env_dict.get("github_repo", "")
        github_token = self.__run_env_dict.get("github_token", "")

        db_file_name = self.__run_env_dict.get("sqlite3", {}).get("db", "")
        db_passwd_file_name = self.__run_env_dict.get("sqlite3", {}).get("pwd", "")

        db_file = os.path.join(sqlite3_db_path, db_file_name)
        db_passwd_file = os.path.join(sqlite3_db_path, db_passwd_file_name)
        if not os.path.exists(db_file) and not os.path.exists(db_passwd_file):
            repo = Repository(github_repo_owner, github_repo_name, github_token=github_token)
            # 下载文件到本地
            _ = repo.download_file(db_file_name, sqlite3_db_path)
            _ = repo.download_file(db_passwd_file_name, sqlite3_db_path)
        return db_file, db_passwd_file

    def __get_mongo_config(self, mongo_config_from_sqlite: dict, mongo_db_list: list) -> dict:
        """ 创建指定MongoDB数据库的client

        Args:
            mongo_config_from_sqlite: dict, 从sqlite3数据库mongodb_config表中读取的数据
            mongo_db_list: 需要使用的MongoDB数据库

        Returns:
            {
                "mongo_client": {
                    "数据库1名字": MongoClient1,
                    "数据库2名字": MongoClient2
                }
            }

        """
        result = {}
        for db_name in mongo_db_list:
            db_info = mongo_config_from_sqlite["db"][db_name]
            if db_info:
                # 如果certs的内容不为空, 则生成证书
                cert_name = db_info["cert"]
                if cert_name:
                    client_cert, _, ca_cert = self.__generate_mongo_cert(
                        db_name, mongo_config_from_sqlite["certs"][cert_name]
                    )
                    # 生成client
                    url = db_info['url']
                    result[db_name] = MongoClient(url, client_cert=client_cert, ca_cert=ca_cert).get_client()
        return result

    def __generate_mongo_cert(self, db_name: str, certs_str_dict: dict) -> tuple[str, str, str]:
        """ 从sqlite数据库里读取证书内容, 生成MongoDB的证书文件并返回路径

        Args:
            db_name (str): 数据库名称
            certs_str_dict (dict): 字典内容为各证书内容的字符串

        Returns:
            客户端证书路径, 服务器端证书路径, ca证书路径
        """
        # 证书目录与sqlite3目录平级
        sqlite3_db_path = self.__run_env_dict.get("sqlite3", {}).get("path", "")
        certs_path = os.path.join(os.path.dirname(sqlite3_db_path), "certs")

        # 读取三个证书的内容
        client_pem_str = certs_str_dict['client_pem']
        server_pem_str = certs_str_dict['server_pem']
        ca_crt_str = certs_str_dict['ca_crt']

        # 写入本地文件
        client_pem_file_path = os.path.join(certs_path, f"{db_name}_client.pem")
        server_pem_file_path = os.path.join(certs_path, f"{db_name}_server.pem")
        ca_crt_file_path = os.path.join(certs_path, f"{db_name}_ca.crt")
        self.__write_mongo_cert_file(client_pem_file_path, client_pem_str)
        self.__write_mongo_cert_file(server_pem_file_path, server_pem_str)
        self.__write_mongo_cert_file(ca_crt_file_path, ca_crt_str)

        return client_pem_file_path, server_pem_file_path, ca_crt_file_path

    @staticmethod
    def __write_mongo_cert_file(cert_file_path: str, cert_file_content: str):
        """ 写入证书文件, 存在时则跳过

        Args:
            cert_file_path: 文件绝对路径
            cert_file_content: 文件内容

        """
        file_path, file_name = os.path.split(cert_file_path)[0], os.path.split(cert_file_path)[1]
        os.makedirs(file_path, exist_ok=True)
        if not list(Path(file_path).rglob(file_name)):
            with open(cert_file_path, 'w') as cf:
                cf.writelines(cert_file_content)

    @staticmethod
    def __get_run_jobs(run_job_config_from_sqlite: dict, run_job_list: list) -> dict:
        """ 删除不需要的job

        Args:
            run_job_config_from_sqlite (dict): 从sqlite数据库表run_job_config读出的数据
            run_job_list: 需要运行的job

        Returns:
            {
                "run_jobs": {
                    "job1": {},
                    "job2": {},
                }
            }

        """
        run_job_config = {"run_jobs": {}}
        # 从run_jobs中删除不需要的job
        for job_name in run_job_list:
            for key, value in run_job_config_from_sqlite["run_jobs"].items():
                if key == job_name:
                    run_job_config["run_jobs"] = value
        return run_job_config


class CustomizeLogger:
    """ 全局logger """

    def __init__(self, log_file: str, format_str: str = '', rotation: str = '20 MB', compression: str = 'zip'):
        self.__log_file_path = log_file
        if format_str:
            self.__log_format_str = format_str
        else:
            self.__log_format_str = '[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level}</level> ' \
                                    '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>]: ' \
                                    '<level>{message}</level>'
        self.__rotation = rotation
        self.__compression = compression
        self.my_logger = self.__customize_logger()

    def __customize_logger(self):
        """ 定义logger """
        from loguru import logger
        logger.add(
            self.__log_file_path,
            format=self.__log_format_str,
            rotation=self.__rotation,
            compression=self.__compression,
            backtrace=False
        )
        return logger
