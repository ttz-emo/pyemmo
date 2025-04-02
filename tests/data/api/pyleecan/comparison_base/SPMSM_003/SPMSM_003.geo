// This script was created with pyemmo (Version 1.3.2, git b7fa90)

DefineConstant[
 Flag_ExpertMode = {1,Name '01View/Expert Mode', Choices {0, 1}}
];

INPUT_MESH = "Input/03Mesh/";
DefineConstant[
	gmsf = {1, Name StrCat[INPUT_MESH, "00Mesh size factor"], Help "Global mesh size factor to modify the mesh size of all points. Is multiplied with the given mesh size."},

Flag_individualColoring = {0,Name StrCat[INPUT_MESH, "09Individual Mesh Coloring"], Choices {0, 1}}
];
Mesh.SurfaceEdges = 1;
Mesh.Light = 0;
Mesh.SurfaceFaces = 1;
Mesh.Algorithm = 6; // Frontal-Delaunay for 2D meshes
Mesh.MshFileVersion = 4.0; // Fix bug in mesh file creation for GetDP Version 3.6.0


// Points
point_pylc_dup = 1654; Point(1654) = {0.2, 0.0, 0, 0.009999999999999998*gmsf};
point_pylc_dup = 1655; Point(1655) = {0.116, 0.0, 0, 0.0009719626168224236*gmsf};
PointM41_dup = 1661; Point(1661) = {0.11520000000000001, 0, 0, 0.0008859813084112094*gmsf};
PointM31_dup = 1662; Point(1662) = {0.1144, 0, 0, 0.0007999999999999937*gmsf};
point_pylc_dup = 1652; Point(1652) = {0.0225, 0.0, 0, 0.01940492957746467*gmsf};
point_pylc_dup = 1653; Point(1653) = {0.1, 0.0, 0, 0.003577464788732372*gmsf};
PointM11_dup = 1657; Point(1657) = {0.1128, 0, 0, 0.0009633802816901378*gmsf};
PointM21_dup = 1659; Point(1659) = {0.1136, 0, 0, 0.0007999999999999952*gmsf};
point_pylc_dup = 1664; Point(1664) = {-0.2, 2.4492935982947065e-17, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 1665; Point(1665) = {-0.116, 1.4205902870109297e-17, 0.0, 0.0009719626168224236*gmsf};
PointM41_dup = 1667; Point(1667) = {-0.11520000000000001, 1.410793112617751e-17, 0.0, 0.0008859813084112094*gmsf};
PointM31_dup = 1668; Point(1668) = {-0.1144, 1.400995938224572e-17, 0.0, 0.0007999999999999937*gmsf};
point_pylc_dup = 1670; Point(1670) = {-0.0225, 2.7554552980815448e-18, 0.0, 0.01940492957746467*gmsf};
point_pylc_dup = 1671; Point(1671) = {-0.1, 1.2246467991473533e-17, 0.0, 0.003577464788732372*gmsf};
PointM11_dup = 1673; Point(1673) = {-0.1128, 1.3814015894382144e-17, 0.0, 0.0009633802816901378*gmsf};
PointM21_dup = 1675; Point(1675) = {-0.1136, 1.3911987638313932e-17, 0.0, 0.0007999999999999952*gmsf};
point_pylc = 1578; Point(1578) = {1.3777276490407724e-18, 0.0225, 0, 0.01940492957746467*gmsf};
point_pylc = 1579; Point(1579) = {0, 0, 0, 0.001*gmsf};
PointM22 = 1646; Point(1646) = {6.955993819156966e-18, 0.1136, 0, 0.0007999999999999952*gmsf};
PointM22_dup = 1693; Point(1693) = {-2.08679814574709e-17, -0.1136, 0.0, 0.0007999999999999952*gmsf};
point_pylc_dup = 1731; Point(1731) = {0.09876883405950741, 0.015643446504063286, 0, 0.003577464788732372*gmsf};
point_pylc_dup = 1732; Point(1732) = {0.1106210941466483, 0.01752066008455088, 0, 0.0011267605633802748*gmsf};
point_pylc_dup = 1735; Point(1735) = {-0.1106210941466483, 0.017520660084550894, 0, 0.0011267605633802748*gmsf};
point_pylc_dup = 1737; Point(1737) = {-0.09876883405950741, 0.0156434465040633, 0, 0.003577464788732372*gmsf};
point_pylc = 1595; Point(1595) = {0.17320508075688776, 0.09999999999999999, 0, 0.009999999999999998*gmsf};
point_pylc_dup = 1697; Point(1697) = {0.10000000000000003, 0.17320508075688773, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 1700; Point(1700) = {4.163336342344337e-17, 0.20000000000000004, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 1703; Point(1703) = {-0.09999999999999998, 0.17320508075688776, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 1706; Point(1706) = {-0.1732050807568877, 0.10000000000000005, 0.0, 0.009999999999999998*gmsf};
PointM32 = 1651; Point(1651) = {0.09907330619293979, 0.057199999999999994, 0, 0.0007999999999999937*gmsf};
PointM32_dup = 1678; Point(1678) = {0.05720000000000002, 0.09907330619293978, 0.0, 0.0007999999999999937*gmsf};
PointM32_dup = 1681; Point(1681) = {2.7755575615628914e-17, 0.1144, 0.0, 0.0007999999999999937*gmsf};
PointM32_dup = 1684; Point(1684) = {-0.05719999999999999, 0.09907330619293979, 0.0, 0.0007999999999999923*gmsf};
PointM32_dup = 1687; Point(1687) = {-0.09907330619293976, 0.05720000000000003, 0.0, 0.0007999999999999937*gmsf};
PointM42_dup = 2136; Point(2136) = {0.09976612651596735, 0.0576, 0, 0.0008859813084112094*gmsf};
PointM42_dup = 2146; Point(2146) = {0.057600000000000026, 0.09976612651596733, 0.0, 0.0008859813084112094*gmsf};
PointM42_dup = 2156; Point(2156) = {2.7755575615628914e-17, 0.11520000000000001, 0.0, 0.0008859813084112094*gmsf};
PointM42_dup = 2166; Point(2166) = {-0.05759999999999999, 0.09976612651596735, 0.0, 0.0008859813084112094*gmsf};
PointM42_dup = 2176; Point(2176) = {-0.09976612651596732, 0.05760000000000003, 0.0, 0.0008859813084112094*gmsf};
point_pylc_dup = 2016; Point(2016) = {0.11371145625611974, 0.022928251483978635, 0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2018; Point(2018) = {0.11763254095460662, 0.02371888084549514, 0, 0.0014018691588785004*gmsf};
point_pylc_dup = 2019; Point(2019) = {0.11373220920115029, 0.03827511711576839, 0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2020; Point(2020) = {0.10994113556111196, 0.03699927987857611, 0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2023; Point(2023) = {0.1004589468389949, 0.057999999999999996, 0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2036; Point(2036) = {0.08701288407713331, 0.07671217637754361, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2038; Point(2038) = {0.09001332835565515, 0.07935742383883823, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 2039; Point(2039) = {0.07935742383883825, 0.09001332835565515, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2040; Point(2040) = {0.07671217637754364, 0.08701288407713331, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2043; Point(2043) = {0.058000000000000024, 0.10045894683899488, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2056; Point(2056) = {0.03699927987857613, 0.10994113556111194, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2058; Point(2058) = {0.038275117115768406, 0.11373220920115028, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2059; Point(2059) = {0.023718880845495158, 0.11763254095460662, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2060; Point(2060) = {0.02292825148397866, 0.11371145625611975, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2063; Point(2063) = {2.7755575615628914e-17, 0.11600000000000002, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2076; Point(2076) = {-0.022928251483978628, 0.11371145625611974, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2078; Point(2078) = {-0.023718880845495133, 0.11763254095460662, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 2079; Point(2079) = {-0.038275117115768385, 0.11373220920115029, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2080; Point(2080) = {-0.036999279878576104, 0.10994113556111196, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2083; Point(2083) = {-0.05799999999999999, 0.1004589468389949, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2096; Point(2096) = {-0.0767121763775436, 0.08701288407713333, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2098; Point(2098) = {-0.0793574238388382, 0.09001332835565515, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2099; Point(2099) = {-0.09001332835565512, 0.07935742383883826, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2100; Point(2100) = {-0.08701288407713328, 0.07671217637754364, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2103; Point(2103) = {-0.10045894683899487, 0.05800000000000004, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2116; Point(2116) = {-0.10994113556111193, 0.03699927987857615, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2118; Point(2118) = {-0.11373220920115026, 0.03827511711576844, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2119; Point(2119) = {-0.11763254095460662, 0.023718880845495185, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2120; Point(2120) = {-0.11371145625611975, 0.022928251483978687, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 1755; Point(1755) = {0.11852260087141653, 0.018772135804827707, 0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1757; Point(1757) = {0.14321480938629497, 0.02268299743083347, 0, 0.004088785046728965*gmsf};
point_pylc_dup = 1760; Point(1760) = {0.13536916184209424, 0.05196335268406853, 0, 0.004088785046728965*gmsf};
point_pylc_dup = 1762; Point(1762) = {0.11202965117966421, 0.04300415394543603, 0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1785; Point(1785) = {0.09325751537483652, 0.07551844692598049, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 1787; Point(1787) = {0.1126861644112608, 0.09125145670222641, 0.0, 0.004088785046728967*gmsf};
point_pylc_dup = 1790; Point(1790) = {0.09125145670222644, 0.11268616441126075, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 1792; Point(1792) = {0.0755184469259805, 0.09325751537483651, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 1815; Point(1815) = {0.043004153945436045, 0.11202965117966421, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1817; Point(1817) = {0.051963352684068556, 0.13536916184209424, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 1820; Point(1820) = {0.022682997430833497, 0.14321480938629494, 0.0, 0.004088785046728962*gmsf};
point_pylc_dup = 1822; Point(1822) = {0.01877213580482772, 0.11852260087141653, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1845; Point(1845) = {-0.0187721358048277, 0.11852260087141653, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1847; Point(1847) = {-0.02268299743083346, 0.14321480938629497, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 1850; Point(1850) = {-0.05196335268406852, 0.13536916184209424, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 1852; Point(1852) = {-0.043004153945436024, 0.11202965117966421, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1875; Point(1875) = {-0.07551844692598048, 0.09325751537483652, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1877; Point(1877) = {-0.0912514567022264, 0.1126861644112608, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 1880; Point(1880) = {-0.11268616441126074, 0.09125145670222644, 0.0, 0.004088785046728962*gmsf};
point_pylc_dup = 1882; Point(1882) = {-0.09325751537483648, 0.0755184469259805, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1905; Point(1905) = {-0.11202965117966421, 0.04300415394543608, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 1907; Point(1907) = {-0.13536916184209422, 0.051963352684068584, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 1910; Point(1910) = {-0.14321480938629494, 0.022682997430833532, 0.0, 0.004088785046728962*gmsf};
point_pylc_dup = 1912; Point(1912) = {-0.11852260087141651, 0.01877213580482775, 0.0, 0.0014018691588784976*gmsf};

// Lines and Curves
Line_dup = 967;Line(Line_dup) = {1654, 1655};
lowerLine4_dup = 970;Line(lowerLine4_dup) = {1655, 1661};
lowerLine3_dup = 971;Line(lowerLine3_dup) = {1662, 1661};
Line_dup = 966;Line(Line_dup) = {1652, 1653};
lowerLine1_dup = 968;Line(lowerLine1_dup) = {1653, 1657};
lowerLine2_dup = 969;Line(lowerLine2_dup) = {1657, 1659};
Line_dup = 972;Line(Line_dup) = {1664, 1665};
lowerLine4_dup = 973;Line(lowerLine4_dup) = {1665, 1667};
lowerLine3_dup = 974;Line(lowerLine3_dup) = {1668, 1667};
Line_dup = 975;Line(Line_dup) = {1670, 1671};
lowerLine1_dup = 976;Line(lowerLine1_dup) = {1671, 1673};
lowerLine2_dup = 977;Line(lowerLine2_dup) = {1673, 1675};
InnerLimit = 913;Circle(InnerLimit) = {1670, 1579, 1578};
InnerLimit = 915;Circle(InnerLimit) = {1578, 1579, 1652};
MB_CurveRotor_1 = 953;Circle(MB_CurveRotor_1) = {1659, 1579, 1646};
MB_CurveRotor_2 = 955;Circle(MB_CurveRotor_2) = {1646, 1579, 1675};
MB_CurveRotor_1_dup = 989;Circle(MB_CurveRotor_1_dup) = {1675, 1579, 1693};
MB_CurveRotor_2_dup = 991;Circle(MB_CurveRotor_2_dup) = {1693, 1579, 1659};
rotorBand1_dup = 1177;Circle(rotorBand1_dup) = {1657, 1579, 1673};
Line_dup = 1014;Line(Line_dup) = {1731, 1732};
CircleArc_dup = 1016;Circle(CircleArc_dup) = {1732, 1579, 1735};
Line_dup = 1017;Line(Line_dup) = {1735, 1737};
CircleArc_dup = 1019;Circle(CircleArc_dup) = {1737, 1579, 1731};
CircleArc_dup = 1165;Circle(CircleArc_dup) = {1653, 1579, 1731};
CircleArc_dup = 1167;Circle(CircleArc_dup) = {1737, 1579, 1671};
OuterLimit = 924;Circle(OuterLimit) = {1595, 1579, 1654};
OuterLimit_dup = 993;Circle(OuterLimit_dup) = {1697, 1579, 1595};
OuterLimit_dup = 995;Circle(OuterLimit_dup) = {1700, 1579, 1697};
OuterLimit_dup = 997;Circle(OuterLimit_dup) = {1703, 1579, 1700};
OuterLimit_dup = 999;Circle(OuterLimit_dup) = {1706, 1579, 1703};
OuterLimit_dup = 1001;Circle(OuterLimit_dup) = {1664, 1579, 1706};
MB_CurveStator = 963;Circle(MB_CurveStator) = {1662, 1579, 1651};
MB_CurveStator_dup = 979;Circle(MB_CurveStator_dup) = {1651, 1579, 1678};
MB_CurveStator_dup = 981;Circle(MB_CurveStator_dup) = {1678, 1579, 1681};
MB_CurveStator_dup = 983;Circle(MB_CurveStator_dup) = {1681, 1579, 1684};
MB_CurveStator_dup = 985;Circle(MB_CurveStator_dup) = {1684, 1579, 1687};
MB_CurveStator_dup = 987;Circle(MB_CurveStator_dup) = {1687, 1579, 1668};
statorCircle4_dup = 1257;Circle(statorCircle4_dup) = {1661, 1579, 2136};
upperLine3_dup = 1261;Line(upperLine3_dup) = {1651, 2136};
statorCircle4_dup = 1263;Circle(statorCircle4_dup) = {2136, 1579, 2146};
upperLine3_dup = 1267;Line(upperLine3_dup) = {1678, 2146};
statorCircle4_dup = 1269;Circle(statorCircle4_dup) = {2146, 1579, 2156};
upperLine3_dup = 1273;Line(upperLine3_dup) = {1681, 2156};
statorCircle4_dup = 1275;Circle(statorCircle4_dup) = {2156, 1579, 2166};
upperLine3_dup = 1279;Line(upperLine3_dup) = {1684, 2166};
statorCircle4_dup = 1281;Circle(statorCircle4_dup) = {2166, 1579, 2176};
upperLine3_dup = 1285;Line(upperLine3_dup) = {1687, 2176};
statorCircle4_dup = 1287;Circle(statorCircle4_dup) = {2176, 1579, 1667};
CircleArc_dup = 1185;Circle(CircleArc_dup) = {1655, 1579, 2016};
Line_dup = 1186;Line(Line_dup) = {2016, 2018};
Line_dup = 1187;Line(Line_dup) = {2019, 2020};
CircleArc_dup = 1189;Circle(CircleArc_dup) = {2020, 1579, 2023};
interface_line_slot_opening___slot_dup = 1191;Circle(interface_line_slot_opening___slot_dup) = {2018, 1579, 2019};
upperLine4_dup = 1195;Line(upperLine4_dup) = {2023, 2136};
CircleArc_dup = 1197;Circle(CircleArc_dup) = {2023, 1579, 2036};
Line_dup = 1198;Line(Line_dup) = {2036, 2038};
Line_dup = 1199;Line(Line_dup) = {2039, 2040};
CircleArc_dup = 1201;Circle(CircleArc_dup) = {2040, 1579, 2043};
interface_line_slot_opening___slot_dup = 1203;Circle(interface_line_slot_opening___slot_dup) = {2038, 1579, 2039};
upperLine4_dup = 1207;Line(upperLine4_dup) = {2043, 2146};
CircleArc_dup = 1209;Circle(CircleArc_dup) = {2043, 1579, 2056};
Line_dup = 1210;Line(Line_dup) = {2056, 2058};
Line_dup = 1211;Line(Line_dup) = {2059, 2060};
CircleArc_dup = 1213;Circle(CircleArc_dup) = {2060, 1579, 2063};
interface_line_slot_opening___slot_dup = 1215;Circle(interface_line_slot_opening___slot_dup) = {2058, 1579, 2059};
upperLine4_dup = 1219;Line(upperLine4_dup) = {2063, 2156};
CircleArc_dup = 1221;Circle(CircleArc_dup) = {2063, 1579, 2076};
Line_dup = 1222;Line(Line_dup) = {2076, 2078};
Line_dup = 1223;Line(Line_dup) = {2079, 2080};
CircleArc_dup = 1225;Circle(CircleArc_dup) = {2080, 1579, 2083};
interface_line_slot_opening___slot_dup = 1227;Circle(interface_line_slot_opening___slot_dup) = {2078, 1579, 2079};
upperLine4_dup = 1231;Line(upperLine4_dup) = {2083, 2166};
CircleArc_dup = 1233;Circle(CircleArc_dup) = {2083, 1579, 2096};
Line_dup = 1234;Line(Line_dup) = {2096, 2098};
Line_dup = 1235;Line(Line_dup) = {2099, 2100};
CircleArc_dup = 1237;Circle(CircleArc_dup) = {2100, 1579, 2103};
interface_line_slot_opening___slot_dup = 1239;Circle(interface_line_slot_opening___slot_dup) = {2098, 1579, 2099};
upperLine4_dup = 1243;Line(upperLine4_dup) = {2103, 2176};
CircleArc_dup = 1245;Circle(CircleArc_dup) = {2103, 1579, 2116};
Line_dup = 1246;Line(Line_dup) = {2116, 2118};
Line_dup = 1247;Line(Line_dup) = {2119, 2120};
CircleArc_dup = 1249;Circle(CircleArc_dup) = {2120, 1579, 1665};
interface_line_slot_opening___slot_dup = 1251;Circle(interface_line_slot_opening___slot_dup) = {2118, 1579, 2119};
Line_dup = 1020;Line(Line_dup) = {2023, 1595};
CircleArc_dup = 1028;Circle(CircleArc_dup) = {2018, 1579, 1755};
Line_dup = 1029;Line(Line_dup) = {1755, 1757};
CircleArc_dup = 1031;Circle(CircleArc_dup) = {1757, 1579, 1760};
Line_dup = 1032;Line(Line_dup) = {1760, 1762};
CircleArc_dup = 1034;Circle(CircleArc_dup) = {1762, 1579, 2019};
Line_dup = 1038;Line(Line_dup) = {2043, 1697};
CircleArc_dup = 1046;Circle(CircleArc_dup) = {2038, 1579, 1785};
Line_dup = 1047;Line(Line_dup) = {1785, 1787};
CircleArc_dup = 1049;Circle(CircleArc_dup) = {1787, 1579, 1790};
Line_dup = 1050;Line(Line_dup) = {1790, 1792};
CircleArc_dup = 1052;Circle(CircleArc_dup) = {1792, 1579, 2039};
Line_dup = 1056;Line(Line_dup) = {2063, 1700};
CircleArc_dup = 1064;Circle(CircleArc_dup) = {2058, 1579, 1815};
Line_dup = 1065;Line(Line_dup) = {1815, 1817};
CircleArc_dup = 1067;Circle(CircleArc_dup) = {1817, 1579, 1820};
Line_dup = 1068;Line(Line_dup) = {1820, 1822};
CircleArc_dup = 1070;Circle(CircleArc_dup) = {1822, 1579, 2059};
Line_dup = 1074;Line(Line_dup) = {2083, 1703};
CircleArc_dup = 1082;Circle(CircleArc_dup) = {2078, 1579, 1845};
Line_dup = 1083;Line(Line_dup) = {1845, 1847};
CircleArc_dup = 1085;Circle(CircleArc_dup) = {1847, 1579, 1850};
Line_dup = 1086;Line(Line_dup) = {1850, 1852};
CircleArc_dup = 1088;Circle(CircleArc_dup) = {1852, 1579, 2079};
Line_dup = 1092;Line(Line_dup) = {2103, 1706};
CircleArc_dup = 1100;Circle(CircleArc_dup) = {2098, 1579, 1875};
Line_dup = 1101;Line(Line_dup) = {1875, 1877};
CircleArc_dup = 1103;Circle(CircleArc_dup) = {1877, 1579, 1880};
Line_dup = 1104;Line(Line_dup) = {1880, 1882};
CircleArc_dup = 1106;Circle(CircleArc_dup) = {1882, 1579, 2099};
CircleArc_dup = 1118;Circle(CircleArc_dup) = {2118, 1579, 1905};
Line_dup = 1119;Line(Line_dup) = {1905, 1907};
CircleArc_dup = 1121;Circle(CircleArc_dup) = {1907, 1579, 1910};
Line_dup = 1122;Line(Line_dup) = {1910, 1912};
CircleArc_dup = 1124;Circle(CircleArc_dup) = {1912, 1579, 2119};
CircleArc_dup = 1129;Circle(CircleArc_dup) = {1755, 1579, 1762};
CircleArc_dup = 1135;Circle(CircleArc_dup) = {1785, 1579, 1792};
CircleArc_dup = 1141;Circle(CircleArc_dup) = {1815, 1579, 1822};
CircleArc_dup = 1147;Circle(CircleArc_dup) = {1845, 1579, 1852};
CircleArc_dup = 1153;Circle(CircleArc_dup) = {1875, 1579, 1882};
CircleArc_dup = 1159;Circle(CircleArc_dup) = {1905, 1579, 1912};

// Surfaces

Curve Loop(121) = {1177,977,-955,-953,-969};
Surf_rotorAirGap2_dup = {121};
Plane Surface(Surf_rotorAirGap2_dup) = {121};

Curve Loop(107) = {1014,1016,1017,1019};
Surf_Magnet_dup = {107};
Plane Surface(Surf_Magnet_dup) = {107};

Curve Loop(120) = {1165,1014,1016,1017,1167,976,-1177,-968};
Surf_rotorAirGap1_dup = {120};
Plane Surface(Surf_rotorAirGap1_dup) = {120};

Curve Loop(106) = {966,1165,-1019,1167,-975,913,915};
Surf_Rotorblech_dup = {106};
Plane Surface(Surf_Rotorblech_dup) = {106};

Curve Loop(128) = {1257,-1261,-963,971};
Surf_statorAirGap2_dup = {128};
Plane Surface(Surf_statorAirGap2_dup) = {128};

Curve Loop(129) = {1263,-1267,-979,1261};
Surf_statorAirGap2_dup = {129};
Plane Surface(Surf_statorAirGap2_dup) = {129};

Curve Loop(130) = {1269,-1273,-981,1267};
Surf_statorAirGap2_dup = {130};
Plane Surface(Surf_statorAirGap2_dup) = {130};

Curve Loop(131) = {1275,-1279,-983,1273};
Surf_statorAirGap2_dup = {131};
Plane Surface(Surf_statorAirGap2_dup) = {131};

Curve Loop(132) = {1281,-1285,-985,1279};
Surf_statorAirGap2_dup = {132};
Plane Surface(Surf_statorAirGap2_dup) = {132};

Curve Loop(133) = {1287,-974,-987,1285};
Surf_statorAirGap2_dup = {133};
Plane Surface(Surf_statorAirGap2_dup) = {133};

Curve Loop(122) = {1185,1186,1191,1187,1189,1195,-1257,-970};
Surf_statorAirGap1_dup = {122};
Plane Surface(Surf_statorAirGap1_dup) = {122};

Curve Loop(123) = {1197,1198,1203,1199,1201,1207,-1263,-1195};
Surf_statorAirGap1_dup = {123};
Plane Surface(Surf_statorAirGap1_dup) = {123};

Curve Loop(124) = {1209,1210,1215,1211,1213,1219,-1269,-1207};
Surf_statorAirGap1_dup = {124};
Plane Surface(Surf_statorAirGap1_dup) = {124};

Curve Loop(125) = {1221,1222,1227,1223,1225,1231,-1275,-1219};
Surf_statorAirGap1_dup = {125};
Plane Surface(Surf_statorAirGap1_dup) = {125};

Curve Loop(126) = {1233,1234,1239,1235,1237,1243,-1281,-1231};
Surf_statorAirGap1_dup = {126};
Plane Surface(Surf_statorAirGap1_dup) = {126};

Curve Loop(127) = {1245,1246,1251,1247,1249,973,-1287,-1243};
Surf_statorAirGap1_dup = {127};
Plane Surface(Surf_statorAirGap1_dup) = {127};

Curve Loop(108) = {1020,924,967,1185,1186,1028,1029,1031,1032,1034,1187,1189};
Surf_Statorblech_dup = {108};
Plane Surface(Surf_Statorblech_dup) = {108};

Curve Loop(109) = {1038,993,-1020,1197,1198,1046,1047,1049,1050,1052,1199,1201};
Surf_Statorblech_dup = {109};
Plane Surface(Surf_Statorblech_dup) = {109};

Curve Loop(110) = {1056,995,-1038,1209,1210,1064,1065,1067,1068,1070,1211,1213};
Surf_Statorblech_dup = {110};
Plane Surface(Surf_Statorblech_dup) = {110};

Curve Loop(111) = {1074,997,-1056,1221,1222,1082,1083,1085,1086,1088,1223,1225};
Surf_Statorblech_dup = {111};
Plane Surface(Surf_Statorblech_dup) = {111};

Curve Loop(112) = {1092,999,-1074,1233,1234,1100,1101,1103,1104,1106,1235,1237};
Surf_Statorblech_dup = {112};
Plane Surface(Surf_Statorblech_dup) = {112};

Curve Loop(113) = {972,-1249,-1247,-1124,-1122,-1121,-1119,-1118,-1246,-1245,1092,-1001};
Surf_Statorblech_dup = {113};
Plane Surface(Surf_Statorblech_dup) = {113};

Curve Loop(114) = {1129,-1032,-1031,-1029};
Surf_Stator_Nut_dup = {114};
Plane Surface(Surf_Stator_Nut_dup) = {114};

Curve Loop(115) = {1135,-1050,-1049,-1047};
Surf_Stator_Nut_dup = {115};
Plane Surface(Surf_Stator_Nut_dup) = {115};

Curve Loop(116) = {1141,-1068,-1067,-1065};
Surf_Stator_Nut_dup = {116};
Plane Surface(Surf_Stator_Nut_dup) = {116};

Curve Loop(117) = {1147,-1086,-1085,-1083};
Surf_Stator_Nut_dup = {117};
Plane Surface(Surf_Stator_Nut_dup) = {117};

Curve Loop(118) = {1153,-1104,-1103,-1101};
Surf_Stator_Nut_dup = {118};
Plane Surface(Surf_Stator_Nut_dup) = {118};

Curve Loop(119) = {1159,-1122,-1121,-1119};
Surf_Stator_Nut_dup = {119};
Plane Surface(Surf_Stator_Nut_dup) = {119};

// Color code
If (!Flag_individualColoring)
Color SkyBlue {Surface {121}; }
Color Red {Surface {107}; }
Color SkyBlue {Surface {120}; }
Color SteelBlue {Surface {106}; }
Color SkyBlue {Surface {128}; }
Color SkyBlue {Surface {129}; }
Color SkyBlue {Surface {130}; }
Color SkyBlue {Surface {131}; }
Color SkyBlue {Surface {132}; }
Color SkyBlue {Surface {133}; }
Color SkyBlue {Surface {122}; }
Color SkyBlue {Surface {123}; }
Color SkyBlue {Surface {124}; }
Color SkyBlue {Surface {125}; }
Color SkyBlue {Surface {126}; }
Color SkyBlue {Surface {127}; }
Color SteelBlue4 {Surface {108}; }
Color SteelBlue4 {Surface {109}; }
Color SteelBlue4 {Surface {110}; }
Color SteelBlue4 {Surface {111}; }
Color SteelBlue4 {Surface {112}; }
Color SteelBlue4 {Surface {113}; }
Color Magenta {Surface {114}; }
Color Magenta {Surface {115}; }
Color Cyan {Surface {116}; }
Color Cyan {Surface {117}; }
Color Yellow4 {Surface {118}; }
Color Yellow4 {Surface {119}; }
EndIf

// Physical Elements
// primaryLineS
Physical Curve("primaryLineS", 3) = {967,970,971};
// primaryLineR
Physical Curve("primaryLineR", 2) = {966,968,969};
// slaveLineS
Physical Curve("slaveLineS", 5) = {972,973,974};
// slaveLineR
Physical Curve("slaveLineR", 4) = {975,976,977};
// innerLimit
Physical Curve("innerLimit", 10) = {913,915};
// Rotor_Bnd_MB_1
Physical Curve("Rotor_Bnd_MB_1", 7) = {953,955};
// Rotor_Bnd_MB_2
Physical Curve("Rotor_Bnd_MB_2", 8) = {989,991};
// LuR2
Physical Surface("LuR2", 21) = {121};
// Mag0_0
Physical Surface("Mag0_0", 12) = {107};
// LuR1
Physical Surface("LuR1", 20) = {120};
// Pol
Physical Surface("Pol", 11) = {106};
// outerLimit
Physical Curve("outerLimit", 9) = {924,993,995,997,999,1001};
// mbStator
Physical Curve("mbStator", 6) = {963,979,981,983,985,987};
// StLu2
Physical Surface("StLu2", 23) = {128,129,130,131,132,133};
// StLu1
Physical Surface("StLu1", 22) = {122,123,124,125,126,127};
// StNut
Physical Surface("StNut", 13) = {108,109,110,111,112,113};
// StCu0_0_Up
Physical Surface("StCu0_0_Up", 14) = {114};
// StCu0_1_Up
Physical Surface("StCu0_1_Up", 15) = {115};
// StCu0_2_Wn
Physical Surface("StCu0_2_Wn", 16) = {116};
// StCu0_3_Wn
Physical Surface("StCu0_3_Wn", 17) = {117};
// StCu0_4_Vp
Physical Surface("StCu0_4_Vp", 18) = {118};
// StCu0_5_Vp
Physical Surface("StCu0_5_Vp", 19) = {119};

DefineConstant[
	mm = 1e-3,
	Flag_SpecifyMeshSize = {0, Name StrCat[INPUT_MESH, "04User defined surface mesh sizes"],Choices {0, 1}}
];
If(Flag_SpecifyMeshSize)
	DefineConstant[
		Mag_msf = {2.082, Name StrCat[INPUT_MESH, "05Mesh Size/Magnet [mm]"],Min 0.2082, Max 20.82, Step 0.1,Visible Flag_SpecifyMeshSize},
		Pol_msf = {9.191, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorblech [mm]"],Min 0.9191, Max 91.91000000000001, Step 0.1,Visible Flag_SpecifyMeshSize},
		LuR_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorluftspalt [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		LuR1_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorluftspalt 1 [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		LuR2_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorluftspalt 2 [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		StCu_msf = {2.396, Name StrCat[INPUT_MESH, "05Mesh Size/Stator-Nut [mm]"],Min 0.23959999999999998, Max 23.96, Step 0.1,Visible Flag_SpecifyMeshSize},
		StNut_msf = {2.975, Name StrCat[INPUT_MESH, "05Mesh Size/Statorblech [mm]"],Min 0.2975, Max 29.75, Step 0.1,Visible Flag_SpecifyMeshSize},
		StLu_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Statorluftspalt [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		StLu1_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Statorluftspalt 1 [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		StLu2_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Statorluftspalt 2 [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize}
	];
	MeshSize { PointsOf {Surface{ 107 };} } = Mag_msf*mm;
	MeshSize { PointsOf {Surface{ 106 };} } = Pol_msf*mm;
	MeshSize { PointsOf {Surface{ 120,121 };} } = LuR_msf*mm;
	MeshSize { PointsOf {Surface{ 120 };} } = LuR1_msf*mm;
	MeshSize { PointsOf {Surface{ 121 };} } = LuR2_msf*mm;
	MeshSize { PointsOf {Surface{ 114,115,116,117,118,119 };} } = StCu_msf*mm;
	MeshSize { PointsOf {Surface{ 108,109,110,111,112,113 };} } = StNut_msf*mm;
	MeshSize { PointsOf {Surface{ 122,123,124,125,126,127,128,129,130,131,132,133 };} } = StLu_msf*mm;
	MeshSize { PointsOf {Surface{ 122,123,124,125,126,127 };} } = StLu1_msf*mm;
	MeshSize { PointsOf {Surface{ 128,129,130,131,132,133 };} } = StLu2_msf*mm;
EndIf

// Mesh operations

// Do not switch mesh algorithm on failure, because this led to mesh errors in the past.
Mesh.AlgorithmSwitchOnFailure = 0;DefineConstant[Flag_CompoundMesh = {0, Name StrCat[INPUT_MESH, "Compound Mesh"], Choices {0,1}, Help "Use Compound Mesh to ignore lines between segments while meshing.",Visible Flag_ExpertMode}];
If (Flag_CompoundMesh)
Compound Surface{108,109,110,111,112,113}; // stator domainLam
Compound Surface{128,129,130,131,132,133}; // stator airGap
EndIf // (Flag_CompoundMesh)

// Add Periodic Mesh to model symmetry boundary-lines
primaryLines = {966,968,969,967,970,971};
secondaryLines = {975,976,977,972,973,974};
Periodic Curve{secondaryLines[]} = {primaryLines[]} Rotate {{0,0,1}, {0,0,0}, 2*Pi/2};

// Add mesh size setting for Movingband lines
DefineConstant[
	NbrMbSegments = {890.0, Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],Max 1440, Min 180, Step 10, Help "Set the number of mesh segments on the interface between rotor/statorairgap and movingband. Value represents number of segments on whole circle.", Visible Flag_ExpertMode},
	r_MB_R = 0.1136
];
MB_LinesR = {953,955,989,991};
MeshSize{ PointsOf{Line{MB_LinesR[]};}} = 2*Pi*r_MB_R/NbrMbSegments;

MB_LinesS = {963,979,981,983,985,987};
MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*0.1144/NbrMbSegments;

Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)

// Create boundary lines for moving rotor contour plot
rotorBndLines[] = Boundary{ Physical Surface{ 12 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 11 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 21 }; };
statorBndLines[] = Boundary{ Physical Surface{ 3,5,6,9,13,14,15,16,17,18,19,22,23 }; };
Physical Line("DomainPlotMovingGeo",1) = {rotorBndLines[], statorBndLines[]};
