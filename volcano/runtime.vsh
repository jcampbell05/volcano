# The Volcano runtime library.
#
LOG_FILE=$(mktemp)
tail -f $LOG_FILE &

print () {
    echo "$1" >> $LOG_FILE
}

# End of Volcano runtime library.
#