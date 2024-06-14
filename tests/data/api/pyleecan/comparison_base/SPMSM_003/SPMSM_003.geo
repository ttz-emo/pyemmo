// This script was created with pyemmo (Version 1.3.1b1, git 86642f)

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
point_pylc_dup = 1865; Point(1865) = {0.2, 0.0, 0, 0.009999999999999998*gmsf};
point_pylc_dup = 1866; Point(1866) = {0.116, 0.0, 0, 0.0009719626168224236*gmsf};
PointM41_dup = 1872; Point(1872) = {0.11520000000000001, 0, 0, 0.0008859813084112094*gmsf};
PointM31_dup = 1873; Point(1873) = {0.1144, 0, 0, 0.0007999999999999937*gmsf};
point_pylc_dup = 1863; Point(1863) = {0.0225, 0.0, 0, 0.01940492957746467*gmsf};
point_pylc_dup = 1864; Point(1864) = {0.1, 0.0, 0, 0.003577464788732372*gmsf};
PointM11_dup = 1868; Point(1868) = {0.1128, 0, 0, 0.0009633802816901378*gmsf};
PointM21_dup = 1870; Point(1870) = {0.1136, 0, 0, 0.0007999999999999952*gmsf};
point_pylc_dup = 1875; Point(1875) = {-0.2, 2.4492935982947065e-17, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 1876; Point(1876) = {-0.116, 1.4205902870109297e-17, 0.0, 0.0009719626168224236*gmsf};
PointM41_dup = 1878; Point(1878) = {-0.11520000000000001, 1.410793112617751e-17, 0.0, 0.0008859813084112094*gmsf};
PointM31_dup = 1879; Point(1879) = {-0.1144, 1.400995938224572e-17, 0.0, 0.0007999999999999937*gmsf};
point_pylc_dup = 1881; Point(1881) = {-0.0225, 2.7554552980815448e-18, 0.0, 0.01940492957746467*gmsf};
point_pylc_dup = 1882; Point(1882) = {-0.1, 1.2246467991473533e-17, 0.0, 0.003577464788732372*gmsf};
PointM11_dup = 1884; Point(1884) = {-0.1128, 1.3814015894382144e-17, 0.0, 0.0009633802816901378*gmsf};
PointM21_dup = 1886; Point(1886) = {-0.1136, 1.3911987638313932e-17, 0.0, 0.0007999999999999952*gmsf};
point_pylc = 1706; Point(1706) = {1.3777276490407724e-18, 0.0225, 0, 0.01940492957746467*gmsf};
point_pylc = 1707; Point(1707) = {0, 0, 0, 0.001*gmsf};
point_pylc_dup = 1939; Point(1939) = {0.09876883405950741, 0.015643446504063286, 0, 0.003577464788732372*gmsf};
point_pylc_dup = 1940; Point(1940) = {0.1106210941466483, 0.01752066008455088, 0, 0.0011267605633802748*gmsf};
point_pylc_dup = 1943; Point(1943) = {-0.1106210941466483, 0.017520660084550894, 0, 0.0011267605633802748*gmsf};
point_pylc_dup = 1945; Point(1945) = {-0.09876883405950741, 0.0156434465040633, 0, 0.003577464788732372*gmsf};
point_pylc = 1723; Point(1723) = {0.17320508075688776, 0.09999999999999999, 0, 0.009999999999999998*gmsf};
point_pylc_dup = 1905; Point(1905) = {0.10000000000000003, 0.17320508075688773, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 1908; Point(1908) = {4.163336342344337e-17, 0.20000000000000004, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 1911; Point(1911) = {-0.09999999999999998, 0.17320508075688776, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 1914; Point(1914) = {-0.1732050807568877, 0.10000000000000005, 0.0, 0.009999999999999998*gmsf};
PointM32 = 1862; Point(1862) = {0.09907330619293979, 0.057199999999999994, 0, 0.0007999999999999937*gmsf};
PointM32_dup = 1889; Point(1889) = {0.05720000000000002, 0.09907330619293978, 0.0, 0.0007999999999999937*gmsf};
PointM32_dup = 1892; Point(1892) = {2.7755575615628914e-17, 0.1144, 0.0, 0.0007999999999999937*gmsf};
PointM32_dup = 1895; Point(1895) = {-0.05719999999999999, 0.09907330619293979, 0.0, 0.0007999999999999923*gmsf};
PointM32_dup = 1898; Point(1898) = {-0.09907330619293976, 0.05720000000000003, 0.0, 0.0007999999999999937*gmsf};
PointM42_dup = 2341; Point(2341) = {0.09976612651596735, 0.0576, 0, 0.0008859813084112094*gmsf};
PointM42_dup = 2351; Point(2351) = {0.057600000000000026, 0.09976612651596733, 0.0, 0.0008859813084112094*gmsf};
PointM42_dup = 2361; Point(2361) = {2.7755575615628914e-17, 0.11520000000000001, 0.0, 0.0008859813084112094*gmsf};
PointM42_dup = 2371; Point(2371) = {-0.05759999999999999, 0.09976612651596735, 0.0, 0.0008859813084112094*gmsf};
PointM42_dup = 2381; Point(2381) = {-0.09976612651596732, 0.05760000000000003, 0.0, 0.0008859813084112094*gmsf};
point_pylc_dup = 2221; Point(2221) = {0.11371145625611974, 0.022928251483978635, 0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2223; Point(2223) = {0.11763254095460662, 0.02371888084549514, 0, 0.0014018691588785004*gmsf};
point_pylc_dup = 2224; Point(2224) = {0.11373220920115029, 0.03827511711576839, 0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2225; Point(2225) = {0.10994113556111196, 0.03699927987857611, 0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2228; Point(2228) = {0.1004589468389949, 0.057999999999999996, 0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2241; Point(2241) = {0.08701288407713331, 0.07671217637754361, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2243; Point(2243) = {0.09001332835565515, 0.07935742383883823, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 2244; Point(2244) = {0.07935742383883825, 0.09001332835565515, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2245; Point(2245) = {0.07671217637754364, 0.08701288407713331, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2248; Point(2248) = {0.058000000000000024, 0.10045894683899488, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2261; Point(2261) = {0.03699927987857613, 0.10994113556111194, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2263; Point(2263) = {0.038275117115768406, 0.11373220920115028, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2264; Point(2264) = {0.023718880845495158, 0.11763254095460662, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2265; Point(2265) = {0.02292825148397866, 0.11371145625611975, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2268; Point(2268) = {2.7755575615628914e-17, 0.11600000000000002, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2281; Point(2281) = {-0.022928251483978628, 0.11371145625611974, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2283; Point(2283) = {-0.023718880845495133, 0.11763254095460662, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 2284; Point(2284) = {-0.038275117115768385, 0.11373220920115029, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2285; Point(2285) = {-0.036999279878576104, 0.10994113556111196, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2288; Point(2288) = {-0.05799999999999999, 0.1004589468389949, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2301; Point(2301) = {-0.0767121763775436, 0.08701288407713333, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2303; Point(2303) = {-0.0793574238388382, 0.09001332835565515, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2304; Point(2304) = {-0.09001332835565512, 0.07935742383883826, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2305; Point(2305) = {-0.08701288407713328, 0.07671217637754364, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 2308; Point(2308) = {-0.10045894683899487, 0.05800000000000004, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2321; Point(2321) = {-0.10994113556111193, 0.03699927987857615, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 2323; Point(2323) = {-0.11373220920115026, 0.03827511711576844, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2324; Point(2324) = {-0.11763254095460662, 0.023718880845495185, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2325; Point(2325) = {-0.11371145625611975, 0.022928251483978687, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 1963; Point(1963) = {0.11852260087141653, 0.018772135804827707, 0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1965; Point(1965) = {0.14321480938629497, 0.02268299743083347, 0, 0.004088785046728965*gmsf};
point_pylc_dup = 1968; Point(1968) = {0.13536916184209424, 0.05196335268406853, 0, 0.004088785046728965*gmsf};
point_pylc_dup = 1970; Point(1970) = {0.11202965117966421, 0.04300415394543603, 0, 0.0014018691588784976*gmsf};
point_pylc_dup = 1993; Point(1993) = {0.09325751537483652, 0.07551844692598049, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 1995; Point(1995) = {0.1126861644112608, 0.09125145670222641, 0.0, 0.004088785046728967*gmsf};
point_pylc_dup = 1998; Point(1998) = {0.09125145670222644, 0.11268616441126075, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 2000; Point(2000) = {0.0755184469259805, 0.09325751537483651, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 2023; Point(2023) = {0.043004153945436045, 0.11202965117966421, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2025; Point(2025) = {0.051963352684068556, 0.13536916184209424, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 2028; Point(2028) = {0.022682997430833497, 0.14321480938629494, 0.0, 0.004088785046728962*gmsf};
point_pylc_dup = 2030; Point(2030) = {0.01877213580482772, 0.11852260087141653, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2053; Point(2053) = {-0.0187721358048277, 0.11852260087141653, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2055; Point(2055) = {-0.02268299743083346, 0.14321480938629497, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 2058; Point(2058) = {-0.05196335268406852, 0.13536916184209424, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 2060; Point(2060) = {-0.043004153945436024, 0.11202965117966421, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2083; Point(2083) = {-0.07551844692598048, 0.09325751537483652, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2085; Point(2085) = {-0.0912514567022264, 0.1126861644112608, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 2088; Point(2088) = {-0.11268616441126074, 0.09125145670222644, 0.0, 0.004088785046728962*gmsf};
point_pylc_dup = 2090; Point(2090) = {-0.09325751537483648, 0.0755184469259805, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 2113; Point(2113) = {-0.11202965117966421, 0.04300415394543608, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 2115; Point(2115) = {-0.13536916184209422, 0.051963352684068584, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 2118; Point(2118) = {-0.14321480938629494, 0.022682997430833532, 0.0, 0.004088785046728962*gmsf};
point_pylc_dup = 2120; Point(2120) = {-0.11852260087141651, 0.01877213580482775, 0.0, 0.0014018691588784976*gmsf};

// Lines and Curves
Line_dup = 965;Line(Line_dup) = {1865, 1866}; 
lowerLine4_dup = 968;Line(lowerLine4_dup) = {1866, 1872}; 
lowerLine3_dup = 969;Line(lowerLine3_dup) = {1873, 1872}; 
Line_dup = 964;Line(Line_dup) = {1863, 1864}; 
lowerLine1_dup = 966;Line(lowerLine1_dup) = {1864, 1868}; 
lowerLine2_dup = 967;Line(lowerLine2_dup) = {1868, 1870}; 
Line_dup = 970;Line(Line_dup) = {1875, 1876}; 
lowerLine4_dup = 971;Line(lowerLine4_dup) = {1876, 1878}; 
lowerLine3_dup = 972;Line(lowerLine3_dup) = {1879, 1878}; 
Line_dup = 973;Line(Line_dup) = {1881, 1882}; 
lowerLine1_dup = 974;Line(lowerLine1_dup) = {1882, 1884}; 
lowerLine2_dup = 975;Line(lowerLine2_dup) = {1884, 1886}; 
InnerLimit = 913;Circle(InnerLimit) = {1881, 1707, 1706}; 
InnerLimit = 915;Circle(InnerLimit) = {1706, 1707, 1863}; 
MB_CurveRotor = 953;Circle(MB_CurveRotor) = {1870, 1707, 1886}; 
rotorBand1_dup = 1173;Circle(rotorBand1_dup) = {1868, 1707, 1884}; 
Line_dup = 1010;Line(Line_dup) = {1939, 1940}; 
CircleArc_dup = 1012;Circle(CircleArc_dup) = {1940, 1707, 1943}; 
Line_dup = 1013;Line(Line_dup) = {1943, 1945}; 
CircleArc_dup = 1015;Circle(CircleArc_dup) = {1945, 1707, 1939}; 
CircleArc_dup = 1161;Circle(CircleArc_dup) = {1864, 1707, 1939}; 
CircleArc_dup = 1163;Circle(CircleArc_dup) = {1945, 1707, 1882}; 
OuterLimit = 924;Circle(OuterLimit) = {1723, 1707, 1865}; 
OuterLimit_dup = 989;Circle(OuterLimit_dup) = {1905, 1707, 1723}; 
OuterLimit_dup = 991;Circle(OuterLimit_dup) = {1908, 1707, 1905}; 
OuterLimit_dup = 993;Circle(OuterLimit_dup) = {1911, 1707, 1908}; 
OuterLimit_dup = 995;Circle(OuterLimit_dup) = {1914, 1707, 1911}; 
OuterLimit_dup = 997;Circle(OuterLimit_dup) = {1875, 1707, 1914}; 
MB_CurveStator = 961;Circle(MB_CurveStator) = {1873, 1707, 1862}; 
MB_CurveStator_dup = 977;Circle(MB_CurveStator_dup) = {1862, 1707, 1889}; 
MB_CurveStator_dup = 979;Circle(MB_CurveStator_dup) = {1889, 1707, 1892}; 
MB_CurveStator_dup = 981;Circle(MB_CurveStator_dup) = {1892, 1707, 1895}; 
MB_CurveStator_dup = 983;Circle(MB_CurveStator_dup) = {1895, 1707, 1898}; 
MB_CurveStator_dup = 985;Circle(MB_CurveStator_dup) = {1898, 1707, 1879}; 
statorCircle4_dup = 1251;Circle(statorCircle4_dup) = {1872, 1707, 2341}; 
upperLine3_dup = 1255;Line(upperLine3_dup) = {1862, 2341}; 
statorCircle4_dup = 1257;Circle(statorCircle4_dup) = {2341, 1707, 2351}; 
upperLine3_dup = 1261;Line(upperLine3_dup) = {1889, 2351}; 
statorCircle4_dup = 1263;Circle(statorCircle4_dup) = {2351, 1707, 2361}; 
upperLine3_dup = 1267;Line(upperLine3_dup) = {1892, 2361}; 
statorCircle4_dup = 1269;Circle(statorCircle4_dup) = {2361, 1707, 2371}; 
upperLine3_dup = 1273;Line(upperLine3_dup) = {1895, 2371}; 
statorCircle4_dup = 1275;Circle(statorCircle4_dup) = {2371, 1707, 2381}; 
upperLine3_dup = 1279;Line(upperLine3_dup) = {1898, 2381}; 
statorCircle4_dup = 1281;Circle(statorCircle4_dup) = {2381, 1707, 1878}; 
CircleArc_dup = 1179;Circle(CircleArc_dup) = {1866, 1707, 2221}; 
Line_dup = 1180;Line(Line_dup) = {2221, 2223}; 
Line_dup = 1181;Line(Line_dup) = {2224, 2225}; 
CircleArc_dup = 1183;Circle(CircleArc_dup) = {2225, 1707, 2228}; 
interface_line_slot_opening___slot_dup = 1185;Circle(interface_line_slot_opening___slot_dup) = {2223, 1707, 2224}; 
upperLine4_dup = 1189;Line(upperLine4_dup) = {2228, 2341}; 
CircleArc_dup = 1191;Circle(CircleArc_dup) = {2228, 1707, 2241}; 
Line_dup = 1192;Line(Line_dup) = {2241, 2243}; 
Line_dup = 1193;Line(Line_dup) = {2244, 2245}; 
CircleArc_dup = 1195;Circle(CircleArc_dup) = {2245, 1707, 2248}; 
interface_line_slot_opening___slot_dup = 1197;Circle(interface_line_slot_opening___slot_dup) = {2243, 1707, 2244}; 
upperLine4_dup = 1201;Line(upperLine4_dup) = {2248, 2351}; 
CircleArc_dup = 1203;Circle(CircleArc_dup) = {2248, 1707, 2261}; 
Line_dup = 1204;Line(Line_dup) = {2261, 2263}; 
Line_dup = 1205;Line(Line_dup) = {2264, 2265}; 
CircleArc_dup = 1207;Circle(CircleArc_dup) = {2265, 1707, 2268}; 
interface_line_slot_opening___slot_dup = 1209;Circle(interface_line_slot_opening___slot_dup) = {2263, 1707, 2264}; 
upperLine4_dup = 1213;Line(upperLine4_dup) = {2268, 2361}; 
CircleArc_dup = 1215;Circle(CircleArc_dup) = {2268, 1707, 2281}; 
Line_dup = 1216;Line(Line_dup) = {2281, 2283}; 
Line_dup = 1217;Line(Line_dup) = {2284, 2285}; 
CircleArc_dup = 1219;Circle(CircleArc_dup) = {2285, 1707, 2288}; 
interface_line_slot_opening___slot_dup = 1221;Circle(interface_line_slot_opening___slot_dup) = {2283, 1707, 2284}; 
upperLine4_dup = 1225;Line(upperLine4_dup) = {2288, 2371}; 
CircleArc_dup = 1227;Circle(CircleArc_dup) = {2288, 1707, 2301}; 
Line_dup = 1228;Line(Line_dup) = {2301, 2303}; 
Line_dup = 1229;Line(Line_dup) = {2304, 2305}; 
CircleArc_dup = 1231;Circle(CircleArc_dup) = {2305, 1707, 2308}; 
interface_line_slot_opening___slot_dup = 1233;Circle(interface_line_slot_opening___slot_dup) = {2303, 1707, 2304}; 
upperLine4_dup = 1237;Line(upperLine4_dup) = {2308, 2381}; 
CircleArc_dup = 1239;Circle(CircleArc_dup) = {2308, 1707, 2321}; 
Line_dup = 1240;Line(Line_dup) = {2321, 2323}; 
Line_dup = 1241;Line(Line_dup) = {2324, 2325}; 
CircleArc_dup = 1243;Circle(CircleArc_dup) = {2325, 1707, 1876}; 
interface_line_slot_opening___slot_dup = 1245;Circle(interface_line_slot_opening___slot_dup) = {2323, 1707, 2324}; 
Line_dup = 1016;Line(Line_dup) = {2228, 1723}; 
CircleArc_dup = 1024;Circle(CircleArc_dup) = {2223, 1707, 1963}; 
Line_dup = 1025;Line(Line_dup) = {1963, 1965}; 
CircleArc_dup = 1027;Circle(CircleArc_dup) = {1965, 1707, 1968}; 
Line_dup = 1028;Line(Line_dup) = {1968, 1970}; 
CircleArc_dup = 1030;Circle(CircleArc_dup) = {1970, 1707, 2224}; 
Line_dup = 1034;Line(Line_dup) = {2248, 1905}; 
CircleArc_dup = 1042;Circle(CircleArc_dup) = {2243, 1707, 1993}; 
Line_dup = 1043;Line(Line_dup) = {1993, 1995}; 
CircleArc_dup = 1045;Circle(CircleArc_dup) = {1995, 1707, 1998}; 
Line_dup = 1046;Line(Line_dup) = {1998, 2000}; 
CircleArc_dup = 1048;Circle(CircleArc_dup) = {2000, 1707, 2244}; 
Line_dup = 1052;Line(Line_dup) = {2268, 1908}; 
CircleArc_dup = 1060;Circle(CircleArc_dup) = {2263, 1707, 2023}; 
Line_dup = 1061;Line(Line_dup) = {2023, 2025}; 
CircleArc_dup = 1063;Circle(CircleArc_dup) = {2025, 1707, 2028}; 
Line_dup = 1064;Line(Line_dup) = {2028, 2030}; 
CircleArc_dup = 1066;Circle(CircleArc_dup) = {2030, 1707, 2264}; 
Line_dup = 1070;Line(Line_dup) = {2288, 1911}; 
CircleArc_dup = 1078;Circle(CircleArc_dup) = {2283, 1707, 2053}; 
Line_dup = 1079;Line(Line_dup) = {2053, 2055}; 
CircleArc_dup = 1081;Circle(CircleArc_dup) = {2055, 1707, 2058}; 
Line_dup = 1082;Line(Line_dup) = {2058, 2060}; 
CircleArc_dup = 1084;Circle(CircleArc_dup) = {2060, 1707, 2284}; 
Line_dup = 1088;Line(Line_dup) = {2308, 1914}; 
CircleArc_dup = 1096;Circle(CircleArc_dup) = {2303, 1707, 2083}; 
Line_dup = 1097;Line(Line_dup) = {2083, 2085}; 
CircleArc_dup = 1099;Circle(CircleArc_dup) = {2085, 1707, 2088}; 
Line_dup = 1100;Line(Line_dup) = {2088, 2090}; 
CircleArc_dup = 1102;Circle(CircleArc_dup) = {2090, 1707, 2304}; 
CircleArc_dup = 1114;Circle(CircleArc_dup) = {2323, 1707, 2113}; 
Line_dup = 1115;Line(Line_dup) = {2113, 2115}; 
CircleArc_dup = 1117;Circle(CircleArc_dup) = {2115, 1707, 2118}; 
Line_dup = 1118;Line(Line_dup) = {2118, 2120}; 
CircleArc_dup = 1120;Circle(CircleArc_dup) = {2120, 1707, 2324}; 
CircleArc_dup = 1125;Circle(CircleArc_dup) = {1963, 1707, 1970}; 
CircleArc_dup = 1131;Circle(CircleArc_dup) = {1993, 1707, 2000}; 
CircleArc_dup = 1137;Circle(CircleArc_dup) = {2023, 1707, 2030}; 
CircleArc_dup = 1143;Circle(CircleArc_dup) = {2053, 1707, 2060}; 
CircleArc_dup = 1149;Circle(CircleArc_dup) = {2083, 1707, 2090}; 
CircleArc_dup = 1155;Circle(CircleArc_dup) = {2113, 1707, 2120}; 

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
