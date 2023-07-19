import os
import vdf
import time 
import argparse
import requests
import traceback 
from multiprocessing.pool import ThreadPool
from multiprocessing.dummy import Pool, Lock

lock = Lock()

def depotkey_merge(config_path, depots_config):
    if not config_path.exists():
        with lock:
            print('config.vdf不存在')
        return
    with open(config_path, encoding='utf-8') as f:
        config = vdf.load(f)
    software = config['InstallConfigStore']['Software']
    valve = software.get('Valve') or software.get('valve')
    steam = valve.get('Steam') or valve.get('steam')
    if 'depots' not in steam:
        steam['depots'] = {}
    steam['depots'].update(depots_config['depots'])
    with open(config_path, 'w', encoding='utf-8') as f:
        vdf.dump(config, f, pretty=True)
    return True


def get(sha, path):
    url_list = [f'https://cdn.jsdelivr.net/gh/{repo}@{sha}/{path}',
                f'https://ghproxy.com/https://raw.githubusercontent.com/{repo}/{sha}/{path}']
    retry = 3
    while True:
        for url in url_list:
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    return r.content
            except requests.exceptions.ConnectionError:
                print(f'获取失败: {path}')
                retry -= 1
                if not retry:
                    print(f'超过最大重试次数: {path}')
                    raise


def get_file_list(sha, path, steam_path, app_id=None):
    try:
        if path == 'README.md':
            content = get(sha, path)
            with lock:
                tBody = content.decode(encoding='utf-8')
                print(f'文件内容: {path} ==> {tBody}')
            return
        
        print(f'文件名:{sha}   {path}')
    except KeyboardInterrupt:
        raise
    except:
        traceback.print_exc()
        raise
    return True


def main(app_id):
    url = f'https://api.github.com/repos/{repo}/branches/{app_id}'
    r = requests.get(url)
    if 'commit' in r.json():
        sha = r.json()['commit']['sha']
        url = r.json()['commit']['commit']['tree']['url']
        r = requests.get(url)
        if 'tree' in r.json():
            result_list = []
            with Pool(32) as pool:
                pool: ThreadPool
                for i in r.json()['tree']:
                    result_list.append(pool.apply_async(get_file_list, (sha, i['path'], "steam_path", app_id)))
                
                try:
                    while pool._state == 'RUN':
                        if all([result.ready() for result in result_list]):
                            break
                        time.sleep(0.1)
                except KeyboardInterrupt:
                    with lock:
                        pool.terminate()
                    raise
            if all([result.successful() for result in result_list]):
                print(f'入库成功: {app_id}')
                print('重启steam生效')
                return True
    print(f'入库失败: {app_id}')
    return False


parser = argparse.ArgumentParser()
parser.add_argument('-r', '--repo', default='steamdk/gameDownloadList')
parser.add_argument('-a', '--app-id', default='master')
parser.add_argument('-p', '--app-path')
args = parser.parse_args()
repo = args.repo
if __name__ == '__main__':
    try:
        if args.app_path:
            print(f' app_id: {args.app_path}')
        else:
            main(args.app_id or input('appid: '))
    except KeyboardInterrupt:
        exit()
    except:
        traceback.print_exc()
    if not args.app_id and not args.app_path:
        os.system('pause')