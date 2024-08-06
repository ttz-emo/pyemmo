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
point_pylc_dup = 6739; Point(6739) = {0.13462, 0.0, 0, 0.006730999999999999*gmsf};
point_pylc_dup = 6740; Point(6740) = {0.08095, 0.0, 0, 0.00018658143413008237*gmsf};
PointM41_dup = 6746; Point(6746) = {0.0808, 0, 0, 0.00016829071706504786*gmsf};
PointM31_dup = 6747; Point(6747) = {0.08065, 0, 0, 0.00015000000000001124*gmsf};
point_pylc_dup = 6737; Point(6737) = {0.05532, 0.0, 0, 0.005871021118012428*gmsf};
point_pylc_dup = 6738; Point(6738) = {0.0802, 0.0, 0, 0.00021816149068324008*gmsf};
PointM11_dup = 6742; Point(6742) = {0.08034999999999999, 0, 0, 0.00018408074534162567*gmsf};
PointM21_dup = 6744; Point(6744) = {0.08049999999999999, 0, 0, 0.00015000000000001124*gmsf};
point_pylc_dup = 6749; Point(6749) = {0.09519071488333303, 0.09519071488333303, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 6750; Point(6750) = {0.057240293937051025, 0.057240293937051025, 0.0, 0.00018658143413008237*gmsf};
PointM41_dup = 6752; Point(6752) = {0.05713422791987304, 0.05713422791987304, 0.0, 0.00016829071706504786*gmsf};
PointM31_dup = 6753; Point(6753) = {0.05702816190269506, 0.05702816190269506, 0.0, 0.00015000000000001124*gmsf};
point_pylc_dup = 6755; Point(6755) = {0.03911714713523981, 0.03911714713523981, 0.0, 0.005871021118012428*gmsf};
point_pylc_dup = 6756; Point(6756) = {0.05670996385116111, 0.05670996385116111, 0.0, 0.00021816149068324008*gmsf};
PointM11_dup = 6758; Point(6758) = {0.05681602986833909, 0.05681602986833909, 0.0, 0.00018408074534162567*gmsf};
PointM21_dup = 6760; Point(6760) = {0.05692209588551707, 0.05692209588551707, 0.0, 0.00015000000000001124*gmsf};
point_pylc = 6611; Point(6611) = {0, 0, 0, 0.001*gmsf};
PointM22_dup = 6778; Point(6778) = {0.0, 0.08049999999999999, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 6781; Point(6781) = {-0.05692209588551706, 0.056922095885517075, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 6784; Point(6784) = {-0.08049999999999999, 0.0, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 6787; Point(6787) = {-0.056922095885517075, -0.05692209588551706, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 6790; Point(6790) = {-6.938893903907228e-18, -0.08049999999999999, 0.0, 0.00015000000000001124*gmsf};
PointM22_dup = 6793; Point(6793) = {0.056922095885517054, -0.05692209588551708, 0.0, 0.00015000000000001124*gmsf};
point_pylc_dup = 6887; Point(6887) = {0.07189332074897073, 0.008478350008583092, 0, 0.001*gmsf};
point_pylc_dup = 6888; Point(6888) = {0.07112686475225904, 0.007836053188487666, 0, 0.001*gmsf};
point_pylc_dup = 6890; Point(6890) = {0.058987454852455525, 0.02232207152633855, 0, 0.001*gmsf};
point_pylc_dup = 6892; Point(6892) = {0.059753910849167216, 0.02296436834643398, 0, 0.001*gmsf};
point_pylc_dup = 6894; Point(6894) = {0.0639694188310815, 0.026497000856958816, 0, 0.001*gmsf};
point_pylc_dup = 6896; Point(6896) = {0.07610882873088501, 0.01201098251910793, 0, 0.000933687570242861*gmsf};
point_pylc_dup = 6907; Point(6907) = {0.056831353407958855, 0.0448411558392746, 0, 0.001*gmsf};
point_pylc_dup = 6908; Point(6908) = {0.055835214738178894, 0.0447533620435427, 0, 0.001*gmsf};
point_pylc_dup = 6910; Point(6910) = {0.057494517477511754, 0.02592634118470148, 0, 0.001*gmsf};
point_pylc_dup = 6912; Point(6912) = {0.05849065614729172, 0.026014134980433378, 0, 0.001*gmsf};
point_pylc_dup = 6916; Point(6916) = {0.06231011609174863, 0.045324021715800036, 0, 0.000933687570242861*gmsf};
point_pylc_dup = 6876; Point(6876) = {0.07838807307237497, 0.007000000000000003, 0, 0.0005589689440993886*gmsf};
point_pylc_dup = 6877; Point(6877) = {0.07313219096927659, 0.007000000000000003, 0, 0.001*gmsf};
point_pylc_dup = 6883; Point(6883) = {0.07810937152746876, 0.009623724828976162, 0, 0.0005589689440993886*gmsf};
point_pylc_dup = 6900; Point(6900) = {0.05864256321587955, 0.024290545016338896, 0, 0.001*gmsf};
point_pylc_dup = 6919; Point(6919) = {0.06037848550192878, 0.050478990565317114, 0, 0.0005589689440993886*gmsf};
point_pylc_dup = 6920; Point(6920) = {0.05666201562571091, 0.04676252068909924, 0, 0.001*gmsf};
point_pylc_dup = 6926; Point(6926) = {0.06203666736813499, 0.048426665194450214, 0, 0.0005589689440993865*gmsf};
point_pylc = 6668; Point(6668) = {0.13346830723814235, 0.017571435996663342, 0, 0.006730999999999999*gmsf};
point_pylc_dup = 6797; Point(6797) = {0.13003293473503436, 0.034842219851701335, 0.0, 0.006730999999999997*gmsf};
point_pylc_dup = 6800; Point(6800) = {0.12437266266666941, 0.051516843664988377, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 6803; Point(6803) = {0.11658433985746111, 0.06731, 0.0, 0.006730999999999999*gmsf};
point_pylc_dup = 6806; Point(6806) = {0.10680122667000608, 0.08195146357315396, 0.0, 0.006730999999999999*gmsf};
PointM32 = 6736; Point(6736) = {0.07996002806979781, 0.010526937402547159, 0, 0.00015000000000001124*gmsf};
PointM32_dup = 6763; Point(6763) = {0.07790191789021336, 0.020873755987518297, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 6766; Point(6766) = {0.07451088429703527, 0.030863418820244487, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 6769; Point(6769) = {0.06984494881521497, 0.040325, 0.0, 0.00015000000000001124*gmsf};
PointM32_dup = 6772; Point(6772) = {0.06398394689448812, 0.04909660924955331, 0.0, 0.00015000000000001124*gmsf};
PointM42_dup = 7348; Point(7348) = {0.08010874479900387, 0.010546516331380167, 0, 0.00016829071706504786*gmsf};
PointM42_dup = 7358; Point(7358) = {0.0780468067641567, 0.020912578844283672, 0.0, 0.00016829071706504786*gmsf};
PointM42_dup = 7368; Point(7368) = {0.07464946622691196, 0.030920821335099248, 0.0, 0.00016829071706504574*gmsf};
PointM42_dup = 7378; Point(7378) = {0.06997485262578262, 0.04039999999999999, 0.0, 0.00016829071706504574*gmsf};
PointM42_dup = 7388; Point(7388) = {0.06410294989553181, 0.04918792346390462, 0.0, 0.00016829071706504786*gmsf};
point_pylc_dup = 7234; Point(7234) = {0.08083405411411097, 0.004331073247704142, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 7236; Point(7236) = {0.08183191303734956, 0.004396476376934286, 0, 0.00030851098907667415*gmsf};
point_pylc_dup = 7237; Point(7237) = {0.08170568499793539, 0.00632234409878479, 0, 0.00030851098907667415*gmsf};
point_pylc_dup = 7238; Point(7238) = {0.08070782607469679, 0.0062569409695546465, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 7241; Point(7241) = {0.08025746152820995, 0.010566095260213175, 0, 0.00018658143413008237*gmsf};
point_pylc_dup = 7253; Point(7253) = {0.07957718907619889, 0.014844981600894352, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 7255; Point(7255) = {0.0805579743566021, 0.015040071922910478, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 7256; Point(7256) = {0.08018145003511097, 0.016932987514088713, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 7257; Point(7257) = {0.07920066475470774, 0.01673789719207258, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 7260; Point(7260) = {0.07819169563810008, 0.020951401701049054, 0.0, 0.0001865814341300845*gmsf};
point_pylc_dup = 7272; Point(7272) = {0.07695873627022805, 0.02510488820308679, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 7274; Point(7274) = {0.07790566639972313, 0.02542632766838995, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 7275; Point(7275) = {0.07728528823168804, 0.027253902818315502, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 7276; Point(7276) = {0.07633835810219293, 0.026932463353012342, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 7279; Point(7279) = {0.07478804815678866, 0.030978223849954016, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 7291; Point(7291) = {0.07302349814968086, 0.03493524320773444, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 7293; Point(7293) = {0.07392037089121353, 0.03537753189795343, 0.0, 0.00030851098907667203*gmsf};
point_pylc_dup = 7294; Point(7294) = {0.07306675371909087, 0.03710849628911152, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 7295; Point(7295) = {0.07216988097755818, 0.036666207598892525, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 7298; Point(7298) = {0.07010475643635031, 0.040475, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 7310; Point(7310) = {0.06783880772985405, 0.04416784651521844, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 7312; Point(7312) = {0.0686702773421566, 0.044723416748238036, 0.0, 0.00030851098907667626*gmsf};
point_pylc_dup = 7313; Point(7313) = {0.06759802679242875, 0.04632815309998195, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 7314; Point(7314) = {0.06676655718012621, 0.04577258286696235, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 7317; Point(7317) = {0.0642219528965755, 0.04927923767825593, 0.0, 0.0001865814341300845*gmsf};
point_pylc_dup = 7329; Point(7329) = {0.0614933765012986, 0.05264472572318653, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 7331; Point(7331) = {0.06224521630877756, 0.05330407153828659, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 7332; Point(7332) = {0.06097267888563443, 0.05475512236672102, 0.0, 0.00030851098907667415*gmsf};
point_pylc_dup = 7333; Point(7333) = {0.06022083907815545, 0.054095776551620955, 0.0, 0.00018658143413008237*gmsf};
point_pylc_dup = 6943; Point(6943) = {0.08193230684071783, 0.002864762929763029, 0, 0.00031246726476474504*gmsf};
point_pylc_dup = 6945; Point(6945) = {0.11126767798545414, 0.0032842862313483155, 0, 0.003889371090557505*gmsf};
point_pylc_dup = 6948; Point(6948) = {0.11499750116148799, 0.007537334441223301, 0, 0.0043683573413105655*gmsf};
point_pylc_dup = 6947; Point(6947) = {0.11100606546853357, 0.0072757219243027305, 0, 0.001*gmsf};
point_pylc_dup = 6951; Point(6951) = {0.110744452951613, 0.011267157617257145, 0, 0.003889371090557505*gmsf};
point_pylc_dup = 6953; Point(6953) = {0.08160529119456712, 0.007854057545956047, 0, 0.00031246726476474716*gmsf};
point_pylc_dup = 6974; Point(6974) = {0.08085743800089684, 0.013534566517491518, 0.0, 0.0003124672647647429*gmsf};
point_pylc_dup = 6976; Point(6976) = {0.10988708219973571, 0.017779535031959233, 0.0, 0.003889371090557503*gmsf};
point_pylc_dup = 6979; Point(6979) = {0.11302986203328413, 0.022483037441636666, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 6978; Point(6978) = {0.10910672091167122, 0.021702676153572156, 0.0, 0.001*gmsf};
point_pylc_dup = 6982; Point(6982) = {0.1083263596236067, 0.025625817275185078, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 6984; Point(6984) = {0.07988198639081623, 0.018438492919507672, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 7005; Point(7005) = {0.07839907597896349, 0.023972789919614962, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 7007; Point(7007) = {0.10662628797112485, 0.03197057105875494, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 7010; Point(7010) = {0.10912825062789262, 0.037044049437948014, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 7009; Point(7009) = {0.10534053010991219, 0.035758291576735365, 0.0, 0.001*gmsf};
point_pylc_dup = 7013; Point(7013) = {0.10405477224869955, 0.03954601209471579, 0.0, 0.003889371090557505*gmsf};
point_pylc_dup = 7015; Point(7015) = {0.07679187865244769, 0.028707440567090493, 0.0, 0.00031246726476474716*gmsf};
point_pylc_dup = 7036; Point(7036) = {0.0745992840306997, 0.034000832239700754, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 7038; Point(7038) = {0.10154108839293599, 0.045614581750818464, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 7041; Point(7041) = {0.10335942459819074, 0.05097122747782523, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 7040; Point(7040) = {0.09977193363205998, 0.04920207271694922, 0.0, 0.001*gmsf};
point_pylc_dup = 7044; Point(7044) = {0.09800277887118398, 0.05278956368307998, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 7046; Point(7046) = {0.07238784057960469, 0.0384851959473642, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 7067; Point(7067) = {0.06952307764984167, 0.043447110893353624, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 7069; Point(7069) = {0.09471849263983566, 0.058478114302374165, 0.0, 0.003889371090557503*gmsf};
point_pylc_dup = 7072; Point(7072) = {0.09582209015696745, 0.06402627368366276, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 7071; Point(7071) = {0.09249621170775726, 0.061803992751584345, 0.0, 0.001*gmsf};
point_pylc_dup = 7075; Point(7075) = {0.09027393077567886, 0.06512987120079453, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 7077; Point(7077) = {0.06674522648474367, 0.047604458954866355, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 7098; Point(7098) = {0.06325731213495615, 0.05214999743380636, 0.0, 0.00031246726476474504*gmsf};
point_pylc_dup = 7100; Point(7100) = {0.08627523721674032, 0.07034107010501991, 0.0, 0.003889371090557505*gmsf};
point_pylc_dup = 7103; Point(7103) = {0.08664521318625597, 0.0759858125953361, 0.0, 0.0043683573413105655*gmsf};
point_pylc_dup = 7102; Point(7102) = {0.08363785395634005, 0.07334842933493584, 0.0, 0.001*gmsf};
point_pylc_dup = 7106; Point(7106) = {0.08100047069593977, 0.07635578856485174, 0.0, 0.0038893710905575068*gmsf};
point_pylc_dup = 7108; Point(7108) = {0.05996058305945583, 0.05590919647120125, 0.0, 0.00031246726476474716*gmsf};

// Lines and Curves
Line_dup = 3910;Line(Line_dup) = {6739, 6740};
lowerLine4_dup = 3913;Line(lowerLine4_dup) = {6740, 6746};
lowerLine3_dup = 3914;Line(lowerLine3_dup) = {6747, 6746};
Line_dup = 3909;Line(Line_dup) = {6737, 6738};
lowerLine1_dup = 3911;Line(lowerLine1_dup) = {6738, 6742};
lowerLine2_dup = 3912;Line(lowerLine2_dup) = {6742, 6744};
Line_dup = 3915;Line(Line_dup) = {6749, 6750};
lowerLine4_dup = 3916;Line(lowerLine4_dup) = {6750, 6752};
lowerLine3_dup = 3917;Line(lowerLine3_dup) = {6753, 6752};
Line_dup = 3918;Line(Line_dup) = {6755, 6756};
lowerLine1_dup = 3919;Line(lowerLine1_dup) = {6756, 6758};
lowerLine2_dup = 3920;Line(lowerLine2_dup) = {6758, 6760};
InnerLimit = 3836;Circle(InnerLimit) = {6755, 6611, 6737};
MB_CurveRotor = 3898;Circle(MB_CurveRotor) = {6744, 6611, 6760};
MB_CurveRotor_dup = 3932;Circle(MB_CurveRotor_dup) = {6760, 6611, 6778};
MB_CurveRotor_dup = 3934;Circle(MB_CurveRotor_dup) = {6778, 6611, 6781};
MB_CurveRotor_dup = 3936;Circle(MB_CurveRotor_dup) = {6781, 6611, 6784};
MB_CurveRotor_dup = 3938;Circle(MB_CurveRotor_dup) = {6784, 6611, 6787};
MB_CurveRotor_dup = 3940;Circle(MB_CurveRotor_dup) = {6787, 6611, 6790};
MB_CurveRotor_dup = 3942;Circle(MB_CurveRotor_dup) = {6790, 6611, 6793};
MB_CurveRotor_dup = 3944;Circle(MB_CurveRotor_dup) = {6793, 6611, 6744};
rotorBand1_dup = 4186;Circle(rotorBand1_dup) = {6742, 6611, 6758};
Line_dup = 3995;Line(Line_dup) = {6887, 6888};
Line_dup = 3996;Line(Line_dup) = {6888, 6890};
Line_dup = 3997;Line(Line_dup) = {6890, 6892};
Line_dup = 3998;Line(Line_dup) = {6892, 6894};
Line_dup = 3999;Line(Line_dup) = {6894, 6896};
Line_dup = 4000;Line(Line_dup) = {6896, 6887};
Line_dup = 4005;Line(Line_dup) = {6907, 6908};
Line_dup = 4006;Line(Line_dup) = {6908, 6910};
Line_dup = 4007;Line(Line_dup) = {6910, 6912};
Line_dup = 4008;Line(Line_dup) = {6912, 6894};
Line_dup = 4009;Line(Line_dup) = {6894, 6916};
Line_dup = 4010;Line(Line_dup) = {6916, 6907};
Line_dup = 3989;Line(Line_dup) = {6876, 6877};
Line_dup = 3990;Line(Line_dup) = {6877, 6887};
Line_dup = 3992;Line(Line_dup) = {6896, 6883};
CircleArc_dup = 3994;Circle(CircleArc_dup) = {6883, 6611, 6876};
Line_dup = 4001;Line(Line_dup) = {6892, 6900};
Line_dup = 4002;Line(Line_dup) = {6900, 6912};
Line_dup = 4011;Line(Line_dup) = {6919, 6920};
Line_dup = 4012;Line(Line_dup) = {6920, 6907};
Line_dup = 4014;Line(Line_dup) = {6916, 6926};
CircleArc_dup = 4016;Circle(CircleArc_dup) = {6926, 6611, 6919};
CircleArc_dup = 4180;Circle(CircleArc_dup) = {6738, 6611, 6756};
OuterLimit = 3867;Circle(OuterLimit) = {6668, 6611, 6739};
OuterLimit_dup = 3946;Circle(OuterLimit_dup) = {6797, 6611, 6668};
OuterLimit_dup = 3948;Circle(OuterLimit_dup) = {6800, 6611, 6797};
OuterLimit_dup = 3950;Circle(OuterLimit_dup) = {6803, 6611, 6800};
OuterLimit_dup = 3952;Circle(OuterLimit_dup) = {6806, 6611, 6803};
OuterLimit_dup = 3954;Circle(OuterLimit_dup) = {6749, 6611, 6806};
MB_CurveStator = 3906;Circle(MB_CurveStator) = {6747, 6611, 6736};
MB_CurveStator_dup = 3922;Circle(MB_CurveStator_dup) = {6736, 6611, 6763};
MB_CurveStator_dup = 3924;Circle(MB_CurveStator_dup) = {6763, 6611, 6766};
MB_CurveStator_dup = 3926;Circle(MB_CurveStator_dup) = {6766, 6611, 6769};
MB_CurveStator_dup = 3928;Circle(MB_CurveStator_dup) = {6769, 6611, 6772};
MB_CurveStator_dup = 3930;Circle(MB_CurveStator_dup) = {6772, 6611, 6753};
statorCircle4_dup = 4258;Circle(statorCircle4_dup) = {6746, 6611, 7348};
upperLine3_dup = 4262;Line(upperLine3_dup) = {6736, 7348};
statorCircle4_dup = 4264;Circle(statorCircle4_dup) = {7348, 6611, 7358};
upperLine3_dup = 4268;Line(upperLine3_dup) = {6763, 7358};
statorCircle4_dup = 4270;Circle(statorCircle4_dup) = {7358, 6611, 7368};
upperLine3_dup = 4274;Line(upperLine3_dup) = {6766, 7368};
statorCircle4_dup = 4276;Circle(statorCircle4_dup) = {7368, 6611, 7378};
upperLine3_dup = 4280;Line(upperLine3_dup) = {6769, 7378};
statorCircle4_dup = 4282;Circle(statorCircle4_dup) = {7378, 6611, 7388};
upperLine3_dup = 4286;Line(upperLine3_dup) = {6772, 7388};
statorCircle4_dup = 4288;Circle(statorCircle4_dup) = {7388, 6611, 6752};
CircleArc_dup = 4192;Circle(CircleArc_dup) = {6740, 6611, 7234};
Line_dup = 4193;Line(Line_dup) = {7234, 7236};
Line_dup = 4194;Line(Line_dup) = {7237, 7238};
CircleArc_dup = 4196;Circle(CircleArc_dup) = {7238, 6611, 7241};
interface_line_slot_opening___slot_dup = 4197;Line(interface_line_slot_opening___slot_dup) = {7236, 7237};
upperLine4_dup = 4201;Line(upperLine4_dup) = {7241, 7348};
CircleArc_dup = 4203;Circle(CircleArc_dup) = {7241, 6611, 7253};
Line_dup = 4204;Line(Line_dup) = {7253, 7255};
Line_dup = 4205;Line(Line_dup) = {7256, 7257};
CircleArc_dup = 4207;Circle(CircleArc_dup) = {7257, 6611, 7260};
interface_line_slot_opening___slot_dup = 4208;Line(interface_line_slot_opening___slot_dup) = {7255, 7256};
upperLine4_dup = 4212;Line(upperLine4_dup) = {7260, 7358};
CircleArc_dup = 4214;Circle(CircleArc_dup) = {7260, 6611, 7272};
Line_dup = 4215;Line(Line_dup) = {7272, 7274};
Line_dup = 4216;Line(Line_dup) = {7275, 7276};
CircleArc_dup = 4218;Circle(CircleArc_dup) = {7276, 6611, 7279};
interface_line_slot_opening___slot_dup = 4219;Line(interface_line_slot_opening___slot_dup) = {7274, 7275};
upperLine4_dup = 4223;Line(upperLine4_dup) = {7279, 7368};
CircleArc_dup = 4225;Circle(CircleArc_dup) = {7279, 6611, 7291};
Line_dup = 4226;Line(Line_dup) = {7291, 7293};
Line_dup = 4227;Line(Line_dup) = {7294, 7295};
CircleArc_dup = 4229;Circle(CircleArc_dup) = {7295, 6611, 7298};
interface_line_slot_opening___slot_dup = 4230;Line(interface_line_slot_opening___slot_dup) = {7293, 7294};
upperLine4_dup = 4234;Line(upperLine4_dup) = {7298, 7378};
CircleArc_dup = 4236;Circle(CircleArc_dup) = {7298, 6611, 7310};
Line_dup = 4237;Line(Line_dup) = {7310, 7312};
Line_dup = 4238;Line(Line_dup) = {7313, 7314};
CircleArc_dup = 4240;Circle(CircleArc_dup) = {7314, 6611, 7317};
interface_line_slot_opening___slot_dup = 4241;Line(interface_line_slot_opening___slot_dup) = {7312, 7313};
upperLine4_dup = 4245;Line(upperLine4_dup) = {7317, 7388};
CircleArc_dup = 4247;Circle(CircleArc_dup) = {7317, 6611, 7329};
Line_dup = 4248;Line(Line_dup) = {7329, 7331};
Line_dup = 4249;Line(Line_dup) = {7332, 7333};
CircleArc_dup = 4251;Circle(CircleArc_dup) = {7333, 6611, 6750};
interface_line_slot_opening___slot_dup = 4252;Line(interface_line_slot_opening___slot_dup) = {7331, 7332};
Line_dup = 4017;Line(Line_dup) = {7241, 6668};
Line_dup = 4024;Line(Line_dup) = {7236, 6943};
Line_dup = 4025;Line(Line_dup) = {6943, 6945};
CircleArc_dup = 4027;Circle(CircleArc_dup) = {6945, 6947, 6948};
CircleArc_dup = 4029;Circle(CircleArc_dup) = {6948, 6947, 6951};
Line_dup = 4030;Line(Line_dup) = {6951, 6953};
Line_dup = 4031;Line(Line_dup) = {6953, 7237};
Line_dup = 4035;Line(Line_dup) = {7260, 6797};
Line_dup = 4042;Line(Line_dup) = {7255, 6974};
Line_dup = 4043;Line(Line_dup) = {6974, 6976};
CircleArc_dup = 4045;Circle(CircleArc_dup) = {6976, 6978, 6979};
CircleArc_dup = 4047;Circle(CircleArc_dup) = {6979, 6978, 6982};
Line_dup = 4048;Line(Line_dup) = {6982, 6984};
Line_dup = 4049;Line(Line_dup) = {6984, 7256};
Line_dup = 4053;Line(Line_dup) = {7279, 6800};
Line_dup = 4060;Line(Line_dup) = {7274, 7005};
Line_dup = 4061;Line(Line_dup) = {7005, 7007};
CircleArc_dup = 4063;Circle(CircleArc_dup) = {7007, 7009, 7010};
CircleArc_dup = 4065;Circle(CircleArc_dup) = {7010, 7009, 7013};
Line_dup = 4066;Line(Line_dup) = {7013, 7015};
Line_dup = 4067;Line(Line_dup) = {7015, 7275};
Line_dup = 4071;Line(Line_dup) = {7298, 6803};
Line_dup = 4078;Line(Line_dup) = {7293, 7036};
Line_dup = 4079;Line(Line_dup) = {7036, 7038};
CircleArc_dup = 4081;Circle(CircleArc_dup) = {7038, 7040, 7041};
CircleArc_dup = 4083;Circle(CircleArc_dup) = {7041, 7040, 7044};
Line_dup = 4084;Line(Line_dup) = {7044, 7046};
Line_dup = 4085;Line(Line_dup) = {7046, 7294};
Line_dup = 4089;Line(Line_dup) = {7317, 6806};
Line_dup = 4096;Line(Line_dup) = {7312, 7067};
Line_dup = 4097;Line(Line_dup) = {7067, 7069};
CircleArc_dup = 4099;Circle(CircleArc_dup) = {7069, 7071, 7072};
CircleArc_dup = 4101;Circle(CircleArc_dup) = {7072, 7071, 7075};
Line_dup = 4102;Line(Line_dup) = {7075, 7077};
Line_dup = 4103;Line(Line_dup) = {7077, 7313};
Line_dup = 4114;Line(Line_dup) = {7331, 7098};
Line_dup = 4115;Line(Line_dup) = {7098, 7100};
CircleArc_dup = 4117;Circle(CircleArc_dup) = {7100, 7102, 7103};
CircleArc_dup = 4119;Circle(CircleArc_dup) = {7103, 7102, 7106};
Line_dup = 4120;Line(Line_dup) = {7106, 7108};
Line_dup = 4121;Line(Line_dup) = {7108, 7332};

// Surfaces

Curve Loop(408) = {4186,3920,-3898,-3912};
Surf_rotorAirGap2_dup = {408};
Plane Surface(Surf_rotorAirGap2_dup) = {408};

Curve Loop(391) = {3995,3996,3997,3998,3999,4000};
Surf_Magnet_dup = {391};
Plane Surface(Surf_Magnet_dup) = {391};

Curve Loop(393) = {4005,4006,4007,4008,4009,4010};
Surf_Magnet_dup = {393};
Plane Surface(Surf_Magnet_dup) = {393};

Curve Loop(390) = {3989,3990,-4000,3992,3994};
Surf_Loch_dup = {390};
Plane Surface(Surf_Loch_dup) = {390};

Curve Loop(392) = {4001,4002,4008,-3998};
Surf_Loch_dup = {392};
Plane Surface(Surf_Loch_dup) = {392};

Curve Loop(394) = {4011,4012,-4010,4014,4016};
Surf_Loch_dup = {394};
Plane Surface(Surf_Loch_dup) = {394};

Curve Loop(407) = {4180,3919,-4186,-3911};
Surf_rotorAirGap1_dup = {407};
Plane Surface(Surf_rotorAirGap1_dup) = {407};

Curve Loop(385) = {3989,3990,-4000,3992,3994};
Surf_Loch_dup = {385};
Plane Surface(Surf_Loch_dup) = {385};
Curve Loop(386) = {3995,3996,3997,3998,3999,4000};
Surf_Magnet_dup = {386};
Plane Surface(Surf_Magnet_dup) = {386};
Curve Loop(387) = {4001,4002,4008,-3998};
Surf_Loch_dup = {387};
Plane Surface(Surf_Loch_dup) = {387};
Curve Loop(388) = {4005,4006,4007,4008,4009,4010};
Surf_Magnet_dup = {388};
Plane Surface(Surf_Magnet_dup) = {388};
Curve Loop(389) = {4011,4012,-4010,4014,4016};
Surf_Loch_dup = {389};
Plane Surface(Surf_Loch_dup) = {389};
Curve Loop(384) = {3909,4180,-3918,3836};
Surf_Rotorblech_dup = {384};
Plane Surface(Surf_Rotorblech_dup) = {384, 385, 386, 387, 388, 389};

Curve Loop(415) = {4258,-4262,-3906,3914};
Surf_statorAirGap2_dup = {415};
Plane Surface(Surf_statorAirGap2_dup) = {415};

Curve Loop(416) = {4264,-4268,-3922,4262};
Surf_statorAirGap2_dup = {416};
Plane Surface(Surf_statorAirGap2_dup) = {416};

Curve Loop(417) = {4270,-4274,-3924,4268};
Surf_statorAirGap2_dup = {417};
Plane Surface(Surf_statorAirGap2_dup) = {417};

Curve Loop(418) = {4276,-4280,-3926,4274};
Surf_statorAirGap2_dup = {418};
Plane Surface(Surf_statorAirGap2_dup) = {418};

Curve Loop(419) = {4282,-4286,-3928,4280};
Surf_statorAirGap2_dup = {419};
Plane Surface(Surf_statorAirGap2_dup) = {419};

Curve Loop(420) = {4288,-3917,-3930,4286};
Surf_statorAirGap2_dup = {420};
Plane Surface(Surf_statorAirGap2_dup) = {420};

Curve Loop(409) = {4192,4193,4197,4194,4196,4201,-4258,-3913};
Surf_statorAirGap1_dup = {409};
Plane Surface(Surf_statorAirGap1_dup) = {409};

Curve Loop(410) = {4203,4204,4208,4205,4207,4212,-4264,-4201};
Surf_statorAirGap1_dup = {410};
Plane Surface(Surf_statorAirGap1_dup) = {410};

Curve Loop(411) = {4214,4215,4219,4216,4218,4223,-4270,-4212};
Surf_statorAirGap1_dup = {411};
Plane Surface(Surf_statorAirGap1_dup) = {411};

Curve Loop(412) = {4225,4226,4230,4227,4229,4234,-4276,-4223};
Surf_statorAirGap1_dup = {412};
Plane Surface(Surf_statorAirGap1_dup) = {412};

Curve Loop(413) = {4236,4237,4241,4238,4240,4245,-4282,-4234};
Surf_statorAirGap1_dup = {413};
Plane Surface(Surf_statorAirGap1_dup) = {413};

Curve Loop(414) = {4247,4248,4252,4249,4251,3916,-4288,-4245};
Surf_statorAirGap1_dup = {414};
Plane Surface(Surf_statorAirGap1_dup) = {414};

Curve Loop(395) = {4017,3867,3910,4192,4193,4024,4025,4027,4029,4030,4031,4194,4196};
Surf_Statorblech_dup = {395};
Plane Surface(Surf_Statorblech_dup) = {395};

Curve Loop(396) = {4035,3946,-4017,4203,4204,4042,4043,4045,4047,4048,4049,4205,4207};
Surf_Statorblech_dup = {396};
Plane Surface(Surf_Statorblech_dup) = {396};

Curve Loop(397) = {4053,3948,-4035,4214,4215,4060,4061,4063,4065,4066,4067,4216,4218};
Surf_Statorblech_dup = {397};
Plane Surface(Surf_Statorblech_dup) = {397};

Curve Loop(398) = {4071,3950,-4053,4225,4226,4078,4079,4081,4083,4084,4085,4227,4229};
Surf_Statorblech_dup = {398};
Plane Surface(Surf_Statorblech_dup) = {398};

Curve Loop(399) = {4089,3952,-4071,4236,4237,4096,4097,4099,4101,4102,4103,4238,4240};
Surf_Statorblech_dup = {399};
Plane Surface(Surf_Statorblech_dup) = {399};

Curve Loop(400) = {3915,-4251,-4249,-4121,-4120,-4119,-4117,-4115,-4114,-4248,-4247,4089,-3954};
Surf_Statorblech_dup = {400};
Plane Surface(Surf_Statorblech_dup) = {400};

Curve Loop(401) = {4024,4025,4027,4029,4030,4031,-4197};
Surf_Stator_Nut_dup = {401};
Plane Surface(Surf_Stator_Nut_dup) = {401};

Curve Loop(402) = {4042,4043,4045,4047,4048,4049,-4208};
Surf_Stator_Nut_dup = {402};
Plane Surface(Surf_Stator_Nut_dup) = {402};

Curve Loop(403) = {4060,4061,4063,4065,4066,4067,-4219};
Surf_Stator_Nut_dup = {403};
Plane Surface(Surf_Stator_Nut_dup) = {403};

Curve Loop(404) = {4078,4079,4081,4083,4084,4085,-4230};
Surf_Stator_Nut_dup = {404};
Plane Surface(Surf_Stator_Nut_dup) = {404};

Curve Loop(405) = {4096,4097,4099,4101,4102,4103,-4241};
Surf_Stator_Nut_dup = {405};
Plane Surface(Surf_Stator_Nut_dup) = {405};

Curve Loop(406) = {4114,4115,4117,4119,4120,4121,-4252};
Surf_Stator_Nut_dup = {406};
Plane Surface(Surf_Stator_Nut_dup) = {406};

// Color code
If (!Flag_individualColoring)
Color SkyBlue {Surface {408}; }
Color Red {Surface {391}; }
Color Red {Surface {393}; }
Color Tomato3 {Surface {390}; }
Color Grey77 {Surface {392}; }
Color Orchid4 {Surface {394}; }
Color SkyBlue {Surface {407}; }
Color SteelBlue {Surface {384}; }
Color SkyBlue {Surface {415}; }
Color SkyBlue {Surface {416}; }
Color SkyBlue {Surface {417}; }
Color SkyBlue {Surface {418}; }
Color SkyBlue {Surface {419}; }
Color SkyBlue {Surface {420}; }
Color SkyBlue {Surface {409}; }
Color SkyBlue {Surface {410}; }
Color SkyBlue {Surface {411}; }
Color SkyBlue {Surface {412}; }
Color SkyBlue {Surface {413}; }
Color SkyBlue {Surface {414}; }
Color SteelBlue4 {Surface {395}; }
Color SteelBlue4 {Surface {396}; }
Color SteelBlue4 {Surface {397}; }
Color SteelBlue4 {Surface {398}; }
Color SteelBlue4 {Surface {399}; }
Color SteelBlue4 {Surface {400}; }
Color Magenta {Surface {401}; }
Color Magenta {Surface {402}; }
Color Cyan {Surface {403}; }
Color Cyan {Surface {404}; }
Color Yellow4 {Surface {405}; }
Color Yellow4 {Surface {406}; }
EndIf

// Physical Elements
// primaryLineS
Physical Curve("primaryLineS", 3) = {3910,3913,3914};
// primaryLineR
Physical Curve("primaryLineR", 2) = {3909,3911,3912};
// slaveLineS
Physical Curve("slaveLineS", 5) = {3915,3916,3917};
// slaveLineR
Physical Curve("slaveLineR", 4) = {3918,3919,3920};
// innerLimit
Physical Curve("innerLimit", 16) = {3836};
// Rotor_Bnd_MB_1
Physical Curve("Rotor_Bnd_MB_1", 7) = {3898};
// Rotor_Bnd_MB_2
Physical Curve("Rotor_Bnd_MB_2", 8) = {3932};
// Rotor_Bnd_MB_3
Physical Curve("Rotor_Bnd_MB_3", 9) = {3934};
// Rotor_Bnd_MB_4
Physical Curve("Rotor_Bnd_MB_4", 10) = {3936};
// Rotor_Bnd_MB_5
Physical Curve("Rotor_Bnd_MB_5", 11) = {3938};
// Rotor_Bnd_MB_6
Physical Curve("Rotor_Bnd_MB_6", 12) = {3940};
// Rotor_Bnd_MB_7
Physical Curve("Rotor_Bnd_MB_7", 13) = {3942};
// Rotor_Bnd_MB_8
Physical Curve("Rotor_Bnd_MB_8", 14) = {3944};
// LuR2
Physical Surface("LuR2", 31) = {408};
// Mag0_0
Physical Surface("Mag0_0", 19) = {391};
// Mag1_0
Physical Surface("Mag1_0", 21) = {393};
// Lpl0
Physical Surface("Lpl0", 18) = {390};
// Lpl1
Physical Surface("Lpl1", 20) = {392};
// Lpl2
Physical Surface("Lpl2", 22) = {394};
// LuR1
Physical Surface("LuR1", 30) = {407};
// Pol
Physical Surface("Pol", 17) = {384};
// outerLimit
Physical Curve("outerLimit", 15) = {3867,3946,3948,3950,3952,3954};
// mbStator
Physical Curve("mbStator", 6) = {3906,3922,3924,3926,3928,3930};
// StLu2
Physical Surface("StLu2", 33) = {415,416,417,418,419,420};
// StLu1
Physical Surface("StLu1", 32) = {409,410,411,412,413,414};
// StNut
Physical Surface("StNut", 23) = {395,396,397,398,399,400};
// StCu0_0_Up
Physical Surface("StCu0_0_Up", 24) = {401};
// StCu0_1_Up
Physical Surface("StCu0_1_Up", 25) = {402};
// StCu0_2_Wn
Physical Surface("StCu0_2_Wn", 26) = {403};
// StCu0_3_Wn
Physical Surface("StCu0_3_Wn", 27) = {404};
// StCu0_4_Vp
Physical Surface("StCu0_4_Vp", 28) = {405};
// StCu0_5_Vp
Physical Surface("StCu0_5_Vp", 29) = {406};

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
	MeshSize { PointsOf {Surface{ 390,392,394 };} } = Lpl_msf*mm;
	MeshSize { PointsOf {Surface{ 391,393 };} } = Mag_msf*mm;
	MeshSize { PointsOf {Surface{ 384 };} } = Pol_msf*mm;
	MeshSize { PointsOf {Surface{ 407,408 };} } = LuR_msf*mm;
	MeshSize { PointsOf {Surface{ 407 };} } = LuR1_msf*mm;
	MeshSize { PointsOf {Surface{ 408 };} } = LuR2_msf*mm;
	MeshSize { PointsOf {Surface{ 401,402,403,404,405,406 };} } = StCu_msf*mm;
	MeshSize { PointsOf {Surface{ 395,396,397,398,399,400 };} } = StNut_msf*mm;
	MeshSize { PointsOf {Surface{ 409,410,411,412,413,414,415,416,417,418,419,420 };} } = StLu_msf*mm;
	MeshSize { PointsOf {Surface{ 409,410,411,412,413,414 };} } = StLu1_msf*mm;
	MeshSize { PointsOf {Surface{ 415,416,417,418,419,420 };} } = StLu2_msf*mm;
EndIf

// Mesh operations

// Do not switch mesh algorithm on failure, because this led to mesh errors in the past.
Mesh.AlgorithmSwitchOnFailure = 0;DefineConstant[Flag_CompoundMesh = {0, Name StrCat[INPUT_MESH, "Compound Mesh"], Choices {0,1}, Help "Use Compound Mesh to ignore lines between segments while meshing.",Visible Flag_ExpertMode}];
If (Flag_CompoundMesh)
Compound Surface{395,396,397,398,399,400}; // stator domainLam
Compound Surface{415,416,417,418,419,420}; // stator airGap
EndIf // (Flag_CompoundMesh)

// Add Periodic Mesh to model symmetry boundary-lines
primaryLines = {3909,3911,3912,3910,3913,3914};
secondaryLines = {3918,3919,3920,3915,3916,3917};
Periodic Curve{secondaryLines[]} = {primaryLines[]} Rotate {{0,0,1}, {0,0,0}, 2*Pi/8};

// Add mesh size setting for Movingband lines
DefineConstant[
	NbrMbSegments = {3370.0, Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],Max 1440, Min 180, Step 10, Help "Set the number of mesh segments on the interface between rotor/statorairgap and movingband. Value represents number of segments on whole circle.", Visible Flag_ExpertMode},
	r_MB_R = 0.08049999999999999
];
MB_LinesR = {3898,3932,3934,3936,3938,3940,3942,3944};
MeshSize{ PointsOf{Line{MB_LinesR[]};}} = 2*Pi*r_MB_R/NbrMbSegments;

MB_LinesS = {3906,3922,3924,3926,3928,3930};
MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*0.08065/NbrMbSegments;

Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)

// Create boundary lines for moving rotor contour plot
rotorBndLines[] = Boundary{ Physical Surface{ 19,21 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 17 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 31 }; };
statorBndLines[] = Boundary{ Physical Surface{ 3,5,6,15,23,24,25,26,27,28,29,32,33 }; };
Physical Line("DomainPlotMovingGeo",1) = {rotorBndLines[], statorBndLines[]};
