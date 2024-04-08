if [[ $PWD = "/mnt/code" ]];
then cd "/mnt/artifacts/"; fi

#list all python packages and versions installed in environment
pip list > packages_start.txt;