input_image="image6.jpg"
output_image="framed_image.jpg"
overlay_image="Untitled.png"
overlay_edit="Untitled2.png"

black_frame_width=30
white_frame_width=100
gap=20

convert $overlay_image -resize 120% $overlay_edit

convert $input_image -bordercolor black -border ${black_frame_width} \
-bordercolor white -border ${white_frame_width} \
-bordercolor none -border ${gap} $output_image

convert $output_image $overlay_edit -geometry +0+30 -gravity south -composite $output_image

convert $output_image -modulate 110,102,100 -sharpen 0x1.0 $output_image
