# pd (Product Development and Deployment)

## Features

1. Project initialization (FastAPI, NextJS, React, Electron).
2. Content downloading (YouTube)
3. File conversion (Image, Audio, Video).
4. EC2 instance management (launch, terminate).
5. Environment setup and configuration (zsh, vim, git, etc.)
6. Nginx configuration management (proxy, static resources).

## Installation

```bash
pip install zf-pd
```

This will install a `pd` binary in your system (even though the package name is `zf-pd`).

Like other shell tools, pd stores its config in `~/.pdconfig.json`.

See the [Config](#config) section for more information.

## Usage

```bash

### 1. Init

`pd init` is great tool for quickly initializing new development projects. It supports FastAPI, React and Electron
projects.

**Example**

You can quickly create a new FastAPI project by running:

```bash
$ pd init fastapi
Name: fastapi-test
```

This will create a new FastAPI project and print the following:

```bash
Created project fastapi-test at ./fastapi-test. Please run the following commands:
cd ./fastapi-test
pip install -r requirements.txt
npm run install
python3 -m uvicorn app.main:app --reload
Open http://localhost:8000
```

By default, `pd init` will create a new project at `./<project-name>` path. You can specify a custom path by running

```bash
$ pd init fastapi --name /path/to/fastapi-test
```

This will initialize a new FastAPI project at `/path/to/fastapi-test`.

For React or NextJS, you can basically do the same:

```bash
$ pd init react
Name: react-test
```

```bash
$ pd init nextjs
Name: nextjs-test
```

This will create a new React project called `react-test` at `./react-test` path.

You can also generate an Electron project:

```bash
$ pd init electron
Name: electron-test
```

The Electron project will come preconfigured with TypeScript, React, Chakra UI, and Apple DMG.

### 2. Download

`pd down` is tool for downloading content form the internet. Often times, when you are working on project, you need to
download resources from the internet in video, audio or text format. `pd down` makes this process easy.

`pd down` support the following commands:

```bash
$ pd down --help

Usage: pd down [OPTIONS] COMMAND [ARGS]...

  Download from the internet

Options:
  --help  Show this message and exit.

Commands:
  youtube  Download a YouTube video
```

#### 2.1 YouTube

`pd down youtube` is a tool for downloading YouTube videos.

```bash
$ pd down youtube --help
                                                 
Usage: pd down youtube [OPTIONS]

  Download a YouTube video

Options:
  -l, --link TEXT    Link to the YouTube video (e.g.
                     https://www.youtube.com/watch?v=...)  [required]
  -f, --format TEXT  Format to download as (e.g. mp4, mp3, txt)  [required]
  --help             Show this message and exit.
```

```bash
$ pd down youtube -l https://www.youtube.com/watch?v=... -f mp4
```

or

```bash
$ pd down youtube --link https://www.youtube.com/watch?v=... --format mp4
```

Not only you can download YouTube videos, you can also download YouTube videos as audio (mp3) or text (txt) files.

```bash
$ pd down youtube -l https://www.youtube.com/watch?v=... -f mp3
```

or

```bash
$ pd down youtube --link https://www.youtube.com/watch?v=... --format txt
```

This will output a file called `<YOUTUBE_TITLE>.txt` at the current directory.

### 4. Convert

`pd conv` is a tool for converting your files into other formats. It support image, video, and audio conversion.

You can list all available conversions by running:

```bash
$ pd conv list
Available conversions:
  text
    txt -> mp3
  image
    jpg, jpeg, webp -> png
    jpg, jpeg, webp, png -> mp4
  audio
    m4a -> wav, mp3
    mp3 -> wav, m4a
  video
    mp4,webm,mov -> mp3
```

**Example**

You can convert a mp4 video file into an audio file by running:

```bash
$ pd conv video -p tests/video.mp4 -f mp3
```

The converted audio file will be saved at `tests/video.mp3`.

Similarly, you can convert a m4a audio file into a mp3 audio file by running:

```bash
$ pd conv audio -p tests/audio.m4a -f mp3
```

The converted audio file will be saved at `tests/audio.mp3`.

You can also convert a text file into an audio file by running:

```bash
$ pd conv text -v "Convert this text to audio" -f mp3
```

This uses the OpenAI API so you will need to set your Open AI API key.

You can also pass options such as the voice:

```bash
$ pd conv text --value "Convert this text to audio" --format mp3 --options voice=Nova
```

```bash

### 4. EC2

`pd ec2` is a tool for managing EC2 instances. It uses `boto3` to manage EC2 instances.

You must configure the following when using `pd ec2` for the first time:

**Environment**:

```bash
export AWS_ACCESS_KEY_ID=<your-access-key-id>
export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
export AWS_DEFAULT_REGION=<your-region>
```

**~/.pdconfig**:

You must update `~/.pdconfig.json` with your EC2 launch template id and key pair path:

```bash
{
  "ec2": {
    "launch-template-id": <your-launch-template-id e.g. lt-1234567890>,
    "key-pair-path": <your-key-pair-path e.g. /home/ubuntu/key.pem>,
  }
}
```

- The key pair path must be an absolute path on the disk.

See [AWS EC2 Launch Templates](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html) for more
information.

`pd ec2` support the following commands:

#### 4.1 Launch

`pd ec2 launch` launches a new EC2 instance.

```bash
$ pd ec2 launch --help
Usage: pd ec2 launch [OPTIONS]

  Launch an EC2 instance

Options:
  -n, --name TEXT      Name of the EC2 instance e.g. ec2-test  [required]
  -c, --count INTEGER  Number of instances to launch [default: 1]
  -p, --project TEXT   Project name e.g /path/to/project

  --help               Show this message and exit.
```

**Example**

```bash
$ pd ec2 launch -n ec2-test -c 1
```

If this EC2 instance is part of a project, you can specify the project path:

```bash
$ pd ec2 launch -n ec2-test -p /path/to/project
```

#### 4.2 Terminate

`pd ec2 terminate` terminates an EC2 instance.

```bash
$ pd ec2 terminate --help
Usage: pd ec2 terminate [OPTIONS]

  Terminate an EC2 instance

Options:
  -i, --instance-id TEXT  ID of the EC2 instance to terminate e.g.
                          i-1234567890abcdef  [required]

  -p, --project TEXT      Project name e.g /path/to/project
  --help                  Show this message and exit.
```

**Example**

```bash
$ pd ec2 terminate -n ec2-test
```

You can additionally pass the project path:

```bash
$ pd ec2 terminate -n ec2-test -p /path/to/project
```

### 5. Nginx

`pd nginx` is a tool for managing Nginx configuration files.

`pd nginx` support the following commands:

#### 5.1 Generate

`pd nginx generate` generates Nginx configuration files.

```bash
pd nginx generate --help
Usage: pd nginx generate [OPTIONS]

  Generate nginx config

Options:
  -h, --host TEXT     Host to proxy to e.g. localhost  [required]
  -p, --port INTEGER  Port to proxy to e.g. 80  [required]
  -d, --domain TEXT   Domain to use for nginx config e.g. example.com
                      [required]

  -s, --static TEXT   Static resources path e.g. /path/to/static
  --help              Show this message and exit.

```

**Example**

```bash
$ pd nginx generate --host 127.0.0.1 --port 8000 --domain example.com
server {
    server_name examaple.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

You can additionally specify the static resources path:

```bash
$ pd nginx generate -h localhost -p 80 -d example.com -s /path/to/static
server {
    server_name example.com;

    root /path/to/static;
    client_max_body_size 50M;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/static;

        # Add CORS 'Access-Control-Allow-Origin' header for fonts
        location ~* \.(ico|png|css|ttf)$ {
            add_header Access-Control-Allow-Origin *;
        }
    }
}
```

## Config

`pd` will store the following information in `~/.pdconfig.json`:

```bash
{
    "projects": [
        {
            "type": "fastapi",
            "name": "project1",
            "path": "/path/to/project1",
            "instances": [
                "instance-1"
            ]
        },
        {
            "type": "fastapi",
            "name": "project2",
            "path": "/path/to/project2",
            "instances": [
                "instance-2"
            ]
        },
        {
            "type": "fastapi",
            "name": "project3",
            "path": "/path/to/project3",
            "instances": [
                "instance-3",
                "instance-4"
            ]
        }
    ],
    "ec2": {
        "launch-template-id": "lt-template-id",
        "key-pair-path": "/path/to/keypair.pem",
        "instances": [
            "instance-1",
            "instance-2",
            "instance-3",
            "instance-4"
        ]
    }
}
```

You can manually edit this file to add new projects or EC2 instances. However, it is recommended to use `pd` commands.
When you init a new project, `pd` will automatically add the project to `~/.pdconfig.json`. Similarly, when you launch
a new EC2 instance, `pd` will automatically add the instance to `~/.pdconfig.json` and associate it with the project
if you specify the project path.

## LICENSE

MIT License

