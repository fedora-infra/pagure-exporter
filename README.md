# Pagure Exporter

Simple exporter tool that helps migrate repository files, data assets and issue tickets from projects on Pagure to GitLab

## Installation

### From PyPI

1. Ensure that you have `python3` and `python3-pip` installed.

    ```
    $ sudo dnf install python3 python3-pip --setopt=install_weak_deps=False
    ```

2. Create and activate a Python virtual environment in that directory.

    ```
    $ python3 -m venv venv
    ```

    ```
    (venv) $ source venv/bin/activate
    ```

3. Install `pagure-exporter` using `pip` in the activated virtual environment.

    ```
    (venv) $ pip install pagure-exporter
    ```

    Sample output

    ```
    Collecting pagure-exporter
      Downloading pagure_exporter-0.1.4-py3-none-any.whl.metadata (20 kB)
    Collecting GitPython<4.0.0,>=3.1.0 (from pagure-exporter)
      Downloading GitPython-3.1.44-py3-none-any.whl.metadata (13 kB)
    Collecting click<9.0.0,>=8.1.3 (from pagure-exporter)
      Using cached click-8.2.1-py3-none-any.whl.metadata (2.5 kB)
    Collecting python-gitlab>=3.14.0 (from pagure-exporter)
      Downloading python_gitlab-6.1.0-py3-none-any.whl.metadata (8.5 kB)
    Collecting requests<3.0.0,>=2.28.0 (from pagure-exporter)
      Using cached requests-2.32.4-py3-none-any.whl.metadata (4.9 kB)
    Collecting gitdb<5,>=4.0.1 (from GitPython<4.0.0,>=3.1.0->pagure-exporter)
      Downloading gitdb-4.0.12-py3-none-any.whl.metadata (1.2 kB)
    Collecting smmap<6,>=3.0.1 (from gitdb<5,>=4.0.1->GitPython<4.0.0,>=3.1.0->pagure-exporter)
      Downloading smmap-5.0.2-py3-none-any.whl.metadata (4.3 kB)
    Collecting charset_normalizer<4,>=2 (from requests<3.0.0,>=2.28.0->pagure-exporter)
      Using cached charset_normalizer-3.4.2-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (35 kB)
    Collecting idna<4,>=2.5 (from requests<3.0.0,>=2.28.0->pagure-exporter)
      Using cached idna-3.10-py3-none-any.whl.metadata (10 kB)
    Collecting urllib3<3,>=1.21.1 (from requests<3.0.0,>=2.28.0->pagure-exporter)
      Using cached urllib3-2.5.0-py3-none-any.whl.metadata (6.5 kB)
    Collecting certifi>=2017.4.17 (from requests<3.0.0,>=2.28.0->pagure-exporter)
      Using cached certifi-2025.6.15-py3-none-any.whl.metadata (2.4 kB)
    Collecting requests-toolbelt>=1.0.0 (from python-gitlab>=3.14.0->pagure-exporter)
      Using cached requests_toolbelt-1.0.0-py2.py3-none-any.whl.metadata (14 kB)
    Downloading pagure_exporter-0.1.4-py3-none-any.whl (40 kB)
    Using cached click-8.2.1-py3-none-any.whl (102 kB)
    Downloading GitPython-3.1.44-py3-none-any.whl (207 kB)
    Downloading gitdb-4.0.12-py3-none-any.whl (62 kB)
    Using cached requests-2.32.4-py3-none-any.whl (64 kB)
    Using cached charset_normalizer-3.4.2-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (148 kB)
    Using cached idna-3.10-py3-none-any.whl (70 kB)
    Downloading smmap-5.0.2-py3-none-any.whl (24 kB)
    Using cached urllib3-2.5.0-py3-none-any.whl (129 kB)
    Using cached certifi-2025.6.15-py3-none-any.whl (157 kB)
    Downloading python_gitlab-6.1.0-py3-none-any.whl (144 kB)
    Using cached requests_toolbelt-1.0.0-py2.py3-none-any.whl (54 kB)
    Installing collected packages: urllib3, smmap, idna, click, charset_normalizer, certifi, requests, gitdb, requests-toolbelt, GitPython, python-gitlab, pagure-exporter
    Successfully installed GitPython-3.1.44 certifi-2025.6.15 charset_normalizer-3.4.2 click-8.2.1 gitdb-4.0.12 idna-3.10 pagure-exporter-0.1.4 python-gitlab-6.1.0 requests-2.32.4 requests-toolbelt-1.0.0 smmap-5.0.2 urllib3-2.5.0
    ```

### From source

1. Ensure that you have `git`, `python3` and `poetry` installed.

    ```
    $ sudo dnf install git python3 poetry --setopt=install_weak_deps=False
    ```

2. Clone the repository to the local storage and make it the present working directory.

    ```
    $ git clone https://github.com/gridhead/pagure-exporter.git
    ```

    ```
    $ cd pagure-exporter
    ```

    Sample output

    ```
    Cloning into 'pagure-exporter'...
    remote: Enumerating objects: 118, done.
    remote: Counting objects: 100% (118/118), done.
    remote: Compressing objects: 100% (78/78), done.
    remote: Total 118 (delta 48), reused 94 (delta 31), pack-reused 0
    Receiving objects: 100% (118/118), 56.38 KiB | 4.34 MiB/s, done.
    Resolving deltas: 100% (48/48), done.
    ```

3. Create and activate a Python virtual environment in that directory.

    ```
    $ python3 -m venv venv
    ```

    ```
    (venv) $ source venv/bin/activate
    ```

4. Check the project configuration's validity and then install the project dependencies.

    ```
    (venv) $ poetry check
    ```

    ```
    (venv) $ poetry install
    ```

    Sample output

    ```
    All set!
    ```

    ```
    Installing dependencies from lock file

    Package operations: 37 installs, 0 updates, 0 removals

      - Installing certifi (2025.6.15)
      - Installing charset-normalizer (3.4.2)
      - Installing idna (3.10)
      - Installing urllib3 (2.5.0)
      - Installing distlib (0.3.9)
      - Installing iniconfig (2.1.0)
      - Installing platformdirs (4.3.8)
      - Installing packaging (25.0)
      - Installing filelock (3.18.0)
      - Installing pluggy (1.6.0)
      - Installing pygments (2.19.2)
      - Installing requests (2.32.4)
      - Installing smmap (5.0.2)
      - Installing cachetools (6.1.0)
      - Installing chardet (5.2.0)
      - Installing colorama (0.4.6)
      - Installing gitdb (4.0.12)
      - Installing cfgv (3.4.0)
      - Installing click (8.2.1)
      - Installing identify (2.6.12)
      - Installing coverage (7.9.1)
      - Installing mypy-extensions (1.1.0)
      - Installing nodeenv (1.9.1)
      - Installing pathspec (0.12.1)
      - Installing pyproject-api (1.9.1)
      - Installing pytest (8.4.1)
      - Installing pyyaml (6.0.2)
      - Installing requests-toolbelt (1.0.0)
      - Installing virtualenv (20.31.2)
      - Installing pre-commit (4.2.0)
      - Installing python-gitlab (6.0.0)
      - Installing tox (4.27.0)
      - Installing gitpython (3.1.44)
      - Installing responses (0.25.7)
      - Installing black (25.1.0)
      - Installing pytest-cov (6.2.1)
      - Installing ruff (0.12.0)

    Installing the current project: pagure-exporter (0.1.4)
    ```

## Usage

### Setup

1. Using an internet browser of your choice, open up [**Pagure**](https://pagure.io) and login to your account.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/01.png)

2. Click on your profile display picture and then, head over to the [**Account Settings**](https://pagure.io/settings) page.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/02.png)

3. Under the [**API Keys**](https://pagure.io/settings#nav-api-tab) section, click on the [**Create new API key**](https://pagure.io/settings/token/new) button in the top right corner.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/03.png)

4. As this is the source namespace, check all the ACLs that are required to read the asset information associated with a repository, set a safe expiration date for the API token and write an appropriate description for its usage before clicking on the [**Create**](#) button.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/04.png)

5. Make note of the API token generated and ensure that they are not shared with others or used for a different purpose.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/05.png)

6. Head over to a repository that the currently logged-in username has at least a READ access to.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/06.png)

7. Make note of the source namespace in the format of `HOLDER/REPONAME` where the `HOLDER` can be a group or a sole user.
   For example, in case of a repository located at `https://pagure.io/fedora-infra/ansible` - the source namespace would be `fedora-infra/ansible`.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/07.png)

8. In another internet browser tab or window, open up [**GitLab**](https://gitlab.com/) and login to your account.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/08.png)

9. Click on the [**New project/repository**](https://gitlab.com/projects/new) option from the sidebar of the profile page and then, click on the [**Create blank project**](https://gitlab.com/projects/new#blank_project) option.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/09.png)

10. Create a new empty repository which will act as the destination for the asset transfer. It is recommended to have the same name as the source namespace to avoid confusion, but it is not strictly required.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/10.png)

11. Head over to the created repository and make note of the **Project ID**.
    For example in this case, it is `42823949` for the destination repository named `gridhead/pagure-exporter-test`.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/11.png)

12. Expand the sidebar to head over to the [**Repository**](#) section from the [**Settings**](#) section.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/17.png)

13. In the [**Protected Branches**](#) section, turn off all existing *branch protection rules* and *allow force pushing* to all branches temporarily to allow for the repository assets to be moved in here.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/18.png)

14. Expand the sidebar to head over to the [**Access Tokens**](#) section from the [**Settings**](#) section.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/12.png)

15. In the [**Project Access Token**](#) page, click on the [**Add new token**](#) button to begin creating a new access token.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/13.png)

16. As this is the destination namespace, check all the scopes that are required to write the asset information associated with a repository, pick an appropriate role, set a safe expiration date and write an appropriate description for its usage before clicking on the [**Create project access token**](#) button.

    Refer [Project access tokens](https://docs.gitlab.com/user/project/settings/project_access_tokens/#scopes-for-a-project-access-token) for more information.

    TLDR;
    - Select `Developer` as the role for smooth migration
    - Select `api`, `read_api`, `read_repository`, `write_repository` as scopes for smooth migration

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/14.png)

17. Make note of the API token generated and ensure that they are not shared with others or used for a different purpose.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/15.png)

18. Ensure that you have the following information handy before proceeding to the next steps.

    1. Username of an account that has at least the READ permissions in the source namespace on Pagure (Say `srceuser`)
    2. Access token belonging to the aforementioned account with appropriate ACLs checked required for at least the READ permissions in the source namespace (Say `srcecode`)
    3. Name of the source namespace in the format `HOLDER/REPONAME` where the `HOLDER` can be a group or a sole user (Say `srcerepo`)
    4. Username of an account that has at least the WRITE permissions in the destination namespace on GitLab (Say `destuser`)
    5. Access token belonging to that aforementioned account appropriate roles and scopes required for at least the WRITE permissions in the destination namespace (Say `destcode`)
    6. Name of the destination namespace in the format of uniquely identifiable `PROJECTID` string (Say `destrepo`)

## Operate

### View help menu

1. Check the current version of the installed project as well as the usage information.

    ```
    (venv) $ pagure-exporter --version
    ```

    ```
    (venv) $ pagure-exporter --help
    ```

    Sample output

    ```
    Pagure Exporter by Akashdeep Dhar <t0xic0der@fedoraproject.org>, version 0.1.4
    ```

    ```
    Usage: pagure-exporter [OPTIONS] COMMAND [ARGS]...

      Pagure Exporter

    Options:
      -a, --splt TEXT  Source hostname for accessing Pagure information  [default:
                       pagure.io]
      -b, --dplt TEXT  Destination hostname for accessing GitLab information
                       [default: gitlab.com]
      -s, --srce TEXT  Source namespace for importing assets from  [required]
      -d, --dest TEXT  Destination namespace for exporting assets to  [required]
      -p, --pkey TEXT  Pagure API key for accessing the source namespace
                       [required]
      -g, --gkey TEXT  GitLab API key for accessing the destination namespace
                       [required]
      -f, --fusr TEXT  Username of the account that owns the Pagure API key
                       [required]
      -t, --tusr TEXT  Username of the account that owns the GitLab API key
                       [required]
      --version        Show the version and exit.
      --help           Show this message and exit.

    Commands:
      repo  Initialize transfer of repository assets
      tkts  Initiate transfer of issue tickets
    ```

2. Check the usage information of the available subcommands.

    ```
    (venv) $ pagure-exporter -a a -b a -s a -d a -p a -g a -f a -t a repo --help
    ```

    ```
    (venv) $ pagure-exporter -a a -b a -s a -d a -p a -g a -f a -t a tkts --help
    ```

    Sample output

    ```
    Usage: pagure-exporter repo [OPTIONS]

      Initialize transfer of repository assets

    Options:
      -b, --brcs TEXT  List of branches to extract
      --help           Show this message and exit.
    ```

    ```
    Usage: pagure-exporter tkts [OPTIONS]

      Initiate transfer of issue tickets

    Options:
      -s, --status [open|shut|full]  Extract issue tickets of the mentioned status
                                     [default: OPEN]
      -r, --ranges TEXT...           Extract issue tickets in the mentioned ranges
      -p, --select TEXT              Extract issue tickets of the selected numbers
      -c, --comments                 Transfer all the associated comments
      -l, --labels                   Migrate all the associated labels
      -a, --commit                   Assert issue ticket states as they were
      -t, --secret                   Confirm issue ticket privacy as they were
      -o, --series                   Ensure issue ticket sequence as they were
      --help                         Show this message and exit.
    ```

### Migrate repository files

1. Ensure that the location where the project repository was cloned is the present working directory and that the previously populated virtual environment is enabled.

    ```
    $ cd pagure-exporter
    ```

    ```
    $ source venv/bin/activate
    ```

2. Using an internet browser of your choice, visit the source namespace repository page on Pagure to pick the branches that you wish to transfer.

    ![](https://raw.githubusercontent.com/gridhead/pagure-exporter/main/data/16.png)

3. Execute the following command to begin migrating the repository assets from the source namespace on Pagure to the destination namespace on GitLab.

    1. If only a set of branches are to be migrated

        ```
        (venv) $ pagure-exporter \
                 --splt pagure.io --dplt gitlab.com \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 repo \
                 --brcs brca,brcb,brcc,brcd
        ```

        For a set of branches available in the source namespace named `brca`, `brcb`, `brcc` and `brcd` to be migrated to the destination namespace.

    2. If all the available branches are to be migrated

        ```
        (venv) $ pagure-exporter \
                 --splt pagure.io --dplt gitlab.com \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 repo
        ```

       This is the default behaviour of the subcommand so if no branch names are provided, all the branches from the source namespace are migrated

4. If there are any contents available in the branches of the destination namespace, they will be overwritten by the contents from the branches migrated from the source namespace.

### Migrate issue tickets

1. Ensure that the location where the project repository was cloned is the present working directory and that the previously populated virtual environment is enabled.

    ```
    $ cd pagure-exporter
    ```

    ```
    $ source venv/bin/activate
    ```

2. Execute the following command to begin extracting the issue tickets from the source namespace on Pagure to the destination namespace.

   1. If the issue tickets of a certain status need to be transferred.

      ```
      (venv) $ pagure-exporter \
                 --splt pagure.io --dplt gitlab.com \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --status open
      ```

   2. If the comments associated with the issue tickets need to be transferred.

      ```
      (venv) $ pagure-exporter \
                 --splt pagure.io --dplt gitlab.com \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --comments
      ```

   3. If the labels associated with the issue tickets need to be transferred.

      ```
      (venv) $ pagure-exporter \
                 --splt pagure.io --dplt gitlab.com \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --labels
      ```

   4. If the states associated with the issue tickets need to be transferred.

      ```
      (venv) $ pagure-exporter \
                 --splt pagure.io --dplt gitlab.com \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --commit
      ```

   5. If the privacy associated with the issue tickets need to be transferred.

      ```
      (venv) $ pagure-exporter \
                 --splt pagure.io --dplt gitlab.com \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --secret
      ```

    6. If the issue tickets need to be transferred in the sequence they were in.

     ```
     (venv) $ pagure-exporter \
                 --splt pagure.io --dplt gitlab.com \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --series
     ```

   7. If the issue tickets from a range of issue identities need to be transferred.

      ```
      (venv) $ pagure-exporter \
                 --splt pagure.io --dplt gitlab.com \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --ranges STRT STOP
      ```

      Issue tickets with identities `STRT`, `STRT+1` ... `STOP-1`, `STOP` would be considered here.

   8. If the issue tickets that need to be considered need to be cherry-picked.

      ```
      (venv) $ pagure-exporter \
                 --splt pagure.io --dplt gitlab.com \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --select NUM1,NUM2,NUM3 ...
      ```

      Issue tickets with identities `NUM1`, `NUM2`, `NUM3` ... would be considered here.

   While these options can be mixed and matched to be used together, the options `--ranges` and `--select` cannot be used at the same time as they perform identical functions.

   For example,

      1. The following command will migrate all issue tickets, the identities of which fall between the range of `STRT` and `STOP` both included, with status `OPEN` along with the associated comments, labels, privacy and identifiers.

         ```
         (venv) $ pagure-exporter \
                    --splt pagure.io --dplt gitlab.com \
                    --fusr srceuser --pkey srcecode --srce srcerepo \
                    --tusr destuser --gkey destcode --dest destrepo \
                    tkts \
                    --status open \
                    --comments \
                    --labels \
                    --secret \
                    --series \
                    --ranges STRT STOP
         ```

      2. The following command will migrate all issue tickets with the identities `NUM1`, `NUM2`, `NUM3` ... with status `SHUT` along with the associated labels, states, privacy and identifiers.

         ```
         (venv) $ pagure-exporter \
                    --splt pagure.io --dplt gitlab.com \
                    --fusr srceuser --pkey srcecode --srce srcerepo \
                    --tusr destuser --gkey destcode --dest destrepo \
                    tkts \
                    --status shut \
                    --labels \
                    --commit \
                    --secret \
                    --series \
                    --select NUM1,NUM2,NUM3 ...
         ```
