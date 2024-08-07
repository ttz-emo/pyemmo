// This script was created with pyemmo (Version 1.3.1b1, git 5fd2a8)

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
point_pylc_dup = 125; Point(125) = {0.13462, 0.0, 0, 0.006730999999999999*gmsf};
point_pylc_dup = 126; Point(126) = {0.08095, 0.0, 0, 0.00018658143413008237*gmsf};
PointM41_dup = 132; Point(132) = {0.0808, 0, 0, 0.00016829071706504786*gmsf};
PointM31_dup = 133; Point(133) = {0.08065, 0, 0, 0.00015000000000001124*gmsf};
point_pylc_dup = 123; Point(123) = {0.05532, 0.0, 0, 0.005871021118012428*gmsf};
point_pylc_dup = 124; Point(124) = {0.0802, 0.0, 0, 0.00021816149068324008*gmsf};
PointM11_dup = 128; Point(128) = {0.08034999999999999, 0, 0, 0.00018408074534162567*gmsf};
PointM21_dup = 130; Point(130) = {0.08049999999999999, 0, 0, 0.00015000000000001124*gmsf};
point_pylc_dup = 135; Point(135) = {0.09519071488333303, 0.09519071488333303, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 136; Point(136) = {0.057240293937051025, 0.057240293937051025, 0.0, 0.00018658143413008237*gmsf};
PointM41_dup = 138; Point(138) = {0.05713422791987304, 0.05713422791987304, 0.0, 0.00016829071706504786*gmsf};
PointM31_dup = 139; Point(139) = {0.05702816190269506, 0.05702816190269506, 0.0, 0.00015000000000001124*gmsf};
point_pylc_dup = 141; Point(141) = {0.03911714713523981, 0.03911714713523981, 0.0, 0.005871021118012428*gmsf};
point_pylc_dup = 142; Point(142) = {0.05670996385116111, 0.05670996385116111, 0.0, 0.00021816149068324008*gmsf};
PointM11_dup = 144; Point(144) = {0.05681602986833909, 0.05681602986833909, 0.0, 0.00018408074534162567*gmsf};
PointM21_dup = 146; Point(146) = {0.05692209588551707, 0.05692209588551707, 0.0, 0.00015000000000001124*gmsf};
point_pylc = 11; Point(11) = {0, 0, 0, 0.001*gmsf};
PointM22_dup = 164; Point(164) = {0.0, 0.08049999999999999, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 167; Point(167) = {-0.05692209588551706, 0.056922095885517075, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 170; Point(170) = {-0.08049999999999999, 0.0, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 173; Point(173) = {-0.056922095885517075, -0.05692209588551706, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 176; Point(176) = {-6.938893903907228e-18, -0.08049999999999999, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 179; Point(179) = {0.056922095885517054, -0.05692209588551708, 0.0, 0.00015000000000001124*gmsf};
point_pylc_dup = 257; Point(257) = {0.06976122233612055, 0.009211657048165817, 0, 0.001*gmsf};
point_pylc_dup = 258; Point(258) = {0.05759575268186625, 0.02108605589995692, 0, 0.001*gmsf};
point_pylc_dup = 260; Point(260) = {0.06213596400755108, 0.02573755900305415, 0, 0.001*gmsf};
point_pylc_dup = 262; Point(262) = {0.07430143366180537, 0.013863160151263048, 0, 0.001*gmsf};
point_pylc_dup = 271; Point(271) = {0.05584225854245618, 0.04281500821301038, 0, 0.001*gmsf};
point_pylc_dup = 272; Point(272) = {0.055636440404229055, 0.025816254173552766, 0, 0.001*gmsf};
point_pylc_dup = 276; Point(276) = {0.062341782145778214, 0.04273631304251177, 0, 0.001*gmsf};
point_pylc_dup = 248; Point(248) = {0.07867689952069529, 0.0019066939477583589, 0, 0.0005589689440993865*gmsf};
point_pylc_dup = 249; Point(249) = {0.0704597163862259, 0.009927272910180775, 0, 0.001*gmsf};
point_pylc_dup = 253; Point(253) = {0.07803354822364487, 0.01022034009356294, 0, 0.0005589689440993865*gmsf};
point_pylc_dup = 265; Point(265) = {0.05829424673197161, 0.02180167176197188, 0, 0.001*gmsf};
point_pylc_dup = 266; Point(266) = {0.05663636711243244, 0.025804147224245285, 0, 0.001*gmsf};
point_pylc_dup = 279; Point(279) = {0.05698120539392355, 0.054284732953708975, 0, 0.0005589689440993886*gmsf};
point_pylc_dup = 280; Point(280) = {0.05684218525065958, 0.04280290126370291, 0, 0.001*gmsf};
point_pylc_dup = 284; Point(284) = {0.062404922895177864, 0.04795117932279565, 0, 0.0005589689440993865*gmsf};
point_pylc = 54; Point(54) = {0.13346830723814235, 0.017571435996663342, 0, 0.006730999999999999*gmsf};
point_pylc_dup = 183; Point(183) = {0.13003293473503436, 0.034842219851701335, 0.0, 0.006730999999999997*gmsf};
point_pylc_dup = 186; Point(186) = {0.12437266266666941, 0.051516843664988377, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 189; Point(189) = {0.11658433985746111, 0.06731, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 192; Point(192) = {0.10680122667000608, 0.08195146357315396, 0.0, 0.006730999999999999*gmsf};
PointM32 = 122; Point(122) = {0.07996002806979781, 0.010526937402547159, 0, 0.00015000000000001124*gmsf};
PointM32_dup = 149; Point(149) = {0.07790191789021336, 0.020873755987518297, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 152; Point(152) = {0.07451088429703527, 0.030863418820244487, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 155; Point(155) = {0.06984494881521497, 0.040325, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 158; Point(158) = {0.06398394689448812, 0.04909660924955331, 0.0, 0.00015000000000001124*gmsf};
PointM42_dup = 706; Point(706) = {0.08010874479900387, 0.010546516331380167, 0, 0.00016829071706504786*gmsf};
PointM42_dup = 716; Point(716) = {0.0780468067641567, 0.020912578844283672, 0.0, 0.00016829071706504786*gmsf};
PointM42_dup = 726; Point(726) = {0.07464946622691196, 0.030920821335099248, 0.0, 0.00016829071706504574*gmsf};
PointM42_dup = 736; Point(736) = {0.06997485262578262, 0.04039999999999999, 0.0, 0.00016829071706504574*gmsf};
PointM42_dup = 746; Point(746) = {0.06410294989553181, 0.04918792346390462, 0.0, 0.00016829071706504786*gmsf};
point_pylc_dup = 592; Point(592) = {0.08083405411411097, 0.004331073247704142, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 594; Point(594) = {0.08183191303734956, 0.004396476376934286, 0, 0.00030851098907667415*gmsf};
point_pylc_dup = 595; Point(595) = {0.08170568499793539, 0.00632234409878479, 0, 0.00030851098907667415*gmsf};
point_pylc_dup = 596; Point(596) = {0.08070782607469679, 0.0062569409695546465, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 599; Point(599) = {0.08025746152820995, 0.010566095260213175, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 611; Point(611) = {0.07957718907619889, 0.014844981600894352, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 613; Point(613) = {0.0805579743566021, 0.015040071922910478, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 614; Point(614) = {0.08018145003511097, 0.016932987514088713, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 615; Point(615) = {0.07920066475470774, 0.01673789719207258, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 618; Point(618) = {0.07819169563810008, 0.020951401701049054, 0.0, 0.0001865814341300845*gmsf};
point_pylc_dup = 630; Point(630) = {0.07695873627022805, 0.02510488820308679, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 632; Point(632) = {0.07790566639972313, 0.02542632766838995, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 633; Point(633) = {0.07728528823168804, 0.027253902818315502, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 634; Point(634) = {0.07633835810219293, 0.026932463353012342, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 637; Point(637) = {0.07478804815678866, 0.030978223849954016, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 649; Point(649) = {0.07302349814968086, 0.03493524320773444, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 651; Point(651) = {0.07392037089121353, 0.03537753189795343, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 652; Point(652) = {0.07306675371909087, 0.03710849628911152, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 653; Point(653) = {0.07216988097755818, 0.036666207598892525, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 656; Point(656) = {0.07010475643635031, 0.040475, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 668; Point(668) = {0.06783880772985405, 0.04416784651521844, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 670; Point(670) = {0.0686702773421566, 0.044723416748238036, 0.0, 0.00030851098907667626*gmsf};
point_pylc_dup = 671; Point(671) = {0.06759802679242875, 0.04632815309998195, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 672; Point(672) = {0.06676655718012621, 0.04577258286696235, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 675; Point(675) = {0.0642219528965755, 0.04927923767825593, 0.0, 0.0001865814341300845*gmsf};
point_pylc_dup = 687; Point(687) = {0.0614933765012986, 0.05264472572318653, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 689; Point(689) = {0.06224521630877756, 0.05330407153828659, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 690; Point(690) = {0.06097267888563443, 0.05475512236672102, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 691; Point(691) = {0.06022083907815545, 0.054095776551620955, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 301; Point(301) = {0.08193230684071783, 0.002864762929763029, 0, 0.00031246726476474504*gmsf};
point_pylc_dup = 303; Point(303) = {0.11126767798545414, 0.0032842862313483155, 0, 0.003889371090557505*gmsf};
point_pylc_dup = 306; Point(306) = {0.11499750116148799, 0.007537334441223301, 0, 0.0043683573413105655*gmsf};
point_pylc_dup = 305; Point(305) = {0.11100606546853357, 0.0072757219243027305, 0, 0.001*gmsf};
point_pylc_dup = 309; Point(309) = {0.110744452951613, 0.011267157617257145, 0, 0.003889371090557505*gmsf};
point_pylc_dup = 311; Point(311) = {0.08160529119456712, 0.007854057545956047, 0, 0.00031246726476474716*gmsf};
point_pylc_dup = 332; Point(332) = {0.08085743800089684, 0.013534566517491518, 0.0, 0.0003124672647647429*gmsf};
point_pylc_dup = 334; Point(334) = {0.10988708219973571, 0.017779535031959233, 0.0, 0.003889371090557503*gmsf};
point_pylc_dup = 337; Point(337) = {0.11302986203328413, 0.022483037441636666, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 336; Point(336) = {0.10910672091167122, 0.021702676153572156, 0.0, 0.001*gmsf};
point_pylc_dup = 340; Point(340) = {0.1083263596236067, 0.025625817275185078, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 342; Point(342) = {0.07988198639081623, 0.018438492919507672, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 363; Point(363) = {0.07839907597896349, 0.023972789919614962, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 365; Point(365) = {0.10662628797112485, 0.03197057105875494, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 368; Point(368) = {0.10912825062789262, 0.037044049437948014, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 367; Point(367) = {0.10534053010991219, 0.035758291576735365, 0.0, 0.001*gmsf};
point_pylc_dup = 371; Point(371) = {0.10405477224869955, 0.03954601209471579, 0.0, 0.003889371090557505*gmsf};
point_pylc_dup = 373; Point(373) = {0.07679187865244769, 0.028707440567090493, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 394; Point(394) = {0.0745992840306997, 0.034000832239700754, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 396; Point(396) = {0.10154108839293599, 0.045614581750818464, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 399; Point(399) = {0.10335942459819074, 0.05097122747782523, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 398; Point(398) = {0.09977193363205998, 0.04920207271694922, 0.0, 0.001*gmsf};
point_pylc_dup = 402; Point(402) = {0.09800277887118398, 0.05278956368307998, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 404; Point(404) = {0.07238784057960469, 0.0384851959473642, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 425; Point(425) = {0.06952307764984167, 0.043447110893353624, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 427; Point(427) = {0.09471849263983566, 0.058478114302374165, 0.0, 0.003889371090557503*gmsf};
point_pylc_dup = 430; Point(430) = {0.09582209015696745, 0.06402627368366276, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 429; Point(429) = {0.09249621170775726, 0.061803992751584345, 0.0, 0.001*gmsf};
point_pylc_dup = 433; Point(433) = {0.09027393077567886, 0.06512987120079453, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 435; Point(435) = {0.06674522648474367, 0.047604458954866355, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 456; Point(456) = {0.06325731213495615, 0.05214999743380636, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 458; Point(458) = {0.08627523721674032, 0.07034107010501991, 0.0, 0.003889371090557505*gmsf};
point_pylc_dup = 461; Point(461) = {0.08664521318625597, 0.0759858125953361, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 460; Point(460) = {0.08363785395634005, 0.07334842933493584, 0.0, 0.001*gmsf};
point_pylc_dup = 464; Point(464) = {0.08100047069593977, 0.07635578856485174, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 466; Point(466) = {0.05996058305945583, 0.05590919647120125, 0.0, 0.00031246726476474716*gmsf};

// Lines and Curves
Line_dup = 73;Line(Line_dup) = {125, 126};
lowerLine4_dup = 76;Line(lowerLine4_dup) = {126, 132};
lowerLine3_dup = 77;Line(lowerLine3_dup) = {133, 132};
Line_dup = 72;Line(Line_dup) = {123, 124};
lowerLine1_dup = 74;Line(lowerLine1_dup) = {124, 128};
lowerLine2_dup = 75;Line(lowerLine2_dup) = {128, 130};
Line_dup = 78;Line(Line_dup) = {135, 136};
lowerLine4_dup = 79;Line(lowerLine4_dup) = {136, 138};
lowerLine3_dup = 80;Line(lowerLine3_dup) = {139, 138};
Line_dup = 81;Line(Line_dup) = {141, 142};
lowerLine1_dup = 82;Line(lowerLine1_dup) = {142, 144};
lowerLine2_dup = 83;Line(lowerLine2_dup) = {144, 146};
InnerLimit = 6;Circle(InnerLimit) = {141, 11, 123};
MB_CurveRotor = 61;Circle(MB_CurveRotor) = {130, 11, 146};
MB_CurveRotor_dup = 95;Circle(MB_CurveRotor_dup) = {146, 11, 164};
MB_CurveRotor_dup = 97;Circle(MB_CurveRotor_dup) = {164, 11, 167};
MB_CurveRotor_dup = 99;Circle(MB_CurveRotor_dup) = {167, 11, 170};
MB_CurveRotor_dup = 101;Circle(MB_CurveRotor_dup) = {170, 11, 173};
MB_CurveRotor_dup = 103;Circle(MB_CurveRotor_dup) = {173, 11, 176};
MB_CurveRotor_dup = 105;Circle(MB_CurveRotor_dup) = {176, 11, 179};
MB_CurveRotor_dup = 107;Circle(MB_CurveRotor_dup) = {179, 11, 130};
rotorBand1_dup = 335;Circle(rotorBand1_dup) = {128, 11, 144};
Line_dup = 150;Line(Line_dup) = {257, 258};
Line_dup = 151;Line(Line_dup) = {258, 260};
Line_dup = 152;Line(Line_dup) = {260, 262};
Line_dup = 153;Line(Line_dup) = {262, 257};
Line_dup = 157;Line(Line_dup) = {271, 272};
Line_dup = 158;Line(Line_dup) = {272, 260};
Line_dup = 159;Line(Line_dup) = {260, 276};
Line_dup = 160;Line(Line_dup) = {276, 271};
Line_dup = 145;Line(Line_dup) = {248, 249};
Line_dup = 146;Line(Line_dup) = {249, 262};
Line_dup = 147;Line(Line_dup) = {262, 253};
CircleArc_dup = 149;Circle(CircleArc_dup) = {253, 11, 248};
Line_dup = 154;Line(Line_dup) = {265, 266};
Line_dup = 155;Line(Line_dup) = {266, 260};
Line_dup = 156;Line(Line_dup) = {260, 265};
Line_dup = 161;Line(Line_dup) = {279, 280};
Line_dup = 162;Line(Line_dup) = {280, 276};
Line_dup = 163;Line(Line_dup) = {276, 284};
CircleArc_dup = 165;Circle(CircleArc_dup) = {284, 11, 279};
CircleArc_dup = 329;Circle(CircleArc_dup) = {124, 11, 142};
OuterLimit = 30;Circle(OuterLimit) = {54, 11, 125};
OuterLimit_dup = 109;Circle(OuterLimit_dup) = {183, 11, 54};
OuterLimit_dup = 111;Circle(OuterLimit_dup) = {186, 11, 183};
OuterLimit_dup = 113;Circle(OuterLimit_dup) = {189, 11, 186};
OuterLimit_dup = 115;Circle(OuterLimit_dup) = {192, 11, 189};
OuterLimit_dup = 117;Circle(OuterLimit_dup) = {135, 11, 192};
MB_CurveStator = 69;Circle(MB_CurveStator) = {133, 11, 122};
MB_CurveStator_dup = 85;Circle(MB_CurveStator_dup) = {122, 11, 149};
MB_CurveStator_dup = 87;Circle(MB_CurveStator_dup) = {149, 11, 152};
MB_CurveStator_dup = 89;Circle(MB_CurveStator_dup) = {152, 11, 155};
MB_CurveStator_dup = 91;Circle(MB_CurveStator_dup) = {155, 11, 158};
MB_CurveStator_dup = 93;Circle(MB_CurveStator_dup) = {158, 11, 139};
statorCircle4_dup = 407;Circle(statorCircle4_dup) = {132, 11, 706};
upperLine3_dup = 411;Line(upperLine3_dup) = {122, 706};
statorCircle4_dup = 413;Circle(statorCircle4_dup) = {706, 11, 716};
upperLine3_dup = 417;Line(upperLine3_dup) = {149, 716};
statorCircle4_dup = 419;Circle(statorCircle4_dup) = {716, 11, 726};
upperLine3_dup = 423;Line(upperLine3_dup) = {152, 726};
statorCircle4_dup = 425;Circle(statorCircle4_dup) = {726, 11, 736};
upperLine3_dup = 429;Line(upperLine3_dup) = {155, 736};
statorCircle4_dup = 431;Circle(statorCircle4_dup) = {736, 11, 746};
upperLine3_dup = 435;Line(upperLine3_dup) = {158, 746};
statorCircle4_dup = 437;Circle(statorCircle4_dup) = {746, 11, 138};
CircleArc_dup = 341;Circle(CircleArc_dup) = {126, 11, 592};
Line_dup = 342;Line(Line_dup) = {592, 594};
Line_dup = 343;Line(Line_dup) = {595, 596};
CircleArc_dup = 345;Circle(CircleArc_dup) = {596, 11, 599};
interface_line_slot_opening___slot_dup = 346;Line(interface_line_slot_opening___slot_dup) = {594, 595};
upperLine4_dup = 350;Line(upperLine4_dup) = {599, 706};
CircleArc_dup = 352;Circle(CircleArc_dup) = {599, 11, 611};
Line_dup = 353;Line(Line_dup) = {611, 613};
Line_dup = 354;Line(Line_dup) = {614, 615};
CircleArc_dup = 356;Circle(CircleArc_dup) = {615, 11, 618};
interface_line_slot_opening___slot_dup = 357;Line(interface_line_slot_opening___slot_dup) = {613, 614};
upperLine4_dup = 361;Line(upperLine4_dup) = {618, 716};
CircleArc_dup = 363;Circle(CircleArc_dup) = {618, 11, 630};
Line_dup = 364;Line(Line_dup) = {630, 632};
Line_dup = 365;Line(Line_dup) = {633, 634};
CircleArc_dup = 367;Circle(CircleArc_dup) = {634, 11, 637};
interface_line_slot_opening___slot_dup = 368;Line(interface_line_slot_opening___slot_dup) = {632, 633};
upperLine4_dup = 372;Line(upperLine4_dup) = {637, 726};
CircleArc_dup = 374;Circle(CircleArc_dup) = {637, 11, 649};
Line_dup = 375;Line(Line_dup) = {649, 651};
Line_dup = 376;Line(Line_dup) = {652, 653};
CircleArc_dup = 378;Circle(CircleArc_dup) = {653, 11, 656};
interface_line_slot_opening___slot_dup = 379;Line(interface_line_slot_opening___slot_dup) = {651, 652};
upperLine4_dup = 383;Line(upperLine4_dup) = {656, 736};
CircleArc_dup = 385;Circle(CircleArc_dup) = {656, 11, 668};
Line_dup = 386;Line(Line_dup) = {668, 670};
Line_dup = 387;Line(Line_dup) = {671, 672};
CircleArc_dup = 389;Circle(CircleArc_dup) = {672, 11, 675};
interface_line_slot_opening___slot_dup = 390;Line(interface_line_slot_opening___slot_dup) = {670, 671};
upperLine4_dup = 394;Line(upperLine4_dup) = {675, 746};
CircleArc_dup = 396;Circle(CircleArc_dup) = {675, 11, 687};
Line_dup = 397;Line(Line_dup) = {687, 689};
Line_dup = 398;Line(Line_dup) = {690, 691};
CircleArc_dup = 400;Circle(CircleArc_dup) = {691, 11, 136};
interface_line_slot_opening___slot_dup = 401;Line(interface_line_slot_opening___slot_dup) = {689, 690};
Line_dup = 166;Line(Line_dup) = {599, 54};
Line_dup = 173;Line(Line_dup) = {594, 301};
Line_dup = 174;Line(Line_dup) = {301, 303};
CircleArc_dup = 176;Circle(CircleArc_dup) = {303, 305, 306};
CircleArc_dup = 178;Circle(CircleArc_dup) = {306, 305, 309};
Line_dup = 179;Line(Line_dup) = {309, 311};
Line_dup = 180;Line(Line_dup) = {311, 595};
Line_dup = 184;Line(Line_dup) = {618, 183};
Line_dup = 191;Line(Line_dup) = {613, 332};
Line_dup = 192;Line(Line_dup) = {332, 334};
CircleArc_dup = 194;Circle(CircleArc_dup) = {334, 336, 337};
CircleArc_dup = 196;Circle(CircleArc_dup) = {337, 336, 340};
Line_dup = 197;Line(Line_dup) = {340, 342};
Line_dup = 198;Line(Line_dup) = {342, 614};
Line_dup = 202;Line(Line_dup) = {637, 186};
Line_dup = 209;Line(Line_dup) = {632, 363};
Line_dup = 210;Line(Line_dup) = {363, 365};
CircleArc_dup = 212;Circle(CircleArc_dup) = {365, 367, 368};
CircleArc_dup = 214;Circle(CircleArc_dup) = {368, 367, 371};
Line_dup = 215;Line(Line_dup) = {371, 373};
Line_dup = 216;Line(Line_dup) = {373, 633};
Line_dup = 220;Line(Line_dup) = {656, 189};
Line_dup = 227;Line(Line_dup) = {651, 394};
Line_dup = 228;Line(Line_dup) = {394, 396};
CircleArc_dup = 230;Circle(CircleArc_dup) = {396, 398, 399};
CircleArc_dup = 232;Circle(CircleArc_dup) = {399, 398, 402};
Line_dup = 233;Line(Line_dup) = {402, 404};
Line_dup = 234;Line(Line_dup) = {404, 652};
Line_dup = 238;Line(Line_dup) = {675, 192};
Line_dup = 245;Line(Line_dup) = {670, 425};
Line_dup = 246;Line(Line_dup) = {425, 427};
CircleArc_dup = 248;Circle(CircleArc_dup) = {427, 429, 430};
CircleArc_dup = 250;Circle(CircleArc_dup) = {430, 429, 433};
Line_dup = 251;Line(Line_dup) = {433, 435};
Line_dup = 252;Line(Line_dup) = {435, 671};
Line_dup = 263;Line(Line_dup) = {689, 456};
Line_dup = 264;Line(Line_dup) = {456, 458};
CircleArc_dup = 266;Circle(CircleArc_dup) = {458, 460, 461};
CircleArc_dup = 268;Circle(CircleArc_dup) = {461, 460, 464};
Line_dup = 269;Line(Line_dup) = {464, 466};
Line_dup = 270;Line(Line_dup) = {466, 690};

// Surfaces

Curve Loop(37) = {335,83,-61,-75};
Surf_rotorAirGap2_dup = {37};
Plane Surface(Surf_rotorAirGap2_dup) = {37};

Curve Loop(20) = {150,151,152,153};
Surf_Magnet_dup = {20};
Plane Surface(Surf_Magnet_dup) = {20};

Curve Loop(22) = {157,158,159,160};
Surf_Magnet_dup = {22};
Plane Surface(Surf_Magnet_dup) = {22};

Curve Loop(19) = {145,146,147,149};
Surf_Loch_dup = {19};
Plane Surface(Surf_Loch_dup) = {19};

Curve Loop(21) = {154,155,156};
Surf_Loch_dup = {21};
Plane Surface(Surf_Loch_dup) = {21};

Curve Loop(23) = {161,162,163,165};
Surf_Loch_dup = {23};
Plane Surface(Surf_Loch_dup) = {23};

Curve Loop(36) = {329,82,-335,-74};
Surf_rotorAirGap1_dup = {36};
Plane Surface(Surf_rotorAirGap1_dup) = {36};

Curve Loop(14) = {145,146,147,149};
Surf_Loch_dup = {14};
Plane Surface(Surf_Loch_dup) = {14};
Curve Loop(15) = {150,151,152,153};
Surf_Magnet_dup = {15};
Plane Surface(Surf_Magnet_dup) = {15};
Curve Loop(16) = {154,155,156};
Surf_Loch_dup = {16};
Plane Surface(Surf_Loch_dup) = {16};
Curve Loop(17) = {157,158,159,160};
Surf_Magnet_dup = {17};
Plane Surface(Surf_Magnet_dup) = {17};
Curve Loop(18) = {161,162,163,165};
Surf_Loch_dup = {18};
Plane Surface(Surf_Loch_dup) = {18};
Curve Loop(13) = {72,329,-81,6};
Surf_Rotorblech_dup = {13};
Plane Surface(Surf_Rotorblech_dup) = {13, 14, 15, 16, 17, 18};

Curve Loop(44) = {407,-411,-69,77};
Surf_statorAirGap2_dup = {44};
Plane Surface(Surf_statorAirGap2_dup) = {44};

Curve Loop(45) = {413,-417,-85,411};
Surf_statorAirGap2_dup = {45};
Plane Surface(Surf_statorAirGap2_dup) = {45};

Curve Loop(46) = {419,-423,-87,417};
Surf_statorAirGap2_dup = {46};
Plane Surface(Surf_statorAirGap2_dup) = {46};

Curve Loop(47) = {425,-429,-89,423};
Surf_statorAirGap2_dup = {47};
Plane Surface(Surf_statorAirGap2_dup) = {47};

Curve Loop(48) = {431,-435,-91,429};
Surf_statorAirGap2_dup = {48};
Plane Surface(Surf_statorAirGap2_dup) = {48};

Curve Loop(49) = {437,-80,-93,435};
Surf_statorAirGap2_dup = {49};
Plane Surface(Surf_statorAirGap2_dup) = {49};

Curve Loop(38) = {341,342,346,343,345,350,-407,-76};
Surf_statorAirGap1_dup = {38};
Plane Surface(Surf_statorAirGap1_dup) = {38};

Curve Loop(39) = {352,353,357,354,356,361,-413,-350};
Surf_statorAirGap1_dup = {39};
Plane Surface(Surf_statorAirGap1_dup) = {39};

Curve Loop(40) = {363,364,368,365,367,372,-419,-361};
Surf_statorAirGap1_dup = {40};
Plane Surface(Surf_statorAirGap1_dup) = {40};

Curve Loop(41) = {374,375,379,376,378,383,-425,-372};
Surf_statorAirGap1_dup = {41};
Plane Surface(Surf_statorAirGap1_dup) = {41};

Curve Loop(42) = {385,386,390,387,389,394,-431,-383};
Surf_statorAirGap1_dup = {42};
Plane Surface(Surf_statorAirGap1_dup) = {42};

Curve Loop(43) = {396,397,401,398,400,79,-437,-394};
Surf_statorAirGap1_dup = {43};
Plane Surface(Surf_statorAirGap1_dup) = {43};

Curve Loop(24) = {166,30,73,341,342,173,174,176,178,179,180,343,345};
Surf_Statorblech_dup = {24};
Plane Surface(Surf_Statorblech_dup) = {24};

Curve Loop(25) = {184,109,-166,352,353,191,192,194,196,197,198,354,356};
Surf_Statorblech_dup = {25};
Plane Surface(Surf_Statorblech_dup) = {25};

Curve Loop(26) = {202,111,-184,363,364,209,210,212,214,215,216,365,367};
Surf_Statorblech_dup = {26};
Plane Surface(Surf_Statorblech_dup) = {26};

Curve Loop(27) = {220,113,-202,374,375,227,228,230,232,233,234,376,378};
Surf_Statorblech_dup = {27};
Plane Surface(Surf_Statorblech_dup) = {27};

Curve Loop(28) = {238,115,-220,385,386,245,246,248,250,251,252,387,389};
Surf_Statorblech_dup = {28};
Plane Surface(Surf_Statorblech_dup) = {28};

Curve Loop(29) = {78,-400,-398,-270,-269,-268,-266,-264,-263,-397,-396,238,-117};
Surf_Statorblech_dup = {29};
Plane Surface(Surf_Statorblech_dup) = {29};

Curve Loop(30) = {173,174,176,178,179,180,-346};
Surf_Stator_Nut_dup = {30};
Plane Surface(Surf_Stator_Nut_dup) = {30};

Curve Loop(31) = {191,192,194,196,197,198,-357};
Surf_Stator_Nut_dup = {31};
Plane Surface(Surf_Stator_Nut_dup) = {31};

Curve Loop(32) = {209,210,212,214,215,216,-368};
Surf_Stator_Nut_dup = {32};
Plane Surface(Surf_Stator_Nut_dup) = {32};

Curve Loop(33) = {227,228,230,232,233,234,-379};
Surf_Stator_Nut_dup = {33};
Plane Surface(Surf_Stator_Nut_dup) = {33};

Curve Loop(34) = {245,246,248,250,251,252,-390};
Surf_Stator_Nut_dup = {34};
Plane Surface(Surf_Stator_Nut_dup) = {34};

Curve Loop(35) = {263,264,266,268,269,270,-401};
Surf_Stator_Nut_dup = {35};
Plane Surface(Surf_Stator_Nut_dup) = {35};

// Color code
If (!Flag_individualColoring)
Color SkyBlue {Surface {37}; }
Color Red {Surface {20}; }
Color Red {Surface {22}; }
Color DodgerBlue2 {Surface {19}; }
Color Green4 {Surface {21}; }
Color SlateBlue {Surface {23}; }
Color SkyBlue {Surface {36}; }
Color SteelBlue {Surface {13}; }
Color SkyBlue {Surface {44}; }
Color SkyBlue {Surface {45}; }
Color SkyBlue {Surface {46}; }
Color SkyBlue {Surface {47}; }
Color SkyBlue {Surface {48}; }
Color SkyBlue {Surface {49}; }
Color SkyBlue {Surface {38}; }
Color SkyBlue {Surface {39}; }
Color SkyBlue {Surface {40}; }
Color SkyBlue {Surface {41}; }
Color SkyBlue {Surface {42}; }
Color SkyBlue {Surface {43}; }
Color SteelBlue4 {Surface {24}; }
Color SteelBlue4 {Surface {25}; }
Color SteelBlue4 {Surface {26}; }
Color SteelBlue4 {Surface {27}; }
Color SteelBlue4 {Surface {28}; }
Color SteelBlue4 {Surface {29}; }
Color Magenta {Surface {30}; }
Color Magenta {Surface {31}; }
Color Cyan {Surface {32}; }
Color Cyan {Surface {33}; }
Color Yellow4 {Surface {34}; }
Color Yellow4 {Surface {35}; }
EndIf

// Physical Elements
// primaryLineS
Physical Curve("primaryLineS", 1002) = {73,76,77};
// primaryLineR
Physical Curve("primaryLineR", 1001) = {72,74,75};
// slaveLineS
Physical Curve("slaveLineS", 1004) = {78,79,80};
// slaveLineR
Physical Curve("slaveLineR", 1003) = {81,82,83};
// innerLimit
Physical Curve("innerLimit", 1015) = {6};
// Rotor_Bnd_MB_1
Physical Curve("Rotor_Bnd_MB_1", 1006) = {61};
// Rotor_Bnd_MB_2
Physical Curve("Rotor_Bnd_MB_2", 1007) = {95};
// Rotor_Bnd_MB_3
Physical Curve("Rotor_Bnd_MB_3", 1008) = {97};
// Rotor_Bnd_MB_4
Physical Curve("Rotor_Bnd_MB_4", 1009) = {99};
// Rotor_Bnd_MB_5
Physical Curve("Rotor_Bnd_MB_5", 1010) = {101};
// Rotor_Bnd_MB_6
Physical Curve("Rotor_Bnd_MB_6", 1011) = {103};
// Rotor_Bnd_MB_7
Physical Curve("Rotor_Bnd_MB_7", 1012) = {105};
// Rotor_Bnd_MB_8
Physical Curve("Rotor_Bnd_MB_8", 1013) = {107};
// LuR2
Physical Surface("LuR2", 1030) = {37};
// Mag0_0
Physical Surface("Mag0_0", 1018) = {20};
// Mag1_0
Physical Surface("Mag1_0", 1020) = {22};
// Lpl0
Physical Surface("Lpl0", 1017) = {19};
// Lpl1
Physical Surface("Lpl1", 1019) = {21};
// Lpl2
Physical Surface("Lpl2", 1021) = {23};
// LuR1
Physical Surface("LuR1", 1029) = {36};
// Pol
Physical Surface("Pol", 1016) = {13};
// outerLimit
Physical Curve("outerLimit", 1014) = {30,109,111,113,115,117};
// mbStator
Physical Curve("mbStator", 1005) = {69,85,87,89,91,93};
// StLu2
Physical Surface("StLu2", 1032) = {44,45,46,47,48,49};
// StLu1
Physical Surface("StLu1", 1031) = {38,39,40,41,42,43};
// StNut
Physical Surface("StNut", 1022) = {24,25,26,27,28,29};
// StCu0_0_Up
Physical Surface("StCu0_0_Up", 1023) = {30};
// StCu0_1_Up
Physical Surface("StCu0_1_Up", 1024) = {31};
// StCu0_2_Wn
Physical Surface("StCu0_2_Wn", 1025) = {32};
// StCu0_3_Wn
Physical Surface("StCu0_3_Wn", 1026) = {33};
// StCu0_4_Vp
Physical Surface("StCu0_4_Vp", 1027) = {34};
// StCu0_5_Vp
Physical Surface("StCu0_5_Vp", 1028) = {35};

DefineConstant[
	mm = 1e-3,
	Flag_SpecifyMeshSize = {0, Name StrCat[INPUT_MESH, "04User defined surface mesh sizes"],Choices {0, 1}}
];
If(Flag_SpecifyMeshSize)
	DefineConstant[
		Lpl_msf = {0.824, Name StrCat[INPUT_MESH, "05Mesh Size/Loch (Polluecke) [mm]"],Min 0.0824, Max 8.24, Step 0.1,Visible Flag_SpecifyMeshSize},
		Mag_msf = {1.0, Name StrCat[INPUT_MESH, "05Mesh Size/Magnet [mm]"],Min 0.1, Max 10.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		Pol_msf = {2.636, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorblech [mm]"],Min 0.2636, Max 26.36, Step 0.1,Visible Flag_SpecifyMeshSize},
		LuR_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorluftspalt [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		LuR1_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorluftspalt 1 [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		LuR2_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorluftspalt 2 [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		StCu_msf = {1.799, Name StrCat[INPUT_MESH, "05Mesh Size/Stator-Nut [mm]"],Min 0.1799, Max 17.99, Step 0.1,Visible Flag_SpecifyMeshSize},
		StNut_msf = {1.973, Name StrCat[INPUT_MESH, "05Mesh Size/Statorblech [mm]"],Min 0.1973, Max 19.73, Step 0.1,Visible Flag_SpecifyMeshSize},
		StLu_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Statorluftspalt [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		StLu1_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Statorluftspalt 1 [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		StLu2_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Statorluftspalt 2 [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize}
	];
	MeshSize { PointsOf {Surface{ 19,21,23 };} } = Lpl_msf*mm;
	MeshSize { PointsOf {Surface{ 20,22 };} } = Mag_msf*mm;
	MeshSize { PointsOf {Surface{ 13 };} } = Pol_msf*mm;
	MeshSize { PointsOf {Surface{ 36,37 };} } = LuR_msf*mm;
	MeshSize { PointsOf {Surface{ 36 };} } = LuR1_msf*mm;
	MeshSize { PointsOf {Surface{ 37 };} } = LuR2_msf*mm;
	MeshSize { PointsOf {Surface{ 30,31,32,33,34,35 };} } = StCu_msf*mm;
	MeshSize { PointsOf {Surface{ 24,25,26,27,28,29 };} } = StNut_msf*mm;
	MeshSize { PointsOf {Surface{ 38,39,40,41,42,43,44,45,46,47,48,49 };} } = StLu_msf*mm;
	MeshSize { PointsOf {Surface{ 38,39,40,41,42,43 };} } = StLu1_msf*mm;
	MeshSize { PointsOf {Surface{ 44,45,46,47,48,49 };} } = StLu2_msf*mm;
EndIf

// Mesh operations

// Do not switch mesh algorithm on failure, because this led to mesh errors in the past.
Mesh.AlgorithmSwitchOnFailure = 0;DefineConstant[Flag_CompoundMesh = {0, Name StrCat[INPUT_MESH, "Compound Mesh"], Choices {0,1}, Help "Use Compound Mesh to ignore lines between segments while meshing.",Visible Flag_ExpertMode}];
If (Flag_CompoundMesh)
Compound Surface{24,25,26,27,28,29}; // stator domainLam
Compound Surface{44,45,46,47,48,49}; // stator airGap
EndIf // (Flag_CompoundMesh)

// Add Periodic Mesh to model symmetry boundary-lines
primaryLines = {72,74,75,73,76,77};
secondaryLines = {81,82,83,78,79,80};
Periodic Curve{secondaryLines[]} = {primaryLines[]} Rotate {{0,0,1}, {0,0,0}, 2*Pi/8};

// Add mesh size setting for Movingband lines
DefineConstant[
	NbrMbSegments = {3370.0, Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],Max 1440, Min 180, Step 10, Help "Set the number of mesh segments on the interface between rotor/statorairgap and movingband. Value represents number of segments on whole circle.", Visible Flag_ExpertMode},
	r_MB_R = 0.08049999999999999
];
MB_LinesR = {61,95,97,99,101,103,105,107};
MeshSize{ PointsOf{Line{MB_LinesR[]};}} = 2*Pi*r_MB_R/NbrMbSegments;

MB_LinesS = {69,85,87,89,91,93};
MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*0.08065/NbrMbSegments;

Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)

// Create boundary lines for moving rotor contour plot
rotorBndLines[] = Boundary{ Physical Surface{ 1018,1020 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 1016 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 1030 }; };
statorBndLines[] = Boundary{ Physical Surface{ 1002,1004,1005,1014,1022,1023,1024,1025,1026,1027,1028,1031,1032 }; };
Physical Line("DomainPlotMovingGeo",1) = {rotorBndLines[], statorBndLines[]};
