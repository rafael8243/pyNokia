
"""
Configuration constants for NOKIA Parser II application.

Contains all magic strings, technology definitions, and processing parameters.
"""

# ============================================================================
# DEFAULT ELEMENT EXPORT LIST
# ============================================================================
# Elements exported when using 'DEFAULT' read mode (vs 'READALL')
DEFAULT_ELEMENT_LIST = [
    'LNCEL_FDD', 'LNBTS', 'LNCEL', 'IRFIM', 'SIB', 'LNMME', 'MOPR',
    'LNADJW', 'LNADJG', 'LNHOIF', 'CAREL', 'LNBTS_FDD', 'WNCELG', 'WNBTS',
    'ADJI', 'WBTS', 'ADJS', 'ADJD', 'WCEL', 'FMCS', 'HOPS',
    'COCO', 'ADJG', 'ADJL', 'RNC', 'LAPD', 'MAL', 'TRX',
    'BCF', 'DAP', 'BTS', 'ADCE', 'ADJW', 'BAL', 'BSC'
]

# ============================================================================
# TECHNOLOGY DETECTION - MANAGED OBJECT (MO) CLASSES
# ============================================================================
# MO classes that identify each technology in XML dumps
TECH_2G_MOS = {
    'BSC', 'BCF', 'TRX', 'ADCE', 'MAL', 'BTS'
}

TECH_3G_MOS = {
    'RNC', 'WBTS', 'ADJI', 'WCEL'
}

TECH_4G_MOS = {
    'LNCEL_FDD', 'IRFIM', 'LNBTS', 'LNCEL', 'LNMME',
    'LNBTS_FDD', 'LNADJW', 'LNADJG', 'LNHOIF', 'CAREL', 'SIB'
}

TECH_5G_MOS = {
    'NRBTS', 'NRCELL'
}

# Mapping of technology to its MO set (for programmatic access)
TECH_INDICATORS = {
    '2G': TECH_2G_MOS,
    '3G': TECH_3G_MOS,
    '4G': TECH_4G_MOS,
    '5G': TECH_5G_MOS,
}

# ============================================================================
# MINI EXPORT PARAMETER TEMPLATES BY TECHNOLOGY AND ELEMENT TYPE
# ============================================================================
# Defines which parameters to export for specific element types in mini exports
PARAMS_MINI_TEMPLATE = {
    'BSC2G': ['name'],
    'RNC3G': ['name'],
    'BTS2G': [
        'nwName', 'adminState', 'angle', 'antennaHopping', 'bsIdentityCodeBCC',
        'bsIdentityCodeNCC', 'btsIsHopping', 'cellBarred', 'cellId',
        'dedicatedGPRScapacity', 'defaultGPRScapacity', 'egprsEnabled',
        'fastReturnToLTE', 'fddQMin', 'fddQOffset', 'gprsEnabled', 'gsmPriority',
        'hoppingMode', 'hoppingSequenceNumber1', 'locationAreaIdLAC', 'maioOffset',
        'maioStep', 'msMaxDistInCallSetup', 'nsei', 'pcuIdentifier', 'penaltyTime',
        'psei', 'qSearchI', 'qSearchP', 'rxLevAccessMin', 'timerPeriodicUpdateMs',
        'usedMobileAllocation', 'wcdmaPriority'
    ],
    'TRX2G': [
        'adminState', 'channel0Pcm', 'channel0Type', 'channel1Type', 'channel2Type',
        'channel3Type', 'channel4Type', 'channel5Type', 'channel6Type', 'channel7Type',
        'preferredBcchMark', 'gprsEnabledTrx', 'daPool_ID', 'initialFrequency',
        'lapdLinkName', 'lapdLinkNumber', 'tsc'
    ],
    'ADCE2G': [
        'adjCellBsicBcc', 'adjCellBsicNcc', 'adjacentCellIdCI', 'adjacentCellIdLac',
        'adjacentCellIdMCC', 'adjacentCellIdMNC', 'adjcIndex', 'bcchFrequency',
        'targetCellDN'
    ],
    'ADJL2G': [
        'earfcn', 'lteAdjCellMcc', 'lteAdjCellMinBand', 'lteAdjCellMnc',
        'lteAdjCellPriority', 'lteAdjCellTac'
    ],
    'ADJW2G': [
        'AdjwCId', 'lac', 'mcc', 'mnc', 'rncId', 'scramblingCode', 'uarfcn',
        'targetCellDN'
    ],
    'LNCEL4G': [
        'cellName', 'name', 'administrativeState', 'angle', 'eutraCelId',
        'expectedCellSize', 'ilReacTimerUl', 'lcrId', 'p0NomPucch', 'p0NomPusch',
        'p0NomPuschIAw', 'pFreqPrio', 'pMax', 'phyCellId', 'tac', 'rcEnableDl',
        'rcEnableUl'
    ],
    'WCEL3G': [
        'name', 'AdminCellState', 'angle', 'CId', 'FMCLIdentifier', 'HSDPAenabled',
        'InitialBitRateDL', 'InitialBitRateUL', 'LAC', 'LTECellReselection',
        'PriScrCode', 'PrxNoise', 'PtxCellMax', 'PtxPrimaryCPICH', 'PtxTarget',
        'QqualMin', 'QrxlevMin', 'SectorID', 'Sintersearch', 'SintersearchConn',
        'Sintrasearch', 'Tcell', 'Treselection', 'UARFCN'
    ],
    'LNCEL_FDD4G': [
        'actMMimo', 'addNumDrbRadioReasHo', 'addNumDrbTimeCriticalHo',
        'addNumQci1DrbRadioReasHo', 'addNumQci1DrbTimeCriticalHo', 'dlChBw',
        'dlMimoMode', 'dlRsBoost', 'earfcnDL', 'maxNumActDrb', 'maxNumActUE',
        'maxNumCaConfUe', 'maxNumUeDl', 'maxNumUeUl', 'prachCS', 'prachConfIndex',
        'rootSeqIndex', 'ulChBw'
    ],
    'NRCELL5G': [
        'name', 'administrativeState', 'chBw', 'configuredEpsTac',
        'freqBandIndicatorNR', 'lcrId', 'nrCellIdentity', 'nrarfcn',
        'physCellId', 'prachRootSequenceIndex'
    ],
    'TRACKINGAREA5G': [
        'TRACKINGAREA', 'fiveGsTac'
    ]
}

# ============================================================================
# CSV PROCESSING SETTINGS
# ============================================================================
# CSV file format and encoding settings
CSV_DELIMITER = '|'
CSV_ENCODING = 'iso-8859-1'

# ============================================================================
# TEMPORARY DIRECTORY SETTINGS
# ============================================================================
# Prefix for temporary directories created during processing
TEMP_DIR_PREFIX = '_dn'

# ============================================================================
# GUI SETTINGS
# ============================================================================
# Default window dimensions
DEFAULT_WINDOW_WIDTH = 550
DEFAULT_WINDOW_HEIGHT = 600
DEFAULT_TEXT_AREA_BG = 'lightgray'

# ============================================================================
# FILE PROCESSING SETTINGS
# ============================================================================
# Nokia dump file identifier patterns (replaced with DUMP in output)
NOKIA_IDENTIFIER_PATTERN = r"NOK[345]"

# Output file extension
OUTPUT_FILE_EXTENSION = '.xlsx'
