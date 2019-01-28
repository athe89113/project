<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<?mso-application progid="Word.Document"?>
<pkg:package xmlns:pkg="http://schemas.microsoft.com/office/2006/xmlPackage">
    <pkg:part pkg:name="/_rels/.rels" pkg:contentType="application/vnd.openxmlformats-package.relationships+xml"
              pkg:padding="512">
        <pkg:xmlData>
            <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
                <Relationship Id="rId3"
                              Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties"
                              Target="docProps/app.xml"/>
                <Relationship Id="rId2"
                              Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties"
                              Target="docProps/core.xml"/>
                <Relationship Id="rId1"
                              Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
                              Target="word/document.xml"/>
            </Relationships>
        </pkg:xmlData>
    </pkg:part>
    <pkg:part pkg:name="/word/_rels/document.xml.rels"
              pkg:contentType="application/vnd.openxmlformats-package.relationships+xml" pkg:padding="256">
        <pkg:xmlData>
            <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
                <Relationship Id="rId8"
                              Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable"
                              Target="fontTable.xml"/>
                <Relationship Id="rId3"
                              Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings"
                              Target="settings.xml"/>
                <Relationship Id="rId2" Type="http://schemas.microsoft.com/office/2007/relationships/stylesWithEffects"
                              Target="stylesWithEffects.xml"/>
                <Relationship Id="rId1"
                              Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"
                              Target="styles.xml"/>
                <Relationship Id="rId6"
                              Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/endnotes"
                              Target="endnotes.xml"/>
                <Relationship Id="rId5"
                              Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes"
                              Target="footnotes.xml"/>
                <Relationship Id="rId4"
                              Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/webSettings"
                              Target="webSettings.xml"/>
                <Relationship Id="rId9" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme"
                              Target="theme/theme1.xml"/>
                <#list imgs as item>
                    <Relationship Id="rId${item_index+100}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
                              Target="media/image${item_index}.jpg"/>
                </#list>
            </Relationships>
        </pkg:xmlData>
    </pkg:part>
    <pkg:part pkg:name="/word/document.xml"
              pkg:contentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml">
        <pkg:xmlData>
            <w:document mc:Ignorable="w14 wp14"
                        xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
                        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                        xmlns:o="urn:schemas-microsoft-com:office:office"
                        xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                        xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
                        xmlns:v="urn:schemas-microsoft-com:vml"
                        xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
                        xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
                        xmlns:w10="urn:schemas-microsoft-com:office:word"
                        xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                        xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
                        xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
                        xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
                        xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
                        xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">
                <w:body>
                    <#list content as item>
                        <#if item.type == 'module' >
                            <w:p w:rsidR="000B3C56" w:rsidRDefault="000B3C56" w:rsidP="000B3C56">
                                <w:pPr>
                                    <w:pStyle w:val="a3"/>
                                    <w:rPr>
                                        <w:rFonts w:asciiTheme="majorEastAsia" w:eastAsiaTheme="majorEastAsia"
                                                  w:hAnsiTheme="majorEastAsia"/>
                                    </w:rPr>
                                </w:pPr>
                                <w:r>
                                    <w:rPr>
                                        <w:rFonts w:hint="eastAsia"/>
                                    </w:rPr>
                                    <w:t>${item.params.title}</w:t>
                                </w:r>
                            </w:p>
                            <w:p w:rsidR="000B3C56" w:rsidRPr="00D420CE" w:rsidRDefault="000B3C56" w:rsidP="000B3C56">
                                <w:pPr>
                                    <w:pStyle w:val="a4"/>
                                    <w:rPr>
                                        <w:rFonts w:asciiTheme="majorEastAsia" w:eastAsiaTheme="majorEastAsia"
                                                  w:hAnsiTheme="majorEastAsia"/>
                                        <w:b w:val="0"/>
                                    </w:rPr>
                                </w:pPr>
                                <w:r w:rsidRPr="00D420CE">
                                    <w:rPr>
                                        <w:rFonts w:asciiTheme="majorEastAsia" w:eastAsiaTheme="majorEastAsia"
                                                  w:hAnsiTheme="majorEastAsia" w:hint="eastAsia"/>
                                        <w:b w:val="0"/>
                                    </w:rPr>
                                    <w:t>${item.params.time}</w:t>
                                </w:r>
                            </w:p>
                        <#elseif item.type == 'title1' >
                            <w:p w:rsidR="000B3C56" w:rsidRPr="000B3C56" w:rsidRDefault="000B3C56" w:rsidP="000B3C56">
                                <w:pPr>
                                    <w:pStyle w:val="1"/>
                                    <w:rPr>
                                        <w:rFonts w:asciiTheme="majorEastAsia" w:eastAsiaTheme="majorEastAsia"
                                                  w:hAnsiTheme="majorEastAsia"/>
                                    </w:rPr>
                                </w:pPr>
                                <w:r w:rsidRPr="000B3C56">
                                    <w:rPr>
                                        <w:rFonts w:asciiTheme="majorEastAsia" w:eastAsiaTheme="majorEastAsia"
                                                  w:hAnsiTheme="majorEastAsia" w:hint="eastAsia"/>
                                    </w:rPr>
                                    <w:t>${item.params.title}</w:t>
                                </w:r>
                            </w:p>
                        <#elseif item.type == 'title2' >
                            <w:p w:rsidR="000B3C56" w:rsidRPr="000B3C56" w:rsidRDefault="000B3C56" w:rsidP="000B3C56">
                                <w:pPr>
                                    <w:pStyle w:val="2"/>
                                </w:pPr>
                                <w:r w:rsidRPr="000B3C56">
                                    <w:rPr>
                                        <w:rFonts w:hint="eastAsia"/>
                                    </w:rPr>
                                    <w:t>${item.params.title}</w:t>
                                </w:r>
                            </w:p>
                        <#elseif item.type == 'title3' >
                            <w:p w:rsidR="000B3C56" w:rsidRPr="000B3C56" w:rsidRDefault="000B3C56" w:rsidP="000B3C56">
                                <w:pPr>
                                    <w:pStyle w:val="3"/>
                                </w:pPr>
                                <w:r w:rsidRPr="000B3C56">
                                    <w:rPr>
                                        <w:rFonts w:hint="eastAsia"/>
                                    </w:rPr>
                                    <w:t>${item.params.title}</w:t>
                                </w:r>
                            </w:p>
                        <#elseif item.type == 'title4' >
                            <w:p w:rsidR="000B3C56" w:rsidRDefault="000B3C56" w:rsidP="000B3C56">
                                <w:pPr>
                                    <w:pStyle w:val="4"/>
                                    <w:rPr>
                                        <w:rFonts w:hint="eastAsia"/>
                                    </w:rPr>
                                </w:pPr>
                                <w:r w:rsidRPr="000B3C56">
                                    <w:rPr>
                                        <w:rFonts w:hint="eastAsia"/>
                                    </w:rPr>
                                    <w:t>${item.params.title}</w:t>
                                </w:r>
                            </w:p>
                        <#elseif item.type == 'text' >
                            <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE">
                                <w:pPr>
                                    <w:rPr>
                                        <w:rFonts w:hint="eastAsia"/>
                                    </w:rPr>
                                </w:pPr>
                                <w:r>
                                    <w:rPr>
                                        <w:rFonts w:hint="eastAsia"/>
                                    </w:rPr>
                                    <w:t>${item.params.title}</w:t>
                                </w:r>
                            </w:p>
                        <#else>
                            <#if item.chart_type == 'table' >
                                <#if item.name??>
                                    <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE">
                                        <w:pPr>
                                            <w:rPr>
                                                <w:rFonts w:hint="eastAsia"/>
                                            </w:rPr>
                                        </w:pPr>
                                        <w:r>
                                            <w:rPr>
                                                <w:rFonts w:hint="eastAsia"/>
                                            </w:rPr>
                                            <w:t>${item.name}</w:t>
                                        </w:r>
                                    </w:p>
                                </#if>
                                <w:tbl>
                                    <w:tblPr>
                                        <w:tblStyle w:val="a8"/>
                                        <w:tblW w:w="0" w:type="auto"/>
                                        <w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0"
                                                   w:noHBand="0" w:noVBand="1"/>
                                    </w:tblPr>
                                    <w:tblGrid>
                                        <#list item.data.labels as lab>
                                            <w:gridCol w:w="${(8520/((item.data.labels?size)+1))?c}"/>
                                        </#list>
                                    </w:tblGrid>
                                    <w:tr w:rsidR="00D420CE" w:rsidTr="00D420CE">
                                        <w:tc>
                                            <w:tcPr>
                                                <w:tcW w:w="${(8520/((item.data.labels?size)+1))?c}" w:type="dxa"/>
                                            </w:tcPr>
                                            <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE"/>
                                        </w:tc>
                                        <#list item.data.labels as lab>
                                            <w:tc>
                                                <w:tcPr>
                                                    <w:tcW w:w="${(8520/((item.data.labels?size)+1))?c}" w:type="dxa"/>
                                                </w:tcPr>
                                                <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE">
                                                    <w:r>
                                                        <w:rPr>
                                                            <w:rFonts w:hint="eastAsia"/>
                                                        </w:rPr>
                                                        <w:t>${lab}</w:t>
                                                    </w:r>
                                                </w:p>
                                            </w:tc>
                                        </#list>
                                    </w:tr>
                                    <#list item.data.data as tr>
                                        <w:tr w:rsidR="00D420CE" w:rsidTr="00D420CE">
                                            <w:tc>
                                                <w:tcPr>
                                                    <w:tcW w:w="${(8520/((item.data.labels?size)+1))?c}" w:type="dxa"/>
                                                </w:tcPr>
                                                <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE">
                                                    <w:r>
                                                        <w:rPr>
                                                            <w:rFonts w:hint="eastAsia"/>
                                                        </w:rPr>
                                                        <w:t>${tr.name}</w:t>
                                                    </w:r>
                                                </w:p>
                                            </w:tc>
                                            <#list tr.data as td>
                                                <w:tc>
                                                    <w:tcPr>
                                                        <w:tcW w:w="${(8520/((item.data.labels?size)+1))?c}" w:type="dxa"/>
                                                    </w:tcPr>
                                                    <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE">
                                                        <w:r>
                                                            <w:rPr>
                                                                <w:rFonts w:hint="eastAsia"/>
                                                            </w:rPr>
                                                            <w:t>${td}</w:t>
                                                        </w:r>
                                                    </w:p>
                                                </w:tc>
                                            </#list>
                                        </w:tr>
                                    </#list>
                                </w:tbl>
                            <#elseif item.chart_type == 'table_merge' >
                                <w:tbl>
                                    <w:tblPr>
                                        <w:tblStyle w:val="a8"/>
                                        <w:tblW w:w="0" w:type="auto"/>
                                        <w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0"
                                                   w:noHBand="0" w:noVBand="1"/>
                                    </w:tblPr>
                                    <w:tblGrid>
                                        <#list item.widths as wid>
                                            <w:gridCol w:w="${(wid * 1420)?c}"/>
                                        </#list>
                                    </w:tblGrid>
                                    <w:tr w:rsidR="00D420CE" w:rsidTr="00D420CE">
                                        <#list item.data.labels as lab>
                                            <w:tc>
                                                <w:tcPr>
                                                    <w:tcW w:w="${(item.widths[lab_index] * 1420)?c}" w:type="dxa"/>
                                                </w:tcPr>
                                                <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE">
                                                    <w:r>
                                                        <w:rPr>
                                                            <w:rFonts w:hint="eastAsia"/>
                                                        </w:rPr>
                                                        <w:t>${lab}</w:t>
                                                    </w:r>
                                                </w:p>
                                            </w:tc>
                                        </#list>
                                    </w:tr>
                                    <#list item.data.data as tr>
                                        <w:tr w:rsidR="00D420CE" w:rsidTr="00D420CE">
                                            <#list tr as td>
                                                <#assign mer = item.merges?seq_contains(td_index)?string("yes", "no") />
                                                    <#if mer=='yes' && (item.data.index?size >0)>
                                                        <#assign ind = item.data.index?seq_contains(tr_index)?string("yes", "no") />
                                                        <#if ind=='yes'>
                                                            <w:tc>
                                                                <w:tcPr>
                                                                    <w:tcW w:w="${(item.widths[td_index] * 1420)?c}" w:type="dxa"/>
                                                                    <w:vMerge w:val="restart"/>
                                                                </w:tcPr>
                                                                <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE">
                                                                    <w:r>
                                                                        <w:rPr>
                                                                            <w:rFonts w:hint="eastAsia"/>
                                                                        </w:rPr>
                                                                        <w:t>${td}</w:t>
                                                                    </w:r>
                                                                </w:p>
                                                            </w:tc>
                                                        <#else>
                                                            <w:tc>
                                                                <w:tcPr>
                                                                    <w:tcW w:w="${(item.widths[td_index] * 1420)?c}" w:type="dxa"/>
                                                                    <w:vMerge/>
                                                                </w:tcPr>
                                                                <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE" />
                                                            </w:tc>
                                                        </#if >
                                                    <#else>
                                                        <w:tc>
                                                            <w:tcPr>
                                                                <w:tcW w:w="${(item.widths[td_index] * 1420)?c}" w:type="dxa"/>
                                                            </w:tcPr>
                                                            <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE">
                                                                <w:r>
                                                                    <w:rPr>
                                                                        <w:rFonts w:hint="eastAsia"/>
                                                                    </w:rPr>
                                                                    <w:t>${td}</w:t>
                                                                </w:r>
                                                            </w:p>
                                                        </w:tc>
                                                    </#if >
                                            </#list>
                                        </w:tr>
                                    </#list>
                                </w:tbl>
                            <#elseif item.chart_type == 'number' >
                                <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE">
                                    <w:pPr>
                                        <w:rPr>
                                            <w:rFonts w:hint="eastAsia"/>
                                        </w:rPr>
                                    </w:pPr>
                                    <w:r>
                                        <w:rPr>
                                            <w:rFonts w:hint="eastAsia"/>
                                        </w:rPr>
                                        <w:t>${item.name}:${item.count}</w:t>
                                    </w:r>
                                </w:p>
                            <#elseif item.chart_type == 'img' >
                                <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE">
                                    <w:pPr>
                                        <w:rPr>
                                            <w:rFonts w:hint="eastAsia"/>
                                        </w:rPr>
                                    </w:pPr>
                                    <w:r>
                                        <w:rPr>
                                            <w:noProof/>
                                        </w:rPr>
                                        <w:drawing>
                                            <wp:inline distT="0" distB="0" distL="0" distR="0">
                                                <wp:extent cx="5274310" cy="3335020"/>
                                                <wp:effectExtent l="0" t="0" r="2540" b="0"/>
                                                <wp:docPr id="${item.img_index}" name="${item.name}"/>
                                                <wp:cNvGraphicFramePr>
                                                    <a:graphicFrameLocks noChangeAspect="1"
                                                                         xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>
                                                </wp:cNvGraphicFramePr>
                                                <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                                                    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
                                                        <pic:pic
                                                                xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
                                                            <pic:nvPicPr>
                                                                <pic:cNvPr id="0" name="adminBg.jpg"/>
                                                                <pic:cNvPicPr/>
                                                            </pic:nvPicPr>
                                                            <pic:blipFill>
                                                                <a:blip r:embed="rId${item.img_index+100}" cstate="print">
                                                                    <a:extLst>
                                                                        <a:ext uri="{28A0092B-C50C-407E-A947-70E740481C1C}">
                                                                            <a14:useLocalDpi val="0"
                                                                                             xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main"/>
                                                                        </a:ext>
                                                                    </a:extLst>
                                                                </a:blip>
                                                                <a:stretch>
                                                                    <a:fillRect/>
                                                                </a:stretch>
                                                            </pic:blipFill>
                                                            <pic:spPr>
                                                                <a:xfrm>
                                                                    <a:off x="0" y="0"/>
                                                                    <a:ext cx="5274310" cy="3335020"/>
                                                                </a:xfrm>
                                                                <a:prstGeom prst="rect">
                                                                    <a:avLst/>
                                                                </a:prstGeom>
                                                            </pic:spPr>
                                                        </pic:pic>
                                                    </a:graphicData>
                                                </a:graphic>
                                            </wp:inline>
                                        </w:drawing>
                                    </w:r>
                                </w:p>
                                <#if (item.has_table?exists) && item.has_table==1 >
                                    <w:tbl>
                                        <w:tblPr>
                                            <w:tblStyle w:val="a8"/>
                                            <w:tblW w:w="0" w:type="auto"/>
                                            <w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0"
                                                       w:noHBand="0" w:noVBand="1"/>
                                        </w:tblPr>
                                        <w:tblGrid>
                                            <#list item.data.labels as lab>
                                                <w:gridCol w:w="${(8520/((item.data.labels?size)+1))?c}"/>
                                            </#list>
                                        </w:tblGrid>
                                        <w:tr w:rsidR="00D420CE" w:rsidTr="00D420CE">
                                            <w:tc>
                                                <w:tcPr>
                                                    <w:tcW w:w="${(8520/((item.data.labels?size)+1))?c}" w:type="dxa"/>
                                                </w:tcPr>
                                                <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE"/>
                                            </w:tc>
                                            <#list item.data.labels as lab>
                                                <w:tc>
                                                    <w:tcPr>
                                                        <w:tcW w:w="${(8520/((item.data.labels?size)+1))?c}" w:type="dxa"/>
                                                    </w:tcPr>
                                                    <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE">
                                                        <w:r>
                                                            <w:rPr>
                                                                <w:rFonts w:hint="eastAsia"/>
                                                            </w:rPr>
                                                            <w:t>${lab}</w:t>
                                                        </w:r>
                                                    </w:p>
                                                </w:tc>
                                            </#list>
                                        </w:tr>
                                        <#list item.data.data as tr>
                                            <w:tr w:rsidR="00D420CE" w:rsidTr="00D420CE">
                                                <w:tc>
                                                    <w:tcPr>
                                                        <w:tcW w:w="${(8520/((item.data.labels?size)+1))?c}" w:type="dxa"/>
                                                    </w:tcPr>
                                                    <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE">
                                                        <w:r>
                                                            <w:rPr>
                                                                <w:rFonts w:hint="eastAsia"/>
                                                            </w:rPr>
                                                            <w:t>${tr.name}</w:t>
                                                        </w:r>
                                                    </w:p>
                                                </w:tc>
                                                <#list tr.data as td>
                                                    <w:tc>
                                                        <w:tcPr>
                                                            <w:tcW w:w="${(8520/((item.data.labels?size)+1))?c}" w:type="dxa"/>
                                                        </w:tcPr>
                                                        <w:p w:rsidR="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE">
                                                            <w:r>
                                                                <w:rPr>
                                                                    <w:rFonts w:hint="eastAsia"/>
                                                                </w:rPr>
                                                                <w:t>${td}</w:t>
                                                            </w:r>
                                                        </w:p>
                                                    </w:tc>
                                                </#list>
                                            </w:tr>
                                        </#list>
                                    </w:tbl>
                                </#if>
                            <#else>
                                new type
                            </#if>
                        </#if>
                    </#list>

                    <w:p w:rsidR="00D420CE" w:rsidRPr="00D420CE" w:rsidRDefault="00D420CE" w:rsidP="00D420CE"/>
                    <w:sectPr w:rsidR="00D420CE" w:rsidRPr="00D420CE">
                        <w:pgSz w:w="11906" w:h="16838"/>
                        <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800" w:header="851" w:footer="992"
                                 w:gutter="0"/>
                        <w:cols w:space="425"/>
                        <w:docGrid w:type="lines" w:linePitch="312"/>
                    </w:sectPr>
                </w:body>
            </w:document>
        </pkg:xmlData>
    </pkg:part>
    <pkg:part pkg:name="/word/footnotes.xml"
              pkg:contentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml">
        <pkg:xmlData>
            <w:footnotes mc:Ignorable="w14 wp14"
                         xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
                         xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                         xmlns:o="urn:schemas-microsoft-com:office:office"
                         xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                         xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
                         xmlns:v="urn:schemas-microsoft-com:vml"
                         xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
                         xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
                         xmlns:w10="urn:schemas-microsoft-com:office:word"
                         xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                         xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
                         xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
                         xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
                         xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
                         xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">
                <w:footnote w:type="separator" w:id="-1">
                    <w:p w:rsidR="00927FB2" w:rsidRDefault="00927FB2" w:rsidP="00D420CE">
                        <w:r>
                            <w:separator/>
                        </w:r>
                    </w:p>
                </w:footnote>
                <w:footnote w:type="continuationSeparator" w:id="0">
                    <w:p w:rsidR="00927FB2" w:rsidRDefault="00927FB2" w:rsidP="00D420CE">
                        <w:r>
                            <w:continuationSeparator/>
                        </w:r>
                    </w:p>
                </w:footnote>
            </w:footnotes>
        </pkg:xmlData>
    </pkg:part>
    <pkg:part pkg:name="/word/endnotes.xml"
              pkg:contentType="application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml">
        <pkg:xmlData>
            <w:endnotes mc:Ignorable="w14 wp14"
                        xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
                        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                        xmlns:o="urn:schemas-microsoft-com:office:office"
                        xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                        xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
                        xmlns:v="urn:schemas-microsoft-com:vml"
                        xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
                        xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
                        xmlns:w10="urn:schemas-microsoft-com:office:word"
                        xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                        xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
                        xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
                        xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
                        xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
                        xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">
                <w:endnote w:type="separator" w:id="-1">
                    <w:p w:rsidR="00927FB2" w:rsidRDefault="00927FB2" w:rsidP="00D420CE">
                        <w:r>
                            <w:separator/>
                        </w:r>
                    </w:p>
                </w:endnote>
                <w:endnote w:type="continuationSeparator" w:id="0">
                    <w:p w:rsidR="00927FB2" w:rsidRDefault="00927FB2" w:rsidP="00D420CE">
                        <w:r>
                            <w:continuationSeparator/>
                        </w:r>
                    </w:p>
                </w:endnote>
            </w:endnotes>
        </pkg:xmlData>
    </pkg:part>
    <pkg:part pkg:name="/word/theme/theme1.xml"
              pkg:contentType="application/vnd.openxmlformats-officedocument.theme+xml">
        <pkg:xmlData>
            <a:theme name="Office 主题​​" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                <a:themeElements>
                    <a:clrScheme name="Office">
                        <a:dk1>
                            <a:sysClr val="windowText" lastClr="000000"/>
                        </a:dk1>
                        <a:lt1>
                            <a:sysClr val="window" lastClr="FFFFFF"/>
                        </a:lt1>
                        <a:dk2>
                            <a:srgbClr val="1F497D"/>
                        </a:dk2>
                        <a:lt2>
                            <a:srgbClr val="EEECE1"/>
                        </a:lt2>
                        <a:accent1>
                            <a:srgbClr val="4F81BD"/>
                        </a:accent1>
                        <a:accent2>
                            <a:srgbClr val="C0504D"/>
                        </a:accent2>
                        <a:accent3>
                            <a:srgbClr val="9BBB59"/>
                        </a:accent3>
                        <a:accent4>
                            <a:srgbClr val="8064A2"/>
                        </a:accent4>
                        <a:accent5>
                            <a:srgbClr val="4BACC6"/>
                        </a:accent5>
                        <a:accent6>
                            <a:srgbClr val="F79646"/>
                        </a:accent6>
                        <a:hlink>
                            <a:srgbClr val="0000FF"/>
                        </a:hlink>
                        <a:folHlink>
                            <a:srgbClr val="800080"/>
                        </a:folHlink>
                    </a:clrScheme>
                    <a:fontScheme name="Office">
                        <a:majorFont>
                            <a:latin typeface="Cambria"/>
                            <a:ea typeface=""/>
                            <a:cs typeface=""/>
                            <a:font script="Jpan" typeface="ＭＳ ゴシック"/>
                            <a:font script="Hang" typeface="맑은 고딕"/>
                            <a:font script="Hans" typeface="宋体"/>
                            <a:font script="Hant" typeface="新細明體"/>
                            <a:font script="Arab" typeface="Times New Roman"/>
                            <a:font script="Hebr" typeface="Times New Roman"/>
                            <a:font script="Thai" typeface="Angsana New"/>
                            <a:font script="Ethi" typeface="Nyala"/>
                            <a:font script="Beng" typeface="Vrinda"/>
                            <a:font script="Gujr" typeface="Shruti"/>
                            <a:font script="Khmr" typeface="MoolBoran"/>
                            <a:font script="Knda" typeface="Tunga"/>
                            <a:font script="Guru" typeface="Raavi"/>
                            <a:font script="Cans" typeface="Euphemia"/>
                            <a:font script="Cher" typeface="Plantagenet Cherokee"/>
                            <a:font script="Yiii" typeface="Microsoft Yi Baiti"/>
                            <a:font script="Tibt" typeface="Microsoft Himalaya"/>
                            <a:font script="Thaa" typeface="MV Boli"/>
                            <a:font script="Deva" typeface="Mangal"/>
                            <a:font script="Telu" typeface="Gautami"/>
                            <a:font script="Taml" typeface="Latha"/>
                            <a:font script="Syrc" typeface="Estrangelo Edessa"/>
                            <a:font script="Orya" typeface="Kalinga"/>
                            <a:font script="Mlym" typeface="Kartika"/>
                            <a:font script="Laoo" typeface="DokChampa"/>
                            <a:font script="Sinh" typeface="Iskoola Pota"/>
                            <a:font script="Mong" typeface="Mongolian Baiti"/>
                            <a:font script="Viet" typeface="Times New Roman"/>
                            <a:font script="Uigh" typeface="Microsoft Uighur"/>
                            <a:font script="Geor" typeface="Sylfaen"/>
                        </a:majorFont>
                        <a:minorFont>
                            <a:latin typeface="Calibri"/>
                            <a:ea typeface=""/>
                            <a:cs typeface=""/>
                            <a:font script="Jpan" typeface="ＭＳ 明朝"/>
                            <a:font script="Hang" typeface="맑은 고딕"/>
                            <a:font script="Hans" typeface="宋体"/>
                            <a:font script="Hant" typeface="新細明體"/>
                            <a:font script="Arab" typeface="Arial"/>
                            <a:font script="Hebr" typeface="Arial"/>
                            <a:font script="Thai" typeface="Cordia New"/>
                            <a:font script="Ethi" typeface="Nyala"/>
                            <a:font script="Beng" typeface="Vrinda"/>
                            <a:font script="Gujr" typeface="Shruti"/>
                            <a:font script="Khmr" typeface="DaunPenh"/>
                            <a:font script="Knda" typeface="Tunga"/>
                            <a:font script="Guru" typeface="Raavi"/>
                            <a:font script="Cans" typeface="Euphemia"/>
                            <a:font script="Cher" typeface="Plantagenet Cherokee"/>
                            <a:font script="Yiii" typeface="Microsoft Yi Baiti"/>
                            <a:font script="Tibt" typeface="Microsoft Himalaya"/>
                            <a:font script="Thaa" typeface="MV Boli"/>
                            <a:font script="Deva" typeface="Mangal"/>
                            <a:font script="Telu" typeface="Gautami"/>
                            <a:font script="Taml" typeface="Latha"/>
                            <a:font script="Syrc" typeface="Estrangelo Edessa"/>
                            <a:font script="Orya" typeface="Kalinga"/>
                            <a:font script="Mlym" typeface="Kartika"/>
                            <a:font script="Laoo" typeface="DokChampa"/>
                            <a:font script="Sinh" typeface="Iskoola Pota"/>
                            <a:font script="Mong" typeface="Mongolian Baiti"/>
                            <a:font script="Viet" typeface="Arial"/>
                            <a:font script="Uigh" typeface="Microsoft Uighur"/>
                            <a:font script="Geor" typeface="Sylfaen"/>
                        </a:minorFont>
                    </a:fontScheme>
                    <a:fmtScheme name="Office">
                        <a:fillStyleLst>
                            <a:solidFill>
                                <a:schemeClr val="phClr"/>
                            </a:solidFill>
                            <a:gradFill rotWithShape="1">
                                <a:gsLst>
                                    <a:gs pos="0">
                                        <a:schemeClr val="phClr">
                                            <a:tint val="50000"/>
                                            <a:satMod val="300000"/>
                                        </a:schemeClr>
                                    </a:gs>
                                    <a:gs pos="35000">
                                        <a:schemeClr val="phClr">
                                            <a:tint val="37000"/>
                                            <a:satMod val="300000"/>
                                        </a:schemeClr>
                                    </a:gs>
                                    <a:gs pos="100000">
                                        <a:schemeClr val="phClr">
                                            <a:tint val="15000"/>
                                            <a:satMod val="350000"/>
                                        </a:schemeClr>
                                    </a:gs>
                                </a:gsLst>
                                <a:lin ang="16200000" scaled="1"/>
                            </a:gradFill>
                            <a:gradFill rotWithShape="1">
                                <a:gsLst>
                                    <a:gs pos="0">
                                        <a:schemeClr val="phClr">
                                            <a:shade val="51000"/>
                                            <a:satMod val="130000"/>
                                        </a:schemeClr>
                                    </a:gs>
                                    <a:gs pos="80000">
                                        <a:schemeClr val="phClr">
                                            <a:shade val="93000"/>
                                            <a:satMod val="130000"/>
                                        </a:schemeClr>
                                    </a:gs>
                                    <a:gs pos="100000">
                                        <a:schemeClr val="phClr">
                                            <a:shade val="94000"/>
                                            <a:satMod val="135000"/>
                                        </a:schemeClr>
                                    </a:gs>
                                </a:gsLst>
                                <a:lin ang="16200000" scaled="0"/>
                            </a:gradFill>
                        </a:fillStyleLst>
                        <a:lnStyleLst>
                            <a:ln w="9525" cap="flat" cmpd="sng" algn="ctr">
                                <a:solidFill>
                                    <a:schemeClr val="phClr">
                                        <a:shade val="95000"/>
                                        <a:satMod val="105000"/>
                                    </a:schemeClr>
                                </a:solidFill>
                                <a:prstDash val="solid"/>
                            </a:ln>
                            <a:ln w="25400" cap="flat" cmpd="sng" algn="ctr">
                                <a:solidFill>
                                    <a:schemeClr val="phClr"/>
                                </a:solidFill>
                                <a:prstDash val="solid"/>
                            </a:ln>
                            <a:ln w="38100" cap="flat" cmpd="sng" algn="ctr">
                                <a:solidFill>
                                    <a:schemeClr val="phClr"/>
                                </a:solidFill>
                                <a:prstDash val="solid"/>
                            </a:ln>
                        </a:lnStyleLst>
                        <a:effectStyleLst>
                            <a:effectStyle>
                                <a:effectLst>
                                    <a:outerShdw blurRad="40000" dist="20000" dir="5400000" rotWithShape="0">
                                        <a:srgbClr val="000000">
                                            <a:alpha val="38000"/>
                                        </a:srgbClr>
                                    </a:outerShdw>
                                </a:effectLst>
                            </a:effectStyle>
                            <a:effectStyle>
                                <a:effectLst>
                                    <a:outerShdw blurRad="40000" dist="23000" dir="5400000" rotWithShape="0">
                                        <a:srgbClr val="000000">
                                            <a:alpha val="35000"/>
                                        </a:srgbClr>
                                    </a:outerShdw>
                                </a:effectLst>
                            </a:effectStyle>
                            <a:effectStyle>
                                <a:effectLst>
                                    <a:outerShdw blurRad="40000" dist="23000" dir="5400000" rotWithShape="0">
                                        <a:srgbClr val="000000">
                                            <a:alpha val="35000"/>
                                        </a:srgbClr>
                                    </a:outerShdw>
                                </a:effectLst>
                                <a:scene3d>
                                    <a:camera prst="orthographicFront">
                                        <a:rot lat="0" lon="0" rev="0"/>
                                    </a:camera>
                                    <a:lightRig rig="threePt" dir="t">
                                        <a:rot lat="0" lon="0" rev="1200000"/>
                                    </a:lightRig>
                                </a:scene3d>
                                <a:sp3d>
                                    <a:bevelT w="63500" h="25400"/>
                                </a:sp3d>
                            </a:effectStyle>
                        </a:effectStyleLst>
                        <a:bgFillStyleLst>
                            <a:solidFill>
                                <a:schemeClr val="phClr"/>
                            </a:solidFill>
                            <a:gradFill rotWithShape="1">
                                <a:gsLst>
                                    <a:gs pos="0">
                                        <a:schemeClr val="phClr">
                                            <a:tint val="40000"/>
                                            <a:satMod val="350000"/>
                                        </a:schemeClr>
                                    </a:gs>
                                    <a:gs pos="40000">
                                        <a:schemeClr val="phClr">
                                            <a:tint val="45000"/>
                                            <a:shade val="99000"/>
                                            <a:satMod val="350000"/>
                                        </a:schemeClr>
                                    </a:gs>
                                    <a:gs pos="100000">
                                        <a:schemeClr val="phClr">
                                            <a:shade val="20000"/>
                                            <a:satMod val="255000"/>
                                        </a:schemeClr>
                                    </a:gs>
                                </a:gsLst>
                                <a:path path="circle">
                                    <a:fillToRect l="50000" t="-80000" r="50000" b="180000"/>
                                </a:path>
                            </a:gradFill>
                            <a:gradFill rotWithShape="1">
                                <a:gsLst>
                                    <a:gs pos="0">
                                        <a:schemeClr val="phClr">
                                            <a:tint val="80000"/>
                                            <a:satMod val="300000"/>
                                        </a:schemeClr>
                                    </a:gs>
                                    <a:gs pos="100000">
                                        <a:schemeClr val="phClr">
                                            <a:shade val="30000"/>
                                            <a:satMod val="200000"/>
                                        </a:schemeClr>
                                    </a:gs>
                                </a:gsLst>
                                <a:path path="circle">
                                    <a:fillToRect l="50000" t="50000" r="50000" b="50000"/>
                                </a:path>
                            </a:gradFill>
                        </a:bgFillStyleLst>
                    </a:fmtScheme>
                </a:themeElements>
                <a:objectDefaults/>
                <a:extraClrSchemeLst/>
            </a:theme>
        </pkg:xmlData>
    </pkg:part>
    <#list imgs as item>
        <pkg:part pkg:name="/word/media/image${item_index}.jpg" pkg:contentType="image/jpeg" pkg:compression="store">
        <pkg:binaryData>${item}
        </pkg:binaryData>
    </pkg:part>
    </#list>
    <pkg:part pkg:name="/word/settings.xml"
              pkg:contentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml">
        <pkg:xmlData>
            <w:settings mc:Ignorable="w14" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                        xmlns:o="urn:schemas-microsoft-com:office:office"
                        xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                        xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
                        xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w10="urn:schemas-microsoft-com:office:word"
                        xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                        xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
                        xmlns:sl="http://schemas.openxmlformats.org/schemaLibrary/2006/main">
                <w:zoom w:percent="105"/>
                <w:bordersDoNotSurroundHeader/>
                <w:bordersDoNotSurroundFooter/>
                <w:proofState w:grammar="clean"/>
                <w:defaultTabStop w:val="420"/>
                <w:drawingGridVerticalSpacing w:val="156"/>
                <w:displayHorizontalDrawingGridEvery w:val="0"/>
                <w:displayVerticalDrawingGridEvery w:val="2"/>
                <w:characterSpacingControl w:val="compressPunctuation"/>
                <w:hdrShapeDefaults>
                    <o:shapedefaults v:ext="edit" spidmax="2049"/>
                </w:hdrShapeDefaults>
                <w:footnotePr>
                    <w:footnote w:id="-1"/>
                    <w:footnote w:id="0"/>
                </w:footnotePr>
                <w:endnotePr>
                    <w:endnote w:id="-1"/>
                    <w:endnote w:id="0"/>
                </w:endnotePr>
                <w:compat>
                    <w:spaceForUL/>
                    <w:balanceSingleByteDoubleByteWidth/>
                    <w:doNotLeaveBackslashAlone/>
                    <w:ulTrailSpace/>
                    <w:doNotExpandShiftReturn/>
                    <w:adjustLineHeightInTable/>
                    <w:useFELayout/>
                    <w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word"
                                     w:val="14"/>
                    <w:compatSetting w:name="overrideTableStyleFontSizeAndJustification"
                                     w:uri="http://schemas.microsoft.com/office/word" w:val="1"/>
                    <w:compatSetting w:name="enableOpenTypeFeatures" w:uri="http://schemas.microsoft.com/office/word"
                                     w:val="1"/>
                    <w:compatSetting w:name="doNotFlipMirrorIndents" w:uri="http://schemas.microsoft.com/office/word"
                                     w:val="1"/>
                </w:compat>
                <w:rsids>
                    <w:rsidRoot w:val="00E7578F"/>
                    <w:rsid w:val="000B3C56"/>
                    <w:rsid w:val="001F5BF1"/>
                    <w:rsid w:val="00826842"/>
                    <w:rsid w:val="00927FB2"/>
                    <w:rsid w:val="00D420CE"/>
                    <w:rsid w:val="00E7578F"/>
                </w:rsids>
                <m:mathPr>
                    <m:mathFont m:val="Cambria Math"/>
                    <m:brkBin m:val="before"/>
                    <m:brkBinSub m:val="--"/>
                    <m:smallFrac m:val="0"/>
                    <m:dispDef/>
                    <m:lMargin m:val="0"/>
                    <m:rMargin m:val="0"/>
                    <m:defJc m:val="centerGroup"/>
                    <m:wrapIndent m:val="1440"/>
                    <m:intLim m:val="subSup"/>
                    <m:naryLim m:val="undOvr"/>
                </m:mathPr>
                <w:themeFontLang w:val="en-US" w:eastAsia="zh-CN"/>
                <w:clrSchemeMapping w:bg1="light1" w:t1="dark1" w:bg2="light2" w:t2="dark2" w:accent1="accent1"
                                    w:accent2="accent2" w:accent3="accent3" w:accent4="accent4" w:accent5="accent5"
                                    w:accent6="accent6" w:hyperlink="hyperlink"
                                    w:followedHyperlink="followedHyperlink"/>
                <w:shapeDefaults>
                    <o:shapedefaults v:ext="edit" spidmax="2049"/>
                    <o:shapelayout v:ext="edit">
                        <o:idmap v:ext="edit" data="1"/>
                    </o:shapelayout>
                </w:shapeDefaults>
                <w:decimalSymbol w:val="."/>
                <w:listSeparator w:val=","/>
            </w:settings>
        </pkg:xmlData>
    </pkg:part>
    <pkg:part pkg:name="/word/webSettings.xml"
              pkg:contentType="application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml">
        <pkg:xmlData>
            <w:webSettings mc:Ignorable="w14" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                           xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                           xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                           xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
                <w:optimizeForBrowser/>
                <w:allowPNG/>
            </w:webSettings>
        </pkg:xmlData>
    </pkg:part>
    <pkg:part pkg:name="/word/stylesWithEffects.xml" pkg:contentType="application/vnd.ms-word.stylesWithEffects+xml">
        <pkg:xmlData>
            <w:styles mc:Ignorable="w14 wp14"
                      xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
                      xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                      xmlns:o="urn:schemas-microsoft-com:office:office"
                      xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                      xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
                      xmlns:v="urn:schemas-microsoft-com:vml"
                      xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
                      xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
                      xmlns:w10="urn:schemas-microsoft-com:office:word"
                      xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                      xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
                      xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
                      xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
                      xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
                      xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">
                <w:docDefaults>
                    <w:rPrDefault>
                        <w:rPr>
                            <w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia"
                                      w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi"/>
                            <w:kern w:val="2"/>
                            <w:sz w:val="21"/>
                            <w:szCs w:val="22"/>
                            <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="ar-SA"/>
                        </w:rPr>
                    </w:rPrDefault>
                    <w:pPrDefault/>
                </w:docDefaults>
                <w:latentStyles w:defLockedState="0" w:defUIPriority="99" w:defSemiHidden="1" w:defUnhideWhenUsed="1"
                                w:defQFormat="0" w:count="267">
                    <w:lsdException w:name="Normal" w:semiHidden="0" w:uiPriority="0" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="heading 1" w:semiHidden="0" w:uiPriority="9" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="heading 2" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="heading 3" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="heading 4" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="heading 5" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="heading 6" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="heading 7" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="heading 8" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="heading 9" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="toc 1" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 2" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 3" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 4" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 5" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 6" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 7" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 8" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 9" w:uiPriority="39"/>
                    <w:lsdException w:name="caption" w:uiPriority="35" w:qFormat="1"/>
                    <w:lsdException w:name="Title" w:semiHidden="0" w:uiPriority="10" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Default Paragraph Font" w:uiPriority="1"/>
                    <w:lsdException w:name="Subtitle" w:semiHidden="0" w:uiPriority="11" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Strong" w:semiHidden="0" w:uiPriority="22" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Emphasis" w:semiHidden="0" w:uiPriority="20" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Table Grid" w:semiHidden="0" w:uiPriority="59" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Placeholder Text" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="No Spacing" w:semiHidden="0" w:uiPriority="1" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Light Shading" w:semiHidden="0" w:uiPriority="60" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light List" w:semiHidden="0" w:uiPriority="61" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Grid" w:semiHidden="0" w:uiPriority="62" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 1" w:semiHidden="0" w:uiPriority="63" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 2" w:semiHidden="0" w:uiPriority="64" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 1" w:semiHidden="0" w:uiPriority="65" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 2" w:semiHidden="0" w:uiPriority="66" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 1" w:semiHidden="0" w:uiPriority="67" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 2" w:semiHidden="0" w:uiPriority="68" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 3" w:semiHidden="0" w:uiPriority="69" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Dark List" w:semiHidden="0" w:uiPriority="70" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Shading" w:semiHidden="0" w:uiPriority="71" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful List" w:semiHidden="0" w:uiPriority="72" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Grid" w:semiHidden="0" w:uiPriority="73" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Shading Accent 1" w:semiHidden="0" w:uiPriority="60"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light List Accent 1" w:semiHidden="0" w:uiPriority="61"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Grid Accent 1" w:semiHidden="0" w:uiPriority="62"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 1 Accent 1" w:semiHidden="0" w:uiPriority="63"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 2 Accent 1" w:semiHidden="0" w:uiPriority="64"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 1 Accent 1" w:semiHidden="0" w:uiPriority="65"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Revision" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="List Paragraph" w:semiHidden="0" w:uiPriority="34" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Quote" w:semiHidden="0" w:uiPriority="29" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Intense Quote" w:semiHidden="0" w:uiPriority="30" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Medium List 2 Accent 1" w:semiHidden="0" w:uiPriority="66"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 1 Accent 1" w:semiHidden="0" w:uiPriority="67"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 2 Accent 1" w:semiHidden="0" w:uiPriority="68"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 3 Accent 1" w:semiHidden="0" w:uiPriority="69"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Dark List Accent 1" w:semiHidden="0" w:uiPriority="70"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Shading Accent 1" w:semiHidden="0" w:uiPriority="71"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful List Accent 1" w:semiHidden="0" w:uiPriority="72"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Grid Accent 1" w:semiHidden="0" w:uiPriority="73"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Shading Accent 2" w:semiHidden="0" w:uiPriority="60"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light List Accent 2" w:semiHidden="0" w:uiPriority="61"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Grid Accent 2" w:semiHidden="0" w:uiPriority="62"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 1 Accent 2" w:semiHidden="0" w:uiPriority="63"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 2 Accent 2" w:semiHidden="0" w:uiPriority="64"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 1 Accent 2" w:semiHidden="0" w:uiPriority="65"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 2 Accent 2" w:semiHidden="0" w:uiPriority="66"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 1 Accent 2" w:semiHidden="0" w:uiPriority="67"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 2 Accent 2" w:semiHidden="0" w:uiPriority="68"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 3 Accent 2" w:semiHidden="0" w:uiPriority="69"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Dark List Accent 2" w:semiHidden="0" w:uiPriority="70"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Shading Accent 2" w:semiHidden="0" w:uiPriority="71"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful List Accent 2" w:semiHidden="0" w:uiPriority="72"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Grid Accent 2" w:semiHidden="0" w:uiPriority="73"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Shading Accent 3" w:semiHidden="0" w:uiPriority="60"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light List Accent 3" w:semiHidden="0" w:uiPriority="61"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Grid Accent 3" w:semiHidden="0" w:uiPriority="62"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 1 Accent 3" w:semiHidden="0" w:uiPriority="63"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 2 Accent 3" w:semiHidden="0" w:uiPriority="64"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 1 Accent 3" w:semiHidden="0" w:uiPriority="65"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 2 Accent 3" w:semiHidden="0" w:uiPriority="66"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 1 Accent 3" w:semiHidden="0" w:uiPriority="67"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 2 Accent 3" w:semiHidden="0" w:uiPriority="68"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 3 Accent 3" w:semiHidden="0" w:uiPriority="69"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Dark List Accent 3" w:semiHidden="0" w:uiPriority="70"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Shading Accent 3" w:semiHidden="0" w:uiPriority="71"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful List Accent 3" w:semiHidden="0" w:uiPriority="72"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Grid Accent 3" w:semiHidden="0" w:uiPriority="73"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Shading Accent 4" w:semiHidden="0" w:uiPriority="60"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light List Accent 4" w:semiHidden="0" w:uiPriority="61"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Grid Accent 4" w:semiHidden="0" w:uiPriority="62"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 1 Accent 4" w:semiHidden="0" w:uiPriority="63"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 2 Accent 4" w:semiHidden="0" w:uiPriority="64"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 1 Accent 4" w:semiHidden="0" w:uiPriority="65"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 2 Accent 4" w:semiHidden="0" w:uiPriority="66"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 1 Accent 4" w:semiHidden="0" w:uiPriority="67"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 2 Accent 4" w:semiHidden="0" w:uiPriority="68"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 3 Accent 4" w:semiHidden="0" w:uiPriority="69"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Dark List Accent 4" w:semiHidden="0" w:uiPriority="70"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Shading Accent 4" w:semiHidden="0" w:uiPriority="71"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful List Accent 4" w:semiHidden="0" w:uiPriority="72"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Grid Accent 4" w:semiHidden="0" w:uiPriority="73"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Shading Accent 5" w:semiHidden="0" w:uiPriority="60"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light List Accent 5" w:semiHidden="0" w:uiPriority="61"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Grid Accent 5" w:semiHidden="0" w:uiPriority="62"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 1 Accent 5" w:semiHidden="0" w:uiPriority="63"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 2 Accent 5" w:semiHidden="0" w:uiPriority="64"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 1 Accent 5" w:semiHidden="0" w:uiPriority="65"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 2 Accent 5" w:semiHidden="0" w:uiPriority="66"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 1 Accent 5" w:semiHidden="0" w:uiPriority="67"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 2 Accent 5" w:semiHidden="0" w:uiPriority="68"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 3 Accent 5" w:semiHidden="0" w:uiPriority="69"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Dark List Accent 5" w:semiHidden="0" w:uiPriority="70"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Shading Accent 5" w:semiHidden="0" w:uiPriority="71"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful List Accent 5" w:semiHidden="0" w:uiPriority="72"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Grid Accent 5" w:semiHidden="0" w:uiPriority="73"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Shading Accent 6" w:semiHidden="0" w:uiPriority="60"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light List Accent 6" w:semiHidden="0" w:uiPriority="61"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Grid Accent 6" w:semiHidden="0" w:uiPriority="62"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 1 Accent 6" w:semiHidden="0" w:uiPriority="63"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 2 Accent 6" w:semiHidden="0" w:uiPriority="64"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 1 Accent 6" w:semiHidden="0" w:uiPriority="65"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 2 Accent 6" w:semiHidden="0" w:uiPriority="66"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 1 Accent 6" w:semiHidden="0" w:uiPriority="67"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 2 Accent 6" w:semiHidden="0" w:uiPriority="68"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 3 Accent 6" w:semiHidden="0" w:uiPriority="69"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Dark List Accent 6" w:semiHidden="0" w:uiPriority="70"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Shading Accent 6" w:semiHidden="0" w:uiPriority="71"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful List Accent 6" w:semiHidden="0" w:uiPriority="72"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Grid Accent 6" w:semiHidden="0" w:uiPriority="73"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Subtle Emphasis" w:semiHidden="0" w:uiPriority="19" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Intense Emphasis" w:semiHidden="0" w:uiPriority="21" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Subtle Reference" w:semiHidden="0" w:uiPriority="31" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Intense Reference" w:semiHidden="0" w:uiPriority="32" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Book Title" w:semiHidden="0" w:uiPriority="33" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Bibliography" w:uiPriority="37"/>
                    <w:lsdException w:name="TOC Heading" w:uiPriority="39" w:qFormat="1"/>
                </w:latentStyles>
                <w:style w:type="paragraph" w:default="1" w:styleId="a">
                    <w:name w:val="Normal"/>
                    <w:qFormat/>
                    <w:pPr>
                        <w:widowControl w:val="0"/>
                        <w:jc w:val="both"/>
                    </w:pPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="1">
                    <w:name w:val="heading 1"/>
                    <w:basedOn w:val="a"/>
                    <w:next w:val="a"/>
                    <w:link w:val="1Char"/>
                    <w:uiPriority w:val="9"/>
                    <w:qFormat/>
                    <w:rsid w:val="000B3C56"/>
                    <w:pPr>
                        <w:keepNext/>
                        <w:keepLines/>
                        <w:spacing w:before="340" w:after="330" w:line="578" w:lineRule="auto"/>
                        <w:outlineLvl w:val="0"/>
                    </w:pPr>
                    <w:rPr>
                        <w:b/>
                        <w:bCs/>
                        <w:kern w:val="44"/>
                        <w:sz w:val="44"/>
                        <w:szCs w:val="44"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="2">
                    <w:name w:val="heading 2"/>
                    <w:basedOn w:val="a"/>
                    <w:next w:val="a"/>
                    <w:link w:val="2Char"/>
                    <w:uiPriority w:val="9"/>
                    <w:unhideWhenUsed/>
                    <w:qFormat/>
                    <w:rsid w:val="000B3C56"/>
                    <w:pPr>
                        <w:keepNext/>
                        <w:keepLines/>
                        <w:spacing w:before="260" w:after="260" w:line="416" w:lineRule="auto"/>
                        <w:outlineLvl w:val="1"/>
                    </w:pPr>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsiaTheme="majorEastAsia" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="3">
                    <w:name w:val="heading 3"/>
                    <w:basedOn w:val="a"/>
                    <w:next w:val="a"/>
                    <w:link w:val="3Char"/>
                    <w:uiPriority w:val="9"/>
                    <w:unhideWhenUsed/>
                    <w:qFormat/>
                    <w:rsid w:val="000B3C56"/>
                    <w:pPr>
                        <w:keepNext/>
                        <w:keepLines/>
                        <w:spacing w:before="260" w:after="260" w:line="416" w:lineRule="auto"/>
                        <w:outlineLvl w:val="2"/>
                    </w:pPr>
                    <w:rPr>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="4">
                    <w:name w:val="heading 4"/>
                    <w:basedOn w:val="a"/>
                    <w:next w:val="a"/>
                    <w:link w:val="4Char"/>
                    <w:uiPriority w:val="9"/>
                    <w:unhideWhenUsed/>
                    <w:qFormat/>
                    <w:rsid w:val="000B3C56"/>
                    <w:pPr>
                        <w:keepNext/>
                        <w:keepLines/>
                        <w:spacing w:before="280" w:after="290" w:line="376" w:lineRule="auto"/>
                        <w:outlineLvl w:val="3"/>
                    </w:pPr>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsiaTheme="majorEastAsia" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="28"/>
                        <w:szCs w:val="28"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:default="1" w:styleId="a0">
                    <w:name w:val="Default Paragraph Font"/>
                    <w:uiPriority w:val="1"/>
                    <w:semiHidden/>
                    <w:unhideWhenUsed/>
                </w:style>
                <w:style w:type="table" w:default="1" w:styleId="a1">
                    <w:name w:val="Normal Table"/>
                    <w:uiPriority w:val="99"/>
                    <w:semiHidden/>
                    <w:unhideWhenUsed/>
                    <w:tblPr>
                        <w:tblInd w:w="0" w:type="dxa"/>
                        <w:tblCellMar>
                            <w:top w:w="0" w:type="dxa"/>
                            <w:left w:w="108" w:type="dxa"/>
                            <w:bottom w:w="0" w:type="dxa"/>
                            <w:right w:w="108" w:type="dxa"/>
                        </w:tblCellMar>
                    </w:tblPr>
                </w:style>
                <w:style w:type="numbering" w:default="1" w:styleId="a2">
                    <w:name w:val="No List"/>
                    <w:uiPriority w:val="99"/>
                    <w:semiHidden/>
                    <w:unhideWhenUsed/>
                </w:style>
                <w:style w:type="paragraph" w:styleId="a3">
                    <w:name w:val="Title"/>
                    <w:basedOn w:val="a"/>
                    <w:next w:val="a"/>
                    <w:link w:val="Char"/>
                    <w:uiPriority w:val="10"/>
                    <w:qFormat/>
                    <w:rsid w:val="000B3C56"/>
                    <w:pPr>
                        <w:spacing w:before="240" w:after="60"/>
                        <w:jc w:val="center"/>
                        <w:outlineLvl w:val="0"/>
                    </w:pPr>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsia="宋体" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="Char">
                    <w:name w:val="标题 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="a3"/>
                    <w:uiPriority w:val="10"/>
                    <w:rsid w:val="000B3C56"/>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsia="宋体" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="a4">
                    <w:name w:val="Subtitle"/>
                    <w:basedOn w:val="a"/>
                    <w:next w:val="a"/>
                    <w:link w:val="Char0"/>
                    <w:uiPriority w:val="11"/>
                    <w:qFormat/>
                    <w:rsid w:val="000B3C56"/>
                    <w:pPr>
                        <w:spacing w:before="240" w:after="60" w:line="312" w:lineRule="auto"/>
                        <w:jc w:val="center"/>
                        <w:outlineLvl w:val="1"/>
                    </w:pPr>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsia="宋体" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:kern w:val="28"/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="Char0">
                    <w:name w:val="副标题 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="a4"/>
                    <w:uiPriority w:val="11"/>
                    <w:rsid w:val="000B3C56"/>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsia="宋体" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:kern w:val="28"/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="1Char">
                    <w:name w:val="标题 1 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="1"/>
                    <w:uiPriority w:val="9"/>
                    <w:rsid w:val="000B3C56"/>
                    <w:rPr>
                        <w:b/>
                        <w:bCs/>
                        <w:kern w:val="44"/>
                        <w:sz w:val="44"/>
                        <w:szCs w:val="44"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="2Char">
                    <w:name w:val="标题 2 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="2"/>
                    <w:uiPriority w:val="9"/>
                    <w:rsid w:val="000B3C56"/>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsiaTheme="majorEastAsia" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="3Char">
                    <w:name w:val="标题 3 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="3"/>
                    <w:uiPriority w:val="9"/>
                    <w:rsid w:val="000B3C56"/>
                    <w:rPr>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="4Char">
                    <w:name w:val="标题 4 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="4"/>
                    <w:uiPriority w:val="9"/>
                    <w:rsid w:val="000B3C56"/>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsiaTheme="majorEastAsia" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="28"/>
                        <w:szCs w:val="28"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="a5">
                    <w:name w:val="header"/>
                    <w:basedOn w:val="a"/>
                    <w:link w:val="Char1"/>
                    <w:uiPriority w:val="99"/>
                    <w:unhideWhenUsed/>
                    <w:rsid w:val="00D420CE"/>
                    <w:pPr>
                        <w:pBdr>
                            <w:bottom w:val="single" w:sz="6" w:space="1" w:color="auto"/>
                        </w:pBdr>
                        <w:tabs>
                            <w:tab w:val="center" w:pos="4153"/>
                            <w:tab w:val="right" w:pos="8306"/>
                        </w:tabs>
                        <w:snapToGrid w:val="0"/>
                        <w:jc w:val="center"/>
                    </w:pPr>
                    <w:rPr>
                        <w:sz w:val="18"/>
                        <w:szCs w:val="18"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="Char1">
                    <w:name w:val="页眉 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="a5"/>
                    <w:uiPriority w:val="99"/>
                    <w:rsid w:val="00D420CE"/>
                    <w:rPr>
                        <w:sz w:val="18"/>
                        <w:szCs w:val="18"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="a6">
                    <w:name w:val="footer"/>
                    <w:basedOn w:val="a"/>
                    <w:link w:val="Char2"/>
                    <w:uiPriority w:val="99"/>
                    <w:unhideWhenUsed/>
                    <w:rsid w:val="00D420CE"/>
                    <w:pPr>
                        <w:tabs>
                            <w:tab w:val="center" w:pos="4153"/>
                            <w:tab w:val="right" w:pos="8306"/>
                        </w:tabs>
                        <w:snapToGrid w:val="0"/>
                        <w:jc w:val="left"/>
                    </w:pPr>
                    <w:rPr>
                        <w:sz w:val="18"/>
                        <w:szCs w:val="18"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="Char2">
                    <w:name w:val="页脚 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="a6"/>
                    <w:uiPriority w:val="99"/>
                    <w:rsid w:val="00D420CE"/>
                    <w:rPr>
                        <w:sz w:val="18"/>
                        <w:szCs w:val="18"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="a7">
                    <w:name w:val="Balloon Text"/>
                    <w:basedOn w:val="a"/>
                    <w:link w:val="Char3"/>
                    <w:uiPriority w:val="99"/>
                    <w:semiHidden/>
                    <w:unhideWhenUsed/>
                    <w:rsid w:val="00D420CE"/>
                    <w:rPr>
                        <w:sz w:val="18"/>
                        <w:szCs w:val="18"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="Char3">
                    <w:name w:val="批注框文本 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="a7"/>
                    <w:uiPriority w:val="99"/>
                    <w:semiHidden/>
                    <w:rsid w:val="00D420CE"/>
                    <w:rPr>
                        <w:sz w:val="18"/>
                        <w:szCs w:val="18"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="table" w:styleId="a8">
                    <w:name w:val="Table Grid"/>
                    <w:basedOn w:val="a1"/>
                    <w:uiPriority w:val="59"/>
                    <w:rsid w:val="00D420CE"/>
                    <w:tblPr>
                        <w:tblBorders>
                            <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                            <w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                            <w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                        </w:tblBorders>
                    </w:tblPr>
                </w:style>
            </w:styles>
        </pkg:xmlData>
    </pkg:part>
    <pkg:part pkg:name="/word/styles.xml"
              pkg:contentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml">
        <pkg:xmlData>
            <w:styles mc:Ignorable="w14" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                      xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                      xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                      xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
                <w:docDefaults>
                    <w:rPrDefault>
                        <w:rPr>
                            <w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia"
                                      w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi"/>
                            <w:kern w:val="2"/>
                            <w:sz w:val="21"/>
                            <w:szCs w:val="22"/>
                            <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="ar-SA"/>
                        </w:rPr>
                    </w:rPrDefault>
                    <w:pPrDefault/>
                </w:docDefaults>
                <w:latentStyles w:defLockedState="0" w:defUIPriority="99" w:defSemiHidden="1" w:defUnhideWhenUsed="1"
                                w:defQFormat="0" w:count="267">
                    <w:lsdException w:name="Normal" w:semiHidden="0" w:uiPriority="0" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="heading 1" w:semiHidden="0" w:uiPriority="9" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="heading 2" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="heading 3" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="heading 4" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="heading 5" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="heading 6" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="heading 7" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="heading 8" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="heading 9" w:uiPriority="9" w:qFormat="1"/>
                    <w:lsdException w:name="toc 1" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 2" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 3" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 4" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 5" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 6" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 7" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 8" w:uiPriority="39"/>
                    <w:lsdException w:name="toc 9" w:uiPriority="39"/>
                    <w:lsdException w:name="caption" w:uiPriority="35" w:qFormat="1"/>
                    <w:lsdException w:name="Title" w:semiHidden="0" w:uiPriority="10" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Default Paragraph Font" w:uiPriority="1"/>
                    <w:lsdException w:name="Subtitle" w:semiHidden="0" w:uiPriority="11" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Strong" w:semiHidden="0" w:uiPriority="22" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Emphasis" w:semiHidden="0" w:uiPriority="20" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Table Grid" w:semiHidden="0" w:uiPriority="59" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Placeholder Text" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="No Spacing" w:semiHidden="0" w:uiPriority="1" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Light Shading" w:semiHidden="0" w:uiPriority="60" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light List" w:semiHidden="0" w:uiPriority="61" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Grid" w:semiHidden="0" w:uiPriority="62" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 1" w:semiHidden="0" w:uiPriority="63" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 2" w:semiHidden="0" w:uiPriority="64" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 1" w:semiHidden="0" w:uiPriority="65" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 2" w:semiHidden="0" w:uiPriority="66" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 1" w:semiHidden="0" w:uiPriority="67" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 2" w:semiHidden="0" w:uiPriority="68" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 3" w:semiHidden="0" w:uiPriority="69" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Dark List" w:semiHidden="0" w:uiPriority="70" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Shading" w:semiHidden="0" w:uiPriority="71" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful List" w:semiHidden="0" w:uiPriority="72" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Grid" w:semiHidden="0" w:uiPriority="73" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Shading Accent 1" w:semiHidden="0" w:uiPriority="60"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light List Accent 1" w:semiHidden="0" w:uiPriority="61"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Grid Accent 1" w:semiHidden="0" w:uiPriority="62"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 1 Accent 1" w:semiHidden="0" w:uiPriority="63"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 2 Accent 1" w:semiHidden="0" w:uiPriority="64"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 1 Accent 1" w:semiHidden="0" w:uiPriority="65"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Revision" w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="List Paragraph" w:semiHidden="0" w:uiPriority="34" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Quote" w:semiHidden="0" w:uiPriority="29" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Intense Quote" w:semiHidden="0" w:uiPriority="30" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Medium List 2 Accent 1" w:semiHidden="0" w:uiPriority="66"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 1 Accent 1" w:semiHidden="0" w:uiPriority="67"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 2 Accent 1" w:semiHidden="0" w:uiPriority="68"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 3 Accent 1" w:semiHidden="0" w:uiPriority="69"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Dark List Accent 1" w:semiHidden="0" w:uiPriority="70"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Shading Accent 1" w:semiHidden="0" w:uiPriority="71"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful List Accent 1" w:semiHidden="0" w:uiPriority="72"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Grid Accent 1" w:semiHidden="0" w:uiPriority="73"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Shading Accent 2" w:semiHidden="0" w:uiPriority="60"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light List Accent 2" w:semiHidden="0" w:uiPriority="61"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Grid Accent 2" w:semiHidden="0" w:uiPriority="62"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 1 Accent 2" w:semiHidden="0" w:uiPriority="63"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 2 Accent 2" w:semiHidden="0" w:uiPriority="64"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 1 Accent 2" w:semiHidden="0" w:uiPriority="65"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 2 Accent 2" w:semiHidden="0" w:uiPriority="66"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 1 Accent 2" w:semiHidden="0" w:uiPriority="67"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 2 Accent 2" w:semiHidden="0" w:uiPriority="68"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 3 Accent 2" w:semiHidden="0" w:uiPriority="69"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Dark List Accent 2" w:semiHidden="0" w:uiPriority="70"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Shading Accent 2" w:semiHidden="0" w:uiPriority="71"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful List Accent 2" w:semiHidden="0" w:uiPriority="72"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Grid Accent 2" w:semiHidden="0" w:uiPriority="73"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Shading Accent 3" w:semiHidden="0" w:uiPriority="60"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light List Accent 3" w:semiHidden="0" w:uiPriority="61"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Grid Accent 3" w:semiHidden="0" w:uiPriority="62"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 1 Accent 3" w:semiHidden="0" w:uiPriority="63"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 2 Accent 3" w:semiHidden="0" w:uiPriority="64"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 1 Accent 3" w:semiHidden="0" w:uiPriority="65"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 2 Accent 3" w:semiHidden="0" w:uiPriority="66"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 1 Accent 3" w:semiHidden="0" w:uiPriority="67"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 2 Accent 3" w:semiHidden="0" w:uiPriority="68"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 3 Accent 3" w:semiHidden="0" w:uiPriority="69"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Dark List Accent 3" w:semiHidden="0" w:uiPriority="70"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Shading Accent 3" w:semiHidden="0" w:uiPriority="71"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful List Accent 3" w:semiHidden="0" w:uiPriority="72"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Grid Accent 3" w:semiHidden="0" w:uiPriority="73"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Shading Accent 4" w:semiHidden="0" w:uiPriority="60"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light List Accent 4" w:semiHidden="0" w:uiPriority="61"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Grid Accent 4" w:semiHidden="0" w:uiPriority="62"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 1 Accent 4" w:semiHidden="0" w:uiPriority="63"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 2 Accent 4" w:semiHidden="0" w:uiPriority="64"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 1 Accent 4" w:semiHidden="0" w:uiPriority="65"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 2 Accent 4" w:semiHidden="0" w:uiPriority="66"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 1 Accent 4" w:semiHidden="0" w:uiPriority="67"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 2 Accent 4" w:semiHidden="0" w:uiPriority="68"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 3 Accent 4" w:semiHidden="0" w:uiPriority="69"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Dark List Accent 4" w:semiHidden="0" w:uiPriority="70"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Shading Accent 4" w:semiHidden="0" w:uiPriority="71"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful List Accent 4" w:semiHidden="0" w:uiPriority="72"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Grid Accent 4" w:semiHidden="0" w:uiPriority="73"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Shading Accent 5" w:semiHidden="0" w:uiPriority="60"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light List Accent 5" w:semiHidden="0" w:uiPriority="61"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Grid Accent 5" w:semiHidden="0" w:uiPriority="62"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 1 Accent 5" w:semiHidden="0" w:uiPriority="63"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 2 Accent 5" w:semiHidden="0" w:uiPriority="64"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 1 Accent 5" w:semiHidden="0" w:uiPriority="65"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 2 Accent 5" w:semiHidden="0" w:uiPriority="66"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 1 Accent 5" w:semiHidden="0" w:uiPriority="67"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 2 Accent 5" w:semiHidden="0" w:uiPriority="68"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 3 Accent 5" w:semiHidden="0" w:uiPriority="69"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Dark List Accent 5" w:semiHidden="0" w:uiPriority="70"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Shading Accent 5" w:semiHidden="0" w:uiPriority="71"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful List Accent 5" w:semiHidden="0" w:uiPriority="72"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Grid Accent 5" w:semiHidden="0" w:uiPriority="73"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Shading Accent 6" w:semiHidden="0" w:uiPriority="60"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light List Accent 6" w:semiHidden="0" w:uiPriority="61"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Light Grid Accent 6" w:semiHidden="0" w:uiPriority="62"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 1 Accent 6" w:semiHidden="0" w:uiPriority="63"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Shading 2 Accent 6" w:semiHidden="0" w:uiPriority="64"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 1 Accent 6" w:semiHidden="0" w:uiPriority="65"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium List 2 Accent 6" w:semiHidden="0" w:uiPriority="66"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 1 Accent 6" w:semiHidden="0" w:uiPriority="67"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 2 Accent 6" w:semiHidden="0" w:uiPriority="68"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Medium Grid 3 Accent 6" w:semiHidden="0" w:uiPriority="69"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Dark List Accent 6" w:semiHidden="0" w:uiPriority="70"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Shading Accent 6" w:semiHidden="0" w:uiPriority="71"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful List Accent 6" w:semiHidden="0" w:uiPriority="72"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Colorful Grid Accent 6" w:semiHidden="0" w:uiPriority="73"
                                    w:unhideWhenUsed="0"/>
                    <w:lsdException w:name="Subtle Emphasis" w:semiHidden="0" w:uiPriority="19" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Intense Emphasis" w:semiHidden="0" w:uiPriority="21" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Subtle Reference" w:semiHidden="0" w:uiPriority="31" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Intense Reference" w:semiHidden="0" w:uiPriority="32" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Book Title" w:semiHidden="0" w:uiPriority="33" w:unhideWhenUsed="0"
                                    w:qFormat="1"/>
                    <w:lsdException w:name="Bibliography" w:uiPriority="37"/>
                    <w:lsdException w:name="TOC Heading" w:uiPriority="39" w:qFormat="1"/>
                </w:latentStyles>
                <w:style w:type="paragraph" w:default="1" w:styleId="a">
                    <w:name w:val="Normal"/>
                    <w:qFormat/>
                    <w:pPr>
                        <w:widowControl w:val="0"/>
                        <w:jc w:val="both"/>
                    </w:pPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="1">
                    <w:name w:val="heading 1"/>
                    <w:basedOn w:val="a"/>
                    <w:next w:val="a"/>
                    <w:link w:val="1Char"/>
                    <w:uiPriority w:val="9"/>
                    <w:qFormat/>
                    <w:rsid w:val="000B3C56"/>
                    <w:pPr>
                        <w:keepNext/>
                        <w:keepLines/>
                        <w:spacing w:before="340" w:after="330" w:line="578" w:lineRule="auto"/>
                        <w:outlineLvl w:val="0"/>
                    </w:pPr>
                    <w:rPr>
                        <w:b/>
                        <w:bCs/>
                        <w:kern w:val="44"/>
                        <w:sz w:val="44"/>
                        <w:szCs w:val="44"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="2">
                    <w:name w:val="heading 2"/>
                    <w:basedOn w:val="a"/>
                    <w:next w:val="a"/>
                    <w:link w:val="2Char"/>
                    <w:uiPriority w:val="9"/>
                    <w:unhideWhenUsed/>
                    <w:qFormat/>
                    <w:rsid w:val="000B3C56"/>
                    <w:pPr>
                        <w:keepNext/>
                        <w:keepLines/>
                        <w:spacing w:before="260" w:after="260" w:line="416" w:lineRule="auto"/>
                        <w:outlineLvl w:val="1"/>
                    </w:pPr>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsiaTheme="majorEastAsia" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="3">
                    <w:name w:val="heading 3"/>
                    <w:basedOn w:val="a"/>
                    <w:next w:val="a"/>
                    <w:link w:val="3Char"/>
                    <w:uiPriority w:val="9"/>
                    <w:unhideWhenUsed/>
                    <w:qFormat/>
                    <w:rsid w:val="000B3C56"/>
                    <w:pPr>
                        <w:keepNext/>
                        <w:keepLines/>
                        <w:spacing w:before="260" w:after="260" w:line="416" w:lineRule="auto"/>
                        <w:outlineLvl w:val="2"/>
                    </w:pPr>
                    <w:rPr>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="4">
                    <w:name w:val="heading 4"/>
                    <w:basedOn w:val="a"/>
                    <w:next w:val="a"/>
                    <w:link w:val="4Char"/>
                    <w:uiPriority w:val="9"/>
                    <w:unhideWhenUsed/>
                    <w:qFormat/>
                    <w:rsid w:val="000B3C56"/>
                    <w:pPr>
                        <w:keepNext/>
                        <w:keepLines/>
                        <w:spacing w:before="280" w:after="290" w:line="376" w:lineRule="auto"/>
                        <w:outlineLvl w:val="3"/>
                    </w:pPr>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsiaTheme="majorEastAsia" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="28"/>
                        <w:szCs w:val="28"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:default="1" w:styleId="a0">
                    <w:name w:val="Default Paragraph Font"/>
                    <w:uiPriority w:val="1"/>
                    <w:semiHidden/>
                    <w:unhideWhenUsed/>
                </w:style>
                <w:style w:type="table" w:default="1" w:styleId="a1">
                    <w:name w:val="Normal Table"/>
                    <w:uiPriority w:val="99"/>
                    <w:semiHidden/>
                    <w:unhideWhenUsed/>
                    <w:tblPr>
                        <w:tblInd w:w="0" w:type="dxa"/>
                        <w:tblCellMar>
                            <w:top w:w="0" w:type="dxa"/>
                            <w:left w:w="108" w:type="dxa"/>
                            <w:bottom w:w="0" w:type="dxa"/>
                            <w:right w:w="108" w:type="dxa"/>
                        </w:tblCellMar>
                    </w:tblPr>
                </w:style>
                <w:style w:type="numbering" w:default="1" w:styleId="a2">
                    <w:name w:val="No List"/>
                    <w:uiPriority w:val="99"/>
                    <w:semiHidden/>
                    <w:unhideWhenUsed/>
                </w:style>
                <w:style w:type="paragraph" w:styleId="a3">
                    <w:name w:val="Title"/>
                    <w:basedOn w:val="a"/>
                    <w:next w:val="a"/>
                    <w:link w:val="Char"/>
                    <w:uiPriority w:val="10"/>
                    <w:qFormat/>
                    <w:rsid w:val="000B3C56"/>
                    <w:pPr>
                        <w:spacing w:before="240" w:after="60"/>
                        <w:jc w:val="center"/>
                        <w:outlineLvl w:val="0"/>
                    </w:pPr>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsia="宋体" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="Char">
                    <w:name w:val="标题 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="a3"/>
                    <w:uiPriority w:val="10"/>
                    <w:rsid w:val="000B3C56"/>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsia="宋体" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="a4">
                    <w:name w:val="Subtitle"/>
                    <w:basedOn w:val="a"/>
                    <w:next w:val="a"/>
                    <w:link w:val="Char0"/>
                    <w:uiPriority w:val="11"/>
                    <w:qFormat/>
                    <w:rsid w:val="000B3C56"/>
                    <w:pPr>
                        <w:spacing w:before="240" w:after="60" w:line="312" w:lineRule="auto"/>
                        <w:jc w:val="center"/>
                        <w:outlineLvl w:val="1"/>
                    </w:pPr>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsia="宋体" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:kern w:val="28"/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="Char0">
                    <w:name w:val="副标题 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="a4"/>
                    <w:uiPriority w:val="11"/>
                    <w:rsid w:val="000B3C56"/>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsia="宋体" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:kern w:val="28"/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="1Char">
                    <w:name w:val="标题 1 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="1"/>
                    <w:uiPriority w:val="9"/>
                    <w:rsid w:val="000B3C56"/>
                    <w:rPr>
                        <w:b/>
                        <w:bCs/>
                        <w:kern w:val="44"/>
                        <w:sz w:val="44"/>
                        <w:szCs w:val="44"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="2Char">
                    <w:name w:val="标题 2 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="2"/>
                    <w:uiPriority w:val="9"/>
                    <w:rsid w:val="000B3C56"/>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsiaTheme="majorEastAsia" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="3Char">
                    <w:name w:val="标题 3 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="3"/>
                    <w:uiPriority w:val="9"/>
                    <w:rsid w:val="000B3C56"/>
                    <w:rPr>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="32"/>
                        <w:szCs w:val="32"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="4Char">
                    <w:name w:val="标题 4 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="4"/>
                    <w:uiPriority w:val="9"/>
                    <w:rsid w:val="000B3C56"/>
                    <w:rPr>
                        <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsiaTheme="majorEastAsia" w:hAnsiTheme="majorHAnsi"
                                  w:cstheme="majorBidi"/>
                        <w:b/>
                        <w:bCs/>
                        <w:sz w:val="28"/>
                        <w:szCs w:val="28"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="a5">
                    <w:name w:val="header"/>
                    <w:basedOn w:val="a"/>
                    <w:link w:val="Char1"/>
                    <w:uiPriority w:val="99"/>
                    <w:unhideWhenUsed/>
                    <w:rsid w:val="00D420CE"/>
                    <w:pPr>
                        <w:pBdr>
                            <w:bottom w:val="single" w:sz="6" w:space="1" w:color="auto"/>
                        </w:pBdr>
                        <w:tabs>
                            <w:tab w:val="center" w:pos="4153"/>
                            <w:tab w:val="right" w:pos="8306"/>
                        </w:tabs>
                        <w:snapToGrid w:val="0"/>
                        <w:jc w:val="center"/>
                    </w:pPr>
                    <w:rPr>
                        <w:sz w:val="18"/>
                        <w:szCs w:val="18"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="Char1">
                    <w:name w:val="页眉 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="a5"/>
                    <w:uiPriority w:val="99"/>
                    <w:rsid w:val="00D420CE"/>
                    <w:rPr>
                        <w:sz w:val="18"/>
                        <w:szCs w:val="18"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="a6">
                    <w:name w:val="footer"/>
                    <w:basedOn w:val="a"/>
                    <w:link w:val="Char2"/>
                    <w:uiPriority w:val="99"/>
                    <w:unhideWhenUsed/>
                    <w:rsid w:val="00D420CE"/>
                    <w:pPr>
                        <w:tabs>
                            <w:tab w:val="center" w:pos="4153"/>
                            <w:tab w:val="right" w:pos="8306"/>
                        </w:tabs>
                        <w:snapToGrid w:val="0"/>
                        <w:jc w:val="left"/>
                    </w:pPr>
                    <w:rPr>
                        <w:sz w:val="18"/>
                        <w:szCs w:val="18"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="Char2">
                    <w:name w:val="页脚 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="a6"/>
                    <w:uiPriority w:val="99"/>
                    <w:rsid w:val="00D420CE"/>
                    <w:rPr>
                        <w:sz w:val="18"/>
                        <w:szCs w:val="18"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="paragraph" w:styleId="a7">
                    <w:name w:val="Balloon Text"/>
                    <w:basedOn w:val="a"/>
                    <w:link w:val="Char3"/>
                    <w:uiPriority w:val="99"/>
                    <w:semiHidden/>
                    <w:unhideWhenUsed/>
                    <w:rsid w:val="00D420CE"/>
                    <w:rPr>
                        <w:sz w:val="18"/>
                        <w:szCs w:val="18"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="character" w:customStyle="1" w:styleId="Char3">
                    <w:name w:val="批注框文本 Char"/>
                    <w:basedOn w:val="a0"/>
                    <w:link w:val="a7"/>
                    <w:uiPriority w:val="99"/>
                    <w:semiHidden/>
                    <w:rsid w:val="00D420CE"/>
                    <w:rPr>
                        <w:sz w:val="18"/>
                        <w:szCs w:val="18"/>
                    </w:rPr>
                </w:style>
                <w:style w:type="table" w:styleId="a8">
                    <w:name w:val="Table Grid"/>
                    <w:basedOn w:val="a1"/>
                    <w:uiPriority w:val="59"/>
                    <w:rsid w:val="00D420CE"/>
                    <w:tblPr>
                        <w:tblBorders>
                            <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                            <w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                            <w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                        </w:tblBorders>
                    </w:tblPr>
                </w:style>
            </w:styles>
        </pkg:xmlData>
    </pkg:part>
    <pkg:part pkg:name="/docProps/core.xml" pkg:contentType="application/vnd.openxmlformats-package.core-properties+xml"
              pkg:padding="256">
        <pkg:xmlData>
            <cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                               xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"
                               xmlns:dcmitype="http://purl.org/dc/dcmitype/"
                               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <dc:creator>Administrator</dc:creator>
                <cp:lastModifiedBy>Administrator</cp:lastModifiedBy>
                <cp:revision>2</cp:revision>
                <dcterms:created xsi:type="dcterms:W3CDTF">2018-09-06T02:45:00Z</dcterms:created>
                <dcterms:modified xsi:type="dcterms:W3CDTF">2018-09-06T02:45:00Z</dcterms:modified>
            </cp:coreProperties>
        </pkg:xmlData>
    </pkg:part>
    <pkg:part pkg:name="/word/fontTable.xml"
              pkg:contentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml">
        <pkg:xmlData>
            <w:fonts mc:Ignorable="w14" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                     xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                     xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                     xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
                <w:font w:name="Calibri">
                    <w:panose1 w:val="020F0502020204030204"/>
                    <w:charset w:val="00"/>
                    <w:family w:val="swiss"/>
                    <w:pitch w:val="variable"/>
                    <w:sig w:usb0="E00002FF" w:usb1="4000ACFF" w:usb2="00000001" w:usb3="00000000" w:csb0="0000019F"
                           w:csb1="00000000"/>
                </w:font>
                <w:font w:name="宋体">
                    <w:altName w:val="SimSun"/>
                    <w:panose1 w:val="02010600030101010101"/>
                    <w:charset w:val="86"/>
                    <w:family w:val="auto"/>
                    <w:pitch w:val="variable"/>
                    <w:sig w:usb0="00000003" w:usb1="288F0000" w:usb2="00000016" w:usb3="00000000" w:csb0="00040001"
                           w:csb1="00000000"/>
                </w:font>
                <w:font w:name="Times New Roman">
                    <w:panose1 w:val="02020603050405020304"/>
                    <w:charset w:val="00"/>
                    <w:family w:val="roman"/>
                    <w:pitch w:val="variable"/>
                    <w:sig w:usb0="E0002AFF" w:usb1="C0007841" w:usb2="00000009" w:usb3="00000000" w:csb0="000001FF"
                           w:csb1="00000000"/>
                </w:font>
                <w:font w:name="Cambria">
                    <w:panose1 w:val="02040503050406030204"/>
                    <w:charset w:val="00"/>
                    <w:family w:val="roman"/>
                    <w:pitch w:val="variable"/>
                    <w:sig w:usb0="E00002FF" w:usb1="400004FF" w:usb2="00000000" w:usb3="00000000" w:csb0="0000019F"
                           w:csb1="00000000"/>
                </w:font>
            </w:fonts>
        </pkg:xmlData>
    </pkg:part>
    <pkg:part pkg:name="/docProps/app.xml"
              pkg:contentType="application/vnd.openxmlformats-officedocument.extended-properties+xml" pkg:padding="256">
        <pkg:xmlData>
            <Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
                        xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
                <Template>Normal.dotm</Template>
                <TotalTime>0</TotalTime>
                <Pages>1</Pages>
                <Words>7</Words>
                <Characters>42</Characters>
                <Application>Microsoft Office Word</Application>
                <DocSecurity>0</DocSecurity>
                <Lines>1</Lines>
                <Paragraphs>1</Paragraphs>
                <ScaleCrop>false</ScaleCrop>
                <Company>微软中国</Company>
                <LinksUpToDate>false</LinksUpToDate>
                <CharactersWithSpaces>48</CharactersWithSpaces>
                <SharedDoc>false</SharedDoc>
                <HyperlinksChanged>false</HyperlinksChanged>
                <AppVersion>14.0000</AppVersion>
            </Properties>
        </pkg:xmlData>
    </pkg:part>
</pkg:package>