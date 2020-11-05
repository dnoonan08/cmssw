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
## For New AE models
autoEncoder_Nominal_443_signal5 = cms.PSet(encoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/Nominal_443/encoder_5_links_signal.pb'),
                                           decoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/Nominal_443/decoder_5_links_signal.pb'))

autoEncoder_8x8_c4_pool_signal5 = cms.PSet(encoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/8x8_c4_pool/encoder_5_links_signal.pb'),
                                           decoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/8x8_c4_pool/decoder_5_links_signal.pb'))

autoEncoder_8x8_c6_pool_signal5 = cms.PSet(encoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/8x8_c6_pool/encoder_5_links_signal.pb'),
                                           decoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/8x8_c6_pool/decoder_5_links_signal.pb'))

autoEncoder_8x8_c8_pool_signal5 = cms.PSet(encoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/8x8_c8_pool/encoder_5_links_signal.pb'),
                                           decoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/8x8_c8_pool/decoder_5_links_signal.pb'))

autoEncoder_SepConv_443_pool_signal5 = cms.PSet(encoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/SepConv_443_pool/encoder_5_links_signal.pb'),
                                           decoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/SepConv_443_pool/decoder_5_links_signal.pb'))

autoEncoder_SepConv_663_c2_signal5 = cms.PSet(encoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/SepConv_663_c2/encoder_5_links_signal.pb'),
                                           decoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/SepConv_663_c2/decoder_5_links_signal.pb'))

autoEncoder_SepConv_663_c4_pool_signal5 = cms.PSet(encoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/SepConv_663_c4_pool/encoder_5_links_signal.pb'),
                                           decoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/SepConv_663_c4_pool/decoder_5_links_signal.pb'))

autoEncoder_SepConv_663_c8_pool_signal5 = cms.PSet(encoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/SepConv_663_c8_pool/encoder_5_links_signal.pb'),
                                           decoderModelFile = cms.FileInPath('L1Trigger/L1THGCalUtilities/test/AEmodels/SepConv_663_c8_pool/decoder_5_links_signal.pb'))


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

autoencoder_triggerCellRemap_8x8 = [28,29,30,31,0,4,8,12,
                                    24,25,26,27,1,5,9,13,
                                    20,21,22,23,2,6,10,14,
                                    16,17,18,19,3,7,11,15,
                                    47,43,39,35,-1,-1,-1,-1,
                                    46,42,38,34,-1,-1,-1,-1,
                                    45,41,37,33,-1,-1,-1,-1,
                                    44,40,36,32,-1,-1,-1,-1]

autoencoder_triggerCellRemapNoDupl_8x8 = [28,29,30,31,0,4,8,12,
                                          24,25,26,27,1,5,9,13,
                                          20,21,22,23,2,6,10,14,
                                          16,17,18,19,3,7,11,15,
                                          47,43,39,35,-1,-1,-1,-1,
                                          46,42,38,34,-1,-1,-1,-1,
                                          45,41,37,33,-1,-1,-1,-1,
                                          44,40,36,32,-1,-1,-1,-1]

autoencoder_triggerCellRemap_663 = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 
                                    -1, -1, -1, 12, 28, 44, 13, 29, 45, 14, 30, 46, 15, 31, 47, 32,  0, 16,
                                    -1, -1, -1,  8, 24, 40,  9, 25, 41, 10, 26, 42, 11, 27, 43, 33,  1, 17,
                                    -1, -1, -1,  4, 20, 36,  5, 21, 37,  6, 22, 38,  7, 23, 39, 34,  2, 18,
                                    -1, -1, -1,  0, 16, 32,  1, 17, 33,  2, 18, 34,  3, 19, 35, 35,  3, 19,
                                    -1, -1, -1, 31, 47, 15, 27, 43, 11, 23, 39,  7, 19, 35,  3, -1, -1, -1]

autoencoder_triggerCellRemapNoDupl_663 = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 
                                          -1, -1, -1, 12, 28, 44, 13, 29, 45, 14, 30, 46, 15, 31, 47, -1, -1, -1,
                                          -1, -1, -1,  8, 24, 40,  9, 25, 41, 10, 26, 42, 11, 27, 43, -1, -1, -1,
                                          -1, -1, -1,  4, 20, 36,  5, 21, 37,  6, 22, 38,  7, 23, 39, -1, -1, -1,
                                          -1, -1, -1,  0, 16, 32,  1, 17, 33,  2, 18, 34,  3, 19, 35, -1, -1, -1,
                                          -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

chains.register_concentrator("AutoEncoderNominal443", 
                             lambda p, i : concentrator.create_autoencoder(p, i, 
                                                                           modelFiles = cms.VPSet([autoEncoder_Nominal_443_signal5]),
                                                                           linkToGraphMap = cms.vuint32([0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
                                                                           encoderShape = cms.vuint32([1,4,4,3]),
                                                                           decoderShape = cms.vuint32([1,16]),
                                                                           cellRemap = cms.vint32(autoencoder_triggerCellRemap_443),
                                                                           cellRemapNoDuplicates = cms.vint32(autoencoder_triggerCellRemap_443)))

chains.register_concentrator("AutoEncoder8x8c4pool", 
                             lambda p, i : concentrator.create_autoencoder(p, i, 
                                                                           modelFiles = cms.VPSet([autoEncoder_8x8_c4_pool_signal5]),
                                                                           linkToGraphMap = cms.vuint32([0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
                                                                           encoderShape = cms.vuint32([1,8,8,1]),
                                                                           decoderShape = cms.vuint32([1,16]),
                                                                           cellRemap = cms.vint32(autoencoder_triggerCellRemap_8x8),
                                                                           cellRemapNoDuplicates = cms.vint32(autoencoder_triggerCellRemapNoDupl_8x8)))

chains.register_concentrator("AutoEncoder8x8c6pool", 
                             lambda p, i : concentrator.create_autoencoder(p, i, 
                                                                           modelFiles = cms.VPSet([autoEncoder_8x8_c6_pool_signal5]),
                                                                           linkToGraphMap = cms.vuint32([0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
                                                                           encoderShape = cms.vuint32([1,8,8,1]),
                                                                           decoderShape = cms.vuint32([1,16]),
                                                                           cellRemap = cms.vint32(autoencoder_triggerCellRemap_8x8),
                                                                           cellRemapNoDuplicates = cms.vint32(autoencoder_triggerCellRemapNoDupl_8x8)))

chains.register_concentrator("AutoEncoder8x8c8pool", 
                             lambda p, i : concentrator.create_autoencoder(p, i, 
                                                                           modelFiles = cms.VPSet([autoEncoder_8x8_c8_pool_signal5]),
                                                                           linkToGraphMap = cms.vuint32([0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
                                                                           encoderShape = cms.vuint32([1,8,8,1]),
                                                                           decoderShape = cms.vuint32([1,16]),
                                                                           cellRemap = cms.vint32(autoencoder_triggerCellRemap_8x8),
                                                                           cellRemapNoDuplicates = cms.vint32(autoencoder_triggerCellRemapNoDupl_8x8)))

chains.register_concentrator("AutoEncoderSepConv443pool", 
                             lambda p, i : concentrator.create_autoencoder(p, i, 
                                                                           modelFiles = cms.VPSet([autoEncoder_SepConv_443_pool_signal5]),
                                                                           linkToGraphMap = cms.vuint32([0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
                                                                           encoderShape = cms.vuint32([1,4,4,3]),
                                                                           decoderShape = cms.vuint32([1,16]),
                                                                           cellRemap = cms.vint32(autoencoder_triggerCellRemap_443),
                                                                           cellRemapNoDuplicates = cms.vint32(autoencoder_triggerCellRemap_443)))

chains.register_concentrator("AutoEncoderSepConv663c2", 
                             lambda p, i : concentrator.create_autoencoder(p, i, 
                                                                           modelFiles = cms.VPSet([autoEncoder_SepConv_663_c2_signal5]),
                                                                           linkToGraphMap = cms.vuint32([0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
                                                                           encoderShape = cms.vuint32([1,6,6,3]),
                                                                           decoderShape = cms.vuint32([1,16]),
                                                                           cellRemap = cms.vint32(autoencoder_triggerCellRemap_663),
                                                                           cellRemapNoDuplicates = cms.vint32(autoencoder_triggerCellRemapNoDupl_663)))

chains.register_concentrator("AutoEncoderSepConv663c4pool", 
                             lambda p, i : concentrator.create_autoencoder(p, i, 
                                                                           modelFiles = cms.VPSet([autoEncoder_SepConv_663_c4_pool_signal5]),
                                                                           linkToGraphMap = cms.vuint32([0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
                                                                           encoderShape = cms.vuint32([1,6,6,3]),
                                                                           decoderShape = cms.vuint32([1,16]),
                                                                           cellRemap = cms.vint32(autoencoder_triggerCellRemap_663),
                                                                           cellRemapNoDuplicates = cms.vint32(autoencoder_triggerCellRemapNoDupl_663)))

chains.register_concentrator("AutoEncoderSepConv663c8pool", 
                             lambda p, i : concentrator.create_autoencoder(p, i, 
                                                                           modelFiles = cms.VPSet([autoEncoder_SepConv_663_c8_pool_signal5]),
                                                                           linkToGraphMap = cms.vuint32([0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
                                                                           encoderShape = cms.vuint32([1,6,6,3]),
                                                                           decoderShape = cms.vuint32([1,16]),
                                                                           cellRemap = cms.vint32(autoencoder_triggerCellRemap_663),
                                                                           cellRemapNoDuplicates = cms.vint32(autoencoder_triggerCellRemapNoDupl_663)))

chains.register_concentrator("BestChoiceSTC16", 
                             lambda p, i : concentrator.create_mixedfeoptions(p, i, 
                                                                              stcSize = cms.vuint32( [16]*(53)*4 ) ))

concentrator_algos = ['AutoEncoderNominal443','AutoEncoder8x8c4pool','AutoEncoder8x8c6pool','AutoEncoder8x8c8pool','AutoEncoderSepConv443pool','AutoEncoderSepConv663c2','AutoEncoderSepConv663c4pool','AutoEncoderSepConv663c8pool','BestChoiceSTC16']

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

