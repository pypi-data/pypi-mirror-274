**Table of contents**
- [Note](#note)
- [Features](#features)
- [Installation](#installation)
  - [Requirements](#requirements)
    - [Git token](#git-token)
    - [Hot get Postman API Key](#hot-get-postman-api-key)
  - [Installing](#installing)
  - [Configuring](#configuring)
- [How to use](#how-to-use)

# Note
- All your data is stored inside `$HOME/.staircase` folder. Don`t share this!
# Features
- Postman management. You can import api`s and your environments into it.
- CI flow management. You can easily run pipeline on any product, pick steps you only need and get output from it.

# Installation
## Requirements
- [fzf](https://github.com/junegunn/fzf#installation)
- [Git token](#git-token)
- [Postman API Key](#hot-get-postman-api-key)
- Marketplace API key

### Git token
Used for clone product.
GitHub token. Go to GitHub.com/Settings/Developer settings/Personal access token/New/Enable SSO.
Add checks to enable repo access.

### Hot get Postman API Key
Follow steps via app or website:
- Click on profile pic 
- Settings 
- API keys 
- Generate API key
  Consider verify that expiration date is okay, you are going need to renew it after.

## Installing 
- Open terminal.
- `pip install staircase-kit`

## Configuring
- Open terminal.
- Run command `staircase config setup` or edit file `staircase config file-path`.

# How to use
- Open terminal
- Run command `staircase` or `sc`
- You can run `--help` to any command to get extra info.
