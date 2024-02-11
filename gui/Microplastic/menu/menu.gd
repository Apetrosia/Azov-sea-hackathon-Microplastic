extends Control


func _on_upload_pressed():
	get_tree().change_scene_to_file("res://upload/upload_menu.tscn")


func _on_saved_photos_pressed():
	get_tree().change_scene_to_file("res://archive/archive.tscn")
