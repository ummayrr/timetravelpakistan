image_dir="downloads"
output_dir="edited"

mkdir -p "$output_dir"
rm -f "$output_dir"/*.*

black_frame_width=30
white_frame_width=100
gap=20

is_black="true"

for input_image in "$image_dir"/*.*; do
    base_name=$(basename "$input_image")
    output_image="$output_dir/${base_name%.*}"_edited."${base_name##*.}"

    if [ "$is_black" = "true" ]; then
        # Black edit
        overlay_image="assets/black/onthisday.png"
        overlay_edit="assets/black/onthisdayedit.png"
        corner_image1="assets/black/bottom_left_corner_mask.png"
        corner_image2="assets/black/top_right_corner_mask.png"
        corner_image3="assets/black/top_left_corner_mask.png"
        corner_image4="assets/black/bottom_right_corner_mask.png"
        corner_image1edit="assets/black/corner_image1edit.png"
        corner_image2edit="assets/black/corner_image2edit.png"
        corner_image3edit="assets/black/corner_image3edit.png"
        corner_image4edit="assets/black/corner_image4edit.png"
        moon="assets/black/moon.png"
        moonedit="assets/black/moonedit.png"
        mooneditrotated="assets/black/mooneditrotated.png"
        title="assets/black/timetravelpakistan.jpg"
        titleedit="assets/black/timetravelpakistanedit.png"

        convert "$input_image" -bordercolor white -border ${black_frame_width} \
        -bordercolor black -border ${white_frame_width} \
        -bordercolor white -border ${gap} "$output_image"

    else
        # White edit
        overlay_image="assets/white/onthisday.png"
        overlay_edit="assets/white/onthisdayedit.png"
        corner_image1="assets/white/bottom_left_corner_mask.png"
        corner_image2="assets/white/top_right_corner_mask.png"
        corner_image3="assets/white/top_left_corner_mask.png"
        corner_image4="assets/white/bottom_right_corner_mask.png"
        corner_image1edit="assets/white/corner_image1edit.png"
        corner_image2edit="assets/white/corner_image2edit.png"
        corner_image3edit="assets/white/corner_image3edit.png"
        corner_image4edit="assets/white/corner_image4edit.png"
        moon="assets/white/moon.png"
        moonedit="assets/white/moonedit.png"
        mooneditrotated="assets/white/mooneditrotated.png"
        title="assets/white/timetravelpakistan.jpg"
        titleedit="assets/white/timetravelpakistanedit.png"

        convert "$input_image" -bordercolor black -border ${black_frame_width} \
        -bordercolor white -border ${white_frame_width} \
        -bordercolor black -border ${gap} "$output_image"

    fi

    convert $overlay_image -resize 120% $overlay_edit
    convert $title -resize 120% $titleedit
    convert $corner_image1 -resize 210% $corner_image1edit
    convert $corner_image2 -resize 210% $corner_image2edit
    convert $corner_image3 -resize 210% $corner_image3edit
    convert $corner_image4 -resize 210% $corner_image4edit
    convert $moon -resize 20% $moonedit

    convert "$output_image" "$overlay_edit" -geometry +30+30 -gravity south -composite "$output_image"
    convert "$output_image" "$titleedit" -geometry +0+30 -gravity north -composite "$output_image"
    convert "$output_image" -modulate 110,102,100 -sharpen 0x1.0 "$output_image"

    convert "$output_image" "$corner_image1edit" -geometry +80+118 -gravity southwest -composite "$output_image"
    convert "$output_image" "$corner_image2edit" -geometry +80+118 -gravity northeast -composite "$output_image"
    convert "$output_image" "$corner_image3edit" -geometry +80+118 -gravity northwest -composite "$output_image"
    convert "$output_image" "$corner_image4edit" -geometry +80+118 -gravity southeast -composite "$output_image"
    convert "$output_image" "$moonedit" -geometry +35+30 -gravity southwest -composite "$output_image"

    convert "$moonedit" -background none -rotate -90 "$mooneditrotated"
    convert "$output_image" "$mooneditrotated" -geometry +35+30 -gravity southeast -composite "$output_image"
    convert "$moonedit" -background none -rotate 180 "$mooneditrotated"
    convert "$output_image" "$mooneditrotated" -geometry +35+30 -gravity northeast -composite "$output_image"
    convert "$moonedit" -background none -rotate 45 "$mooneditrotated"
    convert "$output_image" "$mooneditrotated" -geometry +10+10 -gravity northwest -composite "$output_image"

    if [ "$is_black" = "true" ]; then
        is_black="false"
else
        is_black="true"
fi

done

for edited_image in "$output_dir"/*.*; do
    base_name=$(basename "$edited_image")
    output_jpg="$output_dir/${base_name%.*}".jpg

    convert "$edited_image" "$output_jpg"
done

for edited_image in "$output_dir"/*.*; do
    if [[ "$edited_image" != *.jpg ]]; then
        rm "$edited_image"
    fi
done

rm -f "$image_dir"/*.*
