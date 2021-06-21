java -jar selenium-server-standalone-3.141.59.jar -role node \
-hub http://127.0.0.1:4444/grid/register \
-nodeConfig registerNode.json \
-Dwebdriver.chrome.driver=$(pwd)/../drivers/linux/chromedriver \
-Dwebdriver.ff.driver=$(pwd)/../drivers/linux/geckodriver \
-Dwebdriver.chrome.logfile="chrome.log" \
-Dwebdriver.firefox.logfile="ff.log" \
-Dwebdriver.ie.logfile="ie.log.txt"
