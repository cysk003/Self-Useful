for i in `seq 1 9999`;
 do
   tvid=`printf %04d $i`
   url="http://111.20.33.70/PLTV/88888888/224/322123${tvid}/index.m3u8"
   result=`curl -i  $url 2>/dev/null | grep "200 OK"|wc -l`
   echo $url, $result
   url="http://111.20.33.70/PLTV/88888888/224/322123${tvid}/index.m3u8"
   if [ $result -gt 0 ]; then
       echo $i,$url >> ./id.txt
   fi
 done
