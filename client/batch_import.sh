#!/bin/bash
# insert target file into wtf database


LIST_FILE_LINE_IFS='%%'
TAGS_OVERRIDE='bytedance'

LIST_FILE_PATH=''
WTF=wtf

function show_help()
{
    echo batch import formatted content into wtf db line by line
    echo usage:
    echo     batch_import.sh target
    echo
    echo file content should be formatted as:
    echo '   {key}$LIST_FILE_LINE_IFS{value}$LIST_FILE_LINE_IFS{description}$LIST_FILE_LINE_IFS{tags}'
}

# $1 target file patch
function batch_import()
{
    while read line
    do
        KEY=`echo $line | awk -F $LIST_FILE_LINE_IFS '{print $1}'`
        VALUE=`echo $line | awk -F $LIST_FILE_LINE_IFS '{print $2}'`
        DESP=`echo $line | awk -F $LIST_FILE_LINE_IFS '{print $3}'`
        TAGS=`echo $line | awk -F $LIST_FILE_LINE_IFS '{print $4}'`

        if [ ! -z $TAGS_OVERRIDE ]
        then
            TAGS=$TAGS_OVERRIDE
        fi

        echo adding item:
        echo key: $KEY
        echo value: $VALUE
        echo desp: $DESP
        echo tags: $TAGS
        echo

        if [ ! -z $WTF ]
        then
            $WTF -a "$KEY" \"$VALUE\" $TAGS $DESP
        fi

    done < $1
}

# $1 LIST_FILE_PATH
function main()
{
    LIST_FILE_PATH=$1

    if [ ! -z $LIST_FILE_PATH ]  &&  [ -f $LIST_FILE_PATH ]
    then
        batch_import $LIST_FILE_PATH
    else
        show_help
    fi
}

# entrance
main $@
