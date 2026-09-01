import mods.gamestages.StageHelper;

// Level 1 is the starting state, not an unlock. Grant it to every player on join
// so new and existing saves always have access to the baseline progression tier.
StageHelper.grantStageOnJoin("level_1");
