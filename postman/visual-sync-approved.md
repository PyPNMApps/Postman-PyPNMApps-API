# Visual Sync Approved Mappings

Postman path/name is the source of truth. This file records interactive approvals for HTML rename/move before collection sync.

## Approved

- `DOCSIS-3.0/Upstream/ATDMA-Channel-PreEqualization` <= `DOCSIS-3.0/US-ATDMA-PreEqualization`
- `DOCSIS-3.0/Upstream/ATDMA-Channel-Stats` <= `DOCSIS-3.0/US-ATDMA-Stats`
- `DOCSIS-3.1/System-Diplexer` <= `DOCSIS-3.1/DiplexConfiguration`
- `Device/EventLog` <= `DOCSIS-General/EventLog`
- `MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Echo-Detection-IFFT` <= `MultiCapture/ChannelEstimation/ChannelEstimation-Analysis-Echo-Detection-IFFT`
- `MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Group-Delay` <= `MultiCapture/ChannelEstimation/ChannelEstimation-Analysis-GroupDelay`
- `MultiCapture/ChannelEstimation/Ofdm-ChannelEstimation-Analysis-Min-Avg-Max` <= `MultiCapture/ChannelEstimation/ChannelEstimation-Analysis-MIN_AVG_MAX`
- `MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Echo-Dectection-IFFT` <= `MultiCapture/OfdmaPreEqualization/OfdmaPreEqualization-Analysis-EchoDetection`
- `MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Group-Delay` <= `MultiCapture/OfdmaPreEqualization/OfdmaPreEqualization-Analysis-GroupDelay`
- `MultiCapture/OFDMA-PreEqualization/Ofdma-PreEqualization-Analysis-Min-Avg-Max` <= `MultiCapture/OfdmaPreEqualization/OfdmaPreEqualization-Analysis-MinAvgMax`
- `MultiCapture/RxMER/Ofdm-RxMER-Analysis-Heat-Map` <= `MultiCapture/RxMER/RxMER-Analysis-Rxmer-Heat-Map`
- `MultiCapture/RxMER/Ofdm-RxMER-Analysis-Min-Avg-Max` <= `MultiCapture/RxMER/RxMER-Analysis-MIn-Avg-Max`
- `MultiCapture/RxMER/Ofdm-RxMER-Analysis-Profile-Performance-1` <= `MultiCapture/RxMER/RxMER-Analysis-OFDMA-Profile-Performance-1`
- `SingleCapture/Ofdm-ChannelEstCoeff-GetCapture` <= `SingleCapture/OFDM/GetCapture-ChanEst`
- `SingleCapture/Ofdm-ConstellationDisplay-GetCapture` <= `SingleCapture/OFDM/GetCapture-ConstellationDisplay`
- `SingleCapture/Ofdm-ModulationProfile-GetCapture` <= `SingleCapture/OFDM/GetCapture-ModulationProfile`
- `SingleCapture/Ofdm-RxMER-GetCapture` <= `SingleCapture/OFDM/GetCapture-RxMER`
- `SingleCapture/Ofdma-PreEq-GetCapture` <= `SingleCapture/OFDMA/GetCapture-PreEqualization`
- `SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-OFDM` <= `SingleCapture/SpectrumAnalysis/GetCapture-OFDM`
- `SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-SCQAM` <= `SingleCapture/SpectrumAnalysis/GetCapture-SCQAM`

## Rejected

- `SingleCapture/Histogram-GetCapture` <= `SingleCapture/SpectrumAnalysis/GetCapture`
- `SingleCapture/SpectrumAnalyzer/Snmp-Upload/GetCapture-FullBandCapture` <= `SingleCapture/SpectrumAnalysis/GetCapture`
