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
$ gett file1.txt
Please enter your Ge.tt email: example@example.com
Please enter your Ge.tt password: verysecurepassword
Please enter your API KEY: supersecretapikey
Validating credentials ...
Credentials verified ...
Constructing a new share ...
Uploading file: README.md
Setting up a file name ...
Uploading the file...
Upload successful. Here's your url: http://ge.tt/6zkcEkB1/v/0
----------------------------------------
```

## Examples
`gett` displays a helpful help text when run with the `-h` flag.
``` 
$ gett
usage: gett.py [-h] [-s share_id] [-t share_title] [-i share_id]
               [-d share_id [share_id ...]] [-l] [-r file_url [file_url ...]]
               [-q]
               [files [files ...]]

Upload files to ge.tt via the command line
```

Command Examples - 
```
$ gett                            # show help
$ gett file1 file2 file3          # upload files (in same share)
$ gett *.py                       # linux globs (upload)
$ gett *.py -s sharename          # upload file in the specific share
$ gett *.py -s sharename -t title # gives the title to the new share
$ gett --list                     # show list of shares
$ gett -d share1 share2 share3    # deletes the shares
$ gett -r url1 url2 url 3         # deletes the file url
$ gett -q {etc}                   # quiet mode
$ gett -i sharename               # get share info
```

To upload a file, use the -u flag. By default, `gett` will create a new share for uploading the file. Use the -s flag, alongwith a sharename to upload to an existing share
```
$ gett something.txt
Constructing a new share ...
Setting up a file name ...
Uploading the file...
Upload successful. Here's your url: http://ge.tt/1NcgabB1/v/0
----------------------------------------

$ gett something.txt -s 5d1ctaB1
Setting up a file name ...
Uploading the file...
Upload successful. Here's your url: http://ge.tt/5d1ctaB1/v/1
```

To delete a share use the -d flag. To get more info about a share, use the -s flag accompanied by a sharename.
```
$ gett -d 1NcgabB1
Destroying share ...
1NcgabB1 share has been destroyed

$ gett -r http://ge.tt/6zkcEkB1/v/0
Deleting file ...
File has been successfully destroyed
```

## Upgrade
To upgrade GettUp run the following command
```
sudo pip install -U gettup
```

## Thanks 
Thanks to [gett-cli](https://bitbucket.org/mickael9/gett-cli) for inspiration, which is, at present, for Python 3 only.

## License
Gettup is released under the MIT license.
