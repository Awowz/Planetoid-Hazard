
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

BORDER_KILL_ZONE_X = SCREEN_WIDTH // 2
BORDER_KILL_ZONE_Y = SCREEN_HEIGHT // 2

PAUSE_STATE = "PAUSED"
GAME_STATE = "GAMED"
REWARD_STATE = "REWARD"
EXIT_STATE = "EXIT"

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8  # SECONDS
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_COLOR = (255,0,0)
ASTEROID_BASE_HEALTH = 30
ASTEROID_BASE_EXP_DROP = 10

MELEE_RADIUS = 29
MELEE_SPEED = 80
MELEE_COLOR = (100, 255, 0)
MELEE_BASE_HEALTH = 40
MELEE_BASE_EXP_DROP = 30

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200

CHEST_RADIUS = 20
CHEST_DISTANCE_X = 100
CHEST_TEXT_X_OFFSET = 75
CHEST_TEXT_Y_OFFSET = 50
CHEST_Y_OFFSET = 45
CHEST_X_POS = SCREEN_WIDTH / 2
CHEST_Y_POS = SCREEN_HEIGHT / 2 + CHEST_Y_OFFSET

PLAYER_DEATH_TIMER = 5.5
PLAYER_DEATH_UI_FONT = 124
PLAYER_DEATH_UI_XOFFSET = 50
PLAYER_DEATH_UI_YOFFSET = 150
PLAYER_DEATH_ROTATION_SPEED = 146
PLAYER_DEATH_DEBREE_SPEED = 74

SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOT_COOLDOWN = 0.3
PLAYER_EXP_MAGNET = 60
PLAYER_EXP_REQUIRED_BASE = 100
PLAYER_EXP_MULTIPLIER_BASE = 0.099
PLAYER_EXP_MULTIPLIER_EXPO = 1.5

PLAYER_EXP_DISPLAY_POSITION_X = 0
PLAYER_EXP_DISPLAY_POSITION_Y = SCREEN_HEIGHT * 0.1
PLAYER_EXP_DISPLAY_LENGTH = 200
PLAYER_EXP_DISPLAY_HEIGHT = 5
PLAYER_EXP_DISPLAY_BORDER = 5
PLAYER_EXP_DISPLAY_BORDER_COLOR = (65,65,65)

PLAYER_RELOAD_DISPLAY_LENGTH = 130
PLAYER_RELOAD_DISPLAY_HEIGHT = 5
PLAYER_RELOAD_DISPLAY_BORDER = 5

UI_PLAYER_LVL_OFFSET = 25
UI_FONT_SIZE = 32
UI_FONT_COLOR = (255,255,255)
UI_TEXT_FADE_TIME = 6
UI_TEXT_FLOAT_SPEED = 20
UI_WEAPON_TEXT_SPEED = 35
UI_WEAPON_TEXT_FADE = 1.8

EXP_HIT_BOX_RADIUS = 8
EXP_COLOR = (255, 255, 128)
EXP_SIZE_WIDTH = 20
EXP_SIZE_HEIGHT = 20
EXP_ROTATION_SPEED = 200
EXP_SPEED = 500

PARTICLE_RADIUS = 2
PARTICLE_RADIUS_TRHUST = 3
PARTICLE_THRUST_COOLDOWN = 0.1
PARTICLE_THRUST_DEGREE_VARIANCE = 25
PARTICLE_THRUST_SPEED = 300
PARTICLE_ON_HIT_FADE = 1
PARTICLE_ON_DEATH_SPEED = 20
PARTICLE_ON_DEATH_COLOR_ADJUSTMENT = 50
CONFETTI_PARTICLE_SPEED = 100

EXPLOSION_PARTICLE_SPEED = 200
EXPLOSION_PARTICLE_RADIUS = 7
EXPLOSION_PARTICLE_THICKNESS = 2
EXPLOSION_PARTICLE_FADE = 0.49

WEAPON_SWAP_DELAY = 0.2

PISTOL_FIRE_RATE = 0.3
PISTOL_DAMAGE = 17.0
PISTOL_SHOOT_SPEED = 800
PISTOL_SHOT_RADIUS = 7
PISTOL_ACCURACY = 1
PISTOL_PELLETS = 1
PISTOL_AMMO_CAPACITY = 15
PISTOL_RELOAD = 2.2

SMG_FIRE_RATE = 0.05
SMG_DAMAGE = 6
SMG_SHOOT_SPEED = 450
SMG_SHOT_RADIUS = 1
SMG_ACCURACY = 23
SMG_PELLETS = 1
SMG_AMMO_CAPACITY = 22
SMG_RELOAD = 2.5

SHOTGUN_FIRE_RATE = 0.6
SHOTGUN_DAMAGE = 7
SHOTGUN_SHOOT_SPEED = 500
SHOTGUN_SHOT_RADIUS = 2
SHOTGUN_ACCURACY = 45
SHOTGUN_PELLETS = 5
SHOTGUN_AMMO_CAPACITY = 7
SHOTGUN_RELOAD = 2

TOWER_TIMER_LENGTH = 15
TOWER_TIMER_X_OFFSET = 32
TOWER_TIMER_Y_OFFSET = 50

GAME_DIRECTOR_SCREEN_SPAWN_CAP = 10
GAME_DIRECTOR_SCREEN_SPAWN_DIVIDING_FACTOR = 3
GAME_DIRECTOR_SPAWN_TIMER = 2
GAME_DIRECTOR_FONT_COLOR_END = (165,27,27)
GAME_DIRECTOR_END_OF_FONT_INTENSITY = 30

AUDIO_LOCATION_IMPACT = "Assets/Audio/impact.ogg"
AUDIO_LOCATION_LAZER_GUN = "Assets/Audio/laser-gun.ogg"
AUDIO_LOCATION_ALT_GUN = "Assets/Audio/alt-gun.ogg"

ANIMATION_DAMAGE_INDICATOR_TIME = 0.2
DAMAGE_COLOR_CHANGE_INTINSITY = 255

POCKET_MISSLE_RADIUS = 12
POCKET_MISSLE_SPEED = 560

SHIELD_COLOR = (0,255,255)

ACTION_TIME_LIMIT = 0.2
PAUSE_TEXT_X_OFFSET = 4
PAUSE_TEXT_Y_OFFSET = 7
PAUSE_ESC_TEXT_X_OFFSET = 2.3
PAUSE_ESC_TEXT_Y_OFFSET = 3.5

BACKGROUND_COLOR_DEFAULT = (35,43,43)

MOUSE_HITBOX = 30

ITEM_TEXT_BOX_CENTER_X = SCREEN_WIDTH / 2
ITEM_TEXT_BOX_CENTER_Y = SCREEN_HEIGHT / 2.4
ITEM_TEXT_BOX_HEIGHT = 50
ITEM_TEXT_BOX_WIDTH = 350
ITEM_TEXT_Y_OFFSET = 15

ITEM_BOX_WIDTH = 65
ITEM_BOX_HEIGHT = 65

TAB_REWARD_Y_OFFSET = 40
TAB_BOX_CENTER_X = SCREEN_WIDTH / 2
TAB_BOX_CENTER_Y = SCREEN_HEIGHT - TAB_REWARD_Y_OFFSET
TAB_BOX_WIDTH = 75
TAB_BOX_HEIGHT = 50
TAB_REWARD_FILL = 6
TAB_REWARD_SPEED = 20
TAB_REWARD_SCALE = 3

MAIN_MENU_FONT = 124
MAIN_MENU_FRONT_TEXT_Y_OFFSET = 176

BUTTON_HITBOX = 28
BUTTON_BOX_WIDTH = 55
BUTTON_BOX_HEIGHT = 35

TUTORIAL_TEXT_SIZE = 35
TUTORIAL_TEXT_Y_OFFSET = 100
TUTORIAL_TEXT_SECOND_LINE_Y_OFFSET = 50
TUTORIAL_STEP_DELAY = 1

TITLE_PULSE_SCALE = 27
TITLE_PULSE_SPEED = 1.5

MENU_COLOR_VALUE = 10
MENU_COLOR_SCALE = 10
MENU_COLOR_SPEED = 1.5
MENU_BACKROUND_DEFAULT_COLOR = (35,35,35)

SCORE_FILE = "XBT.XBT"

HIGH_SCORE_X_POS = SCREEN_WIDTH / 8.2
HIGH_SCORE_Y_POS = SCREEN_HEIGHT / 1.2
HIGH_SCORE_Y_OFFSET = 28

PLAYER_WEAPON_Y_OFFSET = -35