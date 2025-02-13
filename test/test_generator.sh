if [ -d ".venv" ]; then
    echo "Le dossier .venv existe."
    source .venv/bin/activate
else
    echo "Le dossier .venv n'existe pas."
    python3 -m venv .venv
    source .venv/bin/activate
fi

pip install -r requirements.txt

for year in 2022 2023 2024
do
    for week in {1..2}
    do
        python3 src/generator.py $year $week
    done
done
