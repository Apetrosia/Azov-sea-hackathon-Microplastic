extends Control

@onready var file_dialog = $FileDialog
@onready var upload = $ColorRect/MarginContainer/VBoxContainer/Upload
#@onready var picture = $ColorRect/MarginContainer/VBoxContainer/Picture


func _on_upload_pressed():
	file_dialog.show()


func _on_file_dialog_file_selected(path):
	var image = Image.new()
	image.load(path)
	#picture.texture = ImageTexture.create_from_image(image)


func _on_saved_photos_pressed():
	get_tree().change_scene_to_file("res://archive/archive.tscn")
