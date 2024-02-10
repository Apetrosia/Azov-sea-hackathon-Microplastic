extends Control

@onready var item_list = $ColorRect/MarginContainer/ScrollContainer/ItemList

var DIR = OS.get_executable_path().get_base_dir()


func _ready():
	if !OS.has_feature("standalone"): # if NOT exported version
		var dir_access: DirAccess = DirAccess.open(ProjectSettings.globalize_path("res://PythonFiles/PhotosInfo"))
		for photo_name in dir_access.get_directories():
			var image = Image.load_from_file(ProjectSettings.globalize_path("res://PythonFiles/PhotosInfo/" + photo_name + "/" + photo_name))
			var texture = ImageTexture.create_from_image(image)
			item_list.add_item(photo_name, texture)
	else:
		var dir_access: DirAccess = DirAccess.open(DIR.path_join("PythonFiles/PhotosInfo/"))
		for photo_name in dir_access.get_directories():
			var image = Image.load_from_file(DIR.path_join("PythonFiles/PhotosInfo/" + photo_name + "/" + photo_name))
			var texture = ImageTexture.create_from_image(image)
			item_list.add_item(photo_name, texture)



func _input(event):
	if event.is_action_pressed("back"):
		get_tree().change_scene_to_file("res://menu/menu.tscn")


func _on_back_pressed():
	get_tree().change_scene_to_file("res://menu/menu.tscn")


func _on_item_list_item_clicked(index, at_position, mouse_button_index):
	CurrentFile.cur_file = item_list.get_item_text(index)
	get_tree().change_scene_to_file("res://photo_analysis/photo_analysis.tscn")
