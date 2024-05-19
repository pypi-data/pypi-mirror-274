#!/usr/bin/env sh


export VERSION=0.0.2

export NAME=mychamp

DESCRIPTION='Stub files to use as the basis of a Python project that'
export DESCRIPTION="${DESCRIPTION} can be packaged and uploaded to PyPI"

export GITHUB_USER='striebel'

export AUTHOR='Jacob Striebel'
export AUTHOR_EMAIL='jacob.striebel@example.com'

export DATA_FILE_PATH_SUFFIXES='meta.sh:data/quote.txt' # When more needed, separate with colon (:)


# logging level str options:
#
#     CRITICAL, ERROR, WARNING, INFO, DEBUG
#
export DEFAULT_LOGGING_LEVEL_STR='DEBUG'


# # # #
# 
# Do not modify statements below this line
#

printf 'global VERSION                  \n'
printf 'global NAME                     \n'
printf 'global DESCRIPTION              \n'
printf 'global GITHUB_USER              \n'
printf 'global AUTHOR                   \n'
printf 'global AUTHOR_EMAIL             \n'
printf 'global DATA_FILE_PATH_SUFFIXES  \n'
printf 'global DEFAULT_LOGGING_LEVEL_STR\n'

printf 'VERSION                   = "%s"\n' $VERSION
printf 'NAME                      = "%s"\n' $NAME
printf 'DESCRIPTION               = "%s"\n' "$DESCRIPTION"
printf 'GITHUB_USER               = "%s"\n' $GITHUB_USER
printf 'AUTHOR                    = "%s"\n' $AUTHOR
printf 'AUTHOR_EMAIL              = "%s"\n' $AUTHOR_EMAIL
printf 'DATA_FILE_PATH_SUFFIXES   = "%s"\n' $DATA_FILE_PATH_SUFFIXES
printf 'DEFAULT_LOGGING_LEVEL_STR = "%s"\n' $DEFAULT_LOGGING_LEVEL_STR
