# Email Generator

## Installation
Download the latest release as a `tar.gz` file.

## Setup
### Build program
Run `setup.sh` (can be run by simply double-clicking on the file).

### Set up the Google API
Follow the guide at https://developers.google.com/gmail/api/quickstart/python#set_up_your_environment to generate OAuth2 credentials, and, when you are at the step to configure the OAuth consent screen, add the `gmail.compose` scope so the script can edit drafts. Download them into `.credentials/credentials.json` (you will have to create this directory yourself, and show hidden files to see it on MacOS).

### Set up the template
Update the email template in `data/template.json`.

#### Template Format
| Key                      | Value                                            |
|--------------------------|--------------------------------------------------|
| `subject` (formatted)    | E-mail subject                                   |
| `body` (formatted)       | E-mail body                                      |
| `attachments` (optional) | Paths to any attachments that should be included |

Formatted fields can include the following variables
| Variable  | Data           |
|-----------|----------------|
| `{name}`  | Company name   |
| `{email}` | Company E-mail |

## Usage
### Prepare data
Copy and paste the table into `data/email-list.txt`.
### Run the program
Run `run.sh` (can be run by double-clicking as well)
The first time it is run, you will need to authenticate with the account that you want to upload the drafts to. A browser window should be opened automatically to do this in (if it is not, copy and paste the URL from the terminal window into your browser). The authentication flow may not work in Firefox or other Gecko-based browsers, so try Chrome, Safari, or another Chromium- or Webkit-based browser if it doesn't work for you.

## Building from source
Install the `build` tool with pip and run `python3 -m build` to build the package.