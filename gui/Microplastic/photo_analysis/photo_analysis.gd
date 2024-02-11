extends Control

@onready var scroll_container = $ColorRect/MarginContainer/ScrollContainer
@onready var photo_name_label = $ColorRect/MarginContainer/ScrollContainer/Info/Name
@onready var photo = $ColorRect/MarginContainer/ScrollContainer/Info/Photo
@onready var histogram_photo = $ColorRect/MarginContainer/ScrollContainer/Info/HistogramPhoto
@onready var colors = $ColorRect/MarginContainer/ScrollContainer/Info/Colors

var DIR = OS.get_executable_path().get_base_dir()
var csv_path
var photo_path
var histogram_path


func _ready():
	var photo_name = CurrentFile.cur_file
	if !OS.has_feature("standalone"): # if NOT exported version
		csv_path = ProjectSettings.globalize_path("res://PythonFiles/PhotosInfo/"+ photo_name + "/info.csv")
		photo_path = ProjectSettings.globalize_path("res://PythonFiles/PhotosInfo/" + photo_name + "/" + photo_name)
		histogram_path = ProjectSettings.globalize_path("res://PythonFiles/PhotosInfo/"+ photo_name + "/histogram.png")
		
		photo_name_label.text = photo_name
		
		var image_photo = Image.new()
		image_photo.load(photo_path)
		photo.texture = ImageTexture.create_from_image(image_photo)
		#var image_histogram = Image.new()
		#image_histogram.load(histogram_path)
		#histogram_photo.texture = ImageTexture.create_from_image(image_histogram)
	else:
		csv_path = DIR.path_join("PythonFiles/PhotosInfo/" + photo_name + "/info.csv")
		photo_path = DIR.path_join("PythonFiles/PhotosInfo/" + photo_name + "/" + photo_name)
		histogram_path = DIR.path_join("PythonFiles/PhotosInfo/"+ photo_name + "/histogram.png")
		
		photo_name_label.text = photo_name
		
		var image_photo = Image.new()
		image_photo.load(photo_path)
		photo.texture = ImageTexture.create_from_image(image_photo)
		#var image_histogram = Image.new()
		#image_histogram.load(histogram_path)
		#histogram_photo.texture = ImageTexture.create_from_image(image_histogram)


func _input(event):
	if event.is_action_pressed("back"):
		get_tree().change_scene_to_file("res://archive/archive.tscn")


func _on_back_pressed():
	get_tree().change_scene_to_file("res://archive/archive.tscn")
