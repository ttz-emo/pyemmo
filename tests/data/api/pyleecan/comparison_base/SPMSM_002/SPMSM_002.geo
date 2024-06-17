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
PointM21 = 972; Point(972) = {0.0274, 0, 0, 0.0001999999999999988*gmsf};
PointM22 = 973; Point(973) = {1.677766114831874e-18, 0.0274, 0, 0.0001999999999999988*gmsf};
centerPointBand = 957; Point(957) = {0, 0, 0, 0.001*gmsf};
PointM22_dup = 1014; Point(1014) = {-0.0274, 3.355532229663748e-18, 0.0, 0.0001999999999999988*gmsf};
PointM22_dup = 1017; Point(1017) = {-5.033298344495622e-18, -0.0274, 0.0, 0.0001999999999999988*gmsf};
PointM11_dup = 1448; Point(1448) = {0.0272, 0, 0, 0.0002423357664233563*gmsf};
PointM12_dup = 1450; Point(1450) = {1.6655196468404003e-18, 0.0272, 0, 0.0002423357664233563*gmsf};
PointM12_dup = 1460; Point(1460) = {-0.0272, 3.3310392936808006e-18, 0.0, 0.0002423357664233563*gmsf};
PointM12_dup = 1470; Point(1470) = {-4.9965589405212005e-18, -0.0272, 0.0, 0.0002423357664233563*gmsf};
point_pylc_dup = 1088; Point(1088) = {0.019861369165220435, 0.0023507477284538635, 0, 0.0017664233576642231*gmsf};
point_pylc_dup = 1089; Point(1089) = {0.026812848373047583, 0.003173509433412717, 0, 0.0002846715328467138*gmsf};
point_pylc_dup = 1092; Point(1092) = {0.003173509433412717, 0.026812848373047583, 0, 0.0002846715328467138*gmsf};
point_pylc_dup = 1094; Point(1094) = {0.0023507477284538635, 0.019861369165220435, 0, 0.0017664233576642231*gmsf};
point_pylc_dup = 1098; Point(1098) = {-0.002350747728453862, 0.019861369165220435, 0.0, 0.0017664233576642231*gmsf};
point_pylc_dup = 1099; Point(1099) = {-0.003173509433412715, 0.026812848373047583, 0.0, 0.0002846715328467138*gmsf};
point_pylc_dup = 1102; Point(1102) = {-0.026812848373047583, 0.0031735094334127186, 0.0, 0.0002846715328467138*gmsf};
point_pylc_dup = 1104; Point(1104) = {-0.019861369165220435, 0.0023507477284538648, 0.0, 0.0017664233576642231*gmsf};
point_pylc_dup = 1108; Point(1108) = {-0.019861369165220435, -0.002350747728453861, 0.0, 0.0017664233576642231*gmsf};
point_pylc_dup = 1109; Point(1109) = {-0.026812848373047583, -0.0031735094334127134, 0.0, 0.0002846715328467138*gmsf};
point_pylc_dup = 1112; Point(1112) = {-0.0031735094334127203, -0.026812848373047583, 0.0, 0.0002846715328467138*gmsf};
point_pylc_dup = 1114; Point(1114) = {-0.002350747728453866, -0.019861369165220435, 0.0, 0.0017664233576642231*gmsf};
point_pylc_dup = 1118; Point(1118) = {0.00235074772845386, -0.019861369165220435, 0.0, 0.0017664233576642231*gmsf};
point_pylc_dup = 1119; Point(1119) = {0.003173509433412712, -0.026812848373047583, 0.0, 0.0002846715328467138*gmsf};
point_pylc_dup = 1122; Point(1122) = {0.026812848373047583, -0.0031735094334127216, 0.0, 0.0002846715328467138*gmsf};
point_pylc_dup = 1124; Point(1124) = {0.019861369165220435, -0.002350747728453867, 0.0, 0.0017664233576642231*gmsf};
point_pylc_dup = 1368; Point(1368) = {0.02, 0.0, 0, 0.0017664233576642231*gmsf};
point_pylc_dup = 1373; Point(1373) = {1.2246467991473532e-18, 0.02, 0, 0.0017664233576642231*gmsf};
point_pylc_dup = 1393; Point(1393) = {-0.02, 2.4492935982947064e-18, 0.0, 0.0017664233576642231*gmsf};
point_pylc_dup = 1413; Point(1413) = {-3.673940397442059e-18, -0.02, 0.0, 0.0017664233576642231*gmsf};
point_pylc = 861; Point(861) = {0.02500000000000001, 0.04330127018922193, 0, 0.0024999999999999996*gmsf};
point_pylc = 862; Point(862) = {0.05, 0.0, 0, 0.0024999999999999996*gmsf};
point_pylc_dup = 1021; Point(1021) = {-0.02499999999999999, 0.043301270189221946, 0.0, 0.0024999999999999996*gmsf};
point_pylc_dup = 1024; Point(1024) = {-0.05, 1.734723475976807e-17, 0.0, 0.0024999999999999996*gmsf};
point_pylc_dup = 1027; Point(1027) = {-0.025000000000000015, -0.04330127018922193, 0.0, 0.0024999999999999996*gmsf};
point_pylc_dup = 1030; Point(1030) = {0.024999999999999977, -0.04330127018922196, 0.0, 0.0024999999999999996*gmsf};
PointM31 = 995; Point(995) = {0.0276, 0, 0, 0.0001999999999999988*gmsf};
PointM32 = 996; Point(996) = {0.013800000000000003, 0.023902301144450504, 0, 0.0001999999999999988*gmsf};
PointM32_dup = 999; Point(999) = {-0.013799999999999993, 0.02390230114445051, 0.0, 0.0001999999999999988*gmsf};
PointM32_dup = 1002; Point(1002) = {-0.0276, 1.0408340855860843e-17, 0.0, 0.0001999999999999988*gmsf};
PointM32_dup = 1005; Point(1005) = {-0.013800000000000007, -0.023902301144450504, 0.0, 0.0001999999999999988*gmsf};
PointM32_dup = 1008; Point(1008) = {0.013799999999999986, -0.023902301144450515, 0.0, 0.0001999999999999988*gmsf};
PointM41_dup = 1608; Point(1608) = {0.027800000000000002, 0, 0, 0.00022053571428571326*gmsf};
PointM42_dup = 1610; Point(1610) = {0.013900000000000004, 0.024075506225207394, 0, 0.00022053571428571326*gmsf};
PointM42_dup = 1620; Point(1620) = {-0.013899999999999996, 0.0240755062252074, 0.0, 0.00022053571428571326*gmsf};
PointM42_dup = 1630; Point(1630) = {-0.0278, 1.0408340855860843e-17, 0.0, 0.0002205357142857129*gmsf};
PointM42_dup = 1640; Point(1640) = {-0.013900000000000008, -0.024075506225207394, 0.0, 0.00022053571428571326*gmsf};
PointM42_dup = 1650; Point(1650) = {0.013899999999999989, -0.024075506225207405, 0.0, 0.00022053571428571326*gmsf};
point_pylc_dup = 1488; Point(1488) = {0.028, 0.0, 0, 0.00024107142857142738*gmsf};
point_pylc_dup = 1490; Point(1490) = {0.025579272813991007, 0.011388626006126492, 0, 0.00024107142857142738*gmsf};
point_pylc_dup = 1492; Point(1492) = {0.027406363729276077, 0.012202099292278383, 0, 0.0004464285714285699*gmsf};
point_pylc_dup = 1493; Point(1493) = {0.02427050983125124, 0.017633557568770313, 0, 0.0004464285714285699*gmsf};
point_pylc_dup = 1494; Point(1494) = {0.02265247584250116, 0.01645798706418563, 0, 0.00024107142857142738*gmsf};
point_pylc_dup = 1497; Point(1497) = {0.014000000000000004, 0.02424871130596428, 0, 0.00024107142857142738*gmsf};
point_pylc_dup = 1510; Point(1510) = {0.0029267969714898527, 0.02784661307031212, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 1512; Point(1512) = {0.003135853898024843, 0.0298356568610487, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 1513; Point(1513) = {-0.003135853898024831, 0.0298356568610487, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 1514; Point(1514) = {-0.002926796971489844, 0.027846613070312123, 0.0, 0.00024107142857142773*gmsf};
point_pylc_dup = 1517; Point(1517) = {-0.013999999999999995, 0.024248711305964288, 0.0, 0.000241071428571427*gmsf};
point_pylc_dup = 1530; Point(1530) = {-0.022652475842501154, 0.016457987064185633, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 1532; Point(1532) = {-0.02427050983125123, 0.01763355756877032, 0.0, 0.0004464285714285695*gmsf};
point_pylc_dup = 1533; Point(1533) = {-0.027406363729276073, 0.012202099292278392, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 1534; Point(1534) = {-0.025579272813991003, 0.011388626006126501, 0.0, 0.000241071428571427*gmsf};
point_pylc_dup = 1537; Point(1537) = {-0.028, 1.0408340855860843e-17, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 1550; Point(1550) = {-0.025579272813991007, -0.011388626006126489, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 1552; Point(1552) = {-0.027406363729276077, -0.01220209929227838, 0.0, 0.0004464285714285695*gmsf};
point_pylc_dup = 1553; Point(1553) = {-0.024270509831251244, -0.01763355756877031, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 1554; Point(1554) = {-0.022652475842501164, -0.016457987064185626, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 1557; Point(1557) = {-0.014000000000000007, -0.02424871130596428, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 1570; Point(1570) = {-0.002926796971489863, -0.027846613070312123, 0.0, 0.00024107142857142773*gmsf};
point_pylc_dup = 1572; Point(1572) = {-0.0031358538980248533, -0.0298356568610487, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 1573; Point(1573) = {0.0031358538980248204, -0.029835656861048703, 0.0, 0.0004464285714285703*gmsf};
point_pylc_dup = 1574; Point(1574) = {0.0029267969714898336, -0.027846613070312127, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 1577; Point(1577) = {0.013999999999999986, -0.024248711305964295, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 1590; Point(1590) = {0.022652475842501144, -0.01645798706418565, 0.0, 0.00024107142857142773*gmsf};
point_pylc_dup = 1592; Point(1592) = {0.024270509831251223, -0.017633557568770334, 0.0, 0.0004464285714285695*gmsf};
point_pylc_dup = 1593; Point(1593) = {0.027406363729276066, -0.012202099292278407, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 1594; Point(1594) = {0.025579272813991, -0.011388626006126515, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 1142; Point(1142) = {0.028977774788670887, 0.007764571353079951, 0, 0.0004464285714285699*gmsf};
point_pylc_dup = 1144; Point(1144) = {0.03863703305156119, 0.010352761804106601, 0, 0.0014732142857142847*gmsf};
point_pylc_dup = 1147; Point(1147) = {0.02828427124746613, 0.028284271247457672, 0, 0.0014732142857142847*gmsf};
point_pylc_dup = 1149; Point(1149) = {0.021213203435599598, 0.021213203435593256, 0, 0.0004464285714285703*gmsf};
point_pylc_dup = 1172; Point(1172) = {0.0077645713530712975, 0.028977774788673204, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 1174; Point(1174) = {0.010352761804095065, 0.038637033051564275, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 1177; Point(1177) = {-0.01035276180409505, 0.03863703305156428, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 1179; Point(1179) = {-0.007764571353071287, 0.028977774788673215, 0.0, 0.0004464285714285703*gmsf};
point_pylc_dup = 1202; Point(1202) = {-0.021213203435599588, 0.02121320343559326, 0.0, 0.0004464285714285695*gmsf};
point_pylc_dup = 1204; Point(1204) = {-0.02828427124746612, 0.028284271247457683, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 1207; Point(1207) = {-0.03863703305156118, 0.010352761804106617, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 1209; Point(1209) = {-0.028977774788670883, 0.007764571353079961, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 1232; Point(1232) = {-0.028977774788670887, -0.007764571353079948, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 1234; Point(1234) = {-0.03863703305156119, -0.010352761804106596, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 1237; Point(1237) = {-0.028284271247466134, -0.02828427124745767, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 1239; Point(1239) = {-0.0212132034355996, -0.021213203435593252, 0.0, 0.0004464285714285703*gmsf};
point_pylc_dup = 1262; Point(1262) = {-0.007764571353071307, -0.028977774788673204, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 1264; Point(1264) = {-0.01035276180409508, -0.03863703305156428, 0.0, 0.0014732142857142854*gmsf};
point_pylc_dup = 1267; Point(1267) = {0.010352761804095037, -0.03863703305156429, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 1269; Point(1269) = {0.00776457135307128, -0.028977774788673215, 0.0, 0.0004464285714285703*gmsf};
point_pylc_dup = 1292; Point(1292) = {0.021213203435599577, -0.021213203435593273, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 1294; Point(1294) = {0.028284271247466106, -0.0282842712474577, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 1297; Point(1297) = {0.03863703305156117, -0.01035276180410664, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 1299; Point(1299) = {0.028977774788670883, -0.007764571353079976, 0.0, 0.0004464285714285703*gmsf};

// Lines and Curves
MB_CurveRotor = 487;Circle(MB_CurveRotor) = {972, 957, 973}; 
MB_CurveRotor_dup = 509;Circle(MB_CurveRotor_dup) = {973, 957, 1014}; 
MB_CurveRotor_dup = 511;Circle(MB_CurveRotor_dup) = {1014, 957, 1017}; 
MB_CurveRotor_dup = 513;Circle(MB_CurveRotor_dup) = {1017, 957, 972}; 
rotorBand1_dup = 773;Circle(rotorBand1_dup) = {1448, 957, 1450}; 
lowerLine2_dup = 776;Line(lowerLine2_dup) = {1448, 972}; 
upperLine2_dup = 777;Line(upperLine2_dup) = {1450, 973}; 
rotorBand1_dup = 779;Circle(rotorBand1_dup) = {1450, 957, 1460}; 
upperLine2_dup = 783;Line(upperLine2_dup) = {1460, 1014}; 
rotorBand1_dup = 785;Circle(rotorBand1_dup) = {1460, 957, 1470}; 
upperLine2_dup = 789;Line(upperLine2_dup) = {1470, 1017}; 
rotorBand1_dup = 791;Circle(rotorBand1_dup) = {1470, 957, 1448}; 
Line_dup = 556;Line(Line_dup) = {1088, 1089}; 
CircleArc_dup = 558;Circle(CircleArc_dup) = {1089, 957, 1092}; 
Line_dup = 559;Line(Line_dup) = {1092, 1094}; 
CircleArc_dup = 561;Circle(CircleArc_dup) = {1094, 957, 1088}; 
Line_dup = 562;Line(Line_dup) = {1098, 1099}; 
CircleArc_dup = 564;Circle(CircleArc_dup) = {1099, 957, 1102}; 
Line_dup = 565;Line(Line_dup) = {1102, 1104}; 
CircleArc_dup = 567;Circle(CircleArc_dup) = {1104, 957, 1098}; 
Line_dup = 568;Line(Line_dup) = {1108, 1109}; 
CircleArc_dup = 570;Circle(CircleArc_dup) = {1109, 957, 1112}; 
Line_dup = 571;Line(Line_dup) = {1112, 1114}; 
CircleArc_dup = 573;Circle(CircleArc_dup) = {1114, 957, 1108}; 
Line_dup = 574;Line(Line_dup) = {1118, 1119}; 
CircleArc_dup = 576;Circle(CircleArc_dup) = {1119, 957, 1122}; 
Line_dup = 577;Line(Line_dup) = {1122, 1124}; 
CircleArc_dup = 579;Circle(CircleArc_dup) = {1124, 957, 1118}; 
CircleArc_dup = 725;Circle(CircleArc_dup) = {1368, 957, 1088}; 
CircleArc_dup = 727;Circle(CircleArc_dup) = {1094, 957, 1373}; 
lowerLine1_dup = 734;Line(lowerLine1_dup) = {1368, 1448}; 
upperLine1_dup = 735;Line(upperLine1_dup) = {1373, 1450}; 
CircleArc_dup = 737;Circle(CircleArc_dup) = {1373, 957, 1098}; 
CircleArc_dup = 739;Circle(CircleArc_dup) = {1104, 957, 1393}; 
upperLine1_dup = 747;Line(upperLine1_dup) = {1393, 1460}; 
CircleArc_dup = 749;Circle(CircleArc_dup) = {1393, 957, 1108}; 
CircleArc_dup = 751;Circle(CircleArc_dup) = {1114, 957, 1413}; 
upperLine1_dup = 759;Line(upperLine1_dup) = {1413, 1470}; 
CircleArc_dup = 761;Circle(CircleArc_dup) = {1413, 957, 1118}; 
CircleArc_dup = 763;Circle(CircleArc_dup) = {1124, 957, 1368}; 
Line_dup = 524;Line(Line_dup) = {957, 1368}; 
Line_dup = 531;Line(Line_dup) = {1373, 957}; 
Line_dup = 539;Line(Line_dup) = {1393, 957}; 
Line_dup = 547;Line(Line_dup) = {1413, 957}; 
OuterLimit = 458;Circle(OuterLimit) = {861, 957, 862}; 
OuterLimit_dup = 515;Circle(OuterLimit_dup) = {1021, 957, 861}; 
OuterLimit_dup = 517;Circle(OuterLimit_dup) = {1024, 957, 1021}; 
OuterLimit_dup = 519;Circle(OuterLimit_dup) = {1027, 957, 1024}; 
OuterLimit_dup = 521;Circle(OuterLimit_dup) = {1030, 957, 1027}; 
OuterLimit_dup = 523;Circle(OuterLimit_dup) = {862, 957, 1030}; 
MB_CurveStator = 495;Circle(MB_CurveStator) = {995, 957, 996}; 
MB_CurveStator_dup = 499;Circle(MB_CurveStator_dup) = {996, 957, 999}; 
MB_CurveStator_dup = 501;Circle(MB_CurveStator_dup) = {999, 957, 1002}; 
MB_CurveStator_dup = 503;Circle(MB_CurveStator_dup) = {1002, 957, 1005}; 
MB_CurveStator_dup = 505;Circle(MB_CurveStator_dup) = {1005, 957, 1008}; 
MB_CurveStator_dup = 507;Circle(MB_CurveStator_dup) = {1008, 957, 995}; 
statorCircle4_dup = 869;Circle(statorCircle4_dup) = {1608, 957, 1610}; 
lowerLine3_dup = 872;Line(lowerLine3_dup) = {995, 1608}; 
upperLine3_dup = 873;Line(upperLine3_dup) = {996, 1610}; 
statorCircle4_dup = 875;Circle(statorCircle4_dup) = {1610, 957, 1620}; 
upperLine3_dup = 879;Line(upperLine3_dup) = {999, 1620}; 
statorCircle4_dup = 881;Circle(statorCircle4_dup) = {1620, 957, 1630}; 
upperLine3_dup = 885;Line(upperLine3_dup) = {1002, 1630}; 
statorCircle4_dup = 887;Circle(statorCircle4_dup) = {1630, 957, 1640}; 
upperLine3_dup = 891;Line(upperLine3_dup) = {1005, 1640}; 
statorCircle4_dup = 893;Circle(statorCircle4_dup) = {1640, 957, 1650}; 
upperLine3_dup = 897;Line(upperLine3_dup) = {1008, 1650}; 
statorCircle4_dup = 899;Circle(statorCircle4_dup) = {1650, 957, 1608}; 
CircleArc_dup = 797;Circle(CircleArc_dup) = {1488, 957, 1490}; 
Line_dup = 798;Line(Line_dup) = {1490, 1492}; 
Line_dup = 799;Line(Line_dup) = {1493, 1494}; 
CircleArc_dup = 801;Circle(CircleArc_dup) = {1494, 957, 1497}; 
interface_line_slot_opening___slot_dup = 803;Circle(interface_line_slot_opening___slot_dup) = {1492, 957, 1493}; 
lowerLine4_dup = 806;Line(lowerLine4_dup) = {1488, 1608}; 
upperLine4_dup = 807;Line(upperLine4_dup) = {1497, 1610}; 
CircleArc_dup = 809;Circle(CircleArc_dup) = {1497, 957, 1510}; 
Line_dup = 810;Line(Line_dup) = {1510, 1512}; 
Line_dup = 811;Line(Line_dup) = {1513, 1514}; 
CircleArc_dup = 813;Circle(CircleArc_dup) = {1514, 957, 1517}; 
interface_line_slot_opening___slot_dup = 815;Circle(interface_line_slot_opening___slot_dup) = {1512, 957, 1513}; 
upperLine4_dup = 819;Line(upperLine4_dup) = {1517, 1620}; 
CircleArc_dup = 821;Circle(CircleArc_dup) = {1517, 957, 1530}; 
Line_dup = 822;Line(Line_dup) = {1530, 1532}; 
Line_dup = 823;Line(Line_dup) = {1533, 1534}; 
CircleArc_dup = 825;Circle(CircleArc_dup) = {1534, 957, 1537}; 
interface_line_slot_opening___slot_dup = 827;Circle(interface_line_slot_opening___slot_dup) = {1532, 957, 1533}; 
upperLine4_dup = 831;Line(upperLine4_dup) = {1537, 1630}; 
CircleArc_dup = 833;Circle(CircleArc_dup) = {1537, 957, 1550}; 
Line_dup = 834;Line(Line_dup) = {1550, 1552}; 
Line_dup = 835;Line(Line_dup) = {1553, 1554}; 
CircleArc_dup = 837;Circle(CircleArc_dup) = {1554, 957, 1557}; 
interface_line_slot_opening___slot_dup = 839;Circle(interface_line_slot_opening___slot_dup) = {1552, 957, 1553}; 
upperLine4_dup = 843;Line(upperLine4_dup) = {1557, 1640}; 
CircleArc_dup = 845;Circle(CircleArc_dup) = {1557, 957, 1570}; 
Line_dup = 846;Line(Line_dup) = {1570, 1572}; 
Line_dup = 847;Line(Line_dup) = {1573, 1574}; 
CircleArc_dup = 849;Circle(CircleArc_dup) = {1574, 957, 1577}; 
interface_line_slot_opening___slot_dup = 851;Circle(interface_line_slot_opening___slot_dup) = {1572, 957, 1573}; 
upperLine4_dup = 855;Line(upperLine4_dup) = {1577, 1650}; 
CircleArc_dup = 857;Circle(CircleArc_dup) = {1577, 957, 1590}; 
Line_dup = 858;Line(Line_dup) = {1590, 1592}; 
Line_dup = 859;Line(Line_dup) = {1593, 1594}; 
CircleArc_dup = 861;Circle(CircleArc_dup) = {1594, 957, 1488}; 
interface_line_slot_opening___slot_dup = 863;Circle(interface_line_slot_opening___slot_dup) = {1592, 957, 1593}; 
Line_dup = 580;Line(Line_dup) = {1497, 861}; 
Line_dup = 583;Line(Line_dup) = {862, 1488}; 
CircleArc_dup = 588;Circle(CircleArc_dup) = {1492, 957, 1142}; 
Line_dup = 589;Line(Line_dup) = {1142, 1144}; 
CircleArc_dup = 591;Circle(CircleArc_dup) = {1144, 957, 1147}; 
Line_dup = 592;Line(Line_dup) = {1147, 1149}; 
CircleArc_dup = 594;Circle(CircleArc_dup) = {1149, 957, 1493}; 
Line_dup = 598;Line(Line_dup) = {1517, 1021}; 
CircleArc_dup = 606;Circle(CircleArc_dup) = {1512, 957, 1172}; 
Line_dup = 607;Line(Line_dup) = {1172, 1174}; 
CircleArc_dup = 609;Circle(CircleArc_dup) = {1174, 957, 1177}; 
Line_dup = 610;Line(Line_dup) = {1177, 1179}; 
CircleArc_dup = 612;Circle(CircleArc_dup) = {1179, 957, 1513}; 
Line_dup = 616;Line(Line_dup) = {1537, 1024}; 
CircleArc_dup = 624;Circle(CircleArc_dup) = {1532, 957, 1202}; 
Line_dup = 625;Line(Line_dup) = {1202, 1204}; 
CircleArc_dup = 627;Circle(CircleArc_dup) = {1204, 957, 1207}; 
Line_dup = 628;Line(Line_dup) = {1207, 1209}; 
CircleArc_dup = 630;Circle(CircleArc_dup) = {1209, 957, 1533}; 
Line_dup = 634;Line(Line_dup) = {1557, 1027}; 
CircleArc_dup = 642;Circle(CircleArc_dup) = {1552, 957, 1232}; 
Line_dup = 643;Line(Line_dup) = {1232, 1234}; 
CircleArc_dup = 645;Circle(CircleArc_dup) = {1234, 957, 1237}; 
Line_dup = 646;Line(Line_dup) = {1237, 1239}; 
CircleArc_dup = 648;Circle(CircleArc_dup) = {1239, 957, 1553}; 
Line_dup = 652;Line(Line_dup) = {1577, 1030}; 
CircleArc_dup = 660;Circle(CircleArc_dup) = {1572, 957, 1262}; 
Line_dup = 661;Line(Line_dup) = {1262, 1264}; 
CircleArc_dup = 663;Circle(CircleArc_dup) = {1264, 957, 1267}; 
Line_dup = 664;Line(Line_dup) = {1267, 1269}; 
CircleArc_dup = 666;Circle(CircleArc_dup) = {1269, 957, 1573}; 
CircleArc_dup = 678;Circle(CircleArc_dup) = {1592, 957, 1292}; 
Line_dup = 679;Line(Line_dup) = {1292, 1294}; 
CircleArc_dup = 681;Circle(CircleArc_dup) = {1294, 957, 1297}; 
Line_dup = 682;Line(Line_dup) = {1297, 1299}; 
CircleArc_dup = 684;Circle(CircleArc_dup) = {1299, 957, 1593}; 
CircleArc_dup = 689;Circle(CircleArc_dup) = {1142, 957, 1149}; 
CircleArc_dup = 695;Circle(CircleArc_dup) = {1172, 957, 1179}; 
CircleArc_dup = 701;Circle(CircleArc_dup) = {1202, 957, 1209}; 
CircleArc_dup = 707;Circle(CircleArc_dup) = {1232, 957, 1239}; 
CircleArc_dup = 713;Circle(CircleArc_dup) = {1262, 957, 1269}; 
CircleArc_dup = 719;Circle(CircleArc_dup) = {1292, 957, 1299}; 

// Surfaces

Curve Loop(82) = {773,777,-487,-776};
Surf_rotorAirGap2_dup = {82};
Plane Surface(Surf_rotorAirGap2_dup) = {82};

Curve Loop(83) = {779,783,-509,-777};
Surf_rotorAirGap2_dup = {83};
Plane Surface(Surf_rotorAirGap2_dup) = {83};

Curve Loop(84) = {785,789,-511,-783};
Surf_rotorAirGap2_dup = {84};
Plane Surface(Surf_rotorAirGap2_dup) = {84};

Curve Loop(85) = {791,776,-513,-789};
Surf_rotorAirGap2_dup = {85};
Plane Surface(Surf_rotorAirGap2_dup) = {85};

Curve Loop(62) = {556,558,559,561};
Surf_Magnet_dup = {62};
Plane Surface(Surf_Magnet_dup) = {62};

Curve Loop(63) = {562,564,565,567};
Surf_Magnet_dup = {63};
Plane Surface(Surf_Magnet_dup) = {63};

Curve Loop(64) = {568,570,571,573};
Surf_Magnet_dup = {64};
Plane Surface(Surf_Magnet_dup) = {64};

Curve Loop(65) = {574,576,577,579};
Surf_Magnet_dup = {65};
Plane Surface(Surf_Magnet_dup) = {65};

Curve Loop(78) = {725,556,558,559,727,735,-773,-734};
Surf_rotorAirGap1_dup = {78};
Plane Surface(Surf_rotorAirGap1_dup) = {78};

Curve Loop(79) = {737,562,564,565,739,747,-779,-735};
Surf_rotorAirGap1_dup = {79};
Plane Surface(Surf_rotorAirGap1_dup) = {79};

Curve Loop(80) = {749,568,570,571,751,759,-785,-747};
Surf_rotorAirGap1_dup = {80};
Plane Surface(Surf_rotorAirGap1_dup) = {80};

Curve Loop(81) = {761,574,576,577,763,734,-791,-759};
Surf_rotorAirGap1_dup = {81};
Plane Surface(Surf_rotorAirGap1_dup) = {81};

Curve Loop(58) = {524,725,-561,727,531};
Surf_Rotorblech_dup = {58};
Plane Surface(Surf_Rotorblech_dup) = {58};

Curve Loop(59) = {531,-539,-739,567,-737};
Surf_Rotorblech_dup = {59};
Plane Surface(Surf_Rotorblech_dup) = {59};

Curve Loop(60) = {539,-547,-751,573,-749};
Surf_Rotorblech_dup = {60};
Plane Surface(Surf_Rotorblech_dup) = {60};

Curve Loop(61) = {547,524,-763,579,-761};
Surf_Rotorblech_dup = {61};
Plane Surface(Surf_Rotorblech_dup) = {61};

Curve Loop(92) = {869,-873,-495,872};
Surf_statorAirGap2_dup = {92};
Plane Surface(Surf_statorAirGap2_dup) = {92};

Curve Loop(93) = {875,-879,-499,873};
Surf_statorAirGap2_dup = {93};
Plane Surface(Surf_statorAirGap2_dup) = {93};

Curve Loop(94) = {881,-885,-501,879};
Surf_statorAirGap2_dup = {94};
Plane Surface(Surf_statorAirGap2_dup) = {94};

Curve Loop(95) = {887,-891,-503,885};
Surf_statorAirGap2_dup = {95};
Plane Surface(Surf_statorAirGap2_dup) = {95};

Curve Loop(96) = {893,-897,-505,891};
Surf_statorAirGap2_dup = {96};
Plane Surface(Surf_statorAirGap2_dup) = {96};

Curve Loop(97) = {899,-872,-507,897};
Surf_statorAirGap2_dup = {97};
Plane Surface(Surf_statorAirGap2_dup) = {97};

Curve Loop(86) = {797,798,803,799,801,807,-869,-806};
Surf_statorAirGap1_dup = {86};
Plane Surface(Surf_statorAirGap1_dup) = {86};

Curve Loop(87) = {809,810,815,811,813,819,-875,-807};
Surf_statorAirGap1_dup = {87};
Plane Surface(Surf_statorAirGap1_dup) = {87};

Curve Loop(88) = {821,822,827,823,825,831,-881,-819};
Surf_statorAirGap1_dup = {88};
Plane Surface(Surf_statorAirGap1_dup) = {88};

Curve Loop(89) = {833,834,839,835,837,843,-887,-831};
Surf_statorAirGap1_dup = {89};
Plane Surface(Surf_statorAirGap1_dup) = {89};

Curve Loop(90) = {845,846,851,847,849,855,-893,-843};
Surf_statorAirGap1_dup = {90};
Plane Surface(Surf_statorAirGap1_dup) = {90};

Curve Loop(91) = {857,858,863,859,861,806,-899,-855};
Surf_statorAirGap1_dup = {91};
Plane Surface(Surf_statorAirGap1_dup) = {91};

Curve Loop(66) = {580,458,583,797,798,588,589,591,592,594,799,801};
Surf_Statorblech_dup = {66};
Plane Surface(Surf_Statorblech_dup) = {66};

Curve Loop(67) = {598,515,-580,809,810,606,607,609,610,612,811,813};
Surf_Statorblech_dup = {67};
Plane Surface(Surf_Statorblech_dup) = {67};

Curve Loop(68) = {616,517,-598,821,822,624,625,627,628,630,823,825};
Surf_Statorblech_dup = {68};
Plane Surface(Surf_Statorblech_dup) = {68};

Curve Loop(69) = {634,519,-616,833,834,642,643,645,646,648,835,837};
Surf_Statorblech_dup = {69};
Plane Surface(Surf_Statorblech_dup) = {69};

Curve Loop(70) = {652,521,-634,845,846,660,661,663,664,666,847,849};
Surf_Statorblech_dup = {70};
Plane Surface(Surf_Statorblech_dup) = {70};

Curve Loop(71) = {583,-861,-859,-684,-682,-681,-679,-678,-858,-857,652,-523};
Surf_Statorblech_dup = {71};
Plane Surface(Surf_Statorblech_dup) = {71};

Curve Loop(72) = {689,-592,-591,-589};
Surf_Stator_Nut_dup = {72};
Plane Surface(Surf_Stator_Nut_dup) = {72};

Curve Loop(73) = {695,-610,-609,-607};
Surf_Stator_Nut_dup = {73};
Plane Surface(Surf_Stator_Nut_dup) = {73};

Curve Loop(74) = {701,-628,-627,-625};
Surf_Stator_Nut_dup = {74};
Plane Surface(Surf_Stator_Nut_dup) = {74};

Curve Loop(75) = {707,-646,-645,-643};
Surf_Stator_Nut_dup = {75};
Plane Surface(Surf_Stator_Nut_dup) = {75};

Curve Loop(76) = {713,-664,-663,-661};
Surf_Stator_Nut_dup = {76};
Plane Surface(Surf_Stator_Nut_dup) = {76};

Curve Loop(77) = {719,-682,-681,-679};
Surf_Stator_Nut_dup = {77};
Plane Surface(Surf_Stator_Nut_dup) = {77};

// Color code
If (!Flag_individualColoring)
Color SkyBlue {Surface {82}; }
Color SkyBlue {Surface {83}; }
Color SkyBlue {Surface {84}; }
Color SkyBlue {Surface {85}; }
Color Red {Surface {62}; }
Color Green {Surface {63}; }
Color Red {Surface {64}; }
Color Green {Surface {65}; }
Color SkyBlue {Surface {78}; }
Color SkyBlue {Surface {79}; }
Color SkyBlue {Surface {80}; }
Color SkyBlue {Surface {81}; }
Color SteelBlue {Surface {58}; }
Color SteelBlue {Surface {59}; }
Color SteelBlue {Surface {60}; }
Color SteelBlue {Surface {61}; }
Color SkyBlue {Surface {92}; }
Color SkyBlue {Surface {93}; }
Color SkyBlue {Surface {94}; }
Color SkyBlue {Surface {95}; }
Color SkyBlue {Surface {96}; }
Color SkyBlue {Surface {97}; }
Color SkyBlue {Surface {86}; }
Color SkyBlue {Surface {87}; }
Color SkyBlue {Surface {88}; }
Color SkyBlue {Surface {89}; }
Color SkyBlue {Surface {90}; }
Color SkyBlue {Surface {91}; }
Color SteelBlue4 {Surface {66}; }
Color SteelBlue4 {Surface {67}; }
Color SteelBlue4 {Surface {68}; }
Color SteelBlue4 {Surface {69}; }
Color SteelBlue4 {Surface {70}; }
Color SteelBlue4 {Surface {71}; }
Color Magenta {Surface {72}; }
Color Magenta {Surface {73}; }
Color Cyan {Surface {74}; }
Color Cyan {Surface {75}; }
Color Yellow4 {Surface {76}; }
Color Yellow4 {Surface {77}; }
EndIf

// Physical Elements
// Rotor_Bnd_MB_1
Physical Curve("Rotor_Bnd_MB_1", 3) = {487,509,511,513};
// LuR2
Physical Surface("LuR2", 18) = {82,83,84,85};
// Mag0_0
Physical Surface("Mag0_0", 6) = {62};
// Mag0_1
Physical Surface("Mag0_1", 7) = {63};
// Mag0_2
Physical Surface("Mag0_2", 8) = {64};
// Mag0_3
Physical Surface("Mag0_3", 9) = {65};
// LuR1
Physical Surface("LuR1", 17) = {78,79,80,81};
// Pol
Physical Surface("Pol", 5) = {58,59,60,61};
// outerLimit
Physical Curve("outerLimit", 4) = {458,515,517,519,521,523};
// mbStator
Physical Curve("mbStator", 2) = {495,499,501,503,505,507};
// StLu2
Physical Surface("StLu2", 20) = {92,93,94,95,96,97};
// StLu1
Physical Surface("StLu1", 19) = {86,87,88,89,90,91};
// StNut
Physical Surface("StNut", 10) = {66,67,68,69,70,71};
// StCu0_0_Up
Physical Surface("StCu0_0_Up", 11) = {72};
// StCu0_1_Un
Physical Surface("StCu0_1_Un", 12) = {73};
// StCu0_2_Wp
Physical Surface("StCu0_2_Wp", 13) = {74};
// StCu0_3_Wn
Physical Surface("StCu0_3_Wn", 14) = {75};
// StCu0_4_Vp
Physical Surface("StCu0_4_Vp", 15) = {76};
// StCu0_5_Vn
Physical Surface("StCu0_5_Vn", 16) = {77};

DefineConstant[
	mm = 1e-3,
	Flag_SpecifyMeshSize = {0, Name StrCat[INPUT_MESH, "04User defined surface mesh sizes"],Choices {0, 1}}
];
If(Flag_SpecifyMeshSize)
	DefineConstant[
		Mag_msf = {1.02, Name StrCat[INPUT_MESH, "05Mesh Size/Magnet [mm]"],Min 0.10200000000000001, Max 10.2, Step 0.1,Visible Flag_SpecifyMeshSize},
		Pol_msf = {1.613, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorblech [mm]"],Min 0.1613, Max 16.13, Step 0.1,Visible Flag_SpecifyMeshSize},
		LuR_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorluftspalt [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		LuR1_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorluftspalt 1 [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		LuR2_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorluftspalt 2 [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		StCu_msf = {0.968, Name StrCat[INPUT_MESH, "05Mesh Size/Stator-Nut [mm]"],Min 0.0968, Max 9.68, Step 0.1,Visible Flag_SpecifyMeshSize},
		StNut_msf = {0.9, Name StrCat[INPUT_MESH, "05Mesh Size/Statorblech [mm]"],Min 0.09, Max 9.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		StLu_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Statorluftspalt [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		StLu1_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Statorluftspalt 1 [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		StLu2_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Statorluftspalt 2 [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize}
	];
	MeshSize { PointsOf {Surface{ 62,63,64,65 };} } = Mag_msf*mm;
	MeshSize { PointsOf {Surface{ 58,59,60,61 };} } = Pol_msf*mm;
	MeshSize { PointsOf {Surface{ 78,79,80,81,82,83,84,85 };} } = LuR_msf*mm;
	MeshSize { PointsOf {Surface{ 78,79,80,81 };} } = LuR1_msf*mm;
	MeshSize { PointsOf {Surface{ 82,83,84,85 };} } = LuR2_msf*mm;
	MeshSize { PointsOf {Surface{ 72,73,74,75,76,77 };} } = StCu_msf*mm;
	MeshSize { PointsOf {Surface{ 66,67,68,69,70,71 };} } = StNut_msf*mm;
	MeshSize { PointsOf {Surface{ 86,87,88,89,90,91,92,93,94,95,96,97 };} } = StLu_msf*mm;
	MeshSize { PointsOf {Surface{ 86,87,88,89,90,91 };} } = StLu1_msf*mm;
	MeshSize { PointsOf {Surface{ 92,93,94,95,96,97 };} } = StLu2_msf*mm;
EndIf

// Mesh operations

// Do not switch mesh algorithm on failure, because this led to mesh errors in the past.
Mesh.AlgorithmSwitchOnFailure = 0;DefineConstant[Flag_CompoundMesh = {0, Name StrCat[INPUT_MESH, "Compound Mesh"], Choices {0,1}, Help "Use Compound Mesh to ignore lines between segments while meshing.",Visible Flag_ExpertMode}];
If (Flag_CompoundMesh)
Compound Surface{58,59,60,61}; // rotor domainLam
Compound Surface{66,67,68,69,70,71}; // stator domainLam
Compound Surface{82,83,84,85}; // rotor airGap
Compound Surface{92,93,94,95,96,97}; // stator airGap
EndIf // (Flag_CompoundMesh)

// Add mesh size setting for Movingband lines
DefineConstant[
	NbrMbSegments = {860.0, Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],Max 1440, Min 180, Step 10, Help "Set the number of mesh segments on the interface between rotor/statorairgap and movingband. Value represents number of segments on whole circle.", Visible Flag_ExpertMode},
	r_MB_R = 0.0274
];
MB_LinesR = {487,509,511,513};
MeshSize{ PointsOf{Line{MB_LinesR[]};}} = 2*Pi*r_MB_R/NbrMbSegments;

MB_LinesS = {495,499,501,503,505,507};
MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*0.0276/NbrMbSegments;

Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)

// Create boundary lines for moving rotor contour plot
rotorBndLines[] = Boundary{ Physical Surface{ 6,7,8,9 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 5 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 18 }; };
statorBndLines[] = Boundary{ Physical Surface{ 2,4,10,11,12,13,14,15,16,19,20 }; };
Physical Line("DomainPlotMovingGeo",1) = {rotorBndLines[], statorBndLines[]}; 
