if [ -d ".venv" ]; then
    echo "virtualenv does exist."
    source .venv/bin/activate
else
    echo "virtualenv does not exist. Creating..."
    python3 -m venv .venv
    source .venv/bin/activate
fi

echo "Downloading requirements..."
pip install -r requirements.txt

# for year in 2022 2023 2024
# do
#     for week in {1..2}
#     do
#         echo "Generating week $week of year $year..."
#         python3 src/generator.py $year $week
#     done
# done

for year in 2025
do
    for week in {1..6}
    do
        echo "Generating week $week of year $year..."
        python3 src/generator.py $year $week
    done
done
