import xml.etree.ElementTree as ET
from xml.dom import minidom


def create_musicxml(filename, instrument, tempo):
    # 创建根元素
    root = ET.Element('score-partwise')
    root.set('version', '3.1')

    # 作品信息
    work = ET.SubElement(root, 'work')
    work_title = ET.SubElement(work, 'work-title')
    work_title.text = filename

    # 添加part-list元素
    part_list = ET.SubElement(root, 'part-list')
    score_part = ET.SubElement(part_list, 'score-part')
    score_part.set('id', 'P1')
    part_name = ET.SubElement(score_part, 'part-name')
    part_name.text = instrument

    # 添加part元素
    part = ET.SubElement(root, 'part')
    part.set('id', 'P1')
    measure = ET.SubElement(part, 'measure')
    measure.set('number', '1')

    # 添加attributes元素
    attributes = ET.SubElement(measure, 'attributes')

    divisions = ET.SubElement(attributes, 'divisions')
    divisions.text = '1'

    key = ET.SubElement(attributes, 'key')
    fifths = ET.SubElement(key, 'fifths')
    fifths.text = '0'
    mode = ET.SubElement(key, 'mode')
    mode.text = 'major'
    # 拍号
    time = ET.SubElement(attributes, 'time')
    beats = ET.SubElement(time, 'beats')
    beats.text = '4'
    beat_type = ET.SubElement(time, 'beat-type')
    beat_type.text = '4'
    # 谱号
    clef = ET.SubElement(attributes, 'clef')
    sign = ET.SubElement(clef, 'sign')
    sign.text = 'G'
    line = ET.SubElement(clef, 'line')
    line.text = '2'

    tempo_elem = ET.SubElement(attributes, 'tempo')
    qpm = ET.SubElement(tempo_elem, 'per-minute')
    qpm.text = str(tempo)

    # 将 ElementTree 对象转换为 Document 对象
    doc = minidom.parseString(ET.tostring(root))
    # 添加 DTD 声明
    doctype = minidom.DocumentType('score-partwise PUBLIC')
    doc.insertBefore(doctype, doc.documentElement)
    # 获取格式化后的 XML 字符串
    pretty_xml = doc.toprettyxml(indent='  ', encoding='utf-8')
    # 将格式化后的 XML 写入文件
    with open(f'{filename}.xml', 'wb') as f:
        f.write(pretty_xml)
    with open(f'{filename}.xml', 'r+') as f:
        lines = f.readlines()
        lines[1] = '<!DOCTYPE score-partwise ' \
                   'PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">\n'
        f.seek(0)
        f.writelines(lines)
        f.truncate()
    f.close()
