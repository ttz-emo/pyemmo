// This script was created with pyemmo (Version 1.3.1b1, git 5c6b9b)

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
PointM21 = 5253; Point(5253) = {0.0274, 0, 0, 0.0001999999999999988*gmsf};
PointM22 = 5254; Point(5254) = {1.677766114831874e-18, 0.0274, 0, 0.0001999999999999988*gmsf};
centerPointBand = 5250; Point(5250) = {0, 0, 0, 0.001*gmsf};
PointM22_dup = 5277; Point(5277) = {-0.0274, 3.355532229663748e-18, 0.0, 0.0001999999999999988*gmsf};
PointM22_dup = 5280; Point(5280) = {-5.033298344495622e-18, -0.0274, 0.0, 0.0001999999999999988*gmsf};
PointM11_dup = 5711; Point(5711) = {0.0272, 0, 0, 0.0002423357664233563*gmsf};
PointM12_dup = 5713; Point(5713) = {1.6655196468404003e-18, 0.0272, 0, 0.0002423357664233563*gmsf};
PointM12_dup = 5723; Point(5723) = {-0.0272, 3.3310392936808006e-18, 0.0, 0.0002423357664233563*gmsf};
PointM12_dup = 5733; Point(5733) = {-4.9965589405212005e-18, -0.0272, 0.0, 0.0002423357664233563*gmsf};
point_pylc_dup = 5351; Point(5351) = {0.019861369165220435, 0.0023507477284538635, 0, 0.0017664233576642231*gmsf};
point_pylc_dup = 5352; Point(5352) = {0.026812848373047583, 0.003173509433412717, 0, 0.0002846715328467138*gmsf};
point_pylc_dup = 5355; Point(5355) = {0.003173509433412717, 0.026812848373047583, 0, 0.0002846715328467138*gmsf};
point_pylc_dup = 5357; Point(5357) = {0.0023507477284538635, 0.019861369165220435, 0, 0.0017664233576642231*gmsf};
point_pylc_dup = 5361; Point(5361) = {-0.002350747728453862, 0.019861369165220435, 0.0, 0.0017664233576642231*gmsf};
point_pylc_dup = 5362; Point(5362) = {-0.003173509433412715, 0.026812848373047583, 0.0, 0.0002846715328467138*gmsf};
point_pylc_dup = 5365; Point(5365) = {-0.026812848373047583, 0.0031735094334127186, 0.0, 0.0002846715328467138*gmsf};
point_pylc_dup = 5367; Point(5367) = {-0.019861369165220435, 0.0023507477284538648, 0.0, 0.0017664233576642231*gmsf};
point_pylc_dup = 5371; Point(5371) = {-0.019861369165220435, -0.002350747728453861, 0.0, 0.0017664233576642231*gmsf};
point_pylc_dup = 5372; Point(5372) = {-0.026812848373047583, -0.0031735094334127134, 0.0, 0.0002846715328467138*gmsf};
point_pylc_dup = 5375; Point(5375) = {-0.0031735094334127203, -0.026812848373047583, 0.0, 0.0002846715328467138*gmsf};
point_pylc_dup = 5377; Point(5377) = {-0.002350747728453866, -0.019861369165220435, 0.0, 0.0017664233576642231*gmsf};
point_pylc_dup = 5381; Point(5381) = {0.00235074772845386, -0.019861369165220435, 0.0, 0.0017664233576642231*gmsf};
point_pylc_dup = 5382; Point(5382) = {0.003173509433412712, -0.026812848373047583, 0.0, 0.0002846715328467138*gmsf};
point_pylc_dup = 5385; Point(5385) = {0.026812848373047583, -0.0031735094334127216, 0.0, 0.0002846715328467138*gmsf};
point_pylc_dup = 5387; Point(5387) = {0.019861369165220435, -0.002350747728453867, 0.0, 0.0017664233576642231*gmsf};
lower_rotor_contour_point_dup = 5631; Point(5631) = {0.02, 0.0, 0, 0.0017664233576642231*gmsf};
upper_rotor_contour_point_dup = 5636; Point(5636) = {1.2246467991473532e-18, 0.02, 0, 0.0017664233576642231*gmsf};
upper_rotor_contour_point_dup = 5656; Point(5656) = {-0.02, 2.4492935982947064e-18, 0.0, 0.0017664233576642231*gmsf};
upper_rotor_contour_point_dup = 5676; Point(5676) = {-3.673940397442059e-18, -0.02, 0.0, 0.0017664233576642231*gmsf};
point_pylc = 5204; Point(5204) = {0.02500000000000001, 0.04330127018922193, 0, 0.0024999999999999996*gmsf};
point_pylc = 5205; Point(5205) = {0.05, 0.0, 0, 0.0024999999999999996*gmsf};
point_pylc_dup = 5284; Point(5284) = {-0.02499999999999999, 0.043301270189221946, 0.0, 0.0024999999999999996*gmsf};
point_pylc_dup = 5287; Point(5287) = {-0.05, 1.734723475976807e-17, 0.0, 0.0024999999999999996*gmsf};
point_pylc_dup = 5290; Point(5290) = {-0.025000000000000015, -0.04330127018922193, 0.0, 0.0024999999999999996*gmsf};
point_pylc_dup = 5293; Point(5293) = {0.024999999999999977, -0.04330127018922196, 0.0, 0.0024999999999999996*gmsf};
PointM31 = 5258; Point(5258) = {0.0276, 0, 0, 0.0001999999999999988*gmsf};
PointM32 = 5259; Point(5259) = {0.013800000000000003, 0.023902301144450504, 0, 0.0001999999999999988*gmsf};
PointM32_dup = 5262; Point(5262) = {-0.013799999999999993, 0.02390230114445051, 0.0, 0.0001999999999999988*gmsf};
PointM32_dup = 5265; Point(5265) = {-0.0276, 1.0408340855860843e-17, 0.0, 0.0001999999999999988*gmsf};
PointM32_dup = 5268; Point(5268) = {-0.013800000000000007, -0.023902301144450504, 0.0, 0.0001999999999999988*gmsf};
PointM32_dup = 5271; Point(5271) = {0.013799999999999986, -0.023902301144450515, 0.0, 0.0001999999999999988*gmsf};
PointM41_dup = 5871; Point(5871) = {0.027800000000000002, 0, 0, 0.00022053571428571326*gmsf};
PointM42_dup = 5873; Point(5873) = {0.013900000000000004, 0.024075506225207394, 0, 0.00022053571428571326*gmsf};
PointM42_dup = 5883; Point(5883) = {-0.013899999999999996, 0.0240755062252074, 0.0, 0.00022053571428571326*gmsf};
PointM42_dup = 5893; Point(5893) = {-0.0278, 1.0408340855860843e-17, 0.0, 0.0002205357142857129*gmsf};
PointM42_dup = 5903; Point(5903) = {-0.013900000000000008, -0.024075506225207394, 0.0, 0.00022053571428571326*gmsf};
PointM42_dup = 5913; Point(5913) = {0.013899999999999989, -0.024075506225207405, 0.0, 0.00022053571428571326*gmsf};
point_pylc_dup = 5751; Point(5751) = {0.028, 0.0, 0, 0.00024107142857142738*gmsf};
point_pylc_dup = 5753; Point(5753) = {0.025579272813991007, 0.011388626006126492, 0, 0.00024107142857142738*gmsf};
point_pylc_dup = 5755; Point(5755) = {0.027406363729276077, 0.012202099292278383, 0, 0.0004464285714285699*gmsf};
point_pylc_dup = 5756; Point(5756) = {0.02427050983125124, 0.017633557568770313, 0, 0.0004464285714285699*gmsf};
point_pylc_dup = 5757; Point(5757) = {0.02265247584250116, 0.01645798706418563, 0, 0.00024107142857142738*gmsf};
point_pylc_dup = 5760; Point(5760) = {0.014000000000000004, 0.02424871130596428, 0, 0.00024107142857142738*gmsf};
point_pylc_dup = 5773; Point(5773) = {0.0029267969714898527, 0.02784661307031212, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 5775; Point(5775) = {0.003135853898024843, 0.0298356568610487, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 5776; Point(5776) = {-0.003135853898024831, 0.0298356568610487, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 5777; Point(5777) = {-0.002926796971489844, 0.027846613070312123, 0.0, 0.00024107142857142773*gmsf};
point_pylc_dup = 5780; Point(5780) = {-0.013999999999999995, 0.024248711305964288, 0.0, 0.000241071428571427*gmsf};
point_pylc_dup = 5793; Point(5793) = {-0.022652475842501154, 0.016457987064185633, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 5795; Point(5795) = {-0.02427050983125123, 0.01763355756877032, 0.0, 0.0004464285714285695*gmsf};
point_pylc_dup = 5796; Point(5796) = {-0.027406363729276073, 0.012202099292278392, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 5797; Point(5797) = {-0.025579272813991003, 0.011388626006126501, 0.0, 0.000241071428571427*gmsf};
point_pylc_dup = 5800; Point(5800) = {-0.028, 1.0408340855860843e-17, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 5813; Point(5813) = {-0.025579272813991007, -0.011388626006126489, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 5815; Point(5815) = {-0.027406363729276077, -0.01220209929227838, 0.0, 0.0004464285714285695*gmsf};
point_pylc_dup = 5816; Point(5816) = {-0.024270509831251244, -0.01763355756877031, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 5817; Point(5817) = {-0.022652475842501164, -0.016457987064185626, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 5820; Point(5820) = {-0.014000000000000007, -0.02424871130596428, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 5833; Point(5833) = {-0.002926796971489863, -0.027846613070312123, 0.0, 0.00024107142857142773*gmsf};
point_pylc_dup = 5835; Point(5835) = {-0.0031358538980248533, -0.0298356568610487, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 5836; Point(5836) = {0.0031358538980248204, -0.029835656861048703, 0.0, 0.0004464285714285703*gmsf};
point_pylc_dup = 5837; Point(5837) = {0.0029267969714898336, -0.027846613070312127, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 5840; Point(5840) = {0.013999999999999986, -0.024248711305964295, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 5853; Point(5853) = {0.022652475842501144, -0.01645798706418565, 0.0, 0.00024107142857142773*gmsf};
point_pylc_dup = 5855; Point(5855) = {0.024270509831251223, -0.017633557568770334, 0.0, 0.0004464285714285695*gmsf};
point_pylc_dup = 5856; Point(5856) = {0.027406363729276066, -0.012202099292278407, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 5857; Point(5857) = {0.025579272813991, -0.011388626006126515, 0.0, 0.00024107142857142738*gmsf};
point_pylc_dup = 5405; Point(5405) = {0.028977774788670887, 0.007764571353079951, 0, 0.0004464285714285699*gmsf};
point_pylc_dup = 5407; Point(5407) = {0.03863703305156119, 0.010352761804106601, 0, 0.0014732142857142847*gmsf};
point_pylc_dup = 5410; Point(5410) = {0.02828427124746613, 0.028284271247457672, 0, 0.0014732142857142847*gmsf};
point_pylc_dup = 5412; Point(5412) = {0.021213203435599598, 0.021213203435593256, 0, 0.0004464285714285703*gmsf};
point_pylc_dup = 5435; Point(5435) = {0.0077645713530712975, 0.028977774788673204, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 5437; Point(5437) = {0.010352761804095065, 0.038637033051564275, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 5440; Point(5440) = {-0.01035276180409505, 0.03863703305156428, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 5442; Point(5442) = {-0.007764571353071287, 0.028977774788673215, 0.0, 0.0004464285714285703*gmsf};
point_pylc_dup = 5465; Point(5465) = {-0.021213203435599588, 0.02121320343559326, 0.0, 0.0004464285714285695*gmsf};
point_pylc_dup = 5467; Point(5467) = {-0.02828427124746612, 0.028284271247457683, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 5470; Point(5470) = {-0.03863703305156118, 0.010352761804106617, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 5472; Point(5472) = {-0.028977774788670883, 0.007764571353079961, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 5495; Point(5495) = {-0.028977774788670887, -0.007764571353079948, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 5497; Point(5497) = {-0.03863703305156119, -0.010352761804106596, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 5500; Point(5500) = {-0.028284271247466134, -0.02828427124745767, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 5502; Point(5502) = {-0.0212132034355996, -0.021213203435593252, 0.0, 0.0004464285714285703*gmsf};
point_pylc_dup = 5525; Point(5525) = {-0.007764571353071307, -0.028977774788673204, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 5527; Point(5527) = {-0.01035276180409508, -0.03863703305156428, 0.0, 0.0014732142857142854*gmsf};
point_pylc_dup = 5530; Point(5530) = {0.010352761804095037, -0.03863703305156429, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 5532; Point(5532) = {0.00776457135307128, -0.028977774788673215, 0.0, 0.0004464285714285703*gmsf};
point_pylc_dup = 5555; Point(5555) = {0.021213203435599577, -0.021213203435593273, 0.0, 0.0004464285714285699*gmsf};
point_pylc_dup = 5557; Point(5557) = {0.028284271247466106, -0.0282842712474577, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 5560; Point(5560) = {0.03863703305156117, -0.01035276180410664, 0.0, 0.0014732142857142847*gmsf};
point_pylc_dup = 5562; Point(5562) = {0.028977774788670883, -0.007764571353079976, 0.0, 0.0004464285714285703*gmsf};

// Lines and Curves
MB_CurveRotor = 3032;Circle(MB_CurveRotor) = {5253, 5250, 5254};
MB_CurveRotor_dup = 3054;Circle(MB_CurveRotor_dup) = {5254, 5250, 5277};
MB_CurveRotor_dup = 3056;Circle(MB_CurveRotor_dup) = {5277, 5250, 5280};
MB_CurveRotor_dup = 3058;Circle(MB_CurveRotor_dup) = {5280, 5250, 5253};
rotorBand1_dup = 3318;Circle(rotorBand1_dup) = {5711, 5250, 5713};
lowerLine2_dup = 3321;Line(lowerLine2_dup) = {5711, 5253};
upperLine2_dup = 3322;Line(upperLine2_dup) = {5713, 5254};
rotorBand1_dup = 3324;Circle(rotorBand1_dup) = {5713, 5250, 5723};
upperLine2_dup = 3328;Line(upperLine2_dup) = {5723, 5277};
rotorBand1_dup = 3330;Circle(rotorBand1_dup) = {5723, 5250, 5733};
upperLine2_dup = 3334;Line(upperLine2_dup) = {5733, 5280};
rotorBand1_dup = 3336;Circle(rotorBand1_dup) = {5733, 5250, 5711};
Line_dup = 3101;Line(Line_dup) = {5351, 5352};
CircleArc_dup = 3103;Circle(CircleArc_dup) = {5352, 5250, 5355};
Line_dup = 3104;Line(Line_dup) = {5355, 5357};
CircleArc_dup = 3106;Circle(CircleArc_dup) = {5357, 5250, 5351};
Line_dup = 3107;Line(Line_dup) = {5361, 5362};
CircleArc_dup = 3109;Circle(CircleArc_dup) = {5362, 5250, 5365};
Line_dup = 3110;Line(Line_dup) = {5365, 5367};
CircleArc_dup = 3112;Circle(CircleArc_dup) = {5367, 5250, 5361};
Line_dup = 3113;Line(Line_dup) = {5371, 5372};
CircleArc_dup = 3115;Circle(CircleArc_dup) = {5372, 5250, 5375};
Line_dup = 3116;Line(Line_dup) = {5375, 5377};
CircleArc_dup = 3118;Circle(CircleArc_dup) = {5377, 5250, 5371};
Line_dup = 3119;Line(Line_dup) = {5381, 5382};
CircleArc_dup = 3121;Circle(CircleArc_dup) = {5382, 5250, 5385};
Line_dup = 3122;Line(Line_dup) = {5385, 5387};
CircleArc_dup = 3124;Circle(CircleArc_dup) = {5387, 5250, 5381};
CircleArc_dup = 3270;Circle(CircleArc_dup) = {5631, 5250, 5351};
CircleArc_dup = 3272;Circle(CircleArc_dup) = {5357, 5250, 5636};
lowerLine1_dup = 3279;Line(lowerLine1_dup) = {5631, 5711};
upperLine1_dup = 3280;Line(upperLine1_dup) = {5636, 5713};
CircleArc_dup = 3282;Circle(CircleArc_dup) = {5636, 5250, 5361};
CircleArc_dup = 3284;Circle(CircleArc_dup) = {5367, 5250, 5656};
upperLine1_dup = 3292;Line(upperLine1_dup) = {5656, 5723};
CircleArc_dup = 3294;Circle(CircleArc_dup) = {5656, 5250, 5371};
CircleArc_dup = 3296;Circle(CircleArc_dup) = {5377, 5250, 5676};
upperLine1_dup = 3304;Line(upperLine1_dup) = {5676, 5733};
CircleArc_dup = 3306;Circle(CircleArc_dup) = {5676, 5250, 5381};
CircleArc_dup = 3308;Circle(CircleArc_dup) = {5387, 5250, 5631};
Line_dup = 3069;Line(Line_dup) = {5250, 5631};
Line_dup = 3076;Line(Line_dup) = {5636, 5250};
Line_dup = 3084;Line(Line_dup) = {5656, 5250};
Line_dup = 3092;Line(Line_dup) = {5676, 5250};
OuterLimit = 3003;Circle(OuterLimit) = {5204, 5250, 5205};
OuterLimit_dup = 3060;Circle(OuterLimit_dup) = {5284, 5250, 5204};
OuterLimit_dup = 3062;Circle(OuterLimit_dup) = {5287, 5250, 5284};
OuterLimit_dup = 3064;Circle(OuterLimit_dup) = {5290, 5250, 5287};
OuterLimit_dup = 3066;Circle(OuterLimit_dup) = {5293, 5250, 5290};
OuterLimit_dup = 3068;Circle(OuterLimit_dup) = {5205, 5250, 5293};
MB_CurveStator = 3040;Circle(MB_CurveStator) = {5258, 5250, 5259};
MB_CurveStator_dup = 3044;Circle(MB_CurveStator_dup) = {5259, 5250, 5262};
MB_CurveStator_dup = 3046;Circle(MB_CurveStator_dup) = {5262, 5250, 5265};
MB_CurveStator_dup = 3048;Circle(MB_CurveStator_dup) = {5265, 5250, 5268};
MB_CurveStator_dup = 3050;Circle(MB_CurveStator_dup) = {5268, 5250, 5271};
MB_CurveStator_dup = 3052;Circle(MB_CurveStator_dup) = {5271, 5250, 5258};
statorCircle4_dup = 3414;Circle(statorCircle4_dup) = {5871, 5250, 5873};
lowerLine3_dup = 3417;Line(lowerLine3_dup) = {5258, 5871};
upperLine3_dup = 3418;Line(upperLine3_dup) = {5259, 5873};
statorCircle4_dup = 3420;Circle(statorCircle4_dup) = {5873, 5250, 5883};
upperLine3_dup = 3424;Line(upperLine3_dup) = {5262, 5883};
statorCircle4_dup = 3426;Circle(statorCircle4_dup) = {5883, 5250, 5893};
upperLine3_dup = 3430;Line(upperLine3_dup) = {5265, 5893};
statorCircle4_dup = 3432;Circle(statorCircle4_dup) = {5893, 5250, 5903};
upperLine3_dup = 3436;Line(upperLine3_dup) = {5268, 5903};
statorCircle4_dup = 3438;Circle(statorCircle4_dup) = {5903, 5250, 5913};
upperLine3_dup = 3442;Line(upperLine3_dup) = {5271, 5913};
statorCircle4_dup = 3444;Circle(statorCircle4_dup) = {5913, 5250, 5871};
CircleArc_dup = 3342;Circle(CircleArc_dup) = {5751, 5250, 5753};
Line_dup = 3343;Line(Line_dup) = {5753, 5755};
Line_dup = 3344;Line(Line_dup) = {5756, 5757};
CircleArc_dup = 3346;Circle(CircleArc_dup) = {5757, 5250, 5760};
interface_line_slot_opening___slot_dup = 3348;Circle(interface_line_slot_opening___slot_dup) = {5755, 5250, 5756};
lowerLine4_dup = 3351;Line(lowerLine4_dup) = {5751, 5871};
upperLine4_dup = 3352;Line(upperLine4_dup) = {5760, 5873};
CircleArc_dup = 3354;Circle(CircleArc_dup) = {5760, 5250, 5773};
Line_dup = 3355;Line(Line_dup) = {5773, 5775};
Line_dup = 3356;Line(Line_dup) = {5776, 5777};
CircleArc_dup = 3358;Circle(CircleArc_dup) = {5777, 5250, 5780};
interface_line_slot_opening___slot_dup = 3360;Circle(interface_line_slot_opening___slot_dup) = {5775, 5250, 5776};
upperLine4_dup = 3364;Line(upperLine4_dup) = {5780, 5883};
CircleArc_dup = 3366;Circle(CircleArc_dup) = {5780, 5250, 5793};
Line_dup = 3367;Line(Line_dup) = {5793, 5795};
Line_dup = 3368;Line(Line_dup) = {5796, 5797};
CircleArc_dup = 3370;Circle(CircleArc_dup) = {5797, 5250, 5800};
interface_line_slot_opening___slot_dup = 3372;Circle(interface_line_slot_opening___slot_dup) = {5795, 5250, 5796};
upperLine4_dup = 3376;Line(upperLine4_dup) = {5800, 5893};
CircleArc_dup = 3378;Circle(CircleArc_dup) = {5800, 5250, 5813};
Line_dup = 3379;Line(Line_dup) = {5813, 5815};
Line_dup = 3380;Line(Line_dup) = {5816, 5817};
CircleArc_dup = 3382;Circle(CircleArc_dup) = {5817, 5250, 5820};
interface_line_slot_opening___slot_dup = 3384;Circle(interface_line_slot_opening___slot_dup) = {5815, 5250, 5816};
upperLine4_dup = 3388;Line(upperLine4_dup) = {5820, 5903};
CircleArc_dup = 3390;Circle(CircleArc_dup) = {5820, 5250, 5833};
Line_dup = 3391;Line(Line_dup) = {5833, 5835};
Line_dup = 3392;Line(Line_dup) = {5836, 5837};
CircleArc_dup = 3394;Circle(CircleArc_dup) = {5837, 5250, 5840};
interface_line_slot_opening___slot_dup = 3396;Circle(interface_line_slot_opening___slot_dup) = {5835, 5250, 5836};
upperLine4_dup = 3400;Line(upperLine4_dup) = {5840, 5913};
CircleArc_dup = 3402;Circle(CircleArc_dup) = {5840, 5250, 5853};
Line_dup = 3403;Line(Line_dup) = {5853, 5855};
Line_dup = 3404;Line(Line_dup) = {5856, 5857};
CircleArc_dup = 3406;Circle(CircleArc_dup) = {5857, 5250, 5751};
interface_line_slot_opening___slot_dup = 3408;Circle(interface_line_slot_opening___slot_dup) = {5855, 5250, 5856};
Line_dup = 3125;Line(Line_dup) = {5760, 5204};
Line_dup = 3128;Line(Line_dup) = {5205, 5751};
CircleArc_dup = 3133;Circle(CircleArc_dup) = {5755, 5250, 5405};
Line_dup = 3134;Line(Line_dup) = {5405, 5407};
CircleArc_dup = 3136;Circle(CircleArc_dup) = {5407, 5250, 5410};
Line_dup = 3137;Line(Line_dup) = {5410, 5412};
CircleArc_dup = 3139;Circle(CircleArc_dup) = {5412, 5250, 5756};
Line_dup = 3143;Line(Line_dup) = {5780, 5284};
CircleArc_dup = 3151;Circle(CircleArc_dup) = {5775, 5250, 5435};
Line_dup = 3152;Line(Line_dup) = {5435, 5437};
CircleArc_dup = 3154;Circle(CircleArc_dup) = {5437, 5250, 5440};
Line_dup = 3155;Line(Line_dup) = {5440, 5442};
CircleArc_dup = 3157;Circle(CircleArc_dup) = {5442, 5250, 5776};
Line_dup = 3161;Line(Line_dup) = {5800, 5287};
CircleArc_dup = 3169;Circle(CircleArc_dup) = {5795, 5250, 5465};
Line_dup = 3170;Line(Line_dup) = {5465, 5467};
CircleArc_dup = 3172;Circle(CircleArc_dup) = {5467, 5250, 5470};
Line_dup = 3173;Line(Line_dup) = {5470, 5472};
CircleArc_dup = 3175;Circle(CircleArc_dup) = {5472, 5250, 5796};
Line_dup = 3179;Line(Line_dup) = {5820, 5290};
CircleArc_dup = 3187;Circle(CircleArc_dup) = {5815, 5250, 5495};
Line_dup = 3188;Line(Line_dup) = {5495, 5497};
CircleArc_dup = 3190;Circle(CircleArc_dup) = {5497, 5250, 5500};
Line_dup = 3191;Line(Line_dup) = {5500, 5502};
CircleArc_dup = 3193;Circle(CircleArc_dup) = {5502, 5250, 5816};
Line_dup = 3197;Line(Line_dup) = {5840, 5293};
CircleArc_dup = 3205;Circle(CircleArc_dup) = {5835, 5250, 5525};
Line_dup = 3206;Line(Line_dup) = {5525, 5527};
CircleArc_dup = 3208;Circle(CircleArc_dup) = {5527, 5250, 5530};
Line_dup = 3209;Line(Line_dup) = {5530, 5532};
CircleArc_dup = 3211;Circle(CircleArc_dup) = {5532, 5250, 5836};
CircleArc_dup = 3223;Circle(CircleArc_dup) = {5855, 5250, 5555};
Line_dup = 3224;Line(Line_dup) = {5555, 5557};
CircleArc_dup = 3226;Circle(CircleArc_dup) = {5557, 5250, 5560};
Line_dup = 3227;Line(Line_dup) = {5560, 5562};
CircleArc_dup = 3229;Circle(CircleArc_dup) = {5562, 5250, 5856};
CircleArc_dup = 3234;Circle(CircleArc_dup) = {5405, 5250, 5412};
CircleArc_dup = 3240;Circle(CircleArc_dup) = {5435, 5250, 5442};
CircleArc_dup = 3246;Circle(CircleArc_dup) = {5465, 5250, 5472};
CircleArc_dup = 3252;Circle(CircleArc_dup) = {5495, 5250, 5502};
CircleArc_dup = 3258;Circle(CircleArc_dup) = {5525, 5250, 5532};
CircleArc_dup = 3264;Circle(CircleArc_dup) = {5555, 5250, 5562};

// Surfaces

Curve Loop(320) = {3318,3322,-3032,-3321};
Surf_rotorAirGap2_dup = {320};
Plane Surface(Surf_rotorAirGap2_dup) = {320};

Curve Loop(321) = {3324,3328,-3054,-3322};
Surf_rotorAirGap2_dup = {321};
Plane Surface(Surf_rotorAirGap2_dup) = {321};

Curve Loop(322) = {3330,3334,-3056,-3328};
Surf_rotorAirGap2_dup = {322};
Plane Surface(Surf_rotorAirGap2_dup) = {322};

Curve Loop(323) = {3336,3321,-3058,-3334};
Surf_rotorAirGap2_dup = {323};
Plane Surface(Surf_rotorAirGap2_dup) = {323};

Curve Loop(300) = {3101,3103,3104,3106};
Surf_Magnet_dup = {300};
Plane Surface(Surf_Magnet_dup) = {300};

Curve Loop(301) = {3107,3109,3110,3112};
Surf_Magnet_dup = {301};
Plane Surface(Surf_Magnet_dup) = {301};

Curve Loop(302) = {3113,3115,3116,3118};
Surf_Magnet_dup = {302};
Plane Surface(Surf_Magnet_dup) = {302};

Curve Loop(303) = {3119,3121,3122,3124};
Surf_Magnet_dup = {303};
Plane Surface(Surf_Magnet_dup) = {303};

Curve Loop(316) = {3270,3101,3103,3104,3272,3280,-3318,-3279};
Surf_rotorAirGap1_dup = {316};
Plane Surface(Surf_rotorAirGap1_dup) = {316};

Curve Loop(317) = {3282,3107,3109,3110,3284,3292,-3324,-3280};
Surf_rotorAirGap1_dup = {317};
Plane Surface(Surf_rotorAirGap1_dup) = {317};

Curve Loop(318) = {3294,3113,3115,3116,3296,3304,-3330,-3292};
Surf_rotorAirGap1_dup = {318};
Plane Surface(Surf_rotorAirGap1_dup) = {318};

Curve Loop(319) = {3306,3119,3121,3122,3308,3279,-3336,-3304};
Surf_rotorAirGap1_dup = {319};
Plane Surface(Surf_rotorAirGap1_dup) = {319};

Curve Loop(296) = {3069,3270,-3106,3272,3076};
Surf_Rotorblech_dup = {296};
Plane Surface(Surf_Rotorblech_dup) = {296};

Curve Loop(297) = {3076,-3084,-3284,3112,-3282};
Surf_Rotorblech_dup = {297};
Plane Surface(Surf_Rotorblech_dup) = {297};

Curve Loop(298) = {3084,-3092,-3296,3118,-3294};
Surf_Rotorblech_dup = {298};
Plane Surface(Surf_Rotorblech_dup) = {298};

Curve Loop(299) = {3092,3069,-3308,3124,-3306};
Surf_Rotorblech_dup = {299};
Plane Surface(Surf_Rotorblech_dup) = {299};

Curve Loop(330) = {3414,-3418,-3040,3417};
Surf_statorAirGap2_dup = {330};
Plane Surface(Surf_statorAirGap2_dup) = {330};

Curve Loop(331) = {3420,-3424,-3044,3418};
Surf_statorAirGap2_dup = {331};
Plane Surface(Surf_statorAirGap2_dup) = {331};

Curve Loop(332) = {3426,-3430,-3046,3424};
Surf_statorAirGap2_dup = {332};
Plane Surface(Surf_statorAirGap2_dup) = {332};

Curve Loop(333) = {3432,-3436,-3048,3430};
Surf_statorAirGap2_dup = {333};
Plane Surface(Surf_statorAirGap2_dup) = {333};

Curve Loop(334) = {3438,-3442,-3050,3436};
Surf_statorAirGap2_dup = {334};
Plane Surface(Surf_statorAirGap2_dup) = {334};

Curve Loop(335) = {3444,-3417,-3052,3442};
Surf_statorAirGap2_dup = {335};
Plane Surface(Surf_statorAirGap2_dup) = {335};

Curve Loop(324) = {3342,3343,3348,3344,3346,3352,-3414,-3351};
Surf_statorAirGap1_dup = {324};
Plane Surface(Surf_statorAirGap1_dup) = {324};

Curve Loop(325) = {3354,3355,3360,3356,3358,3364,-3420,-3352};
Surf_statorAirGap1_dup = {325};
Plane Surface(Surf_statorAirGap1_dup) = {325};

Curve Loop(326) = {3366,3367,3372,3368,3370,3376,-3426,-3364};
Surf_statorAirGap1_dup = {326};
Plane Surface(Surf_statorAirGap1_dup) = {326};

Curve Loop(327) = {3378,3379,3384,3380,3382,3388,-3432,-3376};
Surf_statorAirGap1_dup = {327};
Plane Surface(Surf_statorAirGap1_dup) = {327};

Curve Loop(328) = {3390,3391,3396,3392,3394,3400,-3438,-3388};
Surf_statorAirGap1_dup = {328};
Plane Surface(Surf_statorAirGap1_dup) = {328};

Curve Loop(329) = {3402,3403,3408,3404,3406,3351,-3444,-3400};
Surf_statorAirGap1_dup = {329};
Plane Surface(Surf_statorAirGap1_dup) = {329};

Curve Loop(304) = {3125,3003,3128,3342,3343,3133,3134,3136,3137,3139,3344,3346};
Surf_Statorblech_dup = {304};
Plane Surface(Surf_Statorblech_dup) = {304};

Curve Loop(305) = {3143,3060,-3125,3354,3355,3151,3152,3154,3155,3157,3356,3358};
Surf_Statorblech_dup = {305};
Plane Surface(Surf_Statorblech_dup) = {305};

Curve Loop(306) = {3161,3062,-3143,3366,3367,3169,3170,3172,3173,3175,3368,3370};
Surf_Statorblech_dup = {306};
Plane Surface(Surf_Statorblech_dup) = {306};

Curve Loop(307) = {3179,3064,-3161,3378,3379,3187,3188,3190,3191,3193,3380,3382};
Surf_Statorblech_dup = {307};
Plane Surface(Surf_Statorblech_dup) = {307};

Curve Loop(308) = {3197,3066,-3179,3390,3391,3205,3206,3208,3209,3211,3392,3394};
Surf_Statorblech_dup = {308};
Plane Surface(Surf_Statorblech_dup) = {308};

Curve Loop(309) = {3128,-3406,-3404,-3229,-3227,-3226,-3224,-3223,-3403,-3402,3197,-3068};
Surf_Statorblech_dup = {309};
Plane Surface(Surf_Statorblech_dup) = {309};

Curve Loop(310) = {3234,-3137,-3136,-3134};
Surf_Stator_Nut_dup = {310};
Plane Surface(Surf_Stator_Nut_dup) = {310};

Curve Loop(311) = {3240,-3155,-3154,-3152};
Surf_Stator_Nut_dup = {311};
Plane Surface(Surf_Stator_Nut_dup) = {311};

Curve Loop(312) = {3246,-3173,-3172,-3170};
Surf_Stator_Nut_dup = {312};
Plane Surface(Surf_Stator_Nut_dup) = {312};

Curve Loop(313) = {3252,-3191,-3190,-3188};
Surf_Stator_Nut_dup = {313};
Plane Surface(Surf_Stator_Nut_dup) = {313};

Curve Loop(314) = {3258,-3209,-3208,-3206};
Surf_Stator_Nut_dup = {314};
Plane Surface(Surf_Stator_Nut_dup) = {314};

Curve Loop(315) = {3264,-3227,-3226,-3224};
Surf_Stator_Nut_dup = {315};
Plane Surface(Surf_Stator_Nut_dup) = {315};

// Color code
If (!Flag_individualColoring)
Color SkyBlue {Surface {320}; }
Color SkyBlue {Surface {321}; }
Color SkyBlue {Surface {322}; }
Color SkyBlue {Surface {323}; }
Color Red {Surface {300}; }
Color Green {Surface {301}; }
Color Red {Surface {302}; }
Color Green {Surface {303}; }
Color SkyBlue {Surface {316}; }
Color SkyBlue {Surface {317}; }
Color SkyBlue {Surface {318}; }
Color SkyBlue {Surface {319}; }
Color SteelBlue {Surface {296}; }
Color SteelBlue {Surface {297}; }
Color SteelBlue {Surface {298}; }
Color SteelBlue {Surface {299}; }
Color SkyBlue {Surface {330}; }
Color SkyBlue {Surface {331}; }
Color SkyBlue {Surface {332}; }
Color SkyBlue {Surface {333}; }
Color SkyBlue {Surface {334}; }
Color SkyBlue {Surface {335}; }
Color SkyBlue {Surface {324}; }
Color SkyBlue {Surface {325}; }
Color SkyBlue {Surface {326}; }
Color SkyBlue {Surface {327}; }
Color SkyBlue {Surface {328}; }
Color SkyBlue {Surface {329}; }
Color SteelBlue4 {Surface {304}; }
Color SteelBlue4 {Surface {305}; }
Color SteelBlue4 {Surface {306}; }
Color SteelBlue4 {Surface {307}; }
Color SteelBlue4 {Surface {308}; }
Color SteelBlue4 {Surface {309}; }
Color Magenta {Surface {310}; }
Color Magenta {Surface {311}; }
Color Cyan {Surface {312}; }
Color Cyan {Surface {313}; }
Color Yellow4 {Surface {314}; }
Color Yellow4 {Surface {315}; }
EndIf

// Physical Elements
// Rotor_Bnd_MB_1
Physical Curve("Rotor_Bnd_MB_1", 3) = {3032,3054,3056,3058};
// LuR2
Physical Surface("LuR2", 18) = {320,321,322,323};
// Mag0_0
Physical Surface("Mag0_0", 6) = {300};
// Mag0_1
Physical Surface("Mag0_1", 7) = {301};
// Mag0_2
Physical Surface("Mag0_2", 8) = {302};
// Mag0_3
Physical Surface("Mag0_3", 9) = {303};
// LuR1
Physical Surface("LuR1", 17) = {316,317,318,319};
// Pol
Physical Surface("Pol", 5) = {296,297,298,299};
// outerLimit
Physical Curve("outerLimit", 4) = {3003,3060,3062,3064,3066,3068};
// mbStator
Physical Curve("mbStator", 2) = {3040,3044,3046,3048,3050,3052};
// StLu2
Physical Surface("StLu2", 20) = {330,331,332,333,334,335};
// StLu1
Physical Surface("StLu1", 19) = {324,325,326,327,328,329};
// StNut
Physical Surface("StNut", 10) = {304,305,306,307,308,309};
// StCu0_0_Up
Physical Surface("StCu0_0_Up", 11) = {310};
// StCu0_1_Un
Physical Surface("StCu0_1_Un", 12) = {311};
// StCu0_2_Wp
Physical Surface("StCu0_2_Wp", 13) = {312};
// StCu0_3_Wn
Physical Surface("StCu0_3_Wn", 14) = {313};
// StCu0_4_Vp
Physical Surface("StCu0_4_Vp", 15) = {314};
// StCu0_5_Vn
Physical Surface("StCu0_5_Vn", 16) = {315};

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
	MeshSize { PointsOf {Surface{ 300,301,302,303 };} } = Mag_msf*mm;
	MeshSize { PointsOf {Surface{ 296,297,298,299 };} } = Pol_msf*mm;
	MeshSize { PointsOf {Surface{ 316,317,318,319,320,321,322,323 };} } = LuR_msf*mm;
	MeshSize { PointsOf {Surface{ 316,317,318,319 };} } = LuR1_msf*mm;
	MeshSize { PointsOf {Surface{ 320,321,322,323 };} } = LuR2_msf*mm;
	MeshSize { PointsOf {Surface{ 310,311,312,313,314,315 };} } = StCu_msf*mm;
	MeshSize { PointsOf {Surface{ 304,305,306,307,308,309 };} } = StNut_msf*mm;
	MeshSize { PointsOf {Surface{ 324,325,326,327,328,329,330,331,332,333,334,335 };} } = StLu_msf*mm;
	MeshSize { PointsOf {Surface{ 324,325,326,327,328,329 };} } = StLu1_msf*mm;
	MeshSize { PointsOf {Surface{ 330,331,332,333,334,335 };} } = StLu2_msf*mm;
EndIf

// Mesh operations

// Do not switch mesh algorithm on failure, because this led to mesh errors in the past.
Mesh.AlgorithmSwitchOnFailure = 0;DefineConstant[Flag_CompoundMesh = {0, Name StrCat[INPUT_MESH, "Compound Mesh"], Choices {0,1}, Help "Use Compound Mesh to ignore lines between segments while meshing.",Visible Flag_ExpertMode}];
If (Flag_CompoundMesh)
Compound Surface{296,297,298,299}; // rotor domainLam
Compound Surface{304,305,306,307,308,309}; // stator domainLam
Compound Surface{320,321,322,323}; // rotor airGap
Compound Surface{330,331,332,333,334,335}; // stator airGap
EndIf // (Flag_CompoundMesh)

// Add mesh size setting for Movingband lines
DefineConstant[
	NbrMbSegments = {860.0, Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],Max 1440, Min 180, Step 10, Help "Set the number of mesh segments on the interface between rotor/statorairgap and movingband. Value represents number of segments on whole circle.", Visible Flag_ExpertMode},
	r_MB_R = 0.0274
];
MB_LinesR = {3032,3054,3056,3058};
MeshSize{ PointsOf{Line{MB_LinesR[]};}} = 2*Pi*r_MB_R/NbrMbSegments;

MB_LinesS = {3040,3044,3046,3048,3050,3052};
MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*0.0276/NbrMbSegments;

Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)

// Create boundary lines for moving rotor contour plot
rotorBndLines[] = Boundary{ Physical Surface{ 6,7,8,9 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 5 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 18 }; };
statorBndLines[] = Boundary{ Physical Surface{ 2,4,10,11,12,13,14,15,16,19,20 }; };
Physical Line("DomainPlotMovingGeo",1) = {rotorBndLines[], statorBndLines[]};
