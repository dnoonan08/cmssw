import FWCore.ParameterSet.Config as cms 

from Configuration.Eras.Era_Phase2C9_cff import Phase2C9
process = cms.Process('DIGI',Phase2C9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
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
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
       fileNames = cms.untracked.vstring("file:665687E8-E070-D449-AB48-60A5634E335E.root"),
       inputCommands=cms.untracked.vstring(
           'keep *',
           'drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT',
           'drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT',
           'drop l1tEMTFHit2016s_simEmtfDigis__HLT',
           'drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT',
           'drop l1tEMTFTrack2016s_simEmtfDigis__HLT',
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
    fileName = cms.string("ntuple.root")
    )

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

# load HGCAL TPG simulation
process.load('L1Trigger.L1THGCal.hgcalTriggerPrimitives_cff')
process.load('L1Trigger.L1THGCalUtilities.HGC3DClusterGenMatchSelector_cff')
process.load('L1Trigger.L1THGCalUtilities.hgcalTriggerNtuples_cff')
from L1Trigger.L1THGCalUtilities.hgcalTriggerChains import HGCalTriggerChains
import L1Trigger.L1THGCalUtilities.vfe as vfe
import L1Trigger.L1THGCalUtilities.concentrator as concentrator
import L1Trigger.L1THGCalUtilities.clustering2d as clustering2d
import L1Trigger.L1THGCalUtilities.clustering3d as clustering3d
import L1Trigger.L1THGCalUtilities.selectors as selectors
import L1Trigger.L1THGCalUtilities.customNtuples as ntuple


chains = HGCalTriggerChains()
# Register algorithms
## VFE
chains.register_vfe("Floatingpoint", vfe.create_vfe)
## ECON
chains.register_concentrator("Supertriggercell", concentrator.create_supertriggercell)
chains.register_concentrator("Threshold", concentrator.create_threshold)
chains.register_concentrator("Bestchoice", concentrator.create_bestchoice)
chains.register_concentrator("AutoEncoder", concentrator.create_autoencoder)

##################
## For Pileup AE models
autoEncoder_Nominal_443_pileup2 = cms.PSet(encoderModelFile = cms.FileInPath('L1Trigger/L1THGCal/data/encoder_2eLinks_PUdriven_constantgraph.pb'),
                                           decoderModelFile = cms.FileInPath('L1Trigger/L1THGCal/data/decoder_2eLinks_PUdriven_constantgraph.pb'))

autoEncoder_Nominal_443_pileup3 = cms.PSet(encoderModelFile = cms.FileInPath('L1Trigger/L1THGCal/data/encoder_3eLinks_PUdriven_constantgraph.pb'),
                                           decoderModelFile = cms.FileInPath('L1Trigger/L1THGCal/data/decoder_3eLinks_PUdriven_constantgraph.pb'))

autoEncoder_Nominal_443_pileup4 = cms.PSet(encoderModelFile = cms.FileInPath('L1Trigger/L1THGCal/data/encoder_4eLinks_PUdriven_constantgraph.pb'),
                                           decoderModelFile = cms.FileInPath('L1Trigger/L1THGCal/data/decoder_4eLinks_PUdriven_constantgraph.pb'))

autoEncoder_Nominal_443_pileup5 = cms.PSet(encoderModelFile = cms.FileInPath('L1Trigger/L1THGCal/data/encoder_5eLinks_PUdriven_constantgraph.pb'),
                                           decoderModelFile = cms.FileInPath('L1Trigger/L1THGCal/data/decoder_5eLinks_PUdriven_constantgraph.pb'))

autoencoder_triggerCellRemap_443 = [0,16, 32,
                                    1,17, 33,
                                    2,18, 34,
                                    3,19, 35,
                                    4,20, 36,
                                    5,21, 37,
                                    6,22, 38,
                                    7,23, 39,
                                    8,24, 40,
                                    9,25, 41,
                                    10,26, 42,
                                    11,27, 43,
                                    12,28, 44,
                                    13,29, 45,
                                    14,30, 46,
                                    15,31, 47]


chains.register_concentrator("AutoEncoderNominal443Pileup", 
                             lambda p, i : concentrator.create_autoencoder(p, i, 
                                                                           modelFiles = cms.VPSet([autoEncoder_Nominal_443_pileup2,autoEncoder_Nominal_443_pileup3,autoEncoder_Nominal_443_pileup4,autoEncoder_Nominal_443_pileup5]),
                                                                           linkToGraphMap = cms.vuint32([0,0,0,1,2,3,3,3,3,3,3,3,3,3]),
                                                                           encoderShape = cms.vuint32([1,4,4,3]),
                                                                           decoderShape = cms.vuint32([1,16]),
                                                                           cellRemap = cms.vint32(autoencoder_triggerCellRemap_443),
                                                                           cellRemapNoDuplicates = cms.vint32(autoencoder_triggerCellRemap_443)))

chains.register_concentrator("AutoEncoderNominal443Pileup5", 
                             lambda p, i : concentrator.create_autoencoder(p, i, 
                                                                           modelFiles = cms.VPSet([autoEncoder_Nominal_443_pileup5]),
                                                                           linkToGraphMap = cms.vuint32([0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
                                                                           encoderShape = cms.vuint32([1,4,4,3]),
                                                                           decoderShape = cms.vuint32([1,16]),
                                                                           cellRemap = cms.vint32(autoencoder_triggerCellRemap_443),
                                                                           cellRemapNoDuplicates = cms.vint32(autoencoder_triggerCellRemap_443)))

concentrator_algos = ['AutoEncoderNominal443Pileup','AutoEncoderNominal443Pileup5']

#####################

## BE1
chains.register_backend1("Dummy", clustering2d.create_dummy)
## BE2
chains.register_backend2("Histomax", clustering3d.create_histoMax)
# Register selector
chains.register_selector("Genmatch", selectors.create_genmatch)
# Register ntuples
ntuple_list = ['event', 'gen', 'multiclusters']
chains.register_ntuple("Genclustersntuple", lambda p,i : ntuple.create_ntuple(p,i, ntuple_list))

from L1Trigger.L1THGCal.customTriggerGeometry import custom_geometry_decentralized_V11
process = custom_geometry_decentralized_V11(process, links='pudriven')

# Register trigger chains
#concentrator_algos = ['Supertriggercell', 'Threshold', 'Bestchoice', 'AutoEncoder']
backend_algos = ['Histomax']
## Make cross product fo ECON and BE algos
import itertools
for cc,be in itertools.product(concentrator_algos,backend_algos):
    chains.register_chain('Floatingpoint', cc, 'Dummy', be, 'Genmatch', 'Genclustersntuple')

process = chains.create_sequences(process)

# Remove towers from sequence
process.hgcalTriggerPrimitives.remove(process.hgcalTowerMap)
process.hgcalTriggerPrimitives.remove(process.hgcalTower)

process.hgcl1tpg_step = cms.Path(process.hgcalTriggerPrimitives)
process.selector_step = cms.Path(process.hgcalTriggerSelector)
process.ntuple_step = cms.Path(process.hgcalTriggerNtuples)

# Schedule definition
process.schedule = cms.Schedule(process.hgcl1tpg_step, process.selector_step, process.ntuple_step)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

