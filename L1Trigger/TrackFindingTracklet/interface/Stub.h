#ifndef L1Trigger_TrackFindingTracklet_interface_Stub_h
#define L1Trigger_TrackFindingTracklet_interface_Stub_h

#include <iostream>
#include <fstream>
#include <cassert>
#include <cmath>

#include "L1Trigger/TrackFindingTracklet/interface/FPGAWord.h"
#include "L1Trigger/TrackFindingTracklet/interface/L1TStub.h"
#include "L1Trigger/TrackFindingTracklet/interface/Util.h"
#include "L1Trigger/TrackFindingTracklet/interface/Settings.h"

namespace trklet {

  class Stub {
  public:
    Stub(Settings const& settings);

    Stub(L1TStub& stub, Settings const& settings, double phiminsec, double phimaxsec);

    ~Stub() = default;

    FPGAWord iphivmFineBins(int VMbits, int finebits) const;

    std::string str() const {
      if (layer_.value() != -1) {
        return r_.str() + "|" + z_.str() + "|" + phi_.str() + "|" + bend_.str();
      } else {
        if (isPSmodule()) {
          return r_.str() + "|" + z_.str() + "|" + phi_.str() + "|" + bend_.str();
        } else {
          return "000" + r_.str() + "|" + z_.str() + "|" + phi_.str() + "|" + alphanew_.str() + "|" + bend_.str();
        }
      }
    }

    std::string strbare() const { return bend_.str() + r_.str() + z_.str() + phi_.str(); }

    unsigned int phiregionaddress() const;
    std::string phiregionaddressstr() const;

    void setAllStubIndex(int nstub);  //should migrate away from using this method

    void setPhiCorr(int phiCorr);

    const FPGAWord& bend() const { return bend_; }

    const FPGAWord& r() const { return r_; }
    const FPGAWord& z() const { return z_; }
    const FPGAWord& phi() const { return phi_; }
    const FPGAWord& phicorr() const { return phicorr_; }
    const FPGAWord& alphanew() const { return alphanew_; }

    const FPGAWord& stubindex() const { return stubindex_; }
    const FPGAWord& layer() const { return layer_; }
    const FPGAWord& disk() const { return disk_; }
    unsigned int layerdisk() const;

    bool isBarrel() const { return layer_.value() != -1; }
    bool isDisk() const { return disk_.value() != 0; }

    bool isPSmodule() const { return isBarrel() ? (layer_.value() < (int)N_PSLAYER) : (r_.value() > 10); }

    double rapprox() const;
    double zapprox() const;
    double phiapprox(double phimin, double) const;

    L1TStub* l1tstub() { return l1tstub_; }
    const L1TStub* l1tstub() const { return l1tstub_; }
    void setl1tstub(L1TStub* l1tstub) { l1tstub_ = l1tstub; }

  private:
    FPGAWord layer_;
    FPGAWord disk_;
    FPGAWord r_;
    FPGAWord z_;
    FPGAWord phi_;
    FPGAWord alphanew_;

    FPGAWord bend_;

    FPGAWord phicorr_;  //Corrected for bend to nominal radius

    FPGAWord stubindex_;

    L1TStub* l1tstub_;
    Settings const& settings_;
  };

};  // namespace trklet
#endif
