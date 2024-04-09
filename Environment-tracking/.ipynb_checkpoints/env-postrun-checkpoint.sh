if [[ $PWD = "/mnt/code" ]];
then cd "/mnt/artifacts/"; fi

#list all python packages and versions installed in environment at the end of a code session
pip list > tmp.txt

#search for differences from package list at the beginning of the session
comm -13  <(sort packages_start.txt) <(sort tmp.txt) > session_packages_not_in_environment.txt

python environment-report.py

#remove extra files
rm session_packages_not_in_environment.txt
rm tmp.txt
rm packages_start.txt
