import logging
import os
import json
from typing import Set, List, Dict

from checkov.common.sast.consts import SastLanguages


class FilesFilterManager:
    def __init__(self, source_codes: List[str], languages: Set[SastLanguages]) -> None:
        self.source_codes: List[str] = source_codes
        self.languages: Set[SastLanguages] = languages

    def get_files_to_filter(self) -> List[str]:
        files_to_filter: List[str] = []
        try:
            if SastLanguages.JAVASCRIPT in self.languages:
                files_to_filter += self._get_js_files_to_filter()
        except Exception as e:
            logging.debug(f'Error filtering js files generated by ts: {e}')
        return files_to_filter

    def _get_js_files_to_filter(self) -> List[str]:
        js_files_to_filter = []

        for path in self.source_codes:
            js_files: List[Dict[str, str]] = []
            ts_files: List[Dict[str, str]] = []
            tsconfig_files: List[Dict[str, str]] = []
            for (dirpath, _, filenames) in os.walk(path):
                if '/node_modules/' in dirpath:
                    continue
                for filename in filenames:
                    if filename.endswith('.ts'):
                        ts_files.append({'full_path': os.sep.join([dirpath, filename]), 'dir': dirpath, 'name': filename})
                    if filename.endswith('tsconfig.json'):
                        tsconfig_files.append({'full_path': os.sep.join([dirpath, filename]), 'dir': dirpath, 'name': filename})
                    if filename.endswith('.js'):
                        js_files.append({'full_path': os.sep.join([dirpath, filename]), 'dir': dirpath, 'name': filename})

            js_files_to_filter += FilesFilterManager._filter_by_tsconfig(tsconfig_files)
            js_files_to_filter += FilesFilterManager._filter_direct_build_js(js_files, ts_files, js_files_to_filter)

        return js_files_to_filter

    @staticmethod
    def _filter_direct_build_js(js_files: List[Dict[str, str]], ts_files: List[Dict[str, str]], filtered_by_tsconfig: List[str]) -> List[str]:
        js_files_to_filter: List[str] = []
        for js_file in js_files:
            js_dir = js_file.get('dir', '')
            already_skipped = False
            for filtered_by_tsconfig_path in filtered_by_tsconfig:
                if js_dir.startswith(filtered_by_tsconfig_path):
                    already_skipped = True
                    break
            if already_skipped:
                continue
            for ts_file in ts_files:
                if ts_file.get('dir', '') == js_dir and ts_file.get('name', '')[:-3] == js_file.get('name', '')[:-3]:
                    js_files_to_filter.append(js_file.get('full_path', ''))
                    break
        return js_files_to_filter

    @staticmethod
    def _filter_by_tsconfig(tsconfig_files: List[Dict[str, str]]) -> List[str]:
        js_files_to_filter: List[str] = []
        for tsconfig_file in tsconfig_files:
            with open(tsconfig_file.get('full_path', '')) as fp:
                config = json.load(fp)
            out_dir = config.get('compilerOptions', {}).get('outDir')
            out_file = config.get('compilerOptions', {}).get('outFile')
            if out_dir:
                build_dir = out_dir
            elif out_file:
                build_dir = out_file
            else:
                build_dir = tsconfig_file.get('dir')

            # relative path
            if not build_dir.startswith('/'):
                build_path = os.path.abspath(tsconfig_file.get('dir', '') + '/' + build_dir)
            # absolute path
            else:
                build_path = build_dir
            js_files_to_filter.append(build_path)
        return js_files_to_filter
