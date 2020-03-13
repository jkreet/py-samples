PROJECT_NAME=$1
PROJECT_REPO=$2

echo "Build start"
cd ~
echo "pwd to homedir"

if [ ! -d $PROJECT_NAME ] || [ ! -d $PROJECT_NAME/.git ]
then
    echo "Directory $PROJECT_NAME does not exists"
    git clone $PROJECT_REPO
else
    echo "Directory $PROJECT_NAME exists"
    cd ~/$PROJECT_NAME
    git pull
fi

docker build -t $PROJECT_NAME .