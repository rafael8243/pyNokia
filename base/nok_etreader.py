import lxml.etree as ET
from pathlib import Path

class NokiaXML(object):
    def __init__(self):

        self.xmlFile = ''

        self.all_mo = dict()
        self.all_p = dict()

        self.set_class = set()
        self.set_p = set()

        self.getp = self.getdata_p
        self.startp = self.start_p

        self.this_list = ''

        self.mtype = ['raml']
        self.n = 0


    # DADOS DO PARAMETRO
    def getdata_p(self, d):
        self.this_mo[self.this_p] = d

    def getdada_p_list(self, d):
        if self.this_p in self.this_item:
            self.this_item[self.this_list] += f'¬{d}'
        else:
            self.this_item[self.this_list] = d

    def getdada_p_item(self, d):
        if self.this_p in self.this_item:
            self.this_item[self.this_p] += f'¬{d}'
        else:
            self.this_item[self.this_p] = d


    # INICIO DO PARAMETRO
    def start_p(self, n: str):
        self.this_p = n
        self.set_p.add(self.this_p)

    def start_p_list(self, n = ''):
        self.this_p = self.this_list
        self.set_p.add(self.this_p)

    def start_p_item(self, n: str):
        self.this_p = f'{self.this_list}_{n}'


    # LEITURA
    def start(self, tag, attrib):

        t = tag.split('}')[-1]
        match t:  # Na ordem do mais frequente

            case 'p':
                self.mtype.append('p')

                try:
                    self.startp(attrib.get('name'))
                except (KeyError, TypeError, IndexError):
                    self.startp('') # P sem LIST
                
            case 'list':
                self.mtype.append('list')
                self.startp = self.start_p_list
                self.getp = self.getdada_p_list

                self.this_item = dict()

                self.this_list = attrib.get('name')   #TODO Rever parametros de listas sem ITEM.

            case 'item':
                self.mtype.append('item')
                self.startp = self.start_p_item
                self.getp = self.getdada_p_item

            case 'managedObject':
                self.mtype.append('mo')

                self.mo_id = attrib['id']
                self.mo_class = attrib['class']
                self.mo_dn = attrib['distName']
                
                # Primeiro parâmetro
                self.this_mo = {'xmlfile': self.xmlFile}
                self.set_p.add('xmlfile')

                self.this_mo['DN'] = self.mo_dn
                self.set_p.add('DN')


                sdn = self.mo_dn.split('/')
                for pdn in sdn[1:]:
                    cdn = pdn.split('-')
                    self.this_mo[cdn[0]] = cdn[1]
                    self.set_p.add(cdn[0])
                
                self.this_mo['ID'] = self.mo_id
                self.set_p.add('ID')

                if self.mo_class not in self.set_class:
                    self.all_mo[self.mo_class] = dict()
                    self.all_p[self.mo_class] = list()

                self.set_class.add(self.mo_class)
                

    def end(self, tag):
        
        t = tag.split('}')[-1]
        match t:  # Na ordem do mais frequente

            case 'p':
                self.mtype.pop()
                del self.this_p

            case 'list':
                self.mtype.pop()

                self.this_mo.update(self.this_item)
                del self.this_item

                self.getp = self.getdata_p
                self.startp = self.start_p
                self.this_list = ''

            case 'item':
                self.mtype.pop()
                self.getp = self.getdata_p

            case 'managedObject':
                self.mtype.pop()
                
                # Save this_mo in all_mo dictionary
                self.all_mo[self.mo_class][self.mo_id] = self.this_mo

                # Finds new parameters
                list_newp = list(self.this_mo.keys())
                full_plist = self.all_p[self.mo_class]

                if len(full_plist) >  0:
                    list_missing = list(self.set_p - set(full_plist))

                else:
                    list_missing = list_newp

                # Adds new parameters
                self.all_p[self.mo_class].extend(list_missing)

                self.n +=1
                self.mo_id = 0
                self.mo_class = ''
                self.mo_dn = ''
                self.set_p = set()
                del self.this_mo

    def data(self, data):
        if self.mtype[-1] == 'p':
            self.getp(data)

    def close(self):        
        return self.n


def detect_file_technology(xml_file_path: str) -> set:
    """Scan a single XML file and detect its technology.
    
    Args:
        xml_file_path: Path to XML file to scan
        
    Returns:
        set: Technologies found ('2G', '3G', '4G', '5G')
    """
    tech_set = set()
    
    try:
        # Quick scan to find managedObject class types
        for event, elem in ET.iterparse(xml_file_path, events=('start',)):
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            
            if tag == 'managedObject':
                mo_class = elem.get('class', '')
                
                # Detect technology based on MO class
                if mo_class in ['BSC', 'BCF', 'TRX', 'ADCE', 'BTS']:
                    tech_set.add('2G')
                if mo_class in ['RNC', 'WBTS', 'ADJI', 'WCEL', 'ADJS']:
                    tech_set.add('3G')
                if mo_class in ['LNCEL_FDD', 'IRFIM', 'LNBTS', 'LNCEL', 'LNMME', 'LNBTS_FDD', 'LNADJW', 'LNADJG', 'LNHOIF', 'CAREL', 'SIB']:
                    tech_set.add('4G')
                if mo_class in ['NRBTS', 'NRCELL']:
                    tech_set.add('5G')
    
    except ET.ParseError as e:
        # XML parsing error - file will be skipped
        raise ValueError(f"Invalid XML format in {xml_file_path}: {str(e)}")
    except (IOError, OSError) as e:
        # File access error
        raise ValueError(f"Cannot read file {xml_file_path}: {str(e)}")
    
    return tech_set


def group_files_by_technology(xml_files: list, fprint) -> dict:
    """Group XML files by their technology content.
    
    Validates each file and groups by homogeneous technology.
    Files with mixed technologies are flagged as errors and skipped.
    
    Args:
        xml_files: List of XML file paths to process
        fprint: Callback function for logging messages
        
    Returns:
        dict: Grouped files {technology: [files], 'MIXED': [mixed_files], 'ERRORS': [error_files]}
    """
    grouped_files = {'2G': [], '3G': [], '4G': [], '5G': [], 'MIXED': [], 'ERRORS': []}
    
    for xml_file in xml_files:
        try:
            tech_set = detect_file_technology(xml_file)
            
            if len(tech_set) == 0:
                fprint(f"\n  ⚠ SKIP: {Path(xml_file).name} - No suitable elements found")
                print(tech_set) #TODO RUNTIME CHECK
                grouped_files['ERRORS'].append(xml_file)
            
            elif len(tech_set) > 1:
                # Mixed technology file
                techs_str = ','.join(sorted(tech_set))
                fprint(f"\n  ⚠ ALERT: {Path(xml_file).name} - Mixed technologies ({techs_str})")
                fprint(f"     → File skipped (cannot mix 2G/3G/4G/5G in single output)")
                grouped_files['MIXED'].append(xml_file)
            
            else:
                # Single technology
                tech = list(tech_set)[0]
                grouped_files[tech].append(xml_file)
                fprint(f"\n  ✓ {Path(xml_file).name} - {tech}")
        
        except ValueError as e:
            fprint(f"\n  ✗ ERROR: {str(e)}")
            grouped_files['ERRORS'].append(xml_file)
    
    return grouped_files


def process(xml_files, tmp_path, fReadType, opt_list, fprint):
    """Process XML files grouped by technology into separate outputs.
    
    Creates one output file per technology group. Mixed-tech and error files are skipped.
    
    Args:
        xml_files: List of XML file paths
        tmp_path: Temporary directory for CSV output
        fReadType: Type of read ('DEFAULT' or 'READALL')
        opt_list: List of elements to export in DEFAULT mode
        fprint: Callback function for logging messages
    """
    
    fprint(f"\n\n  >> VALIDATING FILES")
    
    # Group files by technology and validate
    grouped_files = group_files_by_technology(xml_files, fprint)
    
    # Count valid files per technology
    valid_techs = {tech: files for tech, files in grouped_files.items() 
                   if tech not in ['MIXED', 'ERRORS'] and len(files) > 0}
    
    if len(valid_techs) == 0:
        fprint("\n\n  ✗ NO VALID FILES TO PROCESS")
        if len(grouped_files['MIXED']) > 0:
            fprint(f"     {len(grouped_files['MIXED'])} files with mixed technologies were skipped")
        if len(grouped_files['ERRORS']) > 0:
            fprint(f"     {len(grouped_files['ERRORS'])} files had errors and were skipped")
        return {}, {}
    
    fprint(f"\n\n  >> PROCESSING {len(valid_techs)} TECHNOLOGY GROUP(S)")
    
    out_path = Path(xml_files[0]).parent
    params_mini_template = {
        'BSC2G':['name'],
        'RNC3G':['name'],
        'BTS2G':['nwName','adminState','angle','antennaHopping','bsIdentityCodeBCC','bsIdentityCodeNCC','btsIsHopping','cellBarred','cellId','dedicatedGPRScapacity','defaultGPRScapacity','egprsEnabled','fastReturnToLTE','fddQMin','fddQOffset','gprsEnabled','gsmPriority','hoppingMode','hoppingSequenceNumber1','locationAreaIdLAC','maioOffset','maioStep','msMaxDistInCallSetup','nsei','pcuIdentifier','penaltyTime','psei','qSearchI','qSearchP','rxLevAccessMin','timerPeriodicUpdateMs','usedMobileAllocation','wcdmaPriority'],
        'TRX2G':['adminState','channel0Pcm','channel0Type','channel1Type','channel2Type','channel3Type','channel4Type','channel5Type','channel6Type','channel7Type','preferredBcchMark','gprsEnabledTrx','daPool_ID','initialFrequency','lapdLinkName','lapdLinkNumber','tsc'],
        'ADCE2G':['adjCellBsicBcc','adjCellBsicNcc','adjacentCellIdCI','adjacentCellIdLac','adjacentCellIdMCC','adjacentCellIdMNC','adjcIndex','bcchFrequency','targetCellDN'],
        'ADJL2G':['earfcn','lteAdjCellMcc','lteAdjCellMinBand','lteAdjCellMnc','lteAdjCellPriority','lteAdjCellTac'],
        'ADJW2G':['AdjwCId','lac','mcc','mnc','rncId','scramblingCode','uarfcn','targetCellDN'],
        'LNCEL4G':['cellName','name','administrativeState','angle','eutraCelId','expectedCellSize','ilReacTimerUl','lcrId','p0NomPucch','p0NomPusch','p0NomPuschIAw','pFreqPrio','pMax','phyCellId','tac','rcEnableDl','rcEnableUl'],
        'WCEL3G':['name','AdminCellState','angle','CId','FMCLIdentifier','HSDPAenabled','InitialBitRateDL','InitialBitRateUL','LAC','LTECellReselection','PriScrCode','PrxNoise','PtxCellMax','PtxPrimaryCPICH','PtxTarget','QqualMin','QrxlevMin','SectorID','Sintersearch','SintersearchConn','Sintrasearch','Tcell','Treselection','UARFCN'],
        'LNCEL_FDD4G':['actMMimo','addNumDrbRadioReasHo','addNumDrbTimeCriticalHo','addNumQci1DrbRadioReasHo','addNumQci1DrbTimeCriticalHo','dlChBw','dlMimoMode','dlRsBoost','earfcnDL','maxNumActDrb','maxNumActUE','maxNumCaConfUe','maxNumUeDl','maxNumUeUl','prachCS','prachConfIndex','rootSeqIndex','ulChBw'],
        'NRCELL5G':['name','administrativeState','chBw','configuredEpsTac','freqBandIndicatorNR','lcrId','nrCellIdentity','nrarfcn','physCellId','prachRootSequenceIndex'],
        'TRACKINGAREA5G':['TRACKINGAREA','fiveGsTac']
    }
    
    # Process each technology group separately
    for tech in sorted(valid_techs.keys()):
        tech_files = valid_techs[tech]
        
        fprint(f"\n\n  --- Processing {tech} ({len(tech_files)} file(s)) ---")
        
        # Create fresh parser for this technology group
        parser = ET.XMLParser(target=NokiaXML())
        
        # Parse all files in this technology group into the same parser
        for xml_file in tech_files:
            xml_path = Path(xml_file)  # Define before try block
            try:
                parser.target.xmlFile = xml_path.stem
                n = ET.parse(xml_file, parser)
                fprint(f"\n     ✓ {xml_path.name}: {n} elements")
            except ET.ParseError as e:
                fprint(f"\n     ✗ {xml_path.name}: XML parsing error - {str(e)}")
                continue
            except (IOError, OSError) as e:
                fprint(f"\n     ✗ {xml_path.name}: File access error - {str(e)}")
                continue
        
        results = parser.target.all_mo
        params = parser.target.all_p
        
        if len(results) == 0:
            fprint(f"\n     ⚠ No elements extracted from {tech} files")
            continue
        
        # Prepare mini export for this technology
        params_mini = {k: v for k, v in params_mini_template.items() if tech in k}
        
        fprint(f"\n     Exporting {len(results)} element types...")
        
        # Export CSVs for this technology group
        str_added = ''
        for m, d in results.items():
            # Filter export type
            if (fReadType != 'READALL') and (m not in opt_list):
                continue
            
            str_added += '\n    - ' + m.ljust(25) + str(len(d)).rjust(6) + ' elements, ' + str(len(params[m])).rjust(3) + ' params'
            
            output_file = Path(tmp_path) / f'{m}_{tech}.csv'
            
            try:
                with open(output_file, 'w', encoding='utf-8') as out:
                    # Sort parameters alphabetically
                    pList = params[m]
                    ibp = pList.index('ID') + 1
                    
                    bp = pList[:ibp]
                    pNames = pList[ibp:]
                    pNames.sort()
                    
                    bp.extend(pNames)
                    mycols = '|'.join(bp)
                    
                    out.write(mycols)
                    out.write('\n')
                    
                    lines = []
                    for id_val, p in d.items():
                        line = '|'.join(p.get(pp, '') for pp in bp)
                        lines.append(line)
                    out.write('\n'.join(lines))
            
            except (IOError, OSError) as e:
                fprint(f"\n     ✗ Error writing {output_file.name}: {str(e)}")
                continue
            
            # Mini export if available for this element
            if f'{m + tech}' in params_mini.keys():
                output_file_mini = out_path / f'{m + tech}.csv'
                
                try:
                    with open(output_file_mini, 'w', encoding='utf-8') as out_mini:
                        pList_mini = params_mini[m + tech]
                        ibp = pList.index('ID') + 1
                        
                        bp = pList[:ibp]
                        pNames_mini = pList_mini.copy()
                        pNames_mini.sort()
                        
                        bp.extend(pNames_mini)
                        mycols_mini = '|'.join(bp)
                        
                        out_mini.write(mycols_mini)
                        out_mini.write('\n')
                        
                        for id_mini, p_mini in d.items():
                            myvals_mini = ''
                            for pp_mini in bp:
                                try:
                                    myvals_mini += '|' + p_mini.get(pp_mini, '')
                                except (KeyError, TypeError, AttributeError):
                                    myvals_mini += '|'
                            
                            myvals_mini = myvals_mini[1:] + '\n'
                            out_mini.write(myvals_mini)
                
                except (IOError, OSError) as e:
                    fprint(f"\n     ✗ Error writing mini export {output_file_mini.name}: {str(e)}")
                    continue
        
        fprint(str_added)
    
    # Summary report
    fprint(f"\n\n  >> SUMMARY")
    fprint(f"\n     Processed: {sum(len(files) for files in valid_techs.values())} file(s)")
    fprint(f"\n     Skipped (Mixed): {len(grouped_files['MIXED'])}")
    fprint(f"\n     Skipped (Errors): {len(grouped_files['ERRORS'])}")
    fprint(f"\n     Technology groups: {len(valid_techs)}")
    
    # Return mapping of technology to CSV files and original files for Excel generation
    csv_by_tech = {}
    for tech in valid_techs.keys():
        csv_files = list(Path(tmp_path).glob(f'*_{tech}.csv'))
        if csv_files:
            csv_by_tech[tech] = csv_files
    
    return csv_by_tech, valid_techs


