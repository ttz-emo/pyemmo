// This script was created with pyemmo (Version 1.3.1b1)

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
pprimary1 = 706; Point(706) = {0.065, 0, 0, 0.0009657534246575549*gmsf};
pprimary2 = 707; Point(707) = {0.1, 0, 0, 0.006000000000000114*gmsf};
pSlot1_dup = 708; Point(708) = {0.06425, 0.0, 0, 0.0008578767123287846*gmsf};
pprimary1 = 232; Point(232) = {0.02, 0, 0, 0.004346456692913469*gmsf};
pprimary2 = 233; Point(233) = {0.055, 0, 0, 0.0014527559055118378*gmsf};
pMagnet3_dup = 234; Point(234) = {0.06275, 0.0, 0, 0.000812007874015763*gmsf};
pMagnet3_dup = 237; Point(237) = {0.06349999999999999, 0.0, 0, 0.0007500000000000145*gmsf};
pprimary1_dup = 710; Point(710) = {3.980102097228898e-18, 0.065, 0, 0.0009657534246575549*gmsf};
pprimary2_dup = 711; Point(711) = {6.123233995736766e-18, 0.1, 0, 0.006000000000000114*gmsf};
pSlot1_dup = 712; Point(712) = {3.934177842260872e-18, 0.06425, 0, 0.0008578767123287846*gmsf};
pprimary1_dup = 238; Point(238) = {1.2246467991473532e-18, 0.02, 0, 0.004346456692913469*gmsf};
pprimary2_dup = 239; Point(239) = {3.367778697655221e-18, 0.055, 0, 0.0014527559055118378*gmsf};
pMagnet3_dup = 240; Point(240) = {3.842329332324821e-18, 0.06275, 0, 0.000812007874015763*gmsf};
pMagnet3_dup = 243; Point(243) = {3.8882535872928455e-18, 0.06349999999999999, 0, 0.0007500000000000145*gmsf};
pLimitInner1_dup = 165; Point(165) = {0.018477590650225736, 0.007653668647301796, 0, 0.00434645669291347*gmsf};
mittelPunktBohrung = 2; Point(2) = {0, 0, 0, 0.00075*gmsf};
pLimitInner1_dup = 168; Point(168) = {0.01414213562373095, 0.014142135623730952, 0, 0.004346456692913469*gmsf};
pLimitInner1_dup = 171; Point(171) = {0.007653668647301796, 0.018477590650225736, 0, 0.00434645669291347*gmsf};
pMagnet3_dup = 177; Point(177) = {0.058666350314466695, 0.024300397955183194, 0, 0.0007500000000000145*gmsf};
pMagnet3_dup = 189; Point(189) = {0.044901280605345754, 0.04490128060534576, 0, 0.0007500000000000145*gmsf};
pMagnet3_dup = 192; Point(192) = {0.024300397955183194, 0.058666350314466695, 0, 0.0007500000000000145*gmsf};
pMagnet3_dup = 198; Point(198) = {-0.02430039795518319, 0.058666350314466695, 0, 0.0007500000000000145*gmsf};
pMagnet3_dup = 201; Point(201) = {-0.04490128060534576, 0.044901280605345754, 0, 0.0007500000000000145*gmsf};
pMagnet3_dup = 204; Point(204) = {-0.058666350314466695, 0.024300397955183198, 0, 0.0007500000000000145*gmsf};
pMagnet3_dup = 207; Point(207) = {-0.06349999999999999, 7.35770053924646e-18, 0, 0.0007500000000000145*gmsf};
pMagnet3_dup = 210; Point(210) = {-0.058666350314466695, -0.024300397955183187, 0, 0.0007500000000000145*gmsf};
pMagnet3_dup = 213; Point(213) = {-0.04490128060534576, -0.044901280605345754, 0, 0.0007500000000000145*gmsf};
pMagnet3_dup = 216; Point(216) = {-0.0243003979551832, -0.058666350314466695, 0, 0.0007500000000000145*gmsf};
pMagnet3_dup = 219; Point(219) = {-1.1245954126539305e-17, -0.06349999999999999, 0, 0.0007500000000000145*gmsf};
pMagnet3_dup = 222; Point(222) = {0.024300397955183184, -0.0586663503144667, 0, 0.0007500000000000145*gmsf};
pMagnet3_dup = 225; Point(225) = {0.044901280605345754, -0.04490128060534576, 0, 0.0007500000000000145*gmsf};
pMagnet3_dup = 228; Point(228) = {0.05866635031446669, -0.024300397955183205, 0, 0.0007500000000000145*gmsf};
pMagnet3_dup = 14; Point(14) = {0.05797344066508324, 0.024013385380909382, 0, 0.000812007874015763*gmsf};
pMagnet3_dup = 15; Point(15) = {0.04437095051945585, 0.04437095051945585, 0, 0.000812007874015763*gmsf};
pMagnet3_dup = 144; Point(144) = {0.024013385380909382, 0.05797344066508324, 0, 0.000812007874015763*gmsf};
pMagnet1 = 9; Point(9) = {0.05081337428812077, 0.021047588780079937, 0, 0.0014527559055118387*gmsf};
pMagnet2 = 10; Point(10) = {0.041822328108001704, 0.0357196426581601, 0, 0.0014527559055118387*gmsf};
pMagnet4 = 12; Point(12) = {0.04918790709805658, 0.037743208598540676, 0, 0.0008740157480315128*gmsf};
pMagnet3 = 11; Point(11) = {0.05728053101569978, 0.023726372806635566, 0, 0.0008740157480315122*gmsf};
P_61 = 61; Point(61) = {0.06146958140517625, 0.008092623917643198, 0.0, 0.0008740157480315122*gmsf};
P_64 = 64; Point(64) = {0.054830453355322044, 0.004315250265031476, 0.0, 0.0014527559055118387*gmsf};
pMagnet1_dup = 69; Point(69) = {0.021047588780079937, 0.05081337428812077, 0, 0.0014527559055118387*gmsf};
pMagnet2_dup = 71; Point(71) = {0.004315250265031476, 0.054830453355322044, 0, 0.0014527559055118387*gmsf};
pMagnet4_dup = 73; Point(73) = {0.008092623917643205, 0.06146958140517625, 0, 0.0008740157480315122*gmsf};
pMagnet3_dup = 76; Point(76) = {0.023726372806635563, 0.057280531015699784, 0, 0.0008740157480315122*gmsf};
P_61_dup = 83; Point(83) = {0.03774320859854068, 0.04918790709805659, 0.0, 0.0008740157480315114*gmsf};
P_64_dup = 85; Point(85) = {0.035719642658160106, 0.04182232810800171, 0.0, 0.0014527559055118378*gmsf};
pRotor2 = 7; Point(7) = {0.038890872965260115, 0.03889087296526012, 0, 0.0014527559055118372*gmsf};
pLimitOuter1_dup = 672; Point(672) = {0.09659258262890684, 0.025881904510252074, 0, 0.006000000000000114*gmsf};
pLimitOuter1_dup = 678; Point(678) = {0.08660254037844388, 0.05, 0, 0.006000000000000114*gmsf};
pLimitOuter1_dup = 684; Point(684) = {0.07071067811865477, 0.07071067811865475, 0, 0.006000000000000114*gmsf};
pLimitOuter1_dup = 690; Point(690) = {0.05000000000000001, 0.08660254037844387, 0, 0.006000000000000114*gmsf};
pLimitOuter1_dup = 696; Point(696) = {0.025881904510252098, 0.09659258262890683, 0, 0.006000000000000114*gmsf};
pSlot1_dup = 675; Point(675) = {0.06206073433907264, 0.016629123647836953, 0, 0.0008578767123287846*gmsf};
pSlot1_dup = 681; Point(681) = {0.05564213219315019, 0.03212499999999999, 0, 0.0008578767123287846*gmsf};
pSlot1_dup = 687; Point(687) = {0.04543161069123569, 0.04543161069123567, 0, 0.0008578767123287846*gmsf};
pSlot1_dup = 693; Point(693) = {0.03212500000000001, 0.05564213219315018, 0, 0.0008578767123287846*gmsf};
pSlot1_dup = 699; Point(699) = {0.016629123647836974, 0.06206073433907264, 0, 0.0008578767123287846*gmsf};
pSlot1 = 376; Point(376) = {0.06278517870878944, 0.016823237931663848, 0, 0.0009657534246575549*gmsf};
pSi2 = 373; Point(373) = {0.05629165124598852, 0.0325, 0, 0.0009657534246575549*gmsf};
pSlot1_dup = 377; Point(377) = {0.06163331068015557, 0.020647881600867023, 0, 0.0009657534246575562*gmsf};
P_607 = 607; Point(607) = {0.063699953568787, 0.012935065339393627, 0.0, 0.0009657534246575562*gmsf};
pSlot1_dup = 623; Point(623) = {0.04596194077712559, 0.04596194077712558, 0, 0.0009657534246575549*gmsf};
pSi2_dup = 625; Point(625) = {0.032500000000000015, 0.05629165124598852, 0, 0.0009657534246575549*gmsf};
pSlot1_dup = 626; Point(626) = {0.04305207196791998, 0.04869824534076193, 0, 0.0009657534246575562*gmsf};
P_607_dup = 632; Point(632) = {0.04869824534076194, 0.04305207196791995, 0.0, 0.0009657534246575562*gmsf};
pSlot1_dup = 649; Point(649) = {0.016823237931663862, 0.06278517870878944, 0, 0.0009657534246575521*gmsf};
pSlot1_dup = 652; Point(652) = {0.012935065339393648, 0.063699953568787, 0, 0.0009657534246575562*gmsf};
P_607_dup = 658; Point(658) = {0.020647881600867043, 0.06163331068015556, 0.0, 0.0009657534246575562*gmsf};
pSlot1_dup = 378; Point(378) = {0.06664888201394571, 0.017858514112073932, 0, 0.0015410958904109877*gmsf};
pSlot1_dup = 379; Point(379) = {0.06542612979893435, 0.02191852046861268, 0, 0.0015410958904109862*gmsf};
P_557 = 557; Point(557) = {0.06761995071148157, 0.013731069360279388, 0.0, 0.0015410958904109877*gmsf};
pSlot1_dup = 570; Point(570) = {0.04879036790187179, 0.04879036790187177, 0, 0.0015410958904109877*gmsf};
pSlot1_dup = 572; Point(572) = {0.04570143024286888, 0.05169506043865495, 0, 0.0015410958904109862*gmsf};
P_557_dup = 576; Point(576) = {0.051695060438654974, 0.045701430242868865, 0.0, 0.0015410958904109877*gmsf};
pSlot1_dup = 590; Point(590) = {0.01785851411207394, 0.06664888201394571, 0, 0.0015410958904109903*gmsf};
pSlot1_dup = 592; Point(592) = {0.013731069360279402, 0.06761995071148155, 0, 0.0015410958904109877*gmsf};
P_557_dup = 596; Point(596) = {0.0219185204686127, 0.06542612979893436, 0.0, 0.0015410958904109903*gmsf};
pSlot1_dup = 382; Point(382) = {0.08886517601859428, 0.02381135214943191, 0, 0.004849315068493246*gmsf};
pSlot1_dup = 380; Point(380) = {0.06476779834410705, 0.0287425172463562, 0, 0.0018084884520327567*gmsf};
pSlot1_dup = 381; Point(381) = {0.07294349269050363, 0.033003740304857025, 0, 0.003132273888389376*gmsf};
pSlot1_dup = 383; Point(383) = {0.0763081402768364, 0.02044670456309914, 0, 0.003*gmsf};
P_389 = 389; Point(389) = {0.07967278786316917, 0.007889668821341254, 0.0, 0.003132273888389376*gmsf};
P_392 = 392; Point(392) = {0.07046181733636252, 0.007492149067996695, 0.0, 0.001808488452032758*gmsf};
pSlot1_dup = 417; Point(417) = {0.06505382386916239, 0.06505382386916236, 0, 0.004849315068493246*gmsf};
pSlot1_dup = 421; Point(421) = {0.04171930009000631, 0.05727564927611034, 0, 0.0018084884520327567*gmsf};
pSlot1_dup = 423; Point(423) = {0.046669047558312145, 0.06505382386916236, 0, 0.003132273888389373*gmsf};
pSlot1_dup = 425; Point(425) = {0.055861435713737265, 0.05586143571373725, 0, 0.003*gmsf};
P_389_dup = 429; Point(429) = {0.06505382386916238, 0.04666904755831214, 0.0, 0.003132273888389376*gmsf};
P_392_dup = 431; Point(431) = {0.05727564927611036, 0.041719300090006295, 0.0, 0.001808488452032758*gmsf};
pSlot1_dup = 455; Point(455) = {0.02381135214943192, 0.08886517601859428, 0, 0.004849315068493246*gmsf};
pSlot1_dup = 459; Point(459) = {0.0074921490679967125, 0.0704618173363625, 0, 0.0018084884520327567*gmsf};
pSlot1_dup = 461; Point(461) = {0.007889668821341265, 0.07967278786316917, 0, 0.003132273888389376*gmsf};
pSlot1_dup = 463; Point(463) = {0.02044670456309915, 0.07630814027683638, 0, 0.003*gmsf};
P_389_dup = 467; Point(467) = {0.03300374030485704, 0.07294349269050363, 0.0, 0.003132273888389376*gmsf};
P_392_dup = 469; Point(469) = {0.028742517246356222, 0.06476779834410705, 0.0, 0.001808488452032758*gmsf};

// Lines and Curves
lLamprimary = 369;Line(lLamprimary) = {706, 707};
lAir2_dup = 370;Line(lAir2_dup) = {708, 706};
lLamprimary = 156;Line(lLamprimary) = {232, 233};
lAir3_dup = 157;Line(lAir3_dup) = {234, 233};
lAir5_dup = 158;Line(lAir5_dup) = {234, 237};
lLamprimary_dup = 371;Line(lLamprimary_dup) = {710, 711};
lAir2_dup = 372;Line(lAir2_dup) = {712, 710};
lLamprimary_dup = 159;Line(lLamprimary_dup) = {238, 239};
lAir3_dup = 160;Line(lAir3_dup) = {240, 239};
lAir5_dup = 161;Line(lAir5_dup) = {240, 243};
curveInner = 111;Circle(curveInner) = {232, 2, 165};
curveInner_dup = 113;Circle(curveInner_dup) = {165, 2, 168};
curveInner_dup = 115;Circle(curveInner_dup) = {168, 2, 171};
curveInner_dup = 117;Circle(curveInner_dup) = {171, 2, 238};
lAir4_dup = 119;Circle(lAir4_dup) = {237, 2, 177};
lAir4_dup = 127;Circle(lAir4_dup) = {177, 2, 189};
lAir4_dup = 129;Circle(lAir4_dup) = {189, 2, 192};
lAir4_dup = 131;Circle(lAir4_dup) = {192, 2, 243};
lAir4_dup = 133;Circle(lAir4_dup) = {243, 2, 198};
lAir4_dup = 135;Circle(lAir4_dup) = {198, 2, 201};
lAir4_dup = 137;Circle(lAir4_dup) = {201, 2, 204};
lAir4_dup = 139;Circle(lAir4_dup) = {204, 2, 207};
lAir4_dup = 141;Circle(lAir4_dup) = {207, 2, 210};
lAir4_dup = 143;Circle(lAir4_dup) = {210, 2, 213};
lAir4_dup = 145;Circle(lAir4_dup) = {213, 2, 216};
lAir4_dup = 147;Circle(lAir4_dup) = {216, 2, 219};
lAir4_dup = 149;Circle(lAir4_dup) = {219, 2, 222};
lAir4_dup = 151;Circle(lAir4_dup) = {222, 2, 225};
lAir4_dup = 153;Circle(lAir4_dup) = {225, 2, 228};
lAir4_dup = 155;Circle(lAir4_dup) = {228, 2, 237};
lAir1 = 14;Circle(lAir1) = {14, 2, 15};
lAir5 = 19;Line(lAir5) = {14, 177};
lAir6 = 20;Line(lAir6) = {15, 189};
CA_97 = 97;Circle(CA_97) = {234, 2, 14};
lAir1_dup = 99;Circle(lAir1_dup) = {144, 2, 240};
lAir5_dup = 102;Line(lAir5_dup) = {144, 192};
CA_97_dup = 109;Circle(CA_97_dup) = {15, 2, 144};
lMagnet1 = 8;Circle(lMagnet1) = {9, 2, 10};
lMagnet2 = 9;Line(lMagnet2) = {10, 12};
lMagnet3 = 11;Circle(lMagnet3) = {12, 2, 11};
lMagnet4 = 12;Line(lMagnet4) = {11, 9};
CA_49 = 49;Circle(CA_49) = {11, 2, 61};
L_50 = 50;Line(L_50) = {61, 64};
CA_52 = 52;Circle(CA_52) = {64, 2, 9};
lMagnet1_dup = 54;Circle(lMagnet1_dup) = {69, 2, 71};
lMagnet2_dup = 55;Line(lMagnet2_dup) = {71, 73};
lMagnet3_dup = 57;Circle(lMagnet3_dup) = {73, 2, 76};
lMagnet4_dup = 58;Line(lMagnet4_dup) = {76, 69};
CA_49_dup = 61;Circle(CA_49_dup) = {76, 2, 83};
L_50_dup = 62;Line(L_50_dup) = {83, 85};
CA_52_dup = 64;Circle(CA_52_dup) = {85, 2, 69};
lAir2 = 15;Line(lAir2) = {14, 11};
lAir3 = 16;Line(lAir3) = {15, 7};
lRotorAussen = 5;Circle(lRotorAussen) = {7, 2, 10};
CA_69 = 69;Circle(CA_69) = {64, 2, 233};
lAir2_dup = 76;Line(lAir2_dup) = {144, 76};
lRotorAussen_dup = 79;Circle(lRotorAussen_dup) = {239, 2, 71};
CA_69_dup = 87;Circle(CA_69_dup) = {85, 2, 7};
lBlech1 = 3;Line(lBlech1) = {168, 7};
lBlech2 = 6;Line(lBlech2) = {9, 165};
lBlech2_dup = 36;Line(lBlech2_dup) = {69, 171};
curveOuter = 346;Circle(curveOuter) = {707, 2, 672};
curveOuter_dup = 350;Circle(curveOuter_dup) = {672, 2, 678};
curveOuter_dup = 354;Circle(curveOuter_dup) = {678, 2, 684};
curveOuter_dup = 358;Circle(curveOuter_dup) = {684, 2, 690};
curveOuter_dup = 362;Circle(curveOuter_dup) = {690, 2, 696};
curveOuter_dup = 366;Circle(curveOuter_dup) = {696, 2, 711};
lAir1_dup = 348;Circle(lAir1_dup) = {708, 2, 675};
lAir1_dup = 352;Circle(lAir1_dup) = {675, 2, 681};
lAir1_dup = 356;Circle(lAir1_dup) = {681, 2, 687};
lAir1_dup = 360;Circle(lAir1_dup) = {687, 2, 693};
lAir1_dup = 364;Circle(lAir1_dup) = {693, 2, 699};
lAir1_dup = 368;Circle(lAir1_dup) = {699, 2, 712};
lAir2 = 181;Line(lAir2) = {675, 376};
lAir3 = 182;Line(lAir3) = {681, 373};
lSi = 163;Circle(lSi) = {377, 2, 373};
lS1 = 169;Circle(lS1) = {376, 2, 377};
CA_306 = 306;Circle(CA_306) = {607, 2, 376};
CA_308 = 308;Circle(CA_308) = {706, 2, 607};
lAir2_dup = 315;Line(lAir2_dup) = {687, 623};
lAir3_dup = 316;Line(lAir3_dup) = {693, 625};
lSi_dup = 318;Circle(lSi_dup) = {626, 2, 625};
lS1_dup = 320;Circle(lS1_dup) = {623, 2, 626};
CA_306_dup = 322;Circle(CA_306_dup) = {632, 2, 623};
CA_308_dup = 324;Circle(CA_308_dup) = {373, 2, 632};
lAir2_dup = 331;Line(lAir2_dup) = {699, 649};
lSi_dup = 334;Circle(lSi_dup) = {652, 2, 710};
lS1_dup = 336;Circle(lS1_dup) = {649, 2, 652};
CA_306_dup = 338;Circle(CA_306_dup) = {658, 2, 649};
CA_308_dup = 340;Circle(CA_308_dup) = {625, 2, 658};
lS2 = 170;Line(lS2) = {376, 378};
lS3 = 171;Line(lS3) = {377, 379};
lS4 = 173;Circle(lS4) = {378, 2, 379};
CA_276 = 276;Circle(CA_276) = {557, 2, 378};
L_277 = 277;Line(L_277) = {557, 607};
lS2_dup = 283;Line(lS2_dup) = {623, 570};
lS3_dup = 284;Line(lS3_dup) = {626, 572};
lS4_dup = 286;Circle(lS4_dup) = {570, 2, 572};
CA_276_dup = 288;Circle(CA_276_dup) = {576, 2, 570};
L_277_dup = 289;Line(L_277_dup) = {576, 632};
lS2_dup = 295;Line(lS2_dup) = {649, 590};
lS3_dup = 296;Line(lS3_dup) = {652, 592};
lS4_dup = 298;Circle(lS4_dup) = {590, 2, 592};
CA_276_dup = 300;Circle(CA_276_dup) = {596, 2, 590};
L_277_dup = 301;Line(L_277_dup) = {596, 658};
lSBlech1 = 164;Line(lSBlech1) = {373, 678};
lSBlech2 = 167;Line(lSBlech2) = {672, 382};
lS5 = 174;Line(lS5) = {379, 380};
lS6 = 175;Line(lS6) = {380, 381};
lS7 = 177;Circle(lS7) = {381, 383, 382};
CA_186 = 186;Circle(CA_186) = {382, 383, 389};
L_187 = 187;Line(L_187) = {389, 392};
L_188 = 188;Line(L_188) = {392, 557};
lSBlech1_dup = 198;Line(lSBlech1_dup) = {625, 690};
lSBlech2_dup = 201;Line(lSBlech2_dup) = {684, 417};
lS5_dup = 203;Line(lS5_dup) = {572, 421};
lS6_dup = 204;Line(lS6_dup) = {421, 423};
lS7_dup = 206;Circle(lS7_dup) = {423, 425, 417};
CA_186_dup = 208;Circle(CA_186_dup) = {417, 425, 429};
L_187_dup = 209;Line(L_187_dup) = {429, 431};
L_188_dup = 210;Line(L_188_dup) = {431, 576};
lSBlech2_dup = 223;Line(lSBlech2_dup) = {696, 455};
lS5_dup = 225;Line(lS5_dup) = {592, 459};
lS6_dup = 226;Line(lS6_dup) = {459, 461};
lS7_dup = 228;Circle(lS7_dup) = {461, 463, 455};
CA_186_dup = 230;Circle(CA_186_dup) = {455, 463, 467};
L_187_dup = 231;Line(L_187_dup) = {467, 469};
L_188_dup = 232;Line(L_188_dup) = {469, 596};
L_240 = 240;Line(L_240) = {378, 382};
L_240_dup = 247;Line(L_240_dup) = {570, 417};
L_240_dup = 261;Line(L_240_dup) = {590, 455};

// Surfaces

Curve Loop(4) = {14,20,-127,-19};
Surf_sAir2 = {4};
Plane Surface(Surf_sAir2) = {4};

Curve Loop(14) = {158,119,-19,-97};
Surf_s_4 = {14};
Plane Surface(Surf_s_4) = {14};

Curve Loop(15) = {99,161,-131,-102};
Surf_sAir2_dup = {15};
Plane Surface(Surf_sAir2_dup) = {15};

Curve Loop(16) = {20,129,-102,-109};
Surf_s_4_dup = {16};
Plane Surface(Surf_s_4_dup) = {16};

Curve Loop(2) = {8,9,11,12};
Surf_surfaceMagnet = {2};
Plane Surface(Surf_surfaceMagnet) = {2};

Curve Loop(8) = {12,-52,-50,-49};
Surf_s_2 = {8};
Plane Surface(Surf_s_2) = {8};

Curve Loop(9) = {54,55,57,58};
Surf_surfaceMagnet_dup = {9};
Plane Surface(Surf_surfaceMagnet_dup) = {9};

Curve Loop(10) = {58,-64,-62,-61};
Surf_s_2_dup = {10};
Plane Surface(Surf_s_2_dup) = {10};

Curve Loop(3) = {14,16,5,9,11,-15};
Surf_sAir1 = {3};
Plane Surface(Surf_sAir1) = {3};

Curve Loop(11) = {50,69,-157,97,15,49};
Surf_s_3 = {11};
Plane Surface(Surf_s_3) = {11};

Curve Loop(12) = {99,160,79,55,57,-76};
Surf_sAir1_dup = {12};
Plane Surface(Surf_sAir1_dup) = {12};

Curve Loop(13) = {62,87,-16,109,76,61};
Surf_s_3_dup = {13};
Plane Surface(Surf_s_3_dup) = {13};

Curve Loop(1) = {113,3,5,-8,6};
Surf_surfaceRotor = {1};
Plane Surface(Surf_surfaceRotor) = {1};

Curve Loop(5) = {52,6,-111,156,-69};
Surf_s_1 = {5};
Plane Surface(Surf_s_1) = {5};

Curve Loop(6) = {117,159,79,-54,36};
Surf_surfaceRotor_dup = {6};
Plane Surface(Surf_surfaceRotor_dup) = {6};

Curve Loop(7) = {64,36,-115,3,-87};
Surf_s_1_dup = {7};
Plane Surface(Surf_s_1_dup) = {7};

Curve Loop(20) = {352,182,-163,-169,-181};
Surf_sAir1 = {20};
Plane Surface(Surf_sAir1) = {20};

Curve Loop(36) = {306,-181,-348,370,308};
Surf_s_20 = {36};
Plane Surface(Surf_s_20) = {36};

Curve Loop(37) = {360,316,-318,-320,-315};
Surf_sAir1_dup = {37};
Plane Surface(Surf_sAir1_dup) = {37};

Curve Loop(38) = {322,-315,-356,182,324};
Surf_s_20_dup = {38};
Plane Surface(Surf_s_20_dup) = {38};

Curve Loop(39) = {368,372,-334,-336,-331};
Surf_sAir1_dup = {39};
Plane Surface(Surf_sAir1_dup) = {39};

Curve Loop(40) = {338,-331,-364,316,340};
Surf_s_20_dup = {40};
Plane Surface(Surf_s_20_dup) = {40};

Curve Loop(18) = {169,171,-173,-170};
Surf_slotOP = {18};
Plane Surface(Surf_slotOP) = {18};

Curve Loop(31) = {276,-170,-306,-277};
Surf_s_18 = {31};
Plane Surface(Surf_s_18) = {31};

Curve Loop(32) = {320,284,-286,-283};
Surf_slotOP_dup = {32};
Plane Surface(Surf_slotOP_dup) = {32};

Curve Loop(33) = {288,-283,-322,-289};
Surf_s_18_dup = {33};
Plane Surface(Surf_s_18_dup) = {33};

Curve Loop(34) = {336,296,-298,-295};
Surf_slotOP_dup = {34};
Plane Surface(Surf_slotOP_dup) = {34};

Curve Loop(35) = {300,-295,-338,-301};
Surf_s_18_dup = {35};
Plane Surface(Surf_s_18_dup) = {35};

Curve Loop(17) = {163,164,-350,167,-177,-175,-174,-171};
Surf_surfaceStator = {17};
Plane Surface(Surf_surfaceStator) = {17};

Curve Loop(21) = {186,187,188,277,-308,369,346,167};
Surf_s_17 = {21};
Plane Surface(Surf_s_17) = {21};

Curve Loop(22) = {318,198,-358,201,-206,-204,-203,-284};
Surf_surfaceStator_dup = {22};
Plane Surface(Surf_surfaceStator_dup) = {22};

Curve Loop(23) = {208,209,210,289,-324,164,354,201};
Surf_s_17_dup = {23};
Plane Surface(Surf_s_17_dup) = {23};

Curve Loop(24) = {334,371,-366,223,-228,-226,-225,-296};
Surf_surfaceStator_dup = {24};
Plane Surface(Surf_surfaceStator_dup) = {24};

Curve Loop(25) = {230,231,232,301,-340,198,362,223};
Surf_s_17_dup = {25};
Plane Surface(Surf_s_17_dup) = {25};

Curve Loop(26) = {240,186,187,188,276};
Surf_s_19 = {26};
Plane Surface(Surf_s_19) = {26};

Curve Loop(19) = {173,174,175,177,-240};
Surf_slotF1 = {19};
Plane Surface(Surf_slotF1) = {19};

Curve Loop(27) = {247,208,209,210,288};
Surf_s_19_dup = {27};
Plane Surface(Surf_s_19_dup) = {27};

Curve Loop(28) = {286,203,204,206,-247};
Surf_slotF1_dup = {28};
Plane Surface(Surf_slotF1_dup) = {28};

Curve Loop(29) = {261,230,231,232,300};
Surf_s_19_dup = {29};
Plane Surface(Surf_s_19_dup) = {29};

Curve Loop(30) = {298,225,226,228,-261};
Surf_slotF1_dup = {30};
Plane Surface(Surf_slotF1_dup) = {30};

// Color code
If (!Flag_individualColoring)
Color SkyBlue {Surface {4}; }
Color SkyBlue {Surface {14}; }
Color SkyBlue {Surface {15}; }
Color SkyBlue {Surface {16}; }
Color Red {Surface {2}; }
Color Red {Surface {8}; }
Color Green {Surface {9}; }
Color Green {Surface {10}; }
Color SkyBlue {Surface {3}; }
Color SkyBlue {Surface {11}; }
Color SkyBlue {Surface {12}; }
Color SkyBlue {Surface {13}; }
Color SteelBlue {Surface {1}; }
Color SteelBlue {Surface {5}; }
Color SteelBlue {Surface {6}; }
Color SteelBlue {Surface {7}; }
Color SkyBlue {Surface {20}; }
Color SkyBlue {Surface {36}; }
Color SkyBlue {Surface {37}; }
Color SkyBlue {Surface {38}; }
Color SkyBlue {Surface {39}; }
Color SkyBlue {Surface {40}; }
Color SkyBlue {Surface {18}; }
Color SkyBlue {Surface {31}; }
Color SkyBlue {Surface {32}; }
Color SkyBlue {Surface {33}; }
Color SkyBlue {Surface {34}; }
Color SkyBlue {Surface {35}; }
Color SteelBlue4 {Surface {17}; }
Color SteelBlue4 {Surface {21}; }
Color SteelBlue4 {Surface {22}; }
Color SteelBlue4 {Surface {23}; }
Color SteelBlue4 {Surface {24}; }
Color SteelBlue4 {Surface {25}; }
Color Magenta {Surface {26}; }
Color Cyan {Surface {19}; }
Color Yellow4 {Surface {27}; }
Color Magenta {Surface {28}; }
Color Cyan {Surface {29}; }
Color Yellow4 {Surface {30}; }
EndIf

// Physical Elements
// primary_StatorLine
Physical Curve("primary_StatorLine", 1028) = {369,370};
// primary_RotorLine
Physical Curve("primary_RotorLine", 1012) = {156,157,158};
// slave_StatorLine
Physical Curve("slave_StatorLine", 1029) = {371,372};
// slave_RotorLine
Physical Curve("slave_RotorLine", 1013) = {159,160,161};
// innerLimitLine_Rotor
Physical Curve("innerLimitLine_Rotor", 1011) = {111,113,115,117,113,115,117};
// movingBand_RotorLine
Physical Curve("movingBand_RotorLine", 1007) = {119,127,129,131};
// mb_Aux_1008
Physical Curve("mb_Aux_1008", 1008) = {133,135,137,139};
// mb_Aux_1009
Physical Curve("mb_Aux_1009", 1009) = {141,143,145,147};
// mb_Aux_1010
Physical Curve("mb_Aux_1010", 1010) = {149,151,153,155};
// airGapRotor
Physical Surface("airGapRotor", 1005) = {4,14,15,16};
// Magnet_Surface01_1002
Physical Surface("Magnet_Surface01_1002", 1003) = {2,8};
// magnet_SPMSM_1006
Physical Surface("magnet_SPMSM_1006", 1006) = {9,10};
// airRotor
Physical Surface("airRotor", 1004) = {3,11,12,13};
// RotorLamination_Sheet01_Standard_1001
Physical Surface("RotorLamination_Sheet01_Standard_1001", 1001) = {1,5,6,7};
// OuterLimitLine_Stator
Physical Curve("OuterLimitLine_Stator", 1026) = {346,350,354,358,362,366};
// movingBand_StatorLine
Physical Curve("movingBand_StatorLine", 1027) = {348,352,356,360,364,368};
// statorAirGap
Physical Surface("statorAirGap", 1025) = {20,36,37,38,39,40};
// Airslot
Physical Surface("Airslot", 1024) = {18,31,32,33,34,35};
// laminationSPMSM_Stator
Physical Surface("laminationSPMSM_Stator", 1017) = {17,21,22,23,24,25};
// slot_1018
Physical Surface("slot_1018", 1018) = {26};
// slot_1019
Physical Surface("slot_1019", 1019) = {19};
// slot_1020
Physical Surface("slot_1020", 1020) = {27};
// slot_1021
Physical Surface("slot_1021", 1021) = {28};
// slot_1022
Physical Surface("slot_1022", 1022) = {29};
// slot_1023
Physical Surface("slot_1023", 1023) = {30};

// Mesh operations

// Do not switch mesh algorithm on failure, because this led to mesh errors in the past.
Mesh.AlgorithmSwitchOnFailure = 0;DefineConstant[Flag_CompoundMesh = {0, Name StrCat[INPUT_MESH, "Compound Mesh"], Choices {0,1}, Help "Use Compound Mesh to ignore lines between segments while meshing.",Visible Flag_ExpertMode}];
If (Flag_CompoundMesh)
Compound Surface{1,5,6,7}; // rotor domainLam
Compound Surface{17,21,22,23,24,25}; // stator domainLam
Compound Surface{4,14,15,16}; // rotor airGap
Compound Surface{20,36,37,38,39,40}; // stator airGap
EndIf // (Flag_CompoundMesh)

// Add Periodic Mesh to model symmetry boundary-lines
primaryLines = {156,157,158,369,370};
secondaryLines = {159,160,161,371,372};
Periodic Curve{secondaryLines[]} = {primaryLines[]} Rotate {{0,0,1}, {0,0,0}, 2*Pi/4};

// Add mesh size setting for Movingband lines
DefineConstant[
	NbrMbSegments = {530.0, Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],Max 1440, Min 180, Step 10, Help "Set the number of mesh segments on the interface between rotor/statorairgap and movingband. Value represents number of segments on whole circle.", Visible Flag_ExpertMode},
	r_MB_R = 0.06349999999999999
];
MB_LinesR = {119,127,129,131,133,135,137,139,141,143,145,147,149,151,153,155};
MeshSize{ PointsOf{Line{MB_LinesR[]};}} = 2*Pi*r_MB_R/NbrMbSegments;

MB_LinesS = {348,352,356,360,364,368};
MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*0.06425/NbrMbSegments;

Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)

// Create boundary lines for moving rotor contour plot
rotorBndLines[] = Boundary{ Physical Surface{ 1003,1006 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 1001 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 1005 }; };
statorBndLines[] = Boundary{ Physical Surface{ 1017,1018,1019,1020,1021,1022,1023,1024,1025,1026,1027,1028,1029 }; };
Physical Line("DomainPlotMovingGeo",1) = {rotorBndLines[], statorBndLines[]};
