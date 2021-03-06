# -*- coding: utf-8 -*-
import datetime
import json
import os.path

from pyramid.httpexceptions import HTTPBadRequest
import semantic_version as semver

from hel.utils.constants import Constants
from hel.utils.messages import Messages
from hel.utils.query import (
    replace_chars_in_keys,
    parse_url,
    split_path,
    check_path,
    check_filename
)


class ModelPackage:

    def __init__(self, strict=False, **kwargs):
        self.data = {
            'name': '',
            'description': '',
            'short_description': '',
            'owners': [],
            'authors': [],
            'license': '',
            'tags': [],
            'versions': {},
            'screenshots': {},
            'stats': {
                'views': 0,
                'date': {
                    'created': (datetime.datetime.utcnow()
                                .strftime(Constants.date_format)),
                    'last-updated': (datetime.datetime.utcnow()
                                     .strftime(Constants.date_format))
                }
            }
        }

        if strict:
            for k in ['name', 'description', 'short_description', 'authors',
                      'license', 'tags', 'versions', 'screenshots', 'owners']:
                if k not in kwargs:
                    raise KeyError(k)

        for k, v in kwargs.items():
            if k in ['name', 'description', 'license']:
                self.data[k] = str(v)
            elif k in ['authors', 'tags']:
                self.data[k] = [str(x) for x in v]
            elif k == 'owners':
                owners = [str(x) for x in v]
                for owner in owners:
                    if not Constants.user_pattern.match(owner):
                        raise HTTPBadRequest(detail=Messages.user_bad_name)
                if len(owners) == 0:
                    raise HTTPBadRequest(detail=Messages.empty_owner_list)
                self.data[k] = owners
            elif k == 'versions':
                data = {}
                for ver, value in v.items():
                    files = {}
                    for file_url_unchecked, f in value['files'].items():
                        file_url = parse_url(file_url_unchecked)
                        file_dir = file_name = file_path = None
                        if ('path' not in f and
                                'dir' not in f and
                                'name' not in f):
                            f['path']  # raise an error
                        if 'path' in f:
                            check_path(str(f['path']))
                            file_path = os.path.join('/', str(f['path']))
                            file_dir, file_name = split_path(file_path)
                        else:
                            check_path(str(f['name']))
                            check_filename(str(f['name']))
                            file_dir, file_name = str(f['dir']), str(f['name'])
                            file_path = os.path.join('/', f['dir'], f['name'])
                        file_dir = os.path.normpath(file_dir)
                        file_name = os.path.normpath(file_name)
                        file_path = os.path.normpath(file_path)
                        files[str(file_url)] = {
                            'dir': file_dir,
                            'name': file_name,
                            'path': file_path
                        }
                    dependencies = {}
                    for dep_name, dep_info in value['depends'].items():
                        if dep_info['type'] not in [
                                    'recommended',
                                    'optional',
                                    'required'
                                ]:
                            raise ValueError(Messages.wrong_dep_type)
                        semver.Spec(dep_info['version'])
                        dependencies[str(dep_name)] = {
                            'version': str(dep_info['version']),
                            'type': str(dep_info['type'])
                        }
                    data[str(semver.Version.coerce(str(ver)))] = {
                        'files': files,
                        'depends': dependencies,
                        'changes': value['changes']
                    }
                self.data[k] = data
            elif k == 'screenshots':
                self.data[k] = {parse_url(str(url)): str(desc)
                                for url, desc in v.items()}
            elif k == 'short_description':
                self.data[k] = str(v)[:Constants.sdesc_len]

    @property
    def json(self):
        return json.dumps(self.pkg)

    @property
    def pkg(self):
        return replace_chars_in_keys(
            self.data, '.', Constants.key_replace_char)

    def __str__(self):
        return json.dumps(self.data)


class ModelUser:

    def __init__(self, strict=False, **kwargs):
        self.data = {
            'nickname': '',
            'groups': [],
            'password': '',
            'email': '',
            'activation_phrase': '',
            'activation_till': '',
            # TODO: remove in hel@4.0.0
            'salted': True
        }

        if strict:
            for v in ['nickname', 'password', 'email', 'activation_phrase',
                      'activation_till']:
                if v not in kwargs:
                    raise KeyError(v)

        for k, v in kwargs.items():
            if k in ['activation_till', 'password',
                     'email', 'activation_phrase']:
                self.data[k] = str(v)
            elif k == 'nickname':
                if not Constants.user_pattern.match(str(v)):
                    raise HTTPBadRequest(detail=Messages.user_bad_name)
                self.data[k] = str(v)
            elif k == 'groups':
                self.data[k] = [str(x) for x in v]

    @property
    def json(self):
        return json.dumps(self.data)

    def __str__(self):
        return self.json
