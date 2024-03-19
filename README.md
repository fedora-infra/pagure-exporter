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
    Requirement already satisfied: pagure-exporter in ./venv/lib/python3.12/site-packages (0.1.0)
    Requirement already satisfied: GitPython<4.0.0,>=3.1.37 in ./venv/lib/python3.12/site-packages (from pagure-exporter) (3.1.40)
    Requirement already satisfied: click<9.0.0,>=8.1.3 in ./venv/lib/python3.12/site-packages (from pagure-exporter) (8.1.7)
    Requirement already satisfied: requests<3.0.0,>=2.31.0 in ./venv/lib/python3.12/site-packages (from pagure-exporter) (2.31.0)
    Requirement already satisfied: tqdm<5.0.0,>=4.64.1 in ./venv/lib/python3.12/site-packages (from pagure-exporter) (4.66.1)
    Requirement already satisfied: gitdb<5,>=4.0.1 in ./venv/lib/python3.12/site-packages (from GitPython<4.0.0,>=3.1.37->pagure-exporter) (4.0.10)
    Requirement already satisfied: charset-normalizer<4,>=2 in ./venv/lib64/python3.12/site-packages (from requests<3.0.0,>=2.31.0->pagure-exporter) (3.3.0)
    Requirement already satisfied: idna<4,>=2.5 in ./venv/lib/python3.12/site-packages (from requests<3.0.0,>=2.31.0->pagure-exporter) (3.4)
    Requirement already satisfied: urllib3<3,>=1.21.1 in ./venv/lib/python3.12/site-packages (from requests<3.0.0,>=2.31.0->pagure-exporter) (2.0.7)
    Requirement already satisfied: certifi>=2017.4.17 in ./venv/lib/python3.12/site-packages (from requests<3.0.0,>=2.31.0->pagure-exporter) (2023.7.22)
    Requirement already satisfied: smmap<6,>=3.0.1 in ./venv/lib/python3.12/site-packages (from gitdb<5,>=4.0.1->GitPython<4.0.0,>=3.1.37->pagure-exporter) (5.0.1)
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

    Package operations: 19 installs, 0 updates, 0 removals

      • Installing smmap (5.0.0)
      • Installing certifi (2022.12.7)
      • Installing charset-normalizer (3.0.1)
      • Installing click (8.1.3)
      • Installing gitdb (4.0.10)
      • Installing idna (3.4)
      • Installing mccabe (0.6.1)
      • Installing mypy-extensions (0.4.3)
      • Installing pathspec (0.11.0)
      • Installing platformdirs (2.6.2)
      • Installing pycodestyle (2.8.0)
      • Installing pyflakes (2.4.0)
      • Installing urllib3 (1.26.14)
      • Installing black (22.12.0)
      • Installing flake8 (4.0.1)
      • Installing gitpython (3.1.30)
      • Installing isort (5.12.0)
      • Installing requests (2.28.2)
      • Installing tqdm (4.64.1)

    Installing the current project: pagure-exporter (0.1.0)
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
    Pagure Exporter by Akashdeep Dhar <t0xic0der@fedoraproject.org>, version 0.1.0
    ```

    ```
    Usage: pagure-exporter [OPTIONS] COMMAND [ARGS]...

    Options:
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
    (venv) $ pagure-exporter -s a -d a -p a -g a -f a -t a repo --help
    ```

    ```
    (venv) $ pagure-exporter -s a -d a -p a -g a -f a -t a tkts --help
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
      -s, --status [OPEN|SHUT|FULL]  Extract issue tickets of the mentioned status
                                     [default: OPEN]
      -r, --ranges TEXT...           Extract issue tickets in the mentioned ranges
      -p, --select TEXT              Extract issue tickets of the selected numbers
      -c, --comments                 Transfer all the associated comments
      -l, --labels                   Migrate all the associated labels
      -a, --commit                   Assert issue ticket states as they were
      -t, --secret                   Confirm issue ticket privacy as they were
      -o, --series                   Ensure issue tickets sequence as they were
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
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 repo \
                 --brcs brca,brcb,brcc,brcd
        ```

        For a set of branches available in the source namespace named `brca`, `brcb`, `brcc` and `brcd` to be migrated to the destination namespace.

    2. If all the available branches are to be migrated

        ```
        (venv) $ pagure-exporter \
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
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --status open
      ```

   2. If the comments associated with the issue tickets need to be transferred.

      ```
      (venv) $ pagure-exporter \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --comments
      ```

   3. If the labels associated with the issue tickets need to be transferred.

      ```
      (venv) $ pagure-exporter \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --labels
      ```

   4. If the states associated with the issue tickets need to be transferred.

      ```
      (venv) $ pagure-exporter \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --commit
      ```

   5. If the privacy associated with the issue tickets need to be transferred.

      ```
      (venv) $ pagure-exporter \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --secret
      ```

    6. If the issue tickets need to be transferred in the sequence they were in.

     ```
     (venv) $ pagure-exporter \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --series
     ```

   7. If the issue tickets from a range of issue identities need to be transferred.

      ```
      (venv) $ pagure-exporter \
                 --fusr srceuser --pkey srcecode --srce srcerepo \
                 --tusr destuser --gkey destcode --dest destrepo \
                 tkts \
                 --ranges STRT STOP
      ```

      Issue tickets with identities `STRT`, `STRT+1` ... `STOP-1`, `STOP` would be considered here.

   8. If the issue tickets that need to be considered need to be cherry-picked.

      ```
      (venv) $ pagure-exporter \
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
