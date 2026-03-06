# Postman Visual Sync Dry Run (Revised)

Naming source of truth: `postman/collections/PyPNM/**/*.request.yaml` (Postman request/folder paths).

This report is for **HTML visualizer script path/name alignment**. Shared JSON fixtures are allowed where payload shape is the same (for example SpectrumAnalyzer SNMP vs file variants).

## Summary

- Postman visualizer requests: **22**
- Visual HTML files (`visual/PyPNM/**/*.html`): **31**
- Exact HTML path/name matches now: **0**
- Algorithmic HTML rename/move candidates (no manual dictionary): **4**
- Unmatched Postman visualizer requests after algorithmic pass: **18**
- Extra visual HTML files not mapped to Postman visualizer requests: **27**

## Sync Rules (Applied in Next Step)

- Postman names/paths stay unchanged (source of truth).
- Visual HTML files are renamed/moved to match Postman names/paths 1:1 before script insertion.
- Postman test scripts are updated from matched HTML files only.
- JSON fixtures may be shared across variants when payload shape is identical (not required to be 1:1).

## Exact HTML Path/Name Matches

- None

## Proposed HTML Rename/Move Candidates (Algorithmic, No Manual Dictionary)

- Score 104: `SingleCapture/SpectrumAnalysis/GetCapture-OFDM.html` -> `visual/PyPNM/SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-OFDM.html`
  - JSON pair (optional/shared allowed): `visual/PyPNM/SingleCapture/SpectrumAnalysis/GetCapture-OFDM.json` -> `visual/PyPNM/SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-OFDM.json`
- Score 100: `SingleCapture/SpectrumAnalysis/GetCapture-SCQAM.html` -> `visual/PyPNM/SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-SCQAM.html`
  - JSON pair (optional/shared allowed): `visual/PyPNM/SingleCapture/SpectrumAnalysis/GetCapture-SCQAM.json` -> `visual/PyPNM/SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-SCQAM.json`
- Score 42: `MultiCapture/RxMER/RxMER-Analysis-OFDMA-Profile-Performance-1.html` -> `visual/PyPNM/MultiCapture/RxMER/Ofdm-RxMER-Analysis-Profile-Performance-1.html`
  - JSON pair (optional/shared allowed): `visual/PyPNM/MultiCapture/RxMER/RxMER-Analysis-OFDMA-Profile-Performance-1.json` -> `visual/PyPNM/MultiCapture/RxMER/Ofdm-RxMER-Analysis-Profile-Performance-1.json`
- Score 82: `DOCSIS-General/EventLog.html` -> `visual/PyPNM/Device/EventLog.html`
  - JSON pair (optional/shared allowed): `visual/PyPNM/DOCSIS-General/EventLog.json` -> `visual/PyPNM/Device/EventLog.json`

## Likely Shared-JSON Cases (Informational)

- Postman `SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-OFDM` likely reuses a SpectrumAnalyzer fixture shape; candidate HTML source: `SingleCapture/SpectrumAnalysis/GetCapture-OFDM.html`
- Postman `SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-SCQAM` likely reuses a SpectrumAnalyzer fixture shape; candidate HTML source: `SingleCapture/SpectrumAnalysis/GetCapture-SCQAM.html`

## Unmatched Postman Visualizer Requests (Need Better HTML Name Alignment)

- `SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-FullBandCapture`
- `SingleCapture/Ofdma-PreEq-GetCapture`
- `SingleCapture/Ofdm-RxMER-GetCapture`
- `SingleCapture/Ofdm-ConstellationDisplay-GetCapture`
- `SingleCapture/Histogram-GetCapture`
- `SingleCapture/Ofdm-ModulationProfile-GetCapture`
- `SingleCapture/Ofdm-ChannelEstCoeff-GetCapture`
- `MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Min-Avg-Max`
- `MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Group-Delay`
- `MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Echo-Detection-IFFT`
- `MultiCapture/RxMER/Ofdm-RxMER-Analysis-Min-Avg-Max`
- `MultiCapture/RxMER/Ofdm-RxMER-Analysis-Heat-Map`
- `MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Min-Avg-Max`
- `MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Group-Delay`
- `MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Echo-Dectection-IFFT`
- `DOCSIS-3.0/Upstream/ATDMA-Channel-Stats`
- `DOCSIS-3.0/Upstream/ATDMA-Channel-PreEqualization`
- `DOCSIS-3.1/System-Diplexer`

## Extra Visual HTML Files (Not Mapped to a Postman Visualizer Request Yet)

- `DOCSIS-3.0/DS-SCQAM-CodeErrorRate.html`
- `DOCSIS-3.0/DS-SCQAM-Stats.html`
- `DOCSIS-3.0/US-ATDMA-PreEqualization.html`
- `DOCSIS-3.0/US-ATDMA-Stats.html`
- `DOCSIS-3.1/DS-OFDM-ChannelStats.html`
- `DOCSIS-3.1/DS-OFDM-ProfileStats.html`
- `DOCSIS-3.1/DiplexConfiguration.html`
- `DOCSIS-3.1/US-OFDMA-ChannelStats.html`
- `DOCSIS-General/InterfaceStats.html`
- `MultiCapture/ChannelEstimation/ChannelEstimation-Analysis-Echo-Detection-IFFT.html`
- `MultiCapture/ChannelEstimation/ChannelEstimation-Analysis-GroupDelay.html`
- `MultiCapture/ChannelEstimation/ChannelEstimation-Analysis-MIN_AVG_MAX.html`
- `MultiCapture/OfdmaPreEqualization/OfdmaPreEqualization-Analysis-EchoDetection.html`
- `MultiCapture/OfdmaPreEqualization/OfdmaPreEqualization-Analysis-GroupDelay.html`
- `MultiCapture/OfdmaPreEqualization/OfdmaPreEqualization-Analysis-MinAvgMax.html`
- `MultiCapture/RxMER/RxMER-Analysis-MIn-Avg-Max.html`
- `MultiCapture/RxMER/RxMER-Analysis-Rxmer-Heat-Map.html`
- `SingleCapture/Histogram/Histogram.html`
- `SingleCapture/OFDM/GetCapture-ChanEst.html`
- `SingleCapture/OFDM/GetCapture-ConstellationDisplay.html`
- `SingleCapture/OFDM/GetCapture-FecSummary.html`
- `SingleCapture/OFDM/GetCapture-ModulationProfile.html`
- `SingleCapture/OFDM/GetCapture-RxMER.html`
- `SingleCapture/OFDMA/GetCapture-PreEqualization.html`
- `SingleCapture/SpectrumAnalysis/GetCapture-FBC.html`
- `SingleCapture/SpectrumAnalysis/GetCapture-Friendly.html`
- `SingleCapture/SpectrumAnalysis/GetCapture.html`

## Notes

- No collection or visual files were modified when generating this report.
- Next step (if approved): apply high-confidence HTML renames/moves first, regenerate this report, then sync HTML into Postman test scripts by exact 1:1 path/name.
