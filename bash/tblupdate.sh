#!/bin/bash

#################################################################################################
# AUTHOR: Tiago Baptista                                                                        #
# Purpose: Taking date as input <yymmdd>, loops though tables and log files to pre-process data #
#################################################################################################

# STATIC VARIABLES
##################
date=$2
cmd='mysql -u admin -pshark -P3311 mail_logs'
folderdate=$(date -d $(echo $date) '+%Y/%m/%d')

#FUNCTIONS
#################
createtbl() {
$cmd -e "alter table logs$date add email_address varchar(64) default null, add processed int default 0, add msg_id varchar(32) default NULL, add index \`email_address\` (\`email_address\`), add index \`msg_id\` (\`msg_id\`), add index \`processed\` (\`processed\`)";
$cmd -e "CREATE TABLE logs_status_$date ( \
	\`pkey\` bigint(20) unsigned not NULL auto_increment, \
	\`datetime\` datetime DEFAULT NULL, \
	\`log\` text, \
	\`seq\` bigint(20) unsigned DEFAULT NULL, \
	\`email_address\` varchar(64) DEFAULT NULL, \
	\`status\` varchar(12) default null, \
	\`msg_id\` varchar(32) default NULL, \
	PRIMARY KEY (\`pkey\`), \
	KEY \`datetime\` (\`datetime\`), \
	INDEX \`msg_id\` (\`msg_id\`), \
	INDEX \`email_address\` (\`email_address\`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
}

createcsv() {
if [ -f /tmp/insert ]; then
	rm /tmp/insert*
fi

bzcat /var/log/servers/mats-sa-mail-L-1-b/$folderdate/maillog.bz2 /var/log/servers/mob-sa-mail-L-3-r1/$folderdate/maillog.bz2 |\
grep "status=" | egrep -v "status=expired|orig_to=<root>|to=<inContact@fnb.co.za>"  >> /tmp/insert


# Use python for faster csv creation
python - <<END
day = $date
csv = open('/tmp/insert.csv', 'ab+')

with open('/tmp/insert') as f:
	for line in f:
		data = line.split(']: ')[1]
		dt = str(day) + " " + line.split()[2]
		csv.write(dt + "|" + data.split('\n')[0] + '\n')
csv.close()
END
}

loadcsv() {
$cmd -e "LOAD DATA LOCAL INFILE '/tmp/insert.csv' \
                INTO TABLE logs_status_$date \
                FIELDS TERMINATED BY '|' \
                LINES TERMINATED BY '\n' \
                (@datetime, log) \
                SET datetime = STR_TO_DATE(@datetime, '%y%m%d %H:%i:%s')"

rm /tmp/insert*
}

quickdel() {
day=$date

echo "Deleting for $day"

# Get 2x duplicates first to get rid of the initial load
$cmd -e "create table tbl$day as (select seq from logs$day group by msg having count(msg) > 1)"
records=`$cmd -e "select count(*) from tbl$day\G" | grep count | awk '{print $2}'`
echo "Going to delete $records records..."
$cmd -e "delete a.* from logs$day as a inner join tbl$day as b on a.seq = b.seq;"
$cmd -e "drop table tbl$day"

# Now check for stragglers with more than 2x duplicates
$cmd -e "create table tbl$day as (select a.seq from logs$day a inner join (select msg from logs$day group by msg having count(msg) > 1) b on a.msg=b.msg)"
records=`$cmd -e "select count(*) from tbl$day\G" | grep count | awk '{print $2}'`
echo "Going to delete $records stragglers..."
$cmd -e "delete a.* from logs$day as a inner join tbl$day as b on a.seq = b.seq;"
$cmd -e "drop table tbl$day"
records=`$cmd -e "select count(*) from logs$day\G" | grep count | awk '{print $2}'`

echo "Done deleting, left with $records unique logs."
}

runall() {
echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo $(date)
echo "1: Starting alter + index for $date..."
createtbl
echo" 2: Starting with CSV loader..."
createcsv
loadcsv
echo "3: Starting duplicate removal on regular logs..."
quickdel
echo "4: Starting logs and status processor..."
/usr/bin/python /home/f3902293/MaillogsDBProcessor.py --date=$date
echo "Done!"
}

# MAIN
###################
case $1 in
	run)
	runall
	;;

	del)
	quickdel
	;;
	
	csv)
	createcsv
	loadcsv
	;;

	*)
	echo $"Usage: $0 {run|del|csv} {yymmdd}"
	exit 1
esac
