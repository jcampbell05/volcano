#!/usr/bin/env /bin/sh
# Generated by Volcano from hello-world.vol

set -o posix
set -e

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

hello_world_say_hello () {
    RESULT=
    local name=${1:-World}
    hello_world_say_hello_ken_error () {
        RESULT=
        print "Warning Ken detected"
     }

    hello_world_say_hello_check_for_ken () {
        RESULT=
        if [ "$name" = "Ken" ]
        then
            hello_world_say_hello_ken_error 
            RESULT=
            echo "$RESULT"
            return 
        fi

     }

    hello_world_say_hello_check_for_ken
    print "- Hello $name!"
 }

hello_world_goodbye () {
    RESULT=
    local name=${1:-}
    RESULT="Goodbye $name"
    echo "$RESULT"
    return
 }

print "Welcome to Volcano 🌋"
print "Today is $( date )"
print "====================== 
"
print "Here are some examples:"
names="Barbie\ Ken\ $( whoami )"
total_names=3.0
slices_of_pie=6.0
slices_of_pie_each=$( awk "BEGIN {print $slices_of_pie/$total_names}")
number="$( input "Pick a number:" )"
if [ "$number" -lt 2 ]
then
    print "$number is smaller then 2" 
else
    if [ 1 -gt 2 ]
    then
        print "$number is greater then 2" 
    else
        if [ "$number" = 2 ] && [ 2 = "$number" ]
        then
            print "{number} equals 2 and 2 equals {number}" 
        else
            if [  ! "$number" ]
            then
                print "$number is not true" 
            else
                print "None of these are true for $number" 
            fi
 
        fi
 
    fi
 
fi

if [ 3 = 3 ] || [ 4 = 4 ]
then
    print "3 is 3 or 4 is 4" 
else
    print "3 is not 3" 
fi

i="$number"
while [ "$i" -gt 0 ]
do
    print "Counting down... $i" 
    sleep 1 
    i=$( awk "BEGIN {print $i-1}") 
done
print "Countdown done" 

print ""
for name in $names;
do
    hello_world_say_hello "$name"
done
hello_world_say_hello
print "There are $slices_of_pie_each for each of you. $slices_of_pie / $total_names = $slices_of_pie_each"
hello_world_list_comp_1 () {
    RESULT=
    ACCUMULATED=
    for name in $names;
    do
        RESULT="$( print "$( hello_world_goodbye "$name" )" )"
        array_append "$ACCUMULATED" "$RESULT"
        ACCUMULATED="$RESULT"
    done
    RESULT="$ACCUMULATED"
    echo "$RESULT"
    return
 }

hello_world_list_comp_1
print "A second round of goodbyes for luck"
hello_world_list_comp_2 () {
    RESULT=
    ACCUMULATED=
    for name in $names;
    do
        RESULT="$( hello_world_goodbye "$name" )"
        array_append "$ACCUMULATED" "$RESULT"
        ACCUMULATED="$RESULT"
    done
    RESULT="$ACCUMULATED"
    echo "$RESULT"
    return
 }

goodbyes="$( hello_world_list_comp_2 )"
print "$goodbyes"
