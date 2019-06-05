pwd 

mkdir ../just_tiles
git clone .git ../just_tiles
cd  ../just_tiles
git checkout ClassificationIN1.0
cd ../tile_for_classification


mkdir ../inception_with_results
git clone .git ../inception_with_results
cd  ../inception_with_results
git checkout ClassificationIN1.1
cd ../tile_for_classification

mkdir ../inception_overlay_tiles
git clone .git ../inception_overlay_tiles
cd  ../inception_overlay_tiles
git checkout ClassificationIN1.2
cd ../tile_for_classification

mkdir ../inception_overlay_tiles_and_four_points
git clone .git ../inception_overlay_tiles_and_four_points
cd  ../inception_overlay_tiles_and_four_points
git checkout ClassificationIN1.3
cd ../tile_for_classification

read -n1 -r -p "Press any key to continue..." key
