# Headless Raspberry Pi Setup


A script to setup a sd card for a headless raspberry pi setup. 
This script will enable ssh, setup wifi, and change the default password.


## Usage

(use `venv` for better isolation)

To install the dependencies run: 

```bash
$ pip install -r requirements.txt
```


Create a `config.json` file in the root of the project following the `config-SAMPLE.json` file example.

Then run:

```bash
$ python main.py -v <the-path-of-the-sd-volume>
```