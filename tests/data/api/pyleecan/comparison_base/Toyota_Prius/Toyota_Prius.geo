// This script was created with pyemmo (Version 1.3.1b1, git 61d59c)

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
point_pylc_dup = 187; Point(187) = {0.13462, 0.0, 0, 0.001*gmsf};
point_pylc_dup = 188; Point(188) = {0.08095, 0.0, 0, 0.001*gmsf};
PointM41_dup = 194; Point(194) = {0.0808, 0, 0, 0.0014076080417334267*gmsf};
PointM31_dup = 195; Point(195) = {0.08065, 0, 0, 0.0014076080417334267*gmsf};
point_pylc_dup = 185; Point(185) = {0.05532, 0.0, 0, 0.001*gmsf};
point_pylc_dup = 186; Point(186) = {0.0802, 0.0, 0, 0.001*gmsf};
PointM11_dup = 190; Point(190) = {0.08034999999999999, 0, 0, 0.0014049900478554352*gmsf};
PointM21_dup = 192; Point(192) = {0.08049999999999999, 0, 0, 0.0014049900478554352*gmsf};
point_pylc_dup = 197; Point(197) = {0.09519071488333303, 0.09519071488333303, 0.0, 0.001*gmsf};
point_pylc_dup = 198; Point(198) = {0.057240293937051025, 0.057240293937051025, 0.0, 0.001*gmsf};
PointM41_dup = 200; Point(200) = {0.05713422791987304, 0.05713422791987304, 0.0, 0.0014076080417334267*gmsf};
PointM31_dup = 201; Point(201) = {0.05702816190269506, 0.05702816190269506, 0.0, 0.0014076080417334267*gmsf};
point_pylc_dup = 203; Point(203) = {0.03911714713523981, 0.03911714713523981, 0.0, 0.001*gmsf};
point_pylc_dup = 204; Point(204) = {0.05670996385116111, 0.05670996385116111, 0.0, 0.001*gmsf};
PointM11_dup = 206; Point(206) = {0.05681602986833909, 0.05681602986833909, 0.0, 0.0014049900478554352*gmsf};
PointM21_dup = 208; Point(208) = {0.05692209588551707, 0.05692209588551707, 0.0, 0.0014049900478554352*gmsf};
point_pylc = 11; Point(11) = {0, 0, 0, 0.001*gmsf};
PointM22_dup = 226; Point(226) = {0.0, 0.08049999999999999, 0.0, 0.0014049900478554352*gmsf};
PointM22_dup = 229; Point(229) = {-0.05692209588551706, 0.056922095885517075, 0.0, 0.0014049900478554352*gmsf};
PointM22_dup = 232; Point(232) = {-0.08049999999999999, 0.0, 0.0, 0.0014049900478554352*gmsf};
PointM22_dup = 235; Point(235) = {-0.056922095885517075, -0.05692209588551706, 0.0, 0.0014049900478554352*gmsf};
PointM22_dup = 238; Point(238) = {-6.938893903907228e-18, -0.08049999999999999, 0.0, 0.0014049900478554352*gmsf};
PointM22_dup = 241; Point(241) = {0.056922095885517054, -0.05692209588551708, 0.0, 0.0014049900478554352*gmsf};
point_pylc_dup = 335; Point(335) = {0.07189332074897073, 0.008478350008583092, 0, 0.001*gmsf};
point_pylc_dup = 336; Point(336) = {0.07112686475225904, 0.007836053188487666, 0, 0.001*gmsf};
point_pylc_dup = 338; Point(338) = {0.058987454852455525, 0.02232207152633855, 0, 0.001*gmsf};
point_pylc_dup = 340; Point(340) = {0.059753910849167216, 0.02296436834643398, 0, 0.001*gmsf};
point_pylc_dup = 342; Point(342) = {0.0639694188310815, 0.026497000856958816, 0, 0.001*gmsf};
point_pylc_dup = 344; Point(344) = {0.07610882873088501, 0.01201098251910793, 0, 0.001*gmsf};
point_pylc_dup = 355; Point(355) = {0.056831353407958855, 0.0448411558392746, 0, 0.001*gmsf};
point_pylc_dup = 356; Point(356) = {0.055835214738178894, 0.0447533620435427, 0, 0.001*gmsf};
point_pylc_dup = 358; Point(358) = {0.057494517477511754, 0.02592634118470148, 0, 0.001*gmsf};
point_pylc_dup = 360; Point(360) = {0.05849065614729172, 0.026014134980433378, 0, 0.001*gmsf};
point_pylc_dup = 364; Point(364) = {0.06231011609174863, 0.045324021715800036, 0, 0.001*gmsf};
point_pylc_dup = 324; Point(324) = {0.07838807307237497, 0.007000000000000003, 0, 0.001*gmsf};
point_pylc_dup = 325; Point(325) = {0.07313219096927659, 0.007000000000000003, 0, 0.001*gmsf};
point_pylc_dup = 331; Point(331) = {0.07810937152746876, 0.009623724828976162, 0, 0.001*gmsf};
point_pylc_dup = 348; Point(348) = {0.05864256321587955, 0.024290545016338896, 0, 0.001*gmsf};
point_pylc_dup = 367; Point(367) = {0.06037848550192878, 0.050478990565317114, 0, 0.001*gmsf};
point_pylc_dup = 368; Point(368) = {0.05666201562571091, 0.04676252068909924, 0, 0.001*gmsf};
point_pylc_dup = 374; Point(374) = {0.06203666736813499, 0.048426665194450214, 0, 0.001*gmsf};
point_pylc = 68; Point(68) = {0.13346830723814235, 0.017571435996663342, 0, 0.001*gmsf};
point_pylc_dup = 245; Point(245) = {0.13003293473503436, 0.034842219851701335, 0.0, 0.001*gmsf};
point_pylc_dup = 248; Point(248) = {0.12437266266666941, 0.051516843664988377, 0.0, 0.001*gmsf};
point_pylc_dup = 251; Point(251) = {0.11658433985746111, 0.06731, 0.0, 0.001*gmsf};
point_pylc_dup = 254; Point(254) = {0.10680122667000608, 0.08195146357315396, 0.0, 0.001*gmsf};
PointM32 = 184; Point(184) = {0.07996002806979781, 0.010526937402547159, 0, 0.0014076080417334267*gmsf};
PointM32_dup = 211; Point(211) = {0.07790191789021336, 0.020873755987518297, 0.0, 0.0014076080417334267*gmsf};
PointM32_dup = 214; Point(214) = {0.07451088429703527, 0.030863418820244487, 0.0, 0.0014076080417334267*gmsf};
PointM32_dup = 217; Point(217) = {0.06984494881521497, 0.040325, 0.0, 0.0014076080417334267*gmsf};
PointM32_dup = 220; Point(220) = {0.06398394689448812, 0.04909660924955331, 0.0, 0.0014076080417334267*gmsf};
PointM42_dup = 796; Point(796) = {0.08010874479900387, 0.010546516331380167, 0, 0.0014076080417334267*gmsf};
PointM42_dup = 806; Point(806) = {0.0780468067641567, 0.020912578844283672, 0.0, 0.0014076080417334267*gmsf};
PointM42_dup = 816; Point(816) = {0.07464946622691196, 0.030920821335099248, 0.0, 0.0014076080417334267*gmsf};
PointM42_dup = 826; Point(826) = {0.06997485262578262, 0.04039999999999999, 0.0, 0.0014076080417334267*gmsf};
PointM42_dup = 836; Point(836) = {0.06410294989553181, 0.04918792346390462, 0.0, 0.0014076080417334267*gmsf};
point_pylc_dup = 682; Point(682) = {0.08083405411411097, 0.004331073247704142, 0, 0.001*gmsf};
point_pylc_dup = 684; Point(684) = {0.08183191303734956, 0.004396476376934286, 0, 0.001*gmsf};
point_pylc_dup = 685; Point(685) = {0.08170568499793539, 0.00632234409878479, 0, 0.001*gmsf};
point_pylc_dup = 686; Point(686) = {0.08070782607469679, 0.0062569409695546465, 0, 0.001*gmsf};
point_pylc_dup = 689; Point(689) = {0.08025746152820995, 0.010566095260213175, 0, 0.001*gmsf};
point_pylc_dup = 701; Point(701) = {0.07957718907619889, 0.014844981600894352, 0.0, 0.001*gmsf};
point_pylc_dup = 703; Point(703) = {0.0805579743566021, 0.015040071922910478, 0.0, 0.001*gmsf};
point_pylc_dup = 704; Point(704) = {0.08018145003511097, 0.016932987514088713, 0.0, 0.001*gmsf};
point_pylc_dup = 705; Point(705) = {0.07920066475470774, 0.01673789719207258, 0.0, 0.001*gmsf};
point_pylc_dup = 708; Point(708) = {0.07819169563810008, 0.020951401701049054, 0.0, 0.001*gmsf};
point_pylc_dup = 720; Point(720) = {0.07695873627022805, 0.02510488820308679, 0.0, 0.001*gmsf};
point_pylc_dup = 722; Point(722) = {0.07790566639972313, 0.02542632766838995, 0.0, 0.001*gmsf};
point_pylc_dup = 723; Point(723) = {0.07728528823168804, 0.027253902818315502, 0.0, 0.001*gmsf};
point_pylc_dup = 724; Point(724) = {0.07633835810219293, 0.026932463353012342, 0.0, 0.001*gmsf};
point_pylc_dup = 727; Point(727) = {0.07478804815678866, 0.030978223849954016, 0.0, 0.001*gmsf};
point_pylc_dup = 739; Point(739) = {0.07302349814968086, 0.03493524320773444, 0.0, 0.001*gmsf};
point_pylc_dup = 741; Point(741) = {0.07392037089121353, 0.03537753189795343, 0.0, 0.001*gmsf};
point_pylc_dup = 742; Point(742) = {0.07306675371909087, 0.03710849628911152, 0.0, 0.001*gmsf};
point_pylc_dup = 743; Point(743) = {0.07216988097755818, 0.036666207598892525, 0.0, 0.001*gmsf};
point_pylc_dup = 746; Point(746) = {0.07010475643635031, 0.040475, 0.0, 0.001*gmsf};
point_pylc_dup = 758; Point(758) = {0.06783880772985405, 0.04416784651521844, 0.0, 0.001*gmsf};
point_pylc_dup = 760; Point(760) = {0.0686702773421566, 0.044723416748238036, 0.0, 0.001*gmsf};
point_pylc_dup = 761; Point(761) = {0.06759802679242875, 0.04632815309998195, 0.0, 0.001*gmsf};
point_pylc_dup = 762; Point(762) = {0.06676655718012621, 0.04577258286696235, 0.0, 0.001*gmsf};
point_pylc_dup = 765; Point(765) = {0.0642219528965755, 0.04927923767825593, 0.0, 0.001*gmsf};
point_pylc_dup = 777; Point(777) = {0.0614933765012986, 0.05264472572318653, 0.0, 0.001*gmsf};
point_pylc_dup = 779; Point(779) = {0.06224521630877756, 0.05330407153828659, 0.0, 0.001*gmsf};
point_pylc_dup = 780; Point(780) = {0.06097267888563443, 0.05475512236672102, 0.0, 0.001*gmsf};
point_pylc_dup = 781; Point(781) = {0.06022083907815545, 0.054095776551620955, 0.0, 0.001*gmsf};
point_pylc_dup = 391; Point(391) = {0.08193230684071783, 0.002864762929763029, 0, 0.001*gmsf};
point_pylc_dup = 393; Point(393) = {0.11126767798545414, 0.0032842862313483155, 0, 0.001*gmsf};
point_pylc_dup = 396; Point(396) = {0.11499750116148799, 0.007537334441223301, 0, 0.001*gmsf};
point_pylc_dup = 395; Point(395) = {0.11100606546853357, 0.0072757219243027305, 0, 0.001*gmsf};
point_pylc_dup = 399; Point(399) = {0.110744452951613, 0.011267157617257145, 0, 0.001*gmsf};
point_pylc_dup = 401; Point(401) = {0.08160529119456712, 0.007854057545956047, 0, 0.001*gmsf};
point_pylc_dup = 422; Point(422) = {0.08085743800089684, 0.013534566517491518, 0.0, 0.001*gmsf};
point_pylc_dup = 424; Point(424) = {0.10988708219973571, 0.017779535031959233, 0.0, 0.001*gmsf};
point_pylc_dup = 427; Point(427) = {0.11302986203328413, 0.022483037441636666, 0.0, 0.001*gmsf};
point_pylc_dup = 426; Point(426) = {0.10910672091167122, 0.021702676153572156, 0.0, 0.001*gmsf};
point_pylc_dup = 430; Point(430) = {0.1083263596236067, 0.025625817275185078, 0.0, 0.001*gmsf};
point_pylc_dup = 432; Point(432) = {0.07988198639081623, 0.018438492919507672, 0.0, 0.001*gmsf};
point_pylc_dup = 453; Point(453) = {0.07839907597896349, 0.023972789919614962, 0.0, 0.001*gmsf};
point_pylc_dup = 455; Point(455) = {0.10662628797112485, 0.03197057105875494, 0.0, 0.001*gmsf};
point_pylc_dup = 458; Point(458) = {0.10912825062789262, 0.037044049437948014, 0.0, 0.001*gmsf};
point_pylc_dup = 457; Point(457) = {0.10534053010991219, 0.035758291576735365, 0.0, 0.001*gmsf};
point_pylc_dup = 461; Point(461) = {0.10405477224869955, 0.03954601209471579, 0.0, 0.001*gmsf};
point_pylc_dup = 463; Point(463) = {0.07679187865244769, 0.028707440567090493, 0.0, 0.001*gmsf};
point_pylc_dup = 484; Point(484) = {0.0745992840306997, 0.034000832239700754, 0.0, 0.001*gmsf};
point_pylc_dup = 486; Point(486) = {0.10154108839293599, 0.045614581750818464, 0.0, 0.001*gmsf};
point_pylc_dup = 489; Point(489) = {0.10335942459819074, 0.05097122747782523, 0.0, 0.001*gmsf};
point_pylc_dup = 488; Point(488) = {0.09977193363205998, 0.04920207271694922, 0.0, 0.001*gmsf};
point_pylc_dup = 492; Point(492) = {0.09800277887118398, 0.05278956368307998, 0.0, 0.001*gmsf};
point_pylc_dup = 494; Point(494) = {0.07238784057960469, 0.0384851959473642, 0.0, 0.001*gmsf};
point_pylc_dup = 515; Point(515) = {0.06952307764984167, 0.043447110893353624, 0.0, 0.001*gmsf};
point_pylc_dup = 517; Point(517) = {0.09471849263983566, 0.058478114302374165, 0.0, 0.001*gmsf};
point_pylc_dup = 520; Point(520) = {0.09582209015696745, 0.06402627368366276, 0.0, 0.001*gmsf};
point_pylc_dup = 519; Point(519) = {0.09249621170775726, 0.061803992751584345, 0.0, 0.001*gmsf};
point_pylc_dup = 523; Point(523) = {0.09027393077567886, 0.06512987120079453, 0.0, 0.001*gmsf};
point_pylc_dup = 525; Point(525) = {0.06674522648474367, 0.047604458954866355, 0.0, 0.001*gmsf};
point_pylc_dup = 546; Point(546) = {0.06325731213495615, 0.05214999743380636, 0.0, 0.001*gmsf};
point_pylc_dup = 548; Point(548) = {0.08627523721674032, 0.07034107010501991, 0.0, 0.001*gmsf};
point_pylc_dup = 551; Point(551) = {0.08664521318625597, 0.0759858125953361, 0.0, 0.001*gmsf};
point_pylc_dup = 550; Point(550) = {0.08363785395634005, 0.07334842933493584, 0.0, 0.001*gmsf};
point_pylc_dup = 554; Point(554) = {0.08100047069593977, 0.07635578856485174, 0.0, 0.001*gmsf};
point_pylc_dup = 556; Point(556) = {0.05996058305945583, 0.05590919647120125, 0.0, 0.001*gmsf};

// Lines and Curves
Line_dup = 80;Line(Line_dup) = {187, 188}; 
lowerLine4_dup = 83;Line(lowerLine4_dup) = {188, 194}; 
lowerLine3_dup = 84;Line(lowerLine3_dup) = {195, 194}; 
Line_dup = 79;Line(Line_dup) = {185, 186}; 
lowerLine1_dup = 81;Line(lowerLine1_dup) = {186, 190}; 
lowerLine2_dup = 82;Line(lowerLine2_dup) = {190, 192}; 
Line_dup = 85;Line(Line_dup) = {197, 198}; 
lowerLine4_dup = 86;Line(lowerLine4_dup) = {198, 200}; 
lowerLine3_dup = 87;Line(lowerLine3_dup) = {201, 200}; 
Line_dup = 88;Line(Line_dup) = {203, 204}; 
lowerLine1_dup = 89;Line(lowerLine1_dup) = {204, 206}; 
lowerLine2_dup = 90;Line(lowerLine2_dup) = {206, 208}; 
InnerLimit = 6;Circle(InnerLimit) = {203, 11, 185}; 
MB_CurveRotor = 68;Circle(MB_CurveRotor) = {192, 11, 208}; 
MB_CurveRotor_dup = 102;Circle(MB_CurveRotor_dup) = {208, 11, 226}; 
MB_CurveRotor_dup = 104;Circle(MB_CurveRotor_dup) = {226, 11, 229}; 
MB_CurveRotor_dup = 106;Circle(MB_CurveRotor_dup) = {229, 11, 232}; 
MB_CurveRotor_dup = 108;Circle(MB_CurveRotor_dup) = {232, 11, 235}; 
MB_CurveRotor_dup = 110;Circle(MB_CurveRotor_dup) = {235, 11, 238}; 
MB_CurveRotor_dup = 112;Circle(MB_CurveRotor_dup) = {238, 11, 241}; 
MB_CurveRotor_dup = 114;Circle(MB_CurveRotor_dup) = {241, 11, 192}; 
rotorBand1_dup = 356;Circle(rotorBand1_dup) = {190, 11, 206}; 
Line_dup = 165;Line(Line_dup) = {335, 336}; 
Line_dup = 166;Line(Line_dup) = {336, 338}; 
Line_dup = 167;Line(Line_dup) = {338, 340}; 
Line_dup = 168;Line(Line_dup) = {340, 342}; 
Line_dup = 169;Line(Line_dup) = {342, 344}; 
Line_dup = 170;Line(Line_dup) = {344, 335}; 
Line_dup = 175;Line(Line_dup) = {355, 356}; 
Line_dup = 176;Line(Line_dup) = {356, 358}; 
Line_dup = 177;Line(Line_dup) = {358, 360}; 
Line_dup = 178;Line(Line_dup) = {360, 342}; 
Line_dup = 179;Line(Line_dup) = {342, 364}; 
Line_dup = 180;Line(Line_dup) = {364, 355}; 
Line_dup = 159;Line(Line_dup) = {324, 325}; 
Line_dup = 160;Line(Line_dup) = {325, 335}; 
Line_dup = 162;Line(Line_dup) = {344, 331}; 
CircleArc_dup = 164;Circle(CircleArc_dup) = {331, 11, 324}; 
Line_dup = 171;Line(Line_dup) = {340, 348}; 
Line_dup = 172;Line(Line_dup) = {348, 360}; 
Line_dup = 181;Line(Line_dup) = {367, 368}; 
Line_dup = 182;Line(Line_dup) = {368, 355}; 
Line_dup = 184;Line(Line_dup) = {364, 374}; 
CircleArc_dup = 186;Circle(CircleArc_dup) = {374, 11, 367}; 
CircleArc_dup = 350;Circle(CircleArc_dup) = {186, 11, 204}; 
OuterLimit = 37;Circle(OuterLimit) = {68, 11, 187}; 
OuterLimit_dup = 116;Circle(OuterLimit_dup) = {245, 11, 68}; 
OuterLimit_dup = 118;Circle(OuterLimit_dup) = {248, 11, 245}; 
OuterLimit_dup = 120;Circle(OuterLimit_dup) = {251, 11, 248}; 
OuterLimit_dup = 122;Circle(OuterLimit_dup) = {254, 11, 251}; 
OuterLimit_dup = 124;Circle(OuterLimit_dup) = {197, 11, 254}; 
MB_CurveStator = 76;Circle(MB_CurveStator) = {195, 11, 184}; 
MB_CurveStator_dup = 92;Circle(MB_CurveStator_dup) = {184, 11, 211}; 
MB_CurveStator_dup = 94;Circle(MB_CurveStator_dup) = {211, 11, 214}; 
MB_CurveStator_dup = 96;Circle(MB_CurveStator_dup) = {214, 11, 217}; 
MB_CurveStator_dup = 98;Circle(MB_CurveStator_dup) = {217, 11, 220}; 
MB_CurveStator_dup = 100;Circle(MB_CurveStator_dup) = {220, 11, 201}; 
statorCircle4_dup = 428;Circle(statorCircle4_dup) = {194, 11, 796}; 
upperLine3_dup = 432;Line(upperLine3_dup) = {184, 796}; 
statorCircle4_dup = 434;Circle(statorCircle4_dup) = {796, 11, 806}; 
upperLine3_dup = 438;Line(upperLine3_dup) = {211, 806}; 
statorCircle4_dup = 440;Circle(statorCircle4_dup) = {806, 11, 816}; 
upperLine3_dup = 444;Line(upperLine3_dup) = {214, 816}; 
statorCircle4_dup = 446;Circle(statorCircle4_dup) = {816, 11, 826}; 
upperLine3_dup = 450;Line(upperLine3_dup) = {217, 826}; 
statorCircle4_dup = 452;Circle(statorCircle4_dup) = {826, 11, 836}; 
upperLine3_dup = 456;Line(upperLine3_dup) = {220, 836}; 
statorCircle4_dup = 458;Circle(statorCircle4_dup) = {836, 11, 200}; 
CircleArc_dup = 362;Circle(CircleArc_dup) = {188, 11, 682}; 
Line_dup = 363;Line(Line_dup) = {682, 684}; 
Line_dup = 364;Line(Line_dup) = {685, 686}; 
CircleArc_dup = 366;Circle(CircleArc_dup) = {686, 11, 689}; 
interface_line_slot_opening___slot_dup = 367;Line(interface_line_slot_opening___slot_dup) = {684, 685}; 
upperLine4_dup = 371;Line(upperLine4_dup) = {689, 796}; 
CircleArc_dup = 373;Circle(CircleArc_dup) = {689, 11, 701}; 
Line_dup = 374;Line(Line_dup) = {701, 703}; 
Line_dup = 375;Line(Line_dup) = {704, 705}; 
CircleArc_dup = 377;Circle(CircleArc_dup) = {705, 11, 708}; 
interface_line_slot_opening___slot_dup = 378;Line(interface_line_slot_opening___slot_dup) = {703, 704}; 
upperLine4_dup = 382;Line(upperLine4_dup) = {708, 806}; 
CircleArc_dup = 384;Circle(CircleArc_dup) = {708, 11, 720}; 
Line_dup = 385;Line(Line_dup) = {720, 722}; 
Line_dup = 386;Line(Line_dup) = {723, 724}; 
CircleArc_dup = 388;Circle(CircleArc_dup) = {724, 11, 727}; 
interface_line_slot_opening___slot_dup = 389;Line(interface_line_slot_opening___slot_dup) = {722, 723}; 
upperLine4_dup = 393;Line(upperLine4_dup) = {727, 816}; 
CircleArc_dup = 395;Circle(CircleArc_dup) = {727, 11, 739}; 
Line_dup = 396;Line(Line_dup) = {739, 741}; 
Line_dup = 397;Line(Line_dup) = {742, 743}; 
CircleArc_dup = 399;Circle(CircleArc_dup) = {743, 11, 746}; 
interface_line_slot_opening___slot_dup = 400;Line(interface_line_slot_opening___slot_dup) = {741, 742}; 
upperLine4_dup = 404;Line(upperLine4_dup) = {746, 826}; 
CircleArc_dup = 406;Circle(CircleArc_dup) = {746, 11, 758}; 
Line_dup = 407;Line(Line_dup) = {758, 760}; 
Line_dup = 408;Line(Line_dup) = {761, 762}; 
CircleArc_dup = 410;Circle(CircleArc_dup) = {762, 11, 765}; 
interface_line_slot_opening___slot_dup = 411;Line(interface_line_slot_opening___slot_dup) = {760, 761}; 
upperLine4_dup = 415;Line(upperLine4_dup) = {765, 836}; 
CircleArc_dup = 417;Circle(CircleArc_dup) = {765, 11, 777}; 
Line_dup = 418;Line(Line_dup) = {777, 779}; 
Line_dup = 419;Line(Line_dup) = {780, 781}; 
CircleArc_dup = 421;Circle(CircleArc_dup) = {781, 11, 198}; 
interface_line_slot_opening___slot_dup = 422;Line(interface_line_slot_opening___slot_dup) = {779, 780}; 
Line_dup = 187;Line(Line_dup) = {689, 68}; 
Line_dup = 194;Line(Line_dup) = {684, 391}; 
Line_dup = 195;Line(Line_dup) = {391, 393}; 
CircleArc_dup = 197;Circle(CircleArc_dup) = {393, 395, 396}; 
CircleArc_dup = 199;Circle(CircleArc_dup) = {396, 395, 399}; 
Line_dup = 200;Line(Line_dup) = {399, 401}; 
Line_dup = 201;Line(Line_dup) = {401, 685}; 
Line_dup = 205;Line(Line_dup) = {708, 245}; 
Line_dup = 212;Line(Line_dup) = {703, 422}; 
Line_dup = 213;Line(Line_dup) = {422, 424}; 
CircleArc_dup = 215;Circle(CircleArc_dup) = {424, 426, 427}; 
CircleArc_dup = 217;Circle(CircleArc_dup) = {427, 426, 430}; 
Line_dup = 218;Line(Line_dup) = {430, 432}; 
Line_dup = 219;Line(Line_dup) = {432, 704}; 
Line_dup = 223;Line(Line_dup) = {727, 248}; 
Line_dup = 230;Line(Line_dup) = {722, 453}; 
Line_dup = 231;Line(Line_dup) = {453, 455}; 
CircleArc_dup = 233;Circle(CircleArc_dup) = {455, 457, 458}; 
CircleArc_dup = 235;Circle(CircleArc_dup) = {458, 457, 461}; 
Line_dup = 236;Line(Line_dup) = {461, 463}; 
Line_dup = 237;Line(Line_dup) = {463, 723}; 
Line_dup = 241;Line(Line_dup) = {746, 251}; 
Line_dup = 248;Line(Line_dup) = {741, 484}; 
Line_dup = 249;Line(Line_dup) = {484, 486}; 
CircleArc_dup = 251;Circle(CircleArc_dup) = {486, 488, 489}; 
CircleArc_dup = 253;Circle(CircleArc_dup) = {489, 488, 492}; 
Line_dup = 254;Line(Line_dup) = {492, 494}; 
Line_dup = 255;Line(Line_dup) = {494, 742}; 
Line_dup = 259;Line(Line_dup) = {765, 254}; 
Line_dup = 266;Line(Line_dup) = {760, 515}; 
Line_dup = 267;Line(Line_dup) = {515, 517}; 
CircleArc_dup = 269;Circle(CircleArc_dup) = {517, 519, 520}; 
CircleArc_dup = 271;Circle(CircleArc_dup) = {520, 519, 523}; 
Line_dup = 272;Line(Line_dup) = {523, 525}; 
Line_dup = 273;Line(Line_dup) = {525, 761}; 
Line_dup = 284;Line(Line_dup) = {779, 546}; 
Line_dup = 285;Line(Line_dup) = {546, 548}; 
CircleArc_dup = 287;Circle(CircleArc_dup) = {548, 550, 551}; 
CircleArc_dup = 289;Circle(CircleArc_dup) = {551, 550, 554}; 
Line_dup = 290;Line(Line_dup) = {554, 556}; 
Line_dup = 291;Line(Line_dup) = {556, 780}; 

// Surfaces

Curve Loop(37) = {356,90,-68,-82};
Surf_rotorAirGap2_dup = {37};
Plane Surface(Surf_rotorAirGap2_dup) = {37};

Curve Loop(20) = {165,166,167,168,169,170};
Surf_Magnet_dup = {20};
Plane Surface(Surf_Magnet_dup) = {20};

Curve Loop(22) = {175,176,177,178,179,180};
Surf_Magnet_dup = {22};
Plane Surface(Surf_Magnet_dup) = {22};

Curve Loop(19) = {159,160,-170,162,164};
Surf_Loch_dup = {19};
Plane Surface(Surf_Loch_dup) = {19};

Curve Loop(21) = {171,172,178,-168};
Surf_Loch_dup = {21};
Plane Surface(Surf_Loch_dup) = {21};

Curve Loop(23) = {181,182,-180,184,186};
Surf_Loch_dup = {23};
Plane Surface(Surf_Loch_dup) = {23};

Curve Loop(36) = {350,89,-356,-81};
Surf_rotorAirGap1_dup = {36};
Plane Surface(Surf_rotorAirGap1_dup) = {36};

Curve Loop(14) = {159,160,-170,162,164};
Surf_Loch_dup = {14};
Plane Surface(Surf_Loch_dup) = {14};
Curve Loop(15) = {165,166,167,168,169,170};
Surf_Magnet_dup = {15};
Plane Surface(Surf_Magnet_dup) = {15};
Curve Loop(16) = {171,172,178,-168};
Surf_Loch_dup = {16};
Plane Surface(Surf_Loch_dup) = {16};
Curve Loop(17) = {175,176,177,178,179,180};
Surf_Magnet_dup = {17};
Plane Surface(Surf_Magnet_dup) = {17};
Curve Loop(18) = {181,182,-180,184,186};
Surf_Loch_dup = {18};
Plane Surface(Surf_Loch_dup) = {18};
Curve Loop(13) = {79,350,-88,6};
Surf_Rotorblech_dup = {13};
Plane Surface(Surf_Rotorblech_dup) = {13, 14, 15, 16, 17, 18};

Curve Loop(44) = {428,-432,-76,84};
Surf_statorAirGap2_dup = {44};
Plane Surface(Surf_statorAirGap2_dup) = {44};

Curve Loop(45) = {434,-438,-92,432};
Surf_statorAirGap2_dup = {45};
Plane Surface(Surf_statorAirGap2_dup) = {45};

Curve Loop(46) = {440,-444,-94,438};
Surf_statorAirGap2_dup = {46};
Plane Surface(Surf_statorAirGap2_dup) = {46};

Curve Loop(47) = {446,-450,-96,444};
Surf_statorAirGap2_dup = {47};
Plane Surface(Surf_statorAirGap2_dup) = {47};

Curve Loop(48) = {452,-456,-98,450};
Surf_statorAirGap2_dup = {48};
Plane Surface(Surf_statorAirGap2_dup) = {48};

Curve Loop(49) = {458,-87,-100,456};
Surf_statorAirGap2_dup = {49};
Plane Surface(Surf_statorAirGap2_dup) = {49};

Curve Loop(38) = {362,363,367,364,366,371,-428,-83};
Surf_statorAirGap1_dup = {38};
Plane Surface(Surf_statorAirGap1_dup) = {38};

Curve Loop(39) = {373,374,378,375,377,382,-434,-371};
Surf_statorAirGap1_dup = {39};
Plane Surface(Surf_statorAirGap1_dup) = {39};

Curve Loop(40) = {384,385,389,386,388,393,-440,-382};
Surf_statorAirGap1_dup = {40};
Plane Surface(Surf_statorAirGap1_dup) = {40};

Curve Loop(41) = {395,396,400,397,399,404,-446,-393};
Surf_statorAirGap1_dup = {41};
Plane Surface(Surf_statorAirGap1_dup) = {41};

Curve Loop(42) = {406,407,411,408,410,415,-452,-404};
Surf_statorAirGap1_dup = {42};
Plane Surface(Surf_statorAirGap1_dup) = {42};

Curve Loop(43) = {417,418,422,419,421,86,-458,-415};
Surf_statorAirGap1_dup = {43};
Plane Surface(Surf_statorAirGap1_dup) = {43};

Curve Loop(24) = {187,37,80,362,363,194,195,197,199,200,201,364,366};
Surf_Statorblech_dup = {24};
Plane Surface(Surf_Statorblech_dup) = {24};

Curve Loop(25) = {205,116,-187,373,374,212,213,215,217,218,219,375,377};
Surf_Statorblech_dup = {25};
Plane Surface(Surf_Statorblech_dup) = {25};

Curve Loop(26) = {223,118,-205,384,385,230,231,233,235,236,237,386,388};
Surf_Statorblech_dup = {26};
Plane Surface(Surf_Statorblech_dup) = {26};

Curve Loop(27) = {241,120,-223,395,396,248,249,251,253,254,255,397,399};
Surf_Statorblech_dup = {27};
Plane Surface(Surf_Statorblech_dup) = {27};

Curve Loop(28) = {259,122,-241,406,407,266,267,269,271,272,273,408,410};
Surf_Statorblech_dup = {28};
Plane Surface(Surf_Statorblech_dup) = {28};

Curve Loop(29) = {85,-421,-419,-291,-290,-289,-287,-285,-284,-418,-417,259,-124};
Surf_Statorblech_dup = {29};
Plane Surface(Surf_Statorblech_dup) = {29};

Curve Loop(30) = {194,195,197,199,200,201,-367};
Surf_Stator_Nut_dup = {30};
Plane Surface(Surf_Stator_Nut_dup) = {30};

Curve Loop(31) = {212,213,215,217,218,219,-378};
Surf_Stator_Nut_dup = {31};
Plane Surface(Surf_Stator_Nut_dup) = {31};

Curve Loop(32) = {230,231,233,235,236,237,-389};
Surf_Stator_Nut_dup = {32};
Plane Surface(Surf_Stator_Nut_dup) = {32};

Curve Loop(33) = {248,249,251,253,254,255,-400};
Surf_Stator_Nut_dup = {33};
Plane Surface(Surf_Stator_Nut_dup) = {33};

Curve Loop(34) = {266,267,269,271,272,273,-411};
Surf_Stator_Nut_dup = {34};
Plane Surface(Surf_Stator_Nut_dup) = {34};

Curve Loop(35) = {284,285,287,289,290,291,-422};
Surf_Stator_Nut_dup = {35};
Plane Surface(Surf_Stator_Nut_dup) = {35};

// Color code
If (!Flag_individualColoring)
Color SkyBlue {Surface {37}; }
Color Red {Surface {20}; }
Color Red {Surface {22}; }
Color OrangeRed {Surface {19}; }
Color HotPink4 {Surface {21}; }
Color Grey34 {Surface {23}; }
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
Physical Curve("primaryLineS", 1002) = {80,83,84};
// primaryLineR
Physical Curve("primaryLineR", 1001) = {79,81,82};
// slaveLineS
Physical Curve("slaveLineS", 1004) = {85,86,87};
// slaveLineR
Physical Curve("slaveLineR", 1003) = {88,89,90};
// innerLimit
Physical Curve("innerLimit", 1015) = {6};
// Rotor_Bnd_MB_1
Physical Curve("Rotor_Bnd_MB_1", 1006) = {68};
// Rotor_Bnd_MB_2
Physical Curve("Rotor_Bnd_MB_2", 1007) = {102};
// Rotor_Bnd_MB_3
Physical Curve("Rotor_Bnd_MB_3", 1008) = {104};
// Rotor_Bnd_MB_4
Physical Curve("Rotor_Bnd_MB_4", 1009) = {106};
// Rotor_Bnd_MB_5
Physical Curve("Rotor_Bnd_MB_5", 1010) = {108};
// Rotor_Bnd_MB_6
Physical Curve("Rotor_Bnd_MB_6", 1011) = {110};
// Rotor_Bnd_MB_7
Physical Curve("Rotor_Bnd_MB_7", 1012) = {112};
// Rotor_Bnd_MB_8
Physical Curve("Rotor_Bnd_MB_8", 1013) = {114};
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
Physical Curve("outerLimit", 1014) = {37,116,118,120,122,124};
// mbStator
Physical Curve("mbStator", 1005) = {76,92,94,96,98,100};
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
		Lpl_msf = {1.0, Name StrCat[INPUT_MESH, "05Mesh Size/Loch (Polluecke) [mm]"],Min 0.1, Max 10.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		Mag_msf = {1.0, Name StrCat[INPUT_MESH, "05Mesh Size/Magnet [mm]"],Min 0.1, Max 10.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		Pol_msf = {1.0, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorblech [mm]"],Min 0.1, Max 10.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		LuR_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorluftspalt [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		LuR1_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorluftspalt 1 [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		LuR2_msf = {1000.0, Name StrCat[INPUT_MESH, "05Mesh Size/Rotorluftspalt 2 [mm]"],Min 100.0, Max 10000.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		StCu_msf = {1.0, Name StrCat[INPUT_MESH, "05Mesh Size/Stator-Nut [mm]"],Min 0.1, Max 10.0, Step 0.1,Visible Flag_SpecifyMeshSize},
		StNut_msf = {1.0, Name StrCat[INPUT_MESH, "05Mesh Size/Statorblech [mm]"],Min 0.1, Max 10.0, Step 0.1,Visible Flag_SpecifyMeshSize},
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
primaryLines = {79,81,82,80,83,84};
secondaryLines = {88,89,90,85,86,87};
Periodic Curve{secondaryLines[]} = {primaryLines[]} Rotate {{0,0,1}, {0,0,0}, 2*Pi/8};

// Add mesh size setting for Movingband lines
DefineConstant[
	NbrMbSegments = {360.0, Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],Max 1440, Min 180, Step 10, Help "Set the number of mesh segments on the interface between rotor/statorairgap and movingband. Value represents number of segments on whole circle.", Visible Flag_ExpertMode},
	r_MB_R = 0.08049999999999999
];
MB_LinesR = {68,102,104,106,108,110,112,114};
MeshSize{ PointsOf{Line{MB_LinesR[]};}} = 2*Pi*r_MB_R/NbrMbSegments;

MB_LinesS = {76,92,94,96,98,100};
MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*0.08065/NbrMbSegments;

Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)

// Create boundary lines for moving rotor contour plot
rotorBndLines[] = Boundary{ Physical Surface{ 1018,1020 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 1016 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 1030 }; };
statorBndLines[] = Boundary{ Physical Surface{ 1002,1004,1005,1014,1022,1023,1024,1025,1026,1027,1028,1031,1032 }; };
Physical Line("DomainPlotMovingGeo",1) = {rotorBndLines[], statorBndLines[]}; 
