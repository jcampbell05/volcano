# The Volcano runtime library.
#
LOG_FILE=$(mktemp)
tail -f $LOG_FILE &

# TODO: Inject in the AST and user volcano.shell to wrap pre-defined functions
#
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

# TODO: 
#
# Find way to mix .vol and .vsh code together
# so we can extend it from array and have pythonic code
# or perhaps we can jsut put this code in the AST directly.
#
array_append () {

    local array="$1"
    local val="$2"

    set -- $array
    set -- "$@" "$val"
    
    RESULT="$@"
}

export () {
    name = $1
    value = $2

    export $name=$value
}

# End of Volcano runtime library.
#