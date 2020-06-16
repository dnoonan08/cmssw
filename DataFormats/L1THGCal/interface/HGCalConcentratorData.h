#ifndef DataFormats_L1TCalorimeter_HGCalConcentratorData_h
#define DataFormats_L1TCalorimeter_HGCalConcentratorData_h

#include "DataFormats/GeometryVector/interface/GlobalPoint.h"
#include "DataFormats/L1Trigger/interface/L1Candidate.h"
#include "DataFormats/L1Trigger/interface/BXVector.h"
#include "DataFormats/DetId/interface/DetId.h"

namespace l1t {

  class HGCalConcentratorData;
  typedef BXVector<HGCalConcentratorData> HGCalConcentratorDataBxCollection;

  class HGCalConcentratorData : public L1Candidate {
  public:
    HGCalConcentratorData() {}

    HGCalConcentratorData(const LorentzVector& p4, int pt = 0, int eta = 0, int phi = 0, int qual = 0, uint32_t detid = 0);

    ~HGCalConcentratorData() override;

    void setDetId(uint32_t detid) { detid_ = DetId(detid); }
    void setPosition(const GlobalPoint& position) { position_ = position; }

    uint32_t detId() const { return detid_.rawId(); }
    const GlobalPoint& position() const { return position_; }

    void setIndex(uint32_t value) { index_ = value; }

    uint32_t index() const { return index_; }

    int subdetId() const { return detid_.subdetId(); }

  private:
    DetId detid_;
    GlobalPoint position_;

    uint32_t index_{0};
  };

}  // namespace l1t

#endif
