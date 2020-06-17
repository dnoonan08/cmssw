#include "L1Trigger/L1THGCal/interface/concentrator/HGCalConcentratorAutoEncoderImpl.h"
#include "DataFormats/ForwardDetId/interface/HGCalDetId.h"
#include "DataFormats/ForwardDetId/interface/HGCalTriggerDetId.h"

HGCalConcentratorAutoEncoderImpl::HGCalConcentratorAutoEncoderImpl(const edm::ParameterSet& conf)
    : cellRemap_(conf.getParameter<std::vector<int>>("cellRemap")),
      bitsPerInput_(conf.getParameter<int>("nBitsPerInput")),
      maxBitsPerOutput_(conf.getParameter<int>("maxBitsPerOutput")),
      outputBitsPerLink_(conf.getParameter<std::vector<int>>("bitsPerLink")) {
  //construct inverse array, to get U/V for a particular ae output position
  for (unsigned i=0; i<cellRemap_.size(); i++){
    if (cellRemap_.at(i)>-1){
      ae_outputCellU_[cellRemap_.at(i)] = int(i/8);
      ae_outputCellV_[cellRemap_.at(i)] = i%8;
    }
  }
}

void HGCalConcentratorAutoEncoderImpl::select(unsigned nLinks,
					      const std::vector<l1t::HGCalTriggerCell>& trigCellVecInput,
					      std::vector<l1t::HGCalTriggerCell>& trigCellVecOutput,
					      std::vector<l1t::HGCalConcentratorData>& ae_encodedLayer_Output){

  //initialize as all zeros, since trigCellVecInput is zero suppressed
  double mipPt_[48] = {0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,
				 0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,
				 0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.};
  double uncompressedCharge_[48] = {0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,
				    0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,
				    0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.};
  double compressedCharge_[48] = {0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,
				  0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,
				  0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.};

  double ae_inputArray[48];

  double modSum = 0;

  bool printWafer = false; //temp, to print out only one

  int bitsPerOutput = outputBitsPerLink_.at(nLinks);

  for (const auto& trigCell : trigCellVecInput) {
    bool isScintillator = triggerTools_.isScintillator(trigCell.detId());
    if (isScintillator) return; //currently, only silicon modules are setup to work (mapping of scinillators would be different, and needs to be investigated)

    HGCalTriggerDetId id(trigCell.detId());
    uint cellu = id.triggerCellU();
    uint cellv = id.triggerCellV();
    uint inputIndex = cellRemap_.at(cellu * 8 + cellv);
    mipPt_[inputIndex]=trigCell.mipPt();
    uncompressedCharge_[inputIndex]=trigCell.uncompressedCharge();
    compressedCharge_[inputIndex]=trigCell.compressedCharge();

    modSum += trigCell.mipPt();

    //print out vlaues from single module
    if (id.subdet()==1 && triggerTools_.layerWithOffset(trigCell.detId())==7 && id.zside()==1){
      if (id.waferU()==3 && id.waferV()==3){
        printWafer=true;
      }
    }
  }

  if (modSum>0){
    //normalize inputs to module sum
    for (int i=0; i<48; i++) {
      ae_inputArray[i] = mipPt_[i]/modSum;

      //round to precision of input, if bitsPerInput_ is -1 keep full precision
      if (bitsPerInput_>0){
	ae_inputArray[i] = round(ae_inputArray[i]*pow(2.,bitsPerInput_))/pow(2.,bitsPerInput_);
      }
    }
  }

  // INSERT AUTO ENCODER
  double ae_encodedLayer[16] = {15./16, 7./8, 13./16, 3./4, 11./16, 5./8, 9./16, 1./2, 7./16, 3./8, 5./16, 1./4, 3./16, 1./8, 1./16, 0.};

  //truncate the encoded layer
  if (bitsPerOutput>0){
    for (int i=0; i<16; i++){
      ae_encodedLayer[i] = round(ae_encodedLayer[i]*pow(2,bitsPerOutput))/pow(2.,bitsPerOutput);
    }
  }

  // INSERT DECODER
  double ae_outputArray[48];

  // for now, just copy input array mipPt into output
  for (int i=0; i<48; i++) ae_outputArray[i] = ae_inputArray[i];

  // Add data back into trigger cells
  if (modSum>0){
    //get detID for everything but cell, take first entry detID and subtract off cellU and cellV contribution
    HGCalTriggerDetId id(trigCellVecInput.at(0).detId());
    int cellU_ = id.triggerCellU();
    int cellV_ = id.triggerCellV();
    unsigned _id_waferBase = trigCellVecInput.at(0).detId() - (cellU_ << HGCalTriggerDetId::kHGCalCellUOffset) - (cellV_ << HGCalTriggerDetId::kHGCalCellVOffset);

    //use first TC to find mipPt conversions to Et and ADC
    float mipPtToEt_conv = trigCellVecInput.at(0).et() / trigCellVecInput.at(0).mipPt();
    float mipPtToADC_conv = trigCellVecInput.at(0).hwPt() / trigCellVecInput.at(0).mipPt();

    for (int i=0; i<48; i++){
      if (ae_outputArray[i] > 0){
	cellU_ = ae_outputCellU_[i];
	cellV_ = ae_outputCellV_[i];

	//find detID for this cell
	unsigned detID = _id_waferBase + (cellU_ << HGCalTriggerDetId::kHGCalCellUOffset) + (cellV_ << HGCalTriggerDetId::kHGCalCellVOffset);

	double mipPt = ae_outputArray[i]*modSum;
	double ADC = mipPt*mipPtToADC_conv;
	double Et = mipPt*mipPtToEt_conv;

	l1t::HGCalTriggerCell triggerCell(reco::LeafCandidate::LorentzVector(), ADC, 0, 0, 0, detID);
	//Keep the pre-autoencoder charge for this cell
	triggerCell.setUncompressedCharge(uncompressedCharge_[i]);
	triggerCell.setCompressedCharge(compressedCharge_[i]);
	triggerCell.setMipPt(mipPt);

	GlobalPoint point = triggerTools_.getTCPosition(detID);

	math::PtEtaPhiMLorentzVector p4(Et, point.eta(), point.phi(), 0.);

	triggerCell.setP4(p4);
	triggerCell.setPosition(point);

	trigCellVecOutput.push_back(triggerCell);
      }
    }

    if (printWafer) {
	cout << "nLinks: "<< nLinks << " inputBits: " << bitsPerInput_ << "  bitsPerOutput: " << bitsPerOutput << "  maxBitsPerOutput: " << maxBitsPerOutput_ << endl;
	cout << "Encoded layer values" << endl;
    }
    // load encoded layer data into a dummy trigger cell object, 
    // this is a convenient way to store module information, and pass to ntuplizer
    for (int i=0; i<16; i++){
      l1t::HGCalConcentratorData encodedLayerData(reco::LeafCandidate::LorentzVector(), ae_encodedLayer[i]*pow(2, maxBitsPerOutput_), 0, 0, 0, _id_waferBase);
      encodedLayerData.setIndex(i);
      ae_encodedLayer_Output.push_back(encodedLayerData);

      if (printWafer) {
	  cout << ae_encodedLayer[i] << "(" << encodedLayerData.hwPt()<<"), ";
      }
    }
    if (printWafer) {
	cout << endl;
    }
  }

  // temporary dump of single module data
  if (printWafer) {
    cout << "------------" << endl;
    cout << "inputValues" << endl;
    for (const auto& aeValue : ae_inputArray){
      cout << aeValue << ", ";
    }
    cout << endl;
  }

}
