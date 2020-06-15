import FWCore.ParameterSet.Config as cms 

from Configuration.Eras.Era_Phase2C9_cff import Phase2C9
process = cms.Process('DIGI',Phase2C9)

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.register("job", 1, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("Nevents", -1, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.parseArguments()

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D46Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D46_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC14TeV_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.Nevents)
)

# Input source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('root://eoscms.cern.ch//eos/cms/store/cmst3/group/hgcal/CMG_studies/Production/ttbar_ttbar_v11_aged_unbiased_20191101/GSD/physprocttbar_x100_ttbar-1.0To-1.0_GSD_%i.root'%options.job),


#       fileNames = cms.untracked.vstring('file:physprocttbar_x100_ttbar-1.0To-1.0_GSD_2.root'),
#       skipEvents=cms.untracked.uint32(),
       inputCommands=cms.untracked.vstring(
           'keep *',
           'drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT',
           'drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT',
           'drop l1tEMTFHit2016s_simEmtfDigis__HLT',
           'drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT',
           'drop l1tEMTFTrack2016s_simEmtfDigis__HLT',
           'drop FTLClusteredmNewDetSetVector_mtdClusters_FTLBarrel_RECO',
           'drop FTLClusteredmNewDetSetVector_mtdClusters_FTLEndcap_RECO',
           'drop MTDTrackingRecHitedmNewDetSetVector_mtdTrackingRecHits__RECO',
           'drop BTLDetIdBTLSampleFTLDataFrameTsSorted_mix_FTLBarrel_HLT',
           'drop ETLDetIdETLSampleFTLDataFrameTsSorted_mix_FTLEndcap_HLT',
           )
       )

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('SingleElectronPt10_cfi nevts:10'),
    name = cms.untracked.string('Applications')
)

# Output definition
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string("ntuple_ttbar_ttbar_v11_aged_unbiased_20191101_%i.root"%options.job)
    )

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

# load HGCAL TPG simulation
process.load('L1Trigger.L1THGCal.hgcalTriggerPrimitives_cff')

#process.hgcalConcentratorProducer.ProcessorParameters.Method=cms.vstring(['autoEncoder']*3)
    
process.hgcalConcentratorProducer.ProcessorParameters = process.autoEncoder_conc_proc.clone()
#process.hgcalConcentratorProducer.ProcessorParameters.threshold_silicon=-1.
#process.hgcalConcentratorProducer.ProcessorParameters.threshold_scintillator=-1.
print process.hgcalConcentratorProducer.ProcessorParameters.Method

process.hgcl1tpg_step = cms.Path(process.hgcalTriggerPrimitives)


# load ntuplizer
process.load('L1Trigger.L1THGCalUtilities.hgcalTriggerNtuples_cff')
process.ntuple_step = cms.Path(process.hgcalTriggerNtuples)

process.ntuple_triggercells.FillSimEnergy=cms.bool(True)
process.ntuple_digis.isSimhitComp = cms.bool(True)

# process.hgcalConcentratorProducer.ProcessorParameters.triggercell_threshold_silicon = cms.double(-1.)
# process.hgcalConcentratorProducer.ProcessorParameters.triggercell_threshold_scintillator = cms.double(-1.)

# process.hgcalTriggerNtuplizer.Ntuples =  cms.VPSet(
#     process.ntuple_event,
#     process.ntuple_gen,
#     process.ntuple_genjet,
#     process.ntuple_gentau,
#     process.ntuple_digis,
#     process.ntuple_triggercells,
#     process.ntuple_multiclusters,
#     process.ntuple_towers
# )

# Schedule definition
process.schedule = cms.Schedule(process.hgcl1tpg_step, process.ntuple_step)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

