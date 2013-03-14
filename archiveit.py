# -*- coding=utf-8 -*-

#将age大于4个月的文件打包
#打包格式，待选
#打包过的目录删除以节省空间
#对目录的删除必须使用完整的绝对路径，并且只能以专属文件夹为开头名
#必须log
#先完成测试部分的代码

#Debug 判断文件夹age，
#Info 对文件夹进行压缩
#Error 压缩失败，文件夹删除失败

import logging
import os
import subprocess
import sys
import shutil


class ArchiveDirectory(object):
    def __init__(self,dirname):
        self.dirname = dirname
        
        
    def _packit(self, pack_dirname, package_name):
        self.__7zipit(pack_dirname, package_name)
    
    def __7zipit(self, zip_dirname, zip_filename, stay_at_zip_parent_dir=True):
        """
        wrapper 7 zip for command line edition for packing.
        7z <command> [<switch>...] <base_archive_name> [<arguments>...]
        
        7z a archive1.zip subdir\

        adds all files and subfolders from folder subdir to archive archive1.zip.
        The filenames in archive !!will contain!! subdir\ prefix.

        7z a archive2.zip .\subdir\*

        adds all files and subfolders from folder subdir to archive archive2.zip. 
        The filenames in archive !!will not contain!! subdir\ prefix.

        Switches that can be used with this command
        -i (Include)
        -m (Method)
        -p (Set Password)
        -r (Recurse)
        -sfx (create SFX)
        -si (use StdIn)
        -so (use StdOut)
        -ssw (Compress shared files)
        -t (Type of archive)
        -u (Update)
        -v (Volumes)
        -w (Working Dir)
        -x (Exclude) 
        """
        bin_cmd = '7z'
        cmd = 'a'
        archive_type = '-tzip'
        recurse = '-r'
        zip_filename = ''.join(zip_filename, '.zip')
        zip_parent_dirname = os.path.dirname(zip_dirname)
        if stay_at_zip_parent_dir == True:
            zip_parent_dirname = os.path.dirname(zip_dirname)
            zip_filename = ''.join(zip_parent_dirname, os.sep, zip_filename)
        try:        
            subprocess.check_call([bin_cmd, cmd, archive_type, recurse, \
                                   zip_filename, zip_dirname])
            logging.debug('%s has been packed to %s' % \
                          (zip_dirname, zip_filename))
        except subprocess.CalledProcessError as cpe:
            logging.error('failed on packing %s.\n %s'% \
                          (zip_dirname, cpe.output))
            raise SystemError("failure happen at packing process.")
            
        
    def _removeit(self, dirname):
        try:
            if self.__dircheck(dirname) == True:
                shutil.rmtree(dirname)
        except Exception as err:
            logging.exception('removing %s failed.')
            
    def __dircheck(self, dirname):
        path = os.path.splitdrive(dirname)[1]
        path = path.lstrip(os.sep)
        pathcomps = path.split(os.sep)
        if (pathcomps[0].lower() != 'builds') and \
           ((pathcomps[1].lower() != 'applications') or \
            (pathcomps[1].lower() != 'components')):
            logging.error("remove operation denied! %s should not be touched."\
                          % dirname)
            return False
        if (pathcomps[3].lower() != 'auto'):
            logging.error("remove operation denied! Only the data under auto directory can be touched.")
            return False
        return True
    
    def archiveit(self):
        pass
    
    @property
    def dirname(self):
        return self._dirname
    
    @dirname.setter
    def dirname(self, dirname):
        if dirname != None:
            if sys.platform == 'win32':
                if dir[1] != ':':
                    logging.error('The directory name must be absolute path name.')
                    raise SystemError('The directory name must be absolute path name.')
            elif sys.platform == 'linux2':
                if dir[0] != os.sep:
                    logging.error('The directory name must be absolute path name.')
                    raise SystemError('The directory name must be absolute path name.')
            else:
                raise NotImplementedError()
            self._dirname = dirname
