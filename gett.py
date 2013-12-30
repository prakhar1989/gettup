#!/usr/bin/env python
# coding: utf-8 

"""
gettup - A command-line file sharing utility for ge.tt
usage:
$ gett                            > show help
$ gett file1 file2 file3          > upload files (in same share)
$ gett *.py                       > linux globs (upload)
$ gett *.py -p                    > parallelize uploads
$ gett *.py -z                    > zips the files and uploads
$ gett *.py -s sharename          > upload file in the specific share
$ gett *.py -s sharename -t title > gives the title to the new share
$ gett --list                     > show list of shares
$ gett -d share1 share2 share3    > deletes the shares
$ gett -r url1 url2 url 3         > deletes the file url
$ gett -q {etc}                   > quiet mode
$ gett -i sharename               > get share info

"""
import requests
import json
import sys
import argparse
import os
import signal

# GETT URLS
LOGIN_URL = "http://open.ge.tt/1/users/login"
SHARE_URL = "http://open.ge.tt/1/shares/create?accesstoken="
VERBOSE = True

def signal_handler(signal, frame):
    """ graceful exit on keyboard interrupt """
    sys.exit(0)

def logg(msg):
    """ print to screen based on VERBOSE toggling """
    if VERBOSE: print msg

def refresh_access_token():
    """ re-fetches fresh access tokens using the refresh token and writes to the config file """
    logg("Updating expired tokens ...")
    refreshtoken = read_config('refreshtoken')
    r = requests.post(LOGIN_URL, data=json.dumps({'refreshtoken': refreshtoken }))
    if r.status_code != 200:
        print "Error: Cannot fetch tokens. Try deleting the ~/.gett.cfg file and re-trying"
        sys.exit(0)
    accesstoken, refreshtoken = r.json().get('accesstoken'), r.json().get('refreshtoken')
    write_config({'accesstoken': accesstoken, 'refreshtoken': refreshtoken})

def get_shares():
    """ gets the list of all shares using an accesstoken and prints on screen """
    accesstoken = get_access_token()
    logg("Fetching shares ...")
    get_share_url = "http://open.ge.tt/1/shares?accesstoken=" + accesstoken
    r = requests.get(get_share_url)
    shares = r.json()
    if r.status_code != 200:
        refresh_access_token()
        return get_shares()
    if not shares:
        print "You don't have any shares. Create a new share by uploading a file"
    else:
        for shr in shares: # TODO: beautify and humanize
            print "%d file(s) in share: %s (%s)" % \
                (len(shr['files']), shr['sharename'], shr['getturl'])

def get_share_info(sharename):
    """ retrives the information of files stored in a specific share """
    logg("Fetching share info ...")
    get_share_url = "http://open.ge.tt/1/shares/" + sharename
    r = requests.get(get_share_url)
    share_info = r.json()
    if r.status_code != 200:
        print "Error: Share not found"
        return
    print "Share: %s | gett url: %s | total files: %d" % (sharename, share_info['getturl'], len(share_info['files']))
    for f in share_info['files']:
        print f['getturl'], humanize(f['size']), f['filename']

def delete_file(sharename, fileid):
    """ deletes a file in a specific share and a fileId """
    logg("Deleting file ...")
    accesstoken = get_access_token()
    destroy_url = "http://open.ge.tt/1/files/%s/%s/destroy?accesstoken=%s" % \
                  (sharename, fileid, accesstoken)
    r = requests.post(destroy_url)
    if r.status_code != 200:
        refresh_access_token()
        return delete_file(sharename, fileid)
    print "File has been successfully destroyed"

def delete_url(url):
    """ deletes the file corresponding to the URL """
    fields = url.split('/')
    if len(fields) != 6:
        print "Error: Invalid url format"
        return
    delete_file(fields[3], fields[-1])

def create_share(title=None):
    """ creates a new share with an optional title and returns the share id """
    accesstoken = get_access_token()
    logg("Constructing a new share ...")
    if title:
        r = requests.post(SHARE_URL + accesstoken, data=json.dumps({'title': title}))
    else:
        r = requests.post(SHARE_URL + accesstoken)
    if r.status_code != 200:
        refresh_access_token()
        return create_share()
    return r.json().get('sharename')

def destroy_share(sharename):
    # TODO: Goes in infinite loop when the share does not exist
    # as the wrong status code is returned
    logg("Destroying share ...")
    accesstoken = get_access_token()
    url = "http://open.ge.tt/1/shares/%s/destroy?accesstoken=%s" % (sharename, accesstoken)
    r = requests.post(url)
    if r.status_code == 200:
        print "%s share has been destroyed" % sharename
    else:
        refresh_access_token()
        return destroy_share(sharename)

def upload_file(sharename, filename):
    """ upload a file in share with the sharename """
    accesstoken = get_access_token()
    file_url = "http://open.ge.tt/1/files/%s/create?accesstoken=%s" % (sharename, accesstoken)
    logg("Setting up a file name ...")
    r = requests.post(file_url, data=json.dumps({"filename": filename }))
    if r.status_code != 200:
        refresh_access_token()
        return upload_file(sharename, filename)
    gett_url = r.json().get('getturl')
    post_upload_url = r.json()['upload']['posturl']
    logg("Uploading the file...")
    r = requests.post(post_upload_url, files={'file': open(filename, 'rb')})
    if r.status_code == 200:
        print "Upload successful. Here's your url: %s" % gett_url
    else:
        print "Error: " + r.json().get('error')

def config_file():
    """ returns the location (~/.gett.cfg) of the config file in user's home dir """
    home = os.getenv('USERPROFILE') or os.getenv('HOME')
    return os.path.join(home, '.gett.cfg')

def read_config(token):
    """ reads token values from the configuration file """
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
    """ writes a set of fields into the config file """
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

def bulk_upload(files, sharename=None, title=None):
    """ wrapper for uploading more than one files into a share(with optional title) """
    sharename = sharename or create_share(title)
    for f in files:
        print "Uploading file: " + f
        upload_file(sharename, f)
        logg("----------------------------------------")

def setup_tokens():
    """ fetch fresh tokens using user's credentials """
    email = raw_input("Please enter your Ge.tt email: ").strip()
    password = raw_input("Please enter your Ge.tt password: ").strip()
    apikey = raw_input("Please enter your API KEY: ").strip()

    logg("Validating credentials ...")
    r = requests.post(LOGIN_URL, data=json.dumps({'email': email, 'password': password,
                                                  'apikey': apikey}))

    accesstoken, refreshtoken = r.json().get('accesstoken'), r.json().get('refreshtoken')
    if not accesstoken or not refreshtoken:
        print "Error! Your credentials failed validation. Exiting program"
        sys.exit(0)
    logg("Credentials verified ...")
    write_config({'accesstoken': accesstoken, 'refreshtoken': refreshtoken})
    return accesstoken

def get_access_token():
    """ retrieves access token either from the config file or from the user """
    return read_config('accesstoken') or setup_tokens()

def humanize(nbytes):
    """ returns the file size in human readable format """
    for (exp, unit) in ((9, 'GB'), (6, 'MB'), (3, 'KB'), (0, 'B')):
        if nbytes >= 10**exp:
            break
    return "%.2f %s" % (float(nbytes)/10**exp, unit)

def main():
    """ ENTRY METHOD """
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Upload files to ge.tt via the command line",
                                     epilog="For more information, examples & source code visit http://github.com/prakhar1989/gettup")

    # FILE UPLOADS
    file_uploads = parser.add_argument_group("File Uploads")
    file_uploads.add_argument("files", metavar="files", nargs="*",
                             help="list of files you want to upload")
    file_uploads.add_argument("-s", "--share", metavar="share_id",
                             help="upload files to a particular share")
    file_uploads.add_argument("-t", "--title", metavar='share_title',
                             help='title for the new share')

    # SHARE RELATED COMMANDS
    share_group = parser.add_argument_group('Share Related')
    share_group.add_argument("-i", '--info', metavar="share_id",
                            help="get info for a specific share")
    share_group.add_argument('-d', '--delete', metavar="share_id", nargs="+",
                            help="delete a share & all files in it")
    share_group.add_argument('-l', '--list', action="store_true",
                            help="Lists all shares in your account")
    share_group.add_argument('-r', '--remove', metavar="file_url", nargs="+",
                            help="Delete a list of files with associated urls")

    # MISC COMMANDS
    misc_group = parser.add_argument_group('Other actions')
    misc_group.add_argument('-q', '--quiet', action="store_true",
                           help="Toggle verbose off (default is on)")
    args = parser.parse_args()

    global VERBOSE
    VERBOSE = not args.quiet

    if args.info:
        get_share_info(args.info)

    if args.list:
        get_shares()

    if args.delete:
        for sharename in args.delete:
            destroy_share(sharename)

    if args.remove:
        for url in args.remove:
            delete_url(url)

    if args.files:
        bulk_upload(args.files, sharename=args.share, title=args.title)

    if len(sys.argv) == 1:
        parser.print_help()

if __name__ == "__main__":
    main()
