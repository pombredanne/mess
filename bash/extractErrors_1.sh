#!/bin/bash
#USAGE:
# ./extractErrors.sh month day fester
YEAR=`date +%Y`
#DIR='/mnt/syslog/sx-banking-all/2014/05/17'
DIR="/mnt/syslog/sx-banking-all/$YEAR/$1/$2"
#FESTER='fester-8'
FESTER=$3
OUTFILE=$DIR/$FESTER_ERRORS
HISTFILE=$DIR/$FESTER_ERRORS_Hist
FILELIST=`ls -1 $DIR/$FESTER`

#echo "Starting..."
#echo "Getting Errors from $DIR/$FESTER/$file..."

find $DIR/$FESTER -type f | \
parallel -k -j150% -n 1000 -m zgrep -H -a \"ERROR\" {} | strings |\
grep -v "\[AbstractClientHandler\] : Unexpected error with client" | \
grep -v "\[AccountLoader\] : Failed to load customers beneficiaries list" | \
grep -v "\[AbstractClientHandler\] : Failed to send message"| \
grep -v "\[LogonController\] : User logon failed"| \
grep -v "\[PaymentConfirmView\] : UI Validation failed"| \
grep -v "\[LogonController\] : User logon failed"| \
grep -v "\[ClusterServer\] : Failed to process incoming command" | \
grep -v "\[LogonController\] : User logon failed" | \
grep -v "\[AccountLoader\] : Failed to load customers beneficiaries list" | \
grep -v "\[GomezEchoServerModule\] : Unexpected error occured"| \
grep -v "\[TransferConfirmView\] : UI Validation failed, sending client error view"| \
grep -v "\[ThingConnection\] : Unexpected error with thing"| \
grep -v "\[ThingConnection\] : Close connection..."| \
grep -v "\[isPairedController\] : Device linking has not been confirmed by customer on online yet for device"| \
grep -v "\[TransferDoView\] : Failed to perform transfer due to VODS exception"| \
grep -v "\[PairController\] : Unable to pair device as username enetered does not exist"| \
grep -v "\[TransferConfirmView\] : UI Validation failed, sending client error view"| \
grep -v "\[PaymentDoView\] : Failed to perform payment due to VODS exception"| \
grep -v "\[WESTransactionHistoryRequestHandler\] : Failed to get detailed balance on requested account"| \
grep -v "ERROR READING THE DD" | \
grep -v "balanceResponseMessage\=ERROR RETRIEVING BALANCE" | \
grep -v "ERROR RETRIEVING BALANCE" | \
grep -v "Retreived Customer" | \
grep -v "IO Error Connecting and Servicing Async\[FCNBN[34][0-9][0-9]_[GN][HA][AM]\]" | cut -c 1-500 > $DIR/$3_ERRORS.txt

# Extract Error class, the additional grep is to cater for annoying lines from VODS responses
cat $DIR/$3_ERRORS.txt | grep sx-banking-all| awk 'BEGIN {FS="] : "}; {print $2 "] : " $3}' > $3_ERRORS_tmp.txt

# Split sorting over all cores to try and speed it up
split -l200000 $3_ERRORS_tmp.txt '_tmp';

for FILE in `ls -1 _tmp*`
	do sort $FILE -o $FILE &
done
# Wait for subprocesses to finish before merging
wait

sort -m _tmp* |uniq -c | sort -rn >  $DIR/$3_ERRORS_Hist.txt

cat $3_ERRORS_tmp.txt | cut -f1 -d',' | sort | uniq -c |sort -rn > $DIR/$3_ERRORS_Hist.txt

rm -f *_tmp*

#echo "Done"
