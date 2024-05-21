import io
import tqdm
from concurrent.futures import ThreadPoolExecutor
from threading import Semaphore, Thread
from split_file_reader.split_file_writer import SplitFileWriter
from split_file_reader import SplitFileReader
import base64
import dropbox
import requests
from dropboxdrivefs import DropboxDriveFileSystem
from fsspec.implementations.dirfs import DirFileSystem
from ..base import FileSystem
from .config import DropboxConfig
from .util import Pipe

__all__ = ['DropboxBackend']


class MyDropboxFS(DropboxConfig, DropboxDriveFileSystem):
    def connect(self):
        """ connect to the dropbox account with the given token
        """
        self.dbx = dropbox.Dropbox(
            app_key=self.app_key,
            app_secret=self.app_secret,
            oauth2_refresh_token=self.refresh_token
        )
        self.token = self.refresh_token
        self.session = requests.Session()
        self.session.auth = ("Authorization", self.token)

    def copy(self, path1, path2, recursive=True, **kwargs):
        if isinstance(path1, list):
            for file_path in path1:
                assert not file_path.endswith(
                    '/'), 'multiple file copy should takes files as input'
                self.copy(file_path, path2)
        else:
            if path1.endswith('/') and path2.endswith('/'):
                assert recursive, 'recursive should be True for folder copying'
                if not self.exists(path2[:-1]):
                    self.dbx.files_copy(path1[:-1], path2[:-1])
                else:
                    self.rm(path2[:-1], recursive=True)
                    self.dbx.files_copy(path1[:-1], path2[:-1])
            elif path2.endswith('/'):
                self.dbx.files_copy(path1, path2 + path1.split('/')[-1])
            else:
                self.dbx.files_copy(path1, path2)

    def cp_file(self, path1, path2, **kwargs):
        assert not path1.endswith('/'), f'{path1} is not a file'
        assert not path2.endswith('/'), f'{path2} is not a file'
        self.dbx.files_copy(path1, path2)


limit_pool = Semaphore(value=8)


class DropboxBackend(FileSystem):
    """
    Storage object with IO interface left abstract
    """

    def __init__(self, directory='/', chunksize=2000000):
        assert directory.startswith('/')
        root_fs = MyDropboxFS(token='')
        super().__init__(DirFileSystem(directory, root_fs))
        self._chunksize = chunksize

    def upload_core(self, file_obj: io.BytesIO, remote_path: str):
        """Upload file object

        Args:
            file_obj (io.BytesIO): file to be upload
            remote_path (str): remote file path
        """
        self._upload_core(file_obj, remote_path)
        self._check_upload_success(file_obj, remote_path)
        file_obj.flush()
        file_obj.close()

    def _check_upload_success(self, file_obj: io.BytesIO, remote_path: str):
        download_data = self.download_core(remote_path)
        download_data.seek(0)
        file_obj.seek(0)
        assert download_data.getbuffer() == file_obj.getbuffer(), 'upload before != after'
        download_data.flush()
        download_data.close()

    def _upload_core(self, file_obj: io.BytesIO,
                     remote_path: str, max_workers=8, chunk_size=1000000):
        """Upload file object to local storage

        Args:
            file_obj (io.BytesIO): file to be upload
            remote_path (str): remote file path
        """
        assert '.' in remote_path, f'requires file ext .xxx provided in `remote_path` but it is {remote_path}'
        file_name = remote_path.split('.')[0]
        ext = remote_path.split('.')[1]
        if self._fs.exists(file_name):
            self._fs.rm(file_name)
        self._fs.mkdir(file_name)
        file_obj.seek(0)
        chunk_cnt = file_obj.getbuffer().nbytes // chunk_size + 1
        assert self._fs.exists(file_name), f'{file_name} folder make failed'
        dfs = DirFileSystem(f'/{file_name}', self._fs)
        pipe = Pipe(max_workers)
        thread = Thread(target=self._upload_all,
                        args=(dfs, ext, pipe, max_workers, chunk_cnt, remote_path))
        thread.start()

        def gen(pipe):
            while True:
                buff = io.BytesIO()
                pipe.send_input(buff)
                yield buff
        with SplitFileWriter(gen(pipe), chunk_size) as sfw:
            sfw.write(file_obj.getbuffer())
        pipe.close()
        thread.join()

    def _upload_all(self, dfs, ext, pipe, max_workers, chunk_cnt, remote_path):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            input_pipe = enumerate(pipe.generate_output())
            output_pipe = executor.map(
                lambda x: self._upload_chunk(dfs, ext, x[0], x[1]),
                input_pipe)
            output = list(
                tqdm.tqdm(
                    output_pipe,
                    total=chunk_cnt,
                    desc=f'Upload {remote_path}'))
        total_size = len(output)
        print('number of chunks:', total_size)
        with dfs.open('total.txt', 'w') as f:
            f.write(str(total_size))
        print(f'Done upload {total_size} files')

    def _upload_chunk(self, dfs, ext, index, chunk):
        chunk.seek(0)
        with dfs.open(f'{index}.{ext}', 'w') as f:
            data = base64.b64encode(chunk.read()).decode()
            f.write(data)
        chunk.flush()
        chunk.close()

    def download_core(self, remote_path: str) -> io.BytesIO:
        """Download file from remote storage

        Args:
            remote_path (str): remote file path

        Returns:
            io.BytesIO: downloaded file
        """
        assert '.' in remote_path, f'requires file ext .xxx provided in `remote_path` but it is {remote_path}'
        file_name = remote_path.split('.')[0]
        ext = remote_path.split('.')[1]
        assert self._fs.exists(
            f'{file_name}'), f'{file_name} folder does not exists for FileSystem: {self._fs}'
        dfs = DirFileSystem(file_name, self._fs)
        with dfs.open('total.txt', 'r') as f:
            total_size = int(f.read())
        max_workers = 32
        pipe = Pipe(max_workers)
        pipe.set_total_size(total_size)
        print(f'Start download {total_size} files')
        thread = Thread(
            target=self._download_all,
            args=(dfs, ext, pipe, max_workers, total_size, remote_path)
        )
        thread.start()
        with SplitFileReader(pipe) as sfw:
            result = io.BytesIO(sfw.read())
        thread.join()
        print(f'Done download {total_size} files')
        result.seek(0)
        return result

    def _download_all(self, dfs, ext, pipe, max_workers,
                      chunk_cnt, remote_path):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            input_pipe = range(chunk_cnt)
            input_pipe = map(lambda index: (dfs, index, ext), input_pipe)
            chunks = executor.map(self._download_chunk, input_pipe)
            chunks = tqdm.tqdm(
                chunks,
                desc=f'Download {remote_path}',
                total=chunk_cnt
            )
            pipe.load_input(chunks)

    def _download_chunk(self, x):
        dfs, index, ext = x
        with dfs.open(f'{index}.{ext}', 'r') as f:
            chunk = io.BytesIO(base64.b64decode(f.read()))
        return chunk

    def check_exists(self, remote_path: str) -> bool:
        assert '.' in remote_path, f'requires file ext .xxx provided in `remote_path` but it is {remote_path}'
        file_name = remote_path.split('.')[0]
        return self._fs.exists(file_name)

    def drop_file(self, remote_path: str):
        assert '.' in remote_path, f'requires file ext .xxx provided in `remote_path` but it is {remote_path}'
        file_name = remote_path.split('.')[0]
        try:
            return self._fs.rm(file_name)
        except FileNotFoundError:
            pass

    def copy_file(self, src_file: str, dest_file):
        assert '.' in src_file, f'requires file ext .xxx provided in `src_file` but it is {src_file}'
        assert '.' in dest_file, f'requires file ext .xxx provided in `dest_file` but it is {dest_file}'
        self.drop_file(dest_file)
        src_file = src_file.split('.')[0]
        dest_file = dest_file.split('.')[0]
        self._fs.cp(src_file, dest_file, recursive=True)
