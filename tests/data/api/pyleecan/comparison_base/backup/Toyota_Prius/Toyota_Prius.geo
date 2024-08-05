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
point_pylc_dup = 2348; Point(2348) = {0.13462, 0.0, 0, 0.006730999999999999*gmsf};
point_pylc_dup = 2349; Point(2349) = {0.08095, 0.0, 0, 0.00018658143413008237*gmsf};
PointM41_dup = 2355; Point(2355) = {0.0808, 0, 0, 0.00016829071706504786*gmsf};
PointM31_dup = 2356; Point(2356) = {0.08065, 0, 0, 0.00015000000000001124*gmsf};
point_pylc_dup = 2346; Point(2346) = {0.05532, 0.0, 0, 0.005871021118012428*gmsf};
point_pylc_dup = 2347; Point(2347) = {0.0802, 0.0, 0, 0.00021816149068324008*gmsf};
PointM11_dup = 2351; Point(2351) = {0.08034999999999999, 0, 0, 0.00018408074534162567*gmsf};
PointM21_dup = 2353; Point(2353) = {0.08049999999999999, 0, 0, 0.00015000000000001124*gmsf};
point_pylc_dup = 2358; Point(2358) = {0.09519071488333303, 0.09519071488333303, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 2359; Point(2359) = {0.057240293937051025, 0.057240293937051025, 0.0, 0.00018658143413008237*gmsf};
PointM41_dup = 2361; Point(2361) = {0.05713422791987304, 0.05713422791987304, 0.0, 0.00016829071706504786*gmsf};
PointM31_dup = 2362; Point(2362) = {0.05702816190269506, 0.05702816190269506, 0.0, 0.00015000000000001124*gmsf};
point_pylc_dup = 2364; Point(2364) = {0.03911714713523981, 0.03911714713523981, 0.0, 0.005871021118012428*gmsf};
point_pylc_dup = 2365; Point(2365) = {0.05670996385116111, 0.05670996385116111, 0.0, 0.00021816149068324008*gmsf};
PointM11_dup = 2367; Point(2367) = {0.05681602986833909, 0.05681602986833909, 0.0, 0.00018408074534162567*gmsf};
PointM21_dup = 2369; Point(2369) = {0.05692209588551707, 0.05692209588551707, 0.0, 0.00015000000000001124*gmsf};
point_pylc = 2220; Point(2220) = {0, 0, 0, 0.001*gmsf};
PointM22_dup = 2387; Point(2387) = {0.0, 0.08049999999999999, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 2390; Point(2390) = {-0.05692209588551706, 0.056922095885517075, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 2393; Point(2393) = {-0.08049999999999999, 0.0, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 2396; Point(2396) = {-0.056922095885517075, -0.05692209588551706, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 2399; Point(2399) = {-6.938893903907228e-18, -0.08049999999999999, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 2402; Point(2402) = {0.056922095885517054, -0.05692209588551708, 0.0, 0.00015000000000001124*gmsf};
point_pylc_dup = 2496; Point(2496) = {0.07189332074897073, 0.008478350008583092, 0, 0.001*gmsf};
point_pylc_dup = 2497; Point(2497) = {0.07112686475225904, 0.007836053188487666, 0, 0.001*gmsf};
point_pylc_dup = 2499; Point(2499) = {0.058987454852455525, 0.02232207152633855, 0, 0.001*gmsf};
point_pylc_dup = 2501; Point(2501) = {0.059753910849167216, 0.02296436834643398, 0, 0.001*gmsf};
point_pylc_dup = 2503; Point(2503) = {0.0639694188310815, 0.026497000856958816, 0, 0.001*gmsf};
point_pylc_dup = 2505; Point(2505) = {0.07610882873088501, 0.01201098251910793, 0, 0.000933687570242861*gmsf};
point_pylc_dup = 2516; Point(2516) = {0.056831353407958855, 0.0448411558392746, 0, 0.001*gmsf};
point_pylc_dup = 2517; Point(2517) = {0.055835214738178894, 0.0447533620435427, 0, 0.001*gmsf};
point_pylc_dup = 2519; Point(2519) = {0.057494517477511754, 0.02592634118470148, 0, 0.001*gmsf};
point_pylc_dup = 2521; Point(2521) = {0.05849065614729172, 0.026014134980433378, 0, 0.001*gmsf};
point_pylc_dup = 2525; Point(2525) = {0.06231011609174863, 0.045324021715800036, 0, 0.000933687570242861*gmsf};
point_pylc_dup = 2485; Point(2485) = {0.07838807307237497, 0.007000000000000003, 0, 0.0005589689440993886*gmsf};
point_pylc_dup = 2486; Point(2486) = {0.07313219096927659, 0.007000000000000003, 0, 0.001*gmsf};
point_pylc_dup = 2492; Point(2492) = {0.07810937152746876, 0.009623724828976162, 0, 0.0005589689440993886*gmsf};
point_pylc_dup = 2509; Point(2509) = {0.05864256321587955, 0.024290545016338896, 0, 0.001*gmsf};
point_pylc_dup = 2528; Point(2528) = {0.06037848550192878, 0.050478990565317114, 0, 0.0005589689440993886*gmsf};
point_pylc_dup = 2529; Point(2529) = {0.05666201562571091, 0.04676252068909924, 0, 0.001*gmsf};
point_pylc_dup = 2535; Point(2535) = {0.06203666736813499, 0.048426665194450214, 0, 0.0005589689440993865*gmsf};
point_pylc = 2277; Point(2277) = {0.13346830723814235, 0.017571435996663342, 0, 0.006730999999999999*gmsf};
point_pylc_dup = 2406; Point(2406) = {0.13003293473503436, 0.034842219851701335, 0.0, 0.006730999999999997*gmsf};
point_pylc_dup = 2409; Point(2409) = {0.12437266266666941, 0.051516843664988377, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 2412; Point(2412) = {0.11658433985746111, 0.06731, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 2415; Point(2415) = {0.10680122667000608, 0.08195146357315396, 0.0, 0.006730999999999999*gmsf};
PointM32 = 2345; Point(2345) = {0.07996002806979781, 0.010526937402547159, 0, 0.00015000000000001124*gmsf};
PointM32_dup = 2372; Point(2372) = {0.07790191789021336, 0.020873755987518297, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 2375; Point(2375) = {0.07451088429703527, 0.030863418820244487, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 2378; Point(2378) = {0.06984494881521497, 0.040325, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 2381; Point(2381) = {0.06398394689448812, 0.04909660924955331, 0.0, 0.00015000000000001124*gmsf};
PointM42_dup = 2957; Point(2957) = {0.08010874479900387, 0.010546516331380167, 0, 0.00016829071706504786*gmsf};
PointM42_dup = 2967; Point(2967) = {0.0780468067641567, 0.020912578844283672, 0.0, 0.00016829071706504786*gmsf};
PointM42_dup = 2977; Point(2977) = {0.07464946622691196, 0.030920821335099248, 0.0, 0.00016829071706504574*gmsf};
PointM42_dup = 2987; Point(2987) = {0.06997485262578262, 0.04039999999999999, 0.0, 0.00016829071706504574*gmsf};
PointM42_dup = 2997; Point(2997) = {0.06410294989553181, 0.04918792346390462, 0.0, 0.00016829071706504786*gmsf};
point_pylc_dup = 2843; Point(2843) = {0.08083405411411097, 0.004331073247704142, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2845; Point(2845) = {0.08183191303734956, 0.004396476376934286, 0, 0.00030851098907667415*gmsf};
point_pylc_dup = 2846; Point(2846) = {0.08170568499793539, 0.00632234409878479, 0, 0.00030851098907667415*gmsf};
point_pylc_dup = 2847; Point(2847) = {0.08070782607469679, 0.0062569409695546465, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2850; Point(2850) = {0.08025746152820995, 0.010566095260213175, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2862; Point(2862) = {0.07957718907619889, 0.014844981600894352, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2864; Point(2864) = {0.0805579743566021, 0.015040071922910478, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 2865; Point(2865) = {0.08018145003511097, 0.016932987514088713, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 2866; Point(2866) = {0.07920066475470774, 0.01673789719207258, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2869; Point(2869) = {0.07819169563810008, 0.020951401701049054, 0.0, 0.0001865814341300845*gmsf};
point_pylc_dup = 2881; Point(2881) = {0.07695873627022805, 0.02510488820308679, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2883; Point(2883) = {0.07790566639972313, 0.02542632766838995, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 2884; Point(2884) = {0.07728528823168804, 0.027253902818315502, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 2885; Point(2885) = {0.07633835810219293, 0.026932463353012342, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2888; Point(2888) = {0.07478804815678866, 0.030978223849954016, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2900; Point(2900) = {0.07302349814968086, 0.03493524320773444, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2902; Point(2902) = {0.07392037089121353, 0.03537753189795343, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 2903; Point(2903) = {0.07306675371909087, 0.03710849628911152, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 2904; Point(2904) = {0.07216988097755818, 0.036666207598892525, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2907; Point(2907) = {0.07010475643635031, 0.040475, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2919; Point(2919) = {0.06783880772985405, 0.04416784651521844, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2921; Point(2921) = {0.0686702773421566, 0.044723416748238036, 0.0, 0.00030851098907667626*gmsf};
point_pylc_dup = 2922; Point(2922) = {0.06759802679242875, 0.04632815309998195, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 2923; Point(2923) = {0.06676655718012621, 0.04577258286696235, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2926; Point(2926) = {0.0642219528965755, 0.04927923767825593, 0.0, 0.0001865814341300845*gmsf};
point_pylc_dup = 2938; Point(2938) = {0.0614933765012986, 0.05264472572318653, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2940; Point(2940) = {0.06224521630877756, 0.05330407153828659, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 2941; Point(2941) = {0.06097267888563443, 0.05475512236672102, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 2942; Point(2942) = {0.06022083907815545, 0.054095776551620955, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 2552; Point(2552) = {0.08193230684071783, 0.002864762929763029, 0, 0.00031246726476474504*gmsf};
point_pylc_dup = 2554; Point(2554) = {0.11126767798545414, 0.0032842862313483155, 0, 0.003889371090557505*gmsf};
point_pylc_dup = 2557; Point(2557) = {0.11499750116148799, 0.007537334441223301, 0, 0.0043683573413105655*gmsf};
point_pylc_dup = 2556; Point(2556) = {0.11100606546853357, 0.0072757219243027305, 0, 0.001*gmsf};
point_pylc_dup = 2560; Point(2560) = {0.110744452951613, 0.011267157617257145, 0, 0.003889371090557505*gmsf};
point_pylc_dup = 2562; Point(2562) = {0.08160529119456712, 0.007854057545956047, 0, 0.00031246726476474716*gmsf};
point_pylc_dup = 2583; Point(2583) = {0.08085743800089684, 0.013534566517491518, 0.0, 0.0003124672647647429*gmsf};
point_pylc_dup = 2585; Point(2585) = {0.10988708219973571, 0.017779535031959233, 0.0, 0.003889371090557503*gmsf};
point_pylc_dup = 2588; Point(2588) = {0.11302986203328413, 0.022483037441636666, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 2587; Point(2587) = {0.10910672091167122, 0.021702676153572156, 0.0, 0.001*gmsf};
point_pylc_dup = 2591; Point(2591) = {0.1083263596236067, 0.025625817275185078, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 2593; Point(2593) = {0.07988198639081623, 0.018438492919507672, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 2614; Point(2614) = {0.07839907597896349, 0.023972789919614962, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 2616; Point(2616) = {0.10662628797112485, 0.03197057105875494, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 2619; Point(2619) = {0.10912825062789262, 0.037044049437948014, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 2618; Point(2618) = {0.10534053010991219, 0.035758291576735365, 0.0, 0.001*gmsf};
point_pylc_dup = 2622; Point(2622) = {0.10405477224869955, 0.03954601209471579, 0.0, 0.003889371090557505*gmsf};
point_pylc_dup = 2624; Point(2624) = {0.07679187865244769, 0.028707440567090493, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 2645; Point(2645) = {0.0745992840306997, 0.034000832239700754, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 2647; Point(2647) = {0.10154108839293599, 0.045614581750818464, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 2650; Point(2650) = {0.10335942459819074, 0.05097122747782523, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 2649; Point(2649) = {0.09977193363205998, 0.04920207271694922, 0.0, 0.001*gmsf};
point_pylc_dup = 2653; Point(2653) = {0.09800277887118398, 0.05278956368307998, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 2655; Point(2655) = {0.07238784057960469, 0.0384851959473642, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 2676; Point(2676) = {0.06952307764984167, 0.043447110893353624, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 2678; Point(2678) = {0.09471849263983566, 0.058478114302374165, 0.0, 0.003889371090557503*gmsf};
point_pylc_dup = 2681; Point(2681) = {0.09582209015696745, 0.06402627368366276, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 2680; Point(2680) = {0.09249621170775726, 0.061803992751584345, 0.0, 0.001*gmsf};
point_pylc_dup = 2684; Point(2684) = {0.09027393077567886, 0.06512987120079453, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 2686; Point(2686) = {0.06674522648474367, 0.047604458954866355, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 2707; Point(2707) = {0.06325731213495615, 0.05214999743380636, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 2709; Point(2709) = {0.08627523721674032, 0.07034107010501991, 0.0, 0.003889371090557505*gmsf};
point_pylc_dup = 2712; Point(2712) = {0.08664521318625597, 0.0759858125953361, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 2711; Point(2711) = {0.08363785395634005, 0.07334842933493584, 0.0, 0.001*gmsf};
point_pylc_dup = 2715; Point(2715) = {0.08100047069593977, 0.07635578856485174, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 2717; Point(2717) = {0.05996058305945583, 0.05590919647120125, 0.0, 0.00031246726476474716*gmsf};

// Lines and Curves
Line_dup = 1365;Line(Line_dup) = {2348, 2349}; 
lowerLine4_dup = 1368;Line(lowerLine4_dup) = {2349, 2355}; 
lowerLine3_dup = 1369;Line(lowerLine3_dup) = {2356, 2355}; 
Line_dup = 1364;Line(Line_dup) = {2346, 2347}; 
lowerLine1_dup = 1366;Line(lowerLine1_dup) = {2347, 2351}; 
lowerLine2_dup = 1367;Line(lowerLine2_dup) = {2351, 2353}; 
Line_dup = 1370;Line(Line_dup) = {2358, 2359}; 
lowerLine4_dup = 1371;Line(lowerLine4_dup) = {2359, 2361}; 
lowerLine3_dup = 1372;Line(lowerLine3_dup) = {2362, 2361}; 
Line_dup = 1373;Line(Line_dup) = {2364, 2365}; 
lowerLine1_dup = 1374;Line(lowerLine1_dup) = {2365, 2367}; 
lowerLine2_dup = 1375;Line(lowerLine2_dup) = {2367, 2369}; 
InnerLimit = 1291;Circle(InnerLimit) = {2364, 2220, 2346}; 
MB_CurveRotor = 1353;Circle(MB_CurveRotor) = {2353, 2220, 2369}; 
MB_CurveRotor_dup = 1387;Circle(MB_CurveRotor_dup) = {2369, 2220, 2387}; 
MB_CurveRotor_dup = 1389;Circle(MB_CurveRotor_dup) = {2387, 2220, 2390}; 
MB_CurveRotor_dup = 1391;Circle(MB_CurveRotor_dup) = {2390, 2220, 2393}; 
MB_CurveRotor_dup = 1393;Circle(MB_CurveRotor_dup) = {2393, 2220, 2396}; 
MB_CurveRotor_dup = 1395;Circle(MB_CurveRotor_dup) = {2396, 2220, 2399}; 
MB_CurveRotor_dup = 1397;Circle(MB_CurveRotor_dup) = {2399, 2220, 2402}; 
MB_CurveRotor_dup = 1399;Circle(MB_CurveRotor_dup) = {2402, 2220, 2353}; 
rotorBand1_dup = 1641;Circle(rotorBand1_dup) = {2351, 2220, 2367}; 
Line_dup = 1450;Line(Line_dup) = {2496, 2497}; 
Line_dup = 1451;Line(Line_dup) = {2497, 2499}; 
Line_dup = 1452;Line(Line_dup) = {2499, 2501}; 
Line_dup = 1453;Line(Line_dup) = {2501, 2503}; 
Line_dup = 1454;Line(Line_dup) = {2503, 2505}; 
Line_dup = 1455;Line(Line_dup) = {2505, 2496}; 
Line_dup = 1460;Line(Line_dup) = {2516, 2517}; 
Line_dup = 1461;Line(Line_dup) = {2517, 2519}; 
Line_dup = 1462;Line(Line_dup) = {2519, 2521}; 
Line_dup = 1463;Line(Line_dup) = {2521, 2503}; 
Line_dup = 1464;Line(Line_dup) = {2503, 2525}; 
Line_dup = 1465;Line(Line_dup) = {2525, 2516}; 
Line_dup = 1444;Line(Line_dup) = {2485, 2486}; 
Line_dup = 1445;Line(Line_dup) = {2486, 2496}; 
Line_dup = 1447;Line(Line_dup) = {2505, 2492}; 
CircleArc_dup = 1449;Circle(CircleArc_dup) = {2492, 2220, 2485}; 
Line_dup = 1456;Line(Line_dup) = {2501, 2509}; 
Line_dup = 1457;Line(Line_dup) = {2509, 2521}; 
Line_dup = 1466;Line(Line_dup) = {2528, 2529}; 
Line_dup = 1467;Line(Line_dup) = {2529, 2516}; 
Line_dup = 1469;Line(Line_dup) = {2525, 2535}; 
CircleArc_dup = 1471;Circle(CircleArc_dup) = {2535, 2220, 2528}; 
CircleArc_dup = 1635;Circle(CircleArc_dup) = {2347, 2220, 2365}; 
OuterLimit = 1322;Circle(OuterLimit) = {2277, 2220, 2348}; 
OuterLimit_dup = 1401;Circle(OuterLimit_dup) = {2406, 2220, 2277}; 
OuterLimit_dup = 1403;Circle(OuterLimit_dup) = {2409, 2220, 2406}; 
OuterLimit_dup = 1405;Circle(OuterLimit_dup) = {2412, 2220, 2409}; 
OuterLimit_dup = 1407;Circle(OuterLimit_dup) = {2415, 2220, 2412}; 
OuterLimit_dup = 1409;Circle(OuterLimit_dup) = {2358, 2220, 2415}; 
MB_CurveStator = 1361;Circle(MB_CurveStator) = {2356, 2220, 2345}; 
MB_CurveStator_dup = 1377;Circle(MB_CurveStator_dup) = {2345, 2220, 2372}; 
MB_CurveStator_dup = 1379;Circle(MB_CurveStator_dup) = {2372, 2220, 2375}; 
MB_CurveStator_dup = 1381;Circle(MB_CurveStator_dup) = {2375, 2220, 2378}; 
MB_CurveStator_dup = 1383;Circle(MB_CurveStator_dup) = {2378, 2220, 2381}; 
MB_CurveStator_dup = 1385;Circle(MB_CurveStator_dup) = {2381, 2220, 2362}; 
statorCircle4_dup = 1713;Circle(statorCircle4_dup) = {2355, 2220, 2957}; 
upperLine3_dup = 1717;Line(upperLine3_dup) = {2345, 2957}; 
statorCircle4_dup = 1719;Circle(statorCircle4_dup) = {2957, 2220, 2967}; 
upperLine3_dup = 1723;Line(upperLine3_dup) = {2372, 2967}; 
statorCircle4_dup = 1725;Circle(statorCircle4_dup) = {2967, 2220, 2977}; 
upperLine3_dup = 1729;Line(upperLine3_dup) = {2375, 2977}; 
statorCircle4_dup = 1731;Circle(statorCircle4_dup) = {2977, 2220, 2987}; 
upperLine3_dup = 1735;Line(upperLine3_dup) = {2378, 2987}; 
statorCircle4_dup = 1737;Circle(statorCircle4_dup) = {2987, 2220, 2997}; 
upperLine3_dup = 1741;Line(upperLine3_dup) = {2381, 2997}; 
statorCircle4_dup = 1743;Circle(statorCircle4_dup) = {2997, 2220, 2361}; 
CircleArc_dup = 1647;Circle(CircleArc_dup) = {2349, 2220, 2843}; 
Line_dup = 1648;Line(Line_dup) = {2843, 2845}; 
Line_dup = 1649;Line(Line_dup) = {2846, 2847}; 
CircleArc_dup = 1651;Circle(CircleArc_dup) = {2847, 2220, 2850}; 
interface_line_slot_opening___slot_dup = 1652;Line(interface_line_slot_opening___slot_dup) = {2845, 2846}; 
upperLine4_dup = 1656;Line(upperLine4_dup) = {2850, 2957}; 
CircleArc_dup = 1658;Circle(CircleArc_dup) = {2850, 2220, 2862}; 
Line_dup = 1659;Line(Line_dup) = {2862, 2864}; 
Line_dup = 1660;Line(Line_dup) = {2865, 2866}; 
CircleArc_dup = 1662;Circle(CircleArc_dup) = {2866, 2220, 2869}; 
interface_line_slot_opening___slot_dup = 1663;Line(interface_line_slot_opening___slot_dup) = {2864, 2865}; 
upperLine4_dup = 1667;Line(upperLine4_dup) = {2869, 2967}; 
CircleArc_dup = 1669;Circle(CircleArc_dup) = {2869, 2220, 2881}; 
Line_dup = 1670;Line(Line_dup) = {2881, 2883}; 
Line_dup = 1671;Line(Line_dup) = {2884, 2885}; 
CircleArc_dup = 1673;Circle(CircleArc_dup) = {2885, 2220, 2888}; 
interface_line_slot_opening___slot_dup = 1674;Line(interface_line_slot_opening___slot_dup) = {2883, 2884}; 
upperLine4_dup = 1678;Line(upperLine4_dup) = {2888, 2977}; 
CircleArc_dup = 1680;Circle(CircleArc_dup) = {2888, 2220, 2900}; 
Line_dup = 1681;Line(Line_dup) = {2900, 2902}; 
Line_dup = 1682;Line(Line_dup) = {2903, 2904}; 
CircleArc_dup = 1684;Circle(CircleArc_dup) = {2904, 2220, 2907}; 
interface_line_slot_opening___slot_dup = 1685;Line(interface_line_slot_opening___slot_dup) = {2902, 2903}; 
upperLine4_dup = 1689;Line(upperLine4_dup) = {2907, 2987}; 
CircleArc_dup = 1691;Circle(CircleArc_dup) = {2907, 2220, 2919}; 
Line_dup = 1692;Line(Line_dup) = {2919, 2921}; 
Line_dup = 1693;Line(Line_dup) = {2922, 2923}; 
CircleArc_dup = 1695;Circle(CircleArc_dup) = {2923, 2220, 2926}; 
interface_line_slot_opening___slot_dup = 1696;Line(interface_line_slot_opening___slot_dup) = {2921, 2922}; 
upperLine4_dup = 1700;Line(upperLine4_dup) = {2926, 2997}; 
CircleArc_dup = 1702;Circle(CircleArc_dup) = {2926, 2220, 2938}; 
Line_dup = 1703;Line(Line_dup) = {2938, 2940}; 
Line_dup = 1704;Line(Line_dup) = {2941, 2942}; 
CircleArc_dup = 1706;Circle(CircleArc_dup) = {2942, 2220, 2359}; 
interface_line_slot_opening___slot_dup = 1707;Line(interface_line_slot_opening___slot_dup) = {2940, 2941}; 
Line_dup = 1472;Line(Line_dup) = {2850, 2277}; 
Line_dup = 1479;Line(Line_dup) = {2845, 2552}; 
Line_dup = 1480;Line(Line_dup) = {2552, 2554}; 
CircleArc_dup = 1482;Circle(CircleArc_dup) = {2554, 2556, 2557}; 
CircleArc_dup = 1484;Circle(CircleArc_dup) = {2557, 2556, 2560}; 
Line_dup = 1485;Line(Line_dup) = {2560, 2562}; 
Line_dup = 1486;Line(Line_dup) = {2562, 2846}; 
Line_dup = 1490;Line(Line_dup) = {2869, 2406}; 
Line_dup = 1497;Line(Line_dup) = {2864, 2583}; 
Line_dup = 1498;Line(Line_dup) = {2583, 2585}; 
CircleArc_dup = 1500;Circle(CircleArc_dup) = {2585, 2587, 2588}; 
CircleArc_dup = 1502;Circle(CircleArc_dup) = {2588, 2587, 2591}; 
Line_dup = 1503;Line(Line_dup) = {2591, 2593}; 
Line_dup = 1504;Line(Line_dup) = {2593, 2865}; 
Line_dup = 1508;Line(Line_dup) = {2888, 2409}; 
Line_dup = 1515;Line(Line_dup) = {2883, 2614}; 
Line_dup = 1516;Line(Line_dup) = {2614, 2616}; 
CircleArc_dup = 1518;Circle(CircleArc_dup) = {2616, 2618, 2619}; 
CircleArc_dup = 1520;Circle(CircleArc_dup) = {2619, 2618, 2622}; 
Line_dup = 1521;Line(Line_dup) = {2622, 2624}; 
Line_dup = 1522;Line(Line_dup) = {2624, 2884}; 
Line_dup = 1526;Line(Line_dup) = {2907, 2412}; 
Line_dup = 1533;Line(Line_dup) = {2902, 2645}; 
Line_dup = 1534;Line(Line_dup) = {2645, 2647}; 
CircleArc_dup = 1536;Circle(CircleArc_dup) = {2647, 2649, 2650}; 
CircleArc_dup = 1538;Circle(CircleArc_dup) = {2650, 2649, 2653}; 
Line_dup = 1539;Line(Line_dup) = {2653, 2655}; 
Line_dup = 1540;Line(Line_dup) = {2655, 2903}; 
Line_dup = 1544;Line(Line_dup) = {2926, 2415}; 
Line_dup = 1551;Line(Line_dup) = {2921, 2676}; 
Line_dup = 1552;Line(Line_dup) = {2676, 2678}; 
CircleArc_dup = 1554;Circle(CircleArc_dup) = {2678, 2680, 2681}; 
CircleArc_dup = 1556;Circle(CircleArc_dup) = {2681, 2680, 2684}; 
Line_dup = 1557;Line(Line_dup) = {2684, 2686}; 
Line_dup = 1558;Line(Line_dup) = {2686, 2922}; 
Line_dup = 1569;Line(Line_dup) = {2940, 2707}; 
Line_dup = 1570;Line(Line_dup) = {2707, 2709}; 
CircleArc_dup = 1572;Circle(CircleArc_dup) = {2709, 2711, 2712}; 
CircleArc_dup = 1574;Circle(CircleArc_dup) = {2712, 2711, 2715}; 
Line_dup = 1575;Line(Line_dup) = {2715, 2717}; 
Line_dup = 1576;Line(Line_dup) = {2717, 2941}; 

// Surfaces

Curve Loop(170) = {1641,1375,-1353,-1367};
Surf_rotorAirGap2_dup = {170};
Plane Surface(Surf_rotorAirGap2_dup) = {170};

Curve Loop(153) = {1450,1451,1452,1453,1454,1455};
Surf_Magnet_dup = {153};
Plane Surface(Surf_Magnet_dup) = {153};

Curve Loop(155) = {1460,1461,1462,1463,1464,1465};
Surf_Magnet_dup = {155};
Plane Surface(Surf_Magnet_dup) = {155};

Curve Loop(152) = {1444,1445,-1455,1447,1449};
Surf_Loch_dup = {152};
Plane Surface(Surf_Loch_dup) = {152};

Curve Loop(154) = {1456,1457,1463,-1453};
Surf_Loch_dup = {154};
Plane Surface(Surf_Loch_dup) = {154};

Curve Loop(156) = {1466,1467,-1465,1469,1471};
Surf_Loch_dup = {156};
Plane Surface(Surf_Loch_dup) = {156};

Curve Loop(169) = {1635,1374,-1641,-1366};
Surf_rotorAirGap1_dup = {169};
Plane Surface(Surf_rotorAirGap1_dup) = {169};

Curve Loop(147) = {1444,1445,-1455,1447,1449};
Surf_Loch_dup = {147};
Plane Surface(Surf_Loch_dup) = {147};
Curve Loop(148) = {1450,1451,1452,1453,1454,1455};
Surf_Magnet_dup = {148};
Plane Surface(Surf_Magnet_dup) = {148};
Curve Loop(149) = {1456,1457,1463,-1453};
Surf_Loch_dup = {149};
Plane Surface(Surf_Loch_dup) = {149};
Curve Loop(150) = {1460,1461,1462,1463,1464,1465};
Surf_Magnet_dup = {150};
Plane Surface(Surf_Magnet_dup) = {150};
Curve Loop(151) = {1466,1467,-1465,1469,1471};
Surf_Loch_dup = {151};
Plane Surface(Surf_Loch_dup) = {151};
Curve Loop(146) = {1364,1635,-1373,1291};
Surf_Rotorblech_dup = {146};
Plane Surface(Surf_Rotorblech_dup) = {146, 147, 148, 149, 150, 151};

Curve Loop(177) = {1713,-1717,-1361,1369};
Surf_statorAirGap2_dup = {177};
Plane Surface(Surf_statorAirGap2_dup) = {177};

Curve Loop(178) = {1719,-1723,-1377,1717};
Surf_statorAirGap2_dup = {178};
Plane Surface(Surf_statorAirGap2_dup) = {178};

Curve Loop(179) = {1725,-1729,-1379,1723};
Surf_statorAirGap2_dup = {179};
Plane Surface(Surf_statorAirGap2_dup) = {179};

Curve Loop(180) = {1731,-1735,-1381,1729};
Surf_statorAirGap2_dup = {180};
Plane Surface(Surf_statorAirGap2_dup) = {180};

Curve Loop(181) = {1737,-1741,-1383,1735};
Surf_statorAirGap2_dup = {181};
Plane Surface(Surf_statorAirGap2_dup) = {181};

Curve Loop(182) = {1743,-1372,-1385,1741};
Surf_statorAirGap2_dup = {182};
Plane Surface(Surf_statorAirGap2_dup) = {182};

Curve Loop(171) = {1647,1648,1652,1649,1651,1656,-1713,-1368};
Surf_statorAirGap1_dup = {171};
Plane Surface(Surf_statorAirGap1_dup) = {171};

Curve Loop(172) = {1658,1659,1663,1660,1662,1667,-1719,-1656};
Surf_statorAirGap1_dup = {172};
Plane Surface(Surf_statorAirGap1_dup) = {172};

Curve Loop(173) = {1669,1670,1674,1671,1673,1678,-1725,-1667};
Surf_statorAirGap1_dup = {173};
Plane Surface(Surf_statorAirGap1_dup) = {173};

Curve Loop(174) = {1680,1681,1685,1682,1684,1689,-1731,-1678};
Surf_statorAirGap1_dup = {174};
Plane Surface(Surf_statorAirGap1_dup) = {174};

Curve Loop(175) = {1691,1692,1696,1693,1695,1700,-1737,-1689};
Surf_statorAirGap1_dup = {175};
Plane Surface(Surf_statorAirGap1_dup) = {175};

Curve Loop(176) = {1702,1703,1707,1704,1706,1371,-1743,-1700};
Surf_statorAirGap1_dup = {176};
Plane Surface(Surf_statorAirGap1_dup) = {176};

Curve Loop(157) = {1472,1322,1365,1647,1648,1479,1480,1482,1484,1485,1486,1649,1651};
Surf_Statorblech_dup = {157};
Plane Surface(Surf_Statorblech_dup) = {157};

Curve Loop(158) = {1490,1401,-1472,1658,1659,1497,1498,1500,1502,1503,1504,1660,1662};
Surf_Statorblech_dup = {158};
Plane Surface(Surf_Statorblech_dup) = {158};

Curve Loop(159) = {1508,1403,-1490,1669,1670,1515,1516,1518,1520,1521,1522,1671,1673};
Surf_Statorblech_dup = {159};
Plane Surface(Surf_Statorblech_dup) = {159};

Curve Loop(160) = {1526,1405,-1508,1680,1681,1533,1534,1536,1538,1539,1540,1682,1684};
Surf_Statorblech_dup = {160};
Plane Surface(Surf_Statorblech_dup) = {160};

Curve Loop(161) = {1544,1407,-1526,1691,1692,1551,1552,1554,1556,1557,1558,1693,1695};
Surf_Statorblech_dup = {161};
Plane Surface(Surf_Statorblech_dup) = {161};

Curve Loop(162) = {1370,-1706,-1704,-1576,-1575,-1574,-1572,-1570,-1569,-1703,-1702,1544,-1409};
Surf_Statorblech_dup = {162};
Plane Surface(Surf_Statorblech_dup) = {162};

Curve Loop(163) = {1479,1480,1482,1484,1485,1486,-1652};
Surf_Stator_Nut_dup = {163};
Plane Surface(Surf_Stator_Nut_dup) = {163};

Curve Loop(164) = {1497,1498,1500,1502,1503,1504,-1663};
Surf_Stator_Nut_dup = {164};
Plane Surface(Surf_Stator_Nut_dup) = {164};

Curve Loop(165) = {1515,1516,1518,1520,1521,1522,-1674};
Surf_Stator_Nut_dup = {165};
Plane Surface(Surf_Stator_Nut_dup) = {165};

Curve Loop(166) = {1533,1534,1536,1538,1539,1540,-1685};
Surf_Stator_Nut_dup = {166};
Plane Surface(Surf_Stator_Nut_dup) = {166};

Curve Loop(167) = {1551,1552,1554,1556,1557,1558,-1696};
Surf_Stator_Nut_dup = {167};
Plane Surface(Surf_Stator_Nut_dup) = {167};

Curve Loop(168) = {1569,1570,1572,1574,1575,1576,-1707};
Surf_Stator_Nut_dup = {168};
Plane Surface(Surf_Stator_Nut_dup) = {168};

// Color code
If (!Flag_individualColoring)
Color SkyBlue {Surface {170}; }
Color Red {Surface {153}; }
Color Red {Surface {155}; }
Color Aquamarine2 {Surface {152}; }
Color WhiteSmoke {Surface {154}; }
Color DarkGray {Surface {156}; }
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
Physical Curve("primaryLineS", 3) = {1365,1368,1369};
// primaryLineR
Physical Curve("primaryLineR", 2) = {1364,1366,1367};
// slaveLineS
Physical Curve("slaveLineS", 5) = {1370,1371,1372};
// slaveLineR
Physical Curve("slaveLineR", 4) = {1373,1374,1375};
// innerLimit
Physical Curve("innerLimit", 16) = {1291};
// Rotor_Bnd_MB_1
Physical Curve("Rotor_Bnd_MB_1", 7) = {1353};
// Rotor_Bnd_MB_2
Physical Curve("Rotor_Bnd_MB_2", 8) = {1387};
// Rotor_Bnd_MB_3
Physical Curve("Rotor_Bnd_MB_3", 9) = {1389};
// Rotor_Bnd_MB_4
Physical Curve("Rotor_Bnd_MB_4", 10) = {1391};
// Rotor_Bnd_MB_5
Physical Curve("Rotor_Bnd_MB_5", 11) = {1393};
// Rotor_Bnd_MB_6
Physical Curve("Rotor_Bnd_MB_6", 12) = {1395};
// Rotor_Bnd_MB_7
Physical Curve("Rotor_Bnd_MB_7", 13) = {1397};
// Rotor_Bnd_MB_8
Physical Curve("Rotor_Bnd_MB_8", 14) = {1399};
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
Physical Curve("outerLimit", 15) = {1322,1401,1403,1405,1407,1409};
// mbStator
Physical Curve("mbStator", 6) = {1361,1377,1379,1381,1383,1385};
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
primaryLines = {1364,1366,1367,1365,1368,1369};
secondaryLines = {1373,1374,1375,1370,1371,1372};
Periodic Curve{secondaryLines[]} = {primaryLines[]} Rotate {{0,0,1}, {0,0,0}, 2*Pi/8};

// Add mesh size setting for Movingband lines
DefineConstant[
	NbrMbSegments = {3370.0, Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],Max 1440, Min 180, Step 10, Help "Set the number of mesh segments on the interface between rotor/statorairgap and movingband. Value represents number of segments on whole circle.", Visible Flag_ExpertMode},
	r_MB_R = 0.08049999999999999
];
MB_LinesR = {1353,1387,1389,1391,1393,1395,1397,1399};
MeshSize{ PointsOf{Line{MB_LinesR[]};}} = 2*Pi*r_MB_R/NbrMbSegments;

MB_LinesS = {1361,1377,1379,1381,1383,1385};
MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*0.08065/NbrMbSegments;

Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)

// Create boundary lines for moving rotor contour plot
rotorBndLines[] = Boundary{ Physical Surface{ 19,21 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 17 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 31 }; };
statorBndLines[] = Boundary{ Physical Surface{ 3,5,6,15,23,24,25,26,27,28,29,32,33 }; };
Physical Line("DomainPlotMovingGeo",1) = {rotorBndLines[], statorBndLines[]}; 
