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
point_pylc_dup = 4516; Point(4516) = {0.13462, 0.0, 0, 0.006730999999999999*gmsf};
point_pylc_dup = 4517; Point(4517) = {0.08095, 0.0, 0, 0.00018658143413008237*gmsf};
PointM41_dup = 4523; Point(4523) = {0.0808, 0, 0, 0.00016829071706504786*gmsf};
PointM31_dup = 4524; Point(4524) = {0.08065, 0, 0, 0.00015000000000001124*gmsf};
point_pylc_dup = 4514; Point(4514) = {0.05532, 0.0, 0, 0.005871021118012428*gmsf};
point_pylc_dup = 4515; Point(4515) = {0.0802, 0.0, 0, 0.00021816149068324008*gmsf};
PointM11_dup = 4519; Point(4519) = {0.08034999999999999, 0, 0, 0.00018408074534162567*gmsf};
PointM21_dup = 4521; Point(4521) = {0.08049999999999999, 0, 0, 0.00015000000000001124*gmsf};
point_pylc_dup = 4526; Point(4526) = {0.09519071488333303, 0.09519071488333303, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 4527; Point(4527) = {0.057240293937051025, 0.057240293937051025, 0.0, 0.00018658143413008237*gmsf};
PointM41_dup = 4529; Point(4529) = {0.05713422791987304, 0.05713422791987304, 0.0, 0.00016829071706504786*gmsf};
PointM31_dup = 4530; Point(4530) = {0.05702816190269506, 0.05702816190269506, 0.0, 0.00015000000000001124*gmsf};
point_pylc_dup = 4532; Point(4532) = {0.03911714713523981, 0.03911714713523981, 0.0, 0.005871021118012428*gmsf};
point_pylc_dup = 4533; Point(4533) = {0.05670996385116111, 0.05670996385116111, 0.0, 0.00021816149068324008*gmsf};
PointM11_dup = 4535; Point(4535) = {0.05681602986833909, 0.05681602986833909, 0.0, 0.00018408074534162567*gmsf};
PointM21_dup = 4537; Point(4537) = {0.05692209588551707, 0.05692209588551707, 0.0, 0.00015000000000001124*gmsf};
point_pylc = 4402; Point(4402) = {0, 0, 0, 0.001*gmsf};
PointM22_dup = 4555; Point(4555) = {0.0, 0.08049999999999999, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 4558; Point(4558) = {-0.05692209588551706, 0.056922095885517075, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 4561; Point(4561) = {-0.08049999999999999, 0.0, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 4564; Point(4564) = {-0.056922095885517075, -0.05692209588551706, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 4567; Point(4567) = {-6.938893903907228e-18, -0.08049999999999999, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 4570; Point(4570) = {0.056922095885517054, -0.05692209588551708, 0.0, 0.00015000000000001124*gmsf};
point_pylc_dup = 4648; Point(4648) = {0.06976122233612055, 0.009211657048165817, 0, 0.001*gmsf};
point_pylc_dup = 4649; Point(4649) = {0.05759575268186625, 0.02108605589995692, 0, 0.001*gmsf};
point_pylc_dup = 4651; Point(4651) = {0.06213596400755108, 0.02573755900305415, 0, 0.001*gmsf};
point_pylc_dup = 4653; Point(4653) = {0.07430143366180537, 0.013863160151263048, 0, 0.001*gmsf};
point_pylc_dup = 4662; Point(4662) = {0.05584225854245618, 0.04281500821301038, 0, 0.001*gmsf};
point_pylc_dup = 4663; Point(4663) = {0.055636440404229055, 0.025816254173552766, 0, 0.001*gmsf};
point_pylc_dup = 4667; Point(4667) = {0.062341782145778214, 0.04273631304251177, 0, 0.001*gmsf};
point_pylc_dup = 4639; Point(4639) = {0.07867689952069529, 0.0019066939477583589, 0, 0.0005589689440993865*gmsf};
point_pylc_dup = 4640; Point(4640) = {0.0704597163862259, 0.009927272910180775, 0, 0.001*gmsf};
point_pylc_dup = 4644; Point(4644) = {0.07803354822364487, 0.01022034009356294, 0, 0.0005589689440993865*gmsf};
point_pylc_dup = 4656; Point(4656) = {0.05829424673197161, 0.02180167176197188, 0, 0.001*gmsf};
point_pylc_dup = 4657; Point(4657) = {0.05663636711243244, 0.025804147224245285, 0, 0.001*gmsf};
point_pylc_dup = 4670; Point(4670) = {0.05698120539392355, 0.054284732953708975, 0, 0.0005589689440993886*gmsf};
point_pylc_dup = 4671; Point(4671) = {0.05684218525065958, 0.04280290126370291, 0, 0.001*gmsf};
point_pylc_dup = 4675; Point(4675) = {0.062404922895177864, 0.04795117932279565, 0, 0.0005589689440993865*gmsf};
point_pylc = 4445; Point(4445) = {0.13346830723814235, 0.017571435996663342, 0, 0.006730999999999999*gmsf};
point_pylc_dup = 4574; Point(4574) = {0.13003293473503436, 0.034842219851701335, 0.0, 0.006730999999999997*gmsf};
point_pylc_dup = 4577; Point(4577) = {0.12437266266666941, 0.051516843664988377, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 4580; Point(4580) = {0.11658433985746111, 0.06731, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 4583; Point(4583) = {0.10680122667000608, 0.08195146357315396, 0.0, 0.006730999999999999*gmsf};
PointM32 = 4513; Point(4513) = {0.07996002806979781, 0.010526937402547159, 0, 0.00015000000000001124*gmsf};
PointM32_dup = 4540; Point(4540) = {0.07790191789021336, 0.020873755987518297, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 4543; Point(4543) = {0.07451088429703527, 0.030863418820244487, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 4546; Point(4546) = {0.06984494881521497, 0.040325, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 4549; Point(4549) = {0.06398394689448812, 0.04909660924955331, 0.0, 0.00015000000000001124*gmsf};
PointM42_dup = 5097; Point(5097) = {0.08010874479900387, 0.010546516331380167, 0, 0.00016829071706504786*gmsf};
PointM42_dup = 5107; Point(5107) = {0.0780468067641567, 0.020912578844283672, 0.0, 0.00016829071706504786*gmsf};
PointM42_dup = 5117; Point(5117) = {0.07464946622691196, 0.030920821335099248, 0.0, 0.00016829071706504574*gmsf};
PointM42_dup = 5127; Point(5127) = {0.06997485262578262, 0.04039999999999999, 0.0, 0.00016829071706504574*gmsf};
PointM42_dup = 5137; Point(5137) = {0.06410294989553181, 0.04918792346390462, 0.0, 0.00016829071706504786*gmsf};
point_pylc_dup = 4983; Point(4983) = {0.08083405411411097, 0.004331073247704142, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 4985; Point(4985) = {0.08183191303734956, 0.004396476376934286, 0, 0.00030851098907667415*gmsf};
point_pylc_dup = 4986; Point(4986) = {0.08170568499793539, 0.00632234409878479, 0, 0.00030851098907667415*gmsf};
point_pylc_dup = 4987; Point(4987) = {0.08070782607469679, 0.0062569409695546465, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 4990; Point(4990) = {0.08025746152820995, 0.010566095260213175, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 5002; Point(5002) = {0.07957718907619889, 0.014844981600894352, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 5004; Point(5004) = {0.0805579743566021, 0.015040071922910478, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 5005; Point(5005) = {0.08018145003511097, 0.016932987514088713, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 5006; Point(5006) = {0.07920066475470774, 0.01673789719207258, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 5009; Point(5009) = {0.07819169563810008, 0.020951401701049054, 0.0, 0.0001865814341300845*gmsf};
point_pylc_dup = 5021; Point(5021) = {0.07695873627022805, 0.02510488820308679, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 5023; Point(5023) = {0.07790566639972313, 0.02542632766838995, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 5024; Point(5024) = {0.07728528823168804, 0.027253902818315502, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 5025; Point(5025) = {0.07633835810219293, 0.026932463353012342, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 5028; Point(5028) = {0.07478804815678866, 0.030978223849954016, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 5040; Point(5040) = {0.07302349814968086, 0.03493524320773444, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 5042; Point(5042) = {0.07392037089121353, 0.03537753189795343, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 5043; Point(5043) = {0.07306675371909087, 0.03710849628911152, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 5044; Point(5044) = {0.07216988097755818, 0.036666207598892525, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 5047; Point(5047) = {0.07010475643635031, 0.040475, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 5059; Point(5059) = {0.06783880772985405, 0.04416784651521844, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 5061; Point(5061) = {0.0686702773421566, 0.044723416748238036, 0.0, 0.00030851098907667626*gmsf};
point_pylc_dup = 5062; Point(5062) = {0.06759802679242875, 0.04632815309998195, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 5063; Point(5063) = {0.06676655718012621, 0.04577258286696235, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 5066; Point(5066) = {0.0642219528965755, 0.04927923767825593, 0.0, 0.0001865814341300845*gmsf};
point_pylc_dup = 5078; Point(5078) = {0.0614933765012986, 0.05264472572318653, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 5080; Point(5080) = {0.06224521630877756, 0.05330407153828659, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 5081; Point(5081) = {0.06097267888563443, 0.05475512236672102, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 5082; Point(5082) = {0.06022083907815545, 0.054095776551620955, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 4692; Point(4692) = {0.08193230684071783, 0.002864762929763029, 0, 0.00031246726476474504*gmsf};
point_pylc_dup = 4694; Point(4694) = {0.11126767798545414, 0.0032842862313483155, 0, 0.003889371090557505*gmsf};
point_pylc_dup = 4697; Point(4697) = {0.11499750116148799, 0.007537334441223301, 0, 0.0043683573413105655*gmsf};
point_pylc_dup = 4696; Point(4696) = {0.11100606546853357, 0.0072757219243027305, 0, 0.001*gmsf};
point_pylc_dup = 4700; Point(4700) = {0.110744452951613, 0.011267157617257145, 0, 0.003889371090557505*gmsf};
point_pylc_dup = 4702; Point(4702) = {0.08160529119456712, 0.007854057545956047, 0, 0.00031246726476474716*gmsf};
point_pylc_dup = 4723; Point(4723) = {0.08085743800089684, 0.013534566517491518, 0.0, 0.0003124672647647429*gmsf};
point_pylc_dup = 4725; Point(4725) = {0.10988708219973571, 0.017779535031959233, 0.0, 0.003889371090557503*gmsf};
point_pylc_dup = 4728; Point(4728) = {0.11302986203328413, 0.022483037441636666, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 4727; Point(4727) = {0.10910672091167122, 0.021702676153572156, 0.0, 0.001*gmsf};
point_pylc_dup = 4731; Point(4731) = {0.1083263596236067, 0.025625817275185078, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 4733; Point(4733) = {0.07988198639081623, 0.018438492919507672, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 4754; Point(4754) = {0.07839907597896349, 0.023972789919614962, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 4756; Point(4756) = {0.10662628797112485, 0.03197057105875494, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 4759; Point(4759) = {0.10912825062789262, 0.037044049437948014, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 4758; Point(4758) = {0.10534053010991219, 0.035758291576735365, 0.0, 0.001*gmsf};
point_pylc_dup = 4762; Point(4762) = {0.10405477224869955, 0.03954601209471579, 0.0, 0.003889371090557505*gmsf};
point_pylc_dup = 4764; Point(4764) = {0.07679187865244769, 0.028707440567090493, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 4785; Point(4785) = {0.0745992840306997, 0.034000832239700754, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 4787; Point(4787) = {0.10154108839293599, 0.045614581750818464, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 4790; Point(4790) = {0.10335942459819074, 0.05097122747782523, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 4789; Point(4789) = {0.09977193363205998, 0.04920207271694922, 0.0, 0.001*gmsf};
point_pylc_dup = 4793; Point(4793) = {0.09800277887118398, 0.05278956368307998, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 4795; Point(4795) = {0.07238784057960469, 0.0384851959473642, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 4816; Point(4816) = {0.06952307764984167, 0.043447110893353624, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 4818; Point(4818) = {0.09471849263983566, 0.058478114302374165, 0.0, 0.003889371090557503*gmsf};
point_pylc_dup = 4821; Point(4821) = {0.09582209015696745, 0.06402627368366276, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 4820; Point(4820) = {0.09249621170775726, 0.061803992751584345, 0.0, 0.001*gmsf};
point_pylc_dup = 4824; Point(4824) = {0.09027393077567886, 0.06512987120079453, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 4826; Point(4826) = {0.06674522648474367, 0.047604458954866355, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 4847; Point(4847) = {0.06325731213495615, 0.05214999743380636, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 4849; Point(4849) = {0.08627523721674032, 0.07034107010501991, 0.0, 0.003889371090557505*gmsf};
point_pylc_dup = 4852; Point(4852) = {0.08664521318625597, 0.0759858125953361, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 4851; Point(4851) = {0.08363785395634005, 0.07334842933493584, 0.0, 0.001*gmsf};
point_pylc_dup = 4855; Point(4855) = {0.08100047069593977, 0.07635578856485174, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 4857; Point(4857) = {0.05996058305945583, 0.05590919647120125, 0.0, 0.00031246726476474716*gmsf};

// Lines and Curves
Line_dup = 2618;Line(Line_dup) = {4516, 4517};
lowerLine4_dup = 2621;Line(lowerLine4_dup) = {4517, 4523};
lowerLine3_dup = 2622;Line(lowerLine3_dup) = {4524, 4523};
Line_dup = 2617;Line(Line_dup) = {4514, 4515};
lowerLine1_dup = 2619;Line(lowerLine1_dup) = {4515, 4519};
lowerLine2_dup = 2620;Line(lowerLine2_dup) = {4519, 4521};
Line_dup = 2623;Line(Line_dup) = {4526, 4527};
lowerLine4_dup = 2624;Line(lowerLine4_dup) = {4527, 4529};
lowerLine3_dup = 2625;Line(lowerLine3_dup) = {4530, 4529};
Line_dup = 2626;Line(Line_dup) = {4532, 4533};
lowerLine1_dup = 2627;Line(lowerLine1_dup) = {4533, 4535};
lowerLine2_dup = 2628;Line(lowerLine2_dup) = {4535, 4537};
InnerLimit = 2551;Circle(InnerLimit) = {4532, 4402, 4514};
MB_CurveRotor = 2606;Circle(MB_CurveRotor) = {4521, 4402, 4537};
MB_CurveRotor_dup = 2640;Circle(MB_CurveRotor_dup) = {4537, 4402, 4555};
MB_CurveRotor_dup = 2642;Circle(MB_CurveRotor_dup) = {4555, 4402, 4558};
MB_CurveRotor_dup = 2644;Circle(MB_CurveRotor_dup) = {4558, 4402, 4561};
MB_CurveRotor_dup = 2646;Circle(MB_CurveRotor_dup) = {4561, 4402, 4564};
MB_CurveRotor_dup = 2648;Circle(MB_CurveRotor_dup) = {4564, 4402, 4567};
MB_CurveRotor_dup = 2650;Circle(MB_CurveRotor_dup) = {4567, 4402, 4570};
MB_CurveRotor_dup = 2652;Circle(MB_CurveRotor_dup) = {4570, 4402, 4521};
rotorBand1_dup = 2880;Circle(rotorBand1_dup) = {4519, 4402, 4535};
Line_dup = 2695;Line(Line_dup) = {4648, 4649};
Line_dup = 2696;Line(Line_dup) = {4649, 4651};
Line_dup = 2697;Line(Line_dup) = {4651, 4653};
Line_dup = 2698;Line(Line_dup) = {4653, 4648};
Line_dup = 2702;Line(Line_dup) = {4662, 4663};
Line_dup = 2703;Line(Line_dup) = {4663, 4651};
Line_dup = 2704;Line(Line_dup) = {4651, 4667};
Line_dup = 2705;Line(Line_dup) = {4667, 4662};
Line_dup = 2690;Line(Line_dup) = {4639, 4640};
Line_dup = 2691;Line(Line_dup) = {4640, 4653};
Line_dup = 2692;Line(Line_dup) = {4653, 4644};
CircleArc_dup = 2694;Circle(CircleArc_dup) = {4644, 4402, 4639};
Line_dup = 2699;Line(Line_dup) = {4656, 4657};
Line_dup = 2700;Line(Line_dup) = {4657, 4651};
Line_dup = 2701;Line(Line_dup) = {4651, 4656};
Line_dup = 2706;Line(Line_dup) = {4670, 4671};
Line_dup = 2707;Line(Line_dup) = {4671, 4667};
Line_dup = 2708;Line(Line_dup) = {4667, 4675};
CircleArc_dup = 2710;Circle(CircleArc_dup) = {4675, 4402, 4670};
CircleArc_dup = 2874;Circle(CircleArc_dup) = {4515, 4402, 4533};
OuterLimit = 2575;Circle(OuterLimit) = {4445, 4402, 4516};
OuterLimit_dup = 2654;Circle(OuterLimit_dup) = {4574, 4402, 4445};
OuterLimit_dup = 2656;Circle(OuterLimit_dup) = {4577, 4402, 4574};
OuterLimit_dup = 2658;Circle(OuterLimit_dup) = {4580, 4402, 4577};
OuterLimit_dup = 2660;Circle(OuterLimit_dup) = {4583, 4402, 4580};
OuterLimit_dup = 2662;Circle(OuterLimit_dup) = {4526, 4402, 4583};
MB_CurveStator = 2614;Circle(MB_CurveStator) = {4524, 4402, 4513};
MB_CurveStator_dup = 2630;Circle(MB_CurveStator_dup) = {4513, 4402, 4540};
MB_CurveStator_dup = 2632;Circle(MB_CurveStator_dup) = {4540, 4402, 4543};
MB_CurveStator_dup = 2634;Circle(MB_CurveStator_dup) = {4543, 4402, 4546};
MB_CurveStator_dup = 2636;Circle(MB_CurveStator_dup) = {4546, 4402, 4549};
MB_CurveStator_dup = 2638;Circle(MB_CurveStator_dup) = {4549, 4402, 4530};
statorCircle4_dup = 2952;Circle(statorCircle4_dup) = {4523, 4402, 5097};
upperLine3_dup = 2956;Line(upperLine3_dup) = {4513, 5097};
statorCircle4_dup = 2958;Circle(statorCircle4_dup) = {5097, 4402, 5107};
upperLine3_dup = 2962;Line(upperLine3_dup) = {4540, 5107};
statorCircle4_dup = 2964;Circle(statorCircle4_dup) = {5107, 4402, 5117};
upperLine3_dup = 2968;Line(upperLine3_dup) = {4543, 5117};
statorCircle4_dup = 2970;Circle(statorCircle4_dup) = {5117, 4402, 5127};
upperLine3_dup = 2974;Line(upperLine3_dup) = {4546, 5127};
statorCircle4_dup = 2976;Circle(statorCircle4_dup) = {5127, 4402, 5137};
upperLine3_dup = 2980;Line(upperLine3_dup) = {4549, 5137};
statorCircle4_dup = 2982;Circle(statorCircle4_dup) = {5137, 4402, 4529};
CircleArc_dup = 2886;Circle(CircleArc_dup) = {4517, 4402, 4983};
Line_dup = 2887;Line(Line_dup) = {4983, 4985};
Line_dup = 2888;Line(Line_dup) = {4986, 4987};
CircleArc_dup = 2890;Circle(CircleArc_dup) = {4987, 4402, 4990};
interface_line_slot_opening___slot_dup = 2891;Line(interface_line_slot_opening___slot_dup) = {4985, 4986};
upperLine4_dup = 2895;Line(upperLine4_dup) = {4990, 5097};
CircleArc_dup = 2897;Circle(CircleArc_dup) = {4990, 4402, 5002};
Line_dup = 2898;Line(Line_dup) = {5002, 5004};
Line_dup = 2899;Line(Line_dup) = {5005, 5006};
CircleArc_dup = 2901;Circle(CircleArc_dup) = {5006, 4402, 5009};
interface_line_slot_opening___slot_dup = 2902;Line(interface_line_slot_opening___slot_dup) = {5004, 5005};
upperLine4_dup = 2906;Line(upperLine4_dup) = {5009, 5107};
CircleArc_dup = 2908;Circle(CircleArc_dup) = {5009, 4402, 5021};
Line_dup = 2909;Line(Line_dup) = {5021, 5023};
Line_dup = 2910;Line(Line_dup) = {5024, 5025};
CircleArc_dup = 2912;Circle(CircleArc_dup) = {5025, 4402, 5028};
interface_line_slot_opening___slot_dup = 2913;Line(interface_line_slot_opening___slot_dup) = {5023, 5024};
upperLine4_dup = 2917;Line(upperLine4_dup) = {5028, 5117};
CircleArc_dup = 2919;Circle(CircleArc_dup) = {5028, 4402, 5040};
Line_dup = 2920;Line(Line_dup) = {5040, 5042};
Line_dup = 2921;Line(Line_dup) = {5043, 5044};
CircleArc_dup = 2923;Circle(CircleArc_dup) = {5044, 4402, 5047};
interface_line_slot_opening___slot_dup = 2924;Line(interface_line_slot_opening___slot_dup) = {5042, 5043};
upperLine4_dup = 2928;Line(upperLine4_dup) = {5047, 5127};
CircleArc_dup = 2930;Circle(CircleArc_dup) = {5047, 4402, 5059};
Line_dup = 2931;Line(Line_dup) = {5059, 5061};
Line_dup = 2932;Line(Line_dup) = {5062, 5063};
CircleArc_dup = 2934;Circle(CircleArc_dup) = {5063, 4402, 5066};
interface_line_slot_opening___slot_dup = 2935;Line(interface_line_slot_opening___slot_dup) = {5061, 5062};
upperLine4_dup = 2939;Line(upperLine4_dup) = {5066, 5137};
CircleArc_dup = 2941;Circle(CircleArc_dup) = {5066, 4402, 5078};
Line_dup = 2942;Line(Line_dup) = {5078, 5080};
Line_dup = 2943;Line(Line_dup) = {5081, 5082};
CircleArc_dup = 2945;Circle(CircleArc_dup) = {5082, 4402, 4527};
interface_line_slot_opening___slot_dup = 2946;Line(interface_line_slot_opening___slot_dup) = {5080, 5081};
Line_dup = 2711;Line(Line_dup) = {4990, 4445};
Line_dup = 2718;Line(Line_dup) = {4985, 4692};
Line_dup = 2719;Line(Line_dup) = {4692, 4694};
CircleArc_dup = 2721;Circle(CircleArc_dup) = {4694, 4696, 4697};
CircleArc_dup = 2723;Circle(CircleArc_dup) = {4697, 4696, 4700};
Line_dup = 2724;Line(Line_dup) = {4700, 4702};
Line_dup = 2725;Line(Line_dup) = {4702, 4986};
Line_dup = 2729;Line(Line_dup) = {5009, 4574};
Line_dup = 2736;Line(Line_dup) = {5004, 4723};
Line_dup = 2737;Line(Line_dup) = {4723, 4725};
CircleArc_dup = 2739;Circle(CircleArc_dup) = {4725, 4727, 4728};
CircleArc_dup = 2741;Circle(CircleArc_dup) = {4728, 4727, 4731};
Line_dup = 2742;Line(Line_dup) = {4731, 4733};
Line_dup = 2743;Line(Line_dup) = {4733, 5005};
Line_dup = 2747;Line(Line_dup) = {5028, 4577};
Line_dup = 2754;Line(Line_dup) = {5023, 4754};
Line_dup = 2755;Line(Line_dup) = {4754, 4756};
CircleArc_dup = 2757;Circle(CircleArc_dup) = {4756, 4758, 4759};
CircleArc_dup = 2759;Circle(CircleArc_dup) = {4759, 4758, 4762};
Line_dup = 2760;Line(Line_dup) = {4762, 4764};
Line_dup = 2761;Line(Line_dup) = {4764, 5024};
Line_dup = 2765;Line(Line_dup) = {5047, 4580};
Line_dup = 2772;Line(Line_dup) = {5042, 4785};
Line_dup = 2773;Line(Line_dup) = {4785, 4787};
CircleArc_dup = 2775;Circle(CircleArc_dup) = {4787, 4789, 4790};
CircleArc_dup = 2777;Circle(CircleArc_dup) = {4790, 4789, 4793};
Line_dup = 2778;Line(Line_dup) = {4793, 4795};
Line_dup = 2779;Line(Line_dup) = {4795, 5043};
Line_dup = 2783;Line(Line_dup) = {5066, 4583};
Line_dup = 2790;Line(Line_dup) = {5061, 4816};
Line_dup = 2791;Line(Line_dup) = {4816, 4818};
CircleArc_dup = 2793;Circle(CircleArc_dup) = {4818, 4820, 4821};
CircleArc_dup = 2795;Circle(CircleArc_dup) = {4821, 4820, 4824};
Line_dup = 2796;Line(Line_dup) = {4824, 4826};
Line_dup = 2797;Line(Line_dup) = {4826, 5062};
Line_dup = 2808;Line(Line_dup) = {5080, 4847};
Line_dup = 2809;Line(Line_dup) = {4847, 4849};
CircleArc_dup = 2811;Circle(CircleArc_dup) = {4849, 4851, 4852};
CircleArc_dup = 2813;Circle(CircleArc_dup) = {4852, 4851, 4855};
Line_dup = 2814;Line(Line_dup) = {4855, 4857};
Line_dup = 2815;Line(Line_dup) = {4857, 5081};

// Surfaces

Curve Loop(275) = {2880,2628,-2606,-2620};
Surf_rotorAirGap2_dup = {275};
Plane Surface(Surf_rotorAirGap2_dup) = {275};

Curve Loop(258) = {2695,2696,2697,2698};
Surf_Magnet_dup = {258};
Plane Surface(Surf_Magnet_dup) = {258};

Curve Loop(260) = {2702,2703,2704,2705};
Surf_Magnet_dup = {260};
Plane Surface(Surf_Magnet_dup) = {260};

Curve Loop(257) = {2690,2691,2692,2694};
Surf_Loch_dup = {257};
Plane Surface(Surf_Loch_dup) = {257};

Curve Loop(259) = {2699,2700,2701};
Surf_Loch_dup = {259};
Plane Surface(Surf_Loch_dup) = {259};

Curve Loop(261) = {2706,2707,2708,2710};
Surf_Loch_dup = {261};
Plane Surface(Surf_Loch_dup) = {261};

Curve Loop(274) = {2874,2627,-2880,-2619};
Surf_rotorAirGap1_dup = {274};
Plane Surface(Surf_rotorAirGap1_dup) = {274};

Curve Loop(252) = {2690,2691,2692,2694};
Surf_Loch_dup = {252};
Plane Surface(Surf_Loch_dup) = {252};
Curve Loop(253) = {2695,2696,2697,2698};
Surf_Magnet_dup = {253};
Plane Surface(Surf_Magnet_dup) = {253};
Curve Loop(254) = {2699,2700,2701};
Surf_Loch_dup = {254};
Plane Surface(Surf_Loch_dup) = {254};
Curve Loop(255) = {2702,2703,2704,2705};
Surf_Magnet_dup = {255};
Plane Surface(Surf_Magnet_dup) = {255};
Curve Loop(256) = {2706,2707,2708,2710};
Surf_Loch_dup = {256};
Plane Surface(Surf_Loch_dup) = {256};
Curve Loop(251) = {2617,2874,-2626,2551};
Surf_Rotorblech_dup = {251};
Plane Surface(Surf_Rotorblech_dup) = {251, 252, 253, 254, 255, 256};

Curve Loop(282) = {2952,-2956,-2614,2622};
Surf_statorAirGap2_dup = {282};
Plane Surface(Surf_statorAirGap2_dup) = {282};

Curve Loop(283) = {2958,-2962,-2630,2956};
Surf_statorAirGap2_dup = {283};
Plane Surface(Surf_statorAirGap2_dup) = {283};

Curve Loop(284) = {2964,-2968,-2632,2962};
Surf_statorAirGap2_dup = {284};
Plane Surface(Surf_statorAirGap2_dup) = {284};

Curve Loop(285) = {2970,-2974,-2634,2968};
Surf_statorAirGap2_dup = {285};
Plane Surface(Surf_statorAirGap2_dup) = {285};

Curve Loop(286) = {2976,-2980,-2636,2974};
Surf_statorAirGap2_dup = {286};
Plane Surface(Surf_statorAirGap2_dup) = {286};

Curve Loop(287) = {2982,-2625,-2638,2980};
Surf_statorAirGap2_dup = {287};
Plane Surface(Surf_statorAirGap2_dup) = {287};

Curve Loop(276) = {2886,2887,2891,2888,2890,2895,-2952,-2621};
Surf_statorAirGap1_dup = {276};
Plane Surface(Surf_statorAirGap1_dup) = {276};

Curve Loop(277) = {2897,2898,2902,2899,2901,2906,-2958,-2895};
Surf_statorAirGap1_dup = {277};
Plane Surface(Surf_statorAirGap1_dup) = {277};

Curve Loop(278) = {2908,2909,2913,2910,2912,2917,-2964,-2906};
Surf_statorAirGap1_dup = {278};
Plane Surface(Surf_statorAirGap1_dup) = {278};

Curve Loop(279) = {2919,2920,2924,2921,2923,2928,-2970,-2917};
Surf_statorAirGap1_dup = {279};
Plane Surface(Surf_statorAirGap1_dup) = {279};

Curve Loop(280) = {2930,2931,2935,2932,2934,2939,-2976,-2928};
Surf_statorAirGap1_dup = {280};
Plane Surface(Surf_statorAirGap1_dup) = {280};

Curve Loop(281) = {2941,2942,2946,2943,2945,2624,-2982,-2939};
Surf_statorAirGap1_dup = {281};
Plane Surface(Surf_statorAirGap1_dup) = {281};

Curve Loop(262) = {2711,2575,2618,2886,2887,2718,2719,2721,2723,2724,2725,2888,2890};
Surf_Statorblech_dup = {262};
Plane Surface(Surf_Statorblech_dup) = {262};

Curve Loop(263) = {2729,2654,-2711,2897,2898,2736,2737,2739,2741,2742,2743,2899,2901};
Surf_Statorblech_dup = {263};
Plane Surface(Surf_Statorblech_dup) = {263};

Curve Loop(264) = {2747,2656,-2729,2908,2909,2754,2755,2757,2759,2760,2761,2910,2912};
Surf_Statorblech_dup = {264};
Plane Surface(Surf_Statorblech_dup) = {264};

Curve Loop(265) = {2765,2658,-2747,2919,2920,2772,2773,2775,2777,2778,2779,2921,2923};
Surf_Statorblech_dup = {265};
Plane Surface(Surf_Statorblech_dup) = {265};

Curve Loop(266) = {2783,2660,-2765,2930,2931,2790,2791,2793,2795,2796,2797,2932,2934};
Surf_Statorblech_dup = {266};
Plane Surface(Surf_Statorblech_dup) = {266};

Curve Loop(267) = {2623,-2945,-2943,-2815,-2814,-2813,-2811,-2809,-2808,-2942,-2941,2783,-2662};
Surf_Statorblech_dup = {267};
Plane Surface(Surf_Statorblech_dup) = {267};

Curve Loop(268) = {2718,2719,2721,2723,2724,2725,-2891};
Surf_Stator_Nut_dup = {268};
Plane Surface(Surf_Stator_Nut_dup) = {268};

Curve Loop(269) = {2736,2737,2739,2741,2742,2743,-2902};
Surf_Stator_Nut_dup = {269};
Plane Surface(Surf_Stator_Nut_dup) = {269};

Curve Loop(270) = {2754,2755,2757,2759,2760,2761,-2913};
Surf_Stator_Nut_dup = {270};
Plane Surface(Surf_Stator_Nut_dup) = {270};

Curve Loop(271) = {2772,2773,2775,2777,2778,2779,-2924};
Surf_Stator_Nut_dup = {271};
Plane Surface(Surf_Stator_Nut_dup) = {271};

Curve Loop(272) = {2790,2791,2793,2795,2796,2797,-2935};
Surf_Stator_Nut_dup = {272};
Plane Surface(Surf_Stator_Nut_dup) = {272};

Curve Loop(273) = {2808,2809,2811,2813,2814,2815,-2946};
Surf_Stator_Nut_dup = {273};
Plane Surface(Surf_Stator_Nut_dup) = {273};

// Color code
If (!Flag_individualColoring)
Color SkyBlue {Surface {275}; }
Color Red {Surface {258}; }
Color Red {Surface {260}; }
Color PaleVioletRed2 {Surface {257}; }
Color Coral2 {Surface {259}; }
Color Grey74 {Surface {261}; }
Color SkyBlue {Surface {274}; }
Color SteelBlue {Surface {251}; }
Color SkyBlue {Surface {282}; }
Color SkyBlue {Surface {283}; }
Color SkyBlue {Surface {284}; }
Color SkyBlue {Surface {285}; }
Color SkyBlue {Surface {286}; }
Color SkyBlue {Surface {287}; }
Color SkyBlue {Surface {276}; }
Color SkyBlue {Surface {277}; }
Color SkyBlue {Surface {278}; }
Color SkyBlue {Surface {279}; }
Color SkyBlue {Surface {280}; }
Color SkyBlue {Surface {281}; }
Color SteelBlue4 {Surface {262}; }
Color SteelBlue4 {Surface {263}; }
Color SteelBlue4 {Surface {264}; }
Color SteelBlue4 {Surface {265}; }
Color SteelBlue4 {Surface {266}; }
Color SteelBlue4 {Surface {267}; }
Color Magenta {Surface {268}; }
Color Magenta {Surface {269}; }
Color Cyan {Surface {270}; }
Color Cyan {Surface {271}; }
Color Yellow4 {Surface {272}; }
Color Yellow4 {Surface {273}; }
EndIf

// Physical Elements
// primaryLineS
Physical Curve("primaryLineS", 3) = {2618,2621,2622};
// primaryLineR
Physical Curve("primaryLineR", 2) = {2617,2619,2620};
// slaveLineS
Physical Curve("slaveLineS", 5) = {2623,2624,2625};
// slaveLineR
Physical Curve("slaveLineR", 4) = {2626,2627,2628};
// innerLimit
Physical Curve("innerLimit", 16) = {2551};
// Rotor_Bnd_MB_1
Physical Curve("Rotor_Bnd_MB_1", 7) = {2606};
// Rotor_Bnd_MB_2
Physical Curve("Rotor_Bnd_MB_2", 8) = {2640};
// Rotor_Bnd_MB_3
Physical Curve("Rotor_Bnd_MB_3", 9) = {2642};
// Rotor_Bnd_MB_4
Physical Curve("Rotor_Bnd_MB_4", 10) = {2644};
// Rotor_Bnd_MB_5
Physical Curve("Rotor_Bnd_MB_5", 11) = {2646};
// Rotor_Bnd_MB_6
Physical Curve("Rotor_Bnd_MB_6", 12) = {2648};
// Rotor_Bnd_MB_7
Physical Curve("Rotor_Bnd_MB_7", 13) = {2650};
// Rotor_Bnd_MB_8
Physical Curve("Rotor_Bnd_MB_8", 14) = {2652};
// LuR2
Physical Surface("LuR2", 31) = {275};
// Mag0_0
Physical Surface("Mag0_0", 19) = {258};
// Mag1_0
Physical Surface("Mag1_0", 21) = {260};
// Lpl0
Physical Surface("Lpl0", 18) = {257};
// Lpl1
Physical Surface("Lpl1", 20) = {259};
// Lpl2
Physical Surface("Lpl2", 22) = {261};
// LuR1
Physical Surface("LuR1", 30) = {274};
// Pol
Physical Surface("Pol", 17) = {251};
// outerLimit
Physical Curve("outerLimit", 15) = {2575,2654,2656,2658,2660,2662};
// mbStator
Physical Curve("mbStator", 6) = {2614,2630,2632,2634,2636,2638};
// StLu2
Physical Surface("StLu2", 33) = {282,283,284,285,286,287};
// StLu1
Physical Surface("StLu1", 32) = {276,277,278,279,280,281};
// StNut
Physical Surface("StNut", 23) = {262,263,264,265,266,267};
// StCu0_0_Up
Physical Surface("StCu0_0_Up", 24) = {268};
// StCu0_1_Up
Physical Surface("StCu0_1_Up", 25) = {269};
// StCu0_2_Wn
Physical Surface("StCu0_2_Wn", 26) = {270};
// StCu0_3_Wn
Physical Surface("StCu0_3_Wn", 27) = {271};
// StCu0_4_Vp
Physical Surface("StCu0_4_Vp", 28) = {272};
// StCu0_5_Vp
Physical Surface("StCu0_5_Vp", 29) = {273};

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
	MeshSize { PointsOf {Surface{ 257,259,261 };} } = Lpl_msf*mm;
	MeshSize { PointsOf {Surface{ 258,260 };} } = Mag_msf*mm;
	MeshSize { PointsOf {Surface{ 251 };} } = Pol_msf*mm;
	MeshSize { PointsOf {Surface{ 274,275 };} } = LuR_msf*mm;
	MeshSize { PointsOf {Surface{ 274 };} } = LuR1_msf*mm;
	MeshSize { PointsOf {Surface{ 275 };} } = LuR2_msf*mm;
	MeshSize { PointsOf {Surface{ 268,269,270,271,272,273 };} } = StCu_msf*mm;
	MeshSize { PointsOf {Surface{ 262,263,264,265,266,267 };} } = StNut_msf*mm;
	MeshSize { PointsOf {Surface{ 276,277,278,279,280,281,282,283,284,285,286,287 };} } = StLu_msf*mm;
	MeshSize { PointsOf {Surface{ 276,277,278,279,280,281 };} } = StLu1_msf*mm;
	MeshSize { PointsOf {Surface{ 282,283,284,285,286,287 };} } = StLu2_msf*mm;
EndIf

// Mesh operations

// Do not switch mesh algorithm on failure, because this led to mesh errors in the past.
Mesh.AlgorithmSwitchOnFailure = 0;DefineConstant[Flag_CompoundMesh = {0, Name StrCat[INPUT_MESH, "Compound Mesh"], Choices {0,1}, Help "Use Compound Mesh to ignore lines between segments while meshing.",Visible Flag_ExpertMode}];
If (Flag_CompoundMesh)
Compound Surface{262,263,264,265,266,267}; // stator domainLam
Compound Surface{282,283,284,285,286,287}; // stator airGap
EndIf // (Flag_CompoundMesh)

// Add Periodic Mesh to model symmetry boundary-lines
primaryLines = {2617,2619,2620,2618,2621,2622};
secondaryLines = {2626,2627,2628,2623,2624,2625};
Periodic Curve{secondaryLines[]} = {primaryLines[]} Rotate {{0,0,1}, {0,0,0}, 2*Pi/8};

// Add mesh size setting for Movingband lines
DefineConstant[
	NbrMbSegments = {3370.0, Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],Max 1440, Min 180, Step 10, Help "Set the number of mesh segments on the interface between rotor/statorairgap and movingband. Value represents number of segments on whole circle.", Visible Flag_ExpertMode},
	r_MB_R = 0.08049999999999999
];
MB_LinesR = {2606,2640,2642,2644,2646,2648,2650,2652};
MeshSize{ PointsOf{Line{MB_LinesR[]};}} = 2*Pi*r_MB_R/NbrMbSegments;

MB_LinesS = {2614,2630,2632,2634,2636,2638};
MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*0.08065/NbrMbSegments;

Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)

// Create boundary lines for moving rotor contour plot
rotorBndLines[] = Boundary{ Physical Surface{ 19,21 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 17 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 31 }; };
statorBndLines[] = Boundary{ Physical Surface{ 3,5,6,15,23,24,25,26,27,28,29,32,33 }; };
Physical Line("DomainPlotMovingGeo",1) = {rotorBndLines[], statorBndLines[]};
