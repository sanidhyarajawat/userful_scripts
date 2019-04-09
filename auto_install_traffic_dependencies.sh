echo "Beginning to install traffic dependencies>>>>"
touch /home/qet/Documents/detailed_status.txt
#echo "1" >> /home/qet/Documents/progress_bar.txt
echo "Updating..." >> /home/qet/Documents/detailed_status.txt
if sudo apt-get update; then echo ""
else
    echo "Unable to update system. Please try manually: sudo apt-get update" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "5" >> /home/qet/Documents/progress_bar.txt
echo "Installing git" >> /home/qet/Documents/detailed_status.txt
if sudo apt-get install git -y; then echo ""
else
    echo "Unable to install git. Please try manually: sudo apt-get install git" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "10" >> /home/qet/Documents/progress_bar.txt
echo "Installing vim" >> /home/qet/Documents/detailed_status.txt
if sudo apt-get install vim -y; then echo ""
else
    echo "Unable to install vim. Please try manually: sudo apt-get install vim" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "15" >> /home/qet/Documents/progress_bar.txt
echo "Installing python-twisted" >> /home/qet/Documents/detailed_status.txt
if sudo apt-get install python-twisted -y; then echo ""
else
    echo "Unable to install python-twisted. Please try manually: sudo apt-get install python-twisted" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "20" >> /home/qet/Documents/progress_bar.txt
echo "Installing build-essential" >> /home/qet/Documents/detailed_status.txt
if sudo apt-get install build-essential -y; then echo ""
else
    echo "Unable to install build-essential. Please try manually: sudo apt-get install build-essential" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "25" >> /home/qet/Documents/progress_bar.txt
echo "Installing python-dev" >> /home/qet/Documents/detailed_status.txt
if sudo apt-get install python-dev -y; then echo ""
else
    echo "Unable to install python-dev. Please try manually: sudo apt-get install python-dev" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "30" >> /home/qet/Documents/progress_bar.txt
echo "Installing python-pip" >> /home/qet/Documents/detailed_status.txt
if sudo apt-get install python-pip -y; then echo ""
else
    echo "Unable to install python-pip. Please try manually: sudo apt-get install python-pip" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "35" >> /home/qet/Documents/progress_bar.txt
echo "Adding key" >> /home/qet/Documents/detailed_status.txt
if sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10 ; then echo ""
else
    echo "Unable to install keyserver. Please try manually: sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "40" >> /home/qet/Documents/progress_bar.txt
echo "Initilizing mongodb repo" >> /home/qet/Documents/detailed_status.txt
if echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list; then echo ""
else
    echo "Unable to initialize mongodb repo. Please try manually: echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "45" >> /home/qet/Documents/progress_bar.txt
echo "Updating..." >> /home/qet/Documents/detailed_status.txt
if sudo apt-get update; then echo ""
else
    echo "Unable to update system. Please try manually: sudo apt-get update" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "50" >> /home/qet/Documents/progress_bar.txt
echo "Installing python-pycurl" >> /home/qet/Documents/detailed_status.txt
if sudo apt-get install python-pycurl -y; then echo ""
else
    echo "Unable to install python-pycurl. Please try manually: sudo apt-get install python-pycurl" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "55" >> /home/qet/Documents/progress_bar.txt
echo "Installing mongodb 2.6.10" >> /home/qet/Documents/detailed_status.txt
if sudo apt-get install -y mongodb-org=2.6.10 mongodb-org-server=2.6.10 mongodb-org-shell=2.6.10 mongodb-org-mongos=2.6.10 mongodb-org-tools=2.6.10; then echo ""
else
    echo "Unable to install mongodb 2.6.10. Please try manually: sudo apt-get install -y mongodb-org=2.6.10 mongodb-org-server=2.6.10 mongodb-org-shell=2.6.10 mongodb-org-mongos=2.6.10 mongodb-org-tools=2.6.10" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "60" >> /home/qet/Documents/progress_bar.txt
echo "Installing pymongo" >> /home/qet/Documents/detailed_status.txt
if sudo pip install pymongo==2.8; then echo ""
else
    echo "Unable to install pymongo. Please try manually: sudo pip install pymongo==2.8" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "65" >> /home/qet/Documents/progress_bar.txt
echo "Installing dateutils" >> /home/qet/Documents/detailed_status.txt
if sudo pip install dateutils; then echo ""
else
    echo "Unable to install dateutils. Please try manually: sudo pip install dateutils" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "70" >> /home/qet/Documents/progress_bar.txt
echo "Installing xlwt" >> /home/qet/Documents/detailed_status.txt
if sudo pip install xlwt; then echo ""
else
    echo "Unable to install xlwt. Please try manually: sudo pip install xlwt" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "75" >> /home/qet/Documents/progress_bar.txt
echo "Installing xlrd" >> /home/qet/Documents/detailed_status.txt
if sudo pip install xlrd; then echo ""
else
    echo "Unable to install xlrd. Please try manually: sudo pip install xlrd" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "80" >> /home/qet/Documents/progress_bar.txt
echo "Installing num2words" >> /home/qet/Documents/detailed_status.txt
if sudo pip install num2words; then echo ""
else
    echo "Unable to install num2words. Please try manually: sudo pip install num2words" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "90" >> /home/qet/Documents/progress_bar.txt
echo "Installing python-xlsxwriter" >> /home/qet/Documents/detailed_status.txt
if sudo apt-get install python-xlsxwriter; then echo ""
else
    echo "Unable to install python-xlsxwriter. Please try manually: sudo apt-get install python-xlsxwriter" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"

#echo "100" >> /home/qet/Documents/progress_bar.txt
echo "Installing requests" >> /home/qet/Documents/detailed_status.txt
if sudo pip install requests; then echo ""
else
    echo "Unable to install requests. Please try manually: sudo pip install requests" >> /home/qet/Documents/failed_install.txt
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "******************************************************************************************************"
echo "COMPLETED."
