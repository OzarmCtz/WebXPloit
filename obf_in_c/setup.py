import os
import shutil
import subprocess

class ObfInC:
    def __init__(self) -> None:
        self.obf_in_c_dir = '.' 
        #### WEBXPLOIT ####
        self.code_dir = os.path.join(self.obf_in_c_dir, 'WebXploitBackend')
        self.webxploit_dir = os.path.join(self.obf_in_c_dir, '../backend', 'WebXPloitBackend')
        #### WEBXPLOIT ####
        
        
        #### WEBXPLOIT API ####
        self.code_dir_api = os.path.join(self.obf_in_c_dir, 'WebXploitApi')
        self.webxploit_api_dir = os.path.join(self.obf_in_c_dir, '../api', 'WebXploitApi')
        #### WEBXPLOIT API ####
    
    def run(self):
        #### WEBXPLOIT ####
        self.clean_directory(self.code_dir)
        self.copy_project(self.webxploit_dir, self.code_dir , ['api', 'tmp', 'result' , 'database' , 'tools' , '.vscode'  , '.pytest_cache'])
        self.convert_py_to_pyx(self.code_dir)
        self.push_file_obf(f'{self.code_dir}/setup.py')
        self.create_launch_file(self.code_dir , 'run')
        #### WEBXPLOIT ####
        
        
        #### WEBXPLOIT API ####
        self.clean_directory(self.code_dir_api)
        self.copy_project(self.webxploit_api_dir, self.code_dir_api , ['log' , 'result' , 'tests' , 'utils/vuln/git/dump' , '.vscode' , '.pytest_cache' , 'docs'])
        self.convert_py_to_pyx(self.code_dir_api)
        self.push_file_obf(f'{self.code_dir_api}/setup_api.py')
        self.create_launch_file(self.code_dir_api , 'router')
        #### WEBXPLOIT API ####
        
    def clean_directory(self , path):
        try:
            if not os.path.exists(path):
                return
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(path)
        except Exception as e:
            print(f'clean_directory / error occured : {e}')
            
    def copy_project(self , src, dst , patterns):
        try:
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*patterns))
        except Exception as e:
            print(f'copy_project / error occured : {e}')
            
    def convert_py_to_pyx(self , path):
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith('.py') and file != '__init__.py':
                        py_path = os.path.join(root, file)
                        pyx_path = os.path.splitext(py_path)[0] + '.pyx'
                        os.rename(py_path, pyx_path)
        except Exception as e:
            print(f'convert_py_to_pyx / erroc occured : {e}')
 
    def push_file_obf(self , file_path):

        setup_content = """
# -*- coding: utf-8 -*-
from setuptools import setup
from Cython.Build import cythonize
import os

def find_pyx_files(path='.'):
    pyx_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.pyx'):        
                pyx_files.append(os.path.join(root, file))
    return pyx_files

    
pyx_files = find_pyx_files()

setup(ext_modules = cythonize(pyx_files))


def remove_pyx_files(path='.'):
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith('.pyx'):
                        os.remove(os.path.join(root, file))
        except Exception as e:
            print(f'remove_pyx_files / error occured : {e}')
            
remove_pyx_files()"""
        try:
            with open(file_path, 'w') as file:
                file.write(setup_content)
        except Exception as e:
            print(f'push_file_obf / erroc occured : {e}')
            
            
    def execute_command(self , command, path):
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=path)
            return result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            print('execute_command : error occured : ' , e.stdout, e.stderr)
            return e.stdout, e.stderr
        
    
    def create_launch_file(self , path , module):
        try:
            with open(os.path.join(path, 'launch.py'), 'w') as file:
                file.write(f'import {module}')
        except Exception as e:
            print(f'create_launch_file / error occured : {e}')
            

    def delete_file(self , file_path):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Fichier supprimé: {file_path}")
                return True
            else:
                print(f"Le fichier n'existe pas: {file_path}")
                return False
        except Exception as e:
            print(f"delete_file / error occured : {e}")
            return False
 

ObfInC().run()