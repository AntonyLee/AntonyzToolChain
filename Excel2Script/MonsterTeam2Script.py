#coding=utf-8
import os;
import xlrd;
import lxml;

mt_data_col = {
	"stage_name" : 2,
	"team_id" : 1,
	"target_name" : 4,
	"target_id" : 5,
	"mt_monster_id" : 6,
	"mt_monster_level" : 7,
	"mt_monster_pos" : 8,
	"mt_is_stage_boss" : 9,
}

mt_start_row = 2;

class MonsterEntry():
	_template_id = 0;
	_level = 0;
	_pos = 0;
	_is_stage_boss = False;

	def __str__(self):
		return "MonsterTemplate:%d Level:%d Pos:%d"%(int(self._template_id), int(self._level), int(self._pos));


class MonsterTeamEntry():
	_team_id = 0;
	_monsters = [];

	def __init__(self):
		_monsters = [];

	def __str__(self):
		string = "Team Id: " + str(self._team_id)+ "\n";
		for m in self._monsters:
			string += str(m) + "\n";
		return string;

def _UNI2I(obj):
	if isinstance(obj, unicode):
		obj = obj.encode('utf-8');
	if isinstance(obj, str):
		obj = 0;
	obj = int(obj);
	return obj;

def collectMonsterTeamData(workbook):
	worksheet = workbook.sheet_by_index(0);
	mte_list = [];

	mte = None;
	for rowx in range(mt_start_row, worksheet.nrows):
		team_id = _UNI2I(worksheet.cell(rowx, mt_data_col["team_id"]).value);

		if not 0 == team_id:
			mte = MonsterTeamEntry();
			mte._monsters = [];
			mte._team_id = team_id;
			mte_list.append(mte);


		me = MonsterEntry();
		me._template_id = _UNI2I(worksheet.cell(rowx, mt_data_col["mt_monster_id"]).value);
		me._level  		= _UNI2I(worksheet.cell(rowx, mt_data_col["mt_monster_level"]).value);
		me._pos 		= _UNI2I(worksheet.cell(rowx, mt_data_col["mt_monster_pos"]).value);
		mte._monsters.append(me);	

def writeMonsterTeamScript(mt_list):
