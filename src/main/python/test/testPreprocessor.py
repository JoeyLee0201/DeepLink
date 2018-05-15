# -*- coding: UTF-8 -*-

from preprocessor import preprocessor
import re

print preprocessor.processHTML(
    '''
    Examples shown in the javadoc for TESD_DSAFSA_DDS <code>ReplayingDecoder.addOption</code> seems to be wrong. In the document it shows <code>IntegerHeaderFrameDecoder, MyDecoder</code> taking multiple parameters where as in reality it can only accept one. I'm working with versions 4.0.0.CR3, 4.0.0.CR5.
    '''
)

print preprocessor.processDiffCode(
    '''
@@ -349 +349 @@ public class JavadocUtilsTest {
-            "HTML_COMMENT", JavadocUtils.getTokenName(20077));
+            "HTML_COMMENT", JavadocUtils.getTokenName(20078));
    '''
)

print preprocessor.preprocessToWord(
    '''
Examples shown in the javadoc for TESD_DSAFSA_DDS ReplayingDecoder.addOption seems to be wrong. In the document it shows IntegerHeaderFrameDecoder, MyDecoder taking multiple parameters where as in reality it can only accept one. I'm working with versions 4.0.0.CR3, 4.0.0.CR5.
     '''
)

if None:
    print 'none'
else:
    print 'other'
# camelCase1 = re.compile(r'^[A-Z]+[a-z]+.*[A-Z]+.*$') # 3
# camelCase2 = re.compile(r'^[a-z]+.*[A-Z]+.*$') # 12
# upperCase = re.compile(r'^[A-Z]+[0-9]*$') # 7
# upperExtCase = re.compile(r'^[A-Z]*(_+[A-Z]*)+[0-9]*$') # 6
#
# print re.match(upperExtCase, 'aOption'), '1'
# print re.match(upperExtCase, 'addOption'), '2'
# print re.match(upperExtCase, 'AddToDeal'), '3'
# print re.match(upperExtCase, 'dsadfsdf'), '4'
# print re.match(upperExtCase, '123213'), '5'
# print re.match(upperExtCase, 'ASFD_DDSF'), '6'
# print re.match(upperExtCase, '_DDSF_DDSF_DDSF'), 'l6'
# print re.match(upperExtCase, 'ASFD_ASFD_ASFD_'), '6r'
# print re.match(upperExtCase, '_ASFD_ASFD_ASFD_'), '6b'
# print re.match(upperExtCase, 'SDSADSA'), '7'
# print re.match(upperExtCase, 'English'), '8'
# print re.match(upperExtCase, 'EEDSnglish'), '9'
#
# print preprocessor.splitCode('AddToCode')
# print preprocessor.splitCode('addToCode')
# print preprocessor.splitCode('aToCode')
# print preprocessor.splitCode('aToCode090')
#
# print preprocessor.splitFinalExt('_ASFD_ASFD_ASFD_')
# print preprocessor.splitFinalExt('ASFD_DDSF')
# print preprocessor.splitFinalExt('ASFD_ASFD_ASFD_')
# print preprocessor.splitFinalExt('_DDSF_DDSF_DDSF')