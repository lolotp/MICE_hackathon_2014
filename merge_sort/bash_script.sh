awk < $1 -F'|' '{print $3}' | sort | uniq|wc -l
awk < $1 -F'|' '{print $5}' | sort | uniq|wc -l #got bug here, can't handle when '|' character is inside token

