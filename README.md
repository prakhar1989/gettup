GettUp
======

GettUp is a simple command line utility which lets you share and upload files to the [ge.tt](http://ge.tt) sharing service quickly and easily.

## Installation 
GettUp is distributed as a python package. Do the following to install

``` 
sudo pip install gettup
OR 
sudo easy_install gettup
OR
# download source and cd to it
sudo python setup.py install
```

## Usage
1. Make an account on [Ge.tt](http://ge.tt)
2. Obtain an api key by [creating an app](http://ge.tt/developers/create).
3. Run the application. The app will ask for your credentials the first the app is run. 

```
$ gett
Please enter your Ge.tt email: example@example.com
Please enter your Ge.tt password: verysecurepassword
Please enter your API KEY: supersecretapikey
Validating credentials ...
Credentials verified  ...
Fetching shares ...
1 file(s) in share: 5d1ctaB1 (http://ge.tt/5d1ctaB1)
1 file(s) in share: 8BSfsaB1 (http://ge.tt/8BSfsaB1)
1 file(s) in share: 93hTsaB1 (http://ge.tt/93hTsaB1)
2 file(s) in share: 1m4yqaB1 (http://ge.tt/1m4yqaB1)
```

## Examples
`gett` displays a helpful help text when run with the `-h` flag.
``` 
$ gett -h
usage: gett.py [-h] [-s share_name] [-u file] [-d share_name]

Upload files to ge.tt via the command line

optional arguments:
  -h, --help            show this help message and exit
  -s share_name, --share share_name
                        get info for a specific share
  -u file, --upload file
                        provide a file to upload
  -d share_name, --destroy share_name
                        destroy a share & all files in it
```

When `gett` is run from the command line without any arguments, it fetches the list of all shares. Shares are like albums or groups of files on ge.tt. You can have a share containing no files, a single file or lots of files.

```
$ gett
Fetching shares ...
1 file(s) in share: 5d1ctaB1 (http://ge.tt/5d1ctaB1)
1 file(s) in share: 8BSfsaB1 (http://ge.tt/8BSfsaB1)
1 file(s) in share: 93hTsaB1 (http://ge.tt/93hTsaB1)
2 file(s) in share: 1m4yqaB1 (http://ge.tt/1m4yqaB1)
```

To upload a file, use the -u flag. By default, `gett` will create a new share for uploading the file. Use the -s flag, alongwith a sharename to upload to an existing share
```
$ gett -u something.txt
Constructing a new share ...
Setting up a file name ...
Uploading the file...
Upload successful. Here's your url: http://ge.tt/1NcgabB1/v/0

$ gett -u something.txt -s 5d1ctaB1
Setting up a file name ...
Uploading the file...
Upload successful. Here's your url: http://ge.tt/5d1ctaB1/v/1
```

To delete a share use the -d flag. To get more info about a share, use the -s flag accompanied by a sharename.
```
$ gett -d 1NcgabB1
Destroying share ...
1NcgabB1 share has been destroyed

$ gett -s 5d1ctaB1
Fetching share info ...
Share: 5d1ctaB1 | gett url: http://ge.tt/5d1ctaB1 | total files: 2
something.txt 19 bytes  http://ge.tt/5d1ctaB1/v/1
shot2.png 595250 bytes  http://ge.tt/5d1ctaB1/v/0
```

## Upgrade
To upgrade GettUp run the following command
```
sudo pip install -U Markdown
```

## Thanks 
Thanks to [gett-cli](https://bitbucket.org/mickael9/gett-cli) for inspiration, which is, at present, for Python 3 only.

## License
Gettup is released under the MIT license.
