
# follow https://wiki.icecube.wisc.edu/index.php/User_CVMFS#Mounting_the_CVMFS_staging_area_in_a_container
singularity exec -B /tmp:/tmp -B /cvmfs:/cvmfs -B /net/cvmfs_users:/cvmfs/icecube.opensciencegrid.org/users /cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el7:latest bash

eval $(/cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/setup.sh)
cd /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv
python -m venv --clear tensorflow_gpu_py3-v4.3.0
source tensorflow_gpu_py3-v4.3.0/bin/activate

pip install tensorflow==2.14.1 tensorflow_probability==0.22.1
pip install numpy scipy click pyyaml pandas matplotlib pybind11 uncertainties ruamel.yaml gitpython tqdm tables histlite bottleneck python-telegram-bot slackclient healpy xgboost mceq nuveto hirola
pip install --upgrade pip setuptools wheel packaging # extra otherwise not possible to install event-generator

perl -i -0pe 's/_OLD_VIRTUAL_PATH\="\$PATH"\nPATH\="\$VIRTUAL_ENV\/bin:\$PATH"\nexport PATH/_OLD_VIRTUAL_PATH\="\$PATH"\nPATH\="\$VIRTUAL_ENV\/bin:\$PATH"\nexport PATH\n\n# prepend virtual env path to PYTHONPATH if set\nif ! \[ -z "\$\{PYTHONPATH+_\}" \] ; then\n    _OLD_VIRTUAL_PYTHONPATH\="\$PYTHONPATH"\n    export PYTHONPATH\=\$VIRTUAL_ENV\/lib\/python3.11\/site-packages:\$PYTHONPATH\nfi/' tensorflow_gpu_py3-v4.3.0/bin/activate
perl -i -0pe 's/        export PYTHONHOME\n        unset _OLD_VIRTUAL_PYTHONHOME\n    fi/        export PYTHONHOME\n        unset _OLD_VIRTUAL_PYTHONHOME\n    fi\n\n    if ! \[ -z "\$\{_OLD_VIRTUAL_PYTHONPATH+_\}" \] ; then\n        PYTHONPATH\="\$_OLD_VIRTUAL_PYTHONPATH"\n        export PYTHONPATH\n        unset _OLD_VIRTUAL_PYTHONPATH\n    fi/' tensorflow_gpu_py3-v4.3.0/bin/activate

exit
singularity exec -B /tmp:/tmp -B /cvmfs:/cvmfs -B /net/cvmfs_users:/cvmfs/icecube.opensciencegrid.org/users /cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el7:latest bash

/cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/RHEL_7_x86_64/metaprojects/icetray/v1.12.0/env-shell.sh
cd /cvmfs/icecube.opensciencegrid.org/users/tvaneede/venv
source tensorflow_gpu_py3-v4.3.0/bin/activate

# install event-generator
cd /cvmfs/icecube.opensciencegrid.org/users/tvaneede/event-generator
git clone git@github.com:icecube/event-generator.git v2.0.0_master
cd v2.0.0_master
pip install -e . --no-deps

# aux packaages
cd /cvmfs/icecube.opensciencegrid.org/users/tvaneede
mkdir ic3-data
cd ic3-data
git clone git@github.com:icecube/ic3-data.git v1.0.1_master
cd v1.0.1_master
pip install .

cd /cvmfs/icecube.opensciencegrid.org/users/tvaneede
mkdir TFScripts
cd TFScripts
git clone git@github.com:icecube/TFScripts.git v1.0.1_master
cd v1.0.1_master
pip install .