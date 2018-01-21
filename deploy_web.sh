#!/bin/zsh
# This script is used to deploy the Theochrone website
source packager/commonpackagerfunctions.sh

mkdir _deploy_tmp
cp -r programme ./_deploy_tmp

cd _deploy_tmp
rm -r **/.* # deleting all files starting by .
cd programme
rm -r gui 

mv images/fetes web/kalendarium/static/ # for the images of saints
cd web
print Compiling translation files...
django-admin compilemessages
print Please put shtml in the right repertory. Do not forget base widget nor light widget !
./manage.py shell
# changing some lines
line_to_modify='    fpath = os.path.abspath(chemin + "/../spill/static/spill") + "/"'
line_modified='    fpath = os.path.abspath(chemin + "/static/spill") + "/"'
fcm.modify_lines kalendarium/views.py $line_to_modify $line_to_modify
print "DEBUG = False" >> ./web/settings.py
print "ALLOWED_HOSTS = ['theochrone.fr','www.theochrone.fr','theochrone.ga','www.theochrone.ga']" >> ./web/settings.py

cd ../../ # returning to _deploy_tmp
scp -P 22 theochrone@ssh-theochrone-alwaysdata.net:/home/theochrone/_twit_auth ./programme/
scp -P 22 -r programme theochrone@ssh-theochrone.alwaysdata.net:/home/theochrone/

cd .. # returning to wip_fetes
rm -r _deploy_tmp