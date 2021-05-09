set +x
ps aux | grep app.py | grep -iv grep | awk '{print $2}' | xargs sudo kill -9
mkdir -p logs
if [ ! -d venv ]; then 
    python3 -m venv venv
    
fi
source venv/bin/activate
pip install -r requirements.txt
 
python app.py > logs/error.log 2>&1 &