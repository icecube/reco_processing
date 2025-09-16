
# follow https://wiki.icecube.wisc.edu/index.php/User_CVMFS#Mounting_the_CVMFS_staging_area_in_a_container
singularity exec -B /tmp:/tmp -B /cvmfs:/cvmfs -B /net/cvmfs_users:/cvmfs/icecube.opensciencegrid.org/users /cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el7:latest bash

# then https://wiki.icecube.wisc.edu/index.php/User_CVMFS
eval $(/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/setup.sh)
mkdir /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv
cd /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv
python3 -m venv --system-site-packages py3-v4.4.1_reco-v1.1.0
source py3-v4.4.1_reco-v1.1.0/bin/activate

# download reco
mkdir /cvmfs/icecube.opensciencegrid.org/users/tvaneede/reco
cd /cvmfs/icecube.opensciencegrid.org/users/tvaneede/reco
git clone git@github.com:icecube/reco.git v1.1.0
cd v1.1.0
git fetch origin
git checkout 7f46745
pip install .

###
### first it didnt work!! here I tried locally, this seems to work. problem was virtualenv vs venv
###
cd /data/user/tvaneede/software/py_venvs/test_iceprod_reco
eval $(/cvmfs/icecube.opensciencegrid.org/py3-v4.4.1/setup.sh)
python3 -m venv --system-site-packages py3-v4.4.1_reco-v1.1.0
source py3-v4.4.1_reco-v1.1.0/bin/activate
git clone git@github.com:icecube/reco.git v1.1.0
cd v1.1.0
git fetch origin
git checkout 7f46745
pip install .