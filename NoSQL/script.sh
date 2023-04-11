# create virtual environment and activate the virtual environment
virtualenv -p /usr/bin/python2 venv
source venv/bin/activate

# clone the repo for benchmarking
git clone http://github.com/brianfrankcooper/YCSB.git
cd YCSB
mvn -pl site.ycsb:redis-binding -am clean package

cd ..

## Run the container for redis DB and run the tests
printf "\nRunning Benchmarks on redis DB, results can be found in the redis folder \n\n"
docker-compose -f redis/docker-compose.yml up --scale redis-master=1 --scale redis-replica=1 -d
cd YCSB
for i in {1..3}
do
printf "\n##################################################################################\n" >> ../redis/outputLoadRedis.csv
printf "Loading data worload A try $i \n" >> ../redis/outputLoadRedis.csv 
./bin/ycsb load redis -s -P workloads/workloada -p "redis.host=127.0.0.1" -p "redis.port=6379" -p "redis.clustert=true" >> ../redis/outputLoadRedis.csv
printf "\n##################################################################################\n" >> ../redis/outputRunRedis.csv
printf "Running test workoad A try $i\n" >> ../redis/outputRunRedis.csv
./bin/ycsb run redis -s -P workloads/workloada -p "redis.host=127.0.0.1" -p "redis.port=6379" -p "redis.clustert=true" >> ../redis/outputRunRedis.csv

printf "\n##################################################################################\n" >> ../redis/outputLoadRedis.csv 
printf " Loading data worload B try $i \n" >> ../redis/outputLoadRedis.csv 
./bin/ycsb load redis -s -P workloads/workloadb -p "redis.host=127.0.0.1" -p "redis.port=6379" -p "redis.clustert=true" >> ../redis/outputLoadRedis.csv
printf "\n##################################################################################\n" >> ../redis/outputRunRedis.csv
printf "Running test workoad B try $i\n" >> ../redis/outputRunRedis.csv
./bin/ycsb run redis -s -P workloads/workloadb -p "redis.host=127.0.0.1" -p "redis.port=6379" -p "redis.clustert=true" >> ../redis/outputRunRedis.csv

printf "\n##################################################################################\n" >> ../redis/outputLoadRedis.csv 
printf "Loading data worload C try $i\n" >> ../redis/outputLoadRedis.csv 
./bin/ycsb load redis -s -P workloads/workloadc -p "redis.host=127.0.0.1" -p "redis.port=6379" -p "redis.clustert=true" >> ../redis/outputLoadRedis.csv
printf "\n##################################################################################\n" >> ../redis/outputRunRedis.csv
printf "Running test workoad C try $i\n" >> ../redis/outputRunRedis.csv
./bin/ycsb run redis -s -P workloads/workloadc -p "redis.host=127.0.0.1" -p "redis.port=6379" -p "redis.clustert=true" >> ../redis/outputRunRedis.csv

printf "\n##################################################################################\n" >> ../redis/outputLoadRedis.csv 
printf "Loading data worload D  try $i\n" >> ../redis/outputLoadRedis.csv 
./bin/ycsb load redis -s -P workloads/workloadd -p "redis.host=127.0.0.1" -p "redis.port=6379" -p "redis.clustert=true" >> ../redis/outputLoadRedis.csv
printf "\n##################################################################################\n" >> ../redis/outputRunRedis.csv
printf "Running test workoad D try $i\n" >> ../redis/outputRunRedis.csv
./bin/ycsb run redis -s -P workloads/workloadd -p "redis.host=127.0.0.1" -p "redis.port=6379" -p "redis.clustert=true" >> ../redis/outputRunRedis.csv

printf "\n##################################################################################\n" >> ../redis/outputLoadRedis.csv
printf "Loading data worload E try $i\n" >> ../redis/outputLoadRedis.csv 
./bin/ycsb load redis -s -P workloads/workloade -p "redis.host=127.0.0.1" -p "redis.port=6379" -p "redis.clustert=true" >> ../redis/outputLoadRedis.csv
printf "\n##################################################################################\n" >> ../redis/outputRunRedis.csv
printf "Running test workoad E try $i\n" >> ../redis/outputRunRedis.csv
./bin/ycsb run redis -s -P workloads/workloade -p "redis.host=127.0.0.1" -p "redis.port=6379" -p "redis.clustert=true" >> ../redis/outputRunRedis.csv

printf "\n##################################################################################\n" >> ../redis/outputLoadRedis.csv
printf "Loading data worload F try $i\n" >> ../redis/outputLoadRedis.csv 
./bin/ycsb load redis -s -P workloads/workloadf -p "redis.host=127.0.0.1" -p "redis.port=6379" -p "redis.clustert=true" >> ../redis/outputLoadRedis.csv
printf "\n##################################################################################\n" >> ../redis/outputRunRedis.csv
printf "Running test workoad F try $i\n" >> ../redis/outputRunRedis.csv
./bin/ycsb run redis -s -P workloads/workloadf -p "redis.host=127.0.0.1" -p "redis.port=6379" -p "redis.clustert=true" >> ../redis/outputRunRedis.csv
done
cd ..
docker-compose -f redis/docker-compose.yml down -v
printf "\nFinished benchmarking redis DB \n\n"

## Cleaning up everything
deactivate
rm -rf YCSB
rm -rf venv
