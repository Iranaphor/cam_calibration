path=$(dirname $0)/..
new_name=$1

echo $path
echo $new_name

if [ -n "$new_name" ] ; then

    mv $path/ros2_template $path/$new_name
    mv $path/resource/ros2_template $path/resource/$new_name

    sed -i "s/ros2_template/$new_name/g" $path/setup.py
    sed -i "s/ros2_template/$new_name/g" $path/setup.cfg
    sed -i "s/ros2_template/$new_name/g" $path/README.md
    sed -i "s/ros2_template/$new_name/g" $path/package.xml
    sed -i "s/ros2_template/$new_name/g" $path/CMakeLists.txt

fi
