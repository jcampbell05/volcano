#  Volcano shell assembly operations.
#

# Arithmetic operators
#
add() {
    echo $(($1 + $2))
}

sub() {
    echo $(($1 - $2))
}

div() {
    if [ "$2" -ne 0 ]; then
        echo $(($1 / $2))
    else
        echo "Error: Division by zero" >&2
        exit 1
    fi
}

mul() {
    echo $(($1 * $2))
}