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

# Array API
#

define_array() {
    eval $1=0
}

array_append () {
    local idx
    eval ${$1}_$idx=$2
    idx=$(
        add ${$1} 1
    )
}

# End of Volcano runtime library.
#