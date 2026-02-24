# Visual/Postman Rename Pattern Review

Purpose: review likely 1:1 HTML alignment to Postman visualizer requests using rename patterns (no manual dictionary).

## Summary

- Postman visualizer requests: **22**
- Visual HTML files: **31**
- Candidate matches found: **22**
- High confidence candidates: **17**
- Medium confidence candidates: **3**
- Low confidence candidates: **2**

## High Confidence Candidates

- `DOCSIS-3.0/Upstream/ATDMA-Channel-PreEqualization` <= `DOCSIS-3.0/US-ATDMA-PreEqualization` (score 69)
  - Suggested HTML target path: `visual/PyPNM/DOCSIS-3.0/Upstream/ATDMA-Channel-PreEqualization.html`
  - Pattern(s): folder: DOCSIS-3.0/Upstream -> DOCSIS-3.0; rename: ATDMA-Channel-PreEqualization -> US-ATDMA-PreEqualization
- `MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Echo-Detection-IFFT` <= `MultiCapture/ChannelEstimation/ChannelEstimation-Analysis-Echo-Detection-IFFT` (score 92)
  - Suggested HTML target path: `visual/PyPNM/MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Echo-Detection-IFFT.html`
  - Pattern(s): generic token match
- `MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Group-Delay` <= `MultiCapture/ChannelEstimation/ChannelEstimation-Analysis-GroupDelay` (score 71)
  - Suggested HTML target path: `visual/PyPNM/MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Group-Delay.html`
  - Pattern(s): generic token match
- `MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Min-Avg-Max` <= `MultiCapture/ChannelEstimation/ChannelEstimation-Analysis-MIN_AVG_MAX` (score 92)
  - Suggested HTML target path: `visual/PyPNM/MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Min-Avg-Max.html`
  - Pattern(s): generic token match
- `MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Echo-Dectection-IFFT` <= `MultiCapture/OfdmaPreEqualization/OfdmaPreEqualization-Analysis-EchoDetection` (score 73)
  - Suggested HTML target path: `visual/PyPNM/MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Echo-Dectection-IFFT.html`
  - Pattern(s): case/style: OFDMA-PreEqualization -> OfdmaPreEqualization; typo normalization: Dectection -> Detection
- `MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Group-Delay` <= `MultiCapture/OfdmaPreEqualization/OfdmaPreEqualization-Analysis-GroupDelay` (score 85)
  - Suggested HTML target path: `visual/PyPNM/MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Group-Delay.html`
  - Pattern(s): case/style: OFDMA-PreEqualization -> OfdmaPreEqualization
- `MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Min-Avg-Max` <= `MultiCapture/OfdmaPreEqualization/OfdmaPreEqualization-Analysis-MinAvgMax` (score 105)
  - Suggested HTML target path: `visual/PyPNM/MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Min-Avg-Max.html`
  - Pattern(s): case/style: OFDMA-PreEqualization -> OfdmaPreEqualization
- `MultiCapture/RxMER/Ofdm-RxMER-Analysis-Heat-Map` <= `MultiCapture/RxMER/RxMER-Analysis-Rxmer-Heat-Map` (score 69)
  - Suggested HTML target path: `visual/PyPNM/MultiCapture/RxMER/Ofdm-RxMER-Analysis-Heat-Map.html`
  - Pattern(s): case normalization: RxMER/Rxmer
- `MultiCapture/RxMER/Ofdm-RxMER-Analysis-Min-Avg-Max` <= `MultiCapture/RxMER/RxMER-Analysis-MIn-Avg-Max` (score 92)
  - Suggested HTML target path: `visual/PyPNM/MultiCapture/RxMER/Ofdm-RxMER-Analysis-Min-Avg-Max.html`
  - Pattern(s): case normalization: Min/MIn
- `MultiCapture/RxMER/Ofdm-RxMER-Analysis-Profile-Performance-1` <= `MultiCapture/RxMER/RxMER-Analysis-OFDMA-Profile-Performance-1` (score 90)
  - Suggested HTML target path: `visual/PyPNM/MultiCapture/RxMER/Ofdm-RxMER-Analysis-Profile-Performance-1.html`
  - Pattern(s): generic token match
- `SingleCapture/Ofdm-ChannelEstCoeff-GetCapture` <= `SingleCapture/OFDM/GetCapture-ChanEst` (score 62)
  - Suggested HTML target path: `visual/PyPNM/SingleCapture/Ofdm-ChannelEstCoeff-GetCapture.html`
  - Pattern(s): name pattern: Ofdm-<X>-GetCapture -> GetCapture-<X>; abbrev: ChannelEstCoeff -> ChanEst
- `SingleCapture/Ofdm-ConstellationDisplay-GetCapture` <= `SingleCapture/OFDM/GetCapture-ConstellationDisplay` (score 80)
  - Suggested HTML target path: `visual/PyPNM/SingleCapture/Ofdm-ConstellationDisplay-GetCapture.html`
  - Pattern(s): name pattern: Ofdm-<X>-GetCapture -> GetCapture-<X>
- `SingleCapture/Ofdm-ModulationProfile-GetCapture` <= `SingleCapture/OFDM/GetCapture-ModulationProfile` (score 80)
  - Suggested HTML target path: `visual/PyPNM/SingleCapture/Ofdm-ModulationProfile-GetCapture.html`
  - Pattern(s): name pattern: Ofdm-<X>-GetCapture -> GetCapture-<X>
- `SingleCapture/Ofdm-RxMER-GetCapture` <= `SingleCapture/OFDM/GetCapture-RxMER` (score 80)
  - Suggested HTML target path: `visual/PyPNM/SingleCapture/Ofdm-RxMER-GetCapture.html`
  - Pattern(s): name pattern: Ofdm-<X>-GetCapture -> GetCapture-<X>
- `SingleCapture/Ofdma-PreEq-GetCapture` <= `SingleCapture/OFDMA/GetCapture-PreEqualization` (score 64)
  - Suggested HTML target path: `visual/PyPNM/SingleCapture/Ofdma-PreEq-GetCapture.html`
  - Pattern(s): name pattern: Ofdma-<X>-GetCapture -> GetCapture-<X>
- `SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-OFDM` <= `SingleCapture/SpectrumAnalysis/GetCapture-OFDM` (score 71)
  - Suggested HTML target path: `visual/PyPNM/SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-OFDM.html`
  - Pattern(s): folder: SpectrumAnalyzer/Snmp-Upload -> SpectrumAnalysis
- `SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-SCQAM` <= `SingleCapture/SpectrumAnalysis/GetCapture-SCQAM` (score 71)
  - Suggested HTML target path: `visual/PyPNM/SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-SCQAM.html`
  - Pattern(s): folder: SpectrumAnalyzer/Snmp-Upload -> SpectrumAnalysis

## Medium Confidence Candidates

- `DOCSIS-3.0/Upstream/ATDMA-Channel-Stats` <= `DOCSIS-3.0/US-ATDMA-Stats` (score 58)
  - Suggested HTML target path: `visual/PyPNM/DOCSIS-3.0/Upstream/ATDMA-Channel-Stats.html`
  - Pattern(s): folder: DOCSIS-3.0/Upstream -> DOCSIS-3.0; rename: ATDMA-Channel-Stats -> US-ATDMA-Stats
- `SingleCapture/Histogram-GetCapture` <= `SingleCapture/SpectrumAnalysis/GetCapture` (score 47)
  - Suggested HTML target path: `visual/PyPNM/SingleCapture/Histogram-GetCapture.html`
  - Pattern(s): generic token match
- `SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-FullBandCapture` <= `SingleCapture/SpectrumAnalysis/GetCapture` (score 56)
  - Suggested HTML target path: `visual/PyPNM/SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-FullBandCapture.html`
  - Pattern(s): folder: SpectrumAnalyzer/Snmp-Upload -> SpectrumAnalysis

## Low Confidence / Needs Manual Review

- `DOCSIS-3.1/System-Diplexer` <= `DOCSIS-3.1/DiplexConfiguration` (score 26)
  - Pattern(s): rename: System-Diplexer -> DiplexConfiguration
- `Device/EventLog` <= `DOCSIS-General/EventLog` (score 38)
  - Pattern(s): folder: Device -> DOCSIS-General

## Grouped by Rename Pattern

### abbrev: ChannelEstCoeff -> ChanEst

- `SingleCapture/Ofdm-ChannelEstCoeff-GetCapture` <= `SingleCapture/OFDM/GetCapture-ChanEst` (score 62)

### case normalization: Min/MIn

- `MultiCapture/RxMER/Ofdm-RxMER-Analysis-Min-Avg-Max` <= `MultiCapture/RxMER/RxMER-Analysis-MIn-Avg-Max` (score 92)

### case normalization: RxMER/Rxmer

- `MultiCapture/RxMER/Ofdm-RxMER-Analysis-Heat-Map` <= `MultiCapture/RxMER/RxMER-Analysis-Rxmer-Heat-Map` (score 69)

### case/style: OFDMA-PreEqualization -> OfdmaPreEqualization

- `MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Echo-Dectection-IFFT` <= `MultiCapture/OfdmaPreEqualization/OfdmaPreEqualization-Analysis-EchoDetection` (score 73)
- `MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Group-Delay` <= `MultiCapture/OfdmaPreEqualization/OfdmaPreEqualization-Analysis-GroupDelay` (score 85)
- `MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Min-Avg-Max` <= `MultiCapture/OfdmaPreEqualization/OfdmaPreEqualization-Analysis-MinAvgMax` (score 105)

### folder: DOCSIS-3.0/Upstream -> DOCSIS-3.0

- `DOCSIS-3.0/Upstream/ATDMA-Channel-PreEqualization` <= `DOCSIS-3.0/US-ATDMA-PreEqualization` (score 69)
- `DOCSIS-3.0/Upstream/ATDMA-Channel-Stats` <= `DOCSIS-3.0/US-ATDMA-Stats` (score 58)

### folder: Device -> DOCSIS-General

- `Device/EventLog` <= `DOCSIS-General/EventLog` (score 38)

### folder: SpectrumAnalyzer/Snmp-Upload -> SpectrumAnalysis

- `SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-FullBandCapture` <= `SingleCapture/SpectrumAnalysis/GetCapture` (score 56)
- `SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-OFDM` <= `SingleCapture/SpectrumAnalysis/GetCapture-OFDM` (score 71)
- `SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-SCQAM` <= `SingleCapture/SpectrumAnalysis/GetCapture-SCQAM` (score 71)

### generic token match

- `MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Echo-Detection-IFFT` <= `MultiCapture/ChannelEstimation/ChannelEstimation-Analysis-Echo-Detection-IFFT` (score 92)
- `MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Group-Delay` <= `MultiCapture/ChannelEstimation/ChannelEstimation-Analysis-GroupDelay` (score 71)
- `MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Min-Avg-Max` <= `MultiCapture/ChannelEstimation/ChannelEstimation-Analysis-MIN_AVG_MAX` (score 92)
- `MultiCapture/RxMER/Ofdm-RxMER-Analysis-Profile-Performance-1` <= `MultiCapture/RxMER/RxMER-Analysis-OFDMA-Profile-Performance-1` (score 90)
- `SingleCapture/Histogram-GetCapture` <= `SingleCapture/SpectrumAnalysis/GetCapture` (score 47)

### name pattern: Ofdm-<X>-GetCapture -> GetCapture-<X>

- `SingleCapture/Ofdm-ChannelEstCoeff-GetCapture` <= `SingleCapture/OFDM/GetCapture-ChanEst` (score 62)
- `SingleCapture/Ofdm-ConstellationDisplay-GetCapture` <= `SingleCapture/OFDM/GetCapture-ConstellationDisplay` (score 80)
- `SingleCapture/Ofdm-ModulationProfile-GetCapture` <= `SingleCapture/OFDM/GetCapture-ModulationProfile` (score 80)
- `SingleCapture/Ofdm-RxMER-GetCapture` <= `SingleCapture/OFDM/GetCapture-RxMER` (score 80)

### name pattern: Ofdma-<X>-GetCapture -> GetCapture-<X>

- `SingleCapture/Ofdma-PreEq-GetCapture` <= `SingleCapture/OFDMA/GetCapture-PreEqualization` (score 64)

### rename: ATDMA-Channel-PreEqualization -> US-ATDMA-PreEqualization

- `DOCSIS-3.0/Upstream/ATDMA-Channel-PreEqualization` <= `DOCSIS-3.0/US-ATDMA-PreEqualization` (score 69)

### rename: ATDMA-Channel-Stats -> US-ATDMA-Stats

- `DOCSIS-3.0/Upstream/ATDMA-Channel-Stats` <= `DOCSIS-3.0/US-ATDMA-Stats` (score 58)

### rename: System-Diplexer -> DiplexConfiguration

- `DOCSIS-3.1/System-Diplexer` <= `DOCSIS-3.1/DiplexConfiguration` (score 26)

### typo normalization: Dectection -> Detection

- `MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Echo-Dectection-IFFT` <= `MultiCapture/OfdmaPreEqualization/OfdmaPreEqualization-Analysis-EchoDetection` (score 73)

## Notes

- This file is a review aid only; no renames or collection edits were performed.
- Postman path/name remains the source of truth for the eventual sync.