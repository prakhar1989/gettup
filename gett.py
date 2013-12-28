#!/usr/bin/env python
# coding: utf-8 

# Copyright 2013 - Prakhar Srivastav

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import json
import sys
import argparse
import os

# GETT URLS
LOGIN_URL = "http://open.ge.tt/1/users/login"
SHARE_URL = "http://open.ge.tt/1/shares/create?accesstoken="

def refresh_access_token():
    print "Updating expired tokens ..."
    refreshtoken = read_config('refreshtoken')
    r = requests.post(LOGIN_URL, data=json.dumps({'refreshtoken': refreshtoken }))
    accesstoken, refreshtoken = r.json().get('accesstoken'), r.json().get('refreshtoken')
    write_config({'accesstoken': accesstoken, 'refreshtoken': refreshtoken})
    # func(accesstoken)

def get_shares():
    accesstoken = get_access_token()
    print "Fetching shares ..."
    get_share_url = "http://open.ge.tt/1/shares?accesstoken=" + accesstoken
    r = requests.get(get_share_url)
    shares = r.json()
    if r.status_code != 200:
        refresh_access_token()
        return get_shares()
    if not shares:
        print "You don't have any shares. Create a new share by uploading a file"
    else:
        for shr in shares:
            print "%d file(s) in share: %s (%s)" % \
                (len(shr['files']), shr['sharename'], shr['getturl'])

def get_share_info(sharename):
    print "Fetching share info ..."
    get_share_url = "http://open.ge.tt/1/shares/" + sharename
    r = requests.get(get_share_url)
    share_info = r.json()
    print "Share: %s | gett url: %s | total files: %d" % (sharename, share_info['getturl'], len(share_info['files']))
    for f in share_info['files']:
        print f['filename'], "%s bytes " % f['size'], f['getturl']

def create_share():
    accesstoken = get_access_token()
    print "Constructing a new share ..."
    r = requests.post(SHARE_URL + accesstoken)
    if r.status_code != 200:
        refresh_access_token()
        return create_share()
    return r.json().get('sharename')

def destroy_share(sharename):
    print "Destroying share ..."
    accesstoken = get_access_token()
    url = "http://open.ge.tt/1/shares/%s/destroy?accesstoken=%s" % (sharename, accesstoken)
    r = requests.post(url)
    if r.status_code == 200:
        print "%s share has been destroyed" % sharename
    else:
        refresh_access_token()
        return destroy_share(sharename)

def upload_file(sharename, filename):
    accesstoken = get_access_token()
    file_url = "http://open.ge.tt/1/files/%s/create?accesstoken=%s" % (sharename, accesstoken)
    print "Setting up a file name ..."
    r = requests.post(file_url, data=json.dumps({"filename": filename }))
    if r.status_code != 200:
        refresh_access_token()
        return upload_file(sharename, filename)
    gett_url = r.json().get('getturl')
    post_upload_url = r.json()['upload']['posturl']
    print "Uploading the file..."
    r = requests.post(post_upload_url, files={'file': open(filename, 'rb')})
    if r.status_code == 200:
        print "Upload successful. Here's your url: %s" % gett_url
    else:
        print "Error: " + r.json().get('error')

def config_file():
    home = os.getenv('USERPROFILE') or os.getenv('HOME')
    return os.path.join(home, '.gett.cfg')

def read_config(token):
    file_location = config_file()
    if sys.version_info[0] == 3:
        import configparser as cp
    else:
        import ConfigParser as cp
    config = cp.RawConfigParser()
    if not config.read(file_location) or not config.has_section('TOKENS') \
                                  or not config.has_option('TOKENS', token):
        return None
    return config.get('TOKENS', token)

def write_config(fields):
    if sys.version_info[0] == 3:
        import configparser as cp
    else:
        import ConfigParser as cp
    config = cp.RawConfigParser()
    config.add_section("TOKENS")
    for k in fields:
        config.set("TOKENS", k, fields[k])
    file_location = config_file()
    with open(file_location, 'wb') as configfile:
        config.write(configfile)

def setup_tokens():
    email = raw_input("Please enter your Ge.tt email: ").strip()
    password = raw_input("Please enter your Ge.tt password: ").strip()
    apikey = raw_input("Please enter your API KEY: ").strip()

    print "Validating credentials ..."
    r = requests.post(LOGIN_URL, data=json.dumps({'email': email, 'password': password,
                                                  'apikey': apikey}))

    accesstoken, refreshtoken = r.json().get('accesstoken'), r.json().get('refreshtoken')
    if not accesstoken or not refreshtoken:
        print "Error! Your credentials failed validation. Exiting program"
        sys.exit(0)
    print "Credentials verified  ..."
    write_config({'accesstoken': accesstoken, 'refreshtoken': refreshtoken})
    return accesstoken

def get_access_token():
    return read_config('accesstoken') or setup_tokens()

def main():
    parser = argparse.ArgumentParser(description="Upload files to ge.tt via the command line")
    parser.add_argument("-s", "--share", metavar="share_name", type=str,
                        help="get info for a specific share")
    parser.add_argument("-u", "--upload", metavar="file", type=str,
                        help="provide a file to upload")
    parser.add_argument("-d", "--destroy", metavar="share_name", type=str,
                        help="destroy a share & all files in it")
    args = parser.parse_args()
    if args.destroy:
        destroy_share(args.destroy)
    elif args.share and not args.upload:
        get_share_info(args.share)
    elif args.upload and not args.share:
        sharename = create_share()
        upload_file(sharename, args.upload)
    elif args.upload and args.share:
        upload_file(args.share, args.upload)
    else:
        get_shares()

if __name__ == "__main__":
    main()
