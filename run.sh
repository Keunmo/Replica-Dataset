# usage: ./run.sh <task> <scene_name>
if [ "$#" -ne 2 ]; then
    echo "Usage: ./run.sh <task> <scene_name>"
    exit 1
fi
if [[ $1 == "viewer" ]]; then
    echo "Running ReplicaViewer on $2";
    ./build/ReplicaSDK/ReplicaViewer ./replica_v1/$2/mesh.ply ./replica_v1/$2/textures/ ./replica_v1/$2/glass.sur
    exit 1
fi
if [[ $1 == "capture" ]]; then
    echo "Running ReplicaCapture on $2";
    # ./build/ReplicaSDK/ReplicaCapturer ./replica_v1/$2/mesh.ply ./replica_v1/$2/textures/ ./replica_v1/$2/glass.sur /home/keunmo/workspace/Replica-Dataset/output/$2
    ./build/ReplicaSDK/ReplicaCapturer ./replica_v1/$2/mesh.ply ./replica_v1/$2/textures/ /home/keunmo/workspace/Replica-Dataset/output/$2
    exit 1
fi
if [[ $1 == "render" ]]; then
    echo "Running ReplicaRender on $2";
    ./build/ReplicaSDK/ReplicaRenderer ./replica_v1/$2/mesh.ply ./replica_v1/$2/textures/ ./replica_v1/$2/glass.sur
    exit 1
fi
# echo "Running ReplicaViewer on $1";
# ./build/ReplicaSDK/ReplicaViewer ./replica_v1/$1/mesh.ply ./replica_v1/$1/textures/ ./replica_v1/$1/glass.sur