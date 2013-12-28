GettUp
======

GettUp is a simple command line utility which lets you share and upload files to the [ge.tt](http://ge.tt) sharing service quickly and easily.

## Installation 
GettUp is distributed as a python package. Do the following to install

``` sh
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

```sh 
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

## Upgrade
To upgrade GettUp run the following command
```sh
sudo pip install -U Markdown
```
## License
Gettup is released under the MIT license.
