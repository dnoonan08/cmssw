#ifndef __L1Trigger_L1THGCal_HGCalConcentratorAutoEncoderImpl_h__
#define __L1Trigger_L1THGCal_HGCalConcentratorAutoEncoderImpl_h__

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/L1THGCal/interface/HGCalTriggerCell.h"
#include "DataFormats/L1THGCal/interface/HGCalConcentratorData.h"
#include "L1Trigger/L1THGCal/interface/HGCalTriggerTools.h"
#include <vector>

#include "L1Trigger/L1THGCal/interface/HGCalTriggerGeometryBase.h"

class HGCalConcentratorAutoEncoderImpl {
public:
  HGCalConcentratorAutoEncoderImpl(const edm::ParameterSet& conf);

  void select(unsigned nLinks,
	      const std::vector<l1t::HGCalTriggerCell>& trigCellVecInput,
              std::vector<l1t::HGCalTriggerCell>& trigCellVecOutput,
	      std::vector<l1t::HGCalConcentratorData>& ae_EncodedOutput);

  void eventSetup(const edm::EventSetup& es) { triggerTools_.eventSetup(es); }

private:
  std::vector<int> cellRemap_;
  int bitsPerInput_;
  int maxBitsPerOutput_;
  std::vector<int> outputBitsPerLink_;

  int ae_outputCellU_[48];
  int ae_outputCellV_[48];

  HGCalTriggerTools triggerTools_;
};

#endif
