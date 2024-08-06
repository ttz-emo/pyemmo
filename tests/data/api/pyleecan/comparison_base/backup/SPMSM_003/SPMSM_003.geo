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
point_pylc_dup = 6044; Point(6044) = {0.2, 0.0, 0, 0.009999999999999998*gmsf};
point_pylc_dup = 6045; Point(6045) = {0.116, 0.0, 0, 0.0009719626168224236*gmsf};
PointM41_dup = 6051; Point(6051) = {0.11520000000000001, 0, 0, 0.0008859813084112094*gmsf};
PointM31_dup = 6052; Point(6052) = {0.1144, 0, 0, 0.0007999999999999937*gmsf};
point_pylc_dup = 6042; Point(6042) = {0.0225, 0.0, 0, 0.01940492957746467*gmsf};
point_pylc_dup = 6043; Point(6043) = {0.1, 0.0, 0, 0.003577464788732372*gmsf};
PointM11_dup = 6047; Point(6047) = {0.1128, 0, 0, 0.0009633802816901378*gmsf};
PointM21_dup = 6049; Point(6049) = {0.1136, 0, 0, 0.0007999999999999952*gmsf};
point_pylc_dup = 6054; Point(6054) = {-0.2, 2.4492935982947065e-17, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 6055; Point(6055) = {-0.116, 1.4205902870109297e-17, 0.0, 0.0009719626168224236*gmsf};
PointM41_dup = 6057; Point(6057) = {-0.11520000000000001, 1.410793112617751e-17, 0.0, 0.0008859813084112094*gmsf};
PointM31_dup = 6058; Point(6058) = {-0.1144, 1.400995938224572e-17, 0.0, 0.0007999999999999937*gmsf};
point_pylc_dup = 6060; Point(6060) = {-0.0225, 2.7554552980815448e-18, 0.0, 0.01940492957746467*gmsf};
point_pylc_dup = 6061; Point(6061) = {-0.1, 1.2246467991473533e-17, 0.0, 0.003577464788732372*gmsf};
PointM11_dup = 6063; Point(6063) = {-0.1128, 1.3814015894382144e-17, 0.0, 0.0009633802816901378*gmsf};
PointM21_dup = 6065; Point(6065) = {-0.1136, 1.3911987638313932e-17, 0.0, 0.0007999999999999952*gmsf};
point_pylc = 5969; Point(5969) = {1.3777276490407724e-18, 0.0225, 0, 0.01940492957746467*gmsf};
point_pylc = 5970; Point(5970) = {0, 0, 0, 0.001*gmsf};
point_pylc_dup = 6118; Point(6118) = {0.09876883405950741, 0.015643446504063286, 0, 0.003577464788732372*gmsf};
point_pylc_dup = 6119; Point(6119) = {0.1106210941466483, 0.01752066008455088, 0, 0.0011267605633802748*gmsf};
point_pylc_dup = 6122; Point(6122) = {-0.1106210941466483, 0.017520660084550894, 0, 0.0011267605633802748*gmsf};
point_pylc_dup = 6124; Point(6124) = {-0.09876883405950741, 0.0156434465040633, 0, 0.003577464788732372*gmsf};
point_pylc = 5986; Point(5986) = {0.17320508075688776, 0.09999999999999999, 0, 0.009999999999999998*gmsf};
point_pylc_dup = 6084; Point(6084) = {0.10000000000000003, 0.17320508075688773, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 6087; Point(6087) = {4.163336342344337e-17, 0.20000000000000004, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 6090; Point(6090) = {-0.09999999999999998, 0.17320508075688776, 0.0, 0.009999999999999998*gmsf};
point_pylc_dup = 6093; Point(6093) = {-0.1732050807568877, 0.10000000000000005, 0.0, 0.009999999999999998*gmsf};
PointM32 = 6041; Point(6041) = {0.09907330619293979, 0.057199999999999994, 0, 0.0007999999999999937*gmsf};
PointM32_dup = 6068; Point(6068) = {0.05720000000000002, 0.09907330619293978, 0.0, 0.0007999999999999937*gmsf};
PointM32_dup = 6071; Point(6071) = {2.7755575615628914e-17, 0.1144, 0.0, 0.0007999999999999937*gmsf};
PointM32_dup = 6074; Point(6074) = {-0.05719999999999999, 0.09907330619293979, 0.0, 0.0007999999999999923*gmsf};
PointM32_dup = 6077; Point(6077) = {-0.09907330619293976, 0.05720000000000003, 0.0, 0.0007999999999999937*gmsf};
PointM42_dup = 6520; Point(6520) = {0.09976612651596735, 0.0576, 0, 0.0008859813084112094*gmsf};
PointM42_dup = 6530; Point(6530) = {0.057600000000000026, 0.09976612651596733, 0.0, 0.0008859813084112094*gmsf};
PointM42_dup = 6540; Point(6540) = {2.7755575615628914e-17, 0.11520000000000001, 0.0, 0.0008859813084112094*gmsf};
PointM42_dup = 6550; Point(6550) = {-0.05759999999999999, 0.09976612651596735, 0.0, 0.0008859813084112094*gmsf};
PointM42_dup = 6560; Point(6560) = {-0.09976612651596732, 0.05760000000000003, 0.0, 0.0008859813084112094*gmsf};
point_pylc_dup = 6400; Point(6400) = {0.11371145625611974, 0.022928251483978635, 0, 0.0009719626168224236*gmsf};
point_pylc_dup = 6402; Point(6402) = {0.11763254095460662, 0.02371888084549514, 0, 0.0014018691588785004*gmsf};
point_pylc_dup = 6403; Point(6403) = {0.11373220920115029, 0.03827511711576839, 0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6404; Point(6404) = {0.10994113556111196, 0.03699927987857611, 0, 0.0009719626168224222*gmsf};
point_pylc_dup = 6407; Point(6407) = {0.1004589468389949, 0.057999999999999996, 0, 0.0009719626168224236*gmsf};
point_pylc_dup = 6420; Point(6420) = {0.08701288407713331, 0.07671217637754361, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 6422; Point(6422) = {0.09001332835565515, 0.07935742383883823, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 6423; Point(6423) = {0.07935742383883825, 0.09001332835565515, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6424; Point(6424) = {0.07671217637754364, 0.08701288407713331, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 6427; Point(6427) = {0.058000000000000024, 0.10045894683899488, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 6440; Point(6440) = {0.03699927987857613, 0.10994113556111194, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 6442; Point(6442) = {0.038275117115768406, 0.11373220920115028, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6443; Point(6443) = {0.023718880845495158, 0.11763254095460662, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6444; Point(6444) = {0.02292825148397866, 0.11371145625611975, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 6447; Point(6447) = {2.7755575615628914e-17, 0.11600000000000002, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 6460; Point(6460) = {-0.022928251483978628, 0.11371145625611974, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 6462; Point(6462) = {-0.023718880845495133, 0.11763254095460662, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 6463; Point(6463) = {-0.038275117115768385, 0.11373220920115029, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6464; Point(6464) = {-0.036999279878576104, 0.10994113556111196, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 6467; Point(6467) = {-0.05799999999999999, 0.1004589468389949, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 6480; Point(6480) = {-0.0767121763775436, 0.08701288407713333, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 6482; Point(6482) = {-0.0793574238388382, 0.09001332835565515, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6483; Point(6483) = {-0.09001332835565512, 0.07935742383883826, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6484; Point(6484) = {-0.08701288407713328, 0.07671217637754364, 0.0, 0.0009719626168224222*gmsf};
point_pylc_dup = 6487; Point(6487) = {-0.10045894683899487, 0.05800000000000004, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 6500; Point(6500) = {-0.10994113556111193, 0.03699927987857615, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 6502; Point(6502) = {-0.11373220920115026, 0.03827511711576844, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6503; Point(6503) = {-0.11763254095460662, 0.023718880845495185, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6504; Point(6504) = {-0.11371145625611975, 0.022928251483978687, 0.0, 0.0009719626168224236*gmsf};
point_pylc_dup = 6142; Point(6142) = {0.11852260087141653, 0.018772135804827707, 0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6144; Point(6144) = {0.14321480938629497, 0.02268299743083347, 0, 0.004088785046728965*gmsf};
point_pylc_dup = 6147; Point(6147) = {0.13536916184209424, 0.05196335268406853, 0, 0.004088785046728965*gmsf};
point_pylc_dup = 6149; Point(6149) = {0.11202965117966421, 0.04300415394543603, 0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6172; Point(6172) = {0.09325751537483652, 0.07551844692598049, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 6174; Point(6174) = {0.1126861644112608, 0.09125145670222641, 0.0, 0.004088785046728967*gmsf};
point_pylc_dup = 6177; Point(6177) = {0.09125145670222644, 0.11268616441126075, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 6179; Point(6179) = {0.0755184469259805, 0.09325751537483651, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 6202; Point(6202) = {0.043004153945436045, 0.11202965117966421, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6204; Point(6204) = {0.051963352684068556, 0.13536916184209424, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 6207; Point(6207) = {0.022682997430833497, 0.14321480938629494, 0.0, 0.004088785046728962*gmsf};
point_pylc_dup = 6209; Point(6209) = {0.01877213580482772, 0.11852260087141653, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6232; Point(6232) = {-0.0187721358048277, 0.11852260087141653, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6234; Point(6234) = {-0.02268299743083346, 0.14321480938629497, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 6237; Point(6237) = {-0.05196335268406852, 0.13536916184209424, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 6239; Point(6239) = {-0.043004153945436024, 0.11202965117966421, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6262; Point(6262) = {-0.07551844692598048, 0.09325751537483652, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6264; Point(6264) = {-0.0912514567022264, 0.1126861644112608, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 6267; Point(6267) = {-0.11268616441126074, 0.09125145670222644, 0.0, 0.004088785046728962*gmsf};
point_pylc_dup = 6269; Point(6269) = {-0.09325751537483648, 0.0755184469259805, 0.0, 0.0014018691588784976*gmsf};
point_pylc_dup = 6292; Point(6292) = {-0.11202965117966421, 0.04300415394543608, 0.0, 0.0014018691588785004*gmsf};
point_pylc_dup = 6294; Point(6294) = {-0.13536916184209422, 0.051963352684068584, 0.0, 0.004088785046728965*gmsf};
point_pylc_dup = 6297; Point(6297) = {-0.14321480938629494, 0.022682997430833532, 0.0, 0.004088785046728962*gmsf};
point_pylc_dup = 6299; Point(6299) = {-0.11852260087141651, 0.01877213580482775, 0.0, 0.0014018691588784976*gmsf};

// Lines and Curves
Line_dup = 3510;Line(Line_dup) = {6044, 6045};
lowerLine4_dup = 3513;Line(lowerLine4_dup) = {6045, 6051};
lowerLine3_dup = 3514;Line(lowerLine3_dup) = {6052, 6051};
Line_dup = 3509;Line(Line_dup) = {6042, 6043};
lowerLine1_dup = 3511;Line(lowerLine1_dup) = {6043, 6047};
lowerLine2_dup = 3512;Line(lowerLine2_dup) = {6047, 6049};
Line_dup = 3515;Line(Line_dup) = {6054, 6055};
lowerLine4_dup = 3516;Line(lowerLine4_dup) = {6055, 6057};
lowerLine3_dup = 3517;Line(lowerLine3_dup) = {6058, 6057};
Line_dup = 3518;Line(Line_dup) = {6060, 6061};
lowerLine1_dup = 3519;Line(lowerLine1_dup) = {6061, 6063};
lowerLine2_dup = 3520;Line(lowerLine2_dup) = {6063, 6065};
InnerLimit = 3458;Circle(InnerLimit) = {6060, 5970, 5969};
InnerLimit = 3460;Circle(InnerLimit) = {5969, 5970, 6042};
MB_CurveRotor = 3498;Circle(MB_CurveRotor) = {6049, 5970, 6065};
rotorBand1_dup = 3718;Circle(rotorBand1_dup) = {6047, 5970, 6063};
Line_dup = 3555;Line(Line_dup) = {6118, 6119};
CircleArc_dup = 3557;Circle(CircleArc_dup) = {6119, 5970, 6122};
Line_dup = 3558;Line(Line_dup) = {6122, 6124};
CircleArc_dup = 3560;Circle(CircleArc_dup) = {6124, 5970, 6118};
CircleArc_dup = 3706;Circle(CircleArc_dup) = {6043, 5970, 6118};
CircleArc_dup = 3708;Circle(CircleArc_dup) = {6124, 5970, 6061};
OuterLimit = 3469;Circle(OuterLimit) = {5986, 5970, 6044};
OuterLimit_dup = 3534;Circle(OuterLimit_dup) = {6084, 5970, 5986};
OuterLimit_dup = 3536;Circle(OuterLimit_dup) = {6087, 5970, 6084};
OuterLimit_dup = 3538;Circle(OuterLimit_dup) = {6090, 5970, 6087};
OuterLimit_dup = 3540;Circle(OuterLimit_dup) = {6093, 5970, 6090};
OuterLimit_dup = 3542;Circle(OuterLimit_dup) = {6054, 5970, 6093};
MB_CurveStator = 3506;Circle(MB_CurveStator) = {6052, 5970, 6041};
MB_CurveStator_dup = 3522;Circle(MB_CurveStator_dup) = {6041, 5970, 6068};
MB_CurveStator_dup = 3524;Circle(MB_CurveStator_dup) = {6068, 5970, 6071};
MB_CurveStator_dup = 3526;Circle(MB_CurveStator_dup) = {6071, 5970, 6074};
MB_CurveStator_dup = 3528;Circle(MB_CurveStator_dup) = {6074, 5970, 6077};
MB_CurveStator_dup = 3530;Circle(MB_CurveStator_dup) = {6077, 5970, 6058};
statorCircle4_dup = 3796;Circle(statorCircle4_dup) = {6051, 5970, 6520};
upperLine3_dup = 3800;Line(upperLine3_dup) = {6041, 6520};
statorCircle4_dup = 3802;Circle(statorCircle4_dup) = {6520, 5970, 6530};
upperLine3_dup = 3806;Line(upperLine3_dup) = {6068, 6530};
statorCircle4_dup = 3808;Circle(statorCircle4_dup) = {6530, 5970, 6540};
upperLine3_dup = 3812;Line(upperLine3_dup) = {6071, 6540};
statorCircle4_dup = 3814;Circle(statorCircle4_dup) = {6540, 5970, 6550};
upperLine3_dup = 3818;Line(upperLine3_dup) = {6074, 6550};
statorCircle4_dup = 3820;Circle(statorCircle4_dup) = {6550, 5970, 6560};
upperLine3_dup = 3824;Line(upperLine3_dup) = {6077, 6560};
statorCircle4_dup = 3826;Circle(statorCircle4_dup) = {6560, 5970, 6057};
CircleArc_dup = 3724;Circle(CircleArc_dup) = {6045, 5970, 6400};
Line_dup = 3725;Line(Line_dup) = {6400, 6402};
Line_dup = 3726;Line(Line_dup) = {6403, 6404};
CircleArc_dup = 3728;Circle(CircleArc_dup) = {6404, 5970, 6407};
interface_line_slot_opening___slot_dup = 3730;Circle(interface_line_slot_opening___slot_dup) = {6402, 5970, 6403};
upperLine4_dup = 3734;Line(upperLine4_dup) = {6407, 6520};
CircleArc_dup = 3736;Circle(CircleArc_dup) = {6407, 5970, 6420};
Line_dup = 3737;Line(Line_dup) = {6420, 6422};
Line_dup = 3738;Line(Line_dup) = {6423, 6424};
CircleArc_dup = 3740;Circle(CircleArc_dup) = {6424, 5970, 6427};
interface_line_slot_opening___slot_dup = 3742;Circle(interface_line_slot_opening___slot_dup) = {6422, 5970, 6423};
upperLine4_dup = 3746;Line(upperLine4_dup) = {6427, 6530};
CircleArc_dup = 3748;Circle(CircleArc_dup) = {6427, 5970, 6440};
Line_dup = 3749;Line(Line_dup) = {6440, 6442};
Line_dup = 3750;Line(Line_dup) = {6443, 6444};
CircleArc_dup = 3752;Circle(CircleArc_dup) = {6444, 5970, 6447};
interface_line_slot_opening___slot_dup = 3754;Circle(interface_line_slot_opening___slot_dup) = {6442, 5970, 6443};
upperLine4_dup = 3758;Line(upperLine4_dup) = {6447, 6540};
CircleArc_dup = 3760;Circle(CircleArc_dup) = {6447, 5970, 6460};
Line_dup = 3761;Line(Line_dup) = {6460, 6462};
Line_dup = 3762;Line(Line_dup) = {6463, 6464};
CircleArc_dup = 3764;Circle(CircleArc_dup) = {6464, 5970, 6467};
interface_line_slot_opening___slot_dup = 3766;Circle(interface_line_slot_opening___slot_dup) = {6462, 5970, 6463};
upperLine4_dup = 3770;Line(upperLine4_dup) = {6467, 6550};
CircleArc_dup = 3772;Circle(CircleArc_dup) = {6467, 5970, 6480};
Line_dup = 3773;Line(Line_dup) = {6480, 6482};
Line_dup = 3774;Line(Line_dup) = {6483, 6484};
CircleArc_dup = 3776;Circle(CircleArc_dup) = {6484, 5970, 6487};
interface_line_slot_opening___slot_dup = 3778;Circle(interface_line_slot_opening___slot_dup) = {6482, 5970, 6483};
upperLine4_dup = 3782;Line(upperLine4_dup) = {6487, 6560};
CircleArc_dup = 3784;Circle(CircleArc_dup) = {6487, 5970, 6500};
Line_dup = 3785;Line(Line_dup) = {6500, 6502};
Line_dup = 3786;Line(Line_dup) = {6503, 6504};
CircleArc_dup = 3788;Circle(CircleArc_dup) = {6504, 5970, 6055};
interface_line_slot_opening___slot_dup = 3790;Circle(interface_line_slot_opening___slot_dup) = {6502, 5970, 6503};
Line_dup = 3561;Line(Line_dup) = {6407, 5986};
CircleArc_dup = 3569;Circle(CircleArc_dup) = {6402, 5970, 6142};
Line_dup = 3570;Line(Line_dup) = {6142, 6144};
CircleArc_dup = 3572;Circle(CircleArc_dup) = {6144, 5970, 6147};
Line_dup = 3573;Line(Line_dup) = {6147, 6149};
CircleArc_dup = 3575;Circle(CircleArc_dup) = {6149, 5970, 6403};
Line_dup = 3579;Line(Line_dup) = {6427, 6084};
CircleArc_dup = 3587;Circle(CircleArc_dup) = {6422, 5970, 6172};
Line_dup = 3588;Line(Line_dup) = {6172, 6174};
CircleArc_dup = 3590;Circle(CircleArc_dup) = {6174, 5970, 6177};
Line_dup = 3591;Line(Line_dup) = {6177, 6179};
CircleArc_dup = 3593;Circle(CircleArc_dup) = {6179, 5970, 6423};
Line_dup = 3597;Line(Line_dup) = {6447, 6087};
CircleArc_dup = 3605;Circle(CircleArc_dup) = {6442, 5970, 6202};
Line_dup = 3606;Line(Line_dup) = {6202, 6204};
CircleArc_dup = 3608;Circle(CircleArc_dup) = {6204, 5970, 6207};
Line_dup = 3609;Line(Line_dup) = {6207, 6209};
CircleArc_dup = 3611;Circle(CircleArc_dup) = {6209, 5970, 6443};
Line_dup = 3615;Line(Line_dup) = {6467, 6090};
CircleArc_dup = 3623;Circle(CircleArc_dup) = {6462, 5970, 6232};
Line_dup = 3624;Line(Line_dup) = {6232, 6234};
CircleArc_dup = 3626;Circle(CircleArc_dup) = {6234, 5970, 6237};
Line_dup = 3627;Line(Line_dup) = {6237, 6239};
CircleArc_dup = 3629;Circle(CircleArc_dup) = {6239, 5970, 6463};
Line_dup = 3633;Line(Line_dup) = {6487, 6093};
CircleArc_dup = 3641;Circle(CircleArc_dup) = {6482, 5970, 6262};
Line_dup = 3642;Line(Line_dup) = {6262, 6264};
CircleArc_dup = 3644;Circle(CircleArc_dup) = {6264, 5970, 6267};
Line_dup = 3645;Line(Line_dup) = {6267, 6269};
CircleArc_dup = 3647;Circle(CircleArc_dup) = {6269, 5970, 6483};
CircleArc_dup = 3659;Circle(CircleArc_dup) = {6502, 5970, 6292};
Line_dup = 3660;Line(Line_dup) = {6292, 6294};
CircleArc_dup = 3662;Circle(CircleArc_dup) = {6294, 5970, 6297};
Line_dup = 3663;Line(Line_dup) = {6297, 6299};
CircleArc_dup = 3665;Circle(CircleArc_dup) = {6299, 5970, 6503};
CircleArc_dup = 3670;Circle(CircleArc_dup) = {6142, 5970, 6149};
CircleArc_dup = 3676;Circle(CircleArc_dup) = {6172, 5970, 6179};
CircleArc_dup = 3682;Circle(CircleArc_dup) = {6202, 5970, 6209};
CircleArc_dup = 3688;Circle(CircleArc_dup) = {6232, 5970, 6239};
CircleArc_dup = 3694;Circle(CircleArc_dup) = {6262, 5970, 6269};
CircleArc_dup = 3700;Circle(CircleArc_dup) = {6292, 5970, 6299};

// Surfaces

Curve Loop(359) = {3718,3520,-3498,-3512};
Surf_rotorAirGap2_dup = {359};
Plane Surface(Surf_rotorAirGap2_dup) = {359};

Curve Loop(345) = {3555,3557,3558,3560};
Surf_Magnet_dup = {345};
Plane Surface(Surf_Magnet_dup) = {345};

Curve Loop(358) = {3706,3555,3557,3558,3708,3519,-3718,-3511};
Surf_rotorAirGap1_dup = {358};
Plane Surface(Surf_rotorAirGap1_dup) = {358};

Curve Loop(344) = {3509,3706,-3560,3708,-3518,3458,3460};
Surf_Rotorblech_dup = {344};
Plane Surface(Surf_Rotorblech_dup) = {344};

Curve Loop(366) = {3796,-3800,-3506,3514};
Surf_statorAirGap2_dup = {366};
Plane Surface(Surf_statorAirGap2_dup) = {366};

Curve Loop(367) = {3802,-3806,-3522,3800};
Surf_statorAirGap2_dup = {367};
Plane Surface(Surf_statorAirGap2_dup) = {367};

Curve Loop(368) = {3808,-3812,-3524,3806};
Surf_statorAirGap2_dup = {368};
Plane Surface(Surf_statorAirGap2_dup) = {368};

Curve Loop(369) = {3814,-3818,-3526,3812};
Surf_statorAirGap2_dup = {369};
Plane Surface(Surf_statorAirGap2_dup) = {369};

Curve Loop(370) = {3820,-3824,-3528,3818};
Surf_statorAirGap2_dup = {370};
Plane Surface(Surf_statorAirGap2_dup) = {370};

Curve Loop(371) = {3826,-3517,-3530,3824};
Surf_statorAirGap2_dup = {371};
Plane Surface(Surf_statorAirGap2_dup) = {371};

Curve Loop(360) = {3724,3725,3730,3726,3728,3734,-3796,-3513};
Surf_statorAirGap1_dup = {360};
Plane Surface(Surf_statorAirGap1_dup) = {360};

Curve Loop(361) = {3736,3737,3742,3738,3740,3746,-3802,-3734};
Surf_statorAirGap1_dup = {361};
Plane Surface(Surf_statorAirGap1_dup) = {361};

Curve Loop(362) = {3748,3749,3754,3750,3752,3758,-3808,-3746};
Surf_statorAirGap1_dup = {362};
Plane Surface(Surf_statorAirGap1_dup) = {362};

Curve Loop(363) = {3760,3761,3766,3762,3764,3770,-3814,-3758};
Surf_statorAirGap1_dup = {363};
Plane Surface(Surf_statorAirGap1_dup) = {363};

Curve Loop(364) = {3772,3773,3778,3774,3776,3782,-3820,-3770};
Surf_statorAirGap1_dup = {364};
Plane Surface(Surf_statorAirGap1_dup) = {364};

Curve Loop(365) = {3784,3785,3790,3786,3788,3516,-3826,-3782};
Surf_statorAirGap1_dup = {365};
Plane Surface(Surf_statorAirGap1_dup) = {365};

Curve Loop(346) = {3561,3469,3510,3724,3725,3569,3570,3572,3573,3575,3726,3728};
Surf_Statorblech_dup = {346};
Plane Surface(Surf_Statorblech_dup) = {346};

Curve Loop(347) = {3579,3534,-3561,3736,3737,3587,3588,3590,3591,3593,3738,3740};
Surf_Statorblech_dup = {347};
Plane Surface(Surf_Statorblech_dup) = {347};

Curve Loop(348) = {3597,3536,-3579,3748,3749,3605,3606,3608,3609,3611,3750,3752};
Surf_Statorblech_dup = {348};
Plane Surface(Surf_Statorblech_dup) = {348};

Curve Loop(349) = {3615,3538,-3597,3760,3761,3623,3624,3626,3627,3629,3762,3764};
Surf_Statorblech_dup = {349};
Plane Surface(Surf_Statorblech_dup) = {349};

Curve Loop(350) = {3633,3540,-3615,3772,3773,3641,3642,3644,3645,3647,3774,3776};
Surf_Statorblech_dup = {350};
Plane Surface(Surf_Statorblech_dup) = {350};

Curve Loop(351) = {3515,-3788,-3786,-3665,-3663,-3662,-3660,-3659,-3785,-3784,3633,-3542};
Surf_Statorblech_dup = {351};
Plane Surface(Surf_Statorblech_dup) = {351};

Curve Loop(352) = {3670,-3573,-3572,-3570};
Surf_Stator_Nut_dup = {352};
Plane Surface(Surf_Stator_Nut_dup) = {352};

Curve Loop(353) = {3676,-3591,-3590,-3588};
Surf_Stator_Nut_dup = {353};
Plane Surface(Surf_Stator_Nut_dup) = {353};

Curve Loop(354) = {3682,-3609,-3608,-3606};
Surf_Stator_Nut_dup = {354};
Plane Surface(Surf_Stator_Nut_dup) = {354};

Curve Loop(355) = {3688,-3627,-3626,-3624};
Surf_Stator_Nut_dup = {355};
Plane Surface(Surf_Stator_Nut_dup) = {355};

Curve Loop(356) = {3694,-3645,-3644,-3642};
Surf_Stator_Nut_dup = {356};
Plane Surface(Surf_Stator_Nut_dup) = {356};

Curve Loop(357) = {3700,-3663,-3662,-3660};
Surf_Stator_Nut_dup = {357};
Plane Surface(Surf_Stator_Nut_dup) = {357};

// Color code
If (!Flag_individualColoring)
Color SkyBlue {Surface {359}; }
Color Red {Surface {345}; }
Color SkyBlue {Surface {358}; }
Color SteelBlue {Surface {344}; }
Color SkyBlue {Surface {366}; }
Color SkyBlue {Surface {367}; }
Color SkyBlue {Surface {368}; }
Color SkyBlue {Surface {369}; }
Color SkyBlue {Surface {370}; }
Color SkyBlue {Surface {371}; }
Color SkyBlue {Surface {360}; }
Color SkyBlue {Surface {361}; }
Color SkyBlue {Surface {362}; }
Color SkyBlue {Surface {363}; }
Color SkyBlue {Surface {364}; }
Color SkyBlue {Surface {365}; }
Color SteelBlue4 {Surface {346}; }
Color SteelBlue4 {Surface {347}; }
Color SteelBlue4 {Surface {348}; }
Color SteelBlue4 {Surface {349}; }
Color SteelBlue4 {Surface {350}; }
Color SteelBlue4 {Surface {351}; }
Color Magenta {Surface {352}; }
Color Magenta {Surface {353}; }
Color Cyan {Surface {354}; }
Color Cyan {Surface {355}; }
Color Yellow4 {Surface {356}; }
Color Yellow4 {Surface {357}; }
EndIf

// Physical Elements
// primaryLineS
Physical Curve("primaryLineS", 3) = {3510,3513,3514};
// primaryLineR
Physical Curve("primaryLineR", 2) = {3509,3511,3512};
// slaveLineS
Physical Curve("slaveLineS", 5) = {3515,3516,3517};
// slaveLineR
Physical Curve("slaveLineR", 4) = {3518,3519,3520};
// innerLimit
Physical Curve("innerLimit", 10) = {3458,3460};
// Rotor_Bnd_MB_1
Physical Curve("Rotor_Bnd_MB_1", 7) = {3498};
// Rotor_Bnd_MB_2
Physical Curve("Rotor_Bnd_MB_2", 8) = {3498};
// LuR2
Physical Surface("LuR2", 21) = {359};
// Mag0_0
Physical Surface("Mag0_0", 12) = {345};
// LuR1
Physical Surface("LuR1", 20) = {358};
// Pol
Physical Surface("Pol", 11) = {344};
// outerLimit
Physical Curve("outerLimit", 9) = {3469,3534,3536,3538,3540,3542};
// mbStator
Physical Curve("mbStator", 6) = {3506,3522,3524,3526,3528,3530};
// StLu2
Physical Surface("StLu2", 23) = {366,367,368,369,370,371};
// StLu1
Physical Surface("StLu1", 22) = {360,361,362,363,364,365};
// StNut
Physical Surface("StNut", 13) = {346,347,348,349,350,351};
// StCu0_0_Up
Physical Surface("StCu0_0_Up", 14) = {352};
// StCu0_1_Up
Physical Surface("StCu0_1_Up", 15) = {353};
// StCu0_2_Wn
Physical Surface("StCu0_2_Wn", 16) = {354};
// StCu0_3_Wn
Physical Surface("StCu0_3_Wn", 17) = {355};
// StCu0_4_Vp
Physical Surface("StCu0_4_Vp", 18) = {356};
// StCu0_5_Vp
Physical Surface("StCu0_5_Vp", 19) = {357};

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
	MeshSize { PointsOf {Surface{ 345 };} } = Mag_msf*mm;
	MeshSize { PointsOf {Surface{ 344 };} } = Pol_msf*mm;
	MeshSize { PointsOf {Surface{ 358,359 };} } = LuR_msf*mm;
	MeshSize { PointsOf {Surface{ 358 };} } = LuR1_msf*mm;
	MeshSize { PointsOf {Surface{ 359 };} } = LuR2_msf*mm;
	MeshSize { PointsOf {Surface{ 352,353,354,355,356,357 };} } = StCu_msf*mm;
	MeshSize { PointsOf {Surface{ 346,347,348,349,350,351 };} } = StNut_msf*mm;
	MeshSize { PointsOf {Surface{ 360,361,362,363,364,365,366,367,368,369,370,371 };} } = StLu_msf*mm;
	MeshSize { PointsOf {Surface{ 360,361,362,363,364,365 };} } = StLu1_msf*mm;
	MeshSize { PointsOf {Surface{ 366,367,368,369,370,371 };} } = StLu2_msf*mm;
EndIf

// Mesh operations

// Do not switch mesh algorithm on failure, because this led to mesh errors in the past.
Mesh.AlgorithmSwitchOnFailure = 0;DefineConstant[Flag_CompoundMesh = {0, Name StrCat[INPUT_MESH, "Compound Mesh"], Choices {0,1}, Help "Use Compound Mesh to ignore lines between segments while meshing.",Visible Flag_ExpertMode}];
If (Flag_CompoundMesh)
Compound Surface{346,347,348,349,350,351}; // stator domainLam
Compound Surface{366,367,368,369,370,371}; // stator airGap
EndIf // (Flag_CompoundMesh)

// Add Periodic Mesh to model symmetry boundary-lines
primaryLines = {3509,3511,3512,3510,3513,3514};
secondaryLines = {3518,3519,3520,3515,3516,3517};
Periodic Curve{secondaryLines[]} = {primaryLines[]} Rotate {{0,0,1}, {0,0,0}, 2*Pi/2};

// Add mesh size setting for Movingband lines
DefineConstant[
	NbrMbSegments = {890.0, Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],Max 1440, Min 180, Step 10, Help "Set the number of mesh segments on the interface between rotor/statorairgap and movingband. Value represents number of segments on whole circle.", Visible Flag_ExpertMode},
	r_MB_R = 0.1136
];
MB_LinesR = {3498,3532};
MeshSize{ PointsOf{Line{MB_LinesR[]};}} = 2*Pi*r_MB_R/NbrMbSegments;

MB_LinesS = {3506,3522,3524,3526,3528,3530};
MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*0.1144/NbrMbSegments;

Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)

// Create boundary lines for moving rotor contour plot
rotorBndLines[] = Boundary{ Physical Surface{ 12 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 11 }; };
rotorBndLines[] += CombinedBoundary{ Physical Surface{ 21 }; };
statorBndLines[] = Boundary{ Physical Surface{ 3,5,6,9,13,14,15,16,17,18,19,22,23 }; };
Physical Line("DomainPlotMovingGeo",1) = {rotorBndLines[], statorBndLines[]};
