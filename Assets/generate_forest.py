import random

forest = []

def header():
    return """#usda 1.0
(
    defaultPrim = "Forest"
)

def Xform "Forest"
{
"""

def footer():
    return "}\n"

# =========================
# 🌿 CONFIG ASSETS
# =========================

ASSETS = {
    "trees": ["Oak_Tree_1", "Oak_Tree_2"],
    "plains_trees": ["Blossom_Tree_Huge", "Blossom_Tree_Little"],
    "flowers": ["Flower"],
    "rocks": ["Rock_1", "Rock_2"],
    "maples": ["Maple_Tree_1", "Maple_Tree_2"],
    "grass": ["Grass", "Grass_1"],
    "ground_life": ["Mushroom", "Log", "Nest"]
}

# =========================
# 🌱 SCALE RANGES (IMPORTANT)
# =========================

SCALE_RANGES = {
    # 🌲 arbres forêt dense (grands)
    "trees": (0.9, 1.5),

    # 🌸 arbres prairie (plus légers)
    "plains_trees": (0.8, 1.2),

    # 🌳 maples zone rocheuse
    "maples": (0.9, 1.4),

    # 🪨 rochers (moyens à petits)
    "rocks": (0.2, 0.4),

    # 🌸 fleurs (très petites)
    "flowers": (0.08, 0.25),

    # 🌿 herbe (très petite)
    "grass": (0.05, 0.2),

    # 🍄 écosystème (varié petit à moyen)
    "ground_life": (0.05, 0.1)
}

# =========================
# 🧠 HELPERS
# =========================

def pick(category):
    lst = ASSETS.get(category, [])
    if not lst:
        raise ValueError(f"Empty asset category: {category}")
    return random.choice(lst)


def get_scale(category):
    min_s, max_s = SCALE_RANGES.get(category, (1.0, 1.0))
    s = random.uniform(min_s, max_s)

    # variation non uniforme (plus naturel)
    sx = round(s, 3)
    sy = round(s * random.uniform(0.9, 1.1), 3)
    sz = round(s * random.uniform(0.9, 1.1), 3)

    return sx, sy, sz


def ref_block(name, asset, category, pos, rot=True):
    if not name or not asset:
        return ""

    x, y, z = pos
    rot_val = random.randint(0, 360) if rot else 0

    sx, sy, sz = get_scale(category)

    return f"""
        def Xform "{name}"
        (
            prepend references = @Assets/{asset}.usda@
        )
        {{
            double3 xformOp:translate = ({x}, {y}, {z})
            float3 xformOp:rotateXYZ = (-90, {rot_val}, 0)
            float3 xformOp:scale = ({sx}, {sy}, {sz})

            uniform token[] xformOpOrder = [
                "xformOp:translate",
                "xformOp:rotateXYZ",
                "xformOp:scale"
            ]
        }}
"""


def zone(name):
    return f'    def Xform "{name}"\n    {{\n'


def zone_end():
    return "    }\n"


# =========================
# 🌍 FOREST GENERATION
# =========================

forest = []

# -------------------------
# 🌲 Dense Forest
# -------------------------
forest.append(zone("DenseForest"))

for i in range(25):
    forest.append(ref_block(
        f"Oak_{i}",
        pick("trees"),
        "trees",
        (random.randint(-20, -5), 0, random.randint(-20, 20))
    ))

forest.append(zone_end())

# -------------------------
# 🌼 Plains
# -------------------------
forest.append(zone("Plains"))

for i in range(12):
    forest.append(ref_block(
        f"Blossom_{i}",
        pick("plains_trees"),
        "plains_trees",
        (random.randint(5, 25), 0, random.randint(-10, 10))
    ))

for i in range(10):
    forest.append(ref_block(
        f"Flower_{i}",
        pick("flowers"),
        "flowers",
        (random.randint(5, 25), 0, random.randint(-10, 10)),
        rot=False
    ))

forest.append(zone_end())

# -------------------------
# 🪨 Rock Zone
# -------------------------
forest.append(zone("RockZone"))

for i in range(12):
    forest.append(ref_block(
        f"Maple_{i}",
        pick("maples"),
        "maples",
        (random.randint(-25, -10), 0, random.randint(-15, 5))
    ))

for i in range(10):
    forest.append(ref_block(
        f"Rock_{i}",
        pick("rocks"),
        "rocks",
        (random.randint(-25, -10), 0, random.randint(-15, 5))
    ))

forest.append(zone_end())

# -------------------------
# 🌿 Ecosystem (global ground life)
# -------------------------
forest.append(zone("Ecosystem"))

for i in range(10):
    forest.append(ref_block(
        f"Mushroom_{i}",
        "Mushroom",
        "ground_life",
        (random.randint(-25, 25), 0, random.randint(-25, 25))
    ))

for i in range(15):
    forest.append(ref_block(
        f"Grass_{i}",
        pick("grass"),
        "grass",
        (random.randint(-25, 25), 0, random.randint(-25, 25)),
        rot=False
    ))

for i in range(6):
    forest.append(ref_block(
        f"Log_{i}",
        "Log",
        "ground_life",
        (random.randint(-25, 25), 0, random.randint(-25, 25))
    ))

forest.append(zone_end())

forest.append(footer())

# =========================
# 💾 WRITE FILE
# =========================

with open("Forest.usda", "w", encoding="utf-8") as f:
    f.write(header() + "".join(forest))

print("✔ Forest.usda generated successfully")