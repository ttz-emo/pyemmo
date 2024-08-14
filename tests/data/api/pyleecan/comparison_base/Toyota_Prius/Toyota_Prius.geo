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
point_pylc_dup = 2355; Point(2355) = {0.13462, 0.0, 0, 0.006730999999999999*gmsf};
point_pylc_dup = 2356; Point(2356) = {0.08095, 0.0, 0, 0.00018658143413008237*gmsf};
PointM41_dup = 2362; Point(2362) = {0.0808, 0, 0, 0.00016829071706504786*gmsf};
PointM31_dup = 2363; Point(2363) = {0.08065, 0, 0, 0.00015000000000001124*gmsf};
point_pylc_dup = 2353; Point(2353) = {0.05532, 0.0, 0, 0.005871021118012428*gmsf};
point_pylc_dup = 2354; Point(2354) = {0.0802, 0.0, 0, 0.00021816149068324008*gmsf};
PointM11_dup = 2358; Point(2358) = {0.08034999999999999, 0, 0, 0.00018408074534162567*gmsf};
PointM21_dup = 2360; Point(2360) = {0.08049999999999999, 0, 0, 0.00015000000000001124*gmsf};
point_pylc_dup = 2365; Point(2365) = {0.09519071488333303, 0.09519071488333303, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 2366; Point(2366) = {0.057240293937051025, 0.057240293937051025, 0.0, 0.00018658143413008237*gmsf};
PointM41_dup = 2368; Point(2368) = {0.05713422791987304, 0.05713422791987304, 0.0, 0.00016829071706504786*gmsf};
PointM31_dup = 2369; Point(2369) = {0.05702816190269506, 0.05702816190269506, 0.0, 0.00015000000000001124*gmsf};
point_pylc_dup = 2371; Point(2371) = {0.03911714713523981, 0.03911714713523981, 0.0, 0.005871021118012428*gmsf};
point_pylc_dup = 2372; Point(2372) = {0.05670996385116111, 0.05670996385116111, 0.0, 0.00021816149068324008*gmsf};
PointM11_dup = 2374; Point(2374) = {0.05681602986833909, 0.05681602986833909, 0.0, 0.00018408074534162567*gmsf};
PointM21_dup = 2376; Point(2376) = {0.05692209588551707, 0.05692209588551707, 0.0, 0.00015000000000001124*gmsf};
point_pylc = 2227; Point(2227) = {0, 0, 0, 0.001*gmsf};
PointM22_dup = 2394; Point(2394) = {0.0, 0.08049999999999999, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 2397; Point(2397) = {-0.05692209588551706, 0.056922095885517075, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 2400; Point(2400) = {-0.08049999999999999, 0.0, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 2403; Point(2403) = {-0.056922095885517075, -0.05692209588551706, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 2406; Point(2406) = {-6.938893903907228e-18, -0.08049999999999999, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 2409; Point(2409) = {0.056922095885517054, -0.05692209588551708, 0.0, 0.00015000000000001124*gmsf};
point_pylc_dup = 2503; Point(2503) = {0.07189332074897073, 0.008478350008583092, 0, 0.001*gmsf};
point_pylc_dup = 2504; Point(2504) = {0.07112686475225904, 0.007836053188487666, 0, 0.001*gmsf};
point_pylc_dup = 2506; Point(2506) = {0.058987454852455525, 0.02232207152633855, 0, 0.001*gmsf};
point_pylc_dup = 2508; Point(2508) = {0.059753910849167216, 0.02296436834643398, 0, 0.001*gmsf};
point_pylc_dup = 2510; Point(2510) = {0.0639694188310815, 0.026497000856958816, 0, 0.001*gmsf};
point_pylc_dup = 2512; Point(2512) = {0.07610882873088501, 0.01201098251910793, 0, 0.000933687570242861*gmsf};
point_pylc_dup = 2523; Point(2523) = {0.056831353407958855, 0.0448411558392746, 0, 0.001*gmsf};
point_pylc_dup = 2524; Point(2524) = {0.055835214738178894, 0.0447533620435427, 0, 0.001*gmsf};
point_pylc_dup = 2526; Point(2526) = {0.057494517477511754, 0.02592634118470148, 0, 0.001*gmsf};
point_pylc_dup = 2528; Point(2528) = {0.05849065614729172, 0.026014134980433378, 0, 0.001*gmsf};
point_pylc_dup = 2532; Point(2532) = {0.06231011609174863, 0.045324021715800036, 0, 0.000933687570242861*gmsf};
point_pylc_dup = 2492; Point(2492) = {0.07838807307237497, 0.007000000000000003, 0, 0.0005589689440993886*gmsf};
point_pylc_dup = 2493; Point(2493) = {0.07313219096927659, 0.007000000000000003, 0, 0.001*gmsf};
point_pylc_dup = 2499; Point(2499) = {0.07810937152746876, 0.009623724828976162, 0, 0.0005589689440993886*gmsf};
point_pylc_dup = 2516; Point(2516) = {0.05864256321587955, 0.024290545016338896, 0, 0.001*gmsf};
point_pylc_dup = 2535; Point(2535) = {0.06037848550192878, 0.050478990565317114, 0, 0.0005589689440993886*gmsf};
point_pylc_dup = 2536; Point(2536) = {0.05666201562571091, 0.04676252068909924, 0, 0.001*gmsf};
point_pylc_dup = 2542; Point(2542) = {0.06203666736813499, 0.048426665194450214, 0, 0.0005589689440993865*gmsf};
point_pylc = 2284; Point(2284) = {0.13346830723814235, 0.017571435996663342, 0, 0.006730999999999999*gmsf};
point_pylc_dup = 2413; Point(2413) = {0.13003293473503436, 0.034842219851701335, 0.0, 0.006730999999999997*gmsf};
point_pylc_dup = 2416; Point(2416) = {0.12437266266666941, 0.051516843664988377, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 2419; Point(2419) = {0.11658433985746111, 0.06731, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 2422; Point(2422) = {0.10680122667000608, 0.08195146357315396, 0.0, 0.006730999999999999*gmsf};
PointM32 = 2352; Point(2352) = {0.07996002806979781, 0.010526937402547159, 0, 0.00015000000000001124*gmsf};
PointM32_dup = 2379; Point(2379) = {0.07790191789021336, 0.020873755987518297, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 2382; Point(2382) = {0.07451088429703527, 0.030863418820244487, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 2385; Point(2385) = {0.06984494881521497, 0.040325, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 2388; Point(2388) = {0.06398394689448812, 0.04909660924955331, 0.0, 0.00015000000000001124*gmsf};
PointM42_dup = 2964; Point(2964) = {0.08010874479900387, 0.010546516331380167, 0, 0.00016829071706504786*gmsf};
PointM42_dup = 2974; Point(2974) = {0.0780468067641567, 0.020912578844283672, 0.0, 0.00016829071706504786*gmsf};
PointM42_dup = 2984; Point(2984) = {0.07464946622691196, 0.030920821335099248, 0.0, 0.00016829071706504574*gmsf};
PointM42_dup = 2994; Point(2994) = {0.06997485262578262, 0.04039999999999999, 0.0, 0.00016829071706504574*gmsf};
PointM42_dup = 3004; Point(3004) = {0.06410294989553181, 0.04918792346390462, 0.0, 0.00016829071706504786*gmsf};
point_pylc_dup = 2850; Point(2850) = {0.08083405411411097, 0.004331073247704142, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2852; Point(2852) = {0.08183191303734956, 0.004396476376934286, 0, 0.00030851098907667415*gmsf};
point_pylc_dup = 2853; Point(2853) = {0.08170568499793539, 0.00632234409878479, 0, 0.00030851098907667415*gmsf};
point_pylc_dup = 2854; Point(2854) = {0.08070782607469679, 0.0062569409695546465, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2857; Point(2857) = {0.08025746152820995, 0.010566095260213175, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2869; Point(2869) = {0.07957718907619889, 0.014844981600894352, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2871; Point(2871) = {0.0805579743566021, 0.015040071922910478, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 2872; Point(2872) = {0.08018145003511097, 0.016932987514088713, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 2873; Point(2873) = {0.07920066475470774, 0.01673789719207258, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2876; Point(2876) = {0.07819169563810008, 0.020951401701049054, 0.0, 0.0001865814341300845*gmsf};
point_pylc_dup = 2888; Point(2888) = {0.07695873627022805, 0.02510488820308679, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2890; Point(2890) = {0.07790566639972313, 0.02542632766838995, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 2891; Point(2891) = {0.07728528823168804, 0.027253902818315502, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 2892; Point(2892) = {0.07633835810219293, 0.026932463353012342, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2895; Point(2895) = {0.07478804815678866, 0.030978223849954016, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2907; Point(2907) = {0.07302349814968086, 0.03493524320773444, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2909; Point(2909) = {0.07392037089121353, 0.03537753189795343, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 2910; Point(2910) = {0.07306675371909087, 0.03710849628911152, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 2911; Point(2911) = {0.07216988097755818, 0.036666207598892525, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2914; Point(2914) = {0.07010475643635031, 0.040475, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2926; Point(2926) = {0.06783880772985405, 0.04416784651521844, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2928; Point(2928) = {0.0686702773421566, 0.044723416748238036, 0.0, 0.00030851098907667626*gmsf};
point_pylc_dup = 2929; Point(2929) = {0.06759802679242875, 0.04632815309998195, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 2930; Point(2930) = {0.06676655718012621, 0.04577258286696235, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2933; Point(2933) = {0.0642219528965755, 0.04927923767825593, 0.0, 0.0001865814341300845*gmsf};
point_pylc_dup = 2945; Point(2945) = {0.0614933765012986, 0.05264472572318653, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2947; Point(2947) = {0.06224521630877756, 0.05330407153828659, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 2948; Point(2948) = {0.06097267888563443, 0.05475512236672102, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 2949; Point(2949) = {0.06022083907815545, 0.054095776551620955, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2559; Point(2559) = {0.08193230684071783, 0.002864762929763029, 0, 0.00031246726476474504*gmsf};
point_pylc_dup = 2561; Point(2561) = {0.11126767798545414, 0.0032842862313483155, 0, 0.003889371090557505*gmsf};
point_pylc_dup = 2564; Point(2564) = {0.11499750116148799, 0.007537334441223301, 0, 0.0043683573413105655*gmsf};
point_pylc_dup = 2563; Point(2563) = {0.11100606546853357, 0.0072757219243027305, 0, 0.001*gmsf};
point_pylc_dup = 2567; Point(2567) = {0.110744452951613, 0.011267157617257145, 0, 0.003889371090557505*gmsf};
point_pylc_dup = 2569; Point(2569) = {0.08160529119456712, 0.007854057545956047, 0, 0.00031246726476474716*gmsf};
point_pylc_dup = 2590; Point(2590) = {0.08085743800089684, 0.013534566517491518, 0.0, 0.0003124672647647429*gmsf};
point_pylc_dup = 2592; Point(2592) = {0.10988708219973571, 0.017779535031959233, 0.0, 0.003889371090557503*gmsf};
point_pylc_dup = 2595; Point(2595) = {0.11302986203328413, 0.022483037441636666, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 2594; Point(2594) = {0.10910672091167122, 0.021702676153572156, 0.0, 0.001*gmsf};
point_pylc_dup = 2598; Point(2598) = {0.1083263596236067, 0.025625817275185078, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 2600; Point(2600) = {0.07988198639081623, 0.018438492919507672, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 2621; Point(2621) = {0.07839907597896349, 0.023972789919614962, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 2623; Point(2623) = {0.10662628797112485, 0.03197057105875494, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 2626; Point(2626) = {0.10912825062789262, 0.037044049437948014, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 2625; Point(2625) = {0.10534053010991219, 0.035758291576735365, 0.0, 0.001*gmsf};
point_pylc_dup = 2629; Point(2629) = {0.10405477224869955, 0.03954601209471579, 0.0, 0.003889371090557505*gmsf};
point_pylc_dup = 2631; Point(2631) = {0.07679187865244769, 0.028707440567090493, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 2652; Point(2652) = {0.0745992840306997, 0.034000832239700754, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 2654; Point(2654) = {0.10154108839293599, 0.045614581750818464, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 2657; Point(2657) = {0.10335942459819074, 0.05097122747782523, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 2656; Point(2656) = {0.09977193363205998, 0.04920207271694922, 0.0, 0.001*gmsf};
point_pylc_dup = 2660; Point(2660) = {0.09800277887118398, 0.05278956368307998, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 2662; Point(2662) = {0.07238784057960469, 0.0384851959473642, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 2683; Point(2683) = {0.06952307764984167, 0.043447110893353624, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 2685; Point(2685) = {0.09471849263983566, 0.058478114302374165, 0.0, 0.003889371090557503*gmsf};
point_pylc_dup = 2688; Point(2688) = {0.09582209015696745, 0.06402627368366276, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 2687; Point(2687) = {0.09249621170775726, 0.061803992751584345, 0.0, 0.001*gmsf};
point_pylc_dup = 2691; Point(2691) = {0.09027393077567886, 0.06512987120079453, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 2693; Point(2693) = {0.06674522648474367, 0.047604458954866355, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 2714; Point(2714) = {0.06325731213495615, 0.05214999743380636, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 2716; Point(2716) = {0.08627523721674032, 0.07034107010501991, 0.0, 0.003889371090557505*gmsf};
point_pylc_dup = 2719; Point(2719) = {0.08664521318625597, 0.0759858125953361, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 2718; Point(2718) = {0.08363785395634005, 0.07334842933493584, 0.0, 0.001*gmsf};
point_pylc_dup = 2722; Point(2722) = {0.08100047069593977, 0.07635578856485174, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 2724; Point(2724) = {0.05996058305945583, 0.05590919647120125, 0.0, 0.00031246726476474716*gmsf};

// Lines and Curves
Line_dup = 1371;Line(Line_dup) = {2355, 2356};
lowerLine4_dup = 1374;Line(lowerLine4_dup) = {2356, 2362};
lowerLine3_dup = 1375;Line(lowerLine3_dup) = {2363, 2362};
Line_dup = 1370;Line(Line_dup) = {2353, 2354};
lowerLine1_dup = 1372;Line(lowerLine1_dup) = {2354, 2358};
lowerLine2_dup = 1373;Line(lowerLine2_dup) = {2358, 2360};
Line_dup = 1376;Line(Line_dup) = {2365, 2366};
lowerLine4_dup = 1377;Line(lowerLine4_dup) = {2366, 2368};
lowerLine3_dup = 1378;Line(lowerLine3_dup) = {2369, 2368};
Line_dup = 1379;Line(Line_dup) = {2371, 2372};
lowerLine1_dup = 1380;Line(lowerLine1_dup) = {2372, 2374};
lowerLine2_dup = 1381;Line(lowerLine2_dup) = {2374, 2376};
InnerLimit = 1297;Circle(InnerLimit) = {2371, 2227, 2353};
MB_CurveRotor = 1359;Circle(MB_CurveRotor) = {2360, 2227, 2376};
MB_CurveRotor_dup = 1393;Circle(MB_CurveRotor_dup) = {2376, 2227, 2394};
MB_CurveRotor_dup = 1395;Circle(MB_CurveRotor_dup) = {2394, 2227, 2397};
MB_CurveRotor_dup = 1397;Circle(MB_CurveRotor_dup) = {2397, 2227, 2400};
MB_CurveRotor_dup = 1399;Circle(MB_CurveRotor_dup) = {2400, 2227, 2403};
MB_CurveRotor_dup = 1401;Circle(MB_CurveRotor_dup) = {2403, 2227, 2406};
MB_CurveRotor_dup = 1403;Circle(MB_CurveRotor_dup) = {2406, 2227, 2409};
MB_CurveRotor_dup = 1405;Circle(MB_CurveRotor_dup) = {2409, 2227, 2360};
rotorBand1_dup = 1647;Circle(rotorBand1_dup) = {2358, 2227, 2374};
Line_dup = 1456;Line(Line_dup) = {2503, 2504};
Line_dup = 1457;Line(Line_dup) = {2504, 2506};
Line_dup = 1458;Line(Line_dup) = {2506, 2508};
Line_dup = 1459;Line(Line_dup) = {2508, 2510};
Line_dup = 1460;Line(Line_dup) = {2510, 2512};
Line_dup = 1461;Line(Line_dup) = {2512, 2503};
Line_dup = 1466;Line(Line_dup) = {2523, 2524};
Line_dup = 1467;Line(Line_dup) = {2524, 2526};
Line_dup = 1468;Line(Line_dup) = {2526, 2528};
Line_dup = 1469;Line(Line_dup) = {2528, 2510};
Line_dup = 1470;Line(Line_dup) = {2510, 2532};
Line_dup = 1471;Line(Line_dup) = {2532, 2523};
Line_dup = 1450;Line(Line_dup) = {2492, 2493};
Line_dup = 1451;Line(Line_dup) = {2493, 2503};
Line_dup = 1453;Line(Line_dup) = {2512, 2499};
CircleArc_dup = 1455;Circle(CircleArc_dup) = {2499, 2227, 2492};
Line_dup = 1462;Line(Line_dup) = {2508, 2516};
Line_dup = 1463;Line(Line_dup) = {2516, 2528};
Line_dup = 1472;Line(Line_dup) = {2535, 2536};
Line_dup = 1473;Line(Line_dup) = {2536, 2523};
Line_dup = 1475;Line(Line_dup) = {2532, 2542};
CircleArc_dup = 1477;Circle(CircleArc_dup) = {2542, 2227, 2535};
CircleArc_dup = 1641;Circle(CircleArc_dup) = {2354, 2227, 2372};
OuterLimit = 1328;Circle(OuterLimit) = {2284, 2227, 2355};
OuterLimit_dup = 1407;Circle(OuterLimit_dup) = {2413, 2227, 2284};
OuterLimit_dup = 1409;Circle(OuterLimit_dup) = {2416, 2227, 2413};
OuterLimit_dup = 1411;Circle(OuterLimit_dup) = {2419, 2227, 2416};
OuterLimit_dup = 1413;Circle(OuterLimit_dup) = {2422, 2227, 2419};
OuterLimit_dup = 1415;Circle(OuterLimit_dup) = {2365, 2227, 2422};
MB_CurveStator = 1367;Circle(MB_CurveStator) = {2363, 2227, 2352};
MB_CurveStator_dup = 1383;Circle(MB_CurveStator_dup) = {2352, 2227, 2379};
MB_CurveStator_dup = 1385;Circle(MB_CurveStator_dup) = {2379, 2227, 2382};
MB_CurveStator_dup = 1387;Circle(MB_CurveStator_dup) = {2382, 2227, 2385};
MB_CurveStator_dup = 1389;Circle(MB_CurveStator_dup) = {2385, 2227, 2388};
MB_CurveStator_dup = 1391;Circle(MB_CurveStator_dup) = {2388, 2227, 2369};
statorCircle4_dup = 1719;Circle(statorCircle4_dup) = {2362, 2227, 2964};
upperLine3_dup = 1723;Line(upperLine3_dup) = {2352, 2964};
statorCircle4_dup = 1725;Circle(statorCircle4_dup) = {2964, 2227, 2974};
upperLine3_dup = 1729;Line(upperLine3_dup) = {2379, 2974};
statorCircle4_dup = 1731;Circle(statorCircle4_dup) = {2974, 2227, 2984};
upperLine3_dup = 1735;Line(upperLine3_dup) = {2382, 2984};
statorCircle4_dup = 1737;Circle(statorCircle4_dup) = {2984, 2227, 2994};
upperLine3_dup = 1741;Line(upperLine3_dup) = {2385, 2994};
statorCircle4_dup = 1743;Circle(statorCircle4_dup) = {2994, 2227, 3004};
upperLine3_dup = 1747;Line(upperLine3_dup) = {2388, 3004};
statorCircle4_dup = 1749;Circle(statorCircle4_dup) = {3004, 2227, 2368};
CircleArc_dup = 1653;Circle(CircleArc_dup) = {2356, 2227, 2850};
Line_dup = 1654;Line(Line_dup) = {2850, 2852};
Line_dup = 1655;Line(Line_dup) = {2853, 2854};
CircleArc_dup = 1657;Circle(CircleArc_dup) = {2854, 2227, 2857};
interface_line_slot_opening___slot_dup = 1658;Line(interface_line_slot_opening___slot_dup) = {2852, 2853};
upperLine4_dup = 1662;Line(upperLine4_dup) = {2857, 2964};
CircleArc_dup = 1664;Circle(CircleArc_dup) = {2857, 2227, 2869};
Line_dup = 1665;Line(Line_dup) = {2869, 2871};
Line_dup = 1666;Line(Line_dup) = {2872, 2873};
CircleArc_dup = 1668;Circle(CircleArc_dup) = {2873, 2227, 2876};
interface_line_slot_opening___slot_dup = 1669;Line(interface_line_slot_opening___slot_dup) = {2871, 2872};
upperLine4_dup = 1673;Line(upperLine4_dup) = {2876, 2974};
CircleArc_dup = 1675;Circle(CircleArc_dup) = {2876, 2227, 2888};
Line_dup = 1676;Line(Line_dup) = {2888, 2890};
Line_dup = 1677;Line(Line_dup) = {2891, 2892};
CircleArc_dup = 1679;Circle(CircleArc_dup) = {2892, 2227, 2895};
interface_line_slot_opening___slot_dup = 1680;Line(interface_line_slot_opening___slot_dup) = {2890, 2891};
upperLine4_dup = 1684;Line(upperLine4_dup) = {2895, 2984};
CircleArc_dup = 1686;Circle(CircleArc_dup) = {2895, 2227, 2907};
Line_dup = 1687;Line(Line_dup) = {2907, 2909};
Line_dup = 1688;Line(Line_dup) = {2910, 2911};
CircleArc_dup = 1690;Circle(CircleArc_dup) = {2911, 2227, 2914};
interface_line_slot_opening___slot_dup = 1691;Line(interface_line_slot_opening___slot_dup) = {2909, 2910};
upperLine4_dup = 1695;Line(upperLine4_dup) = {2914, 2994};
CircleArc_dup = 1697;Circle(CircleArc_dup) = {2914, 2227, 2926};
Line_dup = 1698;Line(Line_dup) = {2926, 2928};
Line_dup = 1699;Line(Line_dup) = {2929, 2930};
CircleArc_dup = 1701;Circle(CircleArc_dup) = {2930, 2227, 2933};
interface_line_slot_opening___slot_dup = 1702;Line(interface_line_slot_opening___slot_dup) = {2928, 2929};
upperLine4_dup = 1706;Line(upperLine4_dup) = {2933, 3004};
CircleArc_dup = 1708;Circle(CircleArc_dup) = {2933, 2227, 2945};
Line_dup = 1709;Line(Line_dup) = {2945, 2947};
Line_dup = 1710;Line(Line_dup) = {2948, 2949};
CircleArc_dup = 1712;Circle(CircleArc_dup) = {2949, 2227, 2366};
interface_line_slot_opening___slot_dup = 1713;Line(interface_line_slot_opening___slot_dup) = {2947, 2948};
Line_dup = 1478;Line(Line_dup) = {2857, 2284};
Line_dup = 1485;Line(Line_dup) = {2852, 2559};
Line_dup = 1486;Line(Line_dup) = {2559, 2561};
CircleArc_dup = 1488;Circle(CircleArc_dup) = {2561, 2563, 2564};
CircleArc_dup = 1490;Circle(CircleArc_dup) = {2564, 2563, 2567};
Line_dup = 1491;Line(Line_dup) = {2567, 2569};
Line_dup = 1492;Line(Line_dup) = {2569, 2853};
Line_dup = 1496;Line(Line_dup) = {2876, 2413};
Line_dup = 1503;Line(Line_dup) = {2871, 2590};
Line_dup = 1504;Line(Line_dup) = {2590, 2592};
CircleArc_dup = 1506;Circle(CircleArc_dup) = {2592, 2594, 2595};
CircleArc_dup = 1508;Circle(CircleArc_dup) = {2595, 2594, 2598};
Line_dup = 1509;Line(Line_dup) = {2598, 2600};
Line_dup = 1510;Line(Line_dup) = {2600, 2872};
Line_dup = 1514;Line(Line_dup) = {2895, 2416};
Line_dup = 1521;Line(Line_dup) = {2890, 2621};
Line_dup = 1522;Line(Line_dup) = {2621, 2623};
CircleArc_dup = 1524;Circle(CircleArc_dup) = {2623, 2625, 2626};
CircleArc_dup = 1526;Circle(CircleArc_dup) = {2626, 2625, 2629};
Line_dup = 1527;Line(Line_dup) = {2629, 2631};
Line_dup = 1528;Line(Line_dup) = {2631, 2891};
Line_dup = 1532;Line(Line_dup) = {2914, 2419};
Line_dup = 1539;Line(Line_dup) = {2909, 2652};
Line_dup = 1540;Line(Line_dup) = {2652, 2654};
CircleArc_dup = 1542;Circle(CircleArc_dup) = {2654, 2656, 2657};
CircleArc_dup = 1544;Circle(CircleArc_dup) = {2657, 2656, 2660};
Line_dup = 1545;Line(Line_dup) = {2660, 2662};
Line_dup = 1546;Line(Line_dup) = {2662, 2910};
Line_dup = 1550;Line(Line_dup) = {2933, 2422};
Line_dup = 1557;Line(Line_dup) = {2928, 2683};
Line_dup = 1558;Line(Line_dup) = {2683, 2685};
CircleArc_dup = 1560;Circle(CircleArc_dup) = {2685, 2687, 2688};
CircleArc_dup = 1562;Circle(CircleArc_dup) = {2688, 2687, 2691};
Line_dup = 1563;Line(Line_dup) = {2691, 2693};
Line_dup = 1564;Line(Line_dup) = {2693, 2929};
Line_dup = 1575;Line(Line_dup) = {2947, 2714};
Line_dup = 1576;Line(Line_dup) = {2714, 2716};
CircleArc_dup = 1578;Circle(CircleArc_dup) = {2716, 2718, 2719};
CircleArc_dup = 1580;Circle(CircleArc_dup) = {2719, 2718, 2722};
Line_dup = 1581;Line(Line_dup) = {2722, 2724};
Line_dup = 1582;Line(Line_dup) = {2724, 2948};

// Surfaces

Curve Loop(170) = {1647,1381,-1359,-1373};
Surf_rotorAirGap2_dup = {170};
Plane Surface(Surf_rotorAirGap2_dup) = {170};

Curve Loop(153) = {1456,1457,1458,1459,1460,1461};
Surf_Magnet_dup = {153};
Plane Surface(Surf_Magnet_dup) = {153};

Curve Loop(155) = {1466,1467,1468,1469,1470,1471};
Surf_Magnet_dup = {155};
Plane Surface(Surf_Magnet_dup) = {155};

Curve Loop(152) = {1450,1451,-1461,1453,1455};
Surf_Loch_dup = {152};
Plane Surface(Surf_Loch_dup) = {152};

Curve Loop(154) = {1462,1463,1469,-1459};
Surf_Loch_dup = {154};
Plane Surface(Surf_Loch_dup) = {154};

Curve Loop(156) = {1472,1473,-1471,1475,1477};
Surf_Loch_dup = {156};
Plane Surface(Surf_Loch_dup) = {156};

Curve Loop(169) = {1641,1380,-1647,-1372};
Surf_rotorAirGap1_dup = {169};
Plane Surface(Surf_rotorAirGap1_dup) = {169};

Curve Loop(147) = {1450,1451,-1461,1453,1455};
Surf_Loch_dup = {147};
Plane Surface(Surf_Loch_dup) = {147};
Curve Loop(148) = {1456,1457,1458,1459,1460,1461};
Surf_Magnet_dup = {148};
Plane Surface(Surf_Magnet_dup) = {148};
Curve Loop(149) = {1462,1463,1469,-1459};
Surf_Loch_dup = {149};
Plane Surface(Surf_Loch_dup) = {149};
Curve Loop(150) = {1466,1467,1468,1469,1470,1471};
Surf_Magnet_dup = {150};
Plane Surface(Surf_Magnet_dup) = {150};
Curve Loop(151) = {1472,1473,-1471,1475,1477};
Surf_Loch_dup = {151};
Plane Surface(Surf_Loch_dup) = {151};
Curve Loop(146) = {1370,1641,-1379,1297};
Surf_Rotorblech_dup = {146};
Plane Surface(Surf_Rotorblech_dup) = {146, 147, 148, 149, 150, 151};

Curve Loop(177) = {1719,-1723,-1367,1375};
Surf_statorAirGap2_dup = {177};
Plane Surface(Surf_statorAirGap2_dup) = {177};

Curve Loop(178) = {1725,-1729,-1383,1723};
Surf_statorAirGap2_dup = {178};
Plane Surface(Surf_statorAirGap2_dup) = {178};

Curve Loop(179) = {1731,-1735,-1385,1729};
Surf_statorAirGap2_dup = {179};
Plane Surface(Surf_statorAirGap2_dup) = {179};

Curve Loop(180) = {1737,-1741,-1387,1735};
Surf_statorAirGap2_dup = {180};
Plane Surface(Surf_statorAirGap2_dup) = {180};

Curve Loop(181) = {1743,-1747,-1389,1741};
Surf_statorAirGap2_dup = {181};
Plane Surface(Surf_statorAirGap2_dup) = {181};

Curve Loop(182) = {1749,-1378,-1391,1747};
Surf_statorAirGap2_dup = {182};
Plane Surface(Surf_statorAirGap2_dup) = {182};

Curve Loop(171) = {1653,1654,1658,1655,1657,1662,-1719,-1374};
Surf_statorAirGap1_dup = {171};
Plane Surface(Surf_statorAirGap1_dup) = {171};

Curve Loop(172) = {1664,1665,1669,1666,1668,1673,-1725,-1662};
Surf_statorAirGap1_dup = {172};
Plane Surface(Surf_statorAirGap1_dup) = {172};

Curve Loop(173) = {1675,1676,1680,1677,1679,1684,-1731,-1673};
Surf_statorAirGap1_dup = {173};
Plane Surface(Surf_statorAirGap1_dup) = {173};

Curve Loop(174) = {1686,1687,1691,1688,1690,1695,-1737,-1684};
Surf_statorAirGap1_dup = {174};
Plane Surface(Surf_statorAirGap1_dup) = {174};

Curve Loop(175) = {1697,1698,1702,1699,1701,1706,-1743,-1695};
Surf_statorAirGap1_dup = {175};
Plane Surface(Surf_statorAirGap1_dup) = {175};

Curve Loop(176) = {1708,1709,1713,1710,1712,1377,-1749,-1706};
Surf_statorAirGap1_dup = {176};
Plane Surface(Surf_statorAirGap1_dup) = {176};

Curve Loop(157) = {1478,1328,1371,1653,1654,1485,1486,1488,1490,1491,1492,1655,1657};
Surf_Statorblech_dup = {157};
Plane Surface(Surf_Statorblech_dup) = {157};

Curve Loop(158) = {1496,1407,-1478,1664,1665,1503,1504,1506,1508,1509,1510,1666,1668};
Surf_Statorblech_dup = {158};
Plane Surface(Surf_Statorblech_dup) = {158};

Curve Loop(159) = {1514,1409,-1496,1675,1676,1521,1522,1524,1526,1527,1528,1677,1679};
Surf_Statorblech_dup = {159};
Plane Surface(Surf_Statorblech_dup) = {159};

Curve Loop(160) = {1532,1411,-1514,1686,1687,1539,1540,1542,1544,1545,1546,1688,1690};
Surf_Statorblech_dup = {160};
Plane Surface(Surf_Statorblech_dup) = {160};

Curve Loop(161) = {1550,1413,-1532,1697,1698,1557,1558,1560,1562,1563,1564,1699,1701};
Surf_Statorblech_dup = {161};
Plane Surface(Surf_Statorblech_dup) = {161};

Curve Loop(162) = {1376,-1712,-1710,-1582,-1581,-1580,-1578,-1576,-1575,-1709,-1708,1550,-1415};
Surf_Statorblech_dup = {162};
Plane Surface(Surf_Statorblech_dup) = {162};

Curve Loop(163) = {1485,1486,1488,1490,1491,1492,-1658};
Surf_Stator_Nut_dup = {163};
Plane Surface(Surf_Stator_Nut_dup) = {163};

Curve Loop(164) = {1503,1504,1506,1508,1509,1510,-1669};
Surf_Stator_Nut_dup = {164};
Plane Surface(Surf_Stator_Nut_dup) = {164};

Curve Loop(165) = {1521,1522,1524,1526,1527,1528,-1680};
Surf_Stator_Nut_dup = {165};
Plane Surface(Surf_Stator_Nut_dup) = {165};

Curve Loop(166) = {1539,1540,1542,1544,1545,1546,-1691};
Surf_Stator_Nut_dup = {166};
Plane Surface(Surf_Stator_Nut_dup) = {166};

Curve Loop(167) = {1557,1558,1560,1562,1563,1564,-1702};
Surf_Stator_Nut_dup = {167};
Plane Surface(Surf_Stator_Nut_dup) = {167};

Curve Loop(168) = {1575,1576,1578,1580,1581,1582,-1713};
Surf_Stator_Nut_dup = {168};
Plane Surface(Surf_Stator_Nut_dup) = {168};

// Color code
If (!Flag_individualColoring)
Color SkyBlue {Surface {170}; }
Color Red {Surface {153}; }
Color Red {Surface {155}; }
Color Gray70 {Surface {152}; }
Color Grey49 {Surface {154}; }
Color Ivory1 {Surface {156}; }
Color SkyBlue {Surface {169}; }
Color SteelBlue {Surface {146}; }
Color SkyBlue {Surface {177}; }
Color SkyBlue {Surface {178}; }
Color SkyBlue {Surface {179}; }
Color SkyBlue {Surface {180}; }
Color SkyBlue {Surface {181}; }
Color SkyBlue {Surface {182}; }
Color SkyBlue {Surface {171}; }
Color SkyBlue {Surface {172}; }
Color SkyBlue {Surface {173}; }
Color SkyBlue {Surface {174}; }
Color SkyBlue {Surface {175}; }
Color SkyBlue {Surface {176}; }
Color SteelBlue4 {Surface {157}; }
Color SteelBlue4 {Surface {158}; }
Color SteelBlue4 {Surface {159}; }
Color SteelBlue4 {Surface {160}; }
Color SteelBlue4 {Surface {161}; }
Color SteelBlue4 {Surface {162}; }
Color Magenta {Surface {163}; }
Color Magenta {Surface {164}; }
Color Cyan {Surface {165}; }
Color Cyan {Surface {166}; }
Color Yellow4 {Surface {167}; }
Color Yellow4 {Surface {168}; }
EndIf

// Physical Elements
// primaryLineS
Physical Curve("primaryLineS", 3) = {1371,1374,1375};
// primaryLineR
Physical Curve("primaryLineR", 2) = {1370,1372,1373};
// slaveLineS
Physical Curve("slaveLineS", 5) = {1376,1377,1378};
// slaveLineR
Physical Curve("slaveLineR", 4) = {1379,1380,1381};
// innerLimit
Physical Curve("innerLimit", 16) = {1297};
// Rotor_Bnd_MB_1
Physical Curve("Rotor_Bnd_MB_1", 7) = {1359};
// Rotor_Bnd_MB_2
Physical Curve("Rotor_Bnd_MB_2", 8) = {1393};
// Rotor_Bnd_MB_3
Physical Curve("Rotor_Bnd_MB_3", 9) = {1395};
// Rotor_Bnd_MB_4
Physical Curve("Rotor_Bnd_MB_4", 10) = {1397};
// Rotor_Bnd_MB_5
Physical Curve("Rotor_Bnd_MB_5", 11) = {1399};
// Rotor_Bnd_MB_6
Physical Curve("Rotor_Bnd_MB_6", 12) = {1401};
// Rotor_Bnd_MB_7
Physical Curve("Rotor_Bnd_MB_7", 13) = {1403};
// Rotor_Bnd_MB_8
Physical Curve("Rotor_Bnd_MB_8", 14) = {1405};
// LuR2
Physical Surface("LuR2", 31) = {170};
// Mag0_0
Physical Surface("Mag0_0", 19) = {153};
// Mag1_0
Physical Surface("Mag1_0", 21) = {155};
// Lpl0
Physical Surface("Lpl0", 18) = {152};
// Lpl1
Physical Surface("Lpl1", 20) = {154};
// Lpl2
Physical Surface("Lpl2", 22) = {156};
// LuR1
Physical Surface("LuR1", 30) = {169};
// Pol
Physical Surface("Pol", 17) = {146};
// outerLimit
Physical Curve("outerLimit", 15) = {1328,1407,1409,1411,1413,1415};
// mbStator
Physical Curve("mbStator", 6) = {1367,1383,1385,1387,1389,1391};
// StLu2
Physical Surface("StLu2", 33) = {177,178,179,180,181,182};
// StLu1
Physical Surface("StLu1", 32) = {171,172,173,174,175,176};
// StNut
Physical Surface("StNut", 23) = {157,158,159,160,161,162};
// StCu0_0_Up
Physical Surface("StCu0_0_Up", 24) = {163};
// StCu0_1_Up
Physical Surface("StCu0_1_Up", 25) = {164};
// StCu0_2_Wn
Physical Surface("StCu0_2_Wn", 26) = {165};
// StCu0_3_Wn
Physical Surface("StCu0_3_Wn", 27) = {166};
// StCu0_4_Vp
Physical Surface("StCu0_4_Vp", 28) = {167};
// StCu0_5_Vp
Physical Surface("StCu0_5_Vp", 29) = {168};

DefineConstant[
	mm = 1e-3,
	Flag_SpecifyMeshSize = {0, Name StrCat[INPUT_MESH, "04User defined surface mesh sizes"],Choices {0, 1}}
];
If(Flag_SpecifyMeshSize)
	DefineConstant[
		Lpl_msf = {0.842, Name StrCat[INPUT_MESH, "05Mesh Size/Loch (Polluecke) [mm]"],Min 0.0842, Max 8.42, Step 0.1,Visible Flag_SpecifyMeshSize},
		Mag_msf = {0.989, Name StrCat[INPUT_MESH, "05Mesh Size/Magnet [mm]"],Min 0.0989, Max 9.89, Step 0.1,Visible Flag_SpecifyMeshSize},
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
	MeshSize { PointsOf {Surface{ 152,154,156 };} } = Lpl_msf*mm;
	MeshSize { PointsOf {Surface{ 153,155 };} } = Mag_msf*mm;
	MeshSize { PointsOf {Surface{ 146 };} } = Pol_msf*mm;
	MeshSize { PointsOf {Surface{ 169,170 };} } = LuR_msf*mm;
	MeshSize { PointsOf {Surface{ 169 };} } = LuR1_msf*mm;
	MeshSize { PointsOf {Surface{ 170 };} } = LuR2_msf*mm;
	MeshSize { PointsOf {Surface{ 163,164,165,166,167,168 };} } = StCu_msf*mm;
	MeshSize { PointsOf {Surface{ 157,158,159,160,161,162 };} } = StNut_msf*mm;
	MeshSize { PointsOf {Surface{ 171,172,173,174,175,176,177,178,179,180,181,182 };} } = StLu_msf*mm;
	MeshSize { PointsOf {Surface{ 171,172,173,174,175,176 };} } = StLu1_msf*mm;
	MeshSize { PointsOf {Surface{ 177,178,179,180,181,182 };} } = StLu2_msf*mm;
EndIf

// Mesh operations

// Do not switch mesh algorithm on failure, because this led to mesh errors in the past.
Mesh.AlgorithmSwitchOnFailure = 0;DefineConstant[Flag_CompoundMesh = {0, Name StrCat[INPUT_MESH, "Compound Mesh"], Choices {0,1}, Help "Use Compound Mesh to ignore lines between segments while meshing.",Visible Flag_ExpertMode}];
If (Flag_CompoundMesh)
Compound Surface{157,158,159,160,161,162}; // stator domainLam
Compound Surface{177,178,179,180,181,182}; // stator airGap
EndIf // (Flag_CompoundMesh)

// Add Periodic Mesh to model symmetry boundary-lines
primaryLines = {1370,1372,1373,1371,1374,1375};
secondaryLines = {1379,1380,1381,1376,1377,1378};
Periodic Curve{secondaryLines[]} = {primaryLines[]} Rotate {{0,0,1}, {0,0,0}, 2*Pi/8};

// Add mesh size setting for Movingband lines
DefineConstant[
	NbrMbSegments = {3370.0, Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],Max 1440, Min 180, Step 10, Help "Set the number of mesh segments on the interface between rotor/statorairgap and movingband. Value represents number of segments on whole circle.", Visible Flag_ExpertMode},
	r_MB_R = 0.08049999999999999
];
MB_LinesR = {1359,1393,1395,1397,1399,1401,1403,1405};
MeshSize{ PointsOf{Line{MB_LinesR[]};}} = 2*Pi*r_MB_R/NbrMbSegments;

MB_LinesS = {1367,1383,1385,1387,1389,1391};
MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*0.08065/NbrMbSegments;

Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)

// Create boundary lines for moving rotor contour plot
rotorBndLines[] = Boundary{ Physical Surface{ 19,21 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 17 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 31 }; };
statorBndLines[] = Boundary{ Physical Surface{ 3,5,6,15,23,24,25,26,27,28,29,32,33 }; };
Physical Line("DomainPlotMovingGeo",1) = {rotorBndLines[], statorBndLines[]};
