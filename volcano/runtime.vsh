# The Volcano runtime library.
#
LOG_FILE=$(mktemp)

tail -f "$LOG_FILE" &

print () {
    echo "$1" >> "$LOG_FILE"
}

input () {
    read -r -p "$1" RESULT >> "$LOG_FILE"
}

array_append () {

    local array="$1"
    local val="$2"

    set -- "$array"
    set -- "$@" "$val"
    
    RESULT="$*"
}

# End of Volcano runtime library.
#