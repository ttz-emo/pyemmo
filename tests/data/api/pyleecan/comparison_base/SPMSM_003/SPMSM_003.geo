// This script was created with pyemmo (Version 1.3.1b1, git 6eeae4)

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


// Points
point_pylc_dup = 1653; Point(1653) = {0.2, 0.0, 0, 0.009999999999999998*gmsf};
point_pylc_dup = 1654; Point(1654) = {0.116, 0.0, 0, 0.0009719626168224236*gmsf};
PointM41_dup = 1660; Point(1660) = {0.11520000000000001, 0, 0, 0.0008859813084112094*gmsf};
PointM31_dup = 1661; Point(1661) = {0.1144, 0, 0, 0.0007999999999999937*gmsf};
point_pylc_dup = 1651; Point(1651) = {0.0225, 0.0, 0, 0.01940492957746467*gmsf};
point_pylc_dup = 1652; Point(1652) = {0.1, 0.0, 0, 0.003577464788732372*gmsf};
PointM11_dup = 1656; Point(1656) = {0.1128, 0, 0, 0.0009633802816901378*gmsf};
PointM21_dup = 1658; Point(1658) = {0.1136, 0, 0, 0.0007999999999999952*gmsf};
point_pylc_dup = 1663; Point(1663) = {-0.2, 2.4492935982947065e-17, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 1664; Point(1664) = {-0.116, 1.4205902870109297e-17, 0.0, 0.0009719626168224236*gmsf};
PointM41_dup = 1666; Point(1666) = {-0.11520000000000001, 1.410793112617751e-17, 0.0, 0.0008859813084112094*gmsf};
PointM31_dup = 1667; Point(1667) = {-0.1144, 1.400995938224572e-17, 0.0, 0.0007999999999999937*gmsf};
point_pylc_dup = 1669; Point(1669) = {-0.0225, 2.7554552980815448e-18, 0.0, 0.01940492957746467*gmsf};
point_pylc_dup = 1670; Point(1670) = {-0.1, 1.2246467991473533e-17, 0.0, 0.003577464788732372*gmsf};
PointM11_dup = 1672; Point(1672) = {-0.1128, 1.3814015894382144e-17, 0.0, 0.0009633802816901378*gmsf};
PointM21_dup = 1674; Point(1674) = {-0.1136, 1.3911987638313932e-17, 0.0, 0.0007999999999999952*gmsf};
point_pylc = 1578; Point(1578) = {1.3777276490407724e-18, 0.0225, 0, 0.01940492957746467*gmsf};
point_pylc = 1579; Point(1579) = {0, 0, 0, 0.001*gmsf};
point_pylc_dup = 1727; Point(1727) = {0.09876883405950741, 0.015643446504063286, 0, 0.003577464788732372*gmsf};
point_pylc_dup = 1728; Point(1728) = {0.1106210941466483, 0.01752066008455088, 0, 0.0011267605633802748*gmsf};
point_pylc_dup = 1731; Point(1731) = {-0.1106210941466483, 0.017520660084550894, 0, 0.0011267605633802748*gmsf};
point_pylc_dup = 1733; Point(1733) = {-0.09876883405950741, 0.0156434465040633, 0, 0.003577464788732372*gmsf};
point_pylc = 1595; Point(1595) = {0.17320508075688776, 0.09999999999999999, 0, 0.009999999999999998*gmsf};
point_pylc_dup = 1693; Point(1693) = {0.10000000000000003, 0.17320508075688773, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 1696; Point(1696) = {4.163336342344337e-17, 0.20000000000000004, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 1699; Point(1699) = {-0.09999999999999998, 0.17320508075688776, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 1702; Point(1702) = {-0.1732050807568877, 0.10000000000000005, 0.0, 0.009999999999999998*gmsf};
PointM32 = 1650; Point(1650) = {0.09907330619293979, 0.057199999999999994, 0, 0.0007999999999999937*gmsf};
PointM32_dup = 1677; Point(1677) = {0.05720000000000002, 0.09907330619293978, 0.0, 0.0007999999999999937*gmsf};
PointM32_dup = 1680; Point(1680) = {2.7755575615628914e-17, 0.1144, 0.0, 0.0007999999999999937*gmsf};
PointM32_dup = 1683; Point(1683) = {-0.05719999999999999, 0.09907330619293979, 0.0, 0.0007999999999999923*gmsf};
PointM32_dup = 1686; Point(1686) = {-0.09907330619293976, 0.05720000000000003, 0.0, 0.0007999999999999937*gmsf};
PointM42_dup = 2129; Point(2129) = {0.09976612651596735, 0.0576, 0, 0.0008859813084112094*gmsf};
PointM42_dup = 2139; Point(2139) = {0.057600000000000026, 0.09976612651596733, 0.0, 0.0008859813084112094*gmsf};
PointM42_dup = 2149; Point(2149) = {2.7755575615628914e-17, 0.11520000000000001, 0.0, 0.0008859813084112094*gmsf};
PointM42_dup = 2159; Point(2159) = {-0.05759999999999999, 0.09976612651596735, 0.0, 0.0008859813084112094*gmsf};
PointM42_dup = 2169; Point(2169) = {-0.09976612651596732, 0.05760000000000003, 0.0, 0.0008859813084112094*gmsf};
point_pylc_dup = 2009; Point(2009) = {0.11371145625611974, 0.022928251483978635, 0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2011; Point(2011) = {0.11763254095460662, 0.02371888084549514, 0, 0.0014018691588785004*gmsf};
point_pylc_dup = 2012; Point(2012) = {0.11373220920115029, 0.03827511711576839, 0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2013; Point(2013) = {0.10994113556111196, 0.03699927987857611, 0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2016; Point(2016) = {0.1004589468389949, 0.057999999999999996, 0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2029; Point(2029) = {0.08701288407713331, 0.07671217637754361, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2031; Point(2031) = {0.09001332835565515, 0.07935742383883823, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 2032; Point(2032) = {0.07935742383883825, 0.09001332835565515, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2033; Point(2033) = {0.07671217637754364, 0.08701288407713331, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2036; Point(2036) = {0.058000000000000024, 0.10045894683899488, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2049; Point(2049) = {0.03699927987857613, 0.10994113556111194, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2051; Point(2051) = {0.038275117115768406, 0.11373220920115028, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2052; Point(2052) = {0.023718880845495158, 0.11763254095460662, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2053; Point(2053) = {0.02292825148397866, 0.11371145625611975, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2056; Point(2056) = {2.7755575615628914e-17, 0.11600000000000002, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2069; Point(2069) = {-0.022928251483978628, 0.11371145625611974, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2071; Point(2071) = {-0.023718880845495133, 0.11763254095460662, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 2072; Point(2072) = {-0.038275117115768385, 0.11373220920115029, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2073; Point(2073) = {-0.036999279878576104, 0.10994113556111196, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2076; Point(2076) = {-0.05799999999999999, 0.1004589468389949, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2089; Point(2089) = {-0.0767121763775436, 0.08701288407713333, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2091; Point(2091) = {-0.0793574238388382, 0.09001332835565515, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2092; Point(2092) = {-0.09001332835565512, 0.07935742383883826, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2093; Point(2093) = {-0.08701288407713328, 0.07671217637754364, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2096; Point(2096) = {-0.10045894683899487, 0.05800000000000004, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2109; Point(2109) = {-0.10994113556111193, 0.03699927987857615, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2111; Point(2111) = {-0.11373220920115026, 0.03827511711576844, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2112; Point(2112) = {-0.11763254095460662, 0.023718880845495185, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2113; Point(2113) = {-0.11371145625611975, 0.022928251483978687, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 1751; Point(1751) = {0.11852260087141653, 0.018772135804827707, 0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1753; Point(1753) = {0.14321480938629497, 0.02268299743083347, 0, 0.004088785046728965*gmsf};
point_pylc_dup = 1756; Point(1756) = {0.13536916184209424, 0.05196335268406853, 0, 0.004088785046728965*gmsf};
point_pylc_dup = 1758; Point(1758) = {0.11202965117966421, 0.04300415394543603, 0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1781; Point(1781) = {0.09325751537483652, 0.07551844692598049, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 1783; Point(1783) = {0.1126861644112608, 0.09125145670222641, 0.0, 0.004088785046728967*gmsf};
point_pylc_dup = 1786; Point(1786) = {0.09125145670222644, 0.11268616441126075, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 1788; Point(1788) = {0.0755184469259805, 0.09325751537483651, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 1811; Point(1811) = {0.043004153945436045, 0.11202965117966421, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1813; Point(1813) = {0.051963352684068556, 0.13536916184209424, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 1816; Point(1816) = {0.022682997430833497, 0.14321480938629494, 0.0, 0.004088785046728962*gmsf};
point_pylc_dup = 1818; Point(1818) = {0.01877213580482772, 0.11852260087141653, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1841; Point(1841) = {-0.0187721358048277, 0.11852260087141653, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1843; Point(1843) = {-0.02268299743083346, 0.14321480938629497, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 1846; Point(1846) = {-0.05196335268406852, 0.13536916184209424, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 1848; Point(1848) = {-0.043004153945436024, 0.11202965117966421, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1871; Point(1871) = {-0.07551844692598048, 0.09325751537483652, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1873; Point(1873) = {-0.0912514567022264, 0.1126861644112608, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 1876; Point(1876) = {-0.11268616441126074, 0.09125145670222644, 0.0, 0.004088785046728962*gmsf};
point_pylc_dup = 1878; Point(1878) = {-0.09325751537483648, 0.0755184469259805, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1901; Point(1901) = {-0.11202965117966421, 0.04300415394543608, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 1903; Point(1903) = {-0.13536916184209422, 0.051963352684068584, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 1906; Point(1906) = {-0.14321480938629494, 0.022682997430833532, 0.0, 0.004088785046728962*gmsf};
point_pylc_dup = 1908; Point(1908) = {-0.11852260087141651, 0.01877213580482775, 0.0, 0.0014018691588784976*gmsf};

// Lines and Curves
Line_dup = 965;Line(Line_dup) = {1653, 1654}; 
lowerLine4_dup = 968;Line(lowerLine4_dup) = {1654, 1660}; 
lowerLine3_dup = 969;Line(lowerLine3_dup) = {1661, 1660}; 
Line_dup = 964;Line(Line_dup) = {1651, 1652}; 
lowerLine1_dup = 966;Line(lowerLine1_dup) = {1652, 1656}; 
lowerLine2_dup = 967;Line(lowerLine2_dup) = {1656, 1658}; 
Line_dup = 970;Line(Line_dup) = {1663, 1664}; 
lowerLine4_dup = 971;Line(lowerLine4_dup) = {1664, 1666}; 
lowerLine3_dup = 972;Line(lowerLine3_dup) = {1667, 1666}; 
Line_dup = 973;Line(Line_dup) = {1669, 1670}; 
lowerLine1_dup = 974;Line(lowerLine1_dup) = {1670, 1672}; 
lowerLine2_dup = 975;Line(lowerLine2_dup) = {1672, 1674}; 
InnerLimit = 913;Circle(InnerLimit) = {1669, 1579, 1578}; 
InnerLimit = 915;Circle(InnerLimit) = {1578, 1579, 1651}; 
MB_CurveRotor = 953;Circle(MB_CurveRotor) = {1658, 1579, 1674}; 
rotorBand1_dup = 1173;Circle(rotorBand1_dup) = {1656, 1579, 1672}; 
Line_dup = 1010;Line(Line_dup) = {1727, 1728}; 
CircleArc_dup = 1012;Circle(CircleArc_dup) = {1728, 1579, 1731}; 
Line_dup = 1013;Line(Line_dup) = {1731, 1733}; 
CircleArc_dup = 1015;Circle(CircleArc_dup) = {1733, 1579, 1727}; 
CircleArc_dup = 1161;Circle(CircleArc_dup) = {1652, 1579, 1727}; 
CircleArc_dup = 1163;Circle(CircleArc_dup) = {1733, 1579, 1670}; 
OuterLimit = 924;Circle(OuterLimit) = {1595, 1579, 1653}; 
OuterLimit_dup = 989;Circle(OuterLimit_dup) = {1693, 1579, 1595}; 
OuterLimit_dup = 991;Circle(OuterLimit_dup) = {1696, 1579, 1693}; 
OuterLimit_dup = 993;Circle(OuterLimit_dup) = {1699, 1579, 1696}; 
OuterLimit_dup = 995;Circle(OuterLimit_dup) = {1702, 1579, 1699}; 
OuterLimit_dup = 997;Circle(OuterLimit_dup) = {1663, 1579, 1702}; 
MB_CurveStator = 961;Circle(MB_CurveStator) = {1661, 1579, 1650}; 
MB_CurveStator_dup = 977;Circle(MB_CurveStator_dup) = {1650, 1579, 1677}; 
MB_CurveStator_dup = 979;Circle(MB_CurveStator_dup) = {1677, 1579, 1680}; 
MB_CurveStator_dup = 981;Circle(MB_CurveStator_dup) = {1680, 1579, 1683}; 
MB_CurveStator_dup = 983;Circle(MB_CurveStator_dup) = {1683, 1579, 1686}; 
MB_CurveStator_dup = 985;Circle(MB_CurveStator_dup) = {1686, 1579, 1667}; 
statorCircle4_dup = 1251;Circle(statorCircle4_dup) = {1660, 1579, 2129}; 
upperLine3_dup = 1255;Line(upperLine3_dup) = {1650, 2129}; 
statorCircle4_dup = 1257;Circle(statorCircle4_dup) = {2129, 1579, 2139}; 
upperLine3_dup = 1261;Line(upperLine3_dup) = {1677, 2139}; 
statorCircle4_dup = 1263;Circle(statorCircle4_dup) = {2139, 1579, 2149}; 
upperLine3_dup = 1267;Line(upperLine3_dup) = {1680, 2149}; 
statorCircle4_dup = 1269;Circle(statorCircle4_dup) = {2149, 1579, 2159}; 
upperLine3_dup = 1273;Line(upperLine3_dup) = {1683, 2159}; 
statorCircle4_dup = 1275;Circle(statorCircle4_dup) = {2159, 1579, 2169}; 
upperLine3_dup = 1279;Line(upperLine3_dup) = {1686, 2169}; 
statorCircle4_dup = 1281;Circle(statorCircle4_dup) = {2169, 1579, 1666}; 
CircleArc_dup = 1179;Circle(CircleArc_dup) = {1654, 1579, 2009}; 
Line_dup = 1180;Line(Line_dup) = {2009, 2011}; 
Line_dup = 1181;Line(Line_dup) = {2012, 2013}; 
CircleArc_dup = 1183;Circle(CircleArc_dup) = {2013, 1579, 2016}; 
interface_line_slot_opening___slot_dup = 1185;Circle(interface_line_slot_opening___slot_dup) = {2011, 1579, 2012}; 
upperLine4_dup = 1189;Line(upperLine4_dup) = {2016, 2129}; 
CircleArc_dup = 1191;Circle(CircleArc_dup) = {2016, 1579, 2029}; 
Line_dup = 1192;Line(Line_dup) = {2029, 2031}; 
Line_dup = 1193;Line(Line_dup) = {2032, 2033}; 
CircleArc_dup = 1195;Circle(CircleArc_dup) = {2033, 1579, 2036}; 
interface_line_slot_opening___slot_dup = 1197;Circle(interface_line_slot_opening___slot_dup) = {2031, 1579, 2032}; 
upperLine4_dup = 1201;Line(upperLine4_dup) = {2036, 2139}; 
CircleArc_dup = 1203;Circle(CircleArc_dup) = {2036, 1579, 2049}; 
Line_dup = 1204;Line(Line_dup) = {2049, 2051}; 
Line_dup = 1205;Line(Line_dup) = {2052, 2053}; 
CircleArc_dup = 1207;Circle(CircleArc_dup) = {2053, 1579, 2056}; 
interface_line_slot_opening___slot_dup = 1209;Circle(interface_line_slot_opening___slot_dup) = {2051, 1579, 2052}; 
upperLine4_dup = 1213;Line(upperLine4_dup) = {2056, 2149}; 
CircleArc_dup = 1215;Circle(CircleArc_dup) = {2056, 1579, 2069}; 
Line_dup = 1216;Line(Line_dup) = {2069, 2071}; 
Line_dup = 1217;Line(Line_dup) = {2072, 2073}; 
CircleArc_dup = 1219;Circle(CircleArc_dup) = {2073, 1579, 2076}; 
interface_line_slot_opening___slot_dup = 1221;Circle(interface_line_slot_opening___slot_dup) = {2071, 1579, 2072}; 
upperLine4_dup = 1225;Line(upperLine4_dup) = {2076, 2159}; 
CircleArc_dup = 1227;Circle(CircleArc_dup) = {2076, 1579, 2089}; 
Line_dup = 1228;Line(Line_dup) = {2089, 2091}; 
Line_dup = 1229;Line(Line_dup) = {2092, 2093}; 
CircleArc_dup = 1231;Circle(CircleArc_dup) = {2093, 1579, 2096}; 
interface_line_slot_opening___slot_dup = 1233;Circle(interface_line_slot_opening___slot_dup) = {2091, 1579, 2092}; 
upperLine4_dup = 1237;Line(upperLine4_dup) = {2096, 2169}; 
CircleArc_dup = 1239;Circle(CircleArc_dup) = {2096, 1579, 2109}; 
Line_dup = 1240;Line(Line_dup) = {2109, 2111}; 
Line_dup = 1241;Line(Line_dup) = {2112, 2113}; 
CircleArc_dup = 1243;Circle(CircleArc_dup) = {2113, 1579, 1664}; 
interface_line_slot_opening___slot_dup = 1245;Circle(interface_line_slot_opening___slot_dup) = {2111, 1579, 2112}; 
Line_dup = 1016;Line(Line_dup) = {2016, 1595}; 
CircleArc_dup = 1024;Circle(CircleArc_dup) = {2011, 1579, 1751}; 
Line_dup = 1025;Line(Line_dup) = {1751, 1753}; 
CircleArc_dup = 1027;Circle(CircleArc_dup) = {1753, 1579, 1756}; 
Line_dup = 1028;Line(Line_dup) = {1756, 1758}; 
CircleArc_dup = 1030;Circle(CircleArc_dup) = {1758, 1579, 2012}; 
Line_dup = 1034;Line(Line_dup) = {2036, 1693}; 
CircleArc_dup = 1042;Circle(CircleArc_dup) = {2031, 1579, 1781}; 
Line_dup = 1043;Line(Line_dup) = {1781, 1783}; 
CircleArc_dup = 1045;Circle(CircleArc_dup) = {1783, 1579, 1786}; 
Line_dup = 1046;Line(Line_dup) = {1786, 1788}; 
CircleArc_dup = 1048;Circle(CircleArc_dup) = {1788, 1579, 2032}; 
Line_dup = 1052;Line(Line_dup) = {2056, 1696}; 
CircleArc_dup = 1060;Circle(CircleArc_dup) = {2051, 1579, 1811}; 
Line_dup = 1061;Line(Line_dup) = {1811, 1813}; 
CircleArc_dup = 1063;Circle(CircleArc_dup) = {1813, 1579, 1816}; 
Line_dup = 1064;Line(Line_dup) = {1816, 1818}; 
CircleArc_dup = 1066;Circle(CircleArc_dup) = {1818, 1579, 2052}; 
Line_dup = 1070;Line(Line_dup) = {2076, 1699}; 
CircleArc_dup = 1078;Circle(CircleArc_dup) = {2071, 1579, 1841}; 
Line_dup = 1079;Line(Line_dup) = {1841, 1843}; 
CircleArc_dup = 1081;Circle(CircleArc_dup) = {1843, 1579, 1846}; 
Line_dup = 1082;Line(Line_dup) = {1846, 1848}; 
CircleArc_dup = 1084;Circle(CircleArc_dup) = {1848, 1579, 2072}; 
Line_dup = 1088;Line(Line_dup) = {2096, 1702}; 
CircleArc_dup = 1096;Circle(CircleArc_dup) = {2091, 1579, 1871}; 
Line_dup = 1097;Line(Line_dup) = {1871, 1873}; 
CircleArc_dup = 1099;Circle(CircleArc_dup) = {1873, 1579, 1876}; 
Line_dup = 1100;Line(Line_dup) = {1876, 1878}; 
CircleArc_dup = 1102;Circle(CircleArc_dup) = {1878, 1579, 2092}; 
CircleArc_dup = 1114;Circle(CircleArc_dup) = {2111, 1579, 1901}; 
Line_dup = 1115;Line(Line_dup) = {1901, 1903}; 
CircleArc_dup = 1117;Circle(CircleArc_dup) = {1903, 1579, 1906}; 
Line_dup = 1118;Line(Line_dup) = {1906, 1908}; 
CircleArc_dup = 1120;Circle(CircleArc_dup) = {1908, 1579, 2112}; 
CircleArc_dup = 1125;Circle(CircleArc_dup) = {1751, 1579, 1758}; 
CircleArc_dup = 1131;Circle(CircleArc_dup) = {1781, 1579, 1788}; 
CircleArc_dup = 1137;Circle(CircleArc_dup) = {1811, 1579, 1818}; 
CircleArc_dup = 1143;Circle(CircleArc_dup) = {1841, 1579, 1848}; 
CircleArc_dup = 1149;Circle(CircleArc_dup) = {1871, 1579, 1878}; 
CircleArc_dup = 1155;Circle(CircleArc_dup) = {1901, 1579, 1908}; 

// Surfaces

Curve Loop(121) = {1173,975,-953,-967};
Surf_rotorAirGap2_dup = {121};
Plane Surface(Surf_rotorAirGap2_dup) = {121};

Curve Loop(107) = {1010,1012,1013,1015};
Surf_Magnet_dup = {107};
Plane Surface(Surf_Magnet_dup) = {107};

Curve Loop(120) = {1161,1010,1012,1013,1163,974,-1173,-966};
Surf_rotorAirGap1_dup = {120};
Plane Surface(Surf_rotorAirGap1_dup) = {120};

Curve Loop(106) = {964,1161,-1015,1163,-973,913,915};
Surf_Rotorblech_dup = {106};
Plane Surface(Surf_Rotorblech_dup) = {106};

Curve Loop(128) = {1251,-1255,-961,969};
Surf_statorAirGap2_dup = {128};
Plane Surface(Surf_statorAirGap2_dup) = {128};

Curve Loop(129) = {1257,-1261,-977,1255};
Surf_statorAirGap2_dup = {129};
Plane Surface(Surf_statorAirGap2_dup) = {129};

Curve Loop(130) = {1263,-1267,-979,1261};
Surf_statorAirGap2_dup = {130};
Plane Surface(Surf_statorAirGap2_dup) = {130};

Curve Loop(131) = {1269,-1273,-981,1267};
Surf_statorAirGap2_dup = {131};
Plane Surface(Surf_statorAirGap2_dup) = {131};

Curve Loop(132) = {1275,-1279,-983,1273};
Surf_statorAirGap2_dup = {132};
Plane Surface(Surf_statorAirGap2_dup) = {132};

Curve Loop(133) = {1281,-972,-985,1279};
Surf_statorAirGap2_dup = {133};
Plane Surface(Surf_statorAirGap2_dup) = {133};

Curve Loop(122) = {1179,1180,1185,1181,1183,1189,-1251,-968};
Surf_statorAirGap1_dup = {122};
Plane Surface(Surf_statorAirGap1_dup) = {122};

Curve Loop(123) = {1191,1192,1197,1193,1195,1201,-1257,-1189};
Surf_statorAirGap1_dup = {123};
Plane Surface(Surf_statorAirGap1_dup) = {123};

Curve Loop(124) = {1203,1204,1209,1205,1207,1213,-1263,-1201};
Surf_statorAirGap1_dup = {124};
Plane Surface(Surf_statorAirGap1_dup) = {124};

Curve Loop(125) = {1215,1216,1221,1217,1219,1225,-1269,-1213};
Surf_statorAirGap1_dup = {125};
Plane Surface(Surf_statorAirGap1_dup) = {125};

Curve Loop(126) = {1227,1228,1233,1229,1231,1237,-1275,-1225};
Surf_statorAirGap1_dup = {126};
Plane Surface(Surf_statorAirGap1_dup) = {126};

Curve Loop(127) = {1239,1240,1245,1241,1243,971,-1281,-1237};
Surf_statorAirGap1_dup = {127};
Plane Surface(Surf_statorAirGap1_dup) = {127};

Curve Loop(108) = {1016,924,965,1179,1180,1024,1025,1027,1028,1030,1181,1183};
Surf_Statorblech_dup = {108};
Plane Surface(Surf_Statorblech_dup) = {108};

Curve Loop(109) = {1034,989,-1016,1191,1192,1042,1043,1045,1046,1048,1193,1195};
Surf_Statorblech_dup = {109};
Plane Surface(Surf_Statorblech_dup) = {109};

Curve Loop(110) = {1052,991,-1034,1203,1204,1060,1061,1063,1064,1066,1205,1207};
Surf_Statorblech_dup = {110};
Plane Surface(Surf_Statorblech_dup) = {110};

Curve Loop(111) = {1070,993,-1052,1215,1216,1078,1079,1081,1082,1084,1217,1219};
Surf_Statorblech_dup = {111};
Plane Surface(Surf_Statorblech_dup) = {111};

Curve Loop(112) = {1088,995,-1070,1227,1228,1096,1097,1099,1100,1102,1229,1231};
Surf_Statorblech_dup = {112};
Plane Surface(Surf_Statorblech_dup) = {112};

Curve Loop(113) = {970,-1243,-1241,-1120,-1118,-1117,-1115,-1114,-1240,-1239,1088,-997};
Surf_Statorblech_dup = {113};
Plane Surface(Surf_Statorblech_dup) = {113};

Curve Loop(114) = {1125,-1028,-1027,-1025};
Surf_Stator_Nut_dup = {114};
Plane Surface(Surf_Stator_Nut_dup) = {114};

Curve Loop(115) = {1131,-1046,-1045,-1043};
Surf_Stator_Nut_dup = {115};
Plane Surface(Surf_Stator_Nut_dup) = {115};

Curve Loop(116) = {1137,-1064,-1063,-1061};
Surf_Stator_Nut_dup = {116};
Plane Surface(Surf_Stator_Nut_dup) = {116};

Curve Loop(117) = {1143,-1082,-1081,-1079};
Surf_Stator_Nut_dup = {117};
Plane Surface(Surf_Stator_Nut_dup) = {117};

Curve Loop(118) = {1149,-1100,-1099,-1097};
Surf_Stator_Nut_dup = {118};
Plane Surface(Surf_Stator_Nut_dup) = {118};

Curve Loop(119) = {1155,-1118,-1117,-1115};
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
Physical Curve("primaryLineS", 3) = {965,968,969};
// primaryLineR
Physical Curve("primaryLineR", 2) = {964,966,967};
// slaveLineS
Physical Curve("slaveLineS", 5) = {970,971,972};
// slaveLineR
Physical Curve("slaveLineR", 4) = {973,974,975};
// innerLimit
Physical Curve("innerLimit", 10) = {913,915};
// Rotor_Bnd_MB_1
Physical Curve("Rotor_Bnd_MB_1", 7) = {953};
// Rotor_Bnd_MB_2
Physical Curve("Rotor_Bnd_MB_2", 8) = {953};
// LuR2
Physical Surface("LuR2", 21) = {121};
// Mag0_0
Physical Surface("Mag0_0", 12) = {107};
// LuR1
Physical Surface("LuR1", 20) = {120};
// Pol
Physical Surface("Pol", 11) = {106};
// outerLimit
Physical Curve("outerLimit", 9) = {924,989,991,993,995,997};
// mbStator
Physical Curve("mbStator", 6) = {961,977,979,981,983,985};
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
primaryLines = {964,966,967,965,968,969};
secondaryLines = {973,974,975,970,971,972};
Periodic Curve{secondaryLines[]} = {primaryLines[]} Rotate {{0,0,1}, {0,0,0}, 2*Pi/2};

// Add mesh size setting for Movingband lines
DefineConstant[
	NbrMbSegments = {890.0, Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],Max 1440, Min 180, Step 10, Help "Set the number of mesh segments on the interface between rotor/statorairgap and movingband. Value represents number of segments on whole circle.", Visible Flag_ExpertMode},
	r_MB_R = 0.1136
];
MB_LinesR = {953,987};
MeshSize{ PointsOf{Line{MB_LinesR[]};}} = 2*Pi*r_MB_R/NbrMbSegments;

MB_LinesS = {961,977,979,981,983,985};
MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*0.1144/NbrMbSegments;

Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)

// Create boundary lines for moving rotor contour plot
rotorBndLines[] = Boundary{ Physical Surface{ 12 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 11 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 21 }; };
statorBndLines[] = Boundary{ Physical Surface{ 3,5,6,9,13,14,15,16,17,18,19,22,23 }; };
Physical Line("DomainPlotMovingGeo",1) = {rotorBndLines[], statorBndLines[]}; 
