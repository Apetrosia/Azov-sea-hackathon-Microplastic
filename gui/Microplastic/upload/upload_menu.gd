extends Control

@onready var file_dialog = $FileDialog
@onready var place = $ColorRect/MarginContainer/VBoxContainer/Place
@onready var time = $ColorRect/MarginContainer/VBoxContainer/Time

var DIR = OS.get_executable_path().get_base_dir()


func _on_upload_pressed():
	file_dialog.show()


func _on_back_pressed():
	get_tree().change_scene_to_file("res://menu/menu.tscn")


func _on_file_dialog_file_selected(path):
	var photo_name = path.get_file()
	CurrentFile.cur_file = photo_name
	
	if !OS.has_feature("standalone"): # if NOT exported version
		var dir = DirAccess.open("res://PythonFiles/PhotosInfo")
		dir.make_dir(photo_name)
		dir.copy(path, "res://PythonFiles/PhotosInfo/" + photo_name + "/" + photo_name);
		var file = FileAccess.open("res://PythonFiles/PhotosInfo/" + photo_name + "/time_and_place.txt", FileAccess.WRITE)
		file.store_line(place.text + "    " + time.text)
		OS.execute(ProjectSettings.globalize_path("res://PythonFiles/find_microplastic.exe"), [photo_name], [], true, true)
	else:
		var dir = DirAccess.open(DIR.path_join("PythonFiles/PhotosInfo/"))
		dir.make_dir(photo_name)
		dir.copy(path, DIR.path_join("PythonFiles/PhotosInfo/") + photo_name + "/" + photo_name);
		var file = FileAccess.open(DIR.path_join("PythonFiles/PhotosInfo/") + photo_name + "/time_and_place.txt", FileAccess.WRITE)
		file.store_line(place.text + "    " + time.text)
		OS.create_process(DIR.path_join("PythonFiles/find_microplastic.exe"), [photo_name])
	
	
	get_tree().change_scene_to_file("res://photo_analysis/photo_analysis.tscn")


