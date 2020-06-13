#include "L1Trigger/L1THGCal/interface/concentrator/HGCalConcentratorAutoEncoderImpl.h"
#include "DataFormats/ForwardDetId/interface/HGCalDetId.h"
#include "DataFormats/ForwardDetId/interface/HGCalTriggerDetId.h"

HGCalConcentratorAutoEncoderImpl::HGCalConcentratorAutoEncoderImpl(const edm::ParameterSet& conf)
  : cellRemap_(conf.getParameter<std::vector<int>>("cellRemap")) {
  //construct inverse array, to get U/V for a particular ae output position
  for (unsigned i=0; i<cellRemap_.size(); i++){
    if (cellRemap_.at(i)>-1){
      ae_outputCellU_[cellRemap_.at(i)] = int(i/8);
      ae_outputCellV_[cellRemap_.at(i)] = i%8;
    }
  }
}

void HGCalConcentratorAutoEncoderImpl::select(const std::vector<l1t::HGCalTriggerCell>& trigCellVecInput,
					      std::vector<l1t::HGCalTriggerCell>& trigCellVecOutput){

  //initialize as all zeros, since trigCellVecInput is zero suppressed
  double ae_inputArray[3][48] = {{0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,
				  0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,
				  0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.},
				 {0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,
				  0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,
				  0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.},
				 {0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,
				  0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,
				  0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.}};
  double modSum = 0;
  
  bool printWafer = false; //temp, to print out only one

  for (const auto& trigCell : trigCellVecInput) {
    bool isScintillator = triggerTools_.isScintillator(trigCell.detId());
    if (isScintillator) return; //currently, only silicon modules are setup to work (mapping of scinillators would be different, and needs to be investigated)

    HGCalTriggerDetId id(trigCell.detId());
    uint cellu = id.triggerCellU();
    uint cellv = id.triggerCellV();
    uint inputIndex = cellRemap_.at(cellu * 8 + cellv);
    ae_inputArray[0][inputIndex]=trigCell.mipPt();
    ae_inputArray[1][inputIndex]=trigCell.uncompressedCharge();
    ae_inputArray[2][inputIndex]=trigCell.compressedCharge();

    modSum += trigCell.mipPt();

    //print out vlaues from single module
    if (id.subdet()==1 && triggerTools_.layerWithOffset(trigCell.detId())==19 && id.zside()==1){
      if (id.waferU()==6 && id.waferV()==4){
        cout << id.triggerCellU() << "  " << id.triggerCellV() << "  " << trigCell.detId() << "  " <<trigCell.hwPt() << "  " << trigCell.mipPt() << endl;
        printWafer=true;
      }
    }
  }

  

  if (modSum>0){
    for (int i=0; i<48; i++) ae_inputArray[0][i] /= modSum;
  }


  // INSERT AUTO ENCODER AND DECODER
  // for now, just copy input array mipPt into output
  double ae_outputArray[48];
  for (int i=0; i<48; i++) ae_outputArray[i] = ae_inputArray[0][i];

  
  // Add data back into trigger cells
  if (modSum>0){
      //get detID for everything but cell, take first entry detID and subtract off cellU and cellV contribution
      HGCalTriggerDetId id(trigCellVecInput.at(0).detId());
      int cellU_ = id.triggerCellU();
      int cellV_ = id.triggerCellV();
      int _id_waferBase = trigCellVecInput.at(0).detId() - (cellU_ << HGCalTriggerDetId::kHGCalCellUOffset) - (cellV_ << HGCalTriggerDetId::kHGCalCellVOffset);

      //use first TC to find mipPt conversions to Et and ADC
      float mipPtToEt_conv = trigCellVecInput.at(0).et() / trigCellVecInput.at(0).mipPt();
      float mipPtToADC_conv = trigCellVecInput.at(0).hwPt() / trigCellVecInput.at(0).mipPt();

      for (int i=0; i<48; i++){
	if (ae_outputArray[i] > 0){
	  cellU_ = ae_outputCellU_[i];
	  cellV_ = ae_outputCellV_[i];

	  //find detID for this cell
	  int detID = _id_waferBase + (cellU_ << HGCalTriggerDetId::kHGCalCellUOffset) + (cellV_ << HGCalTriggerDetId::kHGCalCellVOffset);
	  
	  double mipPt = ae_outputArray[i]*modSum;
	  double ADC = mipPt*mipPtToADC_conv;
	  double Et = mipPt*mipPtToEt_conv;

	  l1t::HGCalTriggerCell triggerCell(reco::LeafCandidate::LorentzVector(), ADC, 0, 0, 0, detID);

	  //Keep the pre-autoencoder charge for this cell
	  triggerCell.setUncompressedCharge(ae_inputArray[1][i]);
	  triggerCell.setCompressedCharge(ae_inputArray[2][i]);
	  triggerCell.setMipPt(mipPt);

	  GlobalPoint point = triggerTools_.getTCPosition(detID);

	  math::PtEtaPhiMLorentzVector p4(Et, point.eta(), point.phi(), 0.);

	  triggerCell.setP4(p4);
	  triggerCell.setPosition(point);

	  trigCellVecOutput.push_back(triggerCell);
	}
      }

  }
  // for (const auto& aeValue : ae_inputArray){


  // temporary dump of single module data
  if (printWafer) {
    for (const auto& aeValue : ae_inputArray[0]){
      cout << aeValue << ", ";
    }
    cout << endl;
  }




}
