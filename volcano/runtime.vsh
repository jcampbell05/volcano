# The Volcano runtime library.
#
LOG_FILE=$(mktemp)
tail -f $LOG_FILE &

print () {
    echo "$1" >> $LOG_FILE
}

input () {
    read -p "$1" RESULT
}

# End of Volcano runtime library.
#