import math

magnetTypes = {
    0: {"id": "magnet01_surface",
        "laminationParams": {
            "r_We": 20e-3,
            "r_R": 55e-3,
            "meshLength": 3e-3,
        },
        "magnetParams" : {
            "h_M": 7e-3,
            "angularWidth_i": math.pi / 5,
            "angularWidth_a": math.pi / 6,
            "magnetisationDirection": [1, -1, 1, -1, 1, -1, 1, -1],
            "magnetisationType": "radial",
            "meshLength": 3e-3,
        }
    },
    1: {"id": "magnet02_surface",
        "laminationParams": {
            "r_We": 20e-3,
            "r_R": 55e-3,
            "meshLength": 3e-3,
        },
        "magnetParams" : {
            # "h_M": 7e-3,
            "h_M": 4e-3,
            # "w_Mag": 30e-3,
            "w_Mag": 20e-3,
            "r_Mag": 25e-3,
            "magnetisationDirection": [1, -1, 1, -1, 1, -1, 1, -1],
            "magnetisationType": "radial",
            "meshLength": 3e-3,
        }
    },
    2: {"id": "magnet03_surface",
        "laminationParams": {
            "r_We": 20e-3,
            "r_R": 55e-3,
            "meshLength": 3e-3,
        },
        "magnetParams" : {
            "h_M": 7e-3,
            "w_Mag": 30e-3,
            "magnetisationDirection": [1, -1, 1, -1, 1, -1, 1, -1],
            "magnetisationType": "radial",
            "meshLength": 3e-3,
        }
    }
}

slotTypes = {
    0: {
        "id": "slotForm_01",
        "laminationParams": {
            "r_S_i": 65e-3,
            "r_S_a": 100e-3,
            "meshLength": 3e-3,
        },
        "slotParams": {
            "w_SlotOP": 4e-3,
            "h_SlotOP": 4e-3,
            "w_Wedge": 20e-3,
            "h_Wedge": 7e-3,
            "h_Slot": 20e-3,
            "w_Slot": 14e-3,
            "meshLength": 3e-3,
            "slot_OPAir": True,
        }
    },
    1: {
        "id": "slotForm_01",
        "laminationParams": {
            "r_S_i": 65e-3,
            "r_S_a": 100e-3,
            "meshLength": 3e-3,
        },
        "slotParams": {
            "w_SlotOP": 4e-3,
            "h_SlotOP": 4e-3,
            "w_Wedge": 20e-3,
            "h_Wedge": 7e-3,
            "h_Slot": 20e-3,
            "w_Slot": 14e-3,
            "meshLength": 3e-3,
            "slot_OPAir": True,
        }
    }
}