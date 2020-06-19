#include "L1Trigger/L1THGCal/interface/concentrator/HGCalConcentratorAutoEncoderImpl.h"
#include "DataFormats/ForwardDetId/interface/HGCalDetId.h"
#include "DataFormats/ForwardDetId/interface/HGCalTriggerDetId.h"
#include <iomanip>

// Following example of implementing graphloading from here:
// https://gitlab.cern.ch/mrieger/CMSSW-TensorFlowExamples/-/blob/master/GraphLoading/

HGCalConcentratorAutoEncoderImpl::HGCalConcentratorAutoEncoderImpl(const edm::ParameterSet& conf)
    : cellRemap_(conf.getParameter<std::vector<int>>("cellRemap"))
    , bitsPerInput_(conf.getParameter<int>("nBitsPerInput"))
    , maxBitsPerOutput_(conf.getParameter<int>("maxBitsPerOutput"))
    , outputBitsPerLink_(conf.getParameter<std::vector<int>>("bitsPerLink"))
    , graphPath_encoder_(conf.getParameter<edm::FileInPath>("encoderModelFile"))
    , graphDef_encoder_(nullptr)
    , session_encoder_(nullptr) 
    , graphPath_decoder_(conf.getParameter<edm::FileInPath>("decoderModelFile"))
    , graphDef_decoder_(nullptr)
    , session_decoder_(nullptr) 
{
  //construct inverse array, to get U/V for a particular ae output position
  for (unsigned i=0; i<cellRemap_.size(); i++){
    if (cellRemap_.at(i)>-1){
      ae_outputCellU_[cellRemap_.at(i)] = int(i/8);
      ae_outputCellV_[cellRemap_.at(i)] = i%8;
    }
  }

  tensorflow::setLogging("0");

  std::cout << "loading encoder graph from " << graphPath_encoder_.fullPath() << std::endl;
  graphDef_encoder_ = tensorflow::loadGraphDef(graphPath_encoder_.fullPath());
  // create a new session and add the graphDef
  session_encoder_ = tensorflow::createSession(graphDef_encoder_);

  std::cout << "loading decoder graph from " << graphPath_decoder_.fullPath() << std::endl;
  graphDef_decoder_ = tensorflow::loadGraphDef(graphPath_decoder_.fullPath());

  // create a new session and add the graphDef
  session_decoder_ = tensorflow::createSession(graphDef_decoder_);

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

  // double testInputs[48] = {0.030303030303,0.000000000000,0.045454545455,0.000000000000,0.454545454545,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.015151515152,0.000000000000,0.020202020202,0.090909090909,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.015151515152,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.075757575758,0.000000000000,0.000000000000,0.000000000000,0.191919191919,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.000000000000,0.040404040404,0.000000000000,0.020202020202,0.000000000000};
  // double testEncoded[16] = {0.000000000000,0.310191392899,0.000000000000,0.000000000000,0.000000000000,0.473288595676,0.524694979191,0.554164171219,0.000000000000,0.164925053716,0.000000000000,0.898950994015,0.286225616932,0.027442939579,0.000000000000,0.000000000000};

  tensorflow::Tensor encoder_input(tensorflow::DT_FLOAT, { 1, 4, 4, 3 });
  float* d = encoder_input.flat<float>().data();
  for (int i = 0; i < 48; i++, d++)
  {
    *d = ae_inputArray[i];
  }

  if (printWafer){
    std::cout << "session.run" << std::endl;
  }


  std::vector<tensorflow::Tensor> encoder_outputs;
  tensorflow::run(session_encoder_, { { "input_1", encoder_input } }, { "encoder/encoded_vector/Relu" }, &encoder_outputs);


  if (printWafer){
    cout << "Encoder Inputs" << endl;
    std::cout << " -> " << encoder_input.DebugString() << endl;
    d = encoder_input.flat<float>().data();
    for (int i = 0; i < encoder_input.NumElements(); i++, d++){
      cout << setprecision (12) <<*d << ",";
    }
    cout << endl << endl;

    cout << "Encoder Outputs" << endl;
    std::cout << " -> " << encoder_outputs[0].DebugString() << endl;
    d = encoder_outputs[0].flat<float>().data();
    for (int i = 0; i < encoder_outputs[0].NumElements(); i++, d++){
      cout << setprecision (12) <<*d << ",";
    }
    cout << endl << endl;
  }





  double ae_encodedLayer[16];
  d = encoder_outputs[0].flat<float>().data();
  for (int i = 0; i < encoder_outputs[0].NumElements(); i++, d++)
  {
    ae_encodedLayer[i] = *d;
    //truncate the encoded layer bits
    if (bitsPerOutput>0){
      ae_encodedLayer[i] = round(ae_encodedLayer[i]*pow(2,bitsPerOutput))/pow(2.,bitsPerOutput);
    }
  }

  tensorflow::Tensor decoder_input(tensorflow::DT_FLOAT, { 1, 16 });
  d = decoder_input.flat<float>().data();
  for (int i = 0; i < 16; i++, d++)
  {
    *d = ae_encodedLayer[i];
  }




  std::vector<tensorflow::Tensor> decoder_outputs;
  tensorflow::run(session_decoder_, { { "decoder_input", decoder_input } }, { "decoder_output/Sigmoid" }, &decoder_outputs);

  double ae_outputArray[48];

  if (printWafer){
    cout << "Decoder Inputs" << endl;
    std::cout << " -> " << encoder_input.DebugString() << endl;
    d = encoder_input.flat<float>().data();
    for (int i = 0; i < encoder_input.NumElements(); i++, d++){
      cout << setprecision (12) <<*d << ",";
    }
    cout << endl << endl;

    cout << "Decoder Outputs" << endl;
    std::cout << " -> " << decoder_outputs[0].DebugString() << endl;
    d = decoder_outputs[0].flat<float>().data();
    for (int i = 0; i < decoder_outputs[0].NumElements(); i++, d++){
      cout << setprecision (12) <<*d << ",";
    }
    cout << endl << endl;
  }

  d = decoder_outputs[0].flat<float>().data();
  for (int i = 0; i < decoder_outputs[0].NumElements(); i++, d++){
    ae_outputArray[i] = *d;
  }

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
      cout << "------------" << endl;
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
    cout << "inputValues" << endl;
    for (const auto& aeValue : ae_inputArray){
      cout << aeValue << ", ";
    }
    cout << endl;
  }

}
