#!/bin/bash

commands=${*}

if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then 
    echo "Running Interactively" ; 
else
    echo "Running In Batch"
    (>&2 echo "Starting job on " `date`) # Date/time of start of job
    (>&2 echo "Running on: `uname -a`") # Condor job is running on this node
    (>&2 echo "System software: `cat /etc/redhat-release`") # Operating System on that node

    #Copy tarred CMSSW area from eos
    xrdcp root://cmseos.fnal.gov//store/user/dnoonan/HGCAL_Concentrator/ttbarDAQntupleCode_CMSSW_11_1_0_pre6.tgz .

    source /cvmfs/cms.cern.ch/cmsset_default.sh

    echo "tar -xvf ttbarDAQntupleCode_CMSSW_11_1_0_pre6.tgz"
    tar -xzf ttbarDAQntupleCode_CMSSW_11_1_0_pre6.tgz

    rm CMSSW_11_1_0_pre6.tgz

    cd CMSSW_11_1_0_pre6/src/

    eval `scram b ProjectRename `

    eval `scramv1 runtime -sh`
    cd L1Trigger/L1THGCalUtilities/test
    cp ${_CONDOR_SCRATCH_DIR}/ttbarV11_cfg.py .
fi

echo "cmsRun ttbarV11_cfg.py $commands"
cmsRun ttbarV11_cfg.py $commands
# echo "cmsRun hgcalProducer_cfg.py $commands"
# cmsRun hgcalProducer_cfg.py $commands

if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then 
    echo "Running Interactively" ; 
else
    echo "Copying files to eos and cleaning up" ; 
    xrdcp -rf ntuple*root root://cmseos.fnal.gov//store/user/lpchgcal/ConcentratorNtuples/L1THGCal_Ntuples/TTbar_v11

    rm ntuple*root
    cd ${_CONDOR_SCRATCH_DIR}
    rm -rf CMSSW_11_1_0_pre6
fi
