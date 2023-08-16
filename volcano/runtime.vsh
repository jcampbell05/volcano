# The Volcano runtime library.
#
LOG_FILE=$(mktemp)
tail -f $LOG_FILE &

call () {
    RESULT=

    # Get the function name and shift the arguments
    func="$1"
    shift

    # Call the function with the remaining arguments
    "$func" "$@"
    
    echo $RESULT
}

print () {
    echo "$1" >> $LOG_FILE
}

input () {
    read -p "$1" RESULT >> $LOG_FILE
}

# End of Volcano runtime library.
#